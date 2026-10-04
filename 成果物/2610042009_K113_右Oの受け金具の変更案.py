#!/usr/bin/env python3
# K113 右Oの受け金具の変更案（部屋を含まない部分詳細：F7 d。梁2の側面 x=170 は位置の目印として線だけ示す）
# 入力：K112（右O d=70・h=265、φ12.31〜70°、2a=89.68、右の脚 x=162.7〜165.2・h=267.5〜269.5・使用時 d=63.05から）、A06-003（Oのピンφ12両持ち：架台側スペーサーと外側の受け金具、OAは長リンクのCSP側）、
#       A06-004（右：長リンク中心163.95、OA中心161.45）、K100の右Oの受け金具（上板 x=159.2〜169.2・d=68.5〜71.5・h=266.5〜269.5、外板 x=159.2〜160.2・h=263.5〜269.5）、A03-004（CSP外形、収納を7.0下げる）
import math, subprocess, html
TS = subprocess.run(['date','+%y%m%d%H%M'],capture_output=True,text=True,env={'TZ':'Asia/Tokyo'}).stdout.strip()
e = html.escape
O = (70.0, 265.0); L = 89.68; hw = 2.0
B, G, K, R, P, Gr = '#2C6FB0', '#2E9E6B', '#5F5E5A', '#c0392b', '#9b6fc0', '#1F7A4D'
W, H = 1300, 900
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="Noto Sans CJK JP, sans-serif">', f'<rect width="{W}" height="{H}" fill="#fff"/>',
 '<text x="20" y="30" font-size="18" font-weight="bold">K113　右Oの受け金具の変更案（右の脚を通すため）</text>',
 f'<text x="20" y="50" font-size="11" fill="#555">作成 {TS}　部屋を含まない部分詳細（F7 d）。K112の配置。破線・( )は仮。単位cm。新しい受け金具の板厚・形は仮</text>']
def T(x,y,s,fs=11,c='#222',a='middle'): o.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{fs}" fill="{c}" text-anchor="{a}">{e(s)}</text>')
def poly(pts,c,op,dash=True,w=1): o.append(f'<polygon points="{" ".join(f"{a:.1f},{b:.1f}" for a,b in pts)}" fill="{c}" fill-opacity="{op}" stroke="{c}" stroke-width="{w}" {"stroke-dasharray=\"4 2\"" if dash else ""}/>')
# ---- (1) 側面 d-h（右側、x方向に重ねて見る）
X0, Y0, S = 60, 110, 13.0
sx = lambda d: X0+(d-58)*S; sy = lambda h: Y0+(271-h)*S
T(60, 85, '(1) 側面（右側。x方向に重ねて表示）：今の受け金具（赤）と変更案（緑）', 13, '#000', 'start')
for h in (270, 254.5):
    o.append(f'<line x1="{sx(58)}" y1="{sy(h)}" x2="{sx(102)}" y2="{sy(h)}" stroke="#999" stroke-dasharray="6 3"/>')
T(sx(102)+4, sy(270)+4, '掘込面 h=270', 10, '#777', 'start'); T(sx(102)+4, sy(254.5)+4, '梁下面 h=254.5', 10, '#777', 'start')
# OA の掃引（φ12.31〜70°、Oから長さ L/2 のうち図の範囲）
def band(ph, s1):
    u = (math.cos(math.radians(ph)), -math.sin(math.radians(ph))); n = (-u[1], u[0])
    return [(O[0]+n[0]*hw, O[1]+n[1]*hw), (O[0]+u[0]*s1+n[0]*hw, O[1]+u[1]*s1+n[1]*hw), (O[0]+u[0]*s1-n[0]*hw, O[1]+u[1]*s1-n[1]*hw), (O[0]-n[0]*hw, O[1]-n[1]*hw)]
for i in range(0, 41):
    ph = 12.31 + (70-12.31)*i/40
    poly([(sx(a), sy(b)) for a, b in band(ph, 30)], P, 0.03, False, 0)
