def fun1(mot):
    newMot = ''
    for i in range(len(mot)):
        newMot += 'a'
    newListMot = list(newMot)
    for i in reversed(list(range(len(newMot)))):
        newListMot[i] = mot[len(mot) - 1 - i]
    return ''.join(newListMot)

def fun2(mot):
    newListMot = []
    for i in mot:
        newListMot.append(ord(i) + 13)
    return newListMot

def fun3(liste):
    xorWord = 42
    newListMot = []
    for i in liste:
        newListMot.append(i ^ xorWord)
    return ' '.join(map(str, newListMot))
    
flag = input('Flag : ')
print(fun3(fun2(fun1(flag))))
