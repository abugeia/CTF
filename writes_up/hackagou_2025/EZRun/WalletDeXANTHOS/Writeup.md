# wallet de XANTHOS
Catégorie : EZRun — Points : 10 — Auteur : non indiqué

## Énoncé
Une partie des fonds détenus par XANTHOS sont stockés sur un wallet de crypto monnaie sécurisé par une seed de 12 mots BIP39.
Celui qui détient ces mots connait la clé privée permettant l'accès aux fonds liés à l'adresse publique.
Un document a été retrouvé sur un disque dur tout y est !

Pièce jointe : [la_seed.odt](la_seed.odt)

Indice gratuit :
> Un petit effort de mémoire... Le 1er octobre 2025, en face du musée du HacKagou se trouvait le stand de la Police Nationale. Ils avaient un accès WiFi. Son SSID : **GOLD**

## Résolution
Un `.odt` est une archive ZIP. On extrait `content.xml` et les images (`python3 -c "import zipfile; zipfile.ZipFile('la_seed.odt').extractall('odt')"`).

**Texte visible** : il faut donner l'adresse publique du wallet de la crypto créée par Billy Markus et Jackson Palmer en 2013, donc **Dogecoin**. Indice sur l'adresse : `Dmy****************************aNN`. Les mots manquants font obligatoirement partie des 2048 mots BIP39.

**QR code** : c'est un objet `loext:qrcode`, doublé d'une image SVG. Son contenu est lisible directement dans le XML (et confirmé en décodant le SVG avec OpenCV, [qr_decode.py](qr_decode.py)) :
```
Word1 during Word3 method snake gadget assault agree Word9 mosquito daring Word12
```

**Cadre de texte caché** (texte blanc en 3 pt en bas de page, style `T12`) :
```
WordX : Inscrit au dos des polos des cyberbleus
WordX : Rendez vous là bas sans passer par la case départ.
WordX : Le Graal ! Il en faut 100 000 000 pour en posséder 1
WordX : le SSID du musée !
Facile maintenant reste à trouver le bon ordre
```

On en déduit les mots, tous présents dans la liste BIP39 :

| Énigme | Mot |
|---|---|
| Dos des polos des « cyberbleus » (Police nationale) | `police` |
| « Allez en prison, ne passez pas par la case départ » (Monopoly) | `prison` |
| 1 BTC = 100 000 000 satoshis | `satoshi` |
| SSID du stand face au musée (indice gratuit) | `gold` |

Il reste à trouver l'ordre dans les emplacements 1, 3, 9 et 12, soit 4! = 24 possibilités. Seul un ordre sur 16 environ passe le checksum BIP39. Pour chaque candidat valide, on dérive l'adresse Dogecoin sur le chemin BIP44 standard `m/44'/3'/0'/0/0` ([solve_wallet.py](solve_wallet.py)) :

```
$ uv run --with bip-utils python solve_wallet.py
MATCH DMyoS437bE7fMKoRXmHHtMdApJvDcj8aNN | prison during satoshi method snake gadget assault agree police mosquito daring gold
```

Un seul ordre passe le checksum, et son adresse correspond bien au motif `Dmy…aNN`. Attention : le document écrit `Dmy`, mais l'adresse réelle commence par `DMy`. Une comparaison sensible à la casse fait échouer la recherche.

Seed : `prison during satoshi method snake gadget assault agree police mosquito daring gold`

Flag : ``OPENNC{DMyoS437bE7fMKoRXmHHtMdApJvDcj8aNN}``
