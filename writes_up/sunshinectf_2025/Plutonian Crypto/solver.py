import socket
from binascii import unhexlify, hexlify
import string

def xor(a, b):
    return bytes([x ^ y for x, y in zip(a, b)])

def get_ciphertexts(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        
        f = s.makefile('r')
        
        # On lit jusqu'à la ligne de début de transmission
        while True:
            line = f.readline().strip()
            if line == "== BEGINNING TRANSMISSION ==":
                break
        
        f.readline() # On saute la ligne vide
        # On lit les deux chiffrés
        c0_hex = f.readline().strip()
        c1_hex = f.readline().strip()

        print(f"c0_hex: {c0_hex}")
        print(f"c1_hex: {c1_hex}")
        
        return c0_hex, c1_hex

def solve():
    HOST = "chal.sunshinectf.games"
    PORT = 25403
    c0_hex, c1_hex = get_ciphertexts(HOST, PORT)

    if len(c0_hex) % 2 != 0:
        c0_hex = c0_hex[:-1]
    if len(c1_hex) % 2 != 0:
        c1_hex = c1_hex[:-1]
        
    c0 = unhexlify(c0_hex)
    c1 = unhexlify(c1_hex)

    known_plaintext = b"Greetings, Earthlings."
    
    # On va recalculer tout le plaintext à partir du premier bloc
    p_blocks_recovered = [known_plaintext[:16]]
    
    for i in range(1, len(c0) // 16 + (len(c0) % 16 > 0)):
        c0_i = c0[i*16:(i+1)*16]
        c1_prev = c1[(i-1)*16:i*16]
        p_prev = p_blocks_recovered[i-1]
        
        p_i = xor(p_prev, xor(c0_i, c1_prev))
        p_blocks_recovered.append(p_i)
        
    recovered_plaintext = b"".join(p_blocks_recovered)
    
    # On doit tronquer à la bonne longueur
    final_plaintext = recovered_plaintext[:len(c0)]
    
    print(f"Recovered plaintext: {final_plaintext.decode(errors='ignore')}")
    
    # On cherche le flag dans le plaintext
    import re
    match = re.search(r"sun\{[a-zA-Z0-9_-]+\}", final_plaintext.decode(errors='ignore'))
    if match:
        print(f"Flag found: {match.group(0)}")
        flag = match.group(0)
        with open("writes_up/sunshinectf_2025/Plutonian Crypto/wu.md", "a") as f:
            f.write(f"\n\nFlag: {flag}\n")


if __name__ == "__main__":
    solve()