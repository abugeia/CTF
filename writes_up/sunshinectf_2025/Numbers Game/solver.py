from pwn import *
import time
import subprocess

# Boucle pour tester plusieurs timestamps
for i in range(-2, 3):
    try:
        # Connexion au serveur
        r = remote('chal.sunshinectf.games', 25101)

        # Obtenir l'heure actuelle et l'ajuster
        server_time = int(time.time()) + i
        
        # Appeler le générateur C via WSL pour obtenir le nombre
        command = f"wsl -e bash -c \"'/mnt/d/perso/hackagou/writes_up/sunshinectf_2025/Numbers Game/generator' {server_time}\""
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        number_to_guess = int(result.stdout.strip())

        # Recevoir le message de bienvenue
        r.recvuntil(b'fingers.', timeout=2)

        # Envoyer le nombre
        r.sendline(str(number_to_guess).encode())

        # Afficher la réponse
        response = r.recvall(timeout=2).decode()
        print(f"Trying with timestamp offset {i}:")
        print(response)

        # Si le flag est trouvé, on arrête
        if "sun{" in response:
            print("Flag found!")
            with open("writes_up/sunshinectf_2025/Numbers Game/flag.txt", "w") as f:
                f.write(response)
            break
            
        r.close()

    except Exception as e:
        print(f"Erreur avec le timestamp offset {i}: {e}")
        if 'r' in locals() and r:
            r.close()