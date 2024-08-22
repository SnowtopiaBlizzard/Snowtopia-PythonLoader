import binascii
import os
import logging

import tealib.Converter_b64ToBinary as b64_bin
import tealib.Converter_binaryToB64 as bin_b64

import diff_match_patch as dmp_module

logger = logging.getLogger(__name__)

VALIDATE_COUNT = 4096070

def patch_assembly(zip_ext_path, base_path):
    mainAssemblyPath = os.path.join(base_path, "Snowtopia.Game_Data/Managed/Assembly-CSharp.dll")
    
    if (validate(mainAssemblyPath) == VALIDATE_COUNT):
        logger.info("Validation successful.")
    else:
        logger.error("Validation unsuccessful.")
        quit()

    dmp = dmp_module.diff_match_patch()

    bin_b64.Convert(mainAssemblyPath)

    Assembly = open("Assembly-CSharp.txt.b64", "r").read() #original
    NAssembly = open("NewAssembly.txt.b64", "w") #modded(to make)

    changeLog = open(os.path.join(zip_ext_path, "installation/assembly.dll"), 'r').read()

    patches = dmp.patch_fromText(changeLog) #gets pacthes
    Final = dmp.patch_apply(patches, Assembly)[0] #converts Assembly into modded(only need first in list output)

    NAssembly.write(Final)
    NAssembly.close()

    b64_bin.Convert(mainAssemblyPath)
    
    os.remove("Assembly-CSharp.txt.b64")
    os.remove("NewAssembly.txt.b64")

def validate(path):
    count = 0
    scale = 16 # equals to hexadecimal

    with open(path, 'rb') as f:
        hexdata = binascii.hexlify(f.read())
        binary = bin(int(hexdata, scale))[2:]

    for i in str(binary):
        count += int(i)

    return count