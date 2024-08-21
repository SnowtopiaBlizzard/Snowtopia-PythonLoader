import argparse
import os
import requests
import json
import logging
import newest
import patcher
import kill

logging.basicConfig(
    level=logging.DEBUG,  # Set the minimum logging level
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    handlers=[
        logging.StreamHandler()  # Output logs to console
        # Optionally add a file handler to output logs to a file
        # logging.FileHandler('application.log')
    ]
)

logger = logging.getLogger(__name__)  # Create a logger object

logger = logging.getLogger(__name__)

# Setup command-line arguments
parser = argparse.ArgumentParser(description="Snowtopia Blizzard Mod Updater")
parser.add_argument("--version", required=False, default="latest", help="Version name to download")
parser.add_argument("--download-components", required=False, default=None, help="Components to download")
parser.add_argument("-r", help="Restart the program. (Set to y)", required=False)
args = parser.parse_args()

# Restart the Snowtopia process if requested
if args.r == "y":
    kill.kill_process_by_name("Snowtopia.Game.exe")

# Define headers and token for HTTP requests
headers = {
    "User-Agent": "SnowtopiaBlizzard/BootAgent",
    "Host": "bamsestudio.dk"
}
token = "your-token-here"

logger.info("Booting up Blizzard!")

# Paths for Snowtopia and version file
snowtopia_exe = r"C:\Program Files (x86)\Steam\steamapps\common\Snowtopia\Snowtopia.Game.exe"
version_file_path = os.path.join(os.path.dirname(snowtopia_exe), "Blizzard/Data/Version.txt")

logger.debug("Using Snowtopia File Path: %s", snowtopia_exe)

# Determine the current and latest versions
has_latest = None
latest_version = None
is_beta = False

if args.version != "latest":
    latest_version, has_latest, is_beta = newest.install_custom(args.version, headers)
else:
    latest_version, has_latest = newest.install_newest(version_file_path, headers)

if has_latest:
    logger.info("You have the latest version, starting game.")
else:
    logger.info("You do not have the latest version, downloading latest!")

    download_url = "https://bamsestudio.dk/api/snowtopia/install/latest"

    if args.version != "latest":
        download_url = f"https://bamsestudio.dk/api/snowtopia/install/{args.version}"

        if is_beta:
            download_url += f"/{token}"

    # Install the latest version
    patcher.install_latest_version(
        download_url=download_url,
        zip_file_path=os.path.join(os.path.dirname(snowtopia_exe), "Blizzard/Data/out.bd"),
        zip_extraction_path=os.path.join(os.path.dirname(snowtopia_exe), "Blizzard/Data/ZipOut"),
        data_path=os.path.join(os.path.dirname(snowtopia_exe), "Snowtopia.Game_Data/"),
        headers=headers
    )

    # Update the version file
    with open(version_file_path, "w") as file:
        file.write(latest_version)

    logger.info("Latest version is now downloaded, starting game.")

# Start the Snowtopia game
os.system(f'call "{snowtopia_exe}"')
