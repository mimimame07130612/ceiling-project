# K052 左右同期の案（STEP4 4-2→4-4入口、姿勢保持案1・配置β、収納時）
# 収納時に見える同期部材の位置を三面図に重ねて比べる。比較の観点：①収納時に何がどこに見えるか ②片側が故障したとき何が起きるか
# 案S1：CSP保持具（C–C′をつなぐ枠）が同期を兼ねる。案S2：O軸連結（左Oからx方向の軸を右へ渡し、右側はクランク＋平行リンクでO′A′へ）。
# 案S3：左右別モーター＋制御で同期（部材なし、モーター2台）。参考：K051のB–B′直結（収納時に目立つため不採用）。
# 前提値（仮）：a=50、O・O′・レールh=268、左 x=110.9・O/C d=52.73、右 x=168.0・O′/C′ d=70.73、CSP収納 d1=48.5・最下点243.77、wR=0、
#   S2のクランク長8（仮）、S3のモーター外形6×6×6（仮、位置はレールのLP側端の仮置き）。部品は線または仮外形。
import json, math, subprocess, glob
TS=subprocess.run(['date','+%y%m%d%H%M'],capture_output=True,text=True,env={'TZ':'Asia/Tokyo'}).stdout.strip()
NAME='K052_左右同期の案'
CSP=sorted(glob.glob('*_csp.py'))[-1]; SAN=sorted(glob.glob('*_sanmen.py'))[-1]
OUTJ='/mnt/user-data/outputs/%s_%s.json'%(TS,NAME); OUTS='/mnt/user-data/outputs/%s_%s.svg'%(TS,NAME)
a=50.0; CS_H=255.885; STROKE=72.16; t0=268-CS_H
XL,XR=110.9,168.0; DL,DR=52.73,70.73; RK=8.0
def pose(Od,s):
    oc=t0+STROKE*s; C=(Od,268-oc); ph=math.asin(oc/(2*a)); B=(Od+2*a*math.cos(ph),268.0); A=((B[0]+C[0])/2,(B[1]+C[1])/2)
    return ph,A,B,C
subprocess.run(['python3',CSP,'json','-o','/tmp/c52.json','--pose','収納,139.45,48.5,243.77'],check=True,capture_output=True)
C0=json.load(open('/tmp/c52.json',encoding='utf-8'))
items=list(C0['items']); r=lambda v:round(v,2)
GRY='#888888'
# 共通：収納時のリンク（灰）
for Od,x in ((DL,XL),(DR,XR)):
    _,A,B,C=pose(Od,0)
    items.append(dict(t='line',view='side',p=[[Od,268],[r(A[0]),r(A[1])]],color=GRY,w=1.6))
    items.append(dict(t='line',view='side',p=[[r(B[0]),268],[r(C[0]),r(C[1])]],color=GRY,w=1.0,dash=True))
    items.append(dict(t='line',view='plan',p=[[x,Od],[x,r(B[0])]],color=GRY,w=2.0))
