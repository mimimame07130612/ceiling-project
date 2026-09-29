# K041 リンク比を変えた場合のCの軌跡（B水平・C斜め、STEP4 4-1）
# スコットラッセルで OA=AB=AC のとき Cは直線（B⊥C）。AC≠AB にすると Cは楕円 C=O+((a-c)cosθ,(a+c)sinθ) を描く。
# B（スライダ）を水平（天井付近h一定）にしたまま、Cが斜めに降りる楕円弧を、必要経路（78.36°）に最も近づけた例を描く。
# 入力：A03-004〜006（CSP中心の収納cs・使用cu、wR=0）、A01-001、A02-002、D00-005・A00-006・A02-001、D01-001
import json, math, subprocess, glob
import numpy as np
TS=subprocess.run(['date','+%y%m%d%H%M'],capture_output=True,text=True,env={'TZ':'Asia/Tokyo'}).stdout.strip()  # 作図時 2609292258
NAME='K041_リンク比を変えたCの軌跡'
CSP=sorted(glob.glob('*_csp.py'))[-1]; SAN=sorted(glob.glob('*_sanmen.py'))[-1]
OUTJ='/mnt/user-data/outputs/%s_%s.json'%(TS,NAME); OUTS='/mnt/user-data/outputs/%s_%s.svg'%(TS,NAME)
subprocess.run(['python3',CSP,'json','-o','c.json','--pose','収納,139.45,48.5,243.77','--pose','使用,139.45,33,168.51'],check=True,capture_output=True)
C=json.load(open('c.json',encoding='utf-8'))
sd=[it['p'] for it in C['items'] if it['t']=='poly']
cs=np.array([sum(p[0] for p in sd[0])/4,sum(p[1] for p in sd[0])/4])
cu=np.array([sum(p[0] for p in sd[1])/4,sum(p[1] for p in sd[1])/4])
u=(cu-cs)/np.hypot(*(cu-cs))
def params(ts,tu):
    ax=(cs[0]-cu[0])/(math.cos(ts)-math.cos(tu)); by=(cs[1]-cu[1])/(math.sin(ts)-math.sin(tu))
    return ax,by,cs[0]-ax*math.cos(ts),cs[1]-by*math.sin(ts)
def dev(ts,tu):
    ax,by,Od,Oh=params(ts,tu)
    if ax<=0 or by<=0: return 1e9,None
    th=np.linspace(ts,tu,80); P=np.stack([Od+ax*np.cos(th),Oh+by*np.sin(th)],1)
    rel=P-cs; return np.abs(rel[:,0]*u[1]-rel[:,1]*u[0]).max(),(ax,by,Od,Oh)
# 目標 a≈74・スライダ天井付近 で最小ずれのθを細かく探索
bestp=None
for ts in np.linspace(-2.4,2.4,600):
    for tu in np.linspace(-2.4,2.4,600):
        if abs(ts-tu)<0.15: continue
        d,pr=dev(ts,tu)
        if pr is None: continue
        ax,by,Od,Oh=pr; a=(ax+by)/2
        if abs(a-74)>2.0 or not(260<=Oh<=269): continue
        if bestp is None or d<bestp[0]: bestp=(d,ts,tu,ax,by,Od,Oh,a,(by-ax)/2)
dmax,ts,tu,ax,by,Od,Oh,a,c=bestp
def C_of(t): return np.array([Od+ax*math.cos(t),Oh+by*math.sin(t)])
def B_of(t): return np.array([Od+2*a*math.cos(t),Oh])
def A_of(t): return np.array([Od+a*math.cos(t),Oh+a*math.sin(t)])
r2=lambda p:[round(float(p[0]),2),round(float(p[1]),2)]
items=list(C['items'])
# 必要経路（直線）と2cm回廊
items.append(dict(t='line',view='side',p=[r2(cs),r2(cu)],color='#999999',w=1.4,dash=True))
items.append(dict(t='text',view='side',p=r2((cs+cu)/2),s='直線経路（78.4°）',dx=-4,dy=-6,anchor='end',color='#777777'))
# 楕円（全周うすく＋弧を実線）
full=[r2(C_of(t)) for t in np.linspace(0,2*math.pi,120)]
items.append(dict(t='poly',view='side',p=full,color='#2E9E6B',fill='#2E9E6B',op=0.05,w=0.8))
arc=[r2(C_of(t)) for t in np.linspace(ts,tu,60)]
items.append(dict(t='line',view='side',p=arc,color='#2E9E6B',w=2.6))
# 最大ずれ点
th=np.linspace(ts,tu,120); P=np.stack([Od+ax*np.cos(th),Oh+by*np.sin(th)],1)
k=np.argmax(np.abs((P-cs)@np.array([u[1],-u[0]]))); Pm=P[k]
foot=cs+((Pm-cs)@u)*u
items.append(dict(t='line',view='side',p=[r2(Pm),r2(foot)],color='#C0392B',w=1.4))
items.append(dict(t='text',view='side',p=r2(Pm),s='最大ずれ %.1fcm'%dmax,dx=6,dy=2,color='#C0392B'))
# スライダ（水平）
items.append(dict(t='line',view='side',p=[r2(B_of(ts)+np.array([6,0])),r2(B_of(tu)-np.array([6,0]))],color='#111111',w=3.0))
items.append(dict(t='text',view='side',p=r2(B_of(ts)),s='Bのレール（水平 h=%.0f）'%Oh,dx=4,dy=-6,color='#111111'))
# リンク（収納青・使用赤）
for t,col,tag in ((ts,'#2C6FB0','収'),(tu,'#C0392B','使')):
    O=np.array([Od,Oh]); A=A_of(t); B=B_of(t); Cc=C_of(t)
    items.append(dict(t='line',view='side',p=[r2(O),r2(A)],color=col,w=2.0,dash=(tag=='使')))
    items.append(dict(t='line',view='side',p=[r2(B),r2(Cc)],color=col,w=2.0,dash=(tag=='使')))
    for q,nm in ((A,'A'),(B,'B'),(Cc,'C')):
        items.append(dict(t='pt',view='side',p=r2(q),color=col,r=3.0))
        items.append(dict(t='text',view='side',p=r2(q),s='%s(%s)'%(nm,tag),dx=5,dy=(-5 if nm!='B' else 14),color=col))
