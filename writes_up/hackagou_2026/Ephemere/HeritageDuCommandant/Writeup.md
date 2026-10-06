# L'héritage du commandant (HacKagou 2026) — Ephémère

**Réponse :** `Capitaine Nepo` *(QCM — pas de format `OPENNC{}` ici)*
**Valeur :** 10 pts · **Auteur :** \0/
**Statut :** ✅ résolu

## Énoncé

> Dossier sur **Élias Varn**, ancien commandant du **Nautile**. Un vieux portrait (marin
> d'un autre âge : tricorne usé, longue barbe grise, regard sévère) accompagne une
> annotation :
> « Le sang des grands capitaines ne garantit pas leur sagesse… mais certaines familles
> semblent incapables de rester à la surface. »
> Élias Varn serait le **descendant d'un capitaine devenu célèbre**. Duquel ?
> QCM : Capitaine Achab · Capitaine Hatteras · Capitaine Nemo · Capitaine **Nepo**.

Type CTFd `multiple_choice` (plugin `multiple_choice`). La soumission envoie le **texte**
de l'option sélectionnée (cf. `view.js` du plugin : `input.value = answer`), pas un index.

## Analyse

Le piège est évident : **Nautile = Nautilus**, et « incapables de rester à la surface »
= sous-marin → on pense immédiatement au **Capitaine Nemo** (Jules Verne,
*Vingt mille lieues sous les mers*). C'est la fausse piste.

→ Soumission `Capitaine Nemo` : **Incorrect**.

La relecture de l'annotation montre que **tout tourne autour de la lignée** :
« le **sang** des grands capitaines », « certaines **familles** », « **descendant** ».
C'est un jeu de mot sur le **népotisme** (*nepo baby*) : « le sang ne garantit pas la
sagesse » = privilège héréditaire sans mérite. L'option **Nepo** n'est pas un vrai
capitaine célèbre, c'est la **chute humoristique** — signature de l'auteur \0/.

Les deux autres options (Achab de *Moby Dick*, Hatteras de Jules Verne) sont des leurres
de capitaines réels mais hors-sujet.

## Exploitation

```bash
curl -s https://ctf.hackagou.nc/api/v1/challenges/attempt \
  -H "Authorization: Token $CTFD_TOKEN" \
  -H "Accept: application/json" -H "Content-Type: application/json" \
  -X POST --data '{"challenge_id": 22, "submission": "Capitaine Nepo"}'
# => {"success": true, "data": {"status": "correct", "message": "Correct"}}
```

> Note : l'API `ctf.hackagou.nc` exige **à la fois** `Accept: application/json` **et**
> `Content-Type: application/json`, même sur les GET, sinon redirection 302 vers `/login`.

## Réponse

```
Capitaine Nepo
```
