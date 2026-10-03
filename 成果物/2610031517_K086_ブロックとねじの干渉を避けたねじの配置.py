# K086 HSR20C（幅63）とねじの干渉を避けたねじの配置（STEP4 4-3）—— 単独で動くスクリプト（中間スクリプトに依存しない）
# 前提（仮）：K085と同じ構成（Bは THK HSR20C 1ブロック・高さ30・幅63、リンク面 左94.75・右164.75、CSP重心x=134.45、O・O′ h=265（d−0.73・h−3 平行移動）、
#   Oは固定ピン＋球面軸受（面外のモーメントを受けない）、リンク 鋼角パイプ25×25×2.3、架台 鋼板厚8・高さ155、横柱なし、梁のねじ8本/片側・ks=4,500N/mm）。
# HSR20Cのブロック（幅63）はB（h=265）を中心に h=261.85〜268.15 を占め、架台面から4mmしか浮かないため、ブロックが動く範囲
#   （左 d=102.1〜155.0、右 d=120.1〜173.0：B使用〜収納＋ブロック長74の半分）では上の列（h=267.6）にねじを置かない（依頼主判断：案1）。
# ねじの配置（8本/片側）：M1・M2・M3（下記）。荷重：常時LC1×4、猫LC2×2、地震LC3（KH=1.0・KV=0.5）×2、片側故障(c) LC1×1（動的係数2.13）。
# 判定：1本抜け（依頼主判断で重ねる）、余裕＝ねじ長30の引抜き下限1.82kN（若井産業カタログ DXP6--0）÷必要引抜き耐力。
# 立体骨組みの部分はK066（2610021223版）と同じ式（リンク面・CSP重心・リンク断面をK085の値に置き換え）。
# K066 ポータル効果を入れたリンクと架台のモーメント（STEP4 4-3、案(C)の判断材料）
# 左右の機構（OA・AB・AC）とCSP（保持具込み、剛体）を1つの立体骨組みとして解き、地震の左右揺れ（使用位置・収納位置）で
# リンクの曲げ・ねじりと、O・Bから架台に入るモーメントを求める。K065（片側ずつ独立、C点に横力）との比較。
# 前提（仮）：
#   ・計算はmm・N（座標はcmで与えて内部でmmに直す）。座標 x（左右）, d（奥行）, h（高さ）。左 O/C d=52.73・リンク面x=92.0、右 O′/C′ d=70.73・x=168.0（K056）。
#   ・リンクは鋼の角パイプ40×40×3（E=205GPa、G=79GPa）。断面は仮で、結果のモーメントの分かれ方に使う。
#   ・ピン O・A・B・C はx軸まわりの回転だけ自由、それ以外は剛に接合。長リンク（B–A–C）は1本の棒で、Aのピンは短リンクOAとの間。
#   ・リンクの曲げは面外（x方向にたわむ）と面内に分けて出す。
#   ・O：並進3方向と y・z回転を固定（軸受け）。B：並進3方向を固定（レール・ねじ・キャリッジ）、(0)では y・z回転も固定、(C)では自由（球面軸受）。
#   ・CSP：CとC′を結ぶ剛な棒。荷重はCSP重心（x=139.45、d=61.73、h＝C点の高さ）に、水平 KH·W（±x）と鉛直 −(1+KV)·W、KH=2.0・KV=1.0（A04-006）。
import math, csv, subprocess, numpy as np
TS=subprocess.run(['date','+%y%m%d%H%M'],capture_output=True,text=True,env={'TZ':'Asia/Tokyo'}).stdout.strip()
g=9.81; W=(7.90+7.4)*g; a=50.0; CS=255.885; ST=72.16; t0=268-CS
E=205e3; G=79e3   # N/mm2
def tube(b,t):
    bi=b-2*t; A=b*b-bi*bi; I=(b**4-bi**4)/12; J=2*t*(b-t)**4/(2*(b-t))*1.0  # 閉断面の近似 J=4Am²t/周長
    Am=(b-t)**2; J=4*Am*Am*t/(4*(b-t)); return A,I,J
A_,I_,J_=tube(25,2.3)
SIDES={'左':(94.75,52.73),'右':(164.75,70.73)}
def pose(Od,s):
    oc=t0+ST*s; C=(Od,268-oc); ph=math.asin(oc/(2*a)); B=(Od+2*a*math.cos(ph),268.0); A=((B[0]+C[0])/2,(B[1]+C[1])/2)
    return dict(O=(Od,268.0),A=A,B=B,C=C)
