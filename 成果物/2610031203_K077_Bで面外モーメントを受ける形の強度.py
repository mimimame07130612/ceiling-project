# K077 (P2) 面外のモーメントをBのキャリッジで受ける形の強度（STEP4 4-3）
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
src=open('/tmp/k066.py',encoding='utf-8').read().split('rows=[]')[0]
# Oの拘束を選べるようにする
src=src.replace("def build(si,bfree):","def build(si,bfree,ofree=False):")
src=src.replace("fixed+= [6*ix[sn+'O']+c_ for c_ in (0,1,2,4,5)]","fixed+= [6*ix[sn+'O']+c_ for c_ in ((0,1,2) if ofree else (0,1,2,4,5))]")
exec(src)
MF=3.0*g; DD,DH=-0.73,-3.0
PL={'左':dict(xm=899.0,d0=460.0,d1=1659.9,sgn=+1,xl=920.0),'右':dict(xm=1696.0,d0=460.0,d1=1839.9,sgn=-1,xl=1680.0)}
HREF=2622.5; HS=[2570.0,2676.0]
PILL=[(2690.0,470.0),(2630.0,470.0),(2690.0,570.0)]
def reactions(si,hx,ofree,bfree):
    nodes,els,ix,K,fixed=build(si,bfree,ofree); N=K.shape[0]; f=np.zeros(N)
    hC=pose(52.73,si)['C'][1]; pL,pR=nodes['左Cc'],nodes['右Cc']; Gp=np.array([139.45,61.73,hC])*10.0; Fv=np.array([hx*2.0*W,0,-2.0*W])
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
            info[(sn,nn)]=(abs(R[6*i+4])/1000,abs(R[6*i+5])/1000,abs(R[6*i]))
        p=PL[sn]; L.append((np.array([(p['xm']+p['xl'])/2,round((p['d0']+p['d1'])/2,1),2620.0]),np.array([hx*2.0*MF,0,-2.0*MF]),np.zeros(3)))
        # リンクの面外の曲げの最大
        mx=0
        for n1,n2,typ in els:
            if typ!='link' or not n1.startswith(sn): continue
            ke,T,kl=kel(nodes[n1],nodes[n2],A_,I_,I_,J_)
            dof=list(range(6*ix[n1],6*ix[n1]+6))+list(range(6*ix[n2],6*ix[n2]+6)); fl=kl@(T@u[dof]); mx=max(mx,abs(fl[4])/1000,abs(fl[10])/1000)
        info[(sn,'link')]=mx
        out[sn]=L
    return out,info
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
    for h,d in PILL:
        i,j=idx[('左',d)],idx[('右',d)]; v=np.zeros(3*n); v[3*i]=1; v[3*i+1]=h-HREF; v[3*j]=-1; v[3*j+1]=-(h-HREF)
        K+=Ea*Ap/Lt*np.outer(v,v)
        for c_ in (1,2): K[np.ix_([3*i+c_,3*j+c_],[3*i+c_,3*j+c_])]+=Ea*Ip/Lt*np.array([[4,2],[2,4]])
    u=np.linalg.solve(K,F); res={}
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
rows=[]; info_rows=[]
for si,pos in ((1,'使用'),(0,'収納')):
    R2=[reactions(si,hx,True,False) for hx in (1,-1)]
    R0=[reactions(si,hx,False,False) for hx in (1,-1)]
    for sn in SIDES:
        info_rows.append([pos,sn,'(P2) Oはピン・Bで受ける',round(max(r[1][(sn,'O')][0] for r in R2),1),round(max(r[1][(sn,'B')][0] for r in R2),1),round(max(r[1][(sn,'B')][1] for r in R2),1),round(max(r[1][(sn,'link')] for r in R2),1)])
        info_rows.append([pos,sn,'参考 (0) O・Bとも面外に固定',round(max(r[1][(sn,'O')][0] for r in R0),1),round(max(r[1][(sn,'B')][0] for r in R0),1),round(max(r[1][(sn,'B')][1] for r in R0),1),round(max(r[1][(sn,'link')] for r in R0),1)])
    for lay,SCR in LAY.items():
        best={sn:[0,0] for sn in SIDES}
        for L,_ in R2:
            r0=solve(L,SCR)
            for sn in SIDES: best[sn][0]=max(best[sn][0],r0[sn])
            for sn in SIDES:
                for d in SCR[sn]:
                    for h in HS:
                        r1=solve(L,SCR,removed=(sn,d,h))
                        for s2 in SIDES: best[s2][1]=max(best[s2][1],r1[s2])
        for sn in SIDES:
            req=best[sn][1]*4
            rows.append([pos,lay,sn,' / '.join('%.1f'%(x/10) for x in SCR[sn]),round(best[sn][0]),round(best[sn][1]),round(req),round(1820/req,2)]); print(rows[-1])
for r in info_rows: print(r)
out='/mnt/user-data/outputs/%s_K077_Bで面外モーメントを受ける形の強度.csv'%TS
with open(out,'w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f)
    w.writerow(['K077 (P2) Oはピン・面外のモーメントはBのキャリッジで受ける形の強度（地震 KH=2.0・KV=1.0、±xの大きい方）'])
    w.writerow(['依頼主条件（仮）：O・O′ h=265、左O d=52・右O′ d=70、機構とCSPは d−0.73・h−3 平行移動。横柱 SF-20・20 ×3（h=269・d=47、h=263・d=47、h=269・d=57）。架台 鋼板厚8、梁のねじ8本/片側（h=257・267.6）、ks=4,500。鉄板T=10なし。'])
    w.writerow(['必要引抜き耐力＝1本抜け×安全率4。余裕＝ねじ長30の下限1.82kN（若井産業カタログ DXP6--0）÷必要引抜き耐力。'])
    w.writerow([])
    w.writerow(['■ O・Bが受けるモーメントとリンクの面外の曲げ（片側、N·m、安全率前）'])
    w.writerow(['位置','側','継手','O：Md','B：Md','B：Mh','リンクの面外の曲げ 最大'])
    w.writerows(info_rows)
    w.writerow([])
    w.writerow(['■ 梁のねじの引抜き力（ねじ1本あたり、N）'])
    w.writerow(['位置','ねじの配置','側','ねじの列のd位置','引抜き','引抜き(1本抜け)','必要引抜き耐力','余裕（1.82kN÷必要）'])
    w.writerows(rows)
print(out)
