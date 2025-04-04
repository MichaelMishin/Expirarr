import os
import requests
import yaml
from dotenv import load_dotenv
from pathlib import Path
from editor import add_leaving_soon_badge
from downloader import download_image  # now imported from downloader.py
from plex_updater import get_plex_server

def get_config():
    config_path = os.getenv("CONFIG_PATH", "/app/config.yaml")
    with open(config_path, "r") as config_file:
        return yaml.safe_load(config_file)

config = get_config()

PLEX_URL = config["plex"]["url"]
MAINTAINERR_URL = config["maintainerr"]["url"]
MAINTAINERR_API_KEY = config["maintainerr"]["api_key"]
TEST_MODE = config.get("test_mode", False)

TEMP_DIR = Path("/tmp/lastcallposters")
TEMP_DIR.mkdir(parents=True, exist_ok=True)
TEMP_TEST_DIR = TEMP_DIR / "test"
TEMP_TEST_DIR.mkdir(parents=True, exist_ok=True)

HEADERS = {
    "Authorization": f"Bearer {MAINTAINERR_API_KEY}"
}

def get_collections_with_delete_timer():
    url = f"{MAINTAINERR_URL}/api/collections"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    all_collections = response.json()

    if TEST_MODE:
        print("Maintainerr API response:")
        print(all_collections)
    
    return [c for c in all_collections if c.get("deleteAfterDays")]

def process_collections():
    collections = get_collections_with_delete_timer()
    for col in collections:
        plex = get_plex_server()
        title = col.get("title")
        collection_plex_id = col.get("plexId")
        media_items = col.get("media", [])
        delete_after_days = col.get("deleteAfterDays")  # Retrieve deleteAfterDays from the collection

        print(f"Processing collection: {title} ({collection_plex_id})")

        for media in media_items:
            media_plex_id = media.get("plexId")
            add_date = media.get("addDate")
            
            try:
                # Fetch media details from Plex API using plexId
                media_details = plex.fetchItem(media_plex_id)
                media_title = media_details.title
                url = f"{PLEX_URL}/library/metadata/{media_plex_id}/thumb?X-Plex-Token={plex._token}"

                print(f"  Processing media: {media_title} ({media_plex_id})")

                if TEST_MODE:
                    image_path = TEMP_TEST_DIR / f"{media_plex_id}_original.png"
                    edited_path = TEMP_TEST_DIR / f"{media_plex_id}_edited.png"
                else:
                    image_path = TEMP_DIR / f"{media_plex_id}_original.png"
                    edited_path = TEMP_DIR / f"{media_plex_id}_edited.png"

                download_image(url, image_path)
                add_leaving_soon_badge(image_path, edited_path, add_date, delete_after_days)

                if not TEST_MODE:
                    # TODO: Upload back to Plex using plex_updater
                    pass

            except Exception as e:
                print(f"    Failed processing media {media_plex_id}: {e}")

if __name__ == "__main__":
    process_collections()
