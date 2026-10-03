# K070 Oと Bのまわりにねじを集めたときのねじの力（STEP4 4-3、案(D)）
# K068と同じモデル（(0) Bは面外に固定、横材はSC側d=48のみ、右の架台もd=46まで延長：仮）で、ねじの配置を比べる。
#   K068の配置：2列（h=258・266.5）×各列3本（等間隔）＝6本/片側
#   (D1) 列の間隔だけ広げる：h=257・268、各列3本（d位置はK068と同じ）＝6本
#   (D2) Oと Bのまわりに集める：O・B使用位置・B収納位置のそれぞれ d±5 に上下2本（h=258・266.5）＝12本
#   (D3) (D2)＋列の間隔を広げる（h=257・268）＝12本
#   Bの位置は使用 左106.56・右124.56、収納 左151.98・右169.98（BはレールにのってOから2a·cosφ）。
# 以下はK068の前提の記載
# K061は「架台＋横材＝剛な枠」としてねじの力を出した。K064・K066でBからも引きはがしのモーメントが入るとわかったため、
# 架台の板のねじれ・曲げを入れて、ねじ1本の引抜き力がどこまで上がるかを確かめる。
# 前提（仮）：
#   ・リンク・CSPからの力：K066（1223版）の立体骨組みの O・B の反力（使用・収納、地震 KH=2.0・KV=1.0、±x）。(0) Bは面外に固定、(C) Bは球面軸受。
#   ・架台：鋼板 厚10（K056の厚1cm、材質は仮に鋼 E=205GPa・G=79GPa）、高さ155（h=254.5〜270）。dに沿う梁要素
#     （面外たわみ ux・d軸まわりのねじれ θd・h軸まわりの曲げ θh）。曲げ I=155×10³/12、ねじれ J=155×10³/3。面内は剛。
#   ・架台の範囲：左 d=46〜165.99（K062で延長済み）、右 d=46〜183.99（右も横材の位置まで延ばす：K062では右の架台がd=66.73からで横材に届いていなかったため、仮）。
#   ・ねじ：2列（h=258・266.5）×各列3本、d位置はK057と同じ。ねじの軸方向ばね ks（引抜き・押し込み同じ、接触は無視：K057と同じ扱い）。ks=2,000・5,000・20,000 N/mm（仮）で感度を見る。
#   ・横材：x=90.5〜169、d=46〜50（中心48）、鋼角パイプ 40（d）×60（h）×2.3（仮）。架台と剛に接合。
#   ・固定部品 3.0kg/片側（仮）の地震力を架台の中央に加える（K061と同じ）。
#   ・剛な枠の値（K061の考え方）との比較のため、板を十分硬くした場合も同じモデルで出す。
#   ・1本抜け（A04-009）は1本ずつ外した最大、必要引抜き耐力＝1本抜けの値×安全率4（A04-007）。
import math, csv, subprocess, numpy as np
TS=subprocess.run(['date','+%y%m%d%H%M'],capture_output=True,text=True,env={'TZ':'Asia/Tokyo'}).stdout.strip()
exec(open('/tmp/k066.py',encoding='utf-8').read().split('rows=[]')[0])
MF=3.0*g
PL={'左':dict(xm=900.0,d0=460.0,d1=1659.9,sgn=+1,xl=920.0),'右':dict(xm=1695.0,d0=460.0,d1=1839.9,sgn=-1,xl=1680.0)}
SCR={'左':[537.3,1073.6,1609.9],'右':[717.3,1253.6,1789.9]}
HS=[2580.0,2665.0]; HREF=2622.5; DTIE=480.0
def reactions(si,bfree,hx):
    nodes,els,ix,K,fixed=build(si,bfree); N=K.shape[0]; f=np.zeros(N)
    hC=pose(52.73,si)['C'][1]; pL,pR=nodes['左Cc'],nodes['右Cc']; Gp=np.array([139.45,61.73,hC])*10.0; Fv=np.array([hx*2.0*W,0,-2.0*W])
    tL=(pR[0]-Gp[0])/(pR[0]-pL[0]); Pline=pL+(pR-pL)*(1-tL); Mres=np.cross(Gp-Pline,Fv)
    f[6*ix['左Cc']:6*ix['左Cc']+3]+=Fv*tL; f[6*ix['右Cc']:6*ix['右Cc']+3]+=Fv*(1-tL)
    f[6*ix['左Cc']+3:6*ix['左Cc']+6]+=Mres/2; f[6*ix['右Cc']+3:6*ix['右Cc']+6]+=Mres/2
    free=[i for i in range(N) if i not in fixed]; u=np.zeros(N); u[free]=np.linalg.solve(K[np.ix_(free,free)],f[free]); R=K@u-f
    out={}
    for sn in SIDES:
        L=[]
        for nn in ('O','B'):
            i=ix[sn+nn]; L.append((nodes[sn+nn],-R[6*i:6*i+3],-R[6*i+3:6*i+6]))   # 架台が受ける力＝反力の逆
        p=PL[sn]; L.append((np.array([(p['xm']+p['xl'])/2,(p['d0']+p['d1'])/2,2620.0]),np.array([hx*2.0*MF,0,-2.0*MF]),np.zeros(3)))
        out[sn]=L
    return out
