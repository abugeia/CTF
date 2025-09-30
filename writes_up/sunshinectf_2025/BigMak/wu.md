## Write-up 1 — BigMak (Colemak)

### Énoncé
On te donne : `rlk{blpdfp_iajylg_iyi}`. Indice “BigMak / Coleson” → Colemak. Objectif : retrouver le texte voulu (flag) en remappant Colemak → QWERTY.

### Étapes (très synthétiques)
1.  Construire la table de correspondance Colemak→QWERTY.
2.  Remplacer chaque lettre selon le mapping (conserver `{ } _`).
3.  Lire le résultat.

### Script (`decode_colemak.py`)
```python
#!/usr/bin/env python3
# Remplace les caractères tapés en Colemak par leurs équivalents QWERTY.
s = "rlk{blpdfp_iajylg_iyi}"

q_top, c_top = "qwertyuiop", "qwfpgjluy;"
q_mid, c_mid = "asdfghjkl;", "arstdhneio"
q_low, c_low = "zxcvbnm,./", "zxcvbkm,./"

m = {}
for q,c in zip(q_top,c_top): m[c]=q
for q,c in zip(q_mid,c_mid): m[c]=q
for q,c in zip(q_low,c_low): m[c]=q
m.update({k.upper():v.upper() for k,v in m.items()})
for ch in "{}_0123456789-.:,/@": m.setdefault(ch, ch)

print(''.join(m.get(ch, ch) for ch in s))
```

### Flag trouvé
**`sun{burger_layout_lol}`**