# BASEic

## Instructions

The space base is in danger and we lost the key to get in!

Fichier fourni : BASEic

## Analyse

Le fichier fourni est un exécutable ELF 64-bit. La première étape consiste à utiliser `strings` pour extraire les chaînes de caractères. On y trouve notamment `c3Vue2MwdjNyMW5nX3V`, qui ressemble à du Base64.

Pour comprendre comment le binaire valide le flag, on peut commencer par une analyse statique avec `objdump`.
```bash
wsl objdump -d writes_up/sunshinectf_2025/BASEic/BASEic
```
Dans le désassemblage de la fonction `main`, il faut chercher la logique de traitement de l'entrée utilisateur. On peut typiquement repérer un appel à `scanf` (pour lire l'entrée), suivi d'un appel à `strlen` (pour en obtenir la longueur). Juste après l'appel à `strlen`, le programme compare la longueur obtenue. C'est là qu'on trouve l'instruction cruciale :
```
153d: e8 ae fb ff ff          call   10f0 <strlen@plt>
1542: 48 83 f8 16             cmp    $0x16,%rax
```
Cette instruction compare (`cmp`) la longueur de la chaîne (dont la valeur est retournée par `strlen` dans le registre `%rax`) à la valeur hexadécimale `0x16`, qui est 22 en décimal. Le programme n'ira plus loin que si la longueur est exactement de 22 caractères.

Sachant cela, on peut utiliser `ltrace` en lui fournissant une chaîne de 22 caractères qui commence par le décodage du premier fragment. Par exemple, `sun{c0v3r1ng_uAAAAAAA}`.

Voici la sortie de `ltrace` avec cette entrée incorrecte :
```
printf("What is the flag> ")                               = 18
__isoc99_scanf(0x55b95389f094, 0x7ffc448972d0, 0, 0)       = 1
strlen("sun{c0v3r1ng_uAAAAAAA}")                           = 22
<previous line repeated 1 additional times>
malloc(33)                                                 = 0x55b96fa646c0
strncmp("c3Vue2MwdjNyMW5nX3VBQUFBQUFBfQ=="..., "c3Vue2MwdjNyMW5nX3V", 19) = 0
strlen("yX0I0NTM1fQ==")                                    = 13
strncmp("BQUFBQUFBfQ==", "yX0I0NTM1fQ==", 13)              = -55
puts("Soo Close"What is the flag> Soo Close
)                                          = 10
free(0x55b96fa646c0)                                       = <void>
+++ exited (status 0) +++
```

Cette sortie est très instructive :
1.  La première `strncmp` compare notre entrée encodée avec la chaîne `c3Vue2MwdjNyMW5nX3V`. La comparaison réussit sur les 19 premiers caractères.
2.  La deuxième `strncmp` est la clé. Elle compare la fin de notre chaîne encodée (`BQUFBQUFBfQ==`, qui correspond à `AAAAAAA}`) avec la chaîne `yX0I0NTM1fQ==`.

Il suffit donc de décoder `c3Vue2MwdjNyMW5nX3V` et `yX0I0NTM1fQ==` et de les concaténer pour obtenir le flag.

Un simple script Python permet de faire cela :
```python
import base64

part1_encoded = "c3Vue2MwdjNyMW5nX3V"
part2_encoded = "yX0I0NTM1fQ=="

part1_decoded = base64.b64decode(part1_encoded + "==").decode()
part2_decoded = base64.b64decode(part2_encoded).decode()

flag = part1_decoded + part2_decoded
print(flag)
# Output: sun{c0v3r1ng_ur_B4535}
```

## Flag

`sun{c0v3r1ng_ur_B4535}`