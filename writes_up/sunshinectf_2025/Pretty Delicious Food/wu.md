## Write-up 5 — Pretty Delicious Food (PDF with embedded file)

### Challenge
PDF (non stégo) — “something else is out of place too.”

### Flag
**`sun{p33p_d1s_fl@g_y0!}`**

### Résumé
Le PDF contenait une pièce jointe embarquée (embedded file) nommée `payload.txt`. Ce fichier contenait une ligne JavaScript définissant une variable `data` qui était une chaîne Base64. Le décodage du Base64 a donné directement le flag.

### Preuve / extrait important
Fichier embarqué `payload.txt` :
`const data = 'c3Vue3AzM3BfZDFzX2ZsQGdfeTAhfQ==';`

**Décodage** :
```bash
echo 'c3Vue3AzM3BfZDFzX2ZsQGdfeTAhfQ==' | base64 -d
# -> sun{p33p_d1s_fl@g_y0!}
```

### Étapes reproduites (commandes)
1.  **Inspecter le PDF et lister pièces jointes :**
    Avec python `fitz` (PyMuPDF) :
    ```python
    import fitz
    doc = fitz.open("prettydeliciouscakes.pdf")
    print("embedded file count:", doc.embfile_count())
    for i in range(doc.embfile_count()):
        info = doc.embfile_info(i)
        data = doc.embfile_get(i)
        open(f"extracted_{i}_{info.get('filename','payload')}", "wb").write(data)
        print("extracted", info)
    ```
    Ou avec `exiftool` / `pdfdetach` si disponible.

2.  **Lire le payload et décoder :**
    ```bash
    cat payload.txt
    # shows: const data = 'c3Vue3AzM3BfZDFzX2ZsQGdfeTAhfQ==';
    
    # Extract base64 and decode:
    echo 'c3Vue3AzM3BfZDFzX2ZsQGdfeTAhfQ==' | base64 -d
    # -> sun{p33p_d1s_fl@g_y0!}
    ```

### Explication technique
* Les PDF peuvent contenir des **fichiers embarqués** (attachments) via la structure `/EmbeddedFiles`.
* Ici l’auteur a mis le flag sous forme de **Base64** dans un petit script texte, dissimulé comme “payload” dans le PDF.

### Détection / mitigation
* **Détection** : Analyser automatiquement les PDFs entrants pour pièces jointes et les scanner (recherche de Base64, patterns suspects `sun{}`).
* **Mitigation** : Politique de blocage ou d’analyse approfondie des attachments dans les PDF (DLP). Pour un CTF, ce comportement est voulu.

---

## Annexes utiles (commandes résumé)

### Décompresser docx / lister OLE
```bash
unzip file.docx -d out
strings -n 6 out/word/embeddings/oleObject1.bin | head
```

### Décodage base64 + ROT13
```bash
echo 'BASE64_CH' | base64 -d | tr 'A-Za-z' 'N-ZA-Mn-za-m'
```

### Récupérer asset Roblox
```bash
curl -L -o shirt.png "[https://assetdelivery.roblox.com/v1/asset/?id=ASSET_ID](https://assetdelivery.roblox.com/v1/asset/?id=ASSET_ID)"
```

### Extraire embedded file d’un PDF (PyMuPDF)
```python
import fitz
doc = fitz.open("file.pdf")
for i in range(doc.embfile_count()):
    info = doc.embfile_info(i)
    open(info['filename'],"wb").write(doc.embfile_get(i))
```