def kel(p1,p2,A,Iy,Iz,J):
    p1=np.array(p1,float); p2=np.array(p2,float); L=np.linalg.norm(p2-p1); ex=(p2-p1)/L
    ref=np.array([1.0,0,0]) if abs(ex[0])<0.9 else np.array([0,0,1.0])
    ey=np.cross(ref,ex); ey/=np.linalg.norm(ey); ez=np.cross(ex,ey)
    R=np.array([ex,ey,ez]); T=np.zeros((12,12))
    for i in range(4): T[3*i:3*i+3,3*i:3*i+3]=R
    k=np.zeros((12,12)); EA=E*A/L; GJ=G*J/L
    k[0,0]=k[6,6]=EA; k[0,6]=k[6,0]=-EA; k[3,3]=k[9,9]=GJ; k[3,9]=k[9,3]=-GJ
    for (v,th,I,sg) in ((1,5,Iz,1),(2,4,Iy,-1)):
        c=E*I/L**3; idx=[v,th,v+6,th+6]
        m=c*np.array([[12,sg*6*L,-12,sg*6*L],[sg*6*L,4*L*L,-sg*6*L,2*L*L],[-12,-sg*6*L,12,-sg*6*L],[sg*6*L,2*L*L,-sg*6*L,4*L*L]])
        k[np.ix_(idx,idx)]+=m
    return T.T@k@T, T, k
def build(si,bfree):
    nodes={}; els=[]; links=[]; rigid=[]   # links: (n1,n2) 5自由度を結ぶ（x回転は自由）
    def add(name,p): nodes[name]=np.array(p,float)*10.0   # cm→mm（E・断面がmm単位のため）
    for sn,(xl,Od) in SIDES.items():
        P=pose(Od,si); X=lambda q:(xl,q[0],q[1])
        add(sn+'O',X(P['O'])); add(sn+'B',X(P['B']))
        for m in ('OA','AB','AC'):
            for e in m: add(sn+m+e,X(P[e]))
            els.append((sn+m+m[0],sn+m+m[1],'link'))
        add(sn+'Cc',X(P['C']))   # CSP側のC
        # ピン：O（支点）↔OAのO端、A：OA・AB・ACのA端どうし、B：ABのB端↔支点B、C：ACのC端↔CSP側C
        links+= [(sn+'O',sn+'OAO'),(sn+'OAA',sn+'ABA'),(sn+'B',sn+'ABB'),(sn+'ACC',sn+'Cc')]; rigid.append((sn+'ABA',sn+'ACA'))
    els.append(('左Cc','右Cc','csp'))
    names=list(nodes); ix={n:i for i,n in enumerate(names)}; N=6*len(names); K=np.zeros((N,N))
    for n1,n2,typ in els:
        if typ=='link': ke,_,_=kel(nodes[n1],nodes[n2],A_,I_,I_,J_)
        else: ke,_,_=kel(nodes[n1],nodes[n2],1e6,1e10,1e10,1e10)
        dof=list(range(6*ix[n1],6*ix[n1]+6))+list(range(6*ix[n2],6*ix[n2]+6)); K[np.ix_(dof,dof)]+=ke
    kp=1e9
    for n1,n2 in links:
        for c_ in (0,1,2,4,5):
            i,j=6*ix[n1]+c_,6*ix[n2]+c_; K[i,i]+=kp; K[j,j]+=kp; K[i,j]-=kp; K[j,i]-=kp
    for n1,n2 in rigid:
        for c_ in range(6):
            i,j=6*ix[n1]+c_,6*ix[n2]+c_; K[i,i]+=kp; K[j,j]+=kp; K[i,j]-=kp; K[j,i]-=kp
    fixed=[]
    for sn in SIDES:
        fixed+= [6*ix[sn+'O']+c_ for c_ in (0,1,2,4,5)]
        fixed+= [6*ix[sn+'B']+c_ for c_ in ((0,1,2) if bfree else (0,1,2,4,5))]
    # x回転の特異を防ぐため支点のx回転に弱いばね
    for sn in SIDES:
        for nn in (sn+'O',sn+'B'): K[6*ix[nn]+3,6*ix[nn]+3]+=1e-3
    return nodes,els,ix,K,fixed
