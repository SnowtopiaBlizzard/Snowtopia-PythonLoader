import logging
import requests
import json
import os
from zipfile import ZipFile

logger = logging.getLogger(__name__)

def install_newest(version_file_path, headers):
    """Check and return the latest version of the game."""
    logger.info("Checking for newest update")
    
    try:
        with open(version_file_path, "r") as f:
            version_content = f.read().strip()
    except FileNotFoundError:
        logger.error("Version file %s not found.", version_file_path)
        return None, False

    logger.info("Fetching versions")
    try:
        response = requests.get("https://bamsestudio.dk/api/snowtopia/fetch_versions", headers=headers)
        response.raise_for_status()
        versions_content = response.json()
    except requests.RequestException as e:
        logger.error("Failed to fetch versions: %s", e)
        return None, False
    except json.JSONDecodeError:
        logger.error("Failed to decode JSON response from the server.")
        return None, False

    logger.info("Done fetching versions")

    logger.info("Finding newest version")
    latest_version = None
    for version_json, details in versions_content.get("versions", {}).items():
        if details.get("beta") and version_json == version_content:
            logger.info("Has beta version, does not overwrite!")
            return None, True

        if details.get("latest"):
            latest_version = version_json

    if not latest_version:
        logger.error("Cannot find latest version. Please contact support.")
        return None, False

    logger.info("Latest version found: %s", latest_version)
    return latest_version, (version_content == latest_version)

def install_custom(version, headers):
    """Check if a custom version is beta and return relevant information."""
    logger.info("Installing custom version of: %s", version)
    logger.info("Checking if BETA")

    logger.info("Fetching versions")
    try:
        response = requests.get("https://bamsestudio.dk/api/snowtopia/fetch_versions", headers=headers)
        response.raise_for_status()
        versions_content = response.json()
    except requests.RequestException as e:
        logger.error("Failed to fetch versions: %s", e)
        return version, False, False
    except json.JSONDecodeError:
        logger.error("Failed to decode JSON response from the server.")
        return version, False, False

    logger.info("Done fetching versions")

    logger.info("Finding version details")
    is_beta = False
    for version_json, details in versions_content.get("versions", {}).items():
        if details.get("beta") and version_json == version:
            logger.info("Is beta!")
            is_beta = True

    if not is_beta:
        logger.info("Is not beta")
    
    return version, False, is_beta
