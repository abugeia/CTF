# Taylor's Version (HacKagou 2026) — Easter Egg

**Flag :** `OPENNC{...}` *(à compléter)*
**Valeur :** 250 pts · **Auteur :** Ketsui · **Statut :** 🟠 flag **caché** ; rien dans les artefacts hors instance (vérifié le 01/10). Reste : instances docker ou sur place.

## Énoncé

> « **Encore une fois**, Ketsui a dissimulé un flag quelque part dans ce CTF. Il peut être **physique**, caché dans un **autre challenge**… ou pas du tout. Il peut même se trouver dans le challenge d'un **autre membre du staff**. Ouvrez l'œil, vous pourriez être récompensés. »

Illustration : `2026-easter-egg-taylor.png`.

## Analyse / approche

Chasse transverse. Pistes :
- **« Taylor's Version »** (réf. Taylor Swift, comme l'easter egg 2025 « Taylor's back » → `OPENNC{willow}`) : le flag est probablement un **titre/mot** lié à Taylor Swift, dissimulé dans un artefact du CTF.
- Chercher dans les **métadonnées** des images de tous les challenges (EXIF, commentaires PNG, `strings`), dans le **code source** des instances web, les en-têtes HTTP, les pages 404, les fichiers `robots.txt`.
- Élément **physique** possible (affiche, flyer, QR dans la salle) → sur site.

## Précédent : édition 2025 (« Taylor's back », même auteur)

Le flag `OPENNC{willow}` était caché dans les **artefacts des autres challenges de Ketsui** (historique
navigateur du dump Android de *Le Phone*). L'énoncé caché de 2024 se trouvait dans le presse-papiers du
dump mémoire de *L'Agence*. → En 2026, il faut viser les **challenges de Ketsui** : Escape (#18),
Dernier Vol du MANTA-06 (#20), Œil du MANTA-06 (#21), La Passe Sans Retour (#27), Origine du Léviathan
(#28), ainsi que ceux des autres membres du staff (\0/, Yoan, GiGaWaTT, K3rhu0n).

## Recherche à distance (sans instance), 01/10/2026

| Artefact | Vérification | Résultat |
|---|---|---|
| HTML des 13 énoncés non résolus + Escape | commentaires `<!-- -->`, `style=` cachés, mots-clés taylor/swift | rien |
| `2026-easter-egg-taylor.png` (#54) | C2PA OpenAI **Valid** (dataHash OK) | pixels intacts → pas de stégano |
| `illustrationmanta.png` (#20) | C2PA **Invalid**, mais seulement `signingCredential.invalid` (EKU manquante) ; `dataHash.match` OK | fausse piste : pixels intacts |
| `illustraionoeil.png` (#21), `2026_La_passe_sans_retour.png` (#27), `hk2026-origine-leviathan.png` (#28) | C2PA OpenAI **Valid** | pixels intacts |
| `2026-Ronde-Automate.jpeg` (#51), `2026-Lobole-LEVIATAN.jpeg` (#53), `2026-Signal-Aieul.jpeg` (#35) | C2PA Google **Valid** | pixels intacts |
| `escape.png` (#18), sans C2PA (sparkle Gemini visible, manifeste retiré) | chunks PNG (IHDR/IDAT/IEND seuls), `zsteg -a`, plans LSB, alpha (=255 partout), données après IEND | rien |
| `2026_Crypto_DansTousLesSens.webp` (#31, \0/), sans C2PA | chunks RIFF (un seul `VP8 `), strings, visuel | rien |

**Conclusion** : aucun artefact consultable hors instance ne contient le flag. Il se trouve soit **dans
une instance** (code source / routes / données des challenges docker de Ketsui ou du staff), soit **sur
place** (élément physique).

## Prochaines étapes

1. À chaque instance démarrée (surtout #20, #21, #27, #28), faire un `grep -i "taylor\|swift\|OPENNC"`
   sur le HTML/JS/réponses API, regarder `robots.txt`, les commentaires HTML et les en-têtes HTTP.
2. Pour #21 (pcap) et #20 (mémoire du drone) : `strings | grep -i taylor` sur les artefacts récupérés.
3. Sur place : affiches, flyers, QR codes.
4. Le flag sera probablement un **titre de chanson** de Taylor Swift (comme `willow` en 2025),
   peut-être une chanson « Taylor's Version ». **Ne pas deviner** : essais illimités (`max_attempts = 0`) mais tracés par les orgas.

## Flag

```
OPENNC{...}
```
