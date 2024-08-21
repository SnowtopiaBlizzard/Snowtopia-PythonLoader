import argparse
import os
import newest
import patcher
import kill

from colours import CMDCOLOURS

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
token = "27984bd5bd17791d89fe5d09ceff46b004c1f878cce2d658c611fc926dab0573c8efddc49eb7d44662adfd36d900f6b7c255b106849d7320d3f6d7e2517ad5696ea3c8e35bbb9ebc6ae47a4629902ce988bd9630982c5c7ab4c0e9f1b4d66a7b829a7d6ccfee40e5cb3e1db78bdd5769f297f84d440079f27c0180c9c635ac5f"

print(CMDCOLOURS.OKGREEN + "Booting up Blizzard!")

# Paths for Snowtopia and version file
snowtopia_exe = r"C:\Program Files (x86)\Steam\steamapps\common\Snowtopia\Snowtopia.Game.exe"
version_file_path = os.path.join(os.path.dirname(snowtopia_exe), "Blizzard/Data/Version.txt")

print(CMDCOLOURS.OKCYAN + "Using Snowtopia File Path: " + snowtopia_exe)

# Determine the current and latest versions
has_latest = None
latest_version = None
is_beta = False

if args.version != "latest":
    latest_version, has_latest, is_beta = newest.install_custom(args.version, headers)
else:
    latest_version, has_latest = newest.install_newest(version_file_path, headers)

# Check if the latest version is installed
if has_latest:
    print(CMDCOLOURS.OKCYAN + "You have the latest version, starting game.")
else:
    print(CMDCOLOURS.FAIL + "You do not have the latest version, downloading latest!")

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
    
    print(CMDCOLOURS.OKGREEN + "Latest version is now downloaded, starting game.")

print(CMDCOLOURS.ENDC)

# Start the Snowtopia game
os.system(f'call "{snowtopia_exe}"')
