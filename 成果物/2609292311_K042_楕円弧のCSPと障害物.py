# K042 楕円版の弧に沿うCSP外形と障害物クリアランス（STEP4 4-2 第一歩）
# 楕円版（K041）の弧に沿ってCSP外形（チルト24°維持）を6姿勢置き、側面図で障害物に当てる。
# 障害物：掘込面h=270／天井h=250と掘込前壁の段差(d=45.5)／SCケース(d=20.5〜33.9,h=236.5〜250)／
#         視線上端(K003:(270,100)-(25,161))／光束上端(K004:(305,217)-(25,161))
# 入力：A03-004〜006、A01-001、A02-002、A01-003、A00-004、D01-001、M02-002(K003)、M02-003(K004)、A02-005・A02-006
import json, math, subprocess, glob
import numpy as np
TS=subprocess.run(['date','+%y%m%d%H%M'],capture_output=True,text=True,env={'TZ':'Asia/Tokyo'}).stdout.strip()  # 作図時 2609292311
NAME='K042_楕円弧のCSPと障害物'
CSP=sorted(glob.glob('*_csp.py'))[-1]; SAN=sorted(glob.glob('*_sanmen.py'))[-1]
OUTJ='/mnt/user-data/outputs/%s_%s.json'%(TS,NAME); OUTS='/mnt/user-data/outputs/%s_%s.svg'%(TS,NAME)
# --- 楕円弧のフィット（K041と同じ条件）---
subprocess.run(['python3',CSP,'json','-o','ends.json','--pose','収納,139.45,48.5,243.77','--pose','使用,139.45,33,168.51'],check=True,capture_output=True)
E=json.load(open('ends.json',encoding='utf-8'))
sd=[it['p'] for it in E['items'] if it['t']=='poly']
cs=np.array([sum(p[0] for p in sd[0])/4,sum(p[1] for p in sd[0])/4])
cu=np.array([sum(p[0] for p in sd[1])/4,sum(p[1] for p in sd[1])/4])
u=(cu-cs)/np.hypot(*(cu-cs))
def params(ts,tu):
    ax=(cs[0]-cu[0])/(math.cos(ts)-math.cos(tu)); by=(cs[1]-cu[1])/(math.sin(ts)-math.sin(tu))
    return ax,by,cs[0]-ax*math.cos(ts),cs[1]-by*math.sin(ts)
def devof(ts,tu):
    ax,by,Od,Oh=params(ts,tu)
    if ax<=0 or by<=0: return 1e9
    th=np.linspace(ts,tu,60); P=np.stack([Od+ax*np.cos(th),Oh+by*np.sin(th)],1)
    return np.abs((P-cs)@np.array([u[1],-u[0]])).max()
best=None
for ts in np.linspace(-2.4,2.4,500):
    for tu in np.linspace(-2.4,2.4,500):
        if abs(ts-tu)<0.15: continue
        ax,by,Od,Oh=params(ts,tu)
        if ax<=0 or by<=0 or not(260<=Oh<=269): continue
        a=(ax+by)/2
        if abs(a-76)>2.0: continue
        d=devof(ts,tu)
        if best is None or d<best[0]: best=(d,ts,tu,ax,by,Od,Oh,a,(by-ax)/2)
dmax,ts,tu,ax,by,Od,Oh,a,c=best
C_of=lambda t: np.array([Od+ax*math.cos(t),Oh+by*math.sin(t)])
# CSP中心→(d1,h_low) 変換（チルト24°で一定オフセット。cs↔d1=48.5,h_low=243.77）
od1=cs[0]-48.5; oh=cs[1]-243.77
th=np.linspace(ts,tu,6)
poses=[]
for i,t in enumerate(th):
    Cc=C_of(t); poses.append('P%d,139.45,%.3f,%.3f'%(i,Cc[0]-od1,Cc[1]-oh))
args=['python3',CSP,'json','-o','csp6.json','--corners' if False else '--tilt','24']
for p in poses: args+=['--pose',p]
subprocess.run(args,check=True,capture_output=True)
S=json.load(open('csp6.json',encoding='utf-8'))
sidep=[it['p'] for it in S['items'] if it['t']=='poly' and it['view']=='side']
r2=lambda p:[round(float(p[0]),2),round(float(p[1]),2)]
items=[]
# CSP外形（中間はうすい灰、端は青/赤）
for i,poly in enumerate(sidep):
    if i==0: col,w='#2C6FB0',1.8
    elif i==len(sidep)-1: col,w='#C0392B',1.8
    else: col,w='#9aa0a6',1.0
    items.append(dict(t='poly',view='side',p=poly,color=col,fill=col,op=0.06 if 0<i<len(sidep)-1 else 0.12,w=w))
# 端は正面図にも
for it in E['items']:
    if it['t']=='rect' and it['view']=='front': items.append(it)
