# Piste froide
Catégorie : Enquête — Points : 250 (dynamique, min 150) — Auteur : Yoan

## Énoncé
Dernière transmission de Tauira, reçue par le MEH sur un canal sécurisé :

> « Ned, Jocelyne... j'ai mis la main sur quelque chose. Juste avant que NEURONA ne purge les serveurs de développement de XANTHOS, j'ai réussi à exfiltrer deux fragments de données : une brève capture du trafic réseau d'un des développeurs et une archive chiffrée contenant ses communications internes. Je n'ai pas eu le temps de l'analyser, je suis en train de couvrir mes traces. La clé de tout est là-dedans, j'en suis sûr. Le mot de passe de l'archive est quelque part dans le trafic réseau. Une fois dedans, vous trouverez un journal de communications... fragmenté, chiffré. Le développeur utilisait une clé, mais il l'a supprimée pour se protéger. Vous devrez la retrouver. Faites vite, NEURONA sait que des données ont fuité. »

Pièces jointes : [comms_capture.pcapng](comms_capture.pcapng), [classified_intel.7z](classified_intel.7z)

## Résolution

### 1. La capture réseau
143 paquets, tout en loopback. On réassemble les flux TCP avec scapy ([pcap_extract.py](pcap_extract.py), `uv run --with scapy python pcap_extract.py`) :

- **FTP** (port 2121, pyftpdlib) : `USER dev_xanthos` / `PASS Sup3rS3cr3t123!`, puis un `NLST` qui liste `capture.py, comms_capture.pcapng, corporate_logo.png, meme.png, password.txt`. Le fichier `password.txt` n'est jamais téléchargé, et `Sup3rS3cr3t123!` **n'ouvre pas** l'archive (`LZMAError: Corrupt input data`). C'est un leurre.
- **HTTP** (port 8080, SimpleHTTP) : `GET /meme.png` (RGB, métadonnées XMP « Made with Google AI ») et `GET /corporate_logo.png` (logo XANTHOS en RGBA, alpha à 255 partout).

On isole les deux PNG en coupant l'en-tête HTTP (`\r\n\r\n`).

### 2. Stégano LSB dans corporate_logo.png
Le listing FTP laisse penser que `password.txt` a été caché quelque part. On teste plusieurs extractions LSB (ordre des canaux, parcours ligne ou colonne, ordre des bits). La bonne combinaison est **LSB des canaux R, G, B, image parcourue colonne par colonne, bits en LSB-first**. On y trouve un en-tête de 4 octets suivi d'un **ZIP** (`PK\x03\x04 … password.txt`) :

```
$ uv run --with pillow --with numpy python stego_extract.py
header: b'\x0c\x00\x00\x00\x93'
password.txt b'N3URONA_C2_K3Y_R3C0V3RY'
```

([stego_extract.py](stego_extract.py))

### 3. L'archive
```
uv run --with py7zr python -c "import py7zr; py7zr.SevenZipFile('classified_intel.7z', password='N3URONA_C2_K3Y_R3C0V3RY').extractall('intel')"
```
→ `disk.img` (50 Mo, ext4, non copié ici). On l'inspecte avec `debugfs`, sans montage :

```
$ debugfs -R "rdump /home fs" intel/disk.img
fs/home/dev/.config/neurona_client/session.log
```
```
[INFO] Client session started.
[DATA] Fragment 68/50: MWdl9A==
[DATA] Fragment 97/50: Jija0+nOfm
[DATA] Fragment 29/50: VdzaTRA4Vi
[DATA] Fragment 76/50: m6YwjzPz5N
[DATA] Fragment 34/50: 0XRvXKsM11
[INFO] Session terminated.
```

C'est le journal fragmenté : du base64 découpé en morceaux.

### 4. La clé supprimée
`lsdel` ne trouve rien, mais le fichier supprimé a laissé son contenu dans les blocs libres. Un `strings` sur l'image suffit :

```
$ strings -n 5 intel/disk.img | grep XANTHOS
XANTHOS_C2_KEY::
::XANTHOS_KEY_END
```

À l'offset 41943040 (bloc 40960), entre les deux marqueurs, se trouvent **34 octets** :
`1a8c9f035e7b2d6f8a113b9d4c0f2e557799bbddff1032547698badcfe0102034489`

### 5. Déchiffrement
Les 5 fragments mis bout à bout font 48 caractères base64, soit 34 octets décodés : la même longueur que la clé. C'est donc un XOR octet par octet. Le fragment `…==` va forcément à la fin. On teste les 24 ordres possibles des 4 autres et on ne garde que les résultats ASCII ([journal_decrypt.py](journal_decrypt.py)) :

```
key 34 1a8c9f035e7b2d6f8a113b9d4c0f2e557799bbddff1032547698badcfe0102034489
[29, 76, 97, 34, 68] b'OPENNC{F0r3ns1cs_Ch41n_C0mpl3t3d!}'
```

Flag : ``OPENNC{F0r3ns1cs_Ch41n_C0mpl3t3d!}``
