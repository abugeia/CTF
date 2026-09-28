from PIL import Image; import numpy as np, re, sys, itertools
def show(name,bits):
    for order in ('msb','lsb'):
        b=np.packbits(bits,bitorder='big' if order=='msb' else 'little').tobytes()
        m=re.findall(rb'[ -~]{6,}',b)
        if m: print(name,order,[x[:80] for x in m[:5]])
im=Image.open(sys.argv[1]); print(im.mode,im.size,im.info.keys())
if im.mode=='P':
    a=np.array(im); 
    for k in range(8): show(f'idx b{k}',((a>>k)&1).reshape(-1)); show(f'idx b{k} col',((a>>k)&1).T.reshape(-1))
    im=im.convert('RGBA')
a=np.array(im.convert('RGBA'))
chs='RGBA'
for combo in ['R','G','B','A','RGB','RGBA','BGR']:
    idx=[chs.index(c) for c in combo]
    for k in range(8):
        sub=a[:,:,idx]
        show(f'{combo} b{k} xy',((sub>>k)&1).reshape(-1))
        show(f'{combo} b{k} yx',((sub.transpose(1,0,2)>>k)&1).reshape(-1))
