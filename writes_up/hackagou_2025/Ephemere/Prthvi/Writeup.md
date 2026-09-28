# Pṛthvī
Catégorie : Éphémère — Points : 10 — Auteur : \0/

## Énoncé
En sanskrit, pṛthvī (prononcer PRIT-vi) veut dire vaste, étendu.

Cette année, le HacKagou voit grand et s'installe dans l'Arène du Sud !
Mais quelle est donc la surface de l'aire de jeu de ce magnifique lieu ?

![Prthvi](Prthvi.png)

Format du flag : `OPENNC{Surface en cm²}` — par exemple, si la surface est de 30 000 cm², alors le flag est OPENNC{30000}

## Résolution
La page de la Ville de Païta consacrée à l'Arène du Sud contient une **fiche technique** ; pour la grande salle : **Aire de jeu : 1 246 m²**.
Attention à ne pas prendre les autres surfaces (zone public, gradins, VIP…).

Conversion : 1 m² = 100 cm × 100 cm = 10 000 cm², donc 1246 × 10 000 = 12 460 000 cm².

Flag : ``OPENNC{12460000}``

*Source : solution officielle publiée sur legacy.hackagou.nc.*
