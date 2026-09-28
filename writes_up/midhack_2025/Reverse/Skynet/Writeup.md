# Skynet (MidHack 2025)

Catégorie : Reverse — Points : 100 — Auteur : HacKagou / MidHack (k3rhu0n)

## Énoncé

Ned : Tu te souviens de Skynet dans le film Terminator ?

Jocelyne : Oh oui, un vieux film, mais quand même tu crois que c'est possible qu'une IA puisse s'attaquer ainsi à nous ?

Ned : Fieu ben là je sais pas. En tous cas Tauira il m'a parlé d'une **passphrase** avant d'aller en Australie. Il m'a dit que c'était un **SHA256** qui pouvait déverrouiller un coffre numérique. Dans ce coffre, des infos sur les alertes qu'il avait lancées vers le staff du HacKagou qui ont codé des algos qui semblent faire n'importe quoi.

Jocelyne : Et comment on fait pour avoir ce hash ?

Ned : Ben y'a un script Python que j'ai retrouvé dans le Backup, je pense que c'est là qu'il faut chercher. Tu t'en charges ?

Jocelyne : Okay !

![Logo_Terminator](midhack_chall03_Terminator_Logo.png)

Format du flag : `Valeur_SHA256`

Fichier fourni : `skynet.py`

## Résolution

Le script (voir `skynet.py` joint) lit une valeur hex saisie par l'utilisateur, la XOR
avec la clé répétée `CAFEBABE` (octets `CA FE BA BE`), puis compare le résultat à une
cible fixe :

```python
hex2 = "CAFEBABE"
key = (bytes2 * (len(bytes1) // len(bytes2) + 1))[:len(bytes1)]
xor_result = bytes([b1 ^ b2 for b1, b2 in zip(bytes1, key)])
if hex_result.lower() == "7cd180b961130ba45ecdc21d0bccd308317eee977775f3c261ba270482a6fdeb":
    print("Congrats Dude, got it!!!")
```

Le XOR étant sa propre inverse, la valeur attendue en entrée (la passphrase = le SHA256)
se retrouve directement en XORant la cible avec la même clé :

```python
target = bytes.fromhex("7cd180b961130ba45ecdc21d0bccd308317eee977775f3c261ba270482a6fdeb")
k = bytes.fromhex("CAFEBABE")
key = (k * (len(target) // len(k) + 1))[:len(target)]
res = bytes([a ^ b for a, b in zip(target, key)])
print(res.hex())
# b62f3a07abedb11a943378a3c13269b6fb805429bd8b497cab449dba48584755
```

Aucune exécution du script fournie n'est nécessaire : le calcul est purement statique
(reversing du XOR). La cible fait 32 octets, donc la valeur retrouvée fait bien 64
caractères hex — cohérent avec un SHA256.

Le flag est cette valeur SHA256 (le format du flag est directement la valeur, sans
enveloppe `OPENNC{}`).

Flag : ``b62f3a07abedb11a943378a3c13269b6fb805429bd8b497cab449dba48584755``
