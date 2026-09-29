import re,math,numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
xs,ys=[],[]
pat=re.compile(r'sub_pos=([\d.\-]+),([\d.\-]+) \| sub_yaw=([\d.\-]+) \| env=([\d.\-]+),([\d.\-]+),([\d.\-]+) \| ping=([\d.\-]+),([\d.\-]+),([\d.\-]+)')
for line in open('/home/ubuntu/perso/ctf/ctfd-downloads/sonar.log'):
    m=pat.search(line)
    if not m: continue
    sx,sy,yaw,depth,temp,sal,angle,dt,inten=map(float,m.groups())
    if inten<150: continue
    T,S,z=temp,sal,depth
    c=1449.2+4.6*T-0.055*T**2+0.00029*T**3+(1.34-0.01*T)*(S-35)+0.016*z
    r=c*dt/2.0
    xs.append(sx+r*math.cos(yaw+angle)); ys.append(sy+r*math.sin(yaw+angle))
xs=np.array(xs); ys=np.array(ys)
# fit ripple: median Y per X-bin then fit sine
def sine(x,A,w,p,o): return A*np.sin(w*x+p)+o
# bin
order=np.argsort(xs); X=xs[order]; Y=ys[order]
bins=np.linspace(X.min(),X.max(),40); cx=[];cy=[]
for i in range(len(bins)-1):
    msk=(X>=bins[i])&(X<bins[i+1])
    if msk.sum()>0: cx.append((bins[i]+bins[i+1])/2); cy.append(np.median(Y[msk]))
cx=np.array(cx);cy=np.array(cy)
try:
    popt,_=curve_fit(sine,cx,cy,p0=[3,2*math.pi/26,0,36.5],maxfev=20000)
    print("fit A,w,p,o=",popt,"period=",2*math.pi/popt[1])
    ys_corr=ys-sine(xs,popt[0],popt[1],popt[2],0)
except Exception as e:
    print("fit fail",e); ys_corr=ys
plt.figure(figsize=(30,5))
plt.scatter(xs,ys_corr,s=45,c='k')
plt.gca().set_aspect("equal"); plt.gca().invert_yaxis()
plt.savefig('sonar_flip.png',dpi=90,bbox_inches='tight')
print("saved")
