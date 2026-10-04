#!/usr/bin/env python3
# K108 案AのL字の横棒（Δd=18を残す）と、片側駆動のこじれ（部屋を含まない部分詳細：F7 d。梁2の側面 x=170 は位置の目印として線だけ示す）
# 入力：K100機構JSON（2610032002版）の右側の部品の範囲、A06-001（O h=265、B収納 左151.25・右169.25、使用 左105.83・右123.83、φ収納7.0°）、
#       A06-004（リンク面 左95.55・右163.95）、A06-007（HSR20C MA=0.218kN·m）、K090（片側の荷重 Wside=75N、F=Wside·cotφ）、A04-007（常時の安全率4）
import math, subprocess, html
TS = subprocess.run(['date','+%y%m%d%H%M'],capture_output=True,text=True,env={'TZ':'Asia/Tokyo'}).stdout.strip()
e = html.escape
W, H = 1300, 980
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="Noto Sans CJK JP, sans-serif">', f'<rect width="{W}" height="{H}" fill="#fff"/>',
     '<text x="20" y="30" font-size="18" font-weight="bold">K108　案AのL字の横棒と、片側駆動のこじれ</text>',
     f'<text x="20" y="50" font-size="11" fill="#555">作成 {TS}　部屋を含まない部分詳細（F7 d）。破線・( )は仮設定を含む値。単位cm（力N、モーメントN·m）。L字の断面・高さは仮（横棒・脚とも h=267.5〜269.5）</text>']
def R(x,y,w,h,c,op=0.4,dash=True): o.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{c}" fill-opacity="{op}" stroke="{c}" stroke-width="1" {"stroke-dasharray=\"4 2\"" if dash else ""}/>')
def T(x,y,s,fs=11,c='#222',a='middle'): o.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{fs}" fill="{c}" text-anchor="{a}">{e(s)}</text>')
B, G, K = '#2C6FB0', '#2E9E6B', '#5F5E5A'
# (1) 平面図 x-d（上がSC側）
X0, Y0, S = 70, 90, 5.0      # x=88 → X0、d=95 → Y0
px = lambda x: X0+(x-88)*S; py = lambda d: Y0+(d-95)*S*0.85
T(40, 78, '(1) 平面図（収納：青、使用：緑）', 13, '#000', 'start')
o.append(f'<line x1="{px(170)}" y1="{py(95)}" x2="{px(170)}" y2="{py(185)}" stroke="#999" stroke-width="2"/>'); T(px(170)+4, py(97), '梁2の側面 x=170', 10, '#777', 'start')
o.append(f'<line x1="{px(89.5)}" y1="{py(95)}" x2="{px(89.5)}" y2="{py(185)}" stroke="#999" stroke-width="2"/>'); T(px(89.5)-4, py(97), '梁1の側面 x=89.5', 10, '#777', 'end')
for x0,x1,d0,d1 in ((90.3,92.1,99.54,157.54),(167.4,169.2,117.54,175.54)):
    R(px(x0),py(d0),(x1-x0)*S,(d1-d0)*S*0.85,'#555',0.5)
T(px(91.2), py(100)-4, 'レール', 9); T(px(168.3), py(118)-4, 'レール', 9)
for (bl,br,c) in ((151.25,169.25,B),(105.83,123.83,G)):
    R(px(90.7),py(bl-3.7),3.6*S,7.4*S*0.85,c,0.5)       # 左ブロック
    R(px(166.2),py(br-3.7),2.6*S,7.4*S*0.85,c,0.5)      # 右ブロック
    R(px(94.3),py(bl-0.6),(165.2-94.3)*S,1.2*S*0.85,c,0.15)   # 左の長リンク付近（目印）は省略しない：横棒
    R(px(92.1),py(bl-1),(165.2-92.1)*S,2*S*0.85,c,0.55)  # 横棒
    R(px(162.7),py(bl-1),2.5*S,(br-bl+1)*S*0.85,c,0.55)  # L字の脚
    T(px(128),py(bl)-6,f'横棒 d={bl}',10,c)
    T(px(161.5),py((bl+br)/2),f'脚 {br-bl:.0f}',10,c,'end')
    o.append(f'<circle cx="{px(95.55)}" cy="{py(bl)}" r="3" fill="{c}"/><circle cx="{px(163.95)}" cy="{py(br)}" r="3" fill="{c}"/>')
