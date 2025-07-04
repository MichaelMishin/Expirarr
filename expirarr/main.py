import sys
import os
import time
import yaml
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from maintainerr_integration import process_collections
from ahti_the_janitor import cleanup_temp_files, reset_processed_data, validate_config

def load_config():
    with open("config/config.yaml", "r") as file:
        return yaml.safe_load(file)

def parse_cron_schedule(cron_schedule):
    # Parse the cron string into a dictionary for APScheduler
    fields = cron_schedule.split()
    return {
        "minute": fields[0],
        "hour": fields[1],
        "day": fields[2],
        "month": fields[3],
        "day_of_week": fields[4]
    }

scheduler = None
cron_job = None

def scheduled_task():
    if validate_config(load_config()):
        print("\n" + "="*41)
        print(">>> TASK STARTED: {} <<<".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        print("="*41)
        # run cleanup tasks
        cleanup_temp_files()
        reset_processed_data()

        # process collections using Maintainerr API
        process_collections()
        print("-"*41)
        print(">>> TASK COMPLETED <<<")
        print("-"*41)
        # Notify user of next run time
        if scheduler:
            jobs = scheduler.get_jobs()
            if jobs:
                next_run = jobs[0].next_run_time
                if next_run:
                    print(f"Next scheduled run at: {next_run.strftime('%Y-%m-%d %H:%M:%S')}")

def main():
    global scheduler, cron_job
    print("Starting Expirarr with cron scheduling...")
    config = load_config()
    cron_schedule = config.get("cron_schedule", "0 0-23/12 * * *")

    # Run once on start if enabled in config
    if config.get("run_on_start", False):
        print("run_on_start is enabled. Running scheduled task immediately.")
        scheduled_task()

    scheduler = BlockingScheduler()

    # Schedule the task using the cron pattern from the config
    cron_job = scheduler.add_job(scheduled_task, 'cron', **parse_cron_schedule(cron_schedule))

    # Print first scheduled run
    next_run = cron_job.trigger.get_next_fire_time(None, datetime.datetime.now())
    if next_run:
        print(f"Next scheduled run at: {next_run.strftime('%Y-%m-%d %H:%M:%S')}")

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("Scheduler stopped.")

if __name__ == "__main__":
    main()
