#!/usr/bin/env python3
"""Echo du Legacy (HacKagou 2026) — décodeur.

Le texte de l'instance cache 32 noms d'objets. L'initiale de chacun est une
lettre A–P, soit un chiffre hexadécimal (A=0 … J=9, K=a … P=f). Les 32 chiffres
forment l'UUID du flag. Chaque segment de phrase (entre virgules/points) se
termine par un objet ; les mots de liaison varient d'une instance à l'autre.

Usage :
    python3 decode.py http://challs.hackagou.nc:<port>/   # URL de l'instance
    python3 decode.py texte.txt    # fichier (texte brut ou HTML)
    python3 decode.py -            # coller le texte puis Ctrl-D
"""
import html
import re
import sys
import unicodedata
import urllib.request


def strip_accents(s: str) -> str:
    s = s.replace("œ", "oe").replace("æ", "ae")
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()


def extract_text(raw: str) -> str:
    # HTML de l'instance : on ne garde que le paragraphe de l'<article>.
    m = re.search(r"<article[^>]*>(.*?)</article>", raw, re.S)
    if m:
        raw = re.sub(r"<[^>]+>", " ", m.group(1))
    return html.unescape(raw)


def is_hex(w: str) -> bool:
    return "a" <= strip_accents(w)[:1] <= "p"


def to_hex(words: list[str]) -> str:
    return "".join("%x" % (ord(strip_accents(w)[0]) - ord("a")) for w in words)


def is_uuid4(h: str) -> bool:
    return h[12] == "4" and h[16] in "89ab"


def read_input(arg: str) -> str:
    if arg == "-":
        return sys.stdin.read()
    if re.match(r"https?://", arg):
        req = urllib.request.Request(arg, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.read().decode(r.headers.get_content_charset() or "utf-8")
    with open(arg, encoding="utf-8") as f:
        return f.read()


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__, file=sys.stderr)
        return 2
    raw = read_input(sys.argv[1])
    # Gabarit : chaque segment (entre virgules/points) se termine par un objet
    # (« …mentionne un fragment », « avec accouplement », « bouchon »).
    chunks = [re.findall(r"[^\W\d_]+", c.lower())
              for c in re.split(r"[,.;:]", extract_text(raw))]
    chunks = [c for c in chunks if c]
    items = [c[-1] for c in chunks]

    # Exception : « Ensuite instrument rejoint un noyau » porte deux objets.
    # Le premier est absent du découpage : on essaie chaque segment de forme
    # « mot X verbe un Y » et on garde l'insertion qui donne un UUIDv4. Si
    # plusieurs passent (« non loin demeure un… »), on prend celle en position
    # 16 : dans le gabarit, ce segment ouvre le 4e groupe (nibble de variante).
    if len(items) == 31:
        tries = []
        for i, c in enumerate(chunks):
            if len(c) >= 5 and c[3] in ("un", "une") and is_hex(c[1]):
                cand = items[:i] + [c[1]] + items[i:]
                if all(is_hex(w) for w in cand) and is_uuid4(to_hex(cand)):
                    tries.append((i, cand))
        if len(tries) > 1:
            tries = [t for t in tries if t[0] == 16]
        if len(tries) == 1:
            items = tries[0][1]

    bad = [w for w in items if not is_hex(w)]
    if len(items) != 32 or bad:
        print(f"[!] {len(items)} objets trouvés (attendu 32), hors A–P : {bad}", file=sys.stderr)
        for i, w in enumerate(items, 1):
            print(f"  {i:2} {w}", file=sys.stderr)
        return 1

    h = to_hex(items)
    if not is_uuid4(h):
        print("[?] Pas un UUIDv4 valide, vérifier la liste des objets.", file=sys.stderr)
    print(f"OPENNC{{{h[:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:]}}}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
