# SunshineCTF 2025 - Numbers Game

## Analyse du binaire

Le challenge nous fournit un binaire ELF 64-bit non strippé. Une première analyse avec `strings` nous donne des informations intéressantes :

```
Let's make a deal! If you can guess the number of fingers I am holding up behind my b
back, I'll let you have my flag.
[4mHint: I am polydactyl and have 18,466,744,073,709,551,615 fingers.
[31mError with input.
%llu
cat flag.txt
[31mWRONG!!! Maybe next time?
```

On comprend qu'il s'agit d'un jeu de devinette. L'indice `18,466,744,073,709,551,615` correspond à la valeur maximale d'un entier non signé de 64 bits. Une première tentative en envoyant ce nombre échoue.

## Désassemblage

En désassemblant la fonction `main` avec `objdump`, on découvre la logique de génération du nombre :

```c
<main>:
    ...
    call   <time@plt>
    mov    edi,eax
    call   <srand@plt>
    call   <rand@plt>
    movsxd rbx,eax
    call   <rand@plt>
    cdqe
    shl    rax,0x1f
    or     rbx,rax
    call   <rand@plt>
    cdqe
    shl    rax,0x3e
    or     rax,rbx
    mov    QWORD PTR [rbp-0x18],rax
    ...
```

Le programme initialise le générateur de nombres aléatoires avec le timestamp actuel (`time(NULL)`), puis combine trois appels à `rand()` pour former un nombre de 64 bits.

## Solution

Pour résoudre le challenge, il faut prédire la séquence de nombres générés par `rand()`. Comme la `libc` de Windows (`msvcrt.dll`) et celle de Linux ne sont pas identiques, la solution la plus fiable est de reproduire la logique de génération dans un programme C, de le compiler avec `gcc` sous WSL, puis de l'appeler depuis un script Python.

Voici le code du générateur C (`generator.c`) :

```c
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <timestamp>\n", argv[0]);
        return 1;
    }

    long long timestamp = atoll(argv[1]);
    srand(timestamp);

    long long rand1 = rand();
    long long rand2 = rand();
    long long rand3 = rand();

    long long number_to_guess = (rand3 << 62) | (rand2 << 31) | rand1;

    printf("%lld\n", number_to_guess);

    return 0;
}
```

Et voici le script Python final (`solver.py`) qui utilise ce générateur :

```python
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
```

En exécutant le script, on obtient le flag.

## Flag

`sun{I_KNOW_YOU_PLACED_A_MIRROR_BEHIND_ME}`
