Here is a code to one of our relays, can you reach the others?

nc sunshinectf.games 25401

# Write-up : Bits of Space (SunshineCTF 2025)

**Challenge :** Bits of Space
**Catégorie :** Cryptographie
**Description :** Here is a code to one of our relays, can you reach the others?
**Fichiers :** `server.py`, `voyager.bin`

---

## tl;dr

Le challenge se présente comme une attaque par **Padding Oracle** sur de l'AES-CBC, mais c'est un piège. La vérification de la structure des données déchiffrées (`struct.unpack`) rend l'oracle inutilisable. La véritable solution consiste à utiliser le fichier `voyager.bin` comme un ciphertext connu pour mener une attaque par **CBC Bit-Flipping**, en modifiant l'IV pour changer le `device_id` dans le premier bloc du plaintext.

---

## 1. Analyse Initiale et le Faux-Fuyant

À première vue, le code `server.py` semble être un cas d'école pour une attaque par Padding Oracle. Le serveur déchiffre les données reçues en AES-CBC et un bloc `try...except` renvoie un message d'erreur générique (`Invalid subscription. Access denied.`) en cas de problème. Cette différence de comportement (erreur vs. pas d'erreur) est habituellement l'oracle dont on a besoin.

Le but est de forger un message qui, une fois déchiffré, contient le `device_id` `0xdeadbabe` pour obtenir le flag.

Cependant, cette piste est un piège magnifiquement conçu. Après le déchiffrement et la suppression du padding, le code exécute cette ligne :

```python
device_id, start, end, channel = struct.unpack("<IQQI", plaintext)
```

Cette fonction exige que le plaintext ait une taille exacte de 24 octets. Or, une attaque par Padding Oracle standard fonctionne en créant des paddings valides de tailles variables (\x01, \x02\x02, etc.), ce qui produit des plaintexts de tailles différentes de 24 (par exemple, 31, 30, ... octets).

Conclusion : struct.unpack lèvera systématiquement une exception, renvoyant toujours le même message d'erreur. L'oracle est donc cassé et inutilisable. Il fallait chercher ailleurs.

2. La Vraie Vulnérabilité : Le Fichier voyager.bin
La clé de l'énigme est le second fichier fourni : voyager.bin. Il s'agit d'un ciphertext connu, c'est-à-dire un exemple de communication légitime chiffrée. Cela ouvre la porte à une attaque par CBC Bit-Flipping.

Le principe du déchiffrement en CBC est : $P_i = D_k(C_i) \oplus C_{i-1}$.

Cela signifie que le plaintext d'un bloc $P_i$ dépend du ciphertext du bloc précédent $C_{i-1}$. En tant qu'attaquant, si nous modifions $C_{i-1}$, nous pouvons contrôler précisément la modification dans $P_i$. Pour le premier bloc de plaintext $P_1$, son "bloc précédent" est le Vecteur d'Initialisation (IV).

Notre objectif est de modifier le device_id qui se trouve dans le premier bloc de plaintext. Nous allons donc modifier l'IV.

3. Plan d'Attaque
Étape 1 : Analyse de voyager.bin
Ce fichier de 48 octets contient :

Les 16 premiers octets : l'IV original (IV_ancien).

Les 32 octets suivants : le ciphertext original (Ciphertext_original).

Étape 2 : Reconstruction du Plaintext Original
C'est l'étape la plus créative. Le nom "Voyager" est l'indice principal. Nous devons deviner le contenu du message en nous basant sur la structure <IQQI.

start : Le timestamp de lancement d'une sonde Voyager. Prenons Voyager 2, lancée le 20 août 1977, ce qui correspond au timestamp Unix 240994800.

end : On peut raisonnablement supposer 0.

channel : On peut supposer 1 (un des canaux valides).

device_id : On peut supposer l'un des ID valides, par exemple 0x13371337 ("Status Relay").

Nous avons maintenant une hypothèse très solide pour le Plaintext_ancien.

Étape 3 : Création du Payload Malicieux
Nous voulons changer le device_id en 0xdeadbabe. Nous appliquons la formule du bit-flipping sur l'IV :

IV_nouveau = IV_ancien ⊕ Plaintext_bloc1_ancien ⊕ Plaintext_bloc1_cible

On construit le premier bloc du plaintext ancien (avec device_id = 0x13371337).

On construit le premier bloc du plaintext cible (avec device_id = 0xdeadbabe).

On XOR les deux pour obtenir un masque de modification.

On XOR ce masque avec l'IV ancien pour obtenir notre IV forgé.

Étape 4 : Exécution
Le payload final à envoyer au serveur est IV_nouveau || Ciphertext_original. Le serveur utilisera notre IV malicieux pour déchiffrer le ciphertext original, et le device_id sera celui que nous avons choisi, nous donnant accès au flag.

4. Le Script Final
Python

from pwn import *
import struct

# --- Configuration ---
HOST = "sunshinectf.games"
PORT = 25401
BLOCK_SIZE = 16

# --- Étape 1: Lire le fichier voyager.bin ---
with open("voyager.bin", "rb") as f:
    voyager_data = f.read()

iv_ancien = voyager_data[:BLOCK_SIZE]
ciphertext_original = voyager_data[BLOCK_SIZE:]

log.info(f"IV Ancien: {iv_ancien.hex()}")
log.info(f"Ciphertext Original: {ciphertext_original.hex()}")

# --- Étape 2: Reconstruire le plaintext original ---
DEVICE_ID_ANCIEN = 0x13371337
# Timestamp du lancement de Voyager 2 (20 août 1977)
TIMESTAMP_START = 240994800
TIMESTAMP_END = 0
CHANNEL = 1

plaintext_ancien_unpadded = struct.pack(
    '<IQQI',
    DEVICE_ID_ANCIEN,
    TIMESTAMP_START,
    TIMESTAMP_END,
    CHANNEL
)
plaintext_ancien_bloc1 = plaintext_ancien_unpadded[:BLOCK_SIZE]
log.info(f"Plaintext Ancien (Bloc 1): {plaintext_ancien_bloc1.hex()}")

# --- Étape 3: Forger le nouvel IV ---
DEVICE_ID_CIBLE = 0xdeadbabe

plaintext_cible_unpadded = struct.pack(
    '<IQQI',
    DEVICE_ID_CIBLE,
    TIMESTAMP_START,
    TIMESTAMP_END,
    CHANNEL
)
plaintext_cible_bloc1 = plaintext_cible_unpadded[:BLOCK_SIZE]
log.info(f"Plaintext Cible (Bloc 1):  {plaintext_cible_bloc1.hex()}")

# On applique la formule du bit-flipping
masque_xor = xor(plaintext_ancien_bloc1, plaintext_cible_bloc1)
iv_nouveau = xor(iv_ancien, masque_xor)
log.success(f"IV Nouveau (forgé): {iv_nouveau.hex()}")

# --- Étape 4: Envoyer le payload et récupérer le flag ---
payload = iv_nouveau + ciphertext_original

r = remote(HOST, PORT)
r.recvuntil(b"packet:\n")
r.send(payload)

response = r.recvall()
log.success(f"Réponse du serveur:\n{response.decode()}")
Conclusion
Ce challenge était une superbe leçon sur les fausses pistes et l'importance de l'analyse de tous les artéfacts fournis. Il démontre qu'une implémentation cryptographique peut être théoriquement correcte, mais rendue vulnérable par la manière dont elle est utilisée (ici, en fournissant un exemple de communication chiffrée).