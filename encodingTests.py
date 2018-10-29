
"""
This script verifies that the formulas for converting 8-bit color
channel values to 3-bit, 4-bit and 5-bit ones all produce the closest
possible representation in that integer size (when using the Wii's
decoding formulas, as divined from Dolphin).
"""

def decode3(val):
    return val << 5 | val << 2 | val >> 1
def decode4(val):
    return val * 17 # equivalent to "val << 4 | val"
def decode5(val):
    return val << 3 | val >> 2

def encode3(val):
    # 36.5 in binary is 00100100.1
    return int((val + 18) // 36.5)
def encode4(val):
    # 17 in binary is 00010001
    return (val + 8) // 17
def encode5(val):
    # 8.25 in binary is 00001000.01
    return int((val + 4) // 8.25)

funcs = [
    (3, encode3, decode3),
    (4, encode4, decode4),
    (5, encode5, decode5),
]

for bits, encodeFunc, decodeFunc in funcs:
    for i in range(256):
        encoded = encodeFunc(i)
        decoded = decodeFunc(encoded)
        decodedM1 = decodeFunc(encoded - 1)
        decodedP1 = decodeFunc(encoded + 1)

        dist = abs(decoded - i)
        distM1 = abs(decodedM1 - i)
        distP1 = abs(decodedP1 - i)
        if distM1 < dist:
            print(f'encode{bits}({i}) = {encoded}; decode{bits}({encoded}) = {decoded} ({dist} away); decode{bits}({encoded} - 1) = {decodedM1} ({distM1} away)')
        if distP1 < dist:
            print(f'encode{bits}({i}) = {encoded}; decode{bits}({encoded}) = {decoded} ({dist} away); decode{bits}({encoded} + 1) = {decodedP1} ({distP1} away)')
