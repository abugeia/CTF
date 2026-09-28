# Hors de Contrôle : Borne, Elizabeth ! [3/5] (2025)
Catégorie : OSINT — Points : 250 (dynamique, min 150) — Auteur : Ketsui

## Énoncé
La situation est critique. Vous êtes désormais prêt pour votre première vraie mission :
Le MEH confirme que la fuite de la puce Oracle n'est pas le résultat d'une intrusion extérieure, mais d'une compromission interne.
Plus discrète. Plus précise. Plus efficace.

Un employé clé manque à l'appel, et toutes les preuves pointent vers lui.
Votre objectif : localiser cet agent avant qu'il ne disparaisse définitivement.

Nos équipes de traque ont intercepté plusieurs fragments d'informations numériques.
Ces données contiennent assez d'indices pour retrouver le nom du restaurant où il a pris ses habitudes. Cela nous permettra de lui mettre la main dessus.

**Votre mission**

Analysez les éléments fournis, recoupez les pistes et dévoilez le nom exact du restaurant fréquenté par la cible.

Format du flag : `OPENNC{Nom_Restaurant}`

Fichier : [Transcript.pdf](Transcript.pdf)

## Résolution
### 1. Le PDF
`Transcript.pdf` est un export Google Sheets. On en extrait le texte avec [extract_pdf.py](extract_pdf.py) (`uv run --with pymupdf python extract_pdf.py Transcript.pdf`). Il n'y a ni texte caché, ni image, ni lien. Il contient deux tableaux :

| Numéro | Temps | Zone | Stamp |
|---|---|---|---|
| (248) 145-7324 | 67666 | 40.82,-73.93 | 24/08/2025 11:04 |
| (248) 145-7324 | 3636 | 40.81, -73.94 | 24/08/2025 11:30 |
| (248) 145-7324 | - | 40.80, -73.93 | 24/08/2025 12:02 |
| (248) 145-7324 | 8930 | - | |

Messagerie « OnChat » du 24/08/2025 :
- « On mange quoi ce soir ? »
- « Je voulais tester le resto, tu sais celui qui est derière l'ancien batiment qui avait le grand insigne radio ? »
- « A oui l'ancien grand panneau. en dessous il y avait à l'époque un ecran de led. Nov 2017 ahhh la premiere fois que je voyais la pub de **taylor swift** et que son album **réputation** passé en boucle sur cette radio. »
- « C ça oui, le resto Restaurant portoricain »
- « OK ben je passerai vers midi commander pour ce soir. Et si on aime alors ça sera notre rituel chaque vendredi »

### 2. Localisation
Les coordonnées (40.80–40.82 N, 73.93–73.94 O) situent la cible au sud du Bronx (Mott Haven / Port Morris, New York), sur la rive de la Harlem River. Le point de 12:02 (« vers midi commander ») est `40.80,-73.93`.

Le « grand insigne radio » posé sur un ancien bâtiment, avec un écran LED en dessous, est le célèbre panneau du **Bruckner Building, 20 Bruckner Boulevard** (Bronx). Pendant plus de 15 ans, ce panneau a porté les logos de sept marques, dont **iHeartRadio** (puis Uber et History Channel). SNA Displays y a installé un écran LED de 2 096 × 256 px. En novembre 2017, iHeartRadio a promu l'album *reputation* de Taylor Swift (iHeartRadio reputation Album Release Party, station « Taylor Swift reputation Radio »). Cela colle avec le message.

Sources : [Bronx Times, « History Channel advertisement is now history »](https://www.bxtimes.com/history-channel-advertisement-is-now-history/), [SNA Displays, Bruckner Building](https://snadisplays.com/projects/iconic-nyc-billboard-bruckner-building/), [iHeartMedia, reputation release party](https://www.iheartmedia.com/press/iheartmedia-presents-iheartradio-reputation-album-release-party-taylor-swift-presented-att).

### 3. Le restaurant portoricain
Premier essai refusé : `OPENNC{Made_In_Puerto_Rico}`. C'était l'ancien occupant du 26 Bruckner Blvd, qui a fermé puis déménagé à East Tremont.

On cherche « puerto rican restaurant » sur Google Maps (via Playwright), centré sur le Bruckner Building (`@40.8065,-73.9296,17z`). La fiche **Sobro Garden** sort immédiatement :
- catégorie Google : *Puerto Rican restaurant*, « Identifies as Latino-owned » ;
- adresse : **26 Bruckner Blvd, Bronx, NY 10454**, « Located in: **Piano Factory** ». C'est l'ancienne usine de pianos Estey, c'est-à-dire le bâtiment qui portait le panneau radio. Le pin est à 40.80685,-73.92840, donc côté arrière du bâtiment ;
- ouverture en 2025 : la page Facebook s'appelle `sobro.garden.2025`, ce qui correspond au transcript du 24/08/2025 (« je voulais tester le resto ») ;
- sert des plats portoricains (pernil, paella de la casa) et ouvre jusqu'à 2 h.

Les autres restaurants portoricains du secteur sont trop loin du bâtiment : La Pequeña Lechonera (40.8028,-73.9341), El Patio De Fela, El Viejo Gran Cafe (Bruckner/Willis) et El Rincón Boricua.

Sources : [Google Maps – Sobro Garden](https://www.google.com/maps/search/Sobro+Garden+Bronx), [NYC Tourism](https://www.nyctourism.com/restaurants/sobro-garden/), [Yelp](https://www.yelp.com/biz/sobro-garden-bronx), [Facebook](https://www.facebook.com/sobro.garden.2025/), [Toast](https://www.toasttab.com/local/order/sobro-garden-26-bruckner-blvd).

Relecture du PDF brut (spans PyMuPDF, couleurs, métadonnées) : rien de caché. Tout le texte est noir, l'auteur est vide et le créateur est « Google Sheets ». Les colonnes « Temps » et « Zone » (67666, 3636, 8930) ne sont pas exploitées ; ce sont probablement des leurres ou des identifiants de cellule factices. L'indicatif (248) (Michigan) n'est pas exploité non plus. Le titre « Borne, Elizabeth ! » est un jeu de mots sur Élisabeth Borne, commun à la série.

Mention de Taylor Swift : oui, dans le transcript (pub LED de novembre 2017 pour l'album *reputation*).

Refusé : `OPENNC{Made_In_Puerto_Rico}`.

Flag : ``OPENNC{Sobro_Garden}``
