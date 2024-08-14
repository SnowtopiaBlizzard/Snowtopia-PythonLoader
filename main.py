import argparse
import os
import urllib.parse
import requests
import json

import urllib.parse

class CMDCOLOURS:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

parser = argparse.ArgumentParser(description="Snowtopia Blizzard Mod Updater")
parser.add_argument("--version", required=False, default="latest", help="Version name to download")
parser.add_argument("--download-components", required=False, default=None, help="Compontents to download")
args = parser.parse_args()


headers = {
    "User-Agent": "SnowtopiaBlizzard/BootAgent", 
    "Host": "bamsestudio.dk" 
}

print(CMDCOLOURS.OKGREEN + "Booting up Blizzard!")
snowtopiaExe = r"C:\Program Files (x86)\Steam\steamapps\common\Snowtopia\Snowtopia.exe"
versionFilePath = os.path.join(snowtopiaExe, "../Blizzard/Data/Version.txt")
print(CMDCOLOURS.OKCYAN + "Using Snowtopia File Path: " + snowtopiaExe)

print(CMDCOLOURS.OKCYAN + "Checking for newest update")
with open(versionFilePath, "r") as f:
    versionContent = f.read()
print(CMDCOLOURS.ENDC + "Read " + versionContent + " as version")

print(CMDCOLOURS.HEADER + "Fetching versions")
with requests.get("https://bamsestudio.dk/api/snowtopia/fetch_versions", headers=headers) as response:
    decoded_content = response.content.decode() 
    versionsContent = json.loads(decoded_content) 
print(CMDCOLOURS.OKGREEN + "Done fecthing versions")

print(CMDCOLOURS.ENDC + "Finding newest version")
latestVersion = None
for versionJson in versionsContent["versions"]:
    if versionsContent["versions"][versionJson]["latest"] == True:
        latestVersion = versionJson

if (latestVersion == None):
    print(CMDCOLOURS.FAIL + "Cannot find latest version, please content @gaupestudio.no on discord." + CMDCOLOURS.ENDC)
    quit()
print(CMDCOLOURS.OKGREEN + "Latest version found: " + latestVersion)

if (versionContent == latestVersion):
    print(CMDCOLOURS.OKCYAN + "You have the latest version, starting game.")
else:
    print(CMDCOLOURS.FAIL + "You dont have the latest version, downloading latest!")
    with open(versionFilePath, "w") as file:
        file.write(latestVersion)
    print(CMDCOLOURS.OKGREEN + "Latest version is now dowloaded, starting game.")

print(CMDCOLOURS.ENDC)
os.system("call \"" + snowtopiaExe + "\"")