# K021 右限配置で保持具を置ける領域（STEP2 2-1・2-5）
# CSPを右限（右側面＝梁2内面 x=170）に置いた収納状態で、保持具・接続部を置ける空間を側面図・正面図で示す。
# 入力：A01-001、A02-002（24°）、A02-003、A00-001（h=245）、A02-001（h=270）、D01-009（梁1 x=79〜89.5、梁2 x=170〜180.5）、
#       梁下面 h=254.5（部屋.xlsx）、掘込み前壁 d=45.5、照明（d=130、器具径11.4、A00-006 118°）、A02-005（収納d1=46.2）、K015〜K020
# 座標：部屋座標（D00-001〜003）。単位cm。保持具の厚さはすべて0（CSP単体）。
# 使い方：python3 本ファイル <出力svgパス>
import math, sys, html
W, D, H, T = 57.1, 21.4, 17.0, math.radians(24)
c, s = math.cos(T), math.sin(T)
TS = '2609281050'
D1, LOW, HB, HC, HT = 46.2, 245.0, 254.5, 250.0, 270.0
XR = 170.0; XL = XR - W
TAN59 = math.tan(math.radians(59))
def light_d(h): return 130 - 11.4 / 2 - (270 - h) * TAN59
h0 = LOW + D * s
P0 = (D1, h0); P1 = (D1 + D * c, LOW)
P3 = (D1 + D * c + H * s, h0 - D * s + H * c); P2 = (D1 + H * s, h0 + H * c)
def cut(a, b, h):  # 辺a→bと高さhの交点
    t = (h - a[1]) / (b[1] - a[1]); return (a[0] + t * (b[0] - a[0]), h)
Q1 = cut(P1, P3, HB); Q2 = cut(P2, P0, HB)

e = html.escape; out = []
K, RED, GRN, GRY, BLU, ORG, PUR, AMB = '#333333', '#C0392B', '#2E9E6B', '#8a857a', '#2C6FB0', '#D35400', '#6A5FD0', '#C8860A'
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

txt(40, 40, 'K021　右限配置で保持具を置ける領域（STEP2 2-1・2-5）', size=18, bold=True)
txt(40, 62, '作成 %s　部屋座標・単位cm。CSP右側面＝梁2内面 x=170（右限、中心x=141.45）、収納 d1=46.2・チルト24°・最下点h=245（K018のB）。保持具の厚さは0で図示' % TS, size=12)

# ---------- 側面図 ----------
SV = V(60, 110, 40, 274, 11)
txt(60, 100, '側面図（左壁側から+x方向を見る。左がSC側、右がLP側）', size=14, bold=True)
allow = [(45.5, LOW), (light_d(LOW), LOW), (light_d(HT), HT), (45.5, HT)]
poly(SV, allow, col=GRN, fill=GRN, op=0.12, w=1.2)
poly(SV, [P0, P1, P3, P2], col=K, fill='#e8e8e8', op=1)
poly(SV, [P1, P3], col=RED, w=4, close=False)
poly(SV, [P0, P1, Q1, Q2], col=ORG, fill=ORG, op=0.35, w=1.2)
for hv, lab, col, dsh in [(HT, '掘込面 h=270', K, None), (HB, '梁下面 h=254.5', GRY, '6 3'), (LOW, '収納下限 h=245', BLU, '6 3')]:
    poly(SV, [(40, hv), (130, hv)], col=col, w=1.1, dash=dsh, close=False); T_(SV, 130, hv, lab, dx=6, dy=4, col=col)
poly(SV, [(40, HC), (45.5, HC), (45.5, HT)], col=K, w=2, close=False); T_(SV, 40, HC, '天井面 h=250', dy=14, col=GRY, size=11); T_(SV, 45.5, HT, '掘込み前壁 d=45.5', dx=-4, dy=-6, anchor='end')
poly(SV, [(light_d(LOW), LOW), (light_d(HT), HT)], col=AMB, w=1.4, dash='5 3', close=False)
T_(SV, light_d(258), 258, '照明 118°の境界（上ほど後方）', dx=8, col=AMB)
for p, lab, dx, dy in [(P0, 'P0', -8, 4), (P1, 'P1', -4, 16), (P2, 'P2', -4, -6), (P3, 'P3', 6, 0)]:
    T_(SV, *p, lab, dx=dx, dy=dy, anchor='end' if dx < 0 else 'start')
T_(SV, (P0[0] + P1[0]) / 2 - 3, 247.5, '①底面側（K016 支持板）', anchor='middle', col=GRN, size=12)
T_(SV, P3[0] + 2, 250, '②前面側（K017 爪）', col=GRN, size=12)
T_(SV, 58, 266.5, '④上面側', col=GRN, size=12)
T_(SV, 45.8, 262, '③背面側', col=GRN, size=12)
T_(SV, 47, 256.5, '端子', col=PUR, size=11)
T_(SV, (P0[0] + P1[0]) / 2 + 6, 251.3, 'CSP右側面のうち梁下面より下', anchor='middle', col=ORG, size=11)

