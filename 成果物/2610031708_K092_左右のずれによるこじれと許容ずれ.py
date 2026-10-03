# K092 左右のずれが大きいときのこじれ（幾何学的な非線形）と収納付近の許容ずれ（STEP4 4-3）
# 左右のCはどちらも鉛直線上しか動けない（水平・鉛直版スコットラッセル）。CSPは剛体で、CとC′の d方向の間隔は Δd=180mm（側面に投影）。
# 片側のCがもう片側より Δh 低いと、剛体のCSPを保つには d方向の間隔が √(Δd²−Δh²) に縮む必要があるが、Cは鉛直線上しか動けないため、
#   縮もうとする量 e＝Δd−√(Δd²−Δh²) を、機構の d方向のばね（左右直列）が受け止め、その力 F＝k·e がこじれとして入る。
# 機構の d方向のばね k：K086と同じ立体骨組み（リンク角パイプ25×25×2.3、O固定ピン、B固定）で、片側のCに d方向の力を与えたときの変位から求める（左右直列）。
# Δh：遅い側のBが δB 遅れたときの Cの高さの差（厳密な機構の式）。早い側は収納端（φ=7.0°）で停止しているとする。
import math, csv, subprocess, numpy as np
TS=subprocess.run(['date','+%y%m%d%H%M'],capture_output=True,text=True,env={'TZ':'Asia/Tokyo'}).stdout.strip()
src=open('/tmp/k086.py',encoding='utf-8').read().split("Opos={'左':52.0")[0]
exec(src)
def side_k(sn,si):
    xl,Od=SIDES[sn]; P=pose(Od,si); X=lambda q:np.array([xl,q[0],q[1]])*10.0
    nodes={'O':X(P['O']),'B':X(P['B']),'OAO':X(P['O']),'OAA':X(P['A']),'ABA':X(P['A']),'ABB':X(P['B']),'ACA':X(P['A']),'ACC':X(P['C'])}
    names=list(nodes); ix={n:i for i,n in enumerate(names)}; N=6*len(names); K=np.zeros((N,N))
    for n1,n2 in (('OAO','OAA'),('ABA','ABB'),('ACA','ACC')):
        ke,_,_=kel(nodes[n1],nodes[n2],A_,I_,I_,J_); dof=list(range(6*ix[n1],6*ix[n1]+6))+list(range(6*ix[n2],6*ix[n2]+6)); K[np.ix_(dof,dof)]+=ke
    kp=1e9
    def tie(n1,n2,cs):
        for c_ in cs:
            i,j=6*ix[n1]+c_,6*ix[n2]+c_; K[i,i]+=kp; K[j,j]+=kp; K[i,j]-=kp; K[j,i]-=kp
    tie('O','OAO',(0,1,2,4,5)); tie('OAA','ABA',(0,1,2,4,5)); tie('ABA','ACA',range(6)); tie('B','ABB',(0,1,2,4,5))
    fixed=[6*ix['O']+c for c in (0,1,2)]+[6*ix['B']+c for c in (0,1,2,4,5)]
    f=np.zeros(N); f[6*ix['ACC']+1]=1.0
    free=[i for i in range(N) if i not in fixed]
    for i in free: K[i,i]+=1e-6
    u=np.zeros(N); u[free]=np.linalg.solve(K[np.ix_(free,free)],f[free])
    return 1.0/u[6*ix['ACC']+1]   # N/mm
a=500.0; p0=math.radians(7.0)
def hC(xB): return math.sqrt(max((2*a)**2-xB**2,0))   # Cの高さ（Oから下へ）＝2a·sinφ、xB＝2a·cosφ
kL=side_k('左',0); kR=side_k('右',0); k=1/(1/kL+1/kR)
print('d方向のばね 左',round(kL),'右',round(kR),'直列',round(k),'N/mm')
xB0=2*a*math.cos(p0)
rows=[]
for dB in (0.05,0.1,0.2,0.3,0.5,1.0,2.0,4.5):
    dh=hC(xB0-dB)-hC(xB0)   # 遅い側（Bがまだ収納側へ届いていない＝xBが小さい→Cが低い）
    e=180.0-math.sqrt(180.0**2-dh**2)
    F=k*e
    th=math.degrees(math.asin(dh/180.0))
    rows.append([dB,round(dh,2),round(th,2),round(e,4),round(F)])
    print(rows[-1])
out='/mnt/user-data/outputs/%s_K092_左右のずれによるこじれと許容ずれ.csv'%TS
with open(out,'w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f)
    w.writerow(['K092 左右のずれが大きいときのこじれ（収納付近、早い側が収納端 φ=7.0°で停止、遅い側が δB 遅れ）'])
    w.writerow(['CとC′はどちらも鉛直線上しか動けず、CSP（剛体）の d方向の間隔 Δd=180mm を保てないぶん e＝Δd−√(Δd²−Δh²) を機構の d方向のばね k（左右直列）が受け止める。F＝k·e。'])
    w.writerow(['k：K086の立体骨組み（リンク角パイプ25×25×2.3、O固定ピン、B固定）で、Cに d方向の力を与えたときの変位から：左 %d・右 %d・直列 %d N/mm。ピンのすきま（ガタ）は含まない。'%(kL,kR,k)])
    w.writerow([])
    w.writerow(['Bの遅れ δB mm','Cの高さの差 Δh mm','CSPの傾き °','縮もうとする量 e mm','こじれの力 F N（ガタなし）'])
    w.writerows(rows)
print(out)