def plate_solve(loads,ks,tplate,removed=None):
    E_,G_=205e3,79e3; I=155*tplate**3/12; J=155*tplate**3/3
    # 節点：各側の架台のd位置（横材・ねじ・O・B・荷重点・端）
    nd={}
    for sn in SIDES:
        ds={PL[sn]['d0'],PL[sn]['d1'],DTIE}|set(SCR[sn])|{round(float(P[1]),3) for P,_,_ in loads[sn]}
        nd[sn]=sorted(ds)
    idx={}; n=0
    for sn in SIDES:
        for d in nd[sn]: idx[(sn,d)]=n; n+=1
    K=np.zeros((3*n,3*n)); F=np.zeros(3*n)   # dof: ux, θd, θh
    for sn in SIDES:
        ds=nd[sn]
        for a,b in zip(ds[:-1],ds[1:]):
            L=b-a; i,j=idx[(sn,a)],idx[(sn,b)]
            # 曲げ（ux, θh）：h軸まわり。θh正でdが増えるとuxが減る向き（右手系）→ θ=-dux/dd として標準要素
            c=E_*I/L**3; kb=c*np.array([[12,-6*L,-12,-6*L],[-6*L,4*L*L,6*L,2*L*L],[-12,6*L,12,6*L],[-6*L,2*L*L,6*L,4*L*L]])
            dof=[3*i,3*i+2,3*j,3*j+2]; K[np.ix_(dof,dof)]+=kb
            kt=G_*J/L; dof=[3*i+1,3*j+1]; K[np.ix_(dof,dof)]+=kt*np.array([[1,-1],[-1,1]])
        for d in SCR[sn]:
            for h in HS:
                if removed==(sn,d,h): continue
                i=idx[(sn,d)]; z=h-HREF; v=np.zeros(3*n); v[3*i]=1; v[3*i+1]=z   # ねじ位置のx変位 = ux + θd·z
                K+=ks*np.outer(v,v)
        for P,Fo,Mo in loads[sn]:
            i=idx[(sn,round(float(P[1]),3))]; r=P-np.array([PL[sn]['xm'],P[1],HREF]); M=Mo+np.cross(r,Fo)
            F[3*i]+=Fo[0]; F[3*i+1]+=M[1]; F[3*i+2]+=M[2]
    # 横材（x方向の梁、両端は架台のd=48）
    Lt=PL['右']['xm']-PL['左']['xm']; At=2*(40+60)*2.3-4*2.3**2
    Id=(40*60**3-35.4*55.4**3)/12; Ih=(60*40**3-55.4*35.4**3)/12
    i,j=idx[('左',DTIE)],idx[('右',DTIE)]
    K[np.ix_([3*i,3*j],[3*i,3*j])]+=E_*At/Lt*np.array([[1,-1],[-1,1]])
    for c_,II in ((1,Id),(2,Ih)):
        K[np.ix_([3*i+c_,3*j+c_],[3*i+c_,3*j+c_])]+=E_*II/Lt*np.array([[4,2],[2,4]])
    u=np.linalg.solve(K,F)
    res={}
    for sn in SIDES:
        mx=0
        for d in SCR[sn]:
            for h in HS:
                if removed==(sn,d,h): continue
                i=idx[(sn,d)]; dx=u[3*i]+u[3*i+1]*(h-HREF)
                pull=ks*dx*PL[sn]['sgn']   # 梁から離れる向きの変位×ばね＝引抜き
                mx=max(mx,pull)
        res[sn]=mx
    return res
