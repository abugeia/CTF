# Rend le QR code SVG de l'ODT en image puis le décode (OpenCV)
import re, sys, numpy as np, cv2
for f in sys.argv[1:]:
    if f.endswith(".svg"):
        s = open(f).read()
        vb = int(re.search(r'viewBox="0 0 (\d+)', s).group(1))
        img = np.full((vb, vb), 255, np.uint8)
        for x, y in re.findall(r"M(\d+),(\d+)h1v1h-1z", s):
            img[int(y), int(x)] = 0
    else:
        img = cv2.imread(f, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(np.pad(img, 4, constant_values=255), None, fx=10, fy=10, interpolation=cv2.INTER_NEAREST)
    print(f, cv2.QRCodeDetector().detectAndDecode(img)[0])
