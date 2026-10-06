# Origine du Léviathan (HacKagou 2026) — OSINT

**Flag :** `OPENNC{...}` *(à compléter)*
**Valeur :** 100 pts · **Auteur :** Ketsui
**Statut :** 🔴 **non résolu, injouable à distance** — nécessite l'instance + les 6 photos à
géolocaliser. MAJ 2026-10-06 : infra `ctfd-whale` **démontée** post-event (`POST container` →
*Container creation failed*). À reprendre si une instance redevient disponible.

## Énoncé

> Dans la Salle des Cartes, **six photographies de la surface** défilent. « Les paysages ont changé. Les repères, eux, sont restés. » Ces photos seraient liées à l'emplacement d'une **antenne de LÉVIATHAN**. Une **archive verrouillée par code**. Mission : examiner les photos et retrouver le **code secret** qui ouvre le scellé. *« Attention prenez en compte la zone d'erreur. »*

Illustration : `hk2026-origine-leviathan.png`.

## Reconnaissance / analyse

Challenge de **géolocalisation OSINT** :
- 6 photos → 6 lieux à identifier (géoguessing : repères, panneaux, relief, bâtiments calédoniens).
- « les repères sont restés » → comparer avec des vues anciennes/actuelles.
- Le **code** dérive probablement de **coordonnées** (de l'antenne, ou d'un point déduit des 6 photos).
- « zone d'erreur » → la réponse doit être **arrondie / tronquée** à une précision donnée (tolérance sur les coordonnées).

## Plan de résolution

1. Démarrer l'instance, récupérer les 6 photos en pleine résolution.
2. Pour chacune : reverse image search + géoguessing (Google Lens, repères locaux NC), noter les coordonnées.
3. Déduire le point cible (antenne) — intersection, moyenne, ou la 6ᵉ photo = la cible.
4. Former le **code** selon le format attendu par la console (coordonnées arrondies à la « zone d'erreur »).
5. Déverrouiller l'archive → `OPENNC{...}`.

## Flag

```
OPENNC{...}
```
