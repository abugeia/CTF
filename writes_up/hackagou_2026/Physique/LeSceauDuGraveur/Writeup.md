# Le sceau du graveur (HacKagou 2026) — Physique

**Flag :** `OPENNC{...}` *(gravé sur bois par le laser — à relever sur site)*
**Valeur :** 249 pts · **Auteur :** \0/
**Statut :** 🟢 **résolu** (`solved_by_me: true`, +222 pts) — partie à distance ci-dessous
(ordre VARN-041 libéré) ; flag final **gravé physiquement** à l'Atelier de Surface et relevé sur place.

## Énoncé

> Poste **G-06** de l'**Atelier des Graveurs**. Certains ordres sensibles de Varn n'étaient plus confiés à la mémoire du Nautile : transmis sous forme **scellée**, puis **matérialisés sur métal** dans un atelier isolé. Un ordre confidentiel **VARN-041** est présent dans le contrôleur du poste… mais **verrouillé**.

Instance web : `http://challs.hackagou.nc:<port>` — pupitre du contrôleur G-06.

## Reconnaissance

La page expose un pupitre avec deux bons dans la file d'attente :

- **CAL-017** (calibration) : bouton « Aperçu » actif → `action=preview`.
- **VARN-041** (confidentiel) : scellé, bouton verrouillé → `action=release`.

Le journal de maintenance donne tout le mécanisme :

```
[G-06/CTRL] Contrôle de visa : SCEAU32
[G-06/CTRL] CAL-017 autorise action=preview
[G-06/CTRL] VARN-041 attend action=release
[G-06/CTRL] Toute commande modifiée doit présenter un sceau conforme.
```

Le JS du pupitre lit un bon via `/api/calibration-ticket`, puis le POST à
`/api/execute`. Le texte le dit : « Le contrôleur historique ne sait vérifier
que son *sceau* d'intégrité. »

Bon CAL-017 renvoyé par `/api/calibration-ticket` :

```json
{"job":"CAL-017","controller":"SCEAU32",
 "ticket":"c3RhdGlvbj1HMDYm…YnJhc3MtdjE.6a161bf7"}
```

Le ticket est `base64url(payload).crc32hex`. Décodé :

```
station=G06&job=CAL-017&action=preview&profile=brass-v1
```

## Vulnérabilité

**SCEAU32 = CRC32**, pas une signature. Le suffixe est exactement le CRC32 du
payload en clair :

```python
>>> zlib.crc32(b"station=G06&job=CAL-017&action=preview&profile=brass-v1")
0x6a161bf7   # == suffixe du ticket
```

Le CRC32 n'est **pas cryptographique** : connaissant le payload, on recalcule un
sceau valide pour n'importe quel contenu. Le contrôleur ne fait que vérifier
l'intégrité, pas l'authenticité. On forge donc un bon `action=release` pour
VARN-041.

> Détail : le champ `profile=brass-v1` doit être conservé. Sans lui, `/api/execute`
> répond `403 « bon destiné à un autre contrôleur »`.

## Exploitation

```bash
python3 solve.py http://challs.hackagou.nc:<port>
# [execute] HTTP 200 · {"ok":true,"job":"VARN-041","message":"ordre confidentiel libéré",...}
```

Payload forgé : `station=G06&job=VARN-041&action=release&profile=brass-v1`,
re-scellé par CRC32. `/api/execute` l'accepte, `/api/status` passe à
`"released":true`, et le QR de l'ordre s'affiche sur `/qr.png`.

Script : [solve.py](solve.py).

## Livrable : l'ordre scellé

Le QR ([VARN-041_qr.png](VARN-041_qr.png)) ne contient **pas** le flag, mais un
ordre **chiffré** (76 octets) — « le poste de surface possède seul la clé » :

```
OPENNC-LASER:1:y6EtZxYocOZLVHGs-WNS7fIsOtPHWgFvS9AeYMTg1XtCn1J6aGmEB0TMnvnEvI7m0C_0ytndQpJGtw1B5ZnHnW3yw8l-Mcz563dLIw
```

## Finalisation physique (sur site)

C'est le volet « Physique » du challenge : **présenter ce QR au laser de l'Atelier
de Surface**. Le poste détient la clé, déchiffre l'ordre et **grave le flag sur un
morceau de bois**. Le flag `OPENNC{...}` ne se lit que sur la pièce gravée —
irrécupérable à distance.

## Flag

```
OPENNC{...}   # à relever sur la pièce gravée
```