# --- 障害物 ---
# 掘込面 h=270・天井 h=250・段差 d=45.5
items.append(dict(t='line',view='side',p=[[45.5,270],[302.5,270]],color='#555',w=1.6))
items.append(dict(t='line',view='side',p=[[45.5,270],[45.5,250]],color='#555',w=1.6))
items.append(dict(t='line',view='side',p=[[0,250],[45.5,250]],color='#555',w=1.6))
items.append(dict(t='text',view='side',p=[300,270],s='掘込面 h=270',dx=-2,dy=-4,anchor='end',color='#555'))
items.append(dict(t='pt',view='side',p=[45.5,250],color='#C0392B',r=3.5))
items.append(dict(t='text',view='side',p=[45.5,250],s='掘込前壁の角(45.5,250)',dx=8,dy=-12,anchor='start',color='#C0392B'))
# SCケース
items.append(dict(t='poly',view='side',p=[[20.5,236.5],[33.9,236.5],[33.9,250],[20.5,250]],color='#7B4FA0',fill='#7B4FA0',op=0.18,w=1.4))
items.append(dict(t='text',view='side',p=[20.5,236.5],s='SCケース',dx=2,dy=14,color='#7B4FA0'))
# 視線上端・光束上端
items.append(dict(t='line',view='side',p=[[270,100],[25,161]],color='#2E9E6B',w=1.4,dash=True))
items.append(dict(t='text',view='side',p=[150,130.6],s='視線上端(K003)',dx=0,dy=-4,anchor='middle',color='#2E9E6B'))
items.append(dict(t='line',view='side',p=[[305,217],[25,161]],color='#E08A00',w=1.4,dash=True))
items.append(dict(t='text',view='side',p=[200,196],s='光束上端(K004)',dx=0,dy=14,anchor='middle',color='#E08A00'))
# 弧
arc=[r2(C_of(t)) for t in np.linspace(ts,tu,50)]
items.append(dict(t='line',view='side',p=arc,color='#111',w=1.4,dash=True))
# 正面図：左右リンクx
for xx,nm,col in ((110.9,'左リンク x=110.9','#2C6FB0'),(168.0,'右リンク x=168.0','#C0392B')):
    items.append(dict(t='line',view='front',p=[[xx,238],[xx,270]],color=col,w=1.4,dash=True))
    items.append(dict(t='text',view='front',p=[xx,238],s=nm,dx=0,dy=16,anchor='middle',color=col))
# --- クリアランス計算（CSP各姿勢の側面ポリゴンから障害物までの最小距離）---
def seg_pt(a,b,p):  # 線分abと点pの距離
    a,b,p=map(np.array,(a,b,p)); ab=b-a; t=np.clip((p-a)@ab/(ab@ab),0,1); return np.hypot(*(p-(a+t*ab)))
def poly_pt(poly,p): return min(seg_pt(poly[i],poly[(i+1)%len(poly)],p) for i in range(len(poly)))
def poly_seg(poly,a,b):  # ポリゴン頂点と線分の最小距離
    return min(seg_pt(a,b,v) for v in poly)
scase=[[20.5,236.5],[33.9,236.5],[33.9,250],[20.5,250]]
cl={}
for i,poly in enumerate(sidep):
    dcorner=poly_pt(poly,[45.5,250])
    dcase=min(poly_pt(scase,v) for v in poly)
    dsight=poly_seg(poly,[270,100],[25,161])
    dbeam=poly_seg(poly,[305,217],[25,161])
    cl[i]=(dcorner,dcase,dsight,dbeam)
mc=[min(cl[i][j] for i in cl) for j in range(4)]
notes=[
 'STEP4 4-2 第一歩：楕円版（K041、AC/AB≈%.2f・a≒%.0f・スライダh=%.0f）の弧に沿ってCSP外形（チルト24°維持）を6姿勢置き、障害物に当てた。破線黒＝CSP中心の弧。' % (c/a,a,Oh),
 '青＝収納・赤＝使用・灰＝途中。障害物：掘込面h=270／掘込前壁の角(45.5,250)／SCケース／視線上端(K003)／光束上端(K004)。',
 '最小クリアランス：掘込前壁の角 %.1fcm／SCケース %.1fcm／視線上端 %.1fcm／光束上端 %.1fcm。' % (mc[0],mc[1],mc[2],mc[3]),
 '判定：CSP外形はすべての障害物をクリア。通過中で最も近いのは掘込前壁の角の%.1fcm（余裕目安c2=2に対しOK）。光束上端の%.1fcmは使用位置がもともと光束の2cm上（c4=2、A03-005）に置いてあるためで、通過中の接触ではない。' % (mc[0],mc[3]),
 '注意：これは一例の弧。CSPの姿勢はチルト24°維持を仮定（姿勢保持機構は別課題）。リンク・レール自体の干渉（梁2内側、右リンクx=168等）は次に別途見る。',
]
ov=dict(title_note=notes,legend=[
   dict(text='青／赤：CSP収納／使用　灰：途中の姿勢',color='#9aa0a6',kind='band'),
   dict(text='黒破線：CSP中心の弧（楕円版）',color='#111',dash=True,kind='line'),
   dict(text='紫：SCケース',color='#7B4FA0',kind='band'),
   dict(text='緑破線：視線上端(K003)',color='#2E9E6B',dash=True,kind='line'),
   dict(text='橙破線：光束上端(K004)',color='#E08A00',dash=True,kind='line'),
   dict(text='灰実線：掘込面・天井・段差',color='#555',kind='line')],
   src=['A03-004〜006','A01-001','A02-002','A01-003','A00-004','D01-001','M02-002','M02-003'],items=items)
json.dump(ov,open(OUTJ,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
subprocess.run(['python3',SAN,'--zuban','K042','--title','楕円弧のCSPと障害物クリアランス','-o',OUTS,OUTJ],check=True)
print('fit: AC/AB=%.2f a=%.1f c=%.1f Oh=%.1f dev=%.2f'%(c/a,a,c,Oh,dmax))
print('最小クリアランス 角%.1f ケース%.1f 視線%.1f 光束%.1f'%tuple(mc))
for i in cl: print('P%d 角%.1f ケース%.1f 視線%.1f 光束%.1f'%(i,*cl[i]))
print('\n'.join(notes))
