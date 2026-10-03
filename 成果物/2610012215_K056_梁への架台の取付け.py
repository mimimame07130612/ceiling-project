# K056 梁への架台の取付け（STEP4 4-3、水平・鉛直版スコットラッセル、姿勢保持案1・配置β、左右独立駆動の仮前提）
# 梁の内側面（梁1 x=89.5、梁2 x=170）に架台（板、仮厚1）を付け、Oの軸受け・レール・ねじ・モーターを載せる。
# リンク面は梁の側面のすぐそば（左 x=92.0、右 x=168.0、仮）。CSP側面までは保持具で渡す（C点には鉛直荷重だけ）。
# 前提値（仮）：a=50、O・Bの高さ h=268、左 O/C d=52.73、右 O′/C′ d=70.73、wR=0（CSP x=110.9〜168.0）、架台 h=254.5〜270、
#   レール・ねじは架台上 h≈262（Bのピンはh=268の線上、キャリッジの腕で受ける）、モーター6×6×8（仮）はレールのLP側端。
# 入力：K046・K049・K051・K055、A00-005、A01-001、A03-004、D01-001、D01-004、D04-002
import json, math, subprocess, glob
TS=subprocess.run(['date','+%y%m%d%H%M'],capture_output=True,text=True,env={'TZ':'Asia/Tokyo'}).stdout.strip()
NAME='K056_梁への架台の取付け'
CSP=sorted(glob.glob('*_csp.py'))[-1]; SAN=sorted(glob.glob('*_sanmen.py'))[-1]
OUTJ='/mnt/user-data/outputs/%s_%s.json'%(TS,NAME); OUTS='/mnt/user-data/outputs/%s_%s.svg'%(TS,NAME)
a=50.0; CS_H=255.885; STROKE=72.16; t0=268-CS_H
XL,XR=92.0,168.0; DL,DR=52.73,70.73; T=1.0
def pose(Od,s):
    oc=t0+STROKE*s; C=(Od,268-oc); ph=math.asin(oc/(2*a)); B=(Od+2*a*math.cos(ph),268.0); A=((B[0]+C[0])/2,(B[1]+C[1])/2)
    return ph,A,B,C
subprocess.run(['python3',CSP,'json','-o','/tmp/c56.json','--pose','収納,139.45,48.5,243.77','--pose','使用,139.45,48.5,171.61'],check=True,capture_output=True)
C0=json.load(open('/tmp/c56.json',encoding='utf-8'))
items=list(C0['items']); r=lambda v:round(v,2)
FR='#5F5E5A'; LK='#2C6FB0'; HD='#1D9E75'; MT='#D85A30'
spans={}
for side,(xb0,xb1,xl,Od) in {'左':(89.5,89.5+T,XL,DL),'右':(170-T,170,XR,DR)}.items():
    Bu=pose(Od,1)[2][0]; Bs=pose(Od,0)[2][0]
    d0=Od-4; d1=Bs+6+8
    spans[side]=(d0,d1,Bu,Bs)
    items.append(dict(t='rect',view='plan',p=[xb0,r(d0),xb1,r(d1)],color=FR,fill=FR,op=0.6,w=1.2))
    items.append(dict(t='rect',view='front',p=[xb0,254.5,xb1,270],color=FR,fill=FR,op=0.6,w=1.2))
    items.append(dict(t='rect',view='side',p=[r(d0),254.5,r(d1),270],color=FR,fill='none',op=0,w=1.0,dash=(side=='右')))
    # O軸受け・レール・ねじ・モーター（平面）
    items.append(dict(t='line',view='plan',p=[[min(xb0,xb1) if side=='右' else xb1,Od],[xl,Od]],color='#111',w=2.4))
    items.append(dict(t='pt',view='plan',p=[xl,Od],color='#111',r=3.4,ring=True))
    items.append(dict(t='line',view='plan',p=[[xl,r(Bu-6)],[xl,r(Bs+6)]],color='#111',w=2.0))
    mx0,mx1=(xb1,xb1+6) if side=='左' else (xb0-6,xb0)
    items.append(dict(t='rect',view='plan',p=[mx0,r(Bs+6),mx1,r(Bs+14)],color=MT,fill=MT,op=0.35,w=1.0))
    # 正面：リンク面・O・レール
    items.append(dict(t='line',view='front',p=[[xl,180],[xl,268]],color=LK,w=1.4,dash=True))
    items.append(dict(t='line',view='front',p=[[xb1 if side=='左' else xb0,268],[xl,268]],color='#111',w=2.4))
    items.append(dict(t='pt',view='front',p=[xl,268],color='#111',r=3.0,ring=True))
    items.append(dict(t='rect',view='front',p=[mx0,258,mx1,266],color=MT,fill=MT,op=0.35,w=1.0))
    # 側面：O・レール（h≈262）・Bのピン線
    items.append(dict(t='line',view='side',p=[[r(Bu-6),262],[r(Bs+6),262]],color='#111',w=2.0,dash=(side=='右')))
    items.append(dict(t='pt',view='side',p=[Od,268],color='#111',r=3.6,ring=True))
