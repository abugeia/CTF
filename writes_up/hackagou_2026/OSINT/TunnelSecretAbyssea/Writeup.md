# Le tunnel secret vers Abysséa (HacKagou 2026) — OSINT

**Flag :** `OPENNC{Apogoti}`
**Valeur :** 249 pts · **Auteur :** K3rhu0n
**Statut :** ✅ résolu

## Énoncé

> Un **tunnel secret** avec navette mécanique relie la côte calédonienne à Abysséa. LÉVIATHAN en a dissimulé l'emplacement via d'anciennes **fortunes de mer calédoniennes**. Le secret s'appuie sur des **dates de naufrages** et les **noms de passe ou récif** associés : **1885, 1904, 1943**. « LÉVIATHAN a pu ignorer accents et majuscules. »
> Lien laissé par LÉVIATHAN : `https://drive.proton.me/urls/X8Z6EV46K8#tAtSzKnQPxFE`
> Au terme des recherches, des **coordonnées géographiques** mènent à une **anse**. Mission : **trouver le nom de cette anse** (entrée du tunnel).

## Reconnaissance

« Fortunes de mer calédoniennes » est le nom de l'association (FMC, hébergée par le [Musée maritime de Nouvelle-Calédonie](https://museemaritime.nc/fortunesdemer/epaves)) qui recense les naufrages de l'archipel depuis 1831. Elle publie un **tableau chronologique** de tous les naufrages connus : [TableauChrono2019.pdf](https://museemaritime.nc/fortunesdemer/images/articles/TableauChrono2019.pdf).

Extraction du texte (`uv run --with pypdf`) puis filtrage sur les trois années. Plusieurs naufrages par an, dont ceux associés à une passe ou un récif :

| Année | Navire | Lieu (tableau / fiche épave FMC) |
|---|---|---|
| 1885 | *Cher* (transport de la Marine nationale) | Poya, îlot / **récif Contrariété** |
| 1904 | *Ville de Saint-Nazaire* (3-mâts barque, nickel) | Thio, récif Koué — **passe de Kouakoué** sur la fiche épave |
| 1904 | *West Australian* | Surprise (récif des Français) |
| 1904 | *Sarcelle* | Canal de la Havannah |
| 1943 | *YP-422* (ex-*Mist*, patrouilleur US) | **Récif Toombo** (fiche épave) |
| 1943 | *Lipscomb Lykes* | Récif Durand |
| 1943 | *YDG-4* | Passe de Boulari |

Les fiches « Épaves » du site FMC ne retiennent qu'une épave par année : *Le Cher* (Contrariété), *Ville de Saint-Nazaire* (Kouakoué), *YP-422* (Toombo). Ce sont les bonnes.

## Exploitation

Le lien Proton Drive est une page JavaScript : il faut l'ouvrir dans un navigateur (Playwright), WebFetch ne suffit pas. Il demande un mot de passe. Concaténer les trois noms ne fonctionne pas : chaque nom ouvre **un maillon d'une chaîne de trois liens**, en minuscules et sans accent.

| Lien | Mot de passe | Fichier | Contenu |
|---|---|---|---|
| `urls/X8Z6EV46K8#tAtSzKnQPxFE` | `contrariete` (1885) | `Contrariete.txt` | `https://drive.proton.me/urls/AR2YG8S33R#fkV0vDO8p0LQ` |
| `urls/AR2YG8S33R#fkV0vDO8p0LQ` | `kouakoue` (1904) | `Kouakoue.txt` | `https://drive.proton.me/urls/MABJZACJ7M#2FibDQf75cvT` |
| `urls/MABJZACJ7M#2FibDQf75cvT` | `toombo` (1943) | `Toombo.txt` | `-22.19853, 166.4353` |

Géocodage inverse des coordonnées ([Nominatim](https://nominatim.openstreetmap.org/reverse?lat=-22.19853&lon=166.4353&format=json)) : **Pointe à la Dorade, Dumbéa**. Une recherche « anse » autour du point renvoie, à **20 m**, la cale « *Mise à l'eau de l'Anse Apogoti* » (OSM `leisure=slipway`, rue de Provence).

L'anse est donc l'**Anse Apogoti** → flag `OPENNC{Apogoti}`, accepté au premier essai.

## Notes

- Piège : on pense d'abord à un mot de passe unique formé des trois noms. En réalité, il y a un mot de passe par lien, appliqués dans l'ordre chronologique.
- Pour 1904, le tableau indique « récif Koué » ; c'est la fiche épave FMC (« passe de Kouakoué ») qui donne le nom attendu.
- Infra : le DNS de la WSL était en panne (Tailscale). Contournement : résolution DoH (`https://1.1.1.1/dns-query?name=<hôte>&type=A`) puis `curl --resolve`. Le Chromium de Playwright, lui, résolvait normalement.

## Flag

```
OPENNC{Apogoti}
```
