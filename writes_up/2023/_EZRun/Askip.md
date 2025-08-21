Un message codé a été intercepté par l'un de nos perroquets.

> 79 80 69 78 78 67 123 87 104 52 55 95 49 53 95 52 53 99 49 49 63 33 125

Trouvez sa signification !

## Résolution

Ces chiffre sont tout simplement les valeurs ascii des caractères pour obtenir le flag, il faut les convertir pour obtenir les lettres.

Possible en python avec le code suivant  : 

```python
message = [79, 80, 69, 78, 78, 67, 123, 87, 104, 52, 55, 95, 49, 53, 95, 52, 53, 99, 49, 49, 63, 33, 125]

for c in message:
	print(chr(c),end='')
```

On obtient comme résultat : 

> [!question]- Spoiler pour le Flag 
OPENNC{Wh47_15_45c11?!}

