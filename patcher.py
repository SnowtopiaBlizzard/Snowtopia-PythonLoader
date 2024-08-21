import requests
import shutil
import os
import json

from zipfile import ZipFile
from colours import *

def printText(text):
    print(CMDCOLOURS.OKCYAN + text + CMDCOLOURS.ENDC)

def install_latest_version(download_url, zip_file_path, zip_extraction_path, data_path, headers):
    printText("Downloading Latest Version.")
    download_latest_version(download_url, headers, zip_file_path)
    printText("Extracting Files.")
    extract_file(zip_file_path, zip_extraction_path)
    printText("Patching Game.")
    patch_game(zip_extraction_path, data_path)

def download_latest_version(url, headers, zip_file_path):
    response = requests.get(url, headers=headers, stream=True)
    if response.status_code == 200:
        with open(zip_file_path, 'wb') as file:
            shutil.copyfileobj(response.raw, file)
    else:
        raise Exception(f"Failed to download file. Status code: {response.status_code}")
    
def extract_file(zip_file_path, extraction_path):
    with ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extraction_path)
    os.remove(zip_file_path)

def patch_game(zip_extraction_path, data_path):
    json_update_file = os.path.join(zip_extraction_path, "installation/update.json")
    with open(json_update_file, "r") as f:
        json_data = json.load(f)
    installation = json_data.get("installation", {})
    
    # Process folders
    folders = installation.get("folders", [])
    for folder in folders:
        folder_path = folder
        full_folder_path = os.path.join(data_path, "../", folder_path)
        os.makedirs(full_folder_path, exist_ok=True)

    # Copy files
    files = installation.get("files", {})
    for file_path, folder_path in files.items():
        source_file_path = os.path.join(zip_extraction_path, "installation", file_path)
        destination_folder_path = os.path.join(data_path, "../", folder_path)
        destination_file_path = os.path.join(destination_folder_path, os.path.basename(file_path))

        os.makedirs(destination_folder_path, exist_ok=True)
        shutil.copyfile(source_file_path, destination_file_path)

    # Cleanup
    shutil.rmtree(zip_extraction_path)
    print(CMDCOLOURS.OKGREEN + "Game patched successfully!" + CMDCOLOURS.ENDC)