from plexapi.server import PlexServer
from pathlib import Path
import yaml
import os

def get_config():
    config_path = os.getenv("CONFIG_PATH", "/app/config.yaml")
    with open(config_path, "r") as config_file:
        return yaml.safe_load(config_file)

def get_plex_server():
    config = get_config()
    baseurl = config["plex"]["url"]
    token = config["plex"]["token"]
    print(f"Connecting to Plex server at {baseurl}")
    return PlexServer(baseurl, token)

def upload_poster(media, poster_path: Path):
    print(f"Uploading poster to Plex for: {media.title}")
    media.uploadPoster(str(poster_path))
    print(f"Upload complete for: {media.title}")

