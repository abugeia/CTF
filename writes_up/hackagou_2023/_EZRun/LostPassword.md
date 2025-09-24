Un pirate, dont on taira le nom, aurait trouvé l'un des trésors cachés de Capt'N Nepo. Il en aurait profiter pour poser un cadenas afin que notre légendaire pirate ne puisse remettre la main sur le fruit de son dur labeur.

Pouvez-vous aider Capt'N Nepo à ouvrir ce cadenas grâce aux indices fournis par un membre de l'équipage du vil pillard ?

Indices :

- Le mot de passe est composé de 17 caractères.
- Le pirate est né le 12 mars 1985.
- Son film préféré est "Pirates des Caraïbes".
- Il a un chien nommé Massis.
- Il utilise toujours une combinaison de son année de naissance, du nom de son chien et d'un mot lié à son film préféré.

_Format du flag : OPENNC{MotDePasseTrouvé}_

## Résolution

Le but de ce challenge est simplement d’utiliser sa logique pour le résoudre. Tout est dans l’énoncé.

Ce qui nous intéresse pour mettre les informations dans l’ordre : 

>Il utilise toujours une combinaison de son année de naissance, du nom de son chien et d'un mot lié à son film préféré.

* année de naissance : 1985
* nom de son chien : Massis
* film préféré : “Pirates des Caraïbes”, comme il ne peux s’agir que d’un mot parmis les trois, on suppose que c’est “Pirates” qui l’emporte.

On part du principe que l’énoncé nous donne l’ordre dans lequel il faut concaténer les informations, ce qui donne : 1985, massis, pirates.

Il faut également faire attention au format du flag notamment pour la casse : 
> _Format du flag : OPENNC{MotDePasseTrouvé}_

Ce qui donnerait donc en réponse : OPENNC{1985MassisPirates}

On essaye donc le flag qui nous indique que c’est incorrect. Si on part du principe que tout est bon, une seule conclusion possible, il faut modifier l’ordre des composants pour trouver le bon mot de passe.

Et on arrive donc à :

>[!question]- Spoiler du flag
> OPENNC{Massis1985Pirates}

