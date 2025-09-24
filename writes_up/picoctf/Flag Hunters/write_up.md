# picoCTF

Le cœur du programme est la fonction reader, qui agit comme un interpréteur pour les paroles de la chanson. Elle lit le texte ligne par ligne en utilisant une variable lip (Line Instruction Pointer) comme un pointeur vers la ligne actuelle à exécuter.

Le Pointeur de Ligne (lip) : Cette variable décide quelle ligne de song_lines sera lue ensuite. La plupart des commandes, comme l'affichage d'une ligne de parole, incrémentent simplement lip de 1 (lip += 1).

Les Commandes Spéciales :

REFRAIN : Fait sauter lip au début du refrain.

RETURN [nombre] : La commande la plus importante pour nous. Elle fait sauter lip à la ligne spécifiée par [nombre] (ex: RETURN 4 met lip = 4).

L'Entrée Utilisateur (CROWD) : Quand le programme rencontre une ligne contenant CROWD, il te demande de saisir du texte via input('Crowd: '). Le problème est que le texte n'est pas directement interprété comme une commande. Le code le préfixe avec "Crowd: ", ce qui empêche une commande comme RETURN 4 d'être reconnue par l'expression régulière re.match(r"RETURN [0-9]+").

L'Astuce du Point-Virgule (;) : La ligne la plus importante du code est for line in song_lines[lip].split(';'). Le programme sépare une ligne en plusieurs commandes si elles sont séparées par un point-virgule.

C'est ici que se trouve la faille. Si tu fournis une entrée qui contient un point-virgule, comme mon_texte;RETURN 4, la ligne sera modifiée pour devenir 'Crowd: mon_texte;RETURN 4'. Lorsque cette ligne sera (ré)exécutée, le split(';') la découpera en deux "commandes" :

'Crowd: mon_texte'

'RETURN 4'

La deuxième partie, 'RETURN 4', sera reconnue comme une commande valide et redirigera le programme pour qu'il lise la ligne 4 !

Donc une entrée `;RETURN 0` renvoi le flag.

picoCTF{70637h3r_f0r3v3r_b248b032}