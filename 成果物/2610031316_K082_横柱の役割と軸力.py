# K082 横柱の役割：剛接合・両端ピン（押し引きのみ）・なし の比較と横柱の軸力（STEP4 4-3）
# K081のモデル・荷重・安全率で、横柱 SF-20・20 ×3 の扱いを (a) 剛接合（軸力＋曲げ）、(b) 両端ピン（軸力のみ）、(c) なし に変え、
# 梁のねじの余裕と、各横柱の軸力（＋引張・−圧縮、安全率込み）を比べる。
# 以下はK081の前提の記載
# K079からの変更（依頼主判断・仮）：リンク面 左x=94.15・右x=165.35（K080）、CSPを左へ4.4（重心 x=135.05、依頼主判断）、リンク 鋼角パイプ25×25×2.3（仮）。
# O：架台に固定したピンに球面軸受を介してリンクを付ける（面外のモーメントを受けない、P2）。B：リニアガイド（重荷重用H24・2ブロック、K080）。
# 以下はK079の前提の記載
# 依頼主判断（A04-006・A04-007 改訂予定）：LC1 常時 W・安全率4、LC2 猫 W＋5kg×衝撃係数2（鉛直、CSP重心）・安全率2、LC3 地震 KH=1.0・KV=0.5（一般の施設・上層階・一般機器）・安全率2。
# K077と同じモデル・依頼主条件（仮）で、梁のねじ（配置L1）、Bのキャリッジのモーメント、リンクの面外の曲げ・軸力、Oの軸受けの力の必要値（安全率込み）を出す。
# 以下はK077の前提の記載
# Oは軸受け1個のピン（x軸まわりに加え、d軸・h軸まわりの回転も自由＝面外のモーメントを受けない）。Bはキャリッジ（並進3方向と d・h 軸まわりの回転を固定）。
# 依頼主の条件（仮）：O・O′は h=265、左O d=52、右O′ d=70（Δd=18）。機構とCSPは全体を d−0.73・h−3 平行移動（CSPも一緒に下げる）。
#   横柱 SF-20・20（アルミ、E=69GPa、A=190mm²・I=0.75×10⁴mm⁴：ミスミ SF-20・20・1F の値から仮）を (h=269,d=47)・(h=263,d=47)・(h=269,d=57) に3本、架台と剛接合（仮）。
#   架台：鋼板 厚8×高さ155（h=254.5〜270）、d=46〜（左165.99・右183.99）。梁のねじ 8本/片側、h=257・267.6 の2列（縁距離4d：丸鋼の例）、ks=4,500N/mm（K072）。
#   Oの下の鉄板（T=10）は入れない（P2ではOに面外のモーメントが来ないため、要否を結果で判断）。レールによる架台の補強は無視（安全側）。
# 荷重：K066と同じ立体骨組み（リンク 角パイプ40×40×3、CSP剛体）、地震 KH=2.0・KV=1.0、±x。片側ずつの架台・ねじはK073と同じ梁要素モデル（接触なし）。
# ねじの配置は3案を比べる：
#   L1：O（d±0）・B使用位置 d±5・B収納位置（d±0） の4列×2段
#   L2：B使用位置 d±5・B収納位置 d±5 の4列×2段（Oのまわりなし）
#   L3：O（d±0）・B使用位置（d±0）・B収納位置（d±0）・架台LP側の端 の4列×2段
import math, csv, subprocess, numpy as np
TS=subprocess.run(['date','+%y%m%d%H%M'],capture_output=True,text=True,env={'TZ':'Asia/Tokyo'}).stdout.strip()
src=open('/tmp/k066b.py',encoding='utf-8').read().split('rows=[]')[0]
# Oの拘束を選べるようにする
src=src.replace("def build(si,bfree):","def build(si,bfree,ofree=False):")
src=src.replace("fixed+= [6*ix[sn+'O']+c_ for c_ in (0,1,2,4,5)]","fixed+= [6*ix[sn+'O']+c_ for c_ in ((0,1,2) if ofree else (0,1,2,4,5))]")
exec(src)
MF=3.0*g; DD,DH=-0.73,-3.0
PL={'左':dict(xm=899.0,d0=460.0,d1=1659.9,sgn=+1,xl=941.5),'右':dict(xm=1696.0,d0=460.0,d1=1839.9,sgn=-1,xl=1653.5)}
HREF=2622.5; HS=[2570.0,2676.0]
PILL=[(2690.0,470.0),(2630.0,470.0),(2690.0,570.0)]
def reactions(si,hx,ofree,bfree,FV=None):
    nodes,els,ix,K,fixed=build(si,bfree,ofree); N=K.shape[0]; f=np.zeros(N)
    hC=pose(52.73,si)['C'][1]; pL,pR=nodes['左Cc'],nodes['右Cc']; Gp=np.array([135.05,61.73,hC])*10.0; Fv=FV
    tL=(pR[0]-Gp[0])/(pR[0]-pL[0]); Pline=pL+(pR-pL)*(1-tL); Mres=np.cross(Gp-Pline,Fv)
    f[6*ix['左Cc']:6*ix['左Cc']+3]+=Fv*tL; f[6*ix['右Cc']:6*ix['右Cc']+3]+=Fv*(1-tL)
    f[6*ix['左Cc']+3:6*ix['左Cc']+6]+=Mres/2; f[6*ix['右Cc']+3:6*ix['右Cc']+6]+=Mres/2
    free=[i for i in range(N) if i not in fixed]
    for i in free: K[i,i]+=1e-6
    u=np.zeros(N); u[free]=np.linalg.solve(K[np.ix_(free,free)],f[free]); R=K@u-f
    out={}; info={}
    sh=np.array([0,DD*10,DH*10])
    for sn in SIDES:
        L=[]
        for nn in ('O','B'):
            i=ix[sn+nn]; L.append((nodes[sn+nn]+sh,-R[6*i:6*i+3],-R[6*i+3:6*i+6]))
            info[(sn,nn)]=(abs(R[6*i+4])/1000,abs(R[6*i+5])/1000,float(np.linalg.norm(R[6*i:6*i+3])))
        p=PL[sn]; L.append((np.array([(p['xm']+p['xl'])/2,round((p['d0']+p['d1'])/2,1),2620.0]),FV/W*MF if FV is not None else np.zeros(3),np.zeros(3)))
        # リンクの面外の曲げの最大
        mx=0; ax=0; mi=0
        for n1,n2,typ in els:
            if typ!='link' or not n1.startswith(sn): continue
            ke,T,kl=kel(nodes[n1],nodes[n2],A_,I_,I_,J_)
            dof=list(range(6*ix[n1],6*ix[n1]+6))+list(range(6*ix[n2],6*ix[n2]+6)); fl=kl@(T@u[dof]); mx=max(mx,abs(fl[4])/1000,abs(fl[10])/1000); ax=max(ax,abs(fl[0])); mi=max(mi,abs(fl[5])/1000,abs(fl[11])/1000)
        info[(sn,'link')]=(mx,ax,mi)
        out[sn]=L
    return out,info
