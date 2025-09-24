Un message codé a été intercepté par Jules, le fils du capitaine.

> BCRAAP{p4rf4e_p1cu3e_15_345l}

Trouvez sa signfication !

## Résolution

Le nom du challenge nous donne un indice, il faut appliquer le code césar pour déchiffrer le message.

Pour le confirmer on peux utiliser [dcode](../../../../ressouces/tools/dcode.md) pour identifier le cypher. Il nous indique dans les plus probables : 
  
* [Caesar Box Cipher](https://www.dcode.fr/caesar-box-cipher
* [Scytale Cipher](https://www.dcode.fr/scytale-cipher

Le cipher de césar arrive bien en tête ce qui confirme nos soupçons. Maintenant place au déchiffrage, on va donc utiliser le site [cyberchef](../../../../ressouces/tools/cyberchef.md).

la méthode pour déchiffrer le code s’appel du ROTX (X équivalent à un chiffre). Le rot le plus utilisé de base est le ROT13.

On essaye donc celui-là en premier et bingo : 
>[!question]- Spoiler du flag
> OPENNC{c4es4r_c1ph3r_15_345y}