# ===== ここから K086 本体 =====
MF=3.0*g; DD,DH=-0.73,-3.0; CAT=5*2*g; FDYN=2.13
PL={'左':dict(xm=899.0,d0=460.0,d1=1659.9,sgn=+1,xl=947.5),'右':dict(xm=1696.0,d0=460.0,d1=1839.9,sgn=-1,xl=1647.5)}
HREF=2622.5; HLO,HUP=2570.0,2676.0
def build2(si,ofree=True):
    nodes,els,ix,K,fixed=build(si,False)
    if ofree:
        for sn in SIDES:
            for c_ in (4,5):
                k=6*ix[sn+'O']+c_
                if k in fixed: fixed.remove(k)
    return nodes,els,ix,K,fixed
def reactions(si,FV):
    nodes,els,ix,K,fixed=build2(si); N=K.shape[0]; f=np.zeros(N)
    hC=pose(52.73,si)['C'][1]; pL,pR=nodes['左Cc'],nodes['右Cc']; Gp=np.array([134.45,61.73,hC])*10.0
    tL=(pR[0]-Gp[0])/(pR[0]-pL[0]); Pline=pL+(pR-pL)*(1-tL); Mres=np.cross(Gp-Pline,FV)
    f[6*ix['左Cc']:6*ix['左Cc']+3]+=FV*tL; f[6*ix['右Cc']:6*ix['右Cc']+3]+=FV*(1-tL)
    f[6*ix['左Cc']+3:6*ix['左Cc']+6]+=Mres/2; f[6*ix['右Cc']+3:6*ix['右Cc']+6]+=Mres/2
    free=[i for i in range(N) if i not in fixed]
    for i in free: K[i,i]+=1e-6
    u=np.zeros(N); u[free]=np.linalg.solve(K[np.ix_(free,free)],f[free]); R=K@u-f
    sh=np.array([0,DD*10,DH*10]); out={}
    for sn in SIDES:
        L=[(nodes[sn+nn]+sh,-R[6*ix[sn+nn]:6*ix[sn+nn]+3],-R[6*ix[sn+nn]+3:6*ix[sn+nn]+6]) for nn in ('O','B')]
        p=PL[sn]; L.append((np.array([(p['xm']+p['xl'])/2,round((p['d0']+p['d1'])/2,1),2620.0]),FV/W*MF,np.zeros(3)))
        out[sn]=L
    return out
def side_model(sn,si,Fc,Mc):
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
    f=np.zeros(N); f[6*ix['ACC']:6*ix['ACC']+3]=Fc; f[6*ix['ACC']+3:6*ix['ACC']+6]=Mc
    free=[i for i in range(N) if i not in fixed]
    for i in free: K[i,i]+=1e-6
    u=np.zeros(N); u[free]=np.linalg.solve(K[np.ix_(free,free)],f[free]); R=K@u-f
    sh=np.array([0,DD*10,DH*10])
    return [(nodes['O']+sh,-R[6*ix['O']:6*ix['O']+3],-R[6*ix['O']+3:6*ix['O']+6]),(nodes['B']+sh,-R[6*ix['B']:6*ix['B']+3],-R[6*ix['B']+3:6*ix['B']+6])]
def solve(loads,SCR,ks=4500.0,t=8.0,removed=None):
    """架台（鋼板、dに沿う梁要素：面外たわみ・ねじれ・曲げ）＋梁のねじ（位置(d,h)ごとのばね）。返り値：側ごとのねじ引抜きの最大"""
    E_,G_=205e3,79e3; I=155*t**3/12; J=155*t**3/3
    nd={}
    for sn in SIDES:
        p=PL[sn]; ds=set(np.round(np.linspace(p['d0'],p['d1'],int((p['d1']-p['d0'])/25)+1),1))
        ds|={d for d,h in SCR.get(sn,[])}|{round(float(P[1]),1) for P,_,_ in loads.get(sn,[])}
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
        for d,h in SCR[sn]:
            if removed==(sn,d,h): continue
            i=idx[(sn,d)]; v=np.zeros(3*n); v[3*i]=1; v[3*i+1]=h-HREF; K+=ks*np.outer(v,v)
        for P,Fo,Mo in loads.get(sn,[]):
            i=idx[(sn,round(float(P[1]),1))]; r=P-np.array([PL[sn]['xm'],P[1],HREF]); M=Mo+np.cross(r,Fo)
            F[3*i]+=Fo[0]; F[3*i+1]+=M[1]; F[3*i+2]+=M[2]
    for i in range(3*n): K[i,i]+=1e-9
    u=np.linalg.solve(K,F); res={}
    for sn in SIDES:
        mx=0
        for d,h in SCR[sn]:
            if removed==(sn,d,h): continue
            i=idx[(sn,d)]; mx=max(mx,ks*(u[3*i]+u[3*i+1]*(h-HREF))*PL[sn]['sgn'])
        res[sn]=mx
    return res
