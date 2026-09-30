# K043 楕円版リンクの干渉（ずれ最小フィットの問題点、STEP4 4-2）
# ずれ最小で選んだO・比率だと、OAリンクが掘込前壁角(45.5,250)に0.11cm・SCケースに0.32cmまで迫る。
# CSP本体は通る（K042）が、リンクは当たる。→ フィット基準を機構優先に変える必要がある。
# 入力：K042のフィット（fit.npy）、A01-003（SCケース）、D01-001、A03-004〜006
import json, math, subprocess, glob
import numpy as np
TS=subprocess.run(['date','+%y%m%d%H%M'],capture_output=True,text=True,env={'TZ':'Asia/Tokyo'}).stdout.strip()  # 作図時 2609300013
NAME='K043_楕円版リンクの干渉'
CSP=sorted(glob.glob('*_csp.py'))[-1]; SAN=sorted(glob.glob('*_sanmen.py'))[-1]
OUTJ='/mnt/user-data/outputs/%s_%s.json'%(TS,NAME); OUTS='/mnt/user-data/outputs/%s_%s.svg'%(TS,NAME)
d0,ts,tu,ax,by,Od,Oh,a,c=np.load('fit.npy')
def geom(t):
    O=np.array([Od,Oh]);C=np.array([Od+ax*math.cos(t),Oh+by*math.sin(t)]);B=np.array([Od+2*a*math.cos(t),Oh]);A=np.array([Od+a*math.cos(t),Oh+a*math.sin(t)]);return O,A,B,C
r2=lambda p:[round(float(p[0]),2),round(float(p[1]),2)]
# CSP外形（端2姿勢）
subprocess.run(['python3',CSP,'json','-o','ce.json','--pose','収納,139.45,48.5,243.77','--pose','使用,139.45,33,168.51'],check=True,capture_output=True)
CE=json.load(open('ce.json',encoding='utf-8'))
items=[]
for it in CE['items']:
    if it['t']=='poly' and it['view']=='side':
        it2=dict(it); it2['op']=0.10; items.append(it2)
    if it['t']=='rect' and it['view']=='front': items.append(it)
# 障害物
items.append(dict(t='line',view='side',p=[[45.5,270],[302.5,270]],color='#555',w=1.4))
items.append(dict(t='line',view='side',p=[[45.5,270],[45.5,250]],color='#555',w=1.4))
items.append(dict(t='line',view='side',p=[[0,250],[45.5,250]],color='#555',w=1.4))
items.append(dict(t='text',view='side',p=[295,270],s='掘込面h=270',dx=-2,dy=-4,anchor='end',color='#555'))
items.append(dict(t='poly',view='side',p=[[20.5,236.5],[33.9,236.5],[33.9,250],[20.5,250]],color='#7B4FA0',fill='#7B4FA0',op=0.2,w=1.4))
items.append(dict(t='text',view='side',p=[27,243],s='SCケース',dx=0,dy=0,anchor='middle',color='#7B4FA0'))
# 弧
items.append(dict(t='line',view='side',p=[r2(geom(ts+(tu-ts)*i/40)[3]) for i in range(41)],color='#111',w=1.0,dash=True))
# リンク（収納青・使用赤）＋レール
for t,col,tag in ((ts,'#2C6FB0','収'),(tu,'#C0392B','使')):
    O,A,B,C=geom(t)
    items.append(dict(t='line',view='side',p=[r2(O),r2(A)],color=col,w=2.4))     # OAリンク
    items.append(dict(t='line',view='side',p=[r2(B),r2(C)],color=col,w=1.8,dash=True))  # ロッドBC
    for q,nm in ((O,'O'),(A,'A(%s)'%tag),(B,'B(%s)'%tag),(C,'C(%s)'%tag)):
        items.append(dict(t='pt',view='side',p=r2(q),color=col,r=3.0))
# O強調
O=geom(ts)[0]
items.append(dict(t='pt',view='side',p=r2(O),color='#111',r=5,ring=True))
items.append(dict(t='text',view='side',p=r2(O),s='O 固定(d=19.4,h=268)',dx=4,dy=-8,color='#111'))
# レール（B収納〜B使用、水平）
Bs=geom(ts)[2]; Bu=geom(tu)[2]
items.append(dict(t='line',view='side',p=[r2(Bs+np.array([6,0])),r2(Bu-np.array([6,0]))],color='#111',w=3.0))
items.append(dict(t='text',view='side',p=r2(Bs),s='Bレール(水平h=268)',dx=-2,dy=-6,anchor='end',color='#111'))
# 干渉の強調
items.append(dict(t='pt',view='side',p=[45.5,250],color='#D00',r=4))
items.append(dict(t='text',view='side',p=[45.5,250],s='OA↔前壁角 0.11cm',dx=8,dy=8,color='#D00'))
items.append(dict(t='text',view='side',p=[33.9,250],s='OA↔SCケース 0.32cm',dx=8,dy=24,color='#D00'))
# 正面図：左右リンクx
for xx,nm,col in ((110.9,'左リンク x=110.9','#2C6FB0'),(168.0,'右リンク x=168.0','#C0392B')):
    items.append(dict(t='line',view='front',p=[[xx,238],[xx,270]],color=col,w=1.4,dash=True))
    items.append(dict(t='text',view='front',p=[xx,238],s=nm,dx=0,dy=16,anchor='middle',color=col))
notes=[
 'STEP4 4-2：楕円版（ずれ最小フィット：O=(19.4,268)・a=77.7・c=35.2）のリンクを障害物に当てた。太実線＝OAリンク、破線＝ロッドBC、黒太＝Bレール。青収納・赤使用。',
 '問題：使用側でOAリンクが掘込前壁の角(45.5,250)に0.11cm、SCケースに0.32cmまで迫る（ほぼ接触）。ロッドBCは9cm以上で余裕あり。CSP本体は通る（K042）がリンクが当たる。',
 '原因：このO位置・比率は「直線からのずれ最小」で選んだもの。ずれは無価値（依頼主）なので、フィット基準を機構優先（O・リンクが障害物をよけ、素直に取付き、伝達角が破綻しない）に変えるべき。',
 '応力の観点：収納はθ=−6.3°で特異点θ=0の直前。伝達角12.7°・速度比6.54で、収納付近の駆動に大きな力（＝リンク応力）。使用側は伝達角78°で良好。スライダ鉛直反力は(c/a)W≒68Nで一定。',
 '次：Oを梁2内側など取り付けやすい位置に置き、リンクが障害物をよけ、収納が特異点から離れる条件で、比率・O・スライダ高を選び直す（CSP本体クリアランスはK042で余裕あり）。',
]
ov=dict(title_note=notes,legend=[
   dict(text='青／赤：OAリンク（収納／使用）　破線：ロッドBC',color='#2C6FB0',kind='line'),
   dict(text='黒太：Bレール（水平）／黒破線：CSP中心の弧',color='#111',kind='line'),
   dict(text='赤：ほぼ接触の箇所',color='#D00',kind='dot'),
   dict(text='紫：SCケース／灰：掘込面・天井・段差',color='#7B4FA0',kind='band')],
   src=['A03-004〜006','A01-001','A02-002','A01-003','D01-001'],items=items)
json.dump(ov,open(OUTJ,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
subprocess.run(['python3',SAN,'--zuban','K043','--title','楕円版リンクの干渉','-o',OUTS,OUTJ],check=True)
print('wrote',OUTS)
