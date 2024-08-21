from colours import CMDCOLOURS
import requests
import json

def installNewest(versionFilePath, headers):
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
        if versionsContent["versions"][versionJson]["beta"] == True and versionJson == versionContent:
            print("Has beta version, does not overwrite!")
            return None, True

        if versionsContent["versions"][versionJson]["latest"] == True:
            latestVersion = versionJson

    if (latestVersion == None):
        print(CMDCOLOURS.FAIL + "Cannot find latest version, please content @gaupestudio.no on discord." + CMDCOLOURS.ENDC)
        quit()
    print(CMDCOLOURS.OKGREEN + "Latest version found: " + latestVersion)

    return latestVersion, (versionContent == latestVersion)

def installCustom(version, headers):
    print(CMDCOLOURS.OKGREEN + "Installing custom version of: " + version)
    print(CMDCOLOURS.OKBLUE + "Checking if BETA")

    print(CMDCOLOURS.HEADER + "Fetching versions")
    with requests.get("https://bamsestudio.dk/api/snowtopia/fetch_versions", headers=headers) as response:
        decoded_content = response.content.decode() 
        versionsContent = json.loads(decoded_content) 
    print(CMDCOLOURS.OKGREEN + "Done fecthing versions")

    print(CMDCOLOURS.ENDC + "Finding newest version")
    isBeta = False
    for versionJson in versionsContent["versions"]:
        if versionsContent["versions"][versionJson]["beta"] == True and versionJson == version:
            print(CMDCOLOURS.OKBLUE + "Is beta!")
            isBeta = True

    if not isBeta:
        print(CMDCOLOURS.OKCYAN + "Is not beta")
    return version, False, isBeta
