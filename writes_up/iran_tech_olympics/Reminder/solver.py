#!/usr/bin/env python3
from pwn import *

import re

def extended_gcd(a, b):
    """Returns (gcd, x, y) such that a*x + b*y = gcd"""
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = extended_gcd(b % a, a)
        return (g, x - (b // a) * y, y)

def mod_inverse(a, m):
    """Returns modular inverse of a % m"""
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise Exception('Modular inverse does not exist')
    return x % m

def crt(moduli, remainders):
    """
    Solves the Chinese Remainder Theorem.
    Takes a list of moduli and a list of remainders.
    Returns the smallest positive integer solution.
    """
    if len(moduli) != len(remainders):
        raise ValueError("Lists moduli and remainders must have the same length")

    # The product of all moduli
    N = 1
    for n in moduli:
        N *= n

    result = 0
    for n_i, a_i in zip(moduli, remainders):
        p = N // n_i
        result += a_i * mod_inverse(p, n_i) * p
    
    # We return the result and the total product, just like pwntools' function
    return result % N, N

# Lance le programme localement
# context.log_level = 'debug' # Décommente pour voir tous les échanges en détail
p = process('./Reminder/Remainder')

# Boucle pour répondre à toutes les questions
while True:
    try:
        # On lit la sortie du programme jusqu'à "Question"
        # Le timeout est une sécurité pour ne pas attendre indéfiniment
        output = p.recvuntil(b'Question ', timeout=2)
        p.recvline()
        
        # Initialisation des listes pour le solveur CRT
        remainders = [] # Les restes (ex: 4 dans "x ? 4 mod 13")
        moduli = []     # Les modules (ex: 13 dans "x ? 4 mod 13")

        # Chaque question a 3 équations
        for _ in range(3):
            line = p.recvline().decode()
            
            # On utilise une expression régulière pour extraire les nombres
            # Le motif recherche "x ? [nombre1] mod [nombre2]"
            match = re.search(r'x \? (\d+) mod (\d+)', line)
            
            if match:
                # On ajoute les nombres trouvés à nos listes
                remainders.append(int(match.group(1)))
                moduli.append(int(match.group(2)))

        # On s'assure qu'on a bien 3 équations avant de continuer
        if len(moduli) == 3 and len(remainders) == 3:
            log.info(f"Résolution pour : moduli={moduli}, remainders={remainders}")
            
            # On utilise la fonction crt de pwntools pour trouver la solution
            # Elle retourne (solution, produit des modules), on ne veut que la solution
            solution, n_product = crt(moduli, remainders)
            
            log.success(f"Solution trouvée : {solution}")
            
            # On envoie la réponse au programme
            p.sendline(str(solution).encode())
        else:
            # Si le parsing échoue, on arrête
            log.warning("Impossible de parser la question, fin du script.")
            break

    except EOFError:
        # Le programme s'est terminé, c'est la fin !
        log.success("Le programme s'est terminé. Récupération du flag...")
        break

# Passe en mode interactif pour voir la fin et le flag
p.interactive()

# Alternative si p.interactive() ne montre rien :
# print(p.recvall().decode())