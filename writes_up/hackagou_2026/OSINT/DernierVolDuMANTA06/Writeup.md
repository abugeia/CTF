# Le Dernier Vol du MANTA-06 (HacKagou 2026) — OSINT

**Flag :** `OPENNC{...}` *(à compléter)*
**Valeur :** 250 pts · **Auteur :** Ketsui
**Statut :** 🔴 **non résolu, injouable à distance** — nécessite l'instance (interface du
drone). MAJ 2026-10-06 : infra `ctfd-whale` **démontée** post-event (`POST container` →
*Container creation failed*). À reprendre si une instance redevient disponible.

## Énoncé

> Le drone cartographique **MANTA-06** (hors tension, interface de maintenance endommagée) contient en mémoire la **route de cinq balises secrètes**. « Réveillez le MANTA-06, récupérez ce qu'il a vu et ouvrez la **capsule mémoire**. »
> *« Les machines d'Abysséa n'oublient jamais vraiment. Elles apprennent seulement à **mentir**. »* ← indice : certaines données sont **falsifiées / leurres**.

Illustration : `illustrationmanta.png`.

## Reconnaissance / analyse

Mélange OSINT + exploration d'interface embarquée :
- « Réveiller » le drone = déverrouiller/brancher l'interface de maintenance (endpoint, mode debug, creds par défaut).
- « route de 5 balises » → 5 points (coordonnées / photos) à exploiter.
- L'indice « apprennent à mentir » : **méfiance** — des coordonnées/entrées sont des **leurres**, il faut recouper (métadonnées EXIF vs. données affichées, timestamps incohérents).

## Plan de résolution

1. Démarrer l'instance, explorer l'interface du MANTA-06 (routes cachées, logs, firmware, EXIF des images embarquées).
2. Réactiver l'interface de maintenance → accéder à la **mémoire**.
3. Extraire les 5 balises, **écarter les leurres** (recoupement EXIF/horodatage/géoloc).
4. « Ouvrir la capsule mémoire » = reconstituer la route correcte / le code → `OPENNC{...}`.

## Flag

```
OPENNC{...}
```
