import os
import requests
from dotenv import load_dotenv
from pathlib import Path
from editor import add_leaving_soon_badge
from downloader import download_image  # now imported from downloader.py
from plex_updater import get_plex_server

# Load environment variables from .env file
load_dotenv()

PLEX_URL = os.getenv("PLEX_URL")
MAINTAINERR_URL = os.getenv("MAINTAINERR_URL")
MAINTAINERR_API_KEY = os.getenv("MAINTAINERR_API_KEY")
PLEX_TOKEN = os.getenv("PLEX_TOKEN")
TEMP_DIR = Path("/tmp/lastcallposters")
TEMP_DIR.mkdir(parents=True, exist_ok=True)
TEMP_TEST_DIR = TEMP_DIR / "test"
TEMP_TEST_DIR.mkdir(parents=True, exist_ok=True)
TEST_MODE = os.getenv("TEST_MODE", "true").lower() == "true"

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
        collection_plex_id = col.get("plexId")  # Use plexId for the collection
        media_items = col.get("media", [])  # Get the media items in the collection

        print(f"Processing collection: {title} ({collection_plex_id})")

        for media in media_items:
            media_plex_id = media.get("plexId")  # Use plexId for media items

            try:
                # Fetch media details from Plex API using plexId
                media_details = plex.fetchItem(media_plex_id)
                media_title = media_details.title
                url = f"{PLEX_URL}/library/metadata/{media_plex_id}/thumb?X-Plex-Token={plex._token}"  # Construct the URL using media's plexId

                print(f"  Processing media: {media_title} ({media_plex_id})")

                if TEST_MODE:
                    image_path = TEMP_TEST_DIR / f"{media_plex_id}_original.png"  # Save as {media_plex_id}_original.png
                    edited_path = TEMP_TEST_DIR / f"{media_plex_id}_edited.png"
                else:
                    image_path = TEMP_DIR / f"{media_plex_id}_original.png"  # Save as {media_plex_id}_original.png
                    edited_path = TEMP_DIR / f"{media_plex_id}_edited.png"

                download_image(url, image_path)  # Pass the Plex URL to download_image
                add_leaving_soon_badge(image_path, edited_path)

                if not TEST_MODE:
                    # TODO: Upload back to Plex using plex_updater
                    pass

            except Exception as e:
                print(f"    Failed processing media {media_plex_id}: {e}")

if __name__ == "__main__":
    process_collections()
