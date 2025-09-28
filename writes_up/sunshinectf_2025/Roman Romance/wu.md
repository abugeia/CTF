# Roman Romance - sunshinectf 2025

## Analyse

Le challenge nous fournit un binaire `romanromance` et un fichier chiffré `enc.txt`.

En exécutant le binaire, on s'aperçoit qu'il cherche un fichier `flag.txt`. Après avoir créé un fichier `flag.txt` contenant une longue chaîne de "A", on relance le binaire. Le fichier `enc.txt` est alors modifié et contient une longue chaîne de "B". Cela nous indique que le chiffrement est probablement un simple décalage de +1 sur la valeur ASCII de chaque caractère.

L'analyse du binaire avec `ghidra` confirme cette hypothèse. Le programme lit le fichier `flag.txt`, ajoute 1 à la valeur ASCII de chaque caractère, et écrit le résultat dans `enc.txt`.

## Résolution

Il suffit donc de faire l'opération inverse : soustraire 1 à la valeur ASCII de chaque caractère de `enc.txt` pour retrouver le flag.

Voici le script python utilisé :

```python
def decrypt(ciphertext):
    decrypted_text = ""
    for char in ciphertext:
        decrypted_text += chr(ord(char) - 1)
    return decrypted_text

def main():
    with open("enc.txt", "r") as f:
        ciphertext = f.read().strip()
    
    decrypted_text = decrypt(ciphertext)
    print(decrypted_text)

if __name__ == "__main__":
    main()
```

## Flag

`sunshine{kN0w_y0u4_r0m@n_hI5t0rY}`