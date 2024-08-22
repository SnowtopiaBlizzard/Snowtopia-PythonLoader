import argparse
import os
import logging
import newest
import patcher
import kill

if os.path.exists("blizzard.log"):
    os.remove("blizzard.log")

logging.basicConfig(
    level=logging.DEBUG,  # Set the minimum logging level
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('blizzard.log')
    ]
)

logger = logging.getLogger(__name__)  # Create a logger object

snowtopiaPath = r"C:\Program Files (x86)\Steam\steamapps\common\Snowtopia"

# Setup command-line arguments
parser = argparse.ArgumentParser(description="Snowtopia Blizzard Mod Updater")
parser.add_argument("--version", required=False, default="latest", help="Version name to download")
parser.add_argument("--download-components", required=False, default=None, help="Components to download")
parser.add_argument("-f", default="", help="Flags. (include k to kill Snowtopia) (include n to not start Snowtopia)", required=False)
args = parser.parse_args()

killSnowtopia = not (str(args.f).find("k") == -1)
startSnowtopia = str(args.f).find("n") == -1

os.makedirs(snowtopiaPath + r"\Blizzard", exist_ok=True)
os.makedirs(snowtopiaPath + r"\Blizzard\Data", exist_ok=True)

if (not os.path.exists(snowtopiaPath + r"\Blizzard\Data\Version.txt")):
    open(snowtopiaPath + r"\Blizzard\Data\Version.txt", "w").close()

# Restart the Snowtopia process if requested
if killSnowtopia:
    kill.kill_process_by_name("Snowtopia.Game.exe")

# Define headers and token for HTTP requests
headers = {
    "User-Agent": "SnowtopiaBlizzard/BootAgent",
    "Host": "bamsestudio.dk"
}
token = "your-token-here"

logger.info("Booting up Blizzard!")

# Paths for Snowtopia and version file
snowtopia_exe = snowtopiaPath + r"\Snowtopia.Game.exe"
version_file_path = os.path.join(snowtopiaPath, "Blizzard/Data/Version.txt")

logger.debug("Using Snowtopia File Path: %s", snowtopiaPath)

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
        zip_file_path=os.path.join(snowtopiaPath, "Blizzard/Data/out.bd"),
        zip_extraction_path=os.path.join(snowtopiaPath, "Blizzard/Data/ZipOut"),
        base_path=snowtopiaPath,
        headers=headers
    )

    # Update the version file
    with open(version_file_path, "w") as file:
        file.write(latest_version)

    logger.info("Latest version is now downloaded, starting game.")

if (startSnowtopia):
    # Start the Snowtopia game
    os.system(f'call "{snowtopia_exe}"')
