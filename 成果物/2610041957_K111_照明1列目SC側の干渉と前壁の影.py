#!/usr/bin/env python3
# K111 照明1列目のSC側の配光にCSP（収納を7.0下げた場合）が入るとき、前壁（d=0）にできる影。sanmen.py の重ね描きJSONを作る
# 入力：照明 x=129.65・220.65、d=130、h=270（部屋.xlsx、A02-001）、A03-004（CSP外形）、前天井 h=250（d<45.5、部屋.xlsx）、SCケース d=20.5〜33.9・h=236.5〜250
import json, math
D=7.0; S=(129.65,130.0,270.0)
P=[(47.77,249.47-D),(67.32,240.77-D),(54.68,265-D),(74.23,256.3-D)]
def proj(x,d,h):
    t=(0-S[1])/(d-S[1]); return (S[0]+t*(x-S[0]), S[2]+t*(h-S[2]))
pts=[proj(x,d,h) for x in (104.6,161.7) for (d,h) in P]
def hull(p):
    p=sorted(set(p))
    def cr(o,a,b): return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    lo=[];up=[]
    for q in p:
        while len(lo)>=2 and cr(lo[-2],lo[-1],q)<=0: lo.pop()
        lo.append(q)
    for q in reversed(p):
        while len(up)>=2 and cr(up[-2],up[-1],q)<=0: up.pop()
        up.append(q)
    return lo[:-1]+up[:-1]
H=hull(pts)
k=33.9/130; step_h = (236.5-k*270)/(1-k)   # SCケース（d=20.5〜33.9、h=236.5〜250、x=17.95〜274.05）の前下の角で既に光が届かない高さ（前天井の段 h=239.2 より低い）
xs=[q[0] for q in H]; hs=[q[1] for q in H]
print('shadow x %.1f〜%.1f, h %.1f〜%.1f, step %.1f'%(min(xs),max(xs),min(hs),max(hs),step_h))
Y='#E0A100'; R='#c0392b'
it=[{"t":"poly","view":"front","p":[list(q) for q in H],"color":R,"fill":R,"op":0.25,"w":1.2,"dash":True}]
it.append({"t":"line","view":"front","p":[[45.5,step_h],[305.5,step_h]],"color":"#555","w":1.0,"dash":True})
it.append({"t":"text","view":"front","p":[250,step_h+2],"s":"(これより上はSCケースで元から影 h=%.1f)"%step_h,"color":"#555","anchor":"middle"})
for (d,h) in P:
    q=proj(133.15,d,h)
    if q[1] < step_h: it.append({"t":"line","view":"side","p":[[130,270],[0,q[1]]],"color":R,"w":0.8,"dash":True})
    else:
        dd=33.9; hh=q[1]+(dd/130)*(270-q[1]); it.append({"t":"line","view":"side","p":[[130,270],[dd,hh]],"color":R,"w":0.8,"dash":True})
it.append({"t":"poly","view":"side","p":[[130-5.7,270],[130+5.7,270],[130+5.7+(270-233)*math.tan(math.radians(59)),233],[130-5.7-(270-233)*math.tan(math.radians(59)),233]],"color":Y,"fill":Y,"op":0.12,"w":1.0,"dash":False})
J={"title_note":["前提の変更案の確認：照明1列目（d=130）の配光のうちSC側への干渉を許すとき、その影がどこに落ちるか。CSPは収納を7.0下げた場合（変更①でモーターとの間にc=2を取る量）",
 "影は照明 x=129.65 の発光面の中心から見た幾何の影（本影の目安。発光面φ11.4による半影は描いていない）",
 "前壁（d=0）の影：x=%.1f〜%.1f、h=%.1f〜%.1f。そのうち h=%.1f より上はSCケースで元から光が届かないので、新しくできる影は h=%.1f〜%.1f。SCの幕面（h=36.5〜161）にはかからない"%(min(xs),max(xs),min(hs),max(hs),step_h,min(hs),step_h),
 "同じ列のもう1灯（x=220.65）の配光にはCSPは入らないので、この範囲もその灯と2・3列目からは照らされる（真っ暗にはならない）"],
 "legend":[{"text":"赤 破線：前壁の影（照明 x=129.65 から）","color":R,"dash":True,"kind":"band"},{"text":"黄：照明1列目の配光118°","color":Y,"dash":False,"kind":"band"}],
 "src":["部屋.xlsx、A02-001、A03-004、A00-006、K110"],"items":it}
json.dump(J,open('k111.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
