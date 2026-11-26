"""Datos numéricos de las figuras del Tema 1 (curvas implícitas, campos, familias)."""
import numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
D='/home/user/sistemas-de-ODE-lineales/fuentes/figuras/t1/datos/'

def guarda_curvas(nombre, segs):
    """segs: lista de arrays (n,2); se separan con línea en blanco (saltos)."""
    with open(D+nombre,'w') as f:
        f.write('x y\n')
        for s in segs:
            for x,y in s: f.write(f'{x:.5f} {y:.5f}\n')
            f.write('\n')

def contorno(F, xr, yr, nivel, n=900, ymax=None):
    X,Y=np.meshgrid(np.linspace(*xr,n),np.linspace(*yr,n))
    with np.errstate(all='ignore'): Z=F(X,Y)
    Z=np.where(np.abs(X)<0.03,np.nan,Z)
    cs=plt.contour(X,Y,Z,levels=[nivel]); plt.close('all')
    segs=[]
    for p in cs.allsegs[0]:
        if len(p)>3: segs.append(p)
    return segs

def campo(f, xr, yr, nx, ny, L, nombre, filtro=None):
    rows=[]
    for x in np.linspace(*xr,nx):
        for y in np.linspace(*yr,ny):
            if filtro and not filtro(x,y): continue
            with np.errstate(all='ignore'): m=f(x,y)
            if not np.isfinite(m): continue
            u,v=1.0,m; n=np.hypot(u,v); u,v=u/n*L,v/n*L
            rows.append((x-u/2,y-v/2,u,v))
    np.savetxt(D+nombre,np.array(rows),header='x y u v',comments='',fmt='%.4f')

def funcion(nombre, fs, xr, n=1200, ylim=50):
    """varias funciones y=f(x) -> un archivo con columnas y1..yk; |y|>ylim -> nan."""
    x=np.linspace(*xr,n); cols=[x]
    for f in fs:
        with np.errstate(all='ignore'): y=f(x)
        y=np.where(np.abs(y)>ylim,np.nan,y); cols.append(y)
    hdr='x '+' '.join(f'y{i}' for i in range(1,len(fs)+1))
    np.savetxt(D+nombre,np.column_stack(cols),header=hdr,comments='',fmt='%.5f')

# f02: y = x(x^2+2+C)/(x^2+C)
Cs=[-3,-1.5,-0.75,0.5,1.5,3,6]
funcion('f02.dat',[ (lambda x,C=C: x*(x**2+2+C)/(x**2+C)) for C in Cs],(-4,4),n=4001,ylim=16)
# f04: y^2 + 1/x = 2 + C e^{-y^2/2}
for i,C in enumerate([-2,-0.5,0,1,3]):
    segs=contorno(lambda X,Y,C=C: Y**2+1/X-2-C*np.exp(-Y**2/2),(-4,4),(-3,3),0.0)
    guarda_curvas(f'f04_{i}.dat',segs)
campo(lambda x,y: 1/(x*y*(x*y**2+1)),(-3.8,3.8),(-2.8,2.8),17,13,0.32,'f04_campo.dat',
      filtro=lambda x,y: abs(x)>0.15 and abs(y)>0.1)
print('ok')

# f09: y' = x - y ; f10 campo tenue ; f11: y' = sqrt(y)
campo(lambda x,y: x-y,(-1.85,3.85),(-2.8,2.8),19,15,0.26,'f09_campo.dat')
campo(lambda x,y: x-y,(-1.85,3.85),(-2.8,2.8),19,15,0.22,'f10_campo.dat',
      filtro=lambda x,y: min(abs(y-(x-k)) for k in (-1,0,1,2))>0.35)
campo(lambda x,y: np.sqrt(y),(-0.85,3.85),(0.25,3.85),16,11,0.24,'f11_campo.dat',
      filtro=lambda x,y: abs(y-(x*x/4 if x>0 else -9))>0.25)
print('ok2')

# curvas implícitas por contornos
def familia(prefijo, F, xr, yr, niveles, n=900):
    for i,c in enumerate(niveles):
        guarda_curvas(f'{prefijo}_{i}.dat', contorno(F,xr,yr,c,n))
familia('f18',lambda X,Y: 0.5*np.exp(2*X)*(X**2*Y**2+3),(0.0,2.6),(-16,16),[2,5,10,20,50,100,200])
familia('f19',lambda X,Y: np.exp(Y)*(X**2*Y**3+1),(-16,16),(0.0,5.2),[1.5,3,5,10,20,50,100])
familia('f37',lambda X,Y: X+2*Y+3*np.log(np.abs(2*X+3*Y-7)),(-2.2,8.2),(-2.2,8.2),[-5,0,5,10,15],n=1200)
familia('f43',lambda X,Y: X**3+2*X**2*Y+Y**3,(-3.2,3.2),(-3.2,3.2),[-10,-3,0,3,10])
familia('f44',lambda X,Y: (X+Y**2)**2-0*Y,(-2.2,5.2),(-2.6,2.6),[0])  # placeholder
for i,k in enumerate([-5,-2,2,5,10]):
    guarda_curvas(f'f44_{i}.dat',contorno(lambda X,Y,k=k:(X+Y**2)**2-k*(X-Y**2),(-2.2,5.2),(-2.6,2.6),0.0,1000))
# f25: Lagrange paramétrica x=(k+ln|v|)/v^2, y=(2k+2ln|v|+1)/v
segs=[]
for i,k in enumerate([-1.5,-0.5,0.5,1.5,2.5]):
    out=[]
    for rng in [(0.05,6),(-6,-0.05)]:
        v=np.linspace(*rng,3000); x=(k+np.log(np.abs(v)))/v**2; y=(2*k+2*np.log(np.abs(v))+1)/v
        m=(np.abs(x)<4)&(np.abs(y)<6)
        x=np.where(m,x,np.nan); y=np.where(m,y,np.nan)
        out.append(np.column_stack([x,y]))
    with open(D+f'f25_{i}.dat','w') as f:
        f.write('x y\n')
        for a in out:
            for xx,yy in a: f.write(f'{xx:.5f} {yy:.5f}\n' if np.isfinite(xx) else 'nan nan\n')
            f.write('nan nan\n')
print('ok3')