T(px(95.55)+6, py(151.25)+16, 'B左', 10, B, 'start'); T(px(163.95)-6, py(169.25)+4, 'B右', 10, B, 'end')
T(px(128), py(182), 'L字の脚は右の長リンクの真上（x=162.7〜165.2）を通る', 11)
# (2) 正面断面 x-h（d=160、収納時）
X1, Y1, S2 = 560, 120, 22
qx = lambda x: X1+(x-155)*S2; qy = lambda h: Y1+(271-h)*S2
T(560, 78, '(2) 正面断面 d=160（収納時、脚と長リンクの位置）', 13, '#000', 'start')
o.append(f'<line x1="{qx(170)}" y1="{qy(271)}" x2="{qx(170)}" y2="{qy(252)}" stroke="#999" stroke-width="2"/>')
R(qx(169.2),qy(270),0.8*S2,15.5*S2,K,0.6); T(qx(169.6),qy(253)+14,'架台',10)
R(qx(167.4),qy(266),1.8*S2,2*S2,'#555',0.6); T(qx(168.3),qy(263.6),'レール',10)
ch = 265-(169.25-160)*math.tan(math.radians(7)); hw = 2/math.cos(math.radians(7))
R(qx(162.7),qy(ch+hw),2.5*S2,2*hw*S2,B,0.35); T(qx(163.95),qy(ch)+4,'長リンク',10)
R(qx(162.7),qy(269.5),2.5*S2,2*S2,B,0.6); T(qx(163.95),qy(268.5)+4,'L字の脚',10,'#fff')
o.append(f'<line x1="{qx(155)}" y1="{qy(270)}" x2="{qx(171)}" y2="{qy(270)}" stroke="#333" stroke-dasharray="6 3"/>'); T(qx(155)+2,qy(270)-4,'掘込面 h=270',10,'#333','start')
o.append(f'<line x1="{qx(155)}" y1="{qy(254.5)}" x2="{qx(171)}" y2="{qy(254.5)}" stroke="#333" stroke-dasharray="6 3"/>'); T(qx(155)+2,qy(254.5)-4,'梁下面 h=254.5',10,'#333','start')
gap = 267.5-(ch+hw)
T(qx(158.5),qy(266.6),f'すき間 {gap:.2f}',11,'#c0392b')
o.append(f'<line x1="{qx(160.5)}" y1="{qy(267.5)}" x2="{qx(160.5)}" y2="{qy(ch+hw)}" stroke="#c0392b"/>')
T(560, qy(252)+24, '長リンクは収納時φ=7°。d=160での上端 h=%.2f（中心%.2f）。動くとBのまわりで下がる'%(ch+hw,ch), 11, '#222', 'start')
# (3) こじれ
F = 75/math.tan(math.radians(7)); xL, xR = 95.55, 163.95; MA = 218
Y3 = 620
T(40, Y3, '(3) 駆動を1か所で押すときに横棒とガイドにかかるこじれ（収納時、常時荷重、リンクの重さを含まない）', 13, '#000', 'start')
lines = [f'片側のBを押す力 F = Wside·cotφ収納 = 75×cot7.0° = {F:.0f} N（K090、左右同じとする）',
 f'駆動を x=xd で押すと、横棒は左右のBから F ずつ受け、こじれ M = F×|2·xd − xL − xR|（xL={xL}・xR={xR}：リンク面、A06-004）',
 f'左の端（xd=xL）で押すと M = {F:.0f}×{(xR-xL)/100:.3f} = {F*(xR-xL)/100:.0f} N·m。ガイド2個の公表値の合計 {2*MA} N·m に対して余裕{2*MA/(F*(xR-xL)/100):.2f}倍（必要な安全率4に届かない）',
 f'安全率4で受けるには M ≦ {2*MA/4:.0f} N·m → |2·xd − {xL+xR:.1f}| ≦ {2*MA/4/F*100:.1f} → xd = {(xL+xR)/2-2*MA/4/F*100/2:.1f}〜{(xL+xR)/2+2*MA/4/F*100/2:.1f}（左右の真ん中 x={(xL+xR)/2:.2f} の近く）',
 '真ん中付近は照明の列（x=129.65）の真下。収納時に台形ねじ・ナット・モーターを置くと配光（A00-006）に入る（K105）',
 'ガイドのヨー方向の許容モーメントは MA（0.218kN·m、A06-007）と同じと仮定（未確認）。横棒そのものも同じ M を曲げで受ける（断面の計算は未実施）']
for i,s in enumerate(lines): T(40, Y3+28+i*22, s, 12, '#222', 'start')
# グラフ：xd と M
gx0, gy0, gw, gh = 120, Y3+175, 700, 140
xa, xb, Mm = 90, 170, 450
gx = lambda x: gx0+(x-xa)/(xb-xa)*gw; gy = lambda m: gy0+gh-m/Mm*gh
o.append(f'<rect x="{gx0}" y="{gy0}" width="{gw}" height="{gh}" fill="none" stroke="#333"/>')
o.append(f'<polyline points="{gx(xa):.1f},{gy(F*abs(2*xa-xL-xR)/100):.1f} {gx((xL+xR)/2):.1f},{gy(0):.1f} {gx(xb):.1f},{gy(F*abs(2*xb-xL-xR)/100):.1f}" fill="none" stroke="#c0392b" stroke-width="2"/>')
o.append(f'<line x1="{gx0}" y1="{gy(2*MA/4)}" x2="{gx0+gw}" y2="{gy(2*MA/4)}" stroke="{G}" stroke-dasharray="5 3"/>'); T(gx0+gw+4, gy(2*MA/4)+4, f'MA×2÷4={2*MA/4:.0f}', 10, G, 'start')
o.append(f'<line x1="{gx0}" y1="{gy(2*MA)}" x2="{gx0+gw}" y2="{gy(2*MA)}" stroke="#555" stroke-dasharray="5 3"/>'); T(gx0+gw+4, gy(2*MA)+4, f'MA×2={2*MA}', 10, '#555', 'start')
o.append(f'<line x1="{gx(129.65)}" y1="{gy0}" x2="{gx(129.65)}" y2="{gy0+gh}" stroke="#E0A100" stroke-width="2"/>'); T(gx(129.65), gy0-4, '照明の列 x=129.65', 10, '#a07000')
for x in range(90, 171, 10): T(gx(x), gy0+gh+14, str(x), 10)
for m in (0, 100, 200, 300, 400): T(gx0-6, gy(m)+4, str(m), 10, '#222', 'end')
T(gx0+gw/2, gy0+gh+28, '駆動で押す位置 xd', 11); T(gx0-40, gy0-6, 'M（N·m）', 10, '#222', 'start')
o.append('</svg>')
open(f'/mnt/user-data/outputs/{TS}_K108_L字の横棒と片側駆動のこじれ.svg','w',encoding='utf-8').write('\n'.join(o))
print(TS, F, gap, F*(xR-xL)/100)
