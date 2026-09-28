# Réassemble les fragments du journal et XOR avec la clé récupérée dans les blocs libres de disk.img
# Prérequis : 7z x -p"N3URONA_C2_K3Y_R3C0V3RY" classified_intel.7z -ointel  (ou py7zr)
import base64, itertools
frags = {68: "MWdl9A==", 97: "Jija0+nOfm", 29: "VdzaTRA4Vi", 76: "m6YwjzPz5N", 34: "0XRvXKsM11"}
d = open("intel/disk.img", "rb").read()
i = d.find(b"XANTHOS_C2_KEY::") + 16; j = d.find(b"::XANTHOS_KEY_END")
key = d[i:j]
print("key", len(key), key.hex())
others = [k for k in frags if k != 68]
for perm in itertools.permutations(others):
    order = list(perm) + [68]
    ct = base64.b64decode("".join(frags[k] for k in order))
    pt = bytes(c ^ key[n % len(key)] for n, c in enumerate(ct))
    if pt.isascii():
        print(order, pt)
