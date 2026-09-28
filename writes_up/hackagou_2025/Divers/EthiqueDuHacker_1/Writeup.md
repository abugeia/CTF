# L'éthique du hacker [1/3]
Catégorie : Divers — Points : 100 — Auteur : \0/

## Énoncé
Jocelyne : Ned, tu avais vu ce vieux message de Tauira ? "Penser à regarder chez AdDo..."
Ned : Ah oui, je me souviens... Ils étaient là quand tout a commencé ! Je pense pouvoir retrouver leur bâtiment.

![Ethique-1](Chall-ethique-1.png)

Jocelyne et Ned arrivent enfin sur place. [...] A peine entrés, ils trouvent des restes d'affiches faisant référence à l'éthique du hacker, ainsi qu'à une sorte de manifeste d'un certain Mentor !?
Un vieil ordinateur tout déglingué traîne sur une table, Jocelyne arrive tout de même à examiner son disque dur et tombe sur le source de ce qui semble être une page du site d'AdDo.

Tu dois suivre la même piste que Jocelyne et Ned, et retrouver d'où vient ce que tu vas trouver.

Format du flag : `OPENNC{Nom_Numéro}`

## Résolution
1. Aspirer le site d'AdDo et chercher dans les commentaires HTML :
   ```bash
   wget -r -l 2 -np -E --accept=html,shtml,css,js,txt,xml 'https://www.addo.nc/'
   grep -Rn '<!--' www.addo.nc/
   ```
2. Deux commentaires en Base64 :
   - `certifications.shtml` → « Voici des éléments pour le challenge "l'éthique du hacker" du HacKagou de 2025. Toujours disponible sur legacy.hackagou.nc ! » (confirmation de piste)
   - `parcours-ri.shtml` → « Avé comme dirait Blaise ! » suivi de `I pdre d gwsfrjeub hogdm. I iring d qopsithu. Kalw o shfcng, wviv lg crrz. Iw gcev zvaw L kaqw wt wr.`
3. « Blaise » → **Vigenère**, clé `addo` (CyberChef : From Base64 → Vigenère Decode) :
   `I made a discovery today. I found a computer. Wait a second, this is cool. It does what I want it to.`
4. Recherche exacte de la phrase → *The Conscience of a Hacker* (*Hacker Manifesto*) de **The Mentor**, publié dans **Phrack** Volume One, **Issue 7**.

Le flag attend la publication et son numéro (pas l'auteur).

Flag : ``OPENNC{Phrack_7}``

*Source : solution officielle publiée sur legacy.hackagou.nc.*