o.append(f'<circle cx="{sx(O[0])}" cy="{sy(O[1])}" r="{hw*S}" fill="{P}" fill-opacity="0.15"/>')
T(sx(84), sy(258), 'OAの掃引（収納〜使用）', 11, P)
# 右の脚の通り道（使用時 d=63.05 から LP側へ）
poly([(sx(63.05), sy(269.5)), (sx(102), sy(269.5)), (sx(102), sy(267.5)), (sx(63.05), sy(267.5))], G, 0.25)
T(sx(66), sy(268.5)+4, '右の脚の通り道（h=267.5〜269.5、使用時 d=63.05〜）', 10, Gr, 'start')
poly([(sx(62.05), sy(269.5)), (sx(64.05), sy(269.5)), (sx(64.05), sy(267.5)), (sx(62.05), sy(267.5))], G, 0.6, False)
T(sx(63.05), sy(270.2), '横棒（使用）', 10, Gr)
# 今の受け金具（上板・外板）
poly([(sx(68.5), sy(269.5)), (sx(71.5), sy(269.5)), (sx(71.5), sy(263.5)), (sx(68.5), sy(263.5))], R, 0.35)
T(sx(71.8), sy(264.5), '今：上板＋外板', 11, R, 'start')
# 変更案：外板を下げ、SC側（d=64〜67）の下の橋で架台へ
poly([(sx(68.5), sy(267.0)), (sx(71.5), sy(267.0)), (sx(71.5), sy(262.0)), (sx(68.5), sy(262.0))], Gr, 0.35)
poly([(sx(64.0), sy(266.5)), (sx(67.0), sy(266.5)), (sx(67.0), sy(262.0)), (sx(64.0), sy(262.0))], Gr, 0.35)
poly([(sx(67.0), sy(266.5)), (sx(68.5), sy(266.5)), (sx(68.5), sy(262.0)), (sx(67.0), sy(262.0))], Gr, 0.15)
T(sx(64.0)-4, sy(262)+16, '変更案：外板（h≦267）と、SC側の橋（d=64〜67、h=262〜266.5）', 11, Gr, 'start')
o.append(f'<circle cx="{sx(O[0])}" cy="{sy(O[1])}" r="{0.6*S}" fill="#333"/>'); T(sx(O[0])+10, sy(O[1])-6, 'O（ピンφ12）', 10, '#333', 'start')
# CSP 収納（7.0下げ）の上面
P2, P3 = (54.68, 258.0), (74.23, 249.3)
o.append(f'<polyline points="{sx(58):.1f},{sy(P2[1]+(P3[1]-P2[1])*(58-P2[0])/(P3[0]-P2[0])):.1f} {sx(P3[0]):.1f},{sy(P3[1]):.1f}" fill="none" stroke="{B}" stroke-dasharray="4 2"/>')
T(sx(60), sy(255.5), 'CSP収納の上面（x≦161.7）', 10, B, 'start')
for d in range(60, 101, 5): T(sx(d), sy(253.5), str(d), 10)
T(sx(80), sy(252.3), 'd', 11)
# ---- (2) 正面断面 x-h（d=70、O）
X1, Y1, S2 = 760, 130, 26
qx = lambda x: X1+(x-157)*S2; qy = lambda h: Y1+(271-h)*S2
T(760, 85, '(2) 正面断面（O の位置 d=70、SC側から見て左が梁2）', 13, '#000', 'start')
def box(x0, x1, h0, h1, c, op=0.35, dash=True): poly([(qx(x0),qy(h1)),(qx(x1),qy(h1)),(qx(x1),qy(h0)),(qx(x0),qy(h0))], c, op, dash)
o.append(f'<line x1="{qx(170)}" y1="{qy(271)}" x2="{qx(170)}" y2="{qy(253)}" stroke="#999" stroke-width="2"/>'); T(qx(170)+4, qy(271)+12, '梁2', 10, '#777', 'start')
box(169.2, 170, 254.5, 270, K, 0.6, False); T(qx(169.6), qy(253.5), '架台', 10)
box(160.2, 162.7, 263, 267, P, 0.35); T(qx(161.45), qy(262), 'OA', 10, P)
box(159.2, 169.2, 264.4, 265.6, '#333', 0.7, False); T(qx(166.5), qy(264), 'ピン', 10)
box(165.2, 169.2, 263.0, 267.0, K, 0.3); T(qx(167.2), qy(262), 'スペーサー', 10)
box(162.7, 165.2, 267.5, 269.5, G, 0.5); T(qx(163.95), qy(268.5)+4, '右の脚', 10, Gr)
box(159.2, 169.2, 266.5, 269.5, R, 0.15); T(qx(158.9), qy(269.9), '今の上板（脚と重なる）', 10, R, 'start')
box(159.2, 160.2, 262.0, 267.0, Gr, 0.45); T(qx(159.0), qy(261.3), '変更案の外板', 10, Gr, 'start')
for x in range(158, 171, 2): T(qx(x), qy(253.0)+14, str(x), 10)
for hh in (270, 254.5):
    o.append(f'<line x1="{qx(157)}" y1="{qy(hh)}" x2="{qx(170)}" y2="{qy(hh)}" stroke="#999" stroke-dasharray="6 3"/>')
# ---- 説明
lines = ['今の受け金具：外板（x=159.2〜160.2）を上板（h=266.5〜269.5）で架台に吊る形。上板が右の脚の通り道（x=162.7〜165.2、h≧267.5）を横切る',
 '変更案：上板をやめ、外板の上端を h=267.0 に下げる。外板を SC側へ d=64 まで延ばし、橋（d=64〜67、h=262〜266.5、x=159.2〜169.2）で架台へつなぐ',
 '　・橋を SC側に置く理由：OAは収納〜使用でOから LP側・下側にしか振れず、O側の端の丸み（半径2）も d≧68 なので、d≦67 には入らない（すき間1）',
 '　・長リンクは O の近くでは C点（収納 h≦245.9）にしかいないので、x=162.7〜165.2 を橋が横切っても当たらない',
 '　・横棒の使用位置（d=62.05〜64.05、h≧267.5）は橋より上。CSP収納の上面（d=64で h≈253.8）とは 8 以上離れる',
 '確認できていないこと：外板の上端と脚のすき間 0.5、橋と外板の強度、橋が SC側から見えるかどうか（梁下面より上なので許容範囲の想定）']
for i, s in enumerate(lines): T(20, 640+i*24, s, 12, '#222', 'start')
o.append('</svg>')
open(f'/mnt/user-data/outputs/{TS}_K113_右Oの受け金具の変更案.svg','w',encoding='utf-8').write('\n'.join(o))
print(TS)
