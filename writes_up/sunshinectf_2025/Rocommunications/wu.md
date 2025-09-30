### Challenge
Robox shirt dans la boutique du groupe SunshineCTF

### Flag
**`sun{w0w_1_L0v3_Squ4r3_ass3ts}`**

### Résumé
Le seul item dans la boutique du groupe était un Shirt. La texture (image PNG) liée au Shirt contenait, sur une bande graphique, le flag écrit en texte lisible. Il fallait récupérer l’asset image via l’API d’asset delivery Roblox, l’ouvrir et l’extraire (zoom / enhancement si nécessaire).

### Preuve / extrait important
* **Asset ID du shirt** : `110009297654947` (page du catalogue)
* L’XML/asset a référencé la véritable image (par ex. asset id = `99859692989451`), téléchargée via `https://assetdelivery.roblox.com/v1/asset/?id=99859692989451`.
* Après ouverture et amélioration/rotation, le texte visible sur la bande est : `sun{w0w_1_L0v3_Squ4r3_ass3ts}`

### Étapes reproduites (commandes)
1.  **Récupérer la ressource via l’asset ID :**
    ```bash
    curl -L -o shirt.png "[https://assetdelivery.roblox.com/v1/asset/?id=99859692989451](https://assetdelivery.roblox.com/v1/asset/?id=99859692989451)"
    ```
2.  **Ouvrir et inspecter l’image ; si texte petit/penché, zoomer / recadrer / améliorer :**
    Utiliser GIMP / ImageMagick / PIL pour recadrer, contraster, redresser.
3.  **Exemple (Python PIL) — crop + rotate + enhance :**
    ```python
    from PIL import Image, ImageEnhance
    im = Image.open('shirt.png').convert('RGB')
    crop = im.crop((0,0,360,420)).rotate(-38, expand=True)
    crop = ImageEnhance.Contrast(crop).enhance(2.0)
    crop.save('shirt_text.png')
    ```
4.  **Lire le texte sur la bande** (manuellement ou OCR si tu veux).

### Explication technique
* Roblox stocke textures et decals en tant qu’**assets** accessibles via des endpoints d’asset delivery ; il est courant de pouvoir télécharger une texture publique si le serveur la permet.
* Ici l’auteur a mis le flag directement sous forme de **texte** (pas de stégo), il fallait juste récupérer le bon asset et appliquer un traitement d’image si le texte était difficilement lisible à cause de rotation/échelle.

### Détection / mitigation
* **Détection** : Sur une plateforme publique, difficile à empêcher — côté CTF c’est l’intention. Pour une vraie plateforme, contrôler qui peut publier assets et appliquer modération automatique (détection texte dans images).
* **Mitigation** : Restreindre la publication d’images à des comptes vérifiés et scanner pour patterns de fuite/texte sensible (OCR automatique).