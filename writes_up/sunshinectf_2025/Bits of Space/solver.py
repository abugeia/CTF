from pwn import *
import struct

# --- Configuration ---
HOST = "sunshinectf.games"
PORT = 25401
BLOCK_SIZE = 16

# --- Étape 1: Lire le fichier voyager.bin ---
with open("voyager.bin", "rb") as f:
    voyager_data = f.read()

# Les 16 premiers octets sont l'IV, le reste est le ciphertext
iv_ancien = voyager_data[:BLOCK_SIZE]
ciphertext_original = voyager_data[BLOCK_SIZE:]

log.info(f"IV Ancien: {iv_ancien.hex()}")
log.info(f"Ciphertext Original: {ciphertext_original.hex()}")

# --- Étape 2: Reconstruire le plaintext original ---
# Hypothèses basées sur le nom "Voyager" et le code source
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
# On s'intéresse seulement au premier bloc pour modifier l'IV
plaintext_ancien_bloc1 = plaintext_ancien_unpadded[:BLOCK_SIZE]
log.info(f"Plaintext Ancien (Bloc 1): {plaintext_ancien_bloc1.hex()}")

# --- Étape 3: Forger le nouvel IV ---
# On définit notre objectif: le device_id qui donne le flag
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
# Masque_XOR = Plaintext_Ancien XOR Plaintext_Cible
masque_xor = xor(plaintext_ancien_bloc1, plaintext_cible_bloc1)
# IV_Nouveau = IV_Ancien XOR Masque_XOR
iv_nouveau = xor(iv_ancien, masque_xor)
log.success(f"IV Nouveau (forgé): {iv_nouveau.hex()}")

# --- Étape 4: Envoyer le payload et récupérer le flag ---
payload = iv_nouveau + ciphertext_original

r = remote(HOST, PORT)
r.recvuntil(b"packet:\n")
r.send(payload)

response = r.recvall()
log.success(f"Réponse du serveur:\n{response.decode()}")