# 保持具（正面：リンク面→CSP側面）
for s,h,col in ((0,CS_H,'#2C6FB0'),(1,CS_H-STROKE,'#C0392B')):
    items.append(dict(t='line',view='front',p=[[XL,r(h)],[110.9,r(h)]],color=HD,w=3.0))
    items.append(dict(t='line',view='front',p=[[168.0,r(h)],[XR,r(h)]],color=HD,w=3.0))
    items.append(dict(t='pt',view='front',p=[XL,r(h)],color=col,r=2.6)); items.append(dict(t='pt',view='front',p=[XR,r(h)],color=col,r=2.6))
items.append(dict(t='text',view='front',p=[XL,r(CS_H-STROKE)],s='保持具（左 x=92.0→110.9）',dx=4,dy=14,color=HD))
items.append(dict(t='text',view='front',p=[89.5,262],s='架台',dx=-4,anchor='end',color=FR))
# 側面のリンク（収納・使用、左右）
for s,col in ((0,'#2C6FB0'),(1,'#C0392B')):
    for Od,w1 in ((DL,2.2),(DR,1.4)):
        _,A,B,C=pose(Od,s)
        items.append(dict(t='line',view='side',p=[[Od,268],[r(A[0]),r(A[1])]],color=col,w=w1))
        items.append(dict(t='line',view='side',p=[[r(B[0]),268],[r(C[0]),r(C[1])]],color=col,w=w1*0.6,dash=True))
L,R_=spans['左'],spans['右']
notes=[
 'STEP4 4-3（架台の取付け）：梁の内側面（梁1 x=89.5・梁2 x=170、h=254.5〜270）に架台（灰、仮厚1）を付け、Oの軸受け・レール（h≈262）・ねじ・モーター（橙、仮6×6×8）を載せる。Oとねじの受けの水平力は架台の中で打ち消し合う（K055）。',
 'リンク面は梁の側面のそば（左x=92.0・右x=168.0、仮）。Oの張り出しは左2.5・右2.0。CSP側面までは保持具（緑）で渡す：左18.9・右0（wR=0）。C点には鉛直荷重のみ（LC2で片側173N）。',
 '架台の長さ：左 d=%.1f〜%.1f（%.1f）、右 d=%.1f〜%.1f（%.1f）。すべて梁下面h=254.5より上。架台は梁の側面に見える。'%(L[0],L[1],L[1]-L[0],R_[0],R_[1],R_[1]-R_[0]),
 '前提値はすべて仮（a=50、O・Bの高さ268、wR=0、架台厚1、レール・ねじh≈262、モーター寸法）。梁へのねじ（M6まで、A00-005・A04-009）の本数・位置は荷重を出してから決める。',
]
ov=dict(title_note=notes,legend=C0['legend']+[
  dict(text='灰：架台（梁の内側面）',color=FR,kind='band'),
  dict(text='黒：Oの軸受け・レール（ねじ）',color='#111',kind='line'),
  dict(text='緑：保持具（リンク面→CSP側面）',color=HD,kind='line'),
  dict(text='橙：モーター（仮）',color=MT,kind='band'),
  dict(text='青／赤：リンク（収納／使用）、破線：リンク面',color=LK,kind='line')],
  src=['K046','K049','K051','K055','A00-005','A01-001','A03-004','D01-001','D01-004','D04-002'],items=items)
json.dump(ov,open(OUTJ,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
subprocess.run(['python3',SAN,'--zuban','K056','--title','梁への架台の取付け','-o',OUTS,OUTJ],check=True)
print(TS,spans)
