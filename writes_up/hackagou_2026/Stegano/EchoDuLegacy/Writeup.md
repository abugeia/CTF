# Echo du Legacy (HacKagou 2026) — Stégano

**Flag :** propre à chaque instance (3 instances décodées, voir [Flag](#flag))
**Valeur :** 250 pts · **Auteur :** \0/
**Statut :** ✅ flag correct — la plateforme répond `partial` (« all team members must submit a flag ») : chaque membre de l'équipe doit soumettre le sien.

## Énoncé

![Ancien inventaire retrouvé dans les Archives du Nautile](2026_EchoDuLegacy.webp)

> Dans les **Archives du Nautile**, NÉRÉIDE vient de remettre la main sur un étrange inventaire technique. À première vue, rien de remarquable : une succession de pièces, d'instruments et de composants consignés dans un vieux registre. Pourtant, certains éléments semblent avoir été ajoutés bien après la rédaction du document.
>
> NÉRÉIDE a également identifié une provenance inattendue : ces ajouts feraient référence aux anciennes éditions du HacKagou. […] une partie de ces archives est toujours accessible sur legacy.hackagou.nc.
>
> *« Le passé pourrait bien vous indiquer comment lire le présent. »*
>
> **Mission :** analysez le texte fourni par votre instance, retrouvez ce que les anciennes archives peuvent vous apprendre et reconstituez le flag.
>
> **Format :** `OPENNC{XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX}`

Challenge `dynamic_docker` : l'instance (`http://challs.hackagou.nc:<port>`) sert une page HTML « Archive textuelle » contenant un unique paragraphe (copie : [instance.html](instance.html)) :

> Premier bordereau montre un **guide**, avec **ensemble**, près de **laiton**, tandis qu'une annotation signale un **karst**. Figure aussi un **capteur**, **nautile**, **gyroscope**, puis un **journal**. Une seconde page mentionne un **joint**, plus bas revient un **luminaire**, un **pupitre**, **dossier**. Reste encore un **extracteur**, puis un **boulon**, avant d'inspecter un **nœud**, sur une ligne nettement marquée **bouchon**. Ensuite **instrument** rejoint un **noyau**, tout près d'un autre **jerrican**, **automate**, une marge ancienne signale aussi **injecteur**. Mécanicien examine un **kit**, **galet**, et **fusible**. Avant classement demeure un **ballast**, près de **coffret**, avec enfin un **horodateur**, un **embout**, une note effacée cite encore **faisceau**, **numéro**, bordereau final garde encore **hauban**, et enfin **palier**.

## Reconnaissance

- Le format du flag est un **UUID** : 32 chiffres hexadécimaux.
- En retirant les mots de liaison (« Premier bordereau montre un… », « tandis qu'une annotation signale… »), il reste **exactement 32 noms d'objets**.
- Leurs initiales : `G E L K C N G J J L P D E B N B I N J A I K G F B C H E F N H P`. Toutes sont comprises entre **A et P**, soit **16 lettres** : une par chiffre hexadécimal. Pour des noms communs français pris au hasard, ce ne serait quasiment jamais le cas.
- Le clin d'œil aux anciennes éditions : **PasswordFlood (HacKagou 2023)**, dont la solution consistait déjà à « prendre la première lettre de chaque mot de passe ». Les « éléments ajoutés » sont les objets de l'inventaire, et le passé indique comment les lire : par leur initiale.

## Exploitation

Correspondance lettre → nibble : `A=0, B=1, …, J=9, K=a, L=b, M=c, N=d, O=e, P=f`.

| Groupe | Objets | Initiales | Hex |
|---|---|---|---|
| 1 | guide ensemble laiton karst capteur nautile gyroscope journal | G E L K C N G J | `64ba2d69` |
| 2 | joint luminaire pupitre dossier | J L P D | `9bf3` |
| 3 | extracteur boulon nœud bouchon | E B N B | `41d1` |
| 4 | instrument noyau jerrican automate | I N J A | `8d90` |
| 5 | injecteur kit galet fusible ballast coffret horodateur embout faisceau numéro hauban palier | I K G F B C H E F N H P | `8a6512745d7f` |

Validation : le résultat est un **UUIDv4** bien formé. Le 13e chiffre vaut `4` (la version) et le 17e vaut `8` (une valeur autorisée, parmi `8`, `9`, `a`, `b`). Avec des initiales prises au hasard, ça n'arriverait qu'environ une fois sur 64, ce qui confirme la lecture.

Script : [decode.py](decode.py). Il accepte l'URL de l'instance, un fichier (texte brut ou HTML) ou `-` pour coller le texte sur l'entrée standard :

```bash
python3 decode.py http://challs.hackagou.nc:<port>/
python3 decode.py instance.html
# OPENNC{64ba2d69-9bf3-41d1-8d90-8a6512745d7f}
```

Les mots de liaison changent d'une instance à l'autre (« Premier bordereau montre un… » ici, « Ancien registre cite un… » ailleurs). Le script n'en dépend donc pas : il s'appuie sur la structure du gabarit, où **chaque segment entre virgules ou points se termine par un objet**. Seule exception, la tournure « Ensuite *instrument* rejoint un *noyau* », qui porte deux objets. Le script essaie alors d'insérer le 2e mot de ce type de segment. Il garde l'insertion qui produit un UUIDv4 valide, celle en position 16 (début du 4e groupe) en cas d'ambiguïté. Testé sur trois instances ([instance.html](instance.html), [instance2.txt](instance2.txt), [instance3.txt](instance3.txt)) :

```
instance.html → OPENNC{64ba2d69-9bf3-41d1-8d90-8a6512745d7f}
instance2.txt → OPENNC{e09501af-15ae-42e9-bb22-de163e06ab0d}
instance3.txt → OPENNC{3eebecfc-6d99-4158-9e1a-7c8833f0c4e7}
```

## Notes

- **Fausse piste : l'image.** `2026_EchoDuLegacy.webp` est un VP8 lossy à chunk unique, sans EXIF/XMP ni données ajoutées. On y lit un registre « Inventaire – Le Legacy » (Disque 12, Compas 27, Manomètre 31, Accouplement 46, Fusible 53, Boîtier 68, Levier 71), des « Observations » signées E.V., et la plaque « Les archives ne livrent pas tous leurs secrets au premier regard ». Ce n'est qu'une illustration d'ambiance : tout le secret est dans le **texte de l'instance**.
- Le texte (et donc le flag) est **propre à chaque instance** : en mode équipe, chaque membre lance son instance, décode son texte et soumet son flag. Le challenge n'est validé qu'une fois tous les membres passés.
- D'une instance à l'autre, le générateur change les objets **et** les tournures de liaison (« Premier bordereau montre » / « Ancien registre cite », « Mécanicien examine » / « Contrôleur vérifie »…), mais garde la même structure : 7 phrases, un objet en fin de chaque segment, et la tournure « *X* rejoint un *Y* » en ouverture du 4e groupe. Une première version du script, fondée sur une liste fixe de mots de liaison, ne marchait que sur l'instance 1.
- Infra : le DNS de la WSL était en panne pendant la résolution (Tailscale). Contournement : résoudre le nom en DoH (`https://1.1.1.1/dns-query?name=ctf.hackagou.nc&type=A`), puis `curl --resolve ctf.hackagou.nc:443:<ip>`.

## Flag

Un flag par instance, donc un par membre de l'équipe :

| Instance | Texte | Flag |
|---|---|---|
| 1 | [instance.html](instance.html) | `OPENNC{64ba2d69-9bf3-41d1-8d90-8a6512745d7f}` |
| 2 | [instance2.txt](instance2.txt) | `OPENNC{e09501af-15ae-42e9-bb22-de163e06ab0d}` |
| 3 | [instance3.txt](instance3.txt) | `OPENNC{3eebecfc-6d99-4158-9e1a-7c8833f0c4e7}` |
