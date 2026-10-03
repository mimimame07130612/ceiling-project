# K083 P2の形での片側故障の照合（横柱あり・なし）（STEP4 4-3、D04-003、K059・K060の考え方）
# 構成（仮）：K081と同じ（O 固定ピン＋球面軸受・Bリニアガイド重荷重用H24・2ブロック、リンク面 左94.15・右165.35、CSP重心 x=135.05、リンク角パイプ25×25×2.3、
#   架台 鋼板厚8、梁のねじ8本/片側 配置L1、ks=4,500、横柱 SF-20・20×3）。地震は重ねない（依頼主判断）。1本抜けは重ねる（依頼主判断）。
# 故障ケース（K059・K060）：残った側の機構だけで考える（壊れた側の機構は荷重を持たない）。
#   (c) 全荷重が残った側へ移り、CSPは残った側のCまわりに回ってぶら下がる。最下点の力＝動的係数2.13×荷重（K060）。作用点：x＝CSP重心135.05、d＝残った側のC、h＝C−9（ぶら下がり）。
#   (a) O・OA・Aの破断：残った側は健全時の分担（左右のてこ比、CSP重心 x=135.05）＋壊れた側のロッドがCをd方向に押す力（K059：LC1で収納615N・使用48N、荷重に比例）。
# 荷重：LC1 W、LC2 W＋猫5kg×2。判定（依頼主判断の基準）：揺れの係数を入れた荷重が製品の公表値以内（安全率1）。
#   ねじ：引抜きの下限1.82kN（若井産業カタログ、短期許容耐力の公表値がないため最大荷重の下限で代える）。リニアガイド：静的許容モーメントMC=196・MA=184.5N·m（ミスミ、2ブロック密着の参考値）。
#   リンク：角パイプ25×25×2.3の曲げ応力（2方向の曲げを同じ点で足す安全側）と降伏点245MPa（一般的な構造用角形鋼管の値、仮）。
# 横柱：あり（壊れた側の架台は梁に付いたまま、横柱で力を分ける）／なし。
import math, csv, subprocess, numpy as np
TS=subprocess.run(['date','+%y%m%d%H%M'],capture_output=True,text=True,env={'TZ':'Asia/Tokyo'}).stdout.strip()
src=open('/tmp/k082.py',encoding='utf-8').read()
pass
exec(src.split("CAT=5*2*g")[0])
# solve() の横柱の扱いを PMODE で切り替える（K082と同じ置き換え）
import inspect
CAT=5*2*g; FDYN=2.13; HF={'収納':615.0,'使用':48.0}
def side_model(sn,si,Fc,Mc):
    """残った側だけの立体骨組み。C点に力Fc・モーメントMc（N, N·mm）。O：並進固定（回転自由＝球面軸受）、B：並進とd・h軸まわり回転を固定。"""
    xl,Od=SIDES[sn]; P=pose(Od,si); X=lambda q:np.array([xl,q[0],q[1]])*10.0
    nodes={'O':X(P['O']),'B':X(P['B']),'OAO':X(P['O']),'OAA':X(P['A']),'ABA':X(P['A']),'ABB':X(P['B']),'ACA':X(P['A']),'ACC':X(P['C'])}
    names=list(nodes); ix={n:i for i,n in enumerate(names)}; N=6*len(names); K=np.zeros((N,N))
    out={}
    for n1,n2 in (('OAO','OAA'),('ABA','ABB'),('ACA','ACC')):
        ke,_,_=kel(nodes[n1],nodes[n2],A_,I_,I_,J_); dof=list(range(6*ix[n1],6*ix[n1]+6))+list(range(6*ix[n2],6*ix[n2]+6)); K[np.ix_(dof,dof)]+=ke
    kp=1e9
    def tie(n1,n2,cs):
        for c_ in cs:
            i,j=6*ix[n1]+c_,6*ix[n2]+c_; K[i,i]+=kp; K[j,j]+=kp; K[i,j]-=kp; K[j,i]-=kp
    tie('O','OAO',(0,1,2,4,5)); tie('OAA','ABA',(0,1,2,4,5)); tie('ABA','ACA',range(6)); tie('B','ABB',(0,1,2,4,5))
    fixed=[6*ix['O']+c for c in (0,1,2)]+[6*ix['B']+c for c in (0,1,2,4,5)]
    for nn in ('O','B'): K[6*ix[nn]+3,6*ix[nn]+3]+=1e-3
    for c in (3,4,5): K[6*ix['O']+c,6*ix['O']+c]+=1e-6
    f=np.zeros(N); f[6*ix['ACC']:6*ix['ACC']+3]=Fc; f[6*ix['ACC']+3:6*ix['ACC']+6]=Mc
    free=[i for i in range(N) if i not in fixed]
    for i in free: K[i,i]+=1e-6
    u=np.zeros(N); u[free]=np.linalg.solve(K[np.ix_(free,free)],f[free]); R=K@u-f
    sh=np.array([0,DD*10,DH*10])
    loads=[(nodes['O']+sh,-R[6*ix['O']:6*ix['O']+3],-R[6*ix['O']+3:6*ix['O']+6]),(nodes['B']+sh,-R[6*ix['B']:6*ix['B']+3],-R[6*ix['B']+3:6*ix['B']+6])]
    mo=mi=0; ax=0
    for n1,n2 in (('OAO','OAA'),('ABA','ABB'),('ACA','ACC')):
        ke,T,kl=kel(nodes[n1],nodes[n2],A_,I_,I_,J_); dof=list(range(6*ix[n1],6*ix[n1]+6))+list(range(6*ix[n2],6*ix[n2]+6)); fl=kl@(T@u[dof])
        # 面外・面内の曲げ（同じ断面で両端の大きい方）を足す
        for e in (0,6): 
            mo=max(mo,abs(fl[e+4])/1000+abs(fl[e+5])/1000); 
        ax=max(ax,abs(fl[0]))
    MB=R[6*ix['B']+3:6*ix['B']+6]/1000
    return loads,abs(MB[1]),abs(MB[2]),mo,ax
