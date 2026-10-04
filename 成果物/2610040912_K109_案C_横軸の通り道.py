#!/usr/bin/env python3
# K109 案C：モーター1台から左右2本の台形ねじへ回転を分けるときの、横軸（x方向）の通り道。sanmen.py の重ね描きJSONを作る
# 入力：A06-001（a=50、φ7.0〜57.4°、O 左d=52・右d=70、O h=265）、K100（ねじ中心 h=257.4、Oの受け金具）、A03-004（CSP収納の外形）、A00-006（配光118°）
import json, math
t59=math.tan(math.radians(59)); Rc=lambda h:5.7+(270-h)*t59
a=50.0; hw=2.015
def env(O):
    top={}; bot={}
    for i in range(1001):
        ph=math.radians(7.0+(57.4-7.0)*i/1000)
        Bd=O+2*a*math.cos(ph); Ch=265-2*a*math.sin(ph); Ad,Ah=O+a*math.cos(ph),265-a*math.sin(ph)
        for (p,q) in (((Bd,265),(O,Ch)),((O,265),(Ad,Ah))):
            for k in range(201):
                d=p[0]+(q[0]-p[0])*k/200; h=p[1]+(q[1]-p[1])*k/200; key=round(d*2)/2
                top[key]=max(top.get(key,-1),h+hw); bot[key]=min(bot.get(key,999),h-hw)
    ks=sorted(top); return ks,top,bot
def csp_top(d):   # 収納時CSPの外形の上側（P0→P2→P3）。CSPは鉛直に動くので掃引の上端はこれ
    P0,P2,P3=(47.77,249.47),(54.68,265.0),(74.23,256.3)
    if d<P0[0] or d>P3[0]: return None
    if d<=P2[0]: return P0[1]+(P2[1]-P0[1])*(d-P0[0])/(P2[0]-P0[0])
    return P2[1]+(P3[1]-P2[1])*(d-P2[0])/(P3[0]-P2[0])
out={}
for nm,O in (('L',52.0),('R',70.0)):
    ks,top,bot=env(O); out[nm]=(ks,top,bot); out[nm+'poly']=[[k,top[k]] for k in ks]+[[k,bot[k]] for k in reversed(ks)]
free=[]
for i in range(92,331):
    d=i/2
    hlo=max([out[n][1].get(d,0) for n in ('L','R')]+[254.5])
    ct=csp_top(d)
    if ct is not None: hlo=max(hlo,ct)
    for Ld in (130,175):
        dd=abs(d-Ld)
        if dd<=5.7: hlo=999
        elif dd<Rc(254.5): hlo=max(hlo,270-(dd-5.7)/t59)
    if 50.5<=d<=53.5 or 68.5<=d<=71.5: hlo=999
    free.append((d,hlo))
Y='#E0A100'; B='#2C6FB0'; P='#9b6fc0'; G='#1F7A4D'
it=[]
for d in (130,175):
    it.append({"t":"poly","view":"side","p":[[d-5.7,270],[d+5.7,270],[d+Rc(254.5),254.5],[d-Rc(254.5),254.5]],"color":Y,"fill":Y,"op":0.12,"w":1.0,"dash":False})
it.append({"t":"poly","view":"side","p":out['Lpoly'],"color":B,"fill":B,"op":0.15,"w":0.8,"dash":True})
it.append({"t":"poly","view":"side","p":out['Rpoly'],"color":P,"fill":P,"op":0.15,"w":0.8,"dash":True})
segs=[]; cur=[]
for d,h in free:
    if h<268: cur.append((d,h))
    elif cur: segs.append(cur); cur=[]
if cur: segs.append(cur)
for s in segs:
    it.append({"t":"poly","view":"side","p":[[d,270] for d,_ in s]+[[d,h] for d,h in reversed(s)],"color":G,"fill":G,"op":0.35,"w":1.0,"dash":True})
for (x0,x1,d0,d1,c) in ((92.3,93.7,107,160.5,B),(165.8,167.2,125,178.5,P)):
    it.append({"t":"box3","p":[x0,x1,d0,d1,256.7,258.1],"color":c,"fill":c,"op":0.7,"w":1.0,"dash":True})
it.append({"t":"line","view":"side","p":[[45.5,257.4],[200,257.4]],"color":"#c0392b","w":1.0,"dash":True})
it.append({"t":"text","view":"side","p":[48,252],"s":"(窓 d=46〜50)","color":G,"anchor":"start"})
it.append({"t":"line","view":"plan","p":[[45.5,165],[305.5,165]],"color":"#c0392b","w":1.2,"dash":True})
segtxt='、'.join(f'd={s[0][0]:.1f}〜{s[-1][0]:.1f}（最低 h={min(h for _,h in s):.1f}）' for s in segs)
J={"title_note":["案C：モーター1台から左右2本の台形ねじへ回転を分けるとき、左右を結ぶ横軸（x方向にまっすぐ）が通れる範囲を側面で見る。機構はK100（Δd=18、φ7.0〜57.4°）のまま",
 "横軸は全幅を渡るので、左右のリンクの掃引（収納〜使用の全域）、CSPの掃引、Oの受け金具、収納時の配光のどれにも入れない",
 "緑：横軸が通れる範囲（h=270まで、余裕寸法なし）："+segtxt,
 "ねじの中心 h=257.4（赤破線）と同じ高さで通れるのは d=46〜50 の窓だけ（梁エリア前端45.5とCSP収納の前上がりの面の間）。他の範囲はh=263以上で、ねじとの間に高さの段差が要る",
 "d=46〜50 の窓：ねじは左d=107→48・右d=125→48まで延長。C点のピン・保持具・C′保持具との干渉、余裕寸法は未確認"],
 "legend":[{"text":"青：左リンクの掃引（長リンク・短リンク）","color":B,"dash":True,"kind":"band"},{"text":"紫：右リンクの掃引","color":P,"dash":True,"kind":"band"},
           {"text":"緑：横軸が通れる範囲","color":G,"dash":True,"kind":"band"},{"text":"黄：配光118°","color":Y,"dash":False,"kind":"band"},
           {"text":"赤 破線：ねじの中心 h=257.4（側面）／d_max=165（平面）","color":"#c0392b","dash":True,"kind":"line"}],
 "src":["K100、K105、K108、A03-004、A06-001、A06-004、A00-006"],"items":it}
json.dump(J,open('k109.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(segtxt)
