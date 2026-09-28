# Hors de Contrôle : Recrutement [1/5]
Catégorie : Stégano — Points : 100 — Auteur : Ketsui

## Énoncé
![](meh.webp)

Le MEH est une agence secrète spécialisée dans les interventions à travers le monde afin de neutraliser les menaces les plus dangereuses de notre ère moderne. Elle n'a ni drapeau, ni juridiction, et personne ne soupçonne son existence.

Ce que vous ignorez, c'est qu'elle sait déjà tout de vous… et s'apprête à vous soumettre à un test plutôt particulier pour vous recruter. Une énigme, peut-être ?

Attention posez-vous les bonnes questions.

Format du flag : `OPENNC{Quelque_Chose}`

Fichier : [Secret_Doc.pdf](Secret_Doc.pdf)

## Résolution
`Secret_Doc.pdf` est une page exportée depuis Google Docs (Producer `Skia/PDF m140 Google Docs Renderer`). C'est une lettre de recrutement de la MEH qui se termine par « vous saurez trouver ce qui est caché à la vue de tous », suivie de plusieurs lignes qui semblent vides.

Il suffit de sélectionner tout le texte (Ctrl+A) dans un lecteur PDF, ou d'extraire la couche texte (`pdftotext Secret_Doc.pdf -`). Une ligne en bas de page est écrite **en blanc sur fond blanc** (couleur `0xffffff`, 9 pt, position y≈677) :

```bash
uv run --with pymupdf python solve.py
# 0xffffff (72.0, 676.68, 214.59, 686.74) OPENNC{J3_SuiS_4_L4_Haut3ur}
```

Le flag se lit « Je suis à la hauteur ».

Remarques :
- Les `U+200B` (espaces de largeur nulle) en fin de certaines lignes viennent de l'export Google Docs. Ils sont trop peu nombreux et trop réguliers pour cacher un message.
- Aucune mention de Taylor Swift ni d'une chanson (easter egg du challenge « Taylor's back ») dans ce PDF : aucune occurrence de `taylor`, `swift` ou `song` dans les flux décompressés, les métadonnées ou le texte.

Flag : ``OPENNC{J3_SuiS_4_L4_Haut3ur}``