def worst(L,SCR,sn):
    return max(solve(L,SCR,removed=(sn,d,h))[sn] for d,h in SCR[sn])
Opos={'左':52.0,'右':70.0}; Bu={'左':105.83,'右':123.83}; Bs={'左':151.25,'右':169.25}
ZONE={'左':(102.13,154.95),'右':(120.13,172.95)}
def mk(sn,lay):
    o,bu,bs=Opos[sn],Bu[sn],Bs[sn]; z0,z1=ZONE[sn]
    if lay=='M1': L=[(o-5,'U'),(o-5,'L'),(o+5,'U'),(o+5,'L'),(bu-5,'L'),(bu+5,'L'),(bs-5,'L'),(bs+5,'L')]
    if lay=='M2': L=[(o,'U'),(o,'L'),(z0-1.5,'U'),(z1+1.5,'U'),(bu-5,'L'),(bu+5,'L'),(bs-5,'L'),(bs+5,'L')]
    if lay=='M3': L=[(o-5,'L'),(o+5,'L'),(bu-5,'L'),(bu+5,'L'),((bu+bs)/2,'L'),(bs-5,'L'),(bs+5,'L'),(bs+10,'L')]
    out=[]
    for d,r in L:
        h=HUP if r=='U' else HLO
        if r=='U': assert not (z0-0.6<d<z1+0.6), (sn,lay,d)
        out.append((round(d*10,1),h))
    return out
LAYS={'M1：O±5に上下＋B前後に下の列':'M1','M2：Oに上下＋動く範囲の外に上の列＋B前後に下の列':'M2','M3：すべて下の列':'M3'}
rows=[]
for lab,key in LAYS.items():
    SCR={sn:mk(sn,key) for sn in SIDES}
    for lc,SF,FVs in (('LC1 常時',4,[np.array([0,0,-W])]),('LC2 猫',2,[np.array([0,0,-(W+CAT)])]),('LC3 地震 KH=1.0',2,[np.array([1.0*W,0,-1.5*W]),np.array([-1.0*W,0,-1.5*W])])):
        for si,pos in ((1,'使用'),(0,'収納')):
            Rs=[reactions(si,FV) for FV in FVs]
            for sn in SIDES:
                v=max(worst(L,SCR,sn) for L in Rs)
                rows.append([lab,'健全',lc,SF,pos,sn,round(v),round(v*SF),round(1820/(v*SF),2)])
    for sn in SIDES:
        xl,Od=SIDES[sn]; other=[s for s in SIDES if s!=sn][0]
        for si,pos in ((0,'収納'),(1,'使用')):
            F=np.array([0,0,-FDYN*W]); r=np.array([(134.45-xl)*10,0,-90.0])
            loads=side_model(sn,si,F,np.cross(r,F)); p=PL[sn]
            loads.append((np.array([(p['xm']+p['xl'])/2,round((p['d0']+p['d1'])/2,1),2620.0]),np.array([0,0,-MF]),np.zeros(3)))
            v=worst({sn:loads,other:[]},SCR,sn)
            rows.append([lab,'片側故障(c)・残った側','LC1',1,pos,sn,round(v),round(v),round(1820/v,2)])
    print(lab,'最小の余裕',min(r[-1] for r in rows if r[0]==lab))
out='/mnt/user-data/outputs/%s_K086_ブロックとねじの干渉を避けたねじの配置.csv'%TS
with open(out,'w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f)
    w.writerow(['K086 HSR20C（幅63）とねじの干渉を避けたねじの配置（8本/片側、ブロックが動く範囲は下の列 h=257 だけ）'])
    w.writerow(['ねじの位置（d, cm）：O 左52.0・右70.0、B使用 左105.83・右123.83、B収納 左151.25・右169.25、ブロックが動く範囲 左102.1〜155.0・右120.1〜173.0。上の列 h=267.6、下の列 h=257。'])
    w.writerow(['余裕＝1.82kN÷（1本抜けの引抜き×安全率）。架台 鋼板厚8、ks=4,500N/mm、横柱なし（すべて仮）。'])
    for sn in SIDES:
        for lab,key in LAYS.items(): w.writerow(['ねじの位置 %s %s'%(sn,key)]+['d=%.1f h=%.1f'%(d/10,h/10) for d,h in mk(sn,key)])
    w.writerow([])
    w.writerow(['ねじの配置','状態','荷重','安全率','位置','側','引抜き(1本抜け) N','必要引抜き耐力 N','余裕'])
    w.writerows(rows)
print(out)
