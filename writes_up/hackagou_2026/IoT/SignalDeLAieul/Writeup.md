# Le Signal de l'Aïeul (HacKagou 2026) — IoT

**Flag :** `OPENNC{...}` *(à compléter)*
**Valeur :** 340 pts (dynamique) · **Auteur :** GiGaWaTT · **Statut :** 🔴 **présence physique requise (scan BLE)** — non résoluble à distance.

## Énoncé

> Faibles **signaux hertziens** dérivant sous la surface. Ce sont des **balises de repérage autonomes**
> déployées par le Capitaine Nepo, « basées sur des notes léguées par son ancêtre en **2023** ».
> L'une de ces balises transmet toujours un **code de déverrouillage masqué via un protocole sans-fil de
> proximité** :
> *« De la pierre d'Eddy aux dents bleues, un signal se cache dans les profondeurs »*
> À vous de scanner l'éther, d'isoler la bonne balise et d'extraire la clé cachée.

Illustration : `2026-Signal-Aieul.jpeg`, image Google Imagen **signée C2PA, pixels intacts** → pas de
stégano, ce n'est qu'une illustration. Type CTFd `dynamic`, aucun fichier, aucune instance.

## Analyse (décodage de l'indice)

| Indice | Lecture |
|---|---|
| « pierre d'Eddy » | **Eddy-stone** → **Eddystone**, format de balise BLE de Google, publié en **2015** (le « 2023 » est le millésime du lore HacKagou) |
| « dents bleues » | **Bluetooth** (Harald « à la dent bleue ») → **BLE** |
| « balises … l'une d'elles » | plusieurs balises dans la salle, une seule porte le code → filtrer les trames Eddystone |
| « se cache dans les profondeurs » | le code n'est pas dans le nom affiché : il faut lire le **contenu de la trame** (Eddystone-URL / UID namespace+instance / TLM) voire les **services GATT** |

Aucun challenge BLE/Eddystone dans les write-ups 2023-2025 du repo : rien à recouper à distance.

## Exploitation (à faire sur place)

1. Scanner le BLE avec un smartphone : **nRF Connect** (Android/iOS) ou **Beacon Scanner**, ou sous Linux
   `bluetoothctl scan on` / `btmon`.
2. Repérer les trames dont le service data a l'UUID **`0xFEAA`** (Eddystone) :
   - type `0x10` **Eddystone-URL** → URL compressée (préfixe `0x00`=`http://www.`, `0x03`=`https://`…) ;
   - type `0x00` **Eddystone-UID** → namespace (10 o) + instance (6 o) : décoder en hex → ASCII ;
   - type `0x20` **TLM** → télémétrie, éventuellement détournée.
3. Si rien dans l'annonce, s'y **connecter** (nRF Connect → Connect) et lire les caractéristiques GATT.
4. Décoder la charge utile (hex → ASCII, base64…) → `OPENNC{...}`.

```python
# décodage d'un service data Eddystone (hex récupéré dans nRF Connect)
d = bytes.fromhex("10F803...")          # trame après l'UUID 0xFEAA
if d[0] == 0x10:                         # URL
    pre = ["http://www.","https://www.","http://","https://"][d[2]]
    print(pre + d[3:].decode(errors="replace"))
elif d[0] == 0x00:                       # UID
    print(d[2:12].hex(), d[12:18].hex(), d[2:18])
```

## Flag

```
OPENNC{...}
```
