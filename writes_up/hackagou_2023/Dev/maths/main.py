from pwn import *
import base64

conn = remote('ctf2023challs.hackagou.nc', 5006)
for i in range(200):
    conn.recvuntil(b'200) ')
    b64 = conn.recvuntil(b'\n')
    conn.recvuntil(b'>> ')
    result = str(eval(base64.b64decode(b64)))
    log.info(f"{i+1}/200 | {base64.b64decode(b64).decode()} = {result}")
    conn.sendline(result.encode('utf-8'))
conn.recvline().decode()
conn.recvline().decode()
conn.recvline().decode()
print(conn.recvline().decode())