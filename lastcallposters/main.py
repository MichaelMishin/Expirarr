import os
import shutil
from dotenv import load_dotenv
from pathlib import Path
from lastcallposters.downloader import download_image
from lastcallposters.editor import add_leaving_soon_badge
from lastcallposters.plex_updater import get_plex_server, upload_poster

TEMP_DIR = Path("/tmp/lastcallposters")
TEMP_DIR.mkdir(parents=True, exist_ok=True)
TEMP_TEST_DIR = TEMP_DIR / "test"
TEMP_TEST_DIR.mkdir(parents=True, exist_ok=True)

def clean_test_folder():
    """Clean the test folder by deleting all existing test files."""
    for file in TEMP_TEST_DIR.iterdir():
        try:
            if file.is_file():
                print(f"Deleting test file: {file}")
                file.unlink()  # Delete file
            else:
                shutil.rmtree(file)  # Remove directories if any
        except Exception as e:
            print(f"Error deleting file {file}: {e}")


def main():
    print("Loading environment variables...")
    load_dotenv()
    plex = get_plex_server()
    library_name = os.getenv("LIBRARY_NAME")
    test_mode = os.getenv("TEST_MODE", "true").lower() == "true"
    print(f"Test mode is {'ON' if test_mode else 'OFF'}")
    print(f"Accessing Plex library: {library_name}")
    
    # Clean the test folder if test_mode is on
    if test_mode:
        print(f"Cleaning the test folder at {TEMP_TEST_DIR}")
        clean_test_folder()

    for show in plex.library.section(library_name).all():
        print(f"Processing: {show.title}")

        if not show.thumb:
            print(f"No thumbnail found for: {show.title}, skipping.")
            continue

        img_url = plex.url(show.thumb) + "?X-Plex-Token=" + plex._token
        print(f"Image URL: {img_url}")
        original_path = TEMP_DIR / f"{show.ratingKey}_original.jpg"
        edited_path = TEMP_DIR / f"{show.ratingKey}_edited.png"

        try:
            download_image(img_url, original_path)
            add_leaving_soon_badge(original_path, edited_path)

            if test_mode:
                test_output = TEMP_TEST_DIR / f"{show.ratingKey}_test.png"
                edited_path.rename(test_output)  # Save the test file to TEMP_DIR
                print(f"Saved test poster to TEMP_DIR: {test_output}")
            else:
                upload_poster(show, edited_path)
                print(f"Uploaded poster for: {show.title}")

        except Exception as e:
            print(f"Failed to process {show.title}: {e}")

if __name__ == "__main__":
    main()

