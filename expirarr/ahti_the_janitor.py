import os
import json
import requests
import yaml
from pathlib import Path

def get_config():
    config_path = os.getenv("CONFIG_PATH", "./config/config.yaml")
    with open(config_path, "r") as config_file:
        return yaml.safe_load(config_file)

config = get_config()

TEMP_DIR = Path("/app/data/posters")
PROCESSED_FILE = Path("/app/data/processed.json")
MAINTAINERR_URL = config["maintainerr"]["url"]
MAINTAINERR_API_KEY = config["maintainerr"]["api_key"]
TEST_MODE = config.get("test_mode", False)

PROCESSED_FILE = Path("/app/data/processed.json")
PROCESSED_FILE.parent.mkdir(parents=True, exist_ok=True)

HEADERS = {
    "Authorization": f"Bearer {MAINTAINERR_API_KEY}"
}

def load_processed_posters():
    if PROCESSED_FILE.exists():
        with open(PROCESSED_FILE, "r") as file:
            return json.load(file)
    return {}

def save_processed_posters(processed):
    with open(PROCESSED_FILE, "w") as file:
        json.dump(processed, file, indent=4)

def cleanup_temp_files():
    """
    Deletes all files in the temporary posters directory.
    """
    if TEMP_DIR.exists():
        for file in TEMP_DIR.iterdir():
            if file.is_file():
                print(f"Deleting temporary file: {file}")
                file.unlink()

def get_maintainerr_collections():
    """
    Fetches the list of collections from Maintainerr.
    """
    url = f"{MAINTAINERR_URL}/api/collections"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    collections = response.json()
    return collections  # Return the full collection data instead of just plexId values

def reset_processed_data():
    """
    Updates the processed.json file by removing entries not in the Maintainerr collections (already removed from the system).
    """
    if PROCESSED_FILE.exists():
        print(f"Checking processed data file: {PROCESSED_FILE}")
        with PROCESSED_FILE.open("r") as file:
            try:
                processed_data = json.load(file)
            except json.JSONDecodeError:
                print("Processed data file is not a valid JSON. Resetting...")
                processed_data = {}

        maintainerr_collections = get_maintainerr_collections()
        maintainerr_media_ids = {
            str(item["plexId"]) for collection in maintainerr_collections for item in collection.get("media", [])
        }
        updated_data = {
            key: value for key, value in processed_data.items() if key in maintainerr_media_ids
        }

        with PROCESSED_FILE.open("w") as file:
            json.dump(updated_data, file, indent=4)
        print(f"Updated processed data file: {PROCESSED_FILE}")
    else:
        print(f"No processed data file found at: {PROCESSED_FILE}")

if __name__ == "__main__":
    print("Running cleanup tasks...")
    cleanup_temp_files()
    reset_processed_data()
    print("Cleanup completed.")
