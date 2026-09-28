# 🎶 Easter Egg – Taylor's back
Catégorie : Divers — Points : 250 (dynamique) — Auteur : Ketsui

## Énoncé
![taylor.jpg](taylor.jpg)

Vous vous souvenez de l'an dernier ? Je vous avais concocté un challenge où il fallait retrouver où Taylor avait séjourné à Sydney avec Travis.

Eh bien, un an plus tard… les voilà fiancés ! 💍 Il était donc impensable qu'un petit easter egg ne se glisse pas dans cette édition 2025.

Cette fois, pas d'extravagances : c'est beaucoup plus simple. À vous de deviner le titre de chanson de Taylor Swift que je préfère. Ni plus, ni moins.

L'indice ? L'info se cache quelque part dans cette édition 2025… à vous de la dénicher.

Format du Flag : `OPENNC{Titre}` — **Attention qu'un seul try !**

## Résolution
L'auteur (Ketsui) est aussi celui de la série **Hors de Contrôle** : c'est là qu'il faut chercher.

- [3/5] *Borne, Elizabeth !* ([writeup](../../OSINT/HorsDeControle_BorneElizabeth_3/Writeup.md)) : fausse piste / teaser — le transcript parle d'une pub Taylor Swift pour l'album *reputation* (nov. 2017), mais ce n'est pas un titre de chanson.
- [4/5] *Le Phone* ([writeup](../../Enquete/HorsDeControle_LePhone_4/Writeup.md)) : dans le dump Android, l'historique du navigateur Jelly
  `Dump/data-1/org.lineageos.jelly/databases/HistoryDatabase`, table `history` :
  - id 8, 28/08/2025 04:55:00 UTC — « willow taylor swift - YouTube » (`m.youtube.com/results?search_query=willow+taylor+swift`)
  - id 9, 28/08/2025 04:55:07 UTC — « Taylor Swift - willow (Official Music Video) - YouTube » (`m.youtube.com/watch?v=RsEZmictANA`)

  C'est la seule chanson de Taylor Swift présente dans le dump (confirmée par le cache de suggestions `org.lineageos.jelly/cache/suggestion_responses/`).

```bash
sqlite3 Dump/data-1/org.lineageos.jelly/databases/HistoryDatabase "select * from history;"
```

Graphie officielle en minuscules (album *evermore*).

Flag : ``OPENNC{willow}``
