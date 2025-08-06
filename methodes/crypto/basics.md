# Cheatsheet : Bases de la Cryptographie

Cette cheatsheet couvre les concepts fondamentaux et les outils courants en cryptographie, souvent rencontrés dans les CTF.

## Chiffres Classiques

### Chiffre de César
*   Décalage simple des lettres de l'alphabet.
*   Outils : CyberChef, scripts Python simples.
*   Exemple : `ABC` avec un décalage de 3 devient `DEF`.

### Chiffre de Vigenère
*   Utilise une clé pour appliquer différents décalages de César.
*   Outils : CyberChef, Vigenere Solver (en ligne), scripts Python.
*   Nécessite de trouver la longueur de la clé (méthode de Kasiski, indice de coïncidence).

### ROT13
*   Un cas spécial du chiffre de César avec un décalage de 13. Appliquer ROT13 deux fois annule l'opération.
*   Outils : `tr 'A-Za-z' 'N-ZA-Mn-za-m'`, CyberChef.

## Hachage (Hashing)

Fonctions à sens unique qui transforment des données en une chaîne de caractères de taille fixe (empreinte numérique).

*   **MD5, SHA1, SHA256, SHA512 :** Algorithmes de hachage courants.
*   **Utilisation :** Vérification d'intégrité, stockage de mots de passe (avec salage).
*   **Outils :** `hashcat`, `john the ripper`, CyberChef, sites de décryptage de hash.

### Attaques courantes
*   **Attaque par dictionnaire :** Tenter de hacher des mots d'un dictionnaire et comparer.
*   **Attaque par force brute :** Tenter toutes les combinaisons possibles.
*   **Rainbow tables :** Tables précalculées de hashs.

## Chiffrement Symétrique

Utilise la même clé pour le chiffrement et le déchiffrement.

*   **AES (Advanced Encryption Standard) :** Le standard actuel, très sécurisé.
    *   Modes : CBC, GCM, CTR, etc.
*   **DES/3DES :** Anciens standards, moins sécurisés pour DES.
*   **Outils :** OpenSSL, PyCryptodome (Python).

### OpenSSL (Exemples)
*   Chiffrer avec AES-256-CBC :
    ```bash
    openssl enc -aes-256-cbc -salt -in plaintext.txt -out ciphertext.enc -k "ma_cle_secrete"
    ```
*   Déchiffrer :
    ```bash
    openssl enc -aes-256-cbc -d -in ciphertext.enc -out decrypted.txt -k "ma_cle_secrete"
    ```

## Chiffrement Asymétrique (Clé Publique/Privée)

Utilise une paire de clés : une clé publique pour chiffrer, une clé privée pour déchiffrer.

*   **RSA :** Algorithme le plus connu. Basé sur la difficulté de factoriser de grands nombres premiers.
    *   Utilisation : Échange de clés, signatures numériques, chiffrement de petites quantités de données.
*   **Diffie-Hellman :** Protocole d'échange de clés.
*   **ECC (Elliptic Curve Cryptography) :** Plus efficace pour la même sécurité que RSA.

### RSA (Concepts clés)
*   **Clé publique :** `(n, e)`
*   **Clé privée :** `(n, d)`
*   `n = p * q` (p et q sont de grands nombres premiers)
*   `e` est l'exposant public, `d` est l'exposant privé.
*   **Attaques :** Factorisation de `n` (si petit), attaques sur `e` ou `d` faibles.

### Outils
*   **OpenSSL :** Génération de clés, chiffrement/déchiffrement RSA.
*   **factordb.com :** Pour factoriser de petits `n`.
*   **RsaCtfTool :** Pour exploiter des vulnérabilités RSA courantes dans les CTF.

## Outils Génériques

*   **CyberChef :** Le "couteau suisse" de la cryptographie et de l'encodage/décoding. Indispensable pour les CTF.
    *   [https://gchq.github.io/CyberChef/](https://gchq.github.io/CyberChef/)
*   **`strings` :** Pour trouver des chaînes de caractères lisibles dans des fichiers binaires ou chiffrés.
*   **`binwalk` :** Pour analyser des fichiers binaires et trouver des signatures de fichiers embarqués (utile pour la stéganographie).
*   **`zsteg` :** Outil de stéganographie pour les images.
*   **`exiftool` :** Pour lire les métadonnées des fichiers.