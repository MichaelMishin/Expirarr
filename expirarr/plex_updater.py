from plexapi.server import PlexServer
from pathlib import Path
import yaml
import os

def get_config():
    config_path = os.getenv("CONFIG_PATH", "./config/config.yaml")
    with open(config_path, "r") as config_file:
        return yaml.safe_load(config_file)

def get_plex_server():
    config = get_config()
    baseurl = config["plex"]["url"]
    token = config["plex"]["token"]
    print(f"Connecting to Plex server at {baseurl}")
    return PlexServer(baseurl, token)

def upload_poster(media, poster_path: Path):
    if not poster_path.exists():
        print(f"    Error: Poster file does not exist at {poster_path}")
        return

    if poster_path.suffix.lower() not in [".jpg", ".jpeg", ".png"]:
        print(f"    Error: Unsupported file format for {poster_path}. Supported formats are .jpg, .jpeg, .png")
        return

    resolved_path = poster_path.resolve()
    print(f"    Uploading poster to Plex for: {media.title} from {resolved_path}")
    try:
        # Pass the resolved file path directly as a string
        val = media.uploadPoster(filepath=poster_path)
        print(f"    Upload complete for: {media.title}")
    except Exception as e:
        print(f"    Failed to upload poster for {media.title}: {e}")

