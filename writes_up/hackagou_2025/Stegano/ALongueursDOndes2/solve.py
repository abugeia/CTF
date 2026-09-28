from PIL import Image
import numpy as np, re
im=np.array(Image.open('Steg-CTF.png').convert('RGB'))
b=np.packbits((im&1).reshape(-1)).tobytes()
m=re.match(rb'[ -~]+',b).group()
print(len(m)); print(m.decode())
MORSE={'.-':'A','-...':'B','-.-.':'C','-..':'D','.':'E','..-.':'F','--.':'G','....':'H','..':'I','.---':'J','-.-':'K','.-..':'L','--':'M','-.':'N','---':'O','.--.':'P','--.-':'Q','.-.':'R','...':'S','-':'T','..-':'U','...-':'V','.--':'W','-..-':'X','-.--':'Y','--..':'Z','-----':'0','.----':'1','..---':'2','...--':'3','....-':'4','.....':'5','-....':'6','--...':'7','---..':'8','----.':'9','--..--':',','.-.-.-':'.','-..-.':'/','-...-':'=','---...':':'}
print(' '.join(''.join(MORSE.get(c,'?') for c in w.split()) for w in m.decode().split('/')))
