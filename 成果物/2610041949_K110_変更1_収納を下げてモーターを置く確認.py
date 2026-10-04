#!/usr/bin/env python3
# K110 変更①：収納時のCSPを下げてモーター（90角）を x≈130・d=46〜56・h=260〜270 に置くときの確認。sanmen.py の重ね描きJSONを作る
# 入力：依頼主の変更① の位置、A03-004（CSP収納の外形 P0〜P3）、A00-006（配光118°）、照明1列目 d=130・x=129.65（部屋.xlsx）
import json, math
t=math.tan(math.radians(59)); Rc=lambda h:5.7+(270-h)*t
Y='#E0A100'; M='#E6A23C'
def top(d,D):
    P0,P2,P3=(47.77,249.47-D),(54.68,265-D),(74.23,256.3-D)
    if d<=P2[0]: return P0[1]+(P2[1]-P0[1])*(d-P0[0])/(P2[0]-P0[0])
    return P2[1]+(P3[1]-P2[1])*(d-P2[0])/(P3[0]-P2[0])
# 配光でCSPを下げられる限度：P1(d=67.32) が照明1列目(d=130)の配光に入らない
Dmax = (240.77) - (270-(130-67.32-5.7)/t)
it=[]
for d in (130,175):
    it.append({"t":"poly","view":"side","p":[[d-5.7,270],[d+5.7,270],[d+Rc(234),234],[d-Rc(234),234]],"color":Y,"fill":Y,"op":0.12,"w":1.0,"dash":False})
it.append({"t":"poly","view":"front","p":[[129.65-5.7,270],[129.65+5.7,270],[129.65+Rc(234),234],[129.65-Rc(234),234]],"color":Y,"fill":Y,"op":0.10,"w":1.0,"dash":False})
it.append({"t":"box3","p":[125.5,134.5,46,56,260,270],"color":M,"fill":M,"op":0.55,"w":1.2,"dash":True,"label":"(モーター90角)"})
it.append({"t":"text","view":"side","p":[48,272],"s":"(モーター d=46〜56 h=260〜270)","color":"#a0661a","anchor":"start"})
rows=[]
for D in (0, round(Dmax,2), 6.4):
    need=max(top(46+i*0.01,D) for i in range(1001) if 46+i*0.01>=47.77)
    rows.append(f'Δ={D}：CSP上面の最高（d=46〜56の範囲） h={need:.2f}、P1と配光の余裕 {130-Rc(240.77-D)-67.32:.2f}')
J={"title_note":["変更①の確認：収納時のCSPを下げ（Δ）、x≈130・d=46〜56・h=260〜270 にモーター（90角）を置く。CSPの収納姿勢はチルト24°のまま（A02-003）",
 f"収納時のCSPを下げられる限度：Δ≦{Dmax:.2f}（P1 d=67.32 が照明1列目 d=130 の配光118°に入る。A00-006）",
 "d=46〜56 のCSP上面はP2（d=54.68）が最高。モーター下面 h=260 に対して Δ=5.0 ではすき間0（余裕寸法cなし）、c=2 を取るには Δ≧7.0 が要り、限度を超える",
 " ／ ".join(rows)],
 "legend":[{"text":"黄：配光118°（A00-006）","color":Y,"dash":False,"kind":"band"},{"text":"橙 破線：モーター90角（変更①の位置）","color":M,"dash":True,"kind":"band"}],
 "src":["A03-004、A02-003、A00-006、部屋.xlsx、依頼主の変更①"],"items":it}
json.dump(J,open('k110.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(Dmax); [print(r) for r in rows]
