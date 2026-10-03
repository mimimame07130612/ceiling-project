# K051 左右1組ずつの二重スコットラッセルと同期部材の通り道（STEP4 4-2、姿勢保持案1 配置β）
# 左側 O-A-B-C（x=110.9、O・C d=52.73）、右側 O′-A′-B′-C′（x=168.0、O′・C′ d=70.73）。BとB′は同時に動く前提。
# 平面図・正面図で、BとB′を直につなぐ部材（仮）が通る範囲と、照明器具・配光・CSPとの位置関係を見る。
# 前提値（仮設定）：a=50、O・O′・レールh=268、C収納h=255.885→使用183.725、CSP d1=48.5（収納最下点243.77／使用171.61）、wR=0、部品は太さ0
# 入力：K046・K049・K050、A01-001、A01-003、A02-002、A03-004、D01-001、部屋.xlsx（照明 x=129.65/220.65、d=130/175/220、φ11.4）、配光118°（K039と同じ扱い）
import json, math, subprocess, glob
TS=subprocess.run(['date','+%y%m%d%H%M'],capture_output=True,text=True,env={'TZ':'Asia/Tokyo'}).stdout.strip()
NAME='K051_左右1組ずつの配置と同期部材'
CSP=sorted(glob.glob('*_csp.py'))[-1]; SAN=sorted(glob.glob('*_sanmen.py'))[-1]
OUTJ='/mnt/user-data/outputs/%s_%s.json'%(TS,NAME); OUTS='/mnt/user-data/outputs/%s_%s.svg'%(TS,NAME)
a=50.0; CS_H=255.885; STROKE=72.16; t0=268-CS_H
XL,XR=110.9,168.0; DL,DR=52.73,70.73
def pose(Od,s):
    oc=t0+STROKE*s; C=(Od,268-oc); ph=math.asin(oc/(2*a)); B=(Od+2*a*math.cos(ph),268.0); A=((B[0]+C[0])/2,(B[1]+C[1])/2)
    return ph,A,B,C
subprocess.run(['python3',CSP,'json','-o','/tmp/c51.json','--pose','収納,139.45,48.5,243.77','--pose','使用,139.45,48.5,171.61'],check=True,capture_output=True)
C0=json.load(open('/tmp/c51.json',encoding='utf-8'))
items=[it for it in C0['items']]
r=lambda v:round(v,2)
# ---- 側面図 ----
for s,col in ((0,'#2C6FB0'),(1,'#C0392B')):
    for Od,w1,nm in ((DL,2.6,'左'),(DR,1.6,'右')):
        _,A,B,C=pose(Od,s)
        items.append(dict(t='line',view='side',p=[[Od,268],[r(A[0]),r(A[1])]],color=col,w=w1))
        items.append(dict(t='line',view='side',p=[[r(B[0]),268],[r(C[0]),r(C[1])]],color=col,w=w1*0.7,dash=True))
items.append(dict(t='text',view='side',p=[DL,268],s='太＝左(O…C) 細＝右(O′…C′)',dx=-4,dy=-10,anchor='end',color='#111'))
# ---- 平面図・正面図 ----
LED=[(x,d) for x in (129.65,220.65) for d in (130,175,220)]
RB=5.7+2*math.tan(math.radians(59))   # h=268での配光半径
for (x,d) in LED:
    if x<200:
        items.append(dict(t='circle',view='plan',p=[x,d],r=r(RB),color='#BA7517',w=0.8,dash=True))
for s,col,tag in ((0,'#2C6FB0','収納'),(1,'#C0392B','使用')):
    PL=pose(DL,s); PR=pose(DR,s)
    for P,x,Od in ((PL,XL,DL),(PR,XR,DR)):
        dmin=min(Od,P[1][0],P[2][0],P[3][0]); dmax=max(Od,P[1][0],P[2][0],P[3][0])
        items.append(dict(t='line',view='plan',p=[[x,r(dmin)],[x,r(dmax)]],color=col,w=3.0))
        items.append(dict(t='pt',view='plan',p=[x,r(P[2][0])],color=col,r=3.2))
    items.append(dict(t='line',view='plan',p=[[XL,r(PL[2][0])],[XR,r(PR[2][0])]],color=col,w=2.4))
    items.append(dict(t='text',view='plan',p=[XR,r(PR[2][0])],s='B–B′ 直結(%s)'%tag,dx=6,dy=4,color=col))