items.append(dict(t='pt',view='side',p=r2([Od,Oh]),color='#111111',r=4.5,ring=True))
items.append(dict(t='text',view='side',p=r2([Od,Oh]),s='O(楕円中心=固定)',dx=-4,dy=18,anchor='end',color='#111111'))
# 正面図：左右リンクのx（wR=0）
for xx,nm,col in ((110.9,'左リンク x=110.9','#2C6FB0'),(168.0,'右リンク x=168.0','#C0392B')):
    items.append(dict(t='line',view='front',p=[[xx,238],[xx,270]],color=col,w=1.6,dash=True))
    items.append(dict(t='text',view='front',p=[xx,238],s=nm,dx=0,dy=16,color=col,anchor='middle'))
notes=[
 'STEP4 4-1：短リンクの接続比（AC/AB）を変えるとどうなるか。スコットラッセルは OA=AB=AC のとき Cが直線（このときBの直線とCの直線はO上で必ず直交）。',
 'AC≠AB にすると Cの軌跡は楕円 C=O+((a−c)cosθ,(a+c)sinθ)。Bは水平（h一定）のまま、Cは楕円弧に沿って斜めに降ろせる。B⊥Cの縛りは外れる（依頼主の狙いどおり）。',
 '代償：Cの経路が直線でなく曲がる。この例（AC/AB=%.2f、a=%.0f・c=%.0f、スライダ h=%.0f）で、直線経路からの最大ずれ %.1fcm。' % (c/a,a,c,Oh,dmax),
 'リンクを大きくするほど弧は平らになるが、スライダを天井付近に置く条件では大きくしても最小ずれ≒2.9cm止まり（別途スイープで確認）。一直線移動の回廊（天井端・SCケースに余裕2cm、K023・K024）は超える。',
 '利点：Bが天井付近h=%.0fに留まり、梁下面(254.5)より下に垂れない（元のスコットラッセルはB収納がh≒250まで下がっていた）。意匠(S3-b)には有利。' % Oh,
 '評価：直線でなく曲線になるので、成立させるなら「この楕円弧で天井端・SCケースに当たらないか」を4-2で弧そのものについて判定し直す必要がある（直線用の回廊判定は使えない）。CSPの姿勢を保つ課題は直線版と同じく別途必要。',
 '正面図：左右リンクのx位置（x=110.9／168.0、wR=0）。',
]
ov=dict(title_note=notes,legend=C['legend']+[
    dict(text='緑 太線：Cの楕円弧（実際の経路）／うすい緑：楕円全周',color='#2E9E6B',kind='line'),
    dict(text='灰 破線：必要な直線経路（78.4°）',color='#999999',dash=True,kind='line'),
    dict(text='黒 太線：Bのレール（水平）',color='#111111',kind='line'),
    dict(text='青／赤：リンクOA・BC（収納／使用）',color='#2C6FB0',dash=True,kind='line'),
    dict(text='赤 細線：直線からの最大ずれ',color='#C0392B',kind='line')],
    src=C['src']+['A03-004〜006','D00-005','A00-006','A02-001','D01-001'],items=items)
json.dump(ov,open(OUTJ,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
subprocess.run(['python3',SAN,'--zuban','K041','--title','リンク比を変えたCの軌跡','-o',OUTS,OUTJ],check=True)
print('a=%.1f c=%.1f AC/AB=%.2f Oh=%.1f 最大ずれ=%.2f'%(a,c,c/a,Oh,dmax))
print('B: 収納d=%.1f 使用d=%.1f (h=%.1f一定)'%(B_of(ts)[0],B_of(tu)[0],Oh))
print('\n'.join(notes))
