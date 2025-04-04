from plexapi.server import PlexServer
from pathlib import Path
import os

def get_plex_server():
    baseurl = os.getenv("PLEX_URL")
    token = os.getenv("PLEX_TOKEN")
    print(f"Connecting to Plex server at {baseurl}")
    return PlexServer(baseurl, token)

def upload_poster(media, poster_path: Path):
    print(f"Uploading poster to Plex for: {media.title}")
    media.uploadPoster(str(poster_path))
    print(f"Upload complete for: {media.title}")