# 通過範囲（平行四辺形）
b0=pose(DL,1)[2][0]; b1=pose(DL,0)[2][0]
items.append(dict(t='poly',view='plan',p=[[XL,r(b0)],[XR,r(b0+18)],[XR,r(b1+18)],[XL,r(b1)]],color='#6A5FD0',fill='#6A5FD0',op=0.12,w=0.8))
items.append(dict(t='text',view='plan',p=[XL,r((b0+b1)/2)],s='直結部材の通過範囲',dx=-4,anchor='end',color='#6A5FD0'))
# 正面図：同期部材
items.append(dict(t='line',view='front',p=[[XL,268],[XR,268]],color='#6A5FD0',w=2.4))
items.append(dict(t='text',view='front',p=[XR,268],s='直結部材 h=268',dx=4,dy=12,color='#6A5FD0'))
for x,col,nm in ((XL,'#2C6FB0','左 x=110.9'),(XR,'#C0392B','右 x=168.0')):
    items.append(dict(t='line',view='front',p=[[x,172],[x,268]],color=col,w=1.2,dash=True))
    items.append(dict(t='text',view='front',p=[x,210],s=nm,dx=(-4 if x<140 else 4),anchor=('end' if x<140 else 'start'),color=col))
# 数値（照明との関係）
def xing(dL):   # 直結部材が照明中心x=129.65を通るd
    return dL+18*(129.65-XL)/(XR-XL)
stow=xing(b1); use=xing(b0)
dist_stow=min(abs(stow-130),abs(stow-175))
notes=[
 'STEP4 4-2（姿勢保持 案1・配置β、左右1組ずつ）：左 O-A-B-C（x=110.9、O・C d=52.73）、右 O′-A′-B′-C′（x=168.0、O′・C′ d=70.73）。Δd=18。青収納・赤使用。前提値はすべて仮設定（a=50、O・O′・レールh=268、wR=0、部品は太さ0）。',
 '左右の機構は別のx面にあるので、側面図で交差していたロッドBCとO′A′はぶつからない。片側のリンクは2本（OA・ロッド）で、wL・wRの使い方はこれまでと同じ。',
 '同期の一例として、BとB′を直につなぐ部材（h=268、紫）の通り道を示した。平面図ではd方向に18ずれた斜めの部材になり、B(左)d=%.1f〜%.1fの間を動く。'%(b0,b1),
 '照明（x=129.65）の真下を通るdは 使用%.1f〜収納%.1f。d=130の照明の下を動作中に横切る（h=268＝器具面の2下、配光半径%.1fの中）。収納時は照明中心から%.1f離れる。'%(use,stow,RB,dist_stow),
]
ov=dict(title_note=notes,legend=C0['legend']+[
  dict(text='青／赤：リンク・Bの位置（収納／使用）。平面図の太線＝リンクがd方向に占める範囲',color='#2C6FB0',kind='line'),
  dict(text='紫：B–B′直結部材（同期の一例、仮）とその通過範囲',color='#6A5FD0',kind='band'),
  dict(text='黄破線円：h=268での配光の広がり（左列の照明）',color='#BA7517',dash=True,kind='ring')],
  src=['K046','K049','K050','A01-001','A01-003','A02-002','A03-004','D01-001','部屋.xlsx'],items=items)
json.dump(ov,open(OUTJ,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
subprocess.run(['python3',SAN,'--zuban','K051','--title','左右1組ずつの配置と同期部材','-o',OUTS,OUTJ],check=True)
print(TS, 'B左', b0, b1, '照明下', use, stow, 'RB', RB)
