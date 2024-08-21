import argparse
import os
import newest
import patcher
import kill

from colours import *

parser = argparse.ArgumentParser(description="Snowtopia Blizzard Mod Updater")
parser.add_argument("--version", required=False, default="latest", help="Version name to download")
parser.add_argument("--download-components", required=False, default=None, help="Compontents to download")
parser.add_argument("-r", help="Restart the program. (Set to y)", required=False)
args = parser.parse_args()

if (args.r == "y"):
    kill.kill_process_by_name("Snowtopia.Game.exe")

headers = {
    "User-Agent": "SnowtopiaBlizzard/BootAgent", 
    "Host": "bamsestudio.dk" 
}

token="27984bd5bd17791d89fe5d09ceff46b004c1f878cce2d658c611fc926dab0573c8efddc49eb7d44662adfd36d900f6b7c255b106849d7320d3f6d7e2517ad5696ea3c8e35bbb9ebc6ae47a4629902ce988bd9630982c5c7ab4c0e9f1b4d66a7b829a7d6ccfee40e5cb3e1db78bdd5769f297f84d440079f27c0180c9c635ac5f"

print(CMDCOLOURS.OKGREEN + "Booting up Blizzard!")
snowtopiaExe = r"C:\Program Files (x86)\Steam\steamapps\common\Snowtopia\Snowtopia.Game.exe"
versionFilePath = os.path.join(snowtopiaExe, "../Blizzard/Data/Version.txt")
print(CMDCOLOURS.OKCYAN + "Using Snowtopia File Path: " + snowtopiaExe)

hasLatest = None
latestVersion = None
isBeta = False
if (args.version != "latest"):
    latestVersion, hasLatest, isBeta = newest.installCustom(args.version, headers)
else:
    latestVersion, hasLatest = newest.installNewest(versionFilePath, headers)

if (hasLatest):
    print(CMDCOLOURS.OKCYAN + "You have the latest version, starting game.")
else:
    print(CMDCOLOURS.FAIL + "You dont have the latest version, downloading latest!")

    download_url = "https://bamsestudio.dk/api/snowtopia/install/latest"

    if (args.version != "latest"):
        download_url = "https://bamsestudio.dk/api/snowtopia/install/" + args.version

        if (isBeta):
            download_url += "/" + token

    patcher.install_latest_version(
            download_url=download_url,
            zip_file_path=os.path.join(snowtopiaExe, "../Blizzard/Data/out.bd"),
            zip_extraction_path=os.path.join(snowtopiaExe, "../Blizzard/Data/ZipOut"),
            data_path=os.path.join(snowtopiaExe, "../Snowtopia.Game_Data/"),
            headers=headers,
        )

    with open(versionFilePath, "w") as file:
        file.write(latestVersion)
    print(CMDCOLOURS.OKGREEN + "Latest version is now dowloaded, starting game.")

print(CMDCOLOURS.ENDC)
os.system("call \"" + snowtopiaExe + "\"")