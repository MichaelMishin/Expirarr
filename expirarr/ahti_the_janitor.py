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
    all_collections = response.json()

    if TEST_MODE:
        print("Maintainerr API response:")
        print(all_collections)
    
    return [c for c in all_collections if c.get("deleteAfterDays")]

def validate_processed_data():
    """
    Updates the processed.json file by removing entries not in the Maintainerr collections.
    """
    processed_posters = load_processed_posters()
    maintainerr_collections = get_maintainerr_collections()

    # Remove entries not in Maintainerr collections
    updated_processed = {k: v for k, v in processed_posters.items() if k in maintainerr_collections}
    
    # Save the updated processed data
    save_processed_posters(updated_processed)


if __name__ == "__main__":
    print("Running cleanup tasks...")
    cleanup_temp_files()
    validate_processed_data()
    print("Cleanup completed.")
