# Plutonian Crypto - SunshineCTF 2025

## Analyse

Le challenge nous fournit un script Python, `main.py`, qui se connecte à un service distant. Ce service envoie un message chiffré de manière répétée.

L'analyse du script `main.py` révèle que le chiffrement utilisé est l'AES en mode CTR (Counter). Une clé (`KEY`) et un nonce (`NONCE`) sont générés aléatoirement une seule fois. Ensuite, le script entre dans une boucle infinie où il chiffre continuellement le même message (`MESSAGE`).

La vulnérabilité se trouve dans la manière dont le compteur du mode CTR est géré. À chaque itération de la boucle, le compteur est incrémenté de 1, mais le chiffrement est réinitialisé.

Soit `C_i` le chiffré à l'itération `i` et `P` le message en clair.
Soit `KS_i` le keystream à l'itération `i`.

Nous avons :
- `C_0 = P ⊕ KS_0`
- `C_1 = P ⊕ KS_1`

Le keystream pour le mode CTR est généré en chiffrant le nonce concaténé avec la valeur du compteur.
- `KS_0 = AES(KEY, NONCE||0) || AES(KEY, NONCE||1) || ...`
- `KS_1 = AES(KEY, NONCE||1) || AES(KEY, NONCE||2) || ...`

On peut voir que le keystream `KS_1` est simplement le keystream `KS_0` décalé d'un bloc. Si on divise les messages en blocs de 16 octets, on a la relation suivante pour le j-ème bloc :

`KS_1_{j-1} = KS_0_j`

## Exploitation

En utilisant cette relation, nous pouvons établir un lien entre les chiffrés et les blocs de clair :

`C_0_j = P_j ⊕ KS_0_j`
`C_1_{j-1} = P_{j-1} ⊕ KS_1_{j-1} = P_{j-1} ⊕ KS_0_j`

En faisant un XOR entre ces deux équations, le terme `KS_0_j` s'annule :

`C_0_j ⊕ C_1_{j-1} = (P_j ⊕ KS_0_j) ⊕ (P_{j-1} ⊕ KS_0_j) = P_j ⊕ P_{j-1}`

De là, on peut déduire la relation qui nous permet de retrouver chaque bloc de clair `P_j` si on connaît le précédent `P_{j-1}` :

`P_j = P_{j-1} ⊕ C_0_j ⊕ C_1_{j-1}`

Le challenge nous donne une information cruciale : le début du message est `"Greetings, Earthlings."`. Cela correspond à plus d'un bloc de 16 octets. Nous connaissons donc `P_0` et le début de `P_1`. Cela suffit pour démarrer la réaction en chaîne et déchiffrer le message complet.

## Solution

Le script `solver.py` implémente cette logique :
1.  Il se connecte au service `chal.sunshinectf.games:25403`.
2.  Il lit et ignore le "banner" de connexion pour récupérer les deux premiers chiffrés consécutifs (`c0` et `c1`).
3.  Il initialise le premier bloc de clair `p_0` avec les 16 premiers octets du message connu (`"Greetings, Earth"`).
4.  Il applique itérativement la formule `P_j = P_{j-1} ⊕ C_0_j ⊕ C_1_{j-1}` pour retrouver tous les blocs suivants du message.
5.  Il concatène les blocs pour reconstituer le message complet et en extrait le flag.

Le message déchiffré est :
```
Greetings, Earthlings. It has come to our attention that you have chosen to downgrade our mighty planet to the status of 'dwarf'. Let it be known that although we are small, the Plutonian space navy will not stand idly by and accept such disrespect. Please contact us to discuss the terms of Earth's surrender before we arrive in approximately 10 years. Use this transmission code: sun{n3v3r_c0unt_0ut_th3_p1ut0ni4ns}
```

## Flag

`sun{n3v3r_c0unt_0ut_th3_p1ut0ni4ns}`