# ---------- 正面図 ----------
FV = V(60, 520, 70, 274, 6.5)
txt(60, 510, '正面図（LP側から−d方向を見る）　収納時', size=14, bold=True)
for (a0, a1, lab) in [(79, 89.5, '梁1'), (170, 180.5, '梁2')]:
    poly(FV, [(a0, HB), (a1, HB), (a1, HT), (a0, HT)], col=GRY, fill=GRY, op=0.6)
    T_(FV, (a0 + a1) / 2, HT, lab, dy=-6, anchor='middle', bold=True)
poly(FV, [(89.5, HB), (XL, HB), (XL, HT), (89.5, HT)], col=GRN, fill=GRN, op=0.15, w=1)
poly(FV, [(XR, LOW), (205, LOW), (205, HB), (XR, HB)], col=GRN, fill=GRN, op=0.15, w=1, dash='4 3')
poly(FV, [(75, LOW), (XL, LOW), (XL, HB), (75, HB)], col=GRN, fill=GRN, op=0.15, w=1, dash='4 3')
poly(FV, [(XL, LOW), (XR, LOW), (XR, P2[1]), (XL, P2[1])], col=K, fill='#e8e8e8')
poly(FV, [(XL, LOW), (XR, LOW), (XR, HB), (XL, HB)], col=ORG, fill=ORG, op=0.3, w=0)
for hv, lab, col, dsh in [(HT, 'h=270', K, None), (HB, '梁下面 h=254.5', GRY, '6 3'), (LOW, 'h=245', BLU, '6 3')]:
    poly(FV, [(70, hv), (215, hv)], col=col, w=1.1, dash=dsh, close=False); T_(FV, 215, hv, lab, dx=6, dy=4, col=col)
T_(FV, (89.5 + XL) / 2, 262, '左の空き 23.4', anchor='middle', col=GRN)
T_(FV, (89.5 + XL) / 2, 258, '(t左はここまで)', anchor='middle', col=GRN, size=11)
T_(FV, (XR + 205) / 2, 249, '梁2の下', anchor='middle', col=GRN)
T_(FV, (XR + 205) / 2, 246, '(t右を出せる)', anchor='middle', col=GRN, size=11)
T_(FV, (XL + XR) / 2, 262, 'CSP（中心x=141.45）', anchor='middle')
T_(FV, XR, HB + 3, '右側面＝梁2内面 x=170（t右＝0）', dx=-4, anchor='end', col=RED, size=11)

# ---------- 注記 ----------
NX, NY = 1170, 120
txt(NX, NY, '■ 図からわかること', bold=True, size=14)
NOTES = [
    '【左右】右限に置くと、梁下面h=254.5より上では',
    '　右側面が梁2内面に接する → そこでは t右＝0',
    '　梁下面より下は梁がないので、右側に出せる',
    '　（CSP右側面の下部：オレンジ部分）',
    '　左側は梁1内面まで 23.4 の空き',
    '【上下前後（側面図の緑の空間）】',
    '　収納時に使える空間＝ h=245〜270、d=45.5〜照明境界',
    '　チルトしたCSPの周りに4つの空き（①〜④）がある',
    '　① 底面側：P0寄りに厚みを取れる（K016）',
    '　② 前面側：照明境界まで余裕（K017の爪）',
    '　③ 背面側：P0より上は奥へ広がる。端子あり',
    '　④ 上面側：P2寄りは0.77、P3寄りは9.47まで',
    '　全面に均一の厚さを足す（K015）と、',
    '　P1・P2の角でぶつかる',
    '【前提】収納d1=46.2（K013）。d1は56.2まで前へ',
    '　ずらせる（A02-005）→ ③の空きが広がる',
    '　余裕寸法は0（2-4で設定）',
]
for i, t in enumerate(NOTES): txt(NX, NY + 26 + i * 20, t, col='#222' if t.startswith('【') else '#333', size=13)

Wc, Hc = 1640, 820
svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" font-family="Noto Sans CJK JP, Hiragino Sans, Meiryo, sans-serif">' % (Wc, Hc, Wc, Hc),
       '<rect width="100%" height="100%" fill="white"/>'] + out + ['</svg>']
open(sys.argv[1], 'w', encoding='utf-8').write('\n'.join(svg))
print('P0', P0, 'P1', P1, 'P2', P2, 'P3', P3, 'Q1', Q1, 'Q2', Q2, 'light245', light_d(245), 'light270', light_d(270))
