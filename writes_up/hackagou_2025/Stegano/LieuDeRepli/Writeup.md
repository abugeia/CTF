# Lieu de repli
Catégorie : Stégano — Points : 250 (dynamique, min 150) — Auteur : k3rhu0n

## Énoncé
Ned : Les autorités veulent commencer à faire évacuer, le problème c'est que NEURONA anticipe tout et la population est en grand danger. On a eu tellement de pertes humaines... La MEH a transmis un lieu de repli vers des groupes de réfugiés afin qu'ils puissent se cacher après avoir débarqué de l'avion Airbus A330neo d'[Aircalin](https://www.aircalin.nc/), le message a été intercepté et nous devons absolument voir s'il est suffisamment robuste car j'ai de gros doutes.

Jocelyne : Tu veux que je teste pour voir si le lieu de repli est bien protégé ?

Ned : Oui, trop choc merci à toi. J'ai juste un indice supplémentaire, ce serait le nom d'un Fort...

Jocelyne : OK, je regarde ça !

![A330neo.png](A330neo.png)

Le flag est de la forme : `OPENNC{xxxx}`

Fichier : [A330neo2bis.png](A330neo2bis.png)

## Résolution
La pièce jointe `A330neo2bis.png` est identique à l'image de l'énoncé `A330neo.png` (mêmes chunks IHDR/PLTE/tRNS/IDAT), mais pèse 242 octets de plus. Ces octets se trouvent **après le chunk `IEND`** et commencent par `PK\x03\x04` : c'est une archive ZIP collée à la fin du PNG (`binwalk -e` ou `unzip` la trouvent aussi).

L'archive n'est pas chiffrée (bit 0 du champ *general purpose flag* à 0). Elle contient `lieu.txt` ([solve_repli.py](solve_repli.py)) :

```bash
python3 solve_repli.py
# lieu.txt clair
# 16 Takarunga Road, Devonport, Auckland 0624, New Zealand
```

Takarunga est le nom maori du **Mount Victoria**, à Devonport (Auckland). Au sommet se trouve **Fort Victoria**, batterie construite en 1885 lors de la « Russian Scare » et qui conserve un canon escamotable (*disappearing gun*) de 8 pouces restauré par le Fort Victoria Trust. Cela correspond à l'indice « nom d'un Fort ». (Fort Takapuna, l'autre fort de Devonport, est situé à Narrow Neck, pas sur Takarunga Road.)

Sources : [Mount Victoria (Auckland) — Wikipedia](https://en.wikipedia.org/wiki/Mount_Victoria_(Auckland)), [Devonport Military History Trail](http://www.visitdevonport.co.nz/devonport-military-history-trail/).

Les deux indices du challenge sont payants (80 pts chacun) et n'ont pas été débloqués. Le format exact du flag n'est donc pas confirmé.



Piste complémentaire : le 16-18 Takarunga Road correspond aussi à l'entrée de **North Head / Maungauika Historic Reserve** (bureau DOC au 18 Takarunga Road), dont le fort du sommet s'appelait **Fort Cautley** (1885) ; le site comporte aussi North Battery et South Battery. Le mot « robuste » de l'énoncé suggère peut-être une couche supplémentaire (le fort comme mot de passe d'un autre contenu ?). Les deux indices payants (80 pts) n'ont pas été débloqués.

### Réexamen (vague 3)
- **Différence entre les deux PNG** : `cmp` montre que `A330neo2bis.png` = `A330neo.png` octet pour octet, avec 242 octets en plus après IEND. Aucun pixel, palette (PLTE) ou tRNS ne diffère.
- **LSB, palette, tRNS** : balayage de tous les plans de bits des index de palette et des canaux RGBA, en ordre ligne et colonne ([lsb_scan.py](lsb_scan.py)). Rien de lisible, seulement des motifs `UUUU` dus aux aplats. PLTE (256 couleurs) et tRNS (58 octets) ressemblent à ceux d'un PNG quantifié normal (type TinyPNG).
- **ZIP** : une seule entrée `lieu.txt`, *deflate*, **non chiffrée** (flag 0x0008 = descripteur de données uniquement). Pas de commentaire local ni global. Champs extra : `ux` (uid/gid 0/0) et `UT` (mtime 2025-09-22 05:41:56 UTC, atime 05:43:07). Le texte ne contient rien d'autre que l'adresse.
- **Adresse exacte** : d'après OpenStreetMap/Nominatim, le 16 Takarunga Road est à `-36.82749, 174.81019` (Cheltenham, Devonport). Il se trouve au bout de Takarunga Road, **au pied de North Head / Maungauika** (entrée officielle au 18 Takarunga Road), et non au Mount Victoria (≈ 174.797 E, accessible par Kerr St et Takarunga *Summit* Road). Le fort visé est donc celui de North Head, **Fort Cautley** (1885, « Russian Scare », canons escamotables). Fort Victoria est probablement un faux ami créé par le nom « Takarunga ».
- « suffisamment robuste » / « bien protégé » : il n'y a aucune couche de protection (pas de mot de passe ZIP). C'est probablement un simple élément de narration (le lieu n'était pas protégé).

Candidats, par ordre de probabilité (non validés ; `OPENNC{Fort_Cautley}` a déjà été refusé) :
1. `OPENNC{FortCautley}`
2. `OPENNC{Cautley}`
3. `OPENNC{Fort Cautley}` (avec espace) ou `OPENNC{Maungauika}` si le fort est désigné par le nom du maunga.

Le 16 Takarunga Road est au pied de North Head / Maungauika (et non de Mount Victoria, faux ami « Takarunga »). Le fort du sommet s'appelait **Fort Cautley** ; le flag attend seulement le nom : `Cautley` (refusés : Fort_Victoria, FortVictoria, Fort_Cautley, FortCautley).

Flag : ``OPENNC{Cautley}``
