# Le cousin historien
Catégorie : OSINT — Points : ~192 (dynamique) — Auteur : Ketsui

## Énoncé

> Votre cousin [...] vous envoie une photo prise avec sa toute nouvelle caméra 360°. [...] il vous
> lance un défi : retrouver une sculpture célèbre à proximité de l'endroit où la photo a été prise.
>
> [...] aucune sculpture n'est visible ! [...] Il laisse tout de même un indice mystérieux :
> « C'est une installation lourde de sens pour les habitants, rendant hommage aux familles et à
> cette industrie, aussi difficile qu'importante, qui a tant apporté à la région. »
>
> À l'aide de la photo 360 et de cet indice, trouvez **le nom de la sculpture/installation** en
> utilisant Google Maps.
>
> **Format du flag `OPENNC{nom_de_la_sculture}` — tout en minuscule et `_` pour les espaces.**
>
> Auteur : Ketsui

Pièce jointe : `cousin.png` (photo panoramique équirectangulaire 360°, 16384×8192, ~85 Mo — voir
la version réduite `cousin_360_reduit.png`).

## ⚠️ Correction du write-up précédent

Le write-up initial proposait deux flags qui ont été **REFUSÉS** :
`OPENNC{-38.21,175.87}` (coordonnées) et `OPENNC{The_Pine_Man_of_Tokoroa}`.

Deux erreurs :
1. Le format demandé n'est **pas** des coordonnées GPS mais le **nom** de la sculpture.
2. Le format impose **tout en minuscule** ; `The_Pine_Man_of_Tokoroa` contient des majuscules et
   un `_of_Tokoroa` en trop.

## Résolution

### 1. Géolocalisation de la photo 360

La photo panoramique montre un **rond-point d'un centre-ville** (îlot végétalisé central, panneaux
de circulation à conduite à gauche, commerces). Deux éléments remarquables :

- des **poteaux/tours sculptés en bois** au centre du terre-plein (les « Talking Poles ») ;
- l'architecture et la végétation typiques de **Nouvelle-Zélande**.

Une recherche d'image inversée (Google Lens) sur ces éléments + l'exploration de Google Maps mène
à **Tokoroa** (région du Waikato, Île du Nord, Nouvelle-Zélande) — env. `-38.21, 175.87`.

### 2. Interpréter l'indice

> « installation lourde de sens [...] rendant hommage aux **familles** et à **cette industrie,
> aussi difficile qu'importante**, qui a tant apporté à la région. »

Tokoroa est une **ville forestière** (scierie de Kinleith). L'industrie « difficile mais
importante » est la **sylviculture/exploitation du bois**. La sculpture qui rend hommage aux
familles de bûcherons est **« The Pine Man »** (surnommé *Chainsaw Man*) : une statue d'un
bûcheron tenant sa tronçonneuse, réalisée en 2004 par Peter Dooley (et Joe Wilkinson), au cœur du
*Talking Pole Forest* (Leith Place), le long de la State Highway 1 — donc bien « à proximité » du
rond-point de la photo mais **hors champ** de celle-ci.

Sources : South Waikato District Council (page « The Pine Man » de la série *Talking Poles*),
Te Ara, NZ Herald.

### 3. Flag

Nom officiel de l'installation : **« The Pine Man »**. En appliquant le format (minuscules,
espaces → `_`) :

**Non résolu.** Lieu identifié (statue « The Pine Man » / rond-point de Tokoroa, NZ) mais flag non trouvé. Refusés sur le legacy : `OPENNC{-38.21,175.87}`, `OPENNC{The_Pine_Man_of_Tokoroa}`, `OPENNC{the_pine_man}`, `OPENNC{the_pineman}`. Le format/casse exact reste à déterminer.

Confiance : **probable**. Le lieu (Tokoroa) et la sculpture (*The Pine Man*, hommage à l'industrie
forestière et aux familles de bûcherons) sont **certains** ; seule la forme exacte de la chaîne
reste à confirmer.

### Variantes à tester si `the_pine_man` est refusé
- ``OPENNC{the_pineman}`` (souvent écrit en un seul mot : *The Pineman*)
- ``OPENNC{pineman}``
- ``OPENNC{pine_man}``
- ``OPENNC{the_pine_man_of_tokoroa}`` (version minuscule de l'ancien candidat)

## Fichiers

- `cousin_360_reduit.png` : version réduite de la photo 360 (l'originale fait 85 Mo)
- `image*.png` : captures de la démarche (recherche inversée, Google Maps)
