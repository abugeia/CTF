# Extrait le ZIP caché en LSB (RGB, parcours colonne par colonne, bits LSB-first) dans corporate_logo.png
from PIL import Image
import numpy as np, zipfile, io
a = np.array(Image.open("corporate_logo.png")).transpose(1, 0, 2)
by = np.packbits((a[:, :, :3] & 1).flatten(), bitorder="little").tobytes()
print("header:", by[:5])
i = by.find(b"PK\x03\x04"); j = by.find(b"PK\x05\x06")
z = by[i:j + 22]
open("hidden.zip", "wb").write(z)
zf = zipfile.ZipFile(io.BytesIO(z))
for n in zf.namelist(): print(n, zf.read(n))