PMODE=['rigid']; PAX={}
def solve(loads,SCR,ks=4500.0,t=8.0,removed=None):
    E_,G_=205e3,79e3; I=155*t**3/12; J=155*t**3/3
    nd={}
    for sn in SIDES:
        p=PL[sn]; ds=set(np.round(np.linspace(p['d0'],p['d1'],int((p['d1']-p['d0'])/25)+1),1))
        ds|={d for h,d in PILL}|set(SCR[sn])|{round(float(P[1]),1) for P,_,_ in loads[sn]}
        nd[sn]=sorted(ds)
    idx={}; n=0
    for sn in SIDES:
        for d in nd[sn]: idx[(sn,d)]=n; n+=1
    K=np.zeros((3*n,3*n)); F=np.zeros(3*n)
    for sn in SIDES:
        ds=nd[sn]
        for a,b in zip(ds[:-1],ds[1:]):
            L=b-a; i,j=idx[(sn,a)],idx[(sn,b)]; c=E_*I/L**3
            kb=c*np.array([[12,-6*L,-12,-6*L],[-6*L,4*L*L,6*L,2*L*L],[-12,6*L,12,6*L],[-6*L,2*L*L,6*L,4*L*L]])
            dof=[3*i,3*i+2,3*j,3*j+2]; K[np.ix_(dof,dof)]+=kb
            dof=[3*i+1,3*j+1]; K[np.ix_(dof,dof)]+=G_*J/L*np.array([[1,-1],[-1,1]])
        for d in SCR[sn]:
            for h in HS:
                if removed==(sn,d,h): continue
                i=idx[(sn,d)]; v=np.zeros(3*n); v[3*i]=1; v[3*i+1]=h-HREF; K+=ks*np.outer(v,v)
        for P,Fo,Mo in loads[sn]:
            i=idx[(sn,round(float(P[1]),1))]; r=P-np.array([PL[sn]['xm'],P[1],HREF]); M=Mo+np.cross(r,Fo)
            F[3*i]+=Fo[0]; F[3*i+1]+=M[1]; F[3*i+2]+=M[2]
    # 横柱（アルミ SF-20・20）：軸ばね（高さのずれ込み）＋曲げ（θd・θh）
    Ea=69e3; Ap=190.0; Ip=0.75e4; Lt=PL['右']['xm']-PL['左']['xm']
    pv=[]
    for h,d in (PILL if PMODE[0]!='none' else []):
        i,j=idx[('左',d)],idx[('右',d)]; v=np.zeros(3*n); v[3*i]=1; v[3*i+1]=h-HREF; v[3*j]=-1; v[3*j+1]=-(h-HREF)
        K+=Ea*Ap/Lt*np.outer(v,v); pv.append(((h,d),v))
        if PMODE[0]=='rigid':
            for c_ in (1,2): K[np.ix_([3*i+c_,3*j+c_],[3*i+c_,3*j+c_])]+=Ea*Ip/Lt*np.array([[4,2],[2,4]])
    u=np.linalg.solve(K,F); res={}
    for key,v in pv: PAX[key]=-Ea*Ap/Lt*(v@u)   # 左右の架台が離れる向き（v@u<0）で引張＋
    for sn in SIDES:
        mx=0
        for d in SCR[sn]:
            for h in HS:
                if removed==(sn,d,h): continue
                i=idx[(sn,d)]; mx=max(mx,ks*(u[3*i]+u[3*i+1]*(h-HREF))*PL[sn]['sgn'])
        res[sn]=mx
    return res
