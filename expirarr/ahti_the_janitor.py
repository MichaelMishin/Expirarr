import os
import json
import requests
import yaml
import re
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
    Deletes all files in the temporary posters directory and its test subdirectory.
    """
    if TEMP_DIR.exists():
        for file in TEMP_DIR.iterdir():
            if file.is_file():
                print(f"Deleting temporary file: {file}")
                file.unlink()
            elif file.is_dir() and file.name == "test":
                for test_file in file.iterdir():
                    if test_file.is_file():
                        print(f"Deleting test file: {test_file}")
                        test_file.unlink()

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

def validate_config(config):
    """
    Validates the config file for required fields and correct URL/token formats.
    Returns True if valid, False otherwise.
    """
    errors = []

    # Check Plex config
    plex = config.get("plex", {})
    plex_url = plex.get("url", "")
    plex_token = plex.get("token", "")

    # Simple URL validation
    url_pattern = re.compile(r"^https?://[^\s/$.?#].[^\s]*$")
    if not plex_url or not url_pattern.match(plex_url):
        errors.append("Invalid or missing Plex URL.")

    # check for a valid IP address in the URL (example http://192.168.0.1:32400)
    ip_pattern = re.compile(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b")
    if not ip_pattern.search(plex_url): 
        errors.append("Plex URL should contain a valid IP address.")

    if not plex_token or plex_token == "your_token_here":
        errors.append("Missing or placeholder Plex token.")

    # Check Maintainerr config
    maintainerr = config.get("maintainerr", {})
    maintainerr_url = maintainerr.get("url", "")
    maintainerr_api_key = maintainerr.get("api_key", "")

    if not maintainerr_url or not url_pattern.match(maintainerr_url):
        errors.append("Invalid or missing Maintainerr URL.")

    if not ip_pattern.search(maintainerr_url):
        errors.append("Maintainerr URL should contain a valid IP address.")

    if not maintainerr_api_key or maintainerr_api_key == "your_api_key_here":
        errors.append("Missing or placeholder Maintainerr API key.")

    if errors:
        print("Config validation errors:")
        for err in errors:
            print(f"  - {err}")
        return False

    print("Config file validated successfully.")
    return True

if __name__ == "__main__":
    print("Running cleanup tasks...")
    cleanup_temp_files()
    reset_processed_data()
    print("Cleanup completed.")
