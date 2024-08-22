import binascii
import codecs
import diff_match_patch as dmp_module
import argparse
import os
import logging

# Create 'bin' directory if it doesn't exist
os.makedirs("bin", exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Set the minimum logging level
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('bin/app.log')
    ]
)
logger = logging.getLogger(__name__)

# Argument parser setup
parser = argparse.ArgumentParser(description="Snowtopia Blizzard Changelog Creator")
parser.add_argument("-a", required=False, default="bin/Assembly-CSharp.dll", help="Path to the original assembly")
parser.add_argument("-m", required=False, default="bin/ModdedAssembly-CSharp.dll", help="Path to the modded assembly")
parser.add_argument("-c", required=False, default="bin/changelog.log", help="Path to the output changelog")
args = parser.parse_args()

# Helper function to convert a file to base64 encoded text
def convert_to_base64(file_path, output_path):
    with open(file_path, 'rb') as f:
        hexdata = binascii.hexlify(f.read())
        b64data = codecs.encode(codecs.decode(hexdata, 'hex'), 'base64').decode()
        with open(output_path, "w") as out_file:
            out_file.write(b64data)

# Convert original and modded assemblies to base64
convert_to_base64(args.a, "bin/Assembly-CSharp.txt.b64")
convert_to_base64(args.m, "bin/ModdedAssembly-CSharp.txt.b64")

# Load base64 encoded assemblies
with open("bin/Assembly-CSharp.txt.b64", "r") as f:
    original_assembly = f.read()

with open("bin/ModdedAssembly-CSharp.txt.b64", "r") as f:
    modded_assembly = f.read()

# Create and apply patches
dmp = dmp_module.diff_match_patch()
patches = dmp.patch_make(original_assembly, modded_assembly)
patches_text = dmp.patch_toText(patches)

# Write patches to changelog
with open(args.c, "w") as changelog:
    changelog.write(patches_text)

logger.info('Changelog creation completed.')

os.remove("bin/Assembly-CSharp.txt.b64")
os.remove("bin/ModdedAssembly-CSharp.txt.b64")