# SingeBlasé
Catégorie : Web3 — Points : 100 — Contribution : Police Nationale

## Énoncé

> Connor Sturdy, un corsaire bien connu pour son obsession du Capt'N Nepo, aurait réussi à trouver
> sur le marché noir une **peinture faite par Jules, le fils du Capt'N**. Ne la trouvant pas à son
> goût, Connor décide de la **revendre 17 jours plus tard**.
>
> Saurez-vous retrouver le **gain total** de cette opération pour Connor à partir de la photo prise
> du tableau ?
>
> ![quel_gain.png](quel_gain.png)
>
> Format du flag : `OPENNC{md5_du_gain}`
> *Exemple si le gain est de 1.35 BTC avec md5sum("1.35BTC") : OPENNC{dd720cffa415667815031441bf80b226}*
>
> Challenge créé avec la contribution de la Police Nationale [...]

## Analyse de l'image

`quel_gain.png` est un **Bored Ape** (style BAYC), 400×400. Traits visibles :

- **Fond** : turquoise, RGB `(23,230,183)` = trait BAYC **Aquamarine** ;
- **Fourrure** : tachetée = trait BAYC **Cheetah** ;
- **Yeux** : lunettes de soleil sombres = trait **Sunglasses** ;
- **Chapeau** : casquette **noire à visière avec une chaîne** ;
- **Bouche** : *Bored* (fermée) ; **aucun vêtement** visible.

### Identification de l'œuvre d'origine

On croise les traits sur la base de métadonnées complète de la collection
(`github.com/skogard/apebase`, fichier `db`, 10 000 singes) :

```python
# Fur == Cheetah et Hat == "Sea Captain's Hat"  → 9 singes
# Fur == Cheetah et Eyes == "Sunglasses"        → 22 singes
# intersection Cheetah + Sea Captain's Hat + Sunglasses → 1 seul : #742
```

Le **BAYC #742** est le **seul** singe *Cheetah + Sea Captain's Hat + Sunglasses*. En comparant
l'image réelle du #742 (récupérée via IPFS) avec l'image du challenge (voir
`comparaison_bayc742.png`), le **visage, la fourrure, les lunettes et la forme de la casquette sont
identiques**. Les métadonnées officielles du #742 sont :
`Background=Purple, Clothes=Tanktop, Eyes=Sunglasses, Fur=Cheetah, Hat=Sea Captain's Hat, Mouth=Bored Kazoo`.

L'image du challenge est donc une **version retouchée** du #742 (« une peinture faite par Jules, le
fils du Capt'N » = une **copie/contrefaçon**) :
casquette blanche → **noire**, fond violet → **aquamarine**, **kazoo** et **débardeur retirés**.
Le thème « marché noir / peinture par le fils du Capt'N (= *Sea Captain's Hat*) / Police Nationale »
confirme qu'il s'agit d'une **contrefaçon** de l'ape original.

## Méthode de résolution (reproductible)

1. Reverse image search de `quel_gain.png` (Google Lens / Yandex) → tomber sur la fiche
   marketplace de l'ape (OpenSea / Blur).
2. Ouvrir l'onglet **Activity / Item Activity** de l'ape.
3. Repérer les **deux transactions distantes de 17 jours** : un achat (`Sale` entrant, prix P₁)
   puis une revente (`Sale` sortant, prix P₂) 17 jours plus tard.
4. Calculer le **gain** = P₂ − P₁ (en ETH).
5. Construire le flag :
   ```bash
   t=$(echo -n "<gain>ETH" | md5sum | awk '{print $1}'); echo "OPENNC{$t}"
   ```
   (format `<nombre>ETH` sans espace, comme l'exemple `1.35BTC` de l'énoncé).

## Statut : NON RÉSOLU (blocage environnement)

Le **gain exact n'a pas pu être déterminé** dans cet environnement :

- **Reverse image search indisponible** : Google Lens renvoie `HTTP 429 / captcha`, Bing Visual
  Search « Unable to process this search », Yandex et TinEye inaccessibles (timeout / Cloudflare 403)
  depuis l'IP utilisée. Impossible donc de retrouver la **fiche marketplace exacte** de la
  contrefaçon.
- **APIs marketplace / blockchain** nécessitent une clé (Reservoir, Ankr, OpenSea, RPC archive),
  donc l'historique des ventes n'a pas pu être récupéré programmatiquement.
- L'activité du **BAYC #742 authentique** (OpenSea) ne montre qu'un *Mint* + **une seule** vente
  (~333 $, 2021) : **pas de flip à 17 jours**. → La transaction recherchée porte donc sur le **jeton
  de la collection contrefaisante** (dérivé du #742), qu'il faut identifier par reverse image search
  pour lire ses deux ventes espacées de 17 jours.

**À refaire depuis un poste avec un navigateur non bloqué** : reverse-image `quel_gain.png`,
ouvrir la collection dérivée, lire achat/revente à 17 jours d'écart, puis
`md5("<gain>ETH")`.

## Fichiers

- `quel_gain.png` : image du challenge (la « peinture »)
- `comparaison_bayc742.png` : à gauche l'image du challenge, à droite le BAYC #742 authentique
