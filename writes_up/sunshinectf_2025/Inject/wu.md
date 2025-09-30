## Write-up 3 — Inject (Forensic DOCX)

### Challenge
Premier challenge forensic (inject dans un `.docx`)

### Flag
**`sun{t0le_t0le_my_b3l0v3d!}`**

### Résumé
Le document Word contenait un objet OLE embarqué (`word/embeddings/oleObject1.bin`). Dans ce binaire on a trouvé une chaîne Base64. Après décodage la chaîne résultante était encodée en ROT13. ROT13 appliqué sur le texte décodé a donné le flag `sun{...}`.

### Preuve / extrait important
Chaîne Base64 trouvée dans `oleObject1.bin` :
`Zmhhe2cweXJfZzB5cl96bF9vM3kwaTNxIX0=`

* **Décodage base64** → `fha{g0yr_g0yr_zl_o3y0i3q!}`
* **ROT13**(`fha{g0yr_g0yr_zl_o3y0i3q!}`) → `sun{t0le_t0le_my_b3l0v3d!}`

### Étapes reproduites (commandes)
1.  **Décompresser le .docx (docx = zip) :**
    ```bash
    unzip Team_5_-_Inject_72725.docx -d docx_contents
    cd docx_contents
    ```
2.  **Inspecter l’embedding OLE :**
    ```bash
    file word/embeddings/oleObject1.bin
    strings -n 6 word/embeddings/oleObject1.bin | sed -n '1,200p'
    ```
3.  **Rechercher et extraire la chaîne base64 :**
    ```bash
    # Trouver les candidats base64
    grep -a -oE "[A-Za-z0-9+/]{20,}={0,2}" word/embeddings/oleObject1.bin

    # Décoder la chaîne trouvée
    echo 'Zmhhe2cweXJfZzB5cl96bF9vM3kwaTNxIX0=' | base64 -d
    # Affiche : fha{g0yr_g0yr_zl_o3y0i3q!}
    ```
4.  **Appliquer ROT13 pour obtenir le flag :**
    ```bash
    echo 'fha{g0yr_g0yr_zl_o3y0i3q!}' | tr 'A-Za-z' 'N-ZA-Mn-za-m'
    # -> sun{t0le_t0le_my_b3l0v3d!}
    ```

### Explication technique
* Les fichiers Office modernes sont des **archives ZIP**; il est courant de trouver des objets embarqués (OLE) dans `word/embeddings`.
* L’attaquant (ou auteur du challenge) a placé une petite payload texte encodée en **base64** à l’intérieur de l’OLE pour éviter une détection immédiate par inspection visuelle.
* **ROT13** est un simple chiffrement par substitution, fréquemment utilisé en CTF pour “cacher” la chaîne finale tout en restant trivial à inverser.

### Détection / mitigation
* **Détection** : Scanner les docx pour objets OLE (chercher `word/embeddings/*.bin`) et rechercher longues chaînes Base64 dans ces objets. Automatiser extraction + décodage + recherche d’`sun{}`.
* **Mitigation** : Politiques de sécurité autour des pièces jointes (DLP) et sandboxing/scan des attachments Office. Ajouter règles YARA simples pour patterns Base64 inhabituels dans OLE.