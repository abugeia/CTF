# Le Moshpit du Lagon Noir

Catégorie : Stégano — Points : 100 — Auteur : Ketsui

## Énoncé

Un groupe de pirates punks (« Kraken Moshpit ») diffuse sa musique illégalement
sur les fréquences de secours au large de la passe de Dumbéa. La Marine a
intercepté l'affiche numérique de leur prochain concert clandestin, mais leur
« ingénieur » a bidouillé le fichier pour le rendre illisible par les systèmes
standards.

Mission : le mot de passe d'accès au concert (le flag) est écrit en gros sur
l'affiche.

« Punk's not dead, il a juste besoin de branchies. »

Pièce jointe : `Kracken_concert`

## Résolution

### 1. Analyse du fichier

```
$ file Kracken_concert
Kracken_concert: data
$ xxd Kracken_concert | head -1
00000000: 5055 4e4b 5f41 4259 0000 000d 4948 4452  PUNK_ABY....IHDR
```

Le fichier n'est pas reconnu, mais on voit `IHDR` juste après les 8 premiers
octets, puis plus loin `IDAT`/`IEND` : c'est un **PNG dont la signature a été
remplacée**. Les 8 octets `50 55 4E 4B 5F 41 42 59` = `PUNK_ABY` remplacent la
signature PNG standard `89 50 4E 47 0D 0A 1A 0A`.

### 2. Réparation

Il suffit de réécrire les 8 octets de signature :

```bash
printf '\x89\x50\x4e\x47\x0d\x0a\x1a\x0a' | dd of=kracken.png bs=1 count=8 conv=notrunc
file kracken.png
# kracken.png: PNG image data, 2816 x 1296, 8-bit/color RGB, non-interlaced
```

Le PNG s'ouvre alors normalement (chunks IHDR/sRGB/pHYs/IDAT/IEND intacts).

### 3. Lecture

L'affiche « KRAKEN MOSHPIT : ABYSSAL CHAOS » s'affiche, avec le flag écrit en
gros en bas à gauche :

```
OPENNC{PUNKY_C0NC3RT}
```

Voir `kracken_repare.png`.

## Flag

Confiance : **sûr**.

Flag : ``OPENNC{PUNKY_C0NC3RT}``
