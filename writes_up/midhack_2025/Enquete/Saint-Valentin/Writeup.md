# Saint-Valentin

Catégorie : Enquête — Points : 100 — Événement : MidHack 2025 (qualif)

## Énoncé

Ned : Tauira m'a parlé d'un fichier `pdf` qui contiendrait une info super importante sur l'origine des choses étranges qui se passent. Il pense qu'il a été créé à la Saint-Valentin de l'année dernière. Cela pourrait donc remonter avant le HacKagou 2024, mais ils ont fait quoi l'équipe du HacKagou là ?

Jocelyne : Ah ? Et tu l'as ce fichier ?

Ned : Non, mais je peux le chercher sur les serveurs. Par contre il va me falloir la date exacte, car a priori elle a été modifiée par l'entité hostile qui semble se répandre partout. Je pense en particulier à du [Time Stomping](https://attack.mitre.org/techniques/T1070/006/)

Jocelyne : OK, tu veux que je retrouve la date et l'heure ?

Ned : Oui s'il te plaît, j'ai réussi à récupérer des évènements système de type sysmon, je t'envoie le fichier `.evtx`.

Jocelyne : Okay !

![MITRE ATT&CK](midhack_chall04_mitre_attack.png)

Format du flag : `OPENNC{YYYY-MM-DD HH:MM:SS}`

Fichier fourni : `journal_sysmon.evtx.zip` (contient `journal_sysmon.evtx`).

## Résolution

Le scénario pointe vers la technique MITRE **T1070.006 – Indicator Removal: Timestomp**.
Sysmon journalise précisément cette action avec l'**Event ID 2 – « A process changed a file creation time »**, qui conserve à la fois l'ancienne (`PreviousCreationUtcTime`) et la nouvelle (`CreationUtcTime`) date de création.

Extraction du journal (pas d'`unzip` sur la machine, on passe par `zipfile`) :

```bash
python3 -c "import zipfile;zipfile.ZipFile('journal_sysmon.evtx.zip').extractall('.')"
```

Parcours des événements avec `python-evtx` et filtrage des Event ID 2 concernant un PDF :

```bash
uv run --with python-evtx python -c "
import Evtx.Evtx as evtx, re
with evtx.Evtx('journal_sysmon.evtx') as log:
    for rec in log.records():
        x=rec.xml()
        m=re.search(r'<EventID[^>]*>(\d+)</EventID>',x)
        if m and m.group(1)=='2':
            d={dm.group(1):dm.group(2) for dm in re.finditer(r'<Data Name=\"([^\"]+)\">([^<]*)</Data>',x)}
            print(d.get('TargetFilename'),'|prev:',d.get('PreviousCreationUtcTime'),'|new:',d.get('CreationUtcTime'))
" | grep -i pdf
```

Résultat :

```
C:\Users\CyberJunkie\AppData\Roaming\Photo and Fax Vn\Photo and vn 1.1.2\install\F97891C\TempFolder\~.pdf
  |prev: 2024-02-14 03:41:58.404
  |new:  2024-01-14 08:10:06.029
```

L'événement complet (extrait) :

```xml
<Data Name="RuleName">technique_id=T1070.006,technique_name=Timestomp</Data>
<Data Name="UtcTime">2024-02-14 03:41:58.404</Data>
<Data Name="Image">C:\Users\CyberJunkie\Downloads\Preventivo24.02.14.exe.exe</Data>
<Data Name="TargetFilename">...\TempFolder\~.pdf</Data>
<Data Name="CreationUtcTime">2024-01-14 08:10:06.029</Data>
<Data Name="PreviousCreationUtcTime">2024-02-14 03:41:58.404</Data>
```

Le processus malveillant `Preventivo24.02.14.exe.exe` (leurre de type facture, son nom encode d'ailleurs `24.02.14`) a antidaté la date de création du PDF :
- `PreviousCreationUtcTime` = **2024-02-14 03:41:58** (date de création réelle du fichier avant modification = Saint-Valentin, en UTC) ;
- `CreationUtcTime` = **2024-01-14 08:10:06** (date posée par l'attaquant après le timestomp — la date que porte désormais le fichier).

C'est le seul PDF du journal, et le seul fichier associé à un événement de time stomping sur un PDF. Il n'existe aucun FileCreate (EID 11) pour ce PDF ; seulement cet EID 2 et un EID 23 (suppression).

### Candidats (par ordre de probabilité)

La valeur « intuitive » `OPENNC{2024-02-14 03:41:58}` (date de création réelle recouvrée, en UTC) **a été refusée** par la plateforme, de même que sa variante avec millisecondes. Les candidats restants :

1. `OPENNC{2024-01-14 08:10:06}` — la date de création **modifiée** par l'attaquant (`CreationUtcTime`), c.-à-d. la date « exacte » que porte réellement le fichier maintenant. C'est l'unique autre valeur littérale de date de création présente dans l'événement, et elle colle au récit (« la date a été modifiée... il va me falloir la date exacte » pour retrouver le fichier). **Candidat privilégié.**
2. `OPENNC{2024-02-14 14:41:58}` — date de création réelle (`PreviousCreationUtcTime`) convertie en heure locale Nouvelle-Calédonie (UTC+11), ce qui reste le 14 février (Saint-Valentin). Plausible si les organisateurs ont lu l'horodatage dans un observateur d'événements configuré en fuseau NC.
3. `OPENNC{2024-01-14 19:10:06}` — date modifiée convertie en heure locale NC (UTC+11).

Flag : `OPENNC{2024-01-14 08:10:06}`

> Piège : le flag est la date **modifiée** posée par l'attaquant (CreationUtcTime), pas la date réelle (PreviousCreationUtcTime = 2024-02-14). C'est « la date exacte que porte le fichier » pour le retrouver.
