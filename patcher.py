import logging
import shutil
import os
import json
import requests
from zipfile import ZipFile

logger = logging.getLogger(__name__)

def print_text(text):
    """Print text in cyan color."""
    logger.info(text)

def install_latest_version(download_url, zip_file_path, zip_extraction_path, data_path, headers):
    """Download, extract, and patch the latest version of the game."""
    print_text("Downloading Latest Version.")
    download_latest_version(download_url, headers, zip_file_path)
    
    print_text("Extracting Files.")
    extract_file(zip_file_path, zip_extraction_path)
    
    print_text("Patching Game.")
    patch_game(zip_extraction_path, data_path)

def download_latest_version(url, headers, zip_file_path):
    """Download the latest version from the given URL."""
    response = requests.get(url, headers=headers, stream=True)
    if response.status_code == 200:
        with open(zip_file_path, 'wb') as file:
            shutil.copyfileobj(response.raw, file)
    else:
        raise Exception(f"Failed to download file. Status code: {response.status_code}")

def extract_file(zip_file_path, extraction_path):
    """Extract files from a zip archive."""
    with ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extraction_path)
    os.remove(zip_file_path)

def patch_game(zip_extraction_path, data_path):
    """Apply patches from extracted files to the game."""
    json_update_file = os.path.join(zip_extraction_path, "installation/update.json")

    with open(json_update_file) as json_file:
        data = json.load(json_file)

    for patch in data.get("patches", []):
        src = os.path.join(zip_extraction_path, patch["src"])
        dst = os.path.join(data_path, patch["dst"])
        shutil.copyfile(src, dst)

    print_text("Game patched successfully.")
