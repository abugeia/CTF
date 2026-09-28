# Hors de Contrôle : Le Phone [4/5] (2025)
Catégorie : Enquête — Points : 250 (dynamique, min 150) — Auteur : Ketsui

## Énoncé
Grâce à votre précédente découverte, une opération d'interception a été menée avec succès.
Le suspect a été arrêté, mais le rapport du MEH indique qu'il avait repéré nos agents et a tenté de fuir.

La question reste entière : a-t-il pu prévenir un complice ?

Il faut qu'on récupère ORACLE et vite !

Nos analystes ont immédiatement saisi son téléphone.
Pour garantir l'intégrité juridique de la preuve, une image disque complète a été créée et un dump pré-traité vous a été envoyé.

Objectifs
* Rechercher toute preuve du vol de la puce Oracle.
* Identifier s'il existait un complice ou une tentative de communication avant son arrestation.

Format du flag : `OPENNC{flag}`

Fichier : https://drive.proton.me/urls/Q7X3XXY7GG#oBPxO7N5tIMl (`Dump.7z`, 462 Mo — non copié ici)

## Résolution

### 1. Récupération du dump
Le lien Proton Drive déchiffre côté client : téléchargement via un navigateur (Playwright), puis extraction :

```bash
uv run --with py7zr python -c "import py7zr; py7zr.SevenZipFile('Dump.7z').extractall('.')"
```

On obtient une arborescence Android (x86, LineageOS/CyanogenMod) : `Dump/data-1` (= `/data/data`),
`Dump/user_de/0`, `Dump/media/0` (stockage interne). Chaque fichier a un jumeau `*-slack` (slack space de l'export forensique).

### 2. Tri des bases SQLite
`dumpdb.py` parcourt toutes les bases SQLite du dump et en exporte le contenu. Points clés :

- `user_de/0/com.android.providers.telephony/databases/mmssms.db` : table `sms` vide, mais un thread vers `+3385746754`.
- `data-1/com.android.providers.contacts/databases/contacts2.db` : un seul contact, **Eric** `(984) 765-3344`.
- `data-1/com.android.messaging/databases/bugle_db` (app Messages AOSP) : la conversation avec `+33 85746754`
  contient les brouillons/messages (table `parts`, et `draft_snippet_text` de `conversations`) :

```
[2025-08-26] Le resto 16h
[2025-08-26] Le resto 16h, je l ai...
[2025-08-28] On me surveille quel1 approchem la box est la ou du C je v me faire prendre c termine. lance l operakdfhikfdkhbxcn,
             Flag OPENNC{L4_PR3UV3_5}
[2025-09-20] On me surveille quela1 approche je t envoi ou est situe la boite elle est cacheeee deriere la stele<<djkh
             j espere que le ,mms marche, ehara koe i a ia.
             Flag OPENNC{L4_PR3UV3_5}
```

(`extract_bugle.py` pour reproduire.) Le suspect a donc tenté de prévenir un complice (`+33 85746754`) :
la « boîte » (contenant ORACLE) est cachée derrière une stèle, et il annonce l'envoi de sa position par MMS.

### 3. Éléments annexes (utiles pour la suite de la série)
- `media/0/Download/souvenir.png` : panorama équirectangulaire 16384×8192 (type Street View, bord de mer,
  pohutukawa, style Nouvelle-Zélande), téléchargé depuis `https://filebin.net/rznn9xkyjn7syoiv/souvenir.png`
  (vu dans le journal de `org.lineageos.jelly/databases/HistoryDatabase`). Miniature : `souvenir_small.jpg`.
  Probablement le lieu de la stèle pour le [5/5]. « ehara koe i a ia » est du māori.
- Historique Jelly (navigateur) : téléchargement de Discord (APK malavida), recherche `borabora`,
  `restaurant nez yotrk` → TripAdvisor restaurants New York (lien avec le [3/5], Sobro Garden),
  traces vers limewire.com, wetransfer.com, tinyurl.com.
- **Easter egg Taylor Swift** : historique du navigateur Jelly (`data-1/org.lineageos.jelly/databases/HistoryDatabase`, table `history`) :
  - id 8, 2025-08-28 04:55:00 UTC : `willow taylor swift - YouTube` (`m.youtube.com/results?search_query=willow+taylor+swift`)
  - id 9, 2025-08-28 04:55:07 UTC : `Taylor Swift - willow (Official Music Video) - YouTube` (`m.youtube.com/watch?v=RsEZmictANA`)
  - confirmé par le cache de suggestions `org.lineageos.jelly/cache/suggestion_responses/dd64a682…0` et `3733baef…0`.

Flag : ``OPENNC{L4_PR3UV3_5}``
