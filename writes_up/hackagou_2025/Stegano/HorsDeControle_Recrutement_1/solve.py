# uv run --with pymupdf python solve.py
# Liste les spans de texte du PDF avec leur couleur : le flag est écrit en blanc (0xffffff) sur fond blanc.
import pymupdf
page = pymupdf.open('Secret_Doc.pdf')[0]
for bl in page.get_text('dict')['blocks']:
    for l in bl.get('lines', []):
        for s in l['spans']:
            if s['color'] == 0xffffff and s['text'].strip():
                print(hex(s['color']), s['bbox'], s['text'])
