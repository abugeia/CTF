# Invasion au CCP
Catégorie : Crypto — Points : 10 — Auteur : Kerhuon

## Énoncé

> Jeune structure associative financée par des fonds publics, le Centre Cyber du Pacifique a
> vocation à améliorer le niveau de cybersécurité calédonien [...]
> (https://centrecyberpacifique.nc/qui-sommes-nous/).
>
> De nombreux Bakeneko maléfiques échappés du Pays du Soleil levant ont décidé de s'en prendre
> au CCP [...]
>
> ![](chat_malefique.png)
>
> Afin de protéger le coffre-fort numérique contenant les secrets du HacKagou, le CCP utilise un
> mot de passe camouflé sous forme d'**empreinte numérique du logo de son site Web**, de sorte que
> même les **256 chats** n'ont pu le retrouver.
>
> Format du flag : `OPENNC{empreinte_numérique}`

## Résolution

### 1. Lire les indices

- « empreinte numérique du logo » → il faut calculer un **hash** (empreinte) du fichier logo.
- « même les **256 chats** n'ont pu le retrouver » → le nombre **256** désigne l'algorithme :
  **SHA-256**.

### 2. Récupérer le logo du site

Le logo principal affiché dans l'en-tête du site `centrecyberpacifique.nc` est servi à cette
URL (visible via l'inspecteur / le code source de la page) :

```
https://centrecyberpacifique.nc/wp-content/themes/helium/assets/images/logo-light_ccp.svg
```

```bash
curl -sL -A "Mozilla/5.0" \
  "https://centrecyberpacifique.nc/wp-content/themes/helium/assets/images/logo-light_ccp.svg" \
  -o logo-light_ccp.svg          # 20861 octets
```

> Vérification : le fichier servi aujourd'hui est **identique** à la version archivée par la
> Wayback Machine le 14/08/2024 (`web.archive.org/web/20240814120906id_/…logo-light_ccp.svg`),
> donc le hash correspond bien à celui de l'édition 2024 du CTF.

### 3. Calculer l'empreinte SHA-256

```bash
$ sha256sum logo-light_ccp.svg
7f2439c3669d6015f7dc71cb73ffaa71afdcf4eb04e7efe81f9d0e615b23356d  logo-light_ccp.svg
```

Flag : ``OPENNC{7f2439c3669d6015f7dc71cb73ffaa71afdcf4eb04e7efe81f9d0e615b23356d}``

Confiance : **probable**. L'algorithme (SHA-256) est certain grâce à l'indice « 256 » ; la seule
incertitude est *quel* fichier logo. Le candidat retenu est le logo d'en-tête `logo-light_ccp.svg`.

### Variantes à tester en cas de refus

Autres empreintes calculées sur les fichiers logo du site (mêmes octets qu'en 2024) :

| Fichier | SHA-256 |
|---|---|
| `logo-light_ccp.svg` (en-tête, **retenu**) | `7f2439c3669d6015f7dc71cb73ffaa71afdcf4eb04e7efe81f9d0e615b23356d` |
| `logo_footer_ccp.svg` (pied de page) | `ea1541089c1ae5129ec2448daa8e367628d2922817c9d81129b8fb3e47701aa3` |
| `favicon_ccp.png` (2024/05) | `9a07d345b4c7d0c4e2b68965f2909493abe3948ebc7c21d71cb04ae89bf77a92` |

MD5 / SHA-1 du logo d'en-tête (si le format « 256 » n'était pas SHA-256) :
- MD5 : `a4c54008c177ab24c2d687cf3415f99a`
- SHA-1 : `58df3fb2e2097574376126824b68ee63c9baaced`

## Fichiers

- `logo-light_ccp.svg`, `logo_footer_ccp.svg` : logos téléchargés depuis le site du CCP
- `chat_malefique.png` : image d'illustration de l'énoncé
