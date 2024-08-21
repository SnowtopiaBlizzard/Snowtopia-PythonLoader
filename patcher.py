import requests
import shutil
import os
import json
from zipfile import ZipFile
from colours import CMDCOLOURS

def print_text(text):
    """Print text in cyan color."""
    print(CMDCOLOURS.OKCYAN + text + CMDCOLOURS.ENDC)

def install_latest_version(download_url, zip_file_path, zip_extraction_path, data_path, headers):
    """Download, extract, and patch the latest version of the game.

    Args:
        download_url (str): URL to download the latest version.
        zip_file_path (str): Path to save the downloaded zip file.
        zip_extraction_path (str): Directory to extract the zip file.
        data_path (str): Directory where the game files should be patched.
        headers (dict): Headers to use for the download request.
    """
    print_text("Downloading Latest Version.")
    download_latest_version(download_url, headers, zip_file_path)
    
    print_text("Extracting Files.")
    extract_file(zip_file_path, zip_extraction_path)
    
    print_text("Patching Game.")
    patch_game(zip_extraction_path, data_path)

def download_latest_version(url, headers, zip_file_path):
    """Download the latest version from the given URL.

    Args:
        url (str): URL to download the file.
        headers (dict): Headers to use for the request.
        zip_file_path (str): Path to save the downloaded zip file.
    """
    response = requests.get(url, headers=headers, stream=True)
    if response.status_code == 200:
        with open(zip_file_path, 'wb') as file:
            shutil.copyfileobj(response.raw, file)
    else:
        raise Exception(f"Failed to download file. Status code: {response.status_code}")

def extract_file(zip_file_path, extraction_path):
    """Extract files from a zip archive.

    Args:
        zip_file_path (str): Path to the zip file.
        extraction_path (str): Directory to extract files to.
    """
    with ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extraction_path)
    os.remove(zip_file_path)

def patch_game(zip_extraction_path, data_path):
    """Apply patches from extracted files to the game.

    Args:
        zip_extraction_path (str): Directory where files were extracted.
        data_path (str): Directory where the game files should be patched.
    """
    json_update_file = os.path.join(zip_extraction_path, "installation/update.json")

    # Check if the JSON update file exists
    if not os.path.isfile(json_update_file):
        raise FileNotFoundError(f"Update file {json_update_file} not found.")

    with open(json_update_file, "r") as f:
        json_data = json.load(f)
    
    installation = json_data.get("installation", {})
    
    # Process folders
    folders = installation.get("folders", [])
    for folder in folders:
        full_folder_path = os.path.join(data_path, "..", folder)
        os.makedirs(full_folder_path, exist_ok=True)

    # Copy files
    files = installation.get("files", {})
    for file_path, folder_path in files.items():
        source_file_path = os.path.join(zip_extraction_path, "installation", file_path)
        destination_folder_path = os.path.join(data_path, "..", folder_path)
        destination_file_path = os.path.join(destination_folder_path, os.path.basename(file_path))

        if not os.path.isfile(source_file_path):
            print(f"Warning: Source file {source_file_path} not found, skipping.")
            continue

        os.makedirs(destination_folder_path, exist_ok=True)
        shutil.copyfile(source_file_path, destination_file_path)

    # Cleanup
    shutil.rmtree(zip_extraction_path)
    print(CMDCOLOURS.OKGREEN + "Game patched successfully!" + CMDCOLOURS.ENDC)
