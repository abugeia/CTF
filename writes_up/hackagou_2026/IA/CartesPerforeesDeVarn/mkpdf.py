#!/usr/bin/env python3
"""Génère un PDF minimal (texte brut, Helvetica) — porteur du payload d'injection.

Usage: python3 mkpdf.py <sortie.pdf> <texte>
   ou: python3 mkpdf.py <sortie.pdf> -f payload.txt
"""
import sys


def pdf(text, fname):
    parts = ["BT /F1 11 Tf 50 780 Td 14 TL"]
    for ln in text.split("\n"):
        esc = ln.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
        parts.append(f"({esc}) Tj T*")
    parts.append("ET")
    stream = "\n".join(parts).encode()
    objs = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] "
        b"/Resources << /Font << /F1 5 0 R >> >> /Contents 4 0 R >>",
        b"<< /Length %d >>\nstream\n%s\nendstream" % (len(stream), stream),
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]
    out = b"%PDF-1.4\n"
    offs = []
    for i, o in enumerate(objs, 1):
        offs.append(len(out))
        out += b"%d 0 obj\n%s\nendobj\n" % (i, o)
    xref = len(out)
    out += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objs) + 1)
    for off in offs:
        out += b"%010d 00000 n \n" % off
    out += b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF" % (
        len(objs) + 1, xref)
    open(fname, "wb").write(out)


if __name__ == "__main__":
    if sys.argv[2] == "-f":
        text = open(sys.argv[3], encoding="utf-8").read()
    else:
        text = sys.argv[2]
    pdf(text, sys.argv[1])
    print("ok", sys.argv[1])
