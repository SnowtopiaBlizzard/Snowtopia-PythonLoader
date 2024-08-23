import binascii

def validate(path):
    count = 0
    scale = 16 # equals to hexadecimal

    with open(path, 'rb') as f:
        hexdata = binascii.hexlify(f.read())
        binary = bin(int(hexdata, scale))[2:]

    for i in str(binary):
        count += int(i)

    return count

print(validate("Assembly-CSharp.dll"))