b_,t_=25,2.3; Ab=b_*b_-(b_-2*t_)**2; Zb=(b_**4-(b_-2*t_)**4)/(6*b_)
SCR=LAY['L1：O・B使用±5・B収納']
rows=[]
for sn in SIDES:   # sn＝残った側
    xl,Od=SIDES[sn]; other=[s for s in SIDES if s!=sn][0]
    share_={'左':(165.35-135.05)/(165.35-94.15),'右':(135.05-94.15)/(165.35-94.15)}
    for si,pos in ((0,'収納'),(1,'使用')):
        hC=pose(Od,si)['C'][1]
        for lc in ('LC1','LC2'):
            Wl=W+(CAT if lc=='LC2' else 0)
            cases=[]
            F=np.array([0,0,-FDYN*Wl]); r=np.array([(135.05-xl)*10,0,-90.0]); cases.append(('(c) 全荷重が移りぶら下がる（動的係数2.13）',F,np.cross(r,F)))
            for sgn in (1,-1):
                F=np.array([0,sgn*HF[pos]*Wl/W,-share_[sn]*Wl]); cases.append(('(a) O・OA・Aの破断（押す向き%s）'%('+d' if sgn>0 else '−d'),F,np.zeros(3)))
            for cname,F,M in cases:
                loads,MBd,MBh,mo,ax=side_model(sn,si,F,M)
                L={sn:loads,other:[]}
                L[sn].append((np.array([(PL[sn]['xm']+PL[sn]['xl'])/2,round((PL[sn]['d0']+PL[sn]['d1'])/2,1),2620.0]),np.array([0,0,-MF]),np.zeros(3)))
                for pm,plab in (('rigid','横柱あり'),('none','横柱なし')):
                    PMODE[0]=pm
                    v=0
                    for d in SCR[sn]:
                        for h in HS:
                            v=max(v,solve(L,SCR,removed=(sn,d,h))[sn])
                    stress=mo*1e3/Zb+ax/Ab
                    rows.append([sn,pos,lc,cname,plab,round(v),round(1820/v,2) if v>0 else '',round(MBd,1),round(196/MBd,2) if MBd>0 else '',round(MBh,1),round(mo,1),round(stress),round(245/stress,2)])
                    print(rows[-1])
out='/mnt/user-data/outputs/%s_K083_P2の形での片側故障の照合.csv'%TS
with open(out,'w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f)
    w.writerow(['K083 P2の形での片側故障の照合（残った側、横柱あり・なし、安全率1：揺れの係数を入れた荷重と製品の公表値の比較）'])
    w.writerow(['構成はK081と同じ（仮）。ねじ：1本抜けの引抜き、余裕＝1.82kN÷引抜き。リニアガイド：余裕＝MC 196N·m÷B：Md。リンク：応力＝(面外＋面内の曲げ)/Z＋軸力/A（角パイプ25×25×2.3）、余裕＝245MPa÷応力。'])
    w.writerow(['(c)の作用点：x＝CSP重心135.05、d＝残った側のC、h＝C−9。(a)の押す力：K059（LC1で収納615N・使用48N）を荷重に比例。地震は重ねない。'])
    w.writerow([])
    w.writerow(['残った側','位置','荷重','故障','横柱','ねじの引抜き(1本抜け) N','ねじの余裕','B：Md N·m','ガイドの余裕(MC)','B：Mh N·m','リンクの曲げ 最大 N·m','リンクの応力 MPa','リンクの余裕'])
    w.writerows(rows)
print(out)
