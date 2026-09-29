# d0lph1n

Catégorie : Reverse — Points : 100 — Auteur : Yoan

## Énoncé

Un océanographe a téléchargé une pièce jointe suspecte. Depuis, un « malware »
a pris le contrôle de son écran et affiche un dauphin qui se promène
inlassablement. Le programme possède un mécanisme d'arrêt d'urgence si on clique
sur le dauphin, mais la passphrase est inconnue.

Mission : analyser l'exécutable, trouver la passphrase codée en dur et libérer
l'écran.

Format du flag : `OPENNC{Passphrase}`

Pièce jointe : `dolphin_malware`

## Résolution

> Analyse **statique uniquement** — le binaire n'a jamais été exécuté.

### 1. Reconnaissance

```
$ file dolphin_malware
ELF 64-bit LSB pie executable, x86-64, dynamically linked, not stripped
$ readelf -p .comment dolphin_malware
rustc version 1.93.0 ...
```

Binaire **Rust** (~29 Mo), non strippé, application graphique **egui/eframe +
wgpu** (d'où l'animation GPU du dauphin). Les chaînes de l'IHM confirment :

```
Dauphin Malware
Désactivation d'urgence
Entrez la passphrase de désactivation :
Valider
Passphrase incorrecte. Le dauphin reste !
```

### 2. Localisation de la vérification

Les symboles du crate sont conservés :

```
$ nm dolphin_malware | grep dolphin_malware
... _ZN15dolphin_malware4main...
... <dolphin_malware..DolphinApp as eframe..epi..App>::ui ...
```

En désassemblant la fonction `ui`, on trouve une petite routine autonome de
comparaison (appelée `check_passphrase` par objdump) :

```asm
0000000000714100 <check_passphrase>:
  714100: cmp    $0x16,%rsi                 ; longueur == 22 ?
  714104: jne    714130
  714106: movdqu (%rdi),%xmm0               ; input[0..16]
  71410a: movdqu 0x6(%rdi),%xmm1            ; input[6..22]
  71410f: pcmpeqb 0x215a30(%rip),%xmm1      ; == const B
  714117: pcmpeqb 0x214850(%rip),%xmm0      ; == const A
  71411f: pand   %xmm1,%xmm0
  714123: pmovmskb %xmm0,%eax
  714127: cmp    $0xffff,%eax               ; les 16 octets égaux ?
  71412c: sete   %al
  71412f: ret
```

La passphrase fait **22 octets** (`0x16`) et est comparée en SIMD par deux blocs
de 16 octets qui se recouvrent (`[0..16]` et `[6..22]`).

### 3. Extraction des constantes

```
$ objdump -s --start-address=0x214850 --stop-address=0x214860 dolphin_malware
 214850  3ch0l0c4t10n_d3_                 ; input[0..16]
$ objdump -s --start-address=0x215a30 --stop-address=0x215a40 dolphin_malware
 215a30  c4t10n_d3_p01nt3                 ; input[6..22]
```

Recollement (le recouvrement `[6..16]` = `c4t10n_d3_` est cohérent) :

```
3ch0l0c4t10n_d3_ + p01nt3  =  3ch0l0c4t10n_d3_p01nt3   (22 octets)
```

En clair (leet) : **echolocation de pointe** — un clin d'œil au sonar du dauphin.

## Flag

Confiance : **sûr** (lu directement dans la comparaison codée en dur).

Flag : ``OPENNC{3ch0l0c4t10n_d3_p01nt3}``
