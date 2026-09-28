# Décode code.png en comparant chaque bloc de 16 px aux glyphes chiffres dcode (Ancients, Stargate)
from PIL import Image
def load(p):
    im=Image.open(p).convert('RGBA'); bg=Image.new('RGBA',im.size,(255,255,255,255)); bg.alpha_composite(im)
    return bg.convert('L')
glyph={str(d):load(f'glyphs/{48+d}.png') for d in range(10)}
code=load('code.png')
# boîte englobante des pixels sombres
xs=[x for x in range(code.width) for y in range(code.height) if code.getpixel((x,y))<128]
ys=[y for x in range(code.width) for y in range(code.height) if code.getpixel((x,y))<128]
x0,y0=min(xs),min(ys); print('bbox',x0,y0,max(xs),max(ys))
n=(max(xs)-x0+1)//16
res=''
for k in range(n):
    best=None
    for d,g in glyph.items():
        g2=g.resize((16,max(ys)-y0+1))
        diff=sum((code.getpixel((x0+16*k+x,y0+y))<128)!=(g2.getpixel((x,y))<128) for x in range(16) for y in range(g2.height))
        if best is None or diff<best[0]: best=(diff,d)
    res+=best[1]; print(k,best)
print('Nombre :',res)
