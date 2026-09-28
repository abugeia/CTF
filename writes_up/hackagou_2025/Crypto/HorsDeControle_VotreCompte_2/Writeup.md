# Hors de Contrôle : Votre Compte [2/5] (2025)
Catégorie : Crypto — Points : 100 — Auteur : Ketsui

## Énoncé
Félicitations agent, vous avez réussi le test d’entrée.

Afin de recevoir vos premières missions, vous devez récupérer vos identifiants temporaires.

Un SMS vous est parvenu, mais il semble chiffré/obfusqué… Saurez-vous le décoder ?

Attention, vos identifiants temporaires constituent le flag.

```
59--000--6d--000--78--000--68--000--59--000--32--000--74--000--6f--000--59--000--58--000--52--000--6f--000--59--000--57--000--4e--000--72--000--5a--000--58--000--4a--000--36--000--4f--000--6e--000--42--000--68--000--63--000--33--000--4e--000--33--000--62--000--33--000--4a--000--6b--000--4d--000--51--000--3d--000--3d
```

Format attendu : `OPENNC{XXXXX:XXXXX}`

## Résolution
Le message est une suite d'octets hexadécimaux séparés par le bruit `--000--`. Les valeurs sont toutes dans la plage ASCII
imprimable (`0x3d` = `=` à la fin fait immédiatement penser à du Base64).

1. Retirer les séparateurs `--000--` → `596d78685932746f...3d3d`
2. Hex → ASCII : `YmxhY2toYXRoYWNrZXJ6OnBhc3N3b3JkMQ==`
3. Base64 → `blackhathackerz:password1`

```sh
echo "$s" | sed 's/--000--//g' | xxd -r -p | base64 -d
# blackhathackerz:password1
```
(script : `solve.sh`)

On obtient un couple `identifiant:mot de passe`, conforme au format `XXXXX:XXXXX`.

Flag : ``OPENNC{blackhathackerz:password1}``
