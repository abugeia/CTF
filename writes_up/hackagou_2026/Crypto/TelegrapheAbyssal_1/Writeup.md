# Télégraphe Abyssal [1/2] : Dans tous les sens (HacKagou 2026) — Crypto

**Flag :** `OPENNC{...}` *(bloqué — instance Docker indisponible après l'event)*
**Valeur :** 250 pts (parcours jusqu'à 750) · **Auteur :** \0/ · **Solves :** 3
**Statut :** 🟠 **matériel de décodage récupéré, télégramme inaccessible** (infra conteneurs démontée).

## Énoncé

> Console électromécanique qui imprime une **longue suite de lettres** ; aucune table des
> archives ne la lit directement. « Un bon opérateur devait rester **attentif à tout ce
> qui l'entourait** », « certains messages ne se comprennent pas en regardant **dans une
> seule direction** ». Le télégramme de **votre instance** contient un **code opérateur**
> à présenter au terminal.
> ⚠️ « des informations importantes vous seront transmises par certains moyens de
> communication. Soyez attentifs à ce qui se passera **dans la salle de 15h à 15h30**. »

« Dans tous les sens » + « pas une seule direction » → lecture **multi-directionnelle**
(boustrophédon, transposition par colonnes, rail fence, spirale, miroir).

## Matériel de décodage (indices post-event, coût 0)

Le CTF étant terminé, les deux indices officiels livrent ce qui était **diffusé en salle**
le 1er octobre entre 15h et 15h30 (récupérés via l'API `hints` → `unlocks`) :

- **Indice 1 — totem lumineux** (fond de salle). De 15h à 15h30 il clignotait en **Morse** :
  `court-long, court-long-court-court, court-long-long-court, court-court-court-court,
  court-long, long-court-court-court, court, long`
  → `.- / .-.. / .--. / .... / .- / -... / . / -` → **`A L P H A B E T`**.
- **Indice 2 — bande son** : un morceau particulier,
  [*Universo* (Shamanic Tales)](https://shamanictales.bandcamp.com/track/universo).

Interprétation : le totem donne le mot-clé **ALPHABET** (table/convention de lecture), et
la piste audio est le second « sens » de transmission (*dans tous les sens*). Ces éléments
sont la **clé/convention** à croiser avec le télégramme de l'instance.

## Blocage

Le **télégramme** (suite de lettres propre à l'équipe) n'est lisible **que depuis
l'instance Docker** du challenge. Or, après la fin de l'event, le backend `ctfd-whale`
renvoie `{"success": false, "message": "Container creation failed"}` sur
`POST /api/v1/plugins/ctfd-whale/container?challenge_id=31` (infra conteneurs décommissionnée ;
`challs.hackagou.nc` répond en 301 mais n'expose plus aucun port d'instance).

→ Sans le télégramme, impossible d'appliquer la convention **ALPHABET** / lecture
multi-sens. Résolution à reprendre si une instance redevient disponible.

## Plan (dès qu'une instance est dispo)

1. Démarrer l'instance, récupérer le télégramme.
2. Appliquer la lecture multi-directionnelle en s'appuyant sur **ALPHABET** (p. ex.
   Vigenère/variante à clé `ALPHABET`, ou ordre de lecture).
3. Extraire le **code opérateur**, le présenter au terminal → `OPENNC{...}`.

## Flag

```
OPENNC{...}
```
