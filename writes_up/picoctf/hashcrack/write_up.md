Ici on se connecte au serveur via netcat, on nous donne un hash : `482c811da5d5b4bc6d497ffa98491e38`

En le cherchant sur google on trouve directement que c'est le hash md de "password123" qu'on vient entrer dans l'invite.
Puis on nous donne `b7a875fc1ea228b9061041b7cec4bd3c52ab3ce3`, même méthode, on trouve que c'est le sha de "letmein".
Puis `916e8c4f79b25028c9e467f1eb8eee6d6bbdff965f9928310ad30a8d88697745`, sha256 de "qwerty098"

picoCTF{UseStr0nG_h@shEs_&PaSswDs!_5b836723}