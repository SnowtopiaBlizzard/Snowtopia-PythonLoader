from colours import CMDCOLOURS
import requests
import json

def install_newest(version_file_path, headers):
    """Check and return the latest version of the game.

    Args:
        version_file_path (str): Path to the file containing the current version.
        headers (dict): Headers to use for the API requests.

    Returns:
        tuple: (latest_version, is_latest) where `latest_version` is the newest version found
               and `is_latest` is a boolean indicating if the current version is up to date.
    """
    print(CMDCOLOURS.OKCYAN + "Checking for newest update" + CMDCOLOURS.ENDC)
    
    try:
        with open(version_file_path, "r") as f:
            version_content = f.read().strip()
    except FileNotFoundError:
        print(CMDCOLOURS.FAIL + f"Version file {version_file_path} not found." + CMDCOLOURS.ENDC)
        return None, False

    print(CMDCOLOURS.HEADER + "Fetching versions" + CMDCOLOURS.ENDC)
    try:
        response = requests.get("https://bamsestudio.dk/api/snowtopia/fetch_versions", headers=headers)
        response.raise_for_status()
        versions_content = response.json()
    except requests.RequestException as e:
        print(CMDCOLOURS.FAIL + f"Failed to fetch versions: {e}" + CMDCOLOURS.ENDC)
        return None, False
    except json.JSONDecodeError:
        print(CMDCOLOURS.FAIL + "Failed to decode JSON response from the server." + CMDCOLOURS.ENDC)
        return None, False

    print(CMDCOLOURS.OKGREEN + "Done fetching versions" + CMDCOLOURS.ENDC)

    print(CMDCOLOURS.ENDC + "Finding newest version" + CMDCOLOURS.ENDC)
    latest_version = None
    for version_json, details in versions_content.get("versions", {}).items():
        if details.get("beta") and version_json == version_content:
            print(CMDCOLOURS.OKBLUE + "Has beta version, does not overwrite!" + CMDCOLOURS.ENDC)
            return None, True

        if details.get("latest"):
            latest_version = version_json

    if not latest_version:
        print(CMDCOLOURS.FAIL + "Cannot find latest version. Please contact @gaupestudio.no on Discord." + CMDCOLOURS.ENDC)
        return None, False

    print(CMDCOLOURS.OKGREEN + "Latest version found: " + latest_version + CMDCOLOURS.ENDC)
    return latest_version, (version_content == latest_version)

def install_custom(version, headers):
    """Check if a custom version is beta and return relevant information.

    Args:
        version (str): The version to check.
        headers (dict): Headers to use for the API requests.

    Returns:
        tuple: (version, is_latest, is_beta) where `version` is the custom version checked,
               `is_latest` is a boolean indicating if it is the latest version (always False here),
               and `is_beta` is a boolean indicating if the version is a beta.
    """
    print(CMDCOLOURS.OKGREEN + "Installing custom version of: " + version + CMDCOLOURS.ENDC)
    print(CMDCOLOURS.OKBLUE + "Checking if BETA" + CMDCOLOURS.ENDC)

    print(CMDCOLOURS.HEADER + "Fetching versions" + CMDCOLOURS.ENDC)
    try:
        response = requests.get("https://bamsestudio.dk/api/snowtopia/fetch_versions", headers=headers)
        response.raise_for_status()
        versions_content = response.json()
    except requests.RequestException as e:
        print(CMDCOLOURS.FAIL + f"Failed to fetch versions: {e}" + CMDCOLOURS.ENDC)
        return version, False, False
    except json.JSONDecodeError:
        print(CMDCOLOURS.FAIL + "Failed to decode JSON response from the server." + CMDCOLOURS.ENDC)
        return version, False, False

    print(CMDCOLOURS.OKGREEN + "Done fetching versions" + CMDCOLOURS.ENDC)

    print(CMDCOLOURS.ENDC + "Finding version details" + CMDCOLOURS.ENDC)
    is_beta = False
    for version_json, details in versions_content.get("versions", {}).items():
        if details.get("beta") and version_json == version:
            print(CMDCOLOURS.OKBLUE + "Is beta!" + CMDCOLOURS.ENDC)
            is_beta = True

    if not is_beta:
        print(CMDCOLOURS.OKCYAN + "Is not beta" + CMDCOLOURS.ENDC)
    
    return version, False, is_beta
