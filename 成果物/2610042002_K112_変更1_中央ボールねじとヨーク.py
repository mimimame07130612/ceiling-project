#!/usr/bin/env python3
# K112 変更①の配置：中央のボールねじ1本（モーター1台）でヨーク（横棒＋左右の脚）を動かし、左右のBを同時に押す。sanmen.py の重ね描きJSONを作る
# 前提（このセッションで依頼主が変更・仮）：収納を7.0下げる（C収納 h=245.885）、照明1列目のSC側（d≦124.3）の配光干渉は許容、使用時φ=70°（K103の③）
# 据え置き：O h=265、O 左d=52・右d=70（Δd=18、配置β）、C使用 h=180.725、リンク面 左95.55・右163.95（A06-004）、K100のガイド・Oの受け金具の形
import json, math
Oh, Cs, Cu, phu = 265.0, 245.885, 180.725, 70.0
ds, du = Oh-Cs, Oh-Cu
L = du/math.sin(math.radians(phu)); bs = math.sqrt(L*L-ds*ds); bu = L*math.cos(math.radians(phu)); trav = bs-bu
phs = math.degrees(math.asin(ds/L))
OL, OR = 52.0, 70.0
BLs, BLu, BRs, BRu = OL+bs, OL+bu, OR+bs, OR+bu
NS = 120.0; NU = NS-trav                      # ナット中心（収納・使用）
offL, offR = BLs-NS, BRs-NS
t59 = math.tan(math.radians(59)); Rc = lambda h: 5.7+(270-h)*t59
B, G, M, K, Y, R = '#2C6FB0', '#2E9E6B', '#E6A23C', '#5F5E5A', '#E0A100', '#c0392b'
it = []
def bx(p, c, op=0.5, lab=None, dash=True):
    o = {"t":"box3","p":p,"color":c,"fill":c,"op":op,"w":1.0,"dash":dash}
    if lab: o["label"] = lab
    return o
# 配光：1列目はLP側だけ（SC側は許容）、2列目は全周
it.append({"t":"poly","view":"side","p":[[130-5.7,270],[130+5.7,270],[130+5.7+Rc(254.5)-5.7,254.5],[130,254.5]],"color":Y,"fill":Y,"op":0.15,"w":1.0,"dash":False})
it.append({"t":"poly","view":"side","p":[[175-5.7,270],[175+5.7,270],[175+Rc(254.5),254.5],[175-Rc(254.5),254.5]],"color":Y,"fill":Y,"op":0.15,"w":1.0,"dash":False})
it.append(bx([125.5,134.5,46,56,260.5,269.5], M, 0.6, '(モーター90角)'))
it.append(bx([129.4,130.6,56,124,264.4,265.6], '#555', 0.8))
for n, c in ((NS,B),(NU,G)):
    it.append(bx([127,133,n-2.5,n+2.5,262,268], c, 0.6))
    it.append(bx([94.3,165.2,n-1,n+1,267.5,269.5], c, 0.45))                 # 横棒
    it.append(bx([94.3,96.8,n,n+offL,267.5,269.5], c, 0.45))                  # 左の脚
    it.append(bx([162.7,165.2,n,n+offR,267.5,269.5], c, 0.45))                # 右の脚
for (x0,x1,bs_,bu_) in ((90.3,92.1,BLs,BLu),(167.4,169.2,BRs,BRu)):
    it.append(bx([x0,x1,bu_-6.3,bs_+6.3,264,266], '#555', 0.6))              # レール（ブロック半長3.7＋余り2.6）
it.append(bx([90.3,100.3,50.5,53.5,266.5,269.5], K, 0.6))
it.append(bx([159.2,169.2,68.5,71.5,266.5,269.5], R, 0.6, '(右Oの受け金具：右の脚と干渉)'))
for O, Bs_, Bu_ in ((OL,BLs,BLu),(OR,BRs,BRu)):
    for (Bd, ph, c) in ((Bs_, phs, B), (Bu_, phu, G)):
        Ch = Oh-L*math.sin(math.radians(ph)); Ad, Ah = O+L/2*math.cos(math.radians(ph)), Oh-L/2*math.sin(math.radians(ph))
        it.append({"t":"line","view":"side","p":[[Bd,Oh],[O,Ch]],"color":c,"w":1.4,"dash":True})
        it.append({"t":"line","view":"side","p":[[O,Oh],[Ad,Ah]],"color":c,"w":1.4,"dash":True})
it.append({"t":"line","view":"plan","p":[[45.5,165],[305.5,165]],"color":R,"w":1.2,"dash":True})
dmax = BRs+3.7+2.6
J={"title_note":[
 f"変更①の配置（仮）：収納を7.0下げ、中央のボールねじ1本のナットでヨーク（横棒＋左右の脚、h=267.5〜269.5）を動かし左右のBを同時に押す。φ収納{phs:.1f}°〜使用70°、リンク長2a={L:.2f}",
 f"B：左 {BLu:.2f}〜{BLs:.2f}、右 {BRu:.2f}〜{BRs:.2f}（動く量 {trav:.2f}）。ナット中心 {NU:.2f}〜{NS:.2f}。脚の長さ 左{offL:.2f}・右{offR:.2f}。機構の端（右レール端）d={dmax:.2f}",
 f"ナット使用位置の下端 {NU-2.5:.2f}：モーター（d≦56）との間 {NU-2.5-56:.2f} にカップリング・ねじの支持が要る（入るかは未確認）。ねじ端 d=124（1列目の発光面 d=124.3 の手前）",
 f"干渉：右の脚は使用位置で d={NU:.2f}〜{NU+offR:.2f} を通り、右Oの受け金具（d=68.5〜71.5、h=266.5〜269.5の上板）と当たる。左の脚は左O（d=50.5〜53.5）に届かない"],
 "legend":[{"text":"青：収納時","color":B,"dash":True,"kind":"line"},{"text":"緑：使用時","color":G,"dash":True,"kind":"line"},
           {"text":"橙：モーター90角（変更①）","color":M,"dash":True,"kind":"band"},{"text":"黄：配光（1列目はLP側のみ、2列目は全周）","color":Y,"dash":False,"kind":"band"},
           {"text":"赤：干渉する部品／d_max=165","color":R,"dash":True,"kind":"band"}],
 "src":["依頼主の変更①・配光の許容（このセッション）、K103、K108、K110、K111、A06-001、A06-004、K100"],"items":it}
json.dump(J,open('k112.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(f'L={L:.2f} phs={phs:.2f} BL {BLu:.2f}-{BLs:.2f} BR {BRu:.2f}-{BRs:.2f} trav {trav:.2f} nut {NU:.2f}-{NS} offL {offL:.2f} offR {offR:.2f} dmax {dmax:.2f}')
