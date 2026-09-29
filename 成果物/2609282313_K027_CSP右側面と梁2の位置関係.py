# K027 CSP右側面と梁2の位置関係（STEP2 M03-008の見直し用）
# STEP2結論（A03-004、A03-002、A03-003）での収納状態を、梁2まわりの正面図・側面図で示す。
# 入力：A01-001、A02-002（24°）、A02-003、A00-001（h=243.77）、A03-003（c3=2）、A03-004（中心x=139.45、d1=48.5）、
#       D01-009（梁2 x=170〜180.5）、梁下面 h=254.5（部屋.xlsx）、掘込面 h=270、天井面 h=250
# 座標：部屋座標（D00-001〜003）。単位cm。保持具の厚さは0（CSP単体）。
# 使い方：python3 本ファイル <出力svgパス> <タイムスタンプ>
import math, sys, html
W, D, H, T = 57.1, 21.4, 17.0, math.radians(24)
c, s = math.cos(T), math.sin(T)
TS = sys.argv[2]
D1, LOW, HB, HC, HT = 48.5, 243.77, 254.5, 250.0, 270.0
XB = 170.0; XR = XB - 2.0; XL = XR - W
h0 = LOW + D * s
P0 = (D1, h0); P1 = (D1 + D * c, LOW)
P3 = (D1 + D * c + H * s, h0 - D * s + H * c); P2 = (D1 + H * s, h0 + H * c)
TOP = P2[1]
def cut(a, b, h):
    t = (h - a[1]) / (b[1] - a[1]); return (a[0] + t * (b[0] - a[0]), h)
Q1 = cut(P1, P3, HB); Q2 = cut(P2, P0, HB)
e = html.escape; out = []
K, RED, GRN, GRY, BLU, ORG = '#333333', '#C0392B', '#2E9E6B', '#8a857a', '#2C6FB0', '#D35400'
def f(n): return ('%.2f' % n).rstrip('0').rstrip('.')
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
def dim_v(v, u, a, b, lab, col):
    poly(v, [(u, a), (u, b)], col=col, w=1, close=False)
    for hv in (a, b): poly(v, [(u - 0.4, hv), (u + 0.4, hv)], col=col, w=1, close=False)
    T_(v, u, (a + b) / 2, lab, dx=6, dy=4, col=col, size=12)

txt(40, 40, 'K027　CSP右側面と梁2の位置関係（STEP2結論・収納時）', size=18, bold=True)
txt(40, 62, '作成 %s　部屋座標・単位cm。中心x=139.45、右側面x=%s（梁2内面x=170との間 c3=2）、収納d1=48.5、チルト24°、h=%s〜%s。保持具は0で図示' % (TS, f(XR), f(LOW), f(TOP)), size=12)

# 正面図（拡大）
FV = V(60, 110, 148, 272, 15)
txt(60, 100, '正面図（LP側から−d方向を見る）梁2付近の拡大', size=14, bold=True)
poly(FV, [(XB, HB), (180.5, HB), (180.5, HT), (XB, HT)], col=GRY, fill=GRY, op=0.6)
T_(FV, 175.25, 262, '梁2', anchor='middle', bold=True)
poly(FV, [(148, HT), (184, HT)], col=K, w=2, close=False)
poly(FV, [(148, LOW), (XR, LOW), (XR, TOP), (148, TOP)], col=K, fill='#e8e8e8', close=False)
poly(FV, [(XR, HB), (XR, TOP)], col=RED, w=4, close=False)
poly(FV, [(XR, LOW), (XR, HB)], col=ORG, w=4, close=False)
poly(FV, [(XR, HB), (XB, HB), (XB, TOP), (XR, TOP)], col=RED, fill=RED, op=0.15, w=0.8, dash='3 2')
for hv, lab, col, dsh in [(HT, '掘込面 h=270', K, None), (HB, '梁下面 h=254.5', GRY, '6 3'), (LOW, '収納最下点 h=243.77', BLU, '6 3'), (TOP, '最上点 h=%s' % f(TOP), BLU, '2 3')]:
    poly(FV, [(181, hv), (184, hv)], col=col, w=1.1, dash=dsh, close=False); T_(FV, 184, hv, lab, dx=6, dy=4, col=col, size=12)
