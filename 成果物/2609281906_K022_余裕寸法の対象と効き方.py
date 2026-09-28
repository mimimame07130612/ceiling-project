# K022 余裕寸法の対象と効き方（STEP2 2-4）
# 右限・振りなし・チルト24°維持の配置で、余裕寸法をとる対象（c1〜c7）の位置と、余裕 m を取ったときに何が変わるかを示す。
# 入力：A01-001、A02-002、A02-003、A02-004（SC幕面とのすき間8）、A02-005、A02-006、A00-001、A02-001、A00-006、
#       A01-003・A00-004（光束上端面 h=161+(d−25)×56/280）、D01-009、K011、K013、K016、K018、K020、K021
# 座標：部屋座標。単位cm。保持具の厚さは0で図示。
# 使い方：python3 本ファイル <出力svgパス>
import math, sys, html
W, D, H, T = 57.1, 21.4, 17.0, math.radians(24)
c, s = math.cos(T), math.sin(T)
TS = '2609281906'
TAN59 = math.tan(math.radians(59))
def light_d(h): return 130 - 11.4 / 2 - (270 - h) * TAN59
def beam_h(d): return 161 + (d - 25) * 56 / 280
def csp(d1, low):
    h0 = low + D * s
    return [(d1, h0), (d1 + D * c, low), (d1 + D * c + H * s, h0 - D * s + H * c), (d1 + H * s, h0 + H * c)]
ST = csp(46.2, 245.0); US = csp(33.0, 166.5)
XR, XL = 170.0, 170.0 - W
EYE = (270, 100); BAF = (56.0, 174.3)
elev = lambda dh_: math.degrees(math.atan((BAF[1] + dh_ - EYE[1]) / (EYE[0] - BAF[0])))

e = html.escape; out = []
K, RED, GRN, GRY, BLU, ORG, PUR, AMB, MAG = '#333333', '#C0392B', '#2E9E6B', '#8a857a', '#2C6FB0', '#D35400', '#6A5FD0', '#C8860A', '#C8307A'
def f(n): return ('%.1f' % n).rstrip('0').rstrip('.')
class V:
    def __init__(s_, ox, oy, u0, v1, sc): s_.ox, s_.oy, s_.u0, s_.v1, s_.sc = ox, oy, u0, v1, sc
    def X(s_, u): return s_.ox + (u - s_.u0) * s_.sc
    def Y(s_, v): return s_.oy + (s_.v1 - v) * s_.sc
def poly(v, pts, col=K, w=1.4, fill='none', op=1, dash=None, close=True):
    tag = 'polygon' if close else 'polyline'
    out.append('<%s points="%s" fill="%s" fill-opacity="%s" stroke="%s" stroke-width="%s"%s/>' % (
        tag, ' '.join('%s,%s' % (f(v.X(a)), f(v.Y(b))) for a, b in pts), fill, op, col, w,
        ' stroke-dasharray="%s"' % dash if dash else ''))
def txt(x, y, t, col='#222', anchor='start', size=13, bold=False):
    out.append('<text x="%s" y="%s" fill="%s" text-anchor="%s" font-size="%s"%s>%s</text>' % (
        f(x), f(y), col, anchor, size, ' font-weight="bold"' if bold else '', e(t)))
def T_(v, a, b, t, dx=0, dy=0, **k): txt(v.X(a) + dx, v.Y(b) + dy, t, **k)
def tag(v, a, b, lab, dx=0, dy=0):
    out.append('<circle cx="%s" cy="%s" r="11" fill="%s"/>' % (f(v.X(a) + dx), f(v.Y(b) + dy), MAG))
    txt(v.X(a) + dx, v.Y(b) + dy + 4, lab, col='white', anchor='middle', size=11, bold=True)

txt(40, 40, 'K022　余裕寸法の対象と効き方（STEP2 2-4）', size=18, bold=True)
txt(40, 62, '作成 %s　部屋座標・単位cm。右限（中心x=141.45）・振りなし・チルト24°維持（K018のB）。収納d1=46.2・使用d1=33。保持具の厚さは0で図示。桃の丸＝余裕寸法の対象' % TS, size=12)

# ---------- 側面図 ----------
SV = V(60, 110, 15, 276, 5.2)
txt(60, 100, '側面図（左がSC側、右がLP側）', size=14, bold=True)
poly(SV, [(15, 270), (45.5, 270), (45.5, 250), (15, 250)], col=K, w=0, fill=GRY, op=0.15)
poly(SV, [(15, 250), (45.5, 250), (45.5, 270), (125, 270)], col=K, w=2, close=False)
poly(SV, [(20.5, 250), (33.9, 250), (33.9, 236.5), (20.5, 236.5)], col=GRY, dash='4 3')
T_(SV, 20.5, 236.5, 'SCケース', dy=14, col=GRY, size=11)
poly(SV, [(25, 161), (25, 236.5)], col=K, w=2.5, close=False); T_(SV, 25, 170, 'SC幕面 d=25', dx=-6, anchor='end', size=11)
poly(SV, [(25, beam_h(25)), (110, beam_h(110))], col=ORG, w=1.4, dash='6 3', close=False)
T_(SV, 100, beam_h(100), '光束上端面', dy=16, col=ORG, size=11)
poly(SV, [(light_d(245), 245), (light_d(270), 270)], col=AMB, w=1.4, dash='5 3', close=False)
T_(SV, light_d(262), 262, '配光118°境界', dx=8, dy=4, col=AMB, size=11)
poly(SV, [(15, 245), (110, 245)], col=BLU, w=1, dash='6 3', close=False); T_(SV, 110, 245, 'h=245', dx=4, dy=4, col=BLU, size=11)
poly(SV, [(15, 254.5), (110, 254.5)], col=GRY, w=1, dash='6 3', close=False); T_(SV, 110, 254.5, '梁下面', dx=4, dy=4, col=GRY, size=11)
for P, col, lab in [(ST, BLU, '収納'), (US, RED, '使用')]:
    poly(SV, P, col=col, fill=col, op=0.15)
    T_(SV, P[2][0], P[2][1], lab, dx=6, col=col)
