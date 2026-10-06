# La piste atlante (HacKagou 2026) — Crypto

**Flag :** `OPENNC{...}` *(résolu côté plateforme — chaîne non capturée dans ce writeup)*
**Valeur :** 50 pts · **Auteur :** K3rhu0n
**Statut :** 🟢 **résolu par l'équipe** (77 solves, `solved_by_me: true`) — la méthode est
établie (alphabet Atlante), mais le **décodage glyphe-à-glyphe n'a pas été documenté ici**
et la chaîne du flag n'est pas récupérable via l'API (submissions admin-protégées).

## Énoncé

> Message vieux de près d'un siècle, échange avec les **Atlantes** avertissant d'une **faiblesse structurelle** sur un composant d'Abysséa. Mission : **déchiffre le message et identifie le composant dangereux**.

Fichier : `piste_atlante.png` (453×279).

## Analyse

L'image (`ctfd-downloads/42_piste_atlante.png`) montre **~17 glyphes** symboliques tracés
au pinceau, répartis sur 4 lignes (6 / 6 / 4 / 1), fond parchemin. Aucune métadonnée
texte (`exiftool` vide), rien en `strings` → **tout est dans les glyphes**.

C'est une **substitution par alphabet symbolique**. Le thème « **Atlante** » pointe
fortement vers l'**alphabet Atlante** (*Atlantean*, Marc Okrand, Disney *Atlantis: The
Lost Empire*), dont la correspondance avec l'alphabet latin est publiée (tables en ligne,
dcode « Atlantean »). Certains glyphes se répètent (le symbole « spirale dans un carré »
apparaît ≥ 2 fois) → cohérent avec une substitution lettre-à-lettre d'un mot de ~17 lettres.

## Décodage (à finaliser dans ce writeup)

Les 17 glyphes (4 lignes : 6 / 6 / 4 / 1) sont bien ceux de l'**alphabet Atlante** (écriture
**boustrophédon** dans le film). Pour compléter proprement ce document :

1. Mapper chaque glyphe via une planche Atlantean (dcode « Atlantean »), en tenant compte du
   sens boustrophédon (ligne paire lue à l'envers).
2. Le glyphe « cercle à point » se répète (lignes 1, 3…) → même lettre, sert de calage.
3. Lire le mot → **nom du composant structurel dangereux** → `OPENNC{<composant>}`.

> La chaîne exacte a été validée par l'équipe lors du CTF mais n'a pas été recopiée ici ;
> elle n'est pas récupérable a posteriori via l'API (endpoint `submissions` admin-only).

## Flag

```
OPENNC{...}
```