dim_v(FV, 200, HB, TOP, '梁と重なる高さ %s' % f(TOP - HB), RED)
dim_v(FV, 200, LOW, HB, '梁下面より下 %s' % f(HB - LOW), ORG)
T_(FV, 156, 256, 'CSP（右端部）', anchor='middle')
T_(FV, (XR + XB) / 2, TOP + 0.6, '間2', anchor='middle', col=RED, size=12, bold=True)
T_(FV, XR - 0.3, (HB + TOP) / 2, '保持具なし（A03-002）', anchor='end', col=RED, size=12)
T_(FV, XR - 0.3, (LOW + HB) / 2, '右側に出せる', anchor='end', col=ORG, size=12)

# 側面図：右側面のうち梁と重なる部分
SV = V(1130, 110, 42, 272, 10)
txt(1130, 100, '側面図（+x方向を見る）CSP右側面の内訳', size=14, bold=True)
poly(SV, [(42, HT), (96, HT)], col=K, w=2, close=False)
poly(SV, [(42, HC), (45.5, HC), (45.5, HT)], col=K, w=2, close=False)
poly(SV, [(42, HB), (96, HB)], col=GRY, w=1.1, dash='6 3', close=False)
T_(SV, 96, HB, '梁下面 h=254.5', dx=4, dy=4, col=GRY, size=12)
poly(SV, [P0, P1, P3, P2], col=K, fill='#e8e8e8')
poly(SV, [Q2, Q1, P3, P2], col=RED, fill=RED, op=0.3, w=1)
poly(SV, [P0, P1, Q1, Q2], col=ORG, fill=ORG, op=0.35, w=1)
for p, lab, dx, dy in [(P0, 'P0', -8, 4), (P1, 'P1', -4, 16), (P2, 'P2', -4, -6), (P3, 'P3', 6, 0)]:
    T_(SV, *p, lab, dx=dx, dy=dy, anchor='end' if dx < 0 else 'start')
# 面積
def area(pts): return abs(sum(pts[i][0]*pts[(i+1)%len(pts)][1]-pts[(i+1)%len(pts)][0]*pts[i][1] for i in range(len(pts))))/2
A_all = D * H; A_up = area([Q2, Q1, P3, P2])
T_(SV, 42, 238, '橙：梁下面より下（右に出せる）', col=ORG, size=12)
T_(SV, 42, 236, '赤：梁と重なる（保持具なし）', col=RED, size=12)

NX, NY = 1130, 520
txt(NX, NY, '■ 現在の前提（STEP2結論）', bold=True, size=14)
NOTES = [
    '・CSP右側面 x=%s、梁2内面 x=170 → 間は c3=2（仮の余裕）' % f(XR),
    '・右側面のうち梁と重なる高さ：h=254.5〜%s（%s）' % (f(TOP), f(TOP - HB)),
    '　この範囲は右側に保持具を出さない（A03-002）',
    '・梁下面より下：h=%s〜254.5（%s）は右側に出せる' % (f(LOW), f(HB - LOW)),
    '・右側面の面積のうち梁と重なる割合：%.0f%%' % (A_up / A_all * 100),
    '・「密着」ではなく間2だが、その間2は余裕寸法で',
    '　保持具には使えない',
]
for i, t_ in enumerate(NOTES): txt(NX, NY + 26 + i * 22, t_, size=13)
Wc, Hc = 1840, 760
svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" font-family="Noto Sans CJK JP, Hiragino Sans, Meiryo, sans-serif">' % (Wc, Hc, Wc, Hc),
       '<rect width="100%" height="100%" fill="white"/>'] + out + ['</svg>']
open(sys.argv[1], 'w', encoding='utf-8').write('\n'.join(svg))
print('TOP', TOP, 'Q1', Q1, 'Q2', Q2, 'ratio', A_up / A_all)
