# La chaufferie piégée (HacKagou 2026) — Crypto

**Flag :** `OPENNC{...}` *(non trouvé — vecteur d'extraction non identifié)*
**Valeur :** 250 pts · **Auteur :** K3rhu0n · **Solves :** 2
**Statut :** 🔴 **non résolu** — tous les vecteurs stégo classiques éliminés, l'indice « 5409th position » reste énigmatique.

## Énoncé

> Suite de **La piste atlante** (#42, même auteur) : « Les Atlantes avaient raison, il y a
> un composant critique vulnérable. » Un **mot-code de blocage** du protocole *Marée Noire*
> est caché dans une image du journal de bord.
> Indice (section *logbook*) : **« Watch starting from the 5409th position. »**
> Mission : trouver le mot-code. Format `OPENNC{...}`.

Fichier : `lachaufferiepiegee.png` — 1448×1086, RGB (colortype 2, 8 bits), image IA
(chaufferie steampunk) avec plusieurs cadrans/« montres » visibles (jeu de mot sur *watch*).

## Analyse menée (exhaustive)

Image **générée par ChatGPT** : elle embarque un chunk PNG `caBX` = **manifeste C2PA
authentique** (JUMBF/CBOR), signé par la chaîne `SSL.com C2PA` → `OpenAI Media Service`
(`claim_generator = "OpenAI Media Service API"`, `digitalSourceType = trainedAlgorithmicMedia`,
assertion `c2pa.watermarked.unbound`). Les assertions sont **strictement standard**
(`c2pa.icon`, `c2pa.actions.v2`, `c2pa.hash.data`) — **aucune assertion custom**, aucune
donnée injectée. La provenance est réelle, ce n'est **pas** le porteur du secret.

| Piste | Méthode | Résultat |
|---|---|---|
| Octets après `IEND` / polyglotte | scan signatures ZIP/JPEG/PDF/7z/gzip | **0 octet en trop**, aucun fichier embarqué |
| Taille zlib décompressée | `H*(1+W*3)` vs réel | **exacte** (4 718 670 o) → rien de caché dans l'IDAT |
| Métadonnées / chunks | tEXt/zTXt/iTXt, exif | aucune (seul `caBX` C2PA) |
| C2PA CBOR | parse complet des assertions | standard, signé, pas de payload |
| LSB 1 bit | R/G/B/RGB/BGR, row & col, MSB & LSB-first | pas de `OPENNC`/texte |
| LSB 2 bits | idem | que du bruit base64-like |
| Départs testés | bit 5409, octet 5409, pixel 5409 (×3), 5408, 5409·8 | aucun ASCII lisible |
| `stegano.lsb reveal` | `shift` ∈ {0, 5408, 5409, 5410} | *Impossible to detect message* |
| Décimales de constantes | π, e, √2, φ, ln2 à la position 5409 | aucun motif (a1z26, ASCII) |
| Octets pixels bruts @5409 | lecture directe | zone nulle, non imprimable |
| Inspection visuelle HD | horloges, CRT (sous-marin + radar), manomètres | décoratif, aucun code lisible |

→ L'image est **cryptographiquement/stéganographiquement propre** au sens LSB. L'indice
**5409** désigne un point de départ dans un **vecteur non identifié**.

## Pistes restantes (non confirmées)

- **Référence externe indexée en 5409** (comme *Echo du Legacy* dépend de `legacy`) :
  le « 5409ᵉ » pourrait indexer un **texte** (journal de bord = *Vingt mille lieues sous
  les mers* ?) ou un artefact fourni ailleurs dans le parcours.
- **Composante on-site** : plusieurs challenges 2026 avaient du matériel diffusé en salle.
- `U+5409` = 吉 (CJK « chance/propice ») — sens incertain.
- Outil stégo à **passphrase** non-PNG (steghide refuse le PNG) : piste peu probable.

> Reproductibilité de l'analyse : scripts dans la session (téléchargement via API CTFd,
> `PIL`/`numpy` pour le LSB, `cbor2` pour le C2PA). Flag non obtenu.

## Flag

```
OPENNC{...}
```
