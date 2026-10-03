# K093 一時的な傾きでのCSPと周囲のすき間、こじれの力によるリンクの応力（STEP4 4-3、K092の続き）
# (1) 収納時のCSP外形（側面、K062の外形を d−0.73・h−3 平行移動）を、先に止まった側のCまわりに傾け、
#     掘込の前の壁（d=45.5、h≥250）・部屋の天井（h=250、d<45.5）・掘込面（h=270）とのすき間を求める。
# (2) こじれの力（Cに d方向の力）によるリンクの応力：K092と同じ片側の立体骨組みで、Cに d方向 1N を与えたときの最大応力
#     （角パイプ25×25×2.3、2方向の曲げと軸力を足す安全側）から換算。
import math, csv, subprocess
TS=subprocess.run(['date','+%y%m%d%H%M'],capture_output=True,text=True,env={'TZ':'Asia/Tokyo'}).stdout.strip()
P=[(47.77,249.47),(67.32,240.77),(74.23,256.3),(54.68,265.0)]
def rot(pts,c,th):
    s,co=math.sin(th),math.cos(th)
    return [(c[0]+(d-c[0])*co-(h-c[1])*s, c[1]+(d-c[0])*s+(h-c[1])*co) for d,h in pts]
def clr(pts):
    cw=min((d-45.5) if h>=250 else 99 for d,h in pts)
    for (d1,h1),(d2,h2) in zip(pts,pts[1:]+pts[:1]):
        if (h1-250)*(h2-250)<0: cw=min(cw,d1+(250-h1)*(d2-d1)/(h2-h1)-45.5)
    return round(cw,2),round(min(270-h for d,h in pts),2)
SPN=0.0465   # MPa/N（片側の立体骨組みで算出、左右同じ）
K092=[(0.5,1.28,6),(1.0,2.51,24),(2.0,4.88,92),(4.5,10.33,414)]
rows=[]
for dB,th,F in K092:
    a1=clr(rot(P,(52.0,252.885),-math.radians(th))); a2=clr(rot(P,(70.0,252.885),math.radians(th)))
    rows.append([dB,th,F,round(F*SPN,1),a1[0],a1[1],a2[0],a2[1]])
    print(rows[-1])
out='/mnt/user-data/outputs/%s_K093_一時的な傾きのすき間とこじれの応力.csv'%TS
with open(out,'w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f)
    w.writerow(['K093 収納端の手前での一時的な傾き：CSPと周囲のすき間（cm）、こじれの力によるリンクの応力（MPa）'])
    w.writerow(['傾きなしのすき間：前の壁2.51・掘込面5.00。δB・傾き・こじれの力はK092。リンクの応力＝こじれの力×0.0465MPa/N（自重などの応力は含まない）。ピンのすきまは含まない。'])
    w.writerow([])
    w.writerow(['Bの遅れ mm','傾き °','こじれの力 N','リンクの応力 MPa','左が先に停止：前の壁とのすき間','左が先に停止：掘込面とのすき間','右が先に停止：前の壁とのすき間','右が先に停止：掘込面とのすき間'])
    w.writerows(rows)
print(out)
