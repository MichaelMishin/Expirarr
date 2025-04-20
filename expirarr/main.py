import sys
import os
import time
import yaml
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from maintainerr_integration import process_collections
from ahti_the_janitor import cleanup_temp_files, reset_processed_data

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

def scheduled_task():
    print("\n--- Task triggered: {} ---".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    # run cleanup tasks
    cleanup_temp_files()
    reset_processed_data()

    # process collections using Maintainerr API
    process_collections()
    print("Processing completed.")

def main():
    print("Starting Expirarr with cron scheduling...")
    config = load_config()
    cron_schedule = config.get("cron_schedule", "0 0-23/12 * * *")

    scheduler = BlockingScheduler()

    # Schedule the task using the cron pattern from the config
    scheduler.add_job(scheduled_task, 'cron', **parse_cron_schedule(cron_schedule))

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("Scheduler stopped.")

if __name__ == "__main__":
    main()
