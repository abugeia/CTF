# Data-Diver

Catégorie : Crypto — Points : 100 — Auteur : Ketsui

## Énoncé

Vous êtes un « Data-Diver » engagé par le Syndicat Abyssal. La nuit de la Grande
Faille, le réseau de sonars de l'avant-poste de la Fosse des Kermadec a été
désactivé pendant 45 minutes, laissant passer un submersible fantôme.

En explorant la cabine inondée du superviseur des sonars, vous découvrez son
journal de bord, avec une note chiffrée.

Extrait du journal :

> « Le mot de passe de ma console est le nom et prénom attachés (en minuscules,
> sans espace ni caractère spécial) du commandant du célèbre sous-marin militaire
> français de classe Daphné (le **S647**) qui a disparu corps et biens en
> Méditerranée en **janvier 1968**. »

Note chiffrée :

```
OCHERH{lu_nhnrumi_1968_jt_fv_wuvwv_ixt_cxm}
```

« Trouvez la clé via OSINT, déchiffrez le message et retrouvez le flag. »

Format du flag : `OPENNC{...}`

## Résolution

### 1. OSINT — la clé

Le sous-marin français de classe **Daphné** immatriculé **S647**, disparu en
Méditerranée en **janvier 1968**, est **La Minerve** (perdue corps et biens le
27 janvier 1968 au large de Toulon).

Son commandant était le **Lieutenant de vaisseau André Fauve**.

« Nom et prénom, en minuscules, sans espace ni caractère spécial » →
clé = `andrefauve`.

### 2. Nature du chiffrement

Le format `OCHERH{...}` doit donner `OPENNC{...}`. On teste un **Vigenère**
(chiffrement additif) appliqué aux seules lettres :

`P = C - K mod 26`

Vérification sur l'en-tête : `OCHERH` avec la clé `andrefauve` (a,n,d,r,e,f…)
donne bien `OPENNC`. La clé est confirmée.

### 3. Déchiffrement

```python
ct = "OCHERH{lu_nhnrumi_1968_jt_fv_wuvwv_ixt_cxm}"
key = "andrefauve"
def dec(ct, key):
    out = []; ki = 0
    for ch in ct:
        if ch.isalpha():
            k = ord(key[ki % len(key)]) - 97
            base = 65 if ch.isupper() else 97
            out.append(chr((ord(ch) - base - k) % 26 + base)); ki += 1
        else:
            out.append(ch)
    return "".join(out)
print(dec(ct, key))
```

Résultat déterministe :

```
OPENNC{la_sdnerve_1968_et_la_suite_est_ici}
```

### 4. Interprétation et anomalie

Le texte clair se lit « la ****nerve 1968 et la suite est ici ». Le contexte
(sous-marin de 1968) impose **La Minerve**. Le flag *voulu* est donc très
probablement :

```
OPENNC{la_minerve_1968_et_la_suite_est_ici}
```

Anomalie constatée : en re-chiffrant `la_minerve…` avec la clé `andrefauve` on
obtient `lu_hmnrumi…`, alors que la note publiée contient `lu_nhnrumi…`. Le
chiffré publié correspond exactement au clair `la_sdnerve…` (2 lettres « mi » →
« sd » interverties). C'est très vraisemblablement une petite erreur de
génération de l'auteur : le mot recherché reste **minerve**.

## Flags candidats

- **Candidat principal (intention, sémantiquement correct)** : `OPENNC{la_minerve_1968_et_la_suite_est_ici}`
- **Variante (déchiffrement littéral du chiffré publié)** : `OPENNC{la_sdnerve_1968_et_la_suite_est_ici}`

Confiance : probable. Essayer d'abord `la_minerve`, sinon `la_sdnerve`.

Flag : ``OPENNC{la_minerve_1968_et_la_suite_est_ici}`` (candidat, non validé)
