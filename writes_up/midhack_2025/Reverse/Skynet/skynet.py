# -*- coding: utf-8 -*-

# HACKAGOU - k3rhu0n

while True:
    hex1 = input("Type the value: ")
    hex2 = "CAFEBABE"
    bytes2 = bytes.fromhex(hex2)

    try:
        bytes1 = bytes.fromhex(hex1)    
    except:
        print("Error!!!")
        continue

    key = (bytes2 * (len(bytes1) // len(bytes2) + 1))[:len(bytes1)]

    xor_result = bytes([b1 ^ b2 for b1, b2 in zip(bytes1, key)])

    hex_result = xor_result.hex()

    if hex_result.lower() == "7cd180b961130ba45ecdc21d0bccd308317eee977775f3c261ba270482a6fdeb":
        print("Congrats Dude, got it!!!")
        exit()
    else:
        print("Sorry you've lost, try again!")


