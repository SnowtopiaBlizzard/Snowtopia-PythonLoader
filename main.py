import argparse

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

print(CMDCOLOURS.OKGREEN + "Booting up Blizzard!")
snowtopiaExe = r"C:\Program Files (x86)\Steam\steamapps\common\Snowtopia\Snowtopia.exe"
print(CMDCOLOURS.OKCYAN + "Using Snowtopia File Path: " + snowtopiaExe)



print(CMDCOLOURS.ENDC)