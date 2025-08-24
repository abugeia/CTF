
Il semblerait que le vieux briscard des mers qui s'amuse à cacher ses trésors à droite, à gauche, aurait laissé un indice dans son portrait. Saurez-vous le trouver ?

![ellesbe](ellesbe.png)]


## Résolution

On utilise exiftool pour voir s’il y aurait quelque chose dans les métadata. Malheureusement rien pour nous ici.

pas mieux non plus avec un `binwalk`.

On effectue un file sur le fichier et on découvre que : `ellesbe.png: PNG image data, 960 x 1200, 8-bit/color RGBA, non-interlaced` c’est une image en 8bit.
Ce qui veux dire que des messages pourraient être caché et donc révélé avec le bon filtre d’une certaine couleur.

On va passer sur un outil qui fait plus de vérifications : [stegoveritas](../../../../ressouces/tools/stegoveritas.md). Il va aussi effectuer les 256 filtres de couleurs sur l’image et nous fournir les résultats dans un dossier.

Et c’est là qu’on voit dan l’une d’elle…


>[!question]- Spoiler du flag
> OPENNC{57eG4n0_0bfU5c4710n}

