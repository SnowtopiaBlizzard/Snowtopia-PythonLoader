import logging
import shutil
import os
import json
import requests

import urllib.parse
import assembly

from zipfile import ZipFile

logger = logging.getLogger(__name__)

def install_latest_version(download_url, zip_file_path, zip_extraction_path, base_path, headers):
    """Download, extract, and patch the latest version of the game."""
    logger.info("Downloading Latest Version.")
    download_latest_version(download_url, headers, zip_file_path)
    
    logger.info("Extracting Files.")
    extract_file(zip_file_path, zip_extraction_path)
    
    logger.info("Patching Game.")
    patch_game(zip_extraction_path, base_path)

    logger.info("Patching Assembly")
    assembly.patch_assembly(zip_extraction_path, base_path)

def download_latest_version(url, headers, zip_file_path):
    """Download the latest version from the given URL."""
    # Ensure the URL is clean and encoded properly
    url = url.strip()  # Remove leading/trailing whitespace and newline characters
    url = urllib.parse.quote(url, safe=':/')  # Encode the URL properly

    response = requests.get(url, headers=headers, stream=True)
    
    if response.status_code != 200:
        logger.error("Invalid session, while downloading. If you are not downloading a beta version, please ping @gaupestudio.no on the discord.")
        exit()
            
    with open(zip_file_path, 'wb') as file:
        shutil.copyfileobj(response.raw, file)

    logger.info("Download completed successfully.")

def extract_file(zip_file_path, extraction_path):
    """Extract files from a zip archive."""
    with ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extraction_path)
    os.remove(zip_file_path)

def patch_game(zip_extraction_path, base_path):
    """Apply patches from extracted files to the game."""
    json_update_file = os.path.join(zip_extraction_path, "installation/update.json")

    with open(json_update_file) as json_file:
        data = json.load(json_file)

    # Create all necessary folders specified in the JSON
    for folder in data["installation"]["folders"]:
        dst_folder = os.path.join(base_path, folder)
        os.makedirs(dst_folder, exist_ok=True)

    # Iterate through files in the 'installation/files' section of the JSON
    for src_file, dst_folder in data["installation"]["files"].items():
        # Construct the full source path
        src = os.path.join(zip_extraction_path, "installation", src_file)
        # Construct the full destination path
        dst = os.path.join(base_path, dst_folder, os.path.basename(src_file))
        
        # Ensure the destination directory exists (just in case)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        
        # Copy the file
        shutil.copyfile(src, dst)

    logger.info("Game patched successfully.")