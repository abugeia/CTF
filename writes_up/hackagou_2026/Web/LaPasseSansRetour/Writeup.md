# La Passe Sans Retour (HacKagou 2026) — Web

**Flag :** `OPENNC{da0b702b-b393-4de6-86a0-e9e896defa3d}`
**Valeur :** 250 pts · **Auteur :** Ketsui
**Statut :** ✅ résolu

> ⚠️ Flag **dynamique, unique par run/instance** (celui-ci = instance
> `challs.hackagou.nc:48983`). Rejouer le solveur pour obtenir le flag d'une autre instance.

## Énoncé

Console web de navigation sonar. Il faut **traverser 50 secteurs** (puzzles de
déplacement) avant épuisement des **60 s** de réserve respiratoire, en activant dans
chaque secteur les **3 relais** (cuivre → laiton → Varn) **dans l'ordre** avant de
présenter le sous-marin au sas. Arrivée au refuge du capitaine **Élias Varn** = flag.

## Reconnaissance

Le moteur est **côté client** mais la validation du chemin est **côté serveur**.
Fichiers : `game.mjs` (UI + protocole) et `rules.mjs` (règles de navigation, servies au
navigateur). Endpoints :

- `POST /api/start` → `{run_id, ...field}` (secteur 1, `time_left=60`), header de session `X-Run-Token: run_id`.
- `POST /api/submit_path` `{moves, nonce}` → soit le **secteur suivant**, soit `{status:"won", flag, archive}`, soit `{status:"lost", reason}`.
- `GET /api/preview` → secteur d'entraînement (non chronométré, sans flag) — pratique pour inspecter le format JSON.

**Point clé** : `submit_path` accepte la **chaîne de commandes complète** d'un secteur
(`[NSEW.]{1,180}`) et renvoie directement le secteur suivant. On peut donc **ignorer le
jeu temps-réel** et enchaîner start → résoudre → submit × 50 par HTTP. Le chrono (60 s)
se relâche à peine entre secteurs (il décompte le temps réel du run) → il faut un solveur
rapide, mais 50 requêtes locales prennent ~10 s.

### Règles de navigation (`rules.mjs`)

Grille `size`×`size`, cycle de marée `cycle`. État `(x, y, t, r)` ; l'horloge est
`clock = field.phase + t`. À chaque commande (`N/S/W/E/.`) :

- déplacement d'un cran ; la case cible doit être **sûre au tick suivant** : pas un mur `#`,
  pas occupée par une **sentinelle** (obstacle horizontal, position `=(x+vx·clock) mod n`),
  pas un **volet fermé** (shutter périodique : fermé si `(clock+offset) mod period ∉ open`) ;
- interdiction de **croiser** une sentinelle (échange de cases) ;
- si la case d'arrivée est un **courant** (`^ v < >`), on est poussé d'un cran de plus
  (re-vérifié sûr) ;
- les **relais** doivent être atteints dans l'ordre ; arriver sur la **sortie** sans les 3
  relais = `INTERLOCK` (échec).

## Exploitation

On réimplémente fidèlement `rules.mjs` en Python et on résout chaque secteur par **BFS**
(état visité = `(x, y, r, clock mod cycle)`, espace minuscule ≈ 12·12·4·12). Puis on pilote
l'API :

```
POST /api/start                      -> field secteur 1 (+ run_id)
boucle: solve(field) -> moves
        POST /api/submit_path {moves, nonce}  (header X-Run-Token: run_id)
        -> field suivant, ou {status:"won", flag}
```

Scripts : [`solver.py`](solver.py) (règles + BFS) et [`runner.py`](runner.py) (pilotage API).

Résultat :

```
start: HTTP 201 run_id=9508ce... level=1 time_left=60
[L1] OK (32 coups) -> next L2 ...
...
[L50] WON apres 33 coups !  t=10.3s
FLAG: OPENNC{da0b702b-b393-4de6-86a0-e9e896defa3d}
ARCHIVE: Jour 52 — J'ai laissé une route entre les dents de la passe. Pas pour fuir
         Abysséa. Pour permettre à quelqu'un d'y revenir. — É. Varn
```

Les 50 secteurs franchis en **10,3 s** (le serveur régénère un secteur différent à chaque
coup ; le BFS trouve un chemin de 24–41 coups par secteur, toujours < `max_moves`=180).

## Flag

```
OPENNC{da0b702b-b393-4de6-86a0-e9e896defa3d}
```
