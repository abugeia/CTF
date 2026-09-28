# uv run --with pymupdf python solve.py
import re, zipfile, pymupdf
# 1) Les commentaires JPEG (segment COM) des cartes d'embarquement contiennent nom, PNR et siège
z = zipfile.ZipFile('images.zip')
for n in z.namelist():
    m = re.search(rb'([A-Z]+ [A-Za-z]+ \| PNR \w+ \|[^\xff]*?Boarding \d\d:\d\d)', z.read(n))
    print(n, m.group(1).decode('latin1'))
# 2) PDF récupéré sur le Proton Drive (mot de passe = PNR de Tauira K2D3PL) : texte gris clair sous le siège 27F
page = pymupdf.open('plan-cabine-a320neo.pdf')[0]
print(page.get_text().strip())