# 参考：K051 直結部材（不採用）
bl=pose(DL,0)[2][0]
items.append(dict(t='line',view='plan',p=[[XL,r(bl)],[XR,r(bl+18)]],color='#bbbbbb',w=1.6,dash=True))
items.append(dict(t='text',view='plan',p=[XR,r(bl+18)],s='参考：K051直結（不採用）',dx=6,dy=4,color='#999999'))
# S1 保持具の枠（緑）
G='#1D9E75'
items.append(dict(t='poly',view='plan',p=[[XL,DL],[XR,DL],[XR,DR],[XL,DR]],color=G,fill=G,op=0.15,w=2.0))
items.append(dict(t='text',view='plan',p=[XL,DL],s='S1 保持具の枠',dx=-4,dy=12,anchor='end',color=G))
items.append(dict(t='line',view='front',p=[[XL,CS_H],[XR,CS_H]],color=G,w=2.6))
items.append(dict(t='text',view='front',p=[XL,CS_H],s='S1 枠 h=255.9',dx=-4,dy=4,anchor='end',color=G))
items.append(dict(t='line',view='side',p=[[DL,CS_H],[DR,CS_H]],color=G,w=3.0))
# S2 O軸連結（紫）
V='#6A5FD0'
_,AL,_,_=pose(DL,0); ux,uy=(AL[0]-DL)/a,(AL[1]-268)/a
K=(DL+RK*ux,268+RK*uy); K2=(K[0]+18,K[1])
items.append(dict(t='line',view='plan',p=[[XL,DL],[XR,DL]],color=V,w=3.0))
items.append(dict(t='text',view='plan',p=[XR,DL],s='S2 O軸 d=52.7',dx=6,dy=-2,color=V))
items.append(dict(t='line',view='plan',p=[[XR,DL],[XR,r(K2[0])]],color=V,w=3.0))
items.append(dict(t='line',view='front',p=[[XL,268],[XR,268]],color=V,w=2.6))
items.append(dict(t='text',view='front',p=[XR,268],s='S2 O軸 h=268',dx=4,dy=12,color=V))
items.append(dict(t='line',view='side',p=[[DL,268],[r(K[0]),r(K[1])],[r(K2[0]),r(K2[1])],[DR,268]],color=V,w=2.0))
items.append(dict(t='text',view='side',p=[r(K2[0]),r(K2[1])],s='S2 クランク＋平行リンク（右）',dx=4,dy=14,color=V))
# S3 モーター（橙）
O_='#D85A30'
for x,Od in ((XL,DL),(XR,DR)):
    b=pose(Od,0)[2][0]+6
    items.append(dict(t='rect',view='plan',p=[r(x-3),r(b),r(x+3),r(b+6)],color=O_,fill=O_,op=0.35,w=1.2))
    items.append(dict(t='rect',view='front',p=[r(x-3),262,r(x+3),268],color=O_,fill=O_,op=0.35,w=1.2))
items.append(dict(t='text',view='plan',p=[XR+3,r(pose(DR,0)[2][0]+12)],s='S3 モーター×2（仮置き）',dx=4,dy=4,color=O_))
# CSPの平面外形（収納）との重なり確認
cspd=(48.5,74.96)
notes=[
 'STEP4 左右同期の案（収納時）：灰＝収納時のリンク。緑S1＝CSP保持具の枠（C–C′をつなぐ、h=255.9）。紫S2＝O軸連結（左Oからx方向の軸、右はクランク長8＋平行リンクでO′A′へ、h≒267〜268）。橙S3＝左右別モーター（仮置き）。',
 '平面図でCSPの収納外形は x=110.9〜168.0・d=48.5〜74.96。S1の枠（d=52.7〜70.7）とS2の軸（d=52.7）は外形の内側。S2右の平行リンクの端（d=%.1f）は外形から%.1f出る（クランク長%.0fの場合。4.2以下なら内側）。'%(K2[0],K2[0]-74.96,RK),
 '前提値はすべて仮（a=50、O・O′・レールh=268、wR=0、クランク長8、モーター6×6×6）。駆動部（モーター等）はどの案にも要り、位置は4-4で決める。',
 '片側故障時（概念）：S1＝同期力がCSP・枠を通る。S2＝軸が切れてもCSP・枠で高さはそろう（S1に戻る）。S3＝片側だけ動くとCSP・枠に無理な力、検知と停止が要る（S3 a）。',
]
ov=dict(title_note=notes,legend=C0['legend']+[
  dict(text='灰：収納時のリンク（左右）',color=GRY,kind='line'),
  dict(text='緑：S1 保持具の枠',color=G,kind='band'),
  dict(text='紫：S2 O軸連結',color=V,kind='line'),
  dict(text='橙：S3 左右別モーター（仮置き）',color=O_,kind='band')],
  src=['K048','K049','K051','A01-001','A02-002','A03-004','D01-001','部屋.xlsx'],items=items)
json.dump(ov,open(OUTJ,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
subprocess.run(['python3',SAN,'--zuban','K052','--title','左右同期の案（収納時）','-o',OUTS,OUTJ],check=True)
print(TS,'K',K,'K2',K2)
# 使用側の平行リンク位置も確認
for s in (0,0.5,1):
    _,A,_,_=pose(DL,s); ux,uy=(A[0]-DL)/a,(A[1]-268)/a; print(s,(round(DL+RK*ux,1),round(268+RK*uy,1)))
