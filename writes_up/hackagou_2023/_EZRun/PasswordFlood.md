
Notre pirate aurait utilisé un système de codes pour cacher l'un de ses trésors. Nous sommes parvenus à obtenir une liste dont certains des mots de passe sont robustes, tandis que d'autres sont faibles. Il semblerait qu'en distinguant les mots de passe faibles et en prenant le première lettre dans l'ordre de la liste, nous obtiendrions le code tant recherché.

Liste de mots de passe :
- MilleSabords
- Doublons123
- ÎleAuTrésor#Secrète
- Perroquet
- Carte3D#ÎlesPerdues
- \_tresor
- butin123
- 0123456
- Boussole$77Etoile
- unPirate
- longueVue
- Capitaine#Intrépide2023
- 3Iles
- CoffreFort#Rempli$
- taverne
- 7Mers
- TrésorCaché#2023
- epee

_Format du flag : OPENNC{CodeTrouvé}_

## Résolution

On doit déjà trouvé la liste des MDP faibles.

On part du principe qu’un MDP fort contient :
* Majuscule
* Minuscule
* Chiffre
* Caractère spécial
* longueur minimum de 12 caractères

Si le MDP répond à au moins 3 critères on le considère fort.
Ce qui nous laisse avec la liste suivante :
* MilleSabords
* Doublons123
* Perroquet
* \_tresor
* butin123
- 0123456
- unPirate
- longueVue
- 3Iles
- taverne
- 7Mers
- epee

Il ne reste plus qu’à prendre la première lettre de chaque MDP et en déduire le flag.


>[!question]- Spoiler du flag
> OPENNC{MDP_b0ul3t7e}

