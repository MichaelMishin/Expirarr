import requests
from pathlib import Path

def download_image(url: str, save_path: Path) -> Path:
    print(f"Downloading image from: {url}")
    response = requests.get(url)
    response.raise_for_status()
    with open(save_path, 'wb') as f:
        f.write(response.content)
    print(f"Image saved to: {save_path}")
    return save_path

