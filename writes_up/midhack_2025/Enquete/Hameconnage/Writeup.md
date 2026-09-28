# Hameçonnage

Catégorie : Enquête — Points : 50 — Événement : MidHack 2025 (qualif)

## Énoncé

Ned : Tauira m'a envoyé un email bizarre à analyser, je crois que l'IA cherche à nous voler nos identifiants de connexion.

Jocelyne : C'est vraiment inquiétant cette histoire... Et alors ça donne quoi cette analyse ?

Ned : En vrai, je n'ai pas eu le temps. J'ai lancé l'exécution dans une sandbox et j'ai extrait le rapport [`misp`](https://www.misp-project.org/) en format `json`.

Jocelyne : OK, tu veux que je regarde ?

Ned : Oui s'il te plaît, si cet email est du [hameçonnage](https://attack.mitre.org/techniques/T1566/002/), il devrait y avoir un nom de domaine bizarre. Cela ne m'étonnerait pas que l'on retrouve la même origine que certains groupes APT du type **Bear**.

![Bear](midhack_chall05_bear.jpg)

Jocelyne : Okay je cherche le nom de domaine complet !

Format du flag : `OPENNC{xxxxx.xxxxxxxxx.xx}`

Fichier fourni : `challenge05_search_domain_phishing_misp.json` (rapport MISP généré depuis ANY.RUN).

## Résolution

Le rapport MISP contient 628 attributs. Deux indices orientent la recherche :
- le format du flag `xxxxx.xxxxxxxxx.xx` → un sous-domaine de 5 lettres, un domaine de 9 lettres, un TLD de 2 lettres ;
- l'allusion aux **APT « Bear »** (Fancy Bear / Cozy Bear, groupes russes) → TLD `.ru`.

On filtre donc les attributs de type domaine sur `.ru` :

```bash
python3 - <<'PY'
import json,re
d=json.load(open("challenge05_search_domain_phishing_misp.json"))
for a in d["Event"]["Attribute"]:
    v=a.get("value","")
    if re.search(r'\.ru\b', v):
        print(a["category"],"|",a["type"],"|",v)
PY
```

Résultat :

```
Network activity | domain|ip | nofuv.cestaispa.ru|188.114.96.3
Network activity | domain|ip | nofuv.cestaispa.ru|188.114.97.3
```

Un seul domaine `.ru` apparaît : **`nofuv.cestaispa.ru`**, résolu vers des IP Cloudflare (188.114.96.3 / 188.114.97.3).

Vérification du format : `nofuv` = 5 caractères, `cestaispa` = 9, `ru` = 2 → correspond exactement à `xxxxx.xxxxxxxxx.xx`.

Flag : `OPENNC{nofuv.cestaispa.ru}`
