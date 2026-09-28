import sys,re,subprocess,io,urllib.request
from PIL import Image
H={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) Chrome/130','Referer':'https://www.google.com/maps/'}
def get(u,h=True):
    return urllib.request.urlopen(urllib.request.Request(u,headers=H if h else {}),timeout=30).read()
def find(lat,lng,r=50):
    u=f"https://maps.googleapis.com/maps/api/js/GeoPhotoService.SingleImageSearch?pb=!1m5!1sapiv3!5sUS!11m2!1m1!1b0!2m4!1m2!3d{lat}!4d{lng}!2d{r}!3m18!2m2!1sen!2sUS!9m1!1e2!11m12!1m3!1e2!2b1!3e2!1m3!1e3!2b1!3e2!1m3!1e10!2b1!3e2!4m6!1e1!1e2!1e3!1e4!1e8!1e6&callback=_xdc_._v2mub5"
    t=get(u,False).decode()
    m=re.search(r'"([A-Za-z0-9_-]{22})"',t)
    ll=re.search(r'\[\[null,null,(-?[0-9.]+),(-?[0-9.]+)\]',t)
    d=re.search(r'\[(20\d\d),(\d+)\]\]',t)
    return (m.group(1) if m else None, ll.groups() if ll else None, d.groups() if d else None)
def pano(p,z=2,out='p.jpg'):
    nx,ny=2**z,2**(z-1)
    im=Image.new('RGB',(512*nx,512*ny))
    for x in range(nx):
        for y in range(ny):
            b=get(f"https://streetviewpixels-pa.googleapis.com/v1/tile?cb_client=maps_sv.tactile&panoid={p}&x={x}&y={y}&zoom={z}&nbt=1&fover=2")
            im.paste(Image.open(io.BytesIO(b)),(512*x,512*y))
    im.save(out)
if __name__=='__main__':
    lat,lng=sys.argv[1],sys.argv[2]; r=sys.argv[3] if len(sys.argv)>3 else 50
    out=sys.argv[4] if len(sys.argv)>4 else 'p.jpg'
    p,ll,d=find(lat,lng,r); print(p,ll,d)
    if p: pano(p,2,out)