def bpos(Od,si):
    P=pose(Od,si); return round((P['B'][0]+DD)*10,1)
Opos={'左':round((52.73+DD)*10,1),'右':round((70.73+DD)*10,1)}
Bu={sn:bpos(Od,1) for sn,(xl,Od) in SIDES.items()}; Bs={sn:bpos(Od,0) for sn,(xl,Od) in SIDES.items()}
LAY={'L1：O・B使用±5・B収納':{sn:[Opos[sn],Bu[sn]-50,Bu[sn]+50,Bs[sn]] for sn in SIDES},
     'L2：B使用±5・B収納±5':{sn:[Bu[sn]-50,Bu[sn]+50,Bs[sn]-50,Bs[sn]+50] for sn in SIDES},
     'L3：O・B使用・B収納・LP側の端':{sn:[Opos[sn],Bu[sn],Bs[sn],PL[sn]['d1']-50] for sn in SIDES}}
CAT=5*2*g
LCS=[('LC1 常時',4,[np.array([0,0,-W])]),
     ('LC2 猫',2,[np.array([0,0,-(W+CAT)])]),
     ('LC3 地震 KH=1.0・KV=0.5',2,[np.array([1.0*W,0,-1.5*W]),np.array([-1.0*W,0,-1.5*W])])]
SCR=LAY['L1：O・B使用±5・B収納']
rows=[]
for mode,lab in (('rigid','(a) 剛接合'),('pin','(b) 両端ピン（押し引きのみ）'),('none','(c) 横柱なし')):
    PMODE[0]=mode
    for lc,SF,FVs in LCS:
        for si,pos in ((1,'使用'),(0,'収納')):
            Rs=[reactions(si,1,True,False,FV) for FV in FVs]
            scr={sn:0 for sn in SIDES}; ax={k:[0,0] for k in PILL}
            for L,_ in Rs:
                solve(L,SCR)
                for k in PILL:
                    if k in PAX: ax[k][0]=max(ax[k][0],PAX[k]); ax[k][1]=min(ax[k][1],PAX[k])
                for sn in SIDES:
                    for d in SCR[sn]:
                        for h in HS:
                            scr[sn]=max(scr[sn],solve(L,SCR,removed=(sn,d,h))[sn])
            PAX.clear()
            m=min(1820/(scr[sn]*SF) for sn in SIDES)
            row=[lab,lc,SF,pos,round(m,2)]+([v for k in PILL for v in (round(ax[k][0]*SF),round(ax[k][1]*SF))] if mode!='none' else ['']*6)
            rows.append(row); print(row)
out='/mnt/user-data/outputs/%s_K082_横柱の役割と軸力.csv'%TS
with open(out,'w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f)
    w.writerow(['K082 横柱の役割：剛接合・両端ピン・なし の比較（K081の構成・荷重・安全率）'])
    w.writerow(['ねじの余裕＝ねじ長30の下限1.82kN÷必要引抜き耐力（左右の小さい方、1本抜け×安全率）。横柱の軸力は安全率込み、＋引張（左右の架台を引き寄せる向き）・−圧縮（つっかえる向き）、荷重の向き（±x）の最大と最小。'])
    w.writerow(['横柱 SF-20・20（E=69GPa、A=190mm²、I=0.75×10⁴mm⁴：ミスミ SF-20・20・1F の値から仮）。'])
    w.writerow([])
    hdr=['横柱の扱い','荷重','安全率','位置','ねじの余裕（最小）']
    for h,d in PILL: hdr+=['柱 h=%d,d=%d 最大'%(h/10,d/10),'柱 h=%d,d=%d 最小'%(h/10,d/10)]
    w.writerow(hdr); w.writerows(rows)
print(out)
