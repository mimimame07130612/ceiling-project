# K065 Bの継手を球面軸受にしたときの力の入り方（STEP4 4-3、架台と横材の形：案(C)）
# K064の骨組み（リンクOA・AB・AC、面外）で、Bの継手を球面軸受（ロッドエンドなど）に変え、Bでは面外の力（x方向）だけを受け、
# モーメント（Md・Mh）は受けないとした場合の、O・Bから架台に入る力と、リンクの各部材の面外の曲げ・ねじりの最大値を求める。
# 比較：(0) K064と同じ（Bは面外に固定）、(C) Bは球面軸受。前提はK064と同じ（仮）：GJ/EI=0.77、KH=2.0、片側分担をC点にx方向で与える。
# 架台が受けるMd（d軸まわり）には、Bの横力×（Bのピン高さh=268 − ねじ群の中心h=262.25）も加える（(C)ではこれだけ）。
import math, csv, subprocess, numpy as np
TS=subprocess.run(['date','+%y%m%d%H%M'],capture_output=True,text=True,env={'TZ':'Asia/Tokyo'}).stdout.strip()
exec(open('/tmp/k064.py',encoding='utf-8').read().split('rows=[]')[0])
def member_forces(P,u,ratio):
    out={}
    for i,j in (('O','A'),('A','B'),('A','C')):
        (d1,h1),(d2,h2)=P[i],P[j]; L=math.hypot(d2-d1,h2-h1); c=(d2-d1)/L; s=(h2-h1)/L
        k=np.zeros((6,6)); EI=1.0; GJ=ratio
        k[np.ix_([0,2,3,5],[0,2,3,5])]=EI/L**3*np.array([[12,6*L,-12,6*L],[6*L,4*L*L,-6*L,2*L*L],[-12,-6*L,12,-6*L],[6*L,2*L*L,-6*L,4*L*L]])
        k[1,1]=k[4,4]=GJ/L; k[1,4]=k[4,1]=-GJ/L
        T1=np.array([[1,0,0],[0,c,s],[0,-s,c]]); T=np.zeros((6,6)); T[:3,:3]=T1; T[3:,3:]=T1
        ii=['O','A','B','C'].index(i); jj=['O','A','B','C'].index(j)
        ul=T@np.concatenate([u[3*ii:3*ii+3],u[3*jj:3*jj+3]]); fl=k@ul
        out[i+j]=(max(abs(fl[2]),abs(fl[5]))/100, abs(fl[1])/100)   # 曲げ（両端の大きい方）、ねじり  N·m
    return out
rows=[]; HB=268-262.25
for sn in ('左','右'):
    for si,pos in enumerate(('収納','使用')):
        P=pose(OD[sn],si); F=share[sn]*2.0*W
        for case,free in (('(0) Bは面外に固定',[3,4,5,9,10,11]),('(C) Bは球面軸受',[3,4,5,7,8,9,10,11])):
            K,idx=grid(P,0.77); f=np.zeros(12); f[3*idx['C']]=F
            u=np.zeros(12); u[free]=np.linalg.solve(K[np.ix_(free,free)],f[free]); R=K@u-f
            MdB=abs(R[7])/100+abs(R[6])*HB/100
            mf=member_forces(P,u,0.77)
            rows.append([sn,pos,case,round(F,1),round(abs(R[1])/100,1),round(abs(R[0]),1),round(MdB,1),round(abs(R[6]),1),round(P['B'][0],1),
                         round(mf['OA'][0],1),round(mf['OA'][1],1),round(mf['AB'][0],1),round(mf['AB'][1],1),round(mf['AC'][0],1),round(mf['AC'][1],1)])
out='/mnt/user-data/outputs/%s_K065_Bの継手を球面軸受にしたときの力.csv'%TS
with open(out,'w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f)
    w.writerow(['K065 Bの継手を球面軸受にしたときの力（片側、地震の左右揺れKH=2.0、C点にx方向の力）'])
    w.writerow(['K064の骨組み（GJ/EI=0.77、仮）。(0) Bは面外に固定（K064と同じ）、(C) Bは球面軸受（面外の力のみ）。架台のMd＝d軸まわり（梁から引きはがす向き）、BのMdにはBの横力×5.75（ピン高さ−ねじ群中心）を含む'])
    w.writerow(['単位：力N、モーメントN·m。リンクの曲げ・ねじりは部材ごとの最大値（面外）'])
    w.writerow([])
    w.writerow(['側','位置','継手','C点の力','O：Md','O：x方向の力','B：Md','B：x方向の力','Bの位置d','OA 曲げ','OA ねじり','AB 曲げ','AB ねじり','AC 曲げ','AC ねじり'])
    w.writerows(rows)
for r in rows: print(r)
print(out)
