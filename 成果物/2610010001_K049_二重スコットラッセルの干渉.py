# K049 二重スコットラッセルの干渉（STEP4 4-2、姿勢保持案1、配置β Δd=18）
# 部屋三面図に、2組の機構（O-A-B-C／O′-A′-B′-C′）・共有Bキャリッジ・レール・CSPを重ねる。
# 配置β：C・C′をCSP中心(d=61.73,h=255.885)の両側に±9。数値比較（α・β、Δd=6〜23）は K050。
# 入力：K046/K047（水平・鉛直版の幾何）、K048（案1）、A01-001、A01-003、A02-002、D01-001、改訂予定A03-005（使用 d1=48.5・h=171.61）
import json, math, subprocess, glob
TS=json.load(open('/tmp/k050_rows.json'))['ts']
NAME='K049_二重スコットラッセルの干渉'
CSP=sorted(glob.glob('*_csp.py'))[-1]; SAN=sorted(glob.glob('*_sanmen.py'))[-1]
OUTJ='/mnt/user-data/outputs/%s_%s.json'%(TS,NAME); OUTS='/mnt/user-data/outputs/%s_%s.svg'%(TS,NAME)
a=50.0; CS_H=255.885; STROKE=72.16; t0=268-CS_H; DC=61.73; DD=18.0
d1,d2=DC-DD/2,DC+DD/2
def pose(Od,s):
    oc=t0+STROKE*s; C=(Od,268-oc); ph=math.asin(oc/(2*a)); B=(Od+2*a*math.cos(ph),268.0); A=((B[0]+C[0])/2,(B[1]+C[1])/2)
    return ph,A,B,C
subprocess.run(['python3',CSP,'json','-o','/tmp/c49.json','--pose','収納,139.45,48.5,243.77','--pose','使用,139.45,48.5,171.61'],check=True,capture_output=True)
C0=json.load(open('/tmp/c49.json',encoding='utf-8'))
items=[]
for it in C0['items']:
    if it['t']=='poly' and it['view']=='side': it2=dict(it); it2['op']=0.10; items.append(it2)
    if it['t']=='rect': items.append(it)
r2=lambda p:[round(p[0],2),round(p[1],2)]
SCC=[[20.5,236.5],[33.9,236.5],[33.9,250],[20.5,250]]
items.append(dict(t='poly',view='side',p=SCC,color='#7B4FA0',fill='#7B4FA0',op=0.2,w=1.4))
items.append(dict(t='line',view='side',p=[[25,161],[305,217]],color='#D85A30',w=1.2,dash=True))
items.append(dict(t='text',view='side',p=[200,193],s='投射光上端面',color='#D85A30'))
items.append(dict(t='line',view='side',p=[[40,254.5],[330,254.5]],color='#8a857a',w=1.0,dash=True))
for i in range(1,4):
    s=i/4
    for Od in (d1,d2):
        _,A,B,C=pose(Od,s)
        items.append(dict(t='line',view='side',p=[[Od,268],r2(A)],color='#aaaaaa',w=1.0))
        items.append(dict(t='line',view='side',p=[r2(B),r2(C)],color='#aaaaaa',w=0.8))
for s,col,tag in ((0,'#2C6FB0','収'),(1,'#C0392B','使')):
    P1=pose(d1,s); P2=pose(d2,s)
    for (ph,A,B,C),w1,w2 in ((P1,2.6,1.8),(P2,1.8,1.2)):
        items.append(dict(t='line',view='side',p=[[C[0],268],r2(A)],color=col,w=w1))
        items.append(dict(t='line',view='side',p=[r2(B),r2(C)],color=col,w=w2,dash=True))
        for q in (A,B,C): items.append(dict(t='pt',view='side',p=r2(q),color=col,r=2.6))
    items.append(dict(t='line',view='side',p=[r2(P1[3]),r2(P2[3])],color=col,w=3.2))   # CSP保持具（C–C′）
    items.append(dict(t='line',view='side',p=[r2(P1[2]),r2(P2[2])],color=col,w=5,)) # Bキャリッジ
items.append(dict(t='text',view='side',p=r2(pose(d1,1)[3]),s="C–C′ 保持具",dx=-4,dy=14,anchor='end',color='#C0392B'))
items.append(dict(t='text',view='side',p=r2(pose(d2,0)[2]),s="Bキャリッジ(B–B′)",dx=4,dy=14,color='#2C6FB0'))
R0=pose(d1,1)[2][0]-6; R1=pose(d2,0)[2][0]+6
items.append(dict(t='line',view='side',p=[[R0,268],[R1,268]],color='#111',w=2.0))
items.append(dict(t='text',view='side',p=[R1,268],s='レール d=%.1f〜%.1f'%(R0,R1),dx=4,dy=4,color='#111'))
for Od,nm in ((d1,'O'),(d2,'O′')):
    items.append(dict(t='pt',view='side',p=[Od,268],color='#111',r=4.2,ring=True))
items.append(dict(t='text',view='side',p=[d1,268],s='O(d=%.1f)・O′(d=%.1f) h=268'%(d1,d2),dx=-4,dy=-10,anchor='end',color='#111'))
for xx,nm,col in ((110.9,'左リンク群 x≦110.9','#2C6FB0'),(168.0,'右リンク群 x≧168.0','#C0392B')):
    items.append(dict(t='line',view='front',p=[[xx,170],[xx,270]],color=col,w=1.4,dash=True))
    items.append(dict(t='text',view='front',p=[xx,205],s=nm,dx=(-4 if xx<140 else 4),anchor=('end' if xx<140 else 'start'),color=col))
notes=[
 'STEP4 4-2（姿勢保持 案1：二重スコットラッセル、配置β Δd=18）：O-A-B-C（太）とO′-A′-B′-C′（細）を並べ、BとB′は1台のキャリッジ、CとC′は保持具でCSPに固定。青収納・赤使用・灰中間。',
 'C・C′はCSP中心の高さの水平線上、中心の両側±9（CSP側面の弦 d=50.02〜73.44 の内側、余裕2.7）。OはO′とも掘込面の2下（h=268、K046と同じ）。',
 '障害物との最小クリアランス7.2（OAリンク↔掘込前壁）。収納時は2組とも梁下面h=254.5より上。側面図でロッドBCとO′A′リンクが交差する（K050）→ 別のx面に置く必要がある。',
 '部品は線（太さ0）での判定。正面図：リンク群は片側に複数面並ぶため、wL・wR（A03-004）に効く。',
]
ov=dict(title_note=notes,legend=C0['legend']+[
  dict(text='青／赤：リンク（太＝1組目、細＝2組目）　破線：ロッド',color='#2C6FB0',kind='line'),
  dict(text='太帯：Bキャリッジ・C–C′保持具／黒：レール',color='#111',kind='line'),
  dict(text='灰：途中姿勢',color='#aaaaaa',kind='line'),
  dict(text='紫：SCケース／橙破線：投射光上端面',color='#7B4FA0',kind='band')],
  src=['K046','K048','A01-001','A01-003','A02-002','D01-001','A03-005（改訂予定）'],items=items)
json.dump(ov,open(OUTJ,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
subprocess.run(['python3',SAN,'--zuban','K049','--title','二重スコットラッセルの干渉','-o',OUTS,OUTJ],check=True)