tag(SV, *ST[3], 'c1', dy=-16)
tag(SV, 45.5, 253.7, 'c2', dx=-16)
tag(SV, *US[1], 'c4', dy=14)
tag(SV, light_d(245), 245, 'c5', dy=14)
tag(SV, 29, 175, 'c6')
tag(SV, 33.9, 243, 'c7', dx=16)

# ---------- 正面図 ----------
FV = V(640, 110, 70, 276, 4.6)
txt(640, 100, '正面図（LP側から見る）', size=14, bold=True)
for a0, a1, lab in [(79, 89.5, '梁1'), (170, 180.5, '梁2')]:
    poly(FV, [(a0, 254.5), (a1, 254.5), (a1, 270), (a0, 270)], col=GRY, fill=GRY, op=0.6)
    T_(FV, (a0 + a1) / 2, 270, lab, dy=-4, anchor='middle', size=11)
poly(FV, [(70, 270), (200, 270)], col=K, w=2, close=False)
poly(FV, [(XL, 245), (XR, 245), (XR, ST[3][1]), (XL, ST[3][1])], col=BLU, fill=BLU, op=0.15)
poly(FV, [(XL, 166.5), (XR, 166.5), (XR, US[3][1]), (XL, US[3][1])], col=RED, fill=RED, op=0.15)
poly(FV, [(169, 160), (169, 200)], col=PUR, w=1, dash='4 3', close=False); T_(FV, 169, 160, 'LP中央 x=169', dy=14, anchor='middle', col=PUR, size=11)
tag(FV, 170, 262, 'c3', dx=-14)
T_(FV, XL, 245, '収納', dx=4, dy=-6, col=BLU, size=11); T_(FV, XL, 166.5, '使用', dx=4, dy=-6, col=RED, size=11)

# ---------- 表 ----------
TX, TY = 60, 740
txt(TX, TY, '■ 余裕寸法の対象と、余裕 m を取ったときの変化（計算）', bold=True, size=14)
hdr = ['ID', '対象（どこ と どこ の間）', '今の値', '余裕 m を取ると変わること', '今の制約']
cw = [40, 330, 150, 800, 100]
rows = [
    ['c1', '収納時：CSP最上点P2 ↔ 掘込面 h=270', '0.77', 'm≦0.77：支持板の上限 t下（r=0.7）＝3.70 − 1.094·m。m＞0.77：CSP単体でも入らず、h=245 を (m−0.77) 以上下げる（K018）', '拘束'],
    ['c2', '収納時：CSP背面P0 ↔ 掘込み前壁 d=45.5', '0.70（d1=46.2）', '収納d1の下限が上がる。ワンモーション移動の条件（K013）を再計算', '拘束'],
    ['c3', '収納時：CSP右側面 ↔ 梁2内面 x=170', '0', '中心x＝141.45 − m、LP中央とのずれ＝27.55 + m', '拘束'],
    ['c4', '使用時：CSP最下点P1 ↔ 光束上端面', '0', '使用時の最下点 h=166.5 + m、ストローク 78.5 − m、LP目への仰角 +%.2f°/cm' % (elev(1) - elev(0)), '拘束'],
    ['c5', '収納時：CSP前面側 ↔ 配光118°境界', '16.9（h=245）', '収納d1の上限 56.2 − m（今は余裕が大きい）', '拘束なし'],
    ['c6', '使用時：CSP背面 ↔ SC幕面', '8（A02-004）', 'すでに余裕として設定済み（d1≧33）', '設定済み'],
    ['c7', '動作中：CSP ↔ SCケース', '—', '経路で決まる（STEP4で確認、K011の注意）', 'STEP4'],
]
y = TY + 28; x = TX
for h_, w_ in zip(hdr, cw): txt(x, y, h_, bold=True); x += w_
for r in rows:
    y += 22; x = TX
    for v, w_ in zip(r, cw): txt(x, y, v, col=MAG if v.startswith('c') and len(v) == 2 else '#222'); x += w_
y += 32
for t_ in ['左側（梁1内面まで23.4）・照明の横方向は、右限・振りなしの配置では拘束にならない（K019〜K021）',
           '余裕 m の値は依頼主が決める。値はc1〜c4で別々にしてよい']:
    txt(TX, y, t_, col='#444'); y += 20

Wc, Hc = 1500, y + 20
svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" font-family="Noto Sans CJK JP, Hiragino Sans, Meiryo, sans-serif">' % (Wc, Hc, Wc, Hc),
       '<rect width="100%" height="100%" fill="white"/>'] + out + ['</svg>']
open(sys.argv[1], 'w', encoding='utf-8').write('\n'.join(svg))
print('elev/cm %.3f' % (elev(1) - elev(0)), 'c5 %.1f' % (light_d(245) - ST[1][0]))
