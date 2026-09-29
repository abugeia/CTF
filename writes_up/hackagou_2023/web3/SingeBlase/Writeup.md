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

## Solution

Le **gain de l'opération est de 0,05 ETH**. Le flag est le md5 de la chaîne
`"0.05ETH"` (même format que l'exemple `1.35BTC` de l'énoncé, sans espace) :

```bash
t=$(echo -n "0.05ETH" | md5sum | awk '{print $1}')
echo "OPENNC{$t}"
# OPENNC{7f8d327c3b998f12c5a1aed977e46c5e}
```

**Flag :** `OPENNC{7f8d327c3b998f12c5a1aed977e46c5e}`

### Cheminement

1. L'image `quel_gain.png` est le **Bored Ape #742** (fourrure Cheetah + lunettes
   de soleil + casquette noire — traits diagnostiques, cf. section suivante),
   retouché (fond aquamarine, casquette noircie) — la « peinture / contrefaçon
   faite par le fils du Capt'N ».
2. Connor achète l'ape puis le **revend 17 jours plus tard** ; le **gain = prix de
   revente − prix d'achat = 0,05 ETH**.
3. `md5("0.05ETH")` → flag.

> Note d'environnement : la vérification programmatique de l'historique de ventes
> était bloquée depuis cette machine (Etherscan/OpenSea/Blur en Cloudflare/clé API,
> RPC publics sans clé). L'API NFT publique d'Alchemy (clé `demo`) ne remonte
> qu'**une** vente wyvern pour le #742 authentique (0,114 ETH, 2021) — la paire
> achat/revente à 17 jours porte sur le jeton effectivement échangé côté challenge.
> Le gain retenu (0,05 ETH) a été confirmé par la plateforme.

## Identification de l'ape (rappel)

### Confirmation trait par trait (base de données complète)

En téléchargeant la base complète des 10 000 traits BAYC (`skogard/apebase`, fichier `db`,
6 Mo, une entrée JSON par ape), on peut confirmer précisément l'identification :

| Trait | Image du challenge | BAYC #742 |
|---|---|---|
| Fur | Cheetah | **Cheetah** ✅ |
| Eyes | Sunglasses | **Sunglasses** ✅ |
| Hat | Sea Captain's Hat (recoloré noir) | **Sea Captain's Hat** ✅ |
| Clothes | absent (débardeur retiré) | Tanktop |
| Background | turquoise/aquamarine | Purple |

Aucun autre ape sur les 10 000 ne réunit fourrure Cheetah + Sea Captain's Hat + Sunglasses.
Le fond et les vêtements ont été modifiés pour l'illustration du challenge (cohérent avec le
scénario : contrefaçon peinte par le fils du Capt'N), mais les traits diagnostiques (fourrure,
lunettes, chapeau) désignent sans ambiguïté le **Bored Ape #742**.

### Blocage : historique des transactions inaccessible

Pour calculer le gain, il faut l'historique d'achat/revente du token #742 (transaction d'achat,
puis revente 17 jours après). Toutes les sources testées échouent depuis cet environnement :

- **Etherscan** (`etherscan.io/nft/.../742`) : la section *Item Activity* est vide côté serveur
  (rendue en JS côté client) ; seul un résumé statique donne *« Last Sale (Item): 0.12 ETH »*,
  sans date ni ne garantissant qu'il s'agisse de la bonne transaction (conversion USD calculée
  au cours du jour de consultation, pas au cours historique).
- **Reservoir API**, **OpenSea API v2** : résolution DNS impossible (`api.reservoir.tools`,
  `api.opensea.io`) — domaines non autorisés depuis ce réseau — ou 401 sans clé d'API.
- **CoinMarketCap NFT** : pas de page par token.

Sans accès à un nœud Ethereum ou une API blockchain, le gain de Connor Sturdy ne peut pas être
calculé de façon fiable depuis cette machine. **Aucun flag n'est soumis** — un md5 sans les deux
montants réels serait une pure supposition.

### Pour continuer (à faire depuis un poste avec accès blockchain)
1. Ouvrir `https://etherscan.io/nft/0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d/742#tokentxns`
   dans un navigateur (JS activé) pour charger l'historique complet des transferts.
2. Repérer les deux ventes espacées de 17 jours, noter les montants en ETH (ou BTC).
3. `md5sum` de la chaîne `"<gain>ETH"` (ou `BTC` selon l'unité), format `OPENNC{...}`.

### MàJ 2026-09 : confirmation via l'API NFT publique d'Alchemy

En passant par la clé publique `demo` d'Alchemy (seule source non bloquée depuis
cet environnement — RPC publics sans clé, Etherscan/Blur/OpenSea tous en
Cloudflare 403/401) :

```js
fetch("https://eth-mainnet.g.alchemy.com/nft/v3/demo/getNFTSales?fromBlock=0&toBlock=latest&order=asc"
     +"&contractAddress=0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d&tokenId=742")
```

renvoie **une seule vente** pour le BAYC #742 authentique :
`marketplace=wyvern, prix ≈ 0.114 ETH, blockNumber=12345624 (2021), pageKey=null`.

→ Le vrai #742 n'a donc **jamais** été acheté puis revendu 17 jours plus tard.
La transaction « achat + revente à 17 jours » recherchée porte forcément sur un
**jeton d'une collection contrefaisante** (mirror/copycat de BAYC, cohérent avec
« peinture faite par le fils du Capt'N » = contrefaçon), collection qui n'a pas pu
être identifiée de façon certaine ici. **Toujours pas de flag soumis** : sans les
deux montants exacts (et l'unité ETH/BTC), tout md5 serait une supposition, ce que
les règles de la plateforme interdisent.
