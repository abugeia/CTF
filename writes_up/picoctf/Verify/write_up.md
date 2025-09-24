# picoCTF

Ici l'astuce consiste à savoir que la commande sha256sum peut prendre en argument un répertoire.

Une fois connecté au serveur en ssh, on peut donc faire :

```
ctf-player@pico-chall$ sha256sum files/* | grep -f checksum.txt
55b983afdd9d10718f1db3983459efc5cc3f5a66841e2651041e25dec3efd46a  files/2cdcb2de
```

puis :

```
ctf-player@pico-chall$ ./decrypt.sh files/2cdcb2de 
picoCTF{trust_but_verify_2cdcb2de}
```

Ou en one liner :

`./decrypt.sh $(sha256sum files/* | grep -f checksum.txt | awk '{print $2}')
`