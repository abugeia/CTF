### Énoncé
Fichier texte rempli d’emojis 💩 en grille. Les emplacements visibles ne contiennent apparemment que des emojis, mais le flag est encodé en stéganographie via des caractères invisibles autour/entre les emoji (marqueurs de largeur zéro, selectors, etc.). Objectif : extraire le flag.

### Étapes
1.  Inspecter les codepoints pour repérer quels caractères invisibles accompagnent les emoji (ex. `U+200B` ZWSP, `U+FE0F` VS16, `U+200D` ZWJ, etc.).
2.  Pour chaque ligne, parcourir les emoji et lire la présence/absence d’un marqueur invisible après chaque emoji pour produire une séquence de bits.
3.  Interpréter chaque ligne comme un octet (par ex. 8 bits) en testant l’ordre (MSB/LSB) et l’éventuelle inversion des bits.
4.  Assembler les octets ligne par ligne pour obtenir la chaîne complète et repérer le flag.

### Script principal (exécuter localement)
Ce script teste automatiquement plusieurs marqueurs courants, largeurs et ordres, et recherche les sorties lisibles ou contenant `sun{`. Sauvegarde sous `decode_poop.py` et lance `python3 decode_poop.py`.
```python
#!/usr/bin/env python3
# decode_poop.py
# Décodage automatique d'une grille d'emoji 💩 encodant des bits via caractères invisibles.

import sys, re

FNAME = "poop_challenge.txt"
try:
    lines = [ln.rstrip("\n") for ln in open(FNAME, "r", encoding="utf-8")]
except FileNotFoundError:
    print("Fichier", FNAME, "introuvable.")
    sys.exit(1)

markers = {
    "VS16": "\uFE0F",   # Variation Selector-16
    "ZWSP": "\u200B",   # Zero-Width Space
    "ZWNJ": "\u200C",   # Zero-Width Non-Joiner
    "ZWJ":  "\u200D",   # Zero-Width Joiner
    "LRM":  "\u200E",   # Left-to-Right Mark
    "RLM":  "\u200F",   # Right-to-Left Mark
    "BOMZ": "\uFEFF",   # Zero-Width No-Break Space
    "WJ":   "\u2060",   # Word Joiner
}

def bits_from_line_for_marker(line, marker):
    cps = [ord(ch) for ch in line]
    bits = []
    i = 0
    while i < len(cps):
        cp = cps[i]
        if cp == 0x1F4A9:  # poop
            nxt = cps[i+1] if i+1 < len(cps) else None
            if nxt is None:
                bits.append('0')
            else:
                bits.append('1' if chr(nxt) == marker else '0')
            i += 1
            if i < len(cps) and chr(cps[i]) == marker:
                i += 1
        else:
            i += 1
    return bits

def decode_with(marker_chr, width, order_msb_first=True, invert=False):
    out_chars = []
    for ln in lines:
        bits = bits_from_line_for_marker(ln, marker_chr)
        if not bits:
            return None
        b = bits[:width]
        if len(b) < width:
            b = b + ['0'] * (width - len(b))
        if invert:
            b = ['1' if x == '0' else '0' for x in b]
        bitstr = ''.join(b)
        if order_msb_first:
            val = int(bitstr, 2)
        else:
            val = int(''.join(reversed(bitstr)), 2)
        out_chars.append(chr(val))
    return ''.join(out_chars)

candidates = []
widths = list(range(7,13))
for mname, mch in markers.items():
    for width in widths:
        for order in (True, False):
            for invert in (False, True):
                s = decode_with(mch, width, order_msb_first=order, invert=invert)
                if s is None:
                    continue
                printable_frac = sum(1 for ch in s if 32 <= ord(ch) <= 126)/max(1,len(s))
                if s.startswith("sun{") or "sun{" in s or "flag" in s.lower() or (printable_frac > 0.3 and "{" in s):
                    candidates.append((mname, width, "MSB" if order else "LSB", "INV" if invert else "NOP", printable_frac, s[:400]))

if candidates:
    print("Candidates trouvées :")
    for mname, width, ordername, inv, pf, snippet in candidates:
        print(f"marker={mname} width={width} order={ordername} inv={inv} printable_frac={pf:.2f}")
        print(" ->", snippet)
else:
    print("Aucune candidate claire. Exécutez d'abord un dump des codepoints pour identifier le marqueur.")

# Affichage résumé colonne (optionnel)
for mname, mch in markers.items():
    matrix = []
    maxcols = 0
    for ln in lines:
        bits = bits_from_line_for_marker(ln, mch)
        matrix.append(bits)
        maxcols = max(maxcols, len(bits))
    print(f"marker={mname:5s} maxcols={maxcols}")
```

### Script utilitaire (dump codepoints)
Avant d’exécuter le décodage, utile pour confirmer le marqueur utilisé : sauvegarde comme `dump_codepoints.py` et lance `python3 dump_codepoints.py`.
```python
#!/usr/bin/env python3
# dump_codepoints.py — affiche codepoints et noms pour quelques lignes du fichier
import unicodedata
fname = "poop_challenge.txt"
with open(fname, "r", encoding="utf-8") as f:
    for lineno, line in enumerate(f, start=1):
        if lineno > 6:
            break
        line = line.rstrip("\n")
        print(f"--- Line {lineno} (len={len(line)}) ---")
        for i,ch in enumerate(line):
            cp = ord(ch)
            try:
                name = unicodedata.name(ch)
            except ValueError:
                name = "<no name>"
            print(f" idx={i:03d} U+{cp:04X} ({name})")
        print()
```

### Usage
```bash
# Optionnel, pour confirmer le marqueur (ex: U+200B)
python3 dump_codepoints.py

# Lancer le décodage
python3 decode_poop.py
```

### Paramètres courants ayant fonctionné
* **Marqueur détecté** : ZWSP (`U+200B`, zero-width space)
* **Largeur** : 8 bits par ligne
* **Ordre** : MSB first
* Pas d’inversion des bits

### Flag trouvé
**`sun{lesssgooo_solved_the_poop_challenge!}`**