rows=[]
def around(c): return [round((c-5)*10,1),round((c+5)*10,1)]
LAYOUT={
 'K068の配置（6本）':({'左':[537.3,1073.6,1609.9],'右':[717.3,1253.6,1789.9]},[2580.0,2665.0]),
 '(D1) 列の間隔を広げる（6本）':({'左':[537.3,1073.6,1609.9],'右':[717.3,1253.6,1789.9]},[2570.0,2680.0]),
 '(D2) O・Bのまわりに集める（12本）':({'左':around(52.73)+around(106.56)+around(151.98),'右':around(70.73)+around(124.56)+around(169.98)},[2580.0,2665.0]),
 '(D3) 集める＋列の間隔を広げる（12本）':({'左':around(52.73)+around(106.56)+around(151.98),'右':around(70.73)+around(124.56)+around(169.98)},[2570.0,2680.0]),
}
for si,pos in ((1,'使用'),(0,'収納')):
    Ls=[reactions(si,False,hx) for hx in (1,-1)]
    for lay,(scr,hs) in LAYOUT.items():
        SCR.clear(); SCR.update(scr); HS[:]=hs
        for model,tp,ks in (('板 厚10・ks=2,000',10.0,2000.0),('板 厚10・ks=5,000',10.0,5000.0),('板 厚10・ks=20,000',10.0,20000.0)):
            best={sn:[0,0] for sn in SIDES}
            for L in Ls:
                r0=plate_solve(L,ks,tp)
                for sn in SIDES: best[sn][0]=max(best[sn][0],r0[sn])
                for sn in SIDES:
                    for d in SCR[sn]:
                        for h in HS:
                            r1=plate_solve(L,ks,tp,(sn,d,h))
                            for s2 in SIDES: best[s2][1]=max(best[s2][1],r1[s2])
            for sn in SIDES:
                rows.append([pos,lay,model,sn,round(best[sn][0]),round(best[sn][1]),round(best[sn][1]*4)]); print(rows[-1])
out='/mnt/user-data/outputs/%s_K070_OとBのまわりにねじを集めたときの力.csv'%TS
with open(out,'w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f)
    w.writerow(['K070 Oと Bのまわりにねじを集めたときの梁のねじの引抜き力（ねじ1本あたり、N、地震 KH=2.0・KV=1.0、±xの大きい方、(0) Bは面外に固定）'])
    w.writerow(['K068と同じモデル（鋼板厚10×高さ155、横材 角パイプ40×60×2.3をSC側d=48、右の架台もd=46まで延長、すべて仮）。(D2)(D3)はO・B使用位置・B収納位置の d±5 に上下2本ずつ。'])
    w.writerow(['必要引抜き耐力＝1本抜け×安全率4。K063の製品の見込み：引抜き 下限1.82kN（ねじ長30）〜3.63kN（ねじ長45）。ねじの端あき・間隔の規定は未確認'])
    w.writerow([])
    w.writerow(['位置','ねじの配置','架台のモデル','側','引抜き','引抜き(1本抜け)','必要引抜き耐力'])
    w.writerows(rows)
print(out)
