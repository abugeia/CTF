# Résolution : Challenge Web Simple - Analyse de Source

## Énoncé du Challenge

Trouver le flag caché dans le code source d'une page web.

## Outils Utilisés

*   Navigateur web (avec outils de développement)

## Étapes de Résolution

1.  **Accéder à la page web :** Ouvrez la page web fournie pour le challenge dans votre navigateur.
2.  **Inspecter le code source :**
    *   Faites un clic droit sur la page et sélectionnez "Inspecter l'élément" ou "Afficher le code source de la page" (selon votre navigateur).
    *   Alternativement, utilisez le raccourci clavier `Ctrl+U` (Windows/Linux) ou `Cmd+Option+U` (macOS) pour afficher le code source.
3.  **Rechercher le flag :** Parcourez le code HTML à la recherche de commentaires, de balises cachées ou de scripts suspects. Le flag est généralement au format `hackagou{...}`.

    Dans ce cas, le flag était caché dans un commentaire HTML :

    ```html
    <!-- Le flag est ici : hackagou{source_code_is_your_friend} -->
    ```

## Flag Obtenu

`hackagou{source_code_is_your_friend}`