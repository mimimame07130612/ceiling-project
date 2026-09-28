# K017 前面の爪掛け位置（STEP2 2-5）
# 前面（バッフル）でドライバ・ポートにかからない範囲と、爪を前面の下角（P1側）／上角（P3側）に掛けた場合の
# 収納時の高さ条件（K015式①）への効き方を示す。
# 入力：A01-001（W57.1・D21.4・H17.0）、A02-002（24°）、A02-003、A00-001（h=245）、A02-001（h=270）、
#       GH/参考資料 SONIK写真（ドライバ・ポート位置は写真からの目安）、K015、K016
# 座標：前面図は前面の局所座標（x：LPから見て左端0、w：底面0）。側面図はCSP基準（P0原点、d・h）。単位cm。
# 使い方：python3 本ファイル <出力svgパス>
import math, sys, html
W, D, H, T = 57.1, 21.4, 17.0, math.radians(24)
c, s = math.cos(T), math.sin(T)
TS = '2609280013'
def dh(u, w): return (u * c + w * s, -u * s + w * c)
TOP = dh(0, H)[1]; P1h = dh(D, 0)[1]; P3 = dh(D, H)
MARGIN = 25 - (TOP - P1h)            # 0.77
WOOF = [(15.3, 8.3, 7.2), (41.7, 8.3, 7.2)]; TWT = (28.6, 7.8, 5.0)
PORTS = [(3.6, 5.3), (51.4, 53.2)]; PW = (4.8, 11.9)
G = 2.0                               # 爪の模式厚さ（値ではない）
e = html.escape
out = []
K, RED, GRN, GRY, BLU, ORG = '#333333', '#C0392B', '#2E9E6B', '#8a857a', '#2C6FB0', '#D35400'
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
def rect(v, a0, b0, a1, b1, **k): poly(v, [(a0, b0), (a1, b0), (a1, b1), (a0, b1)], **k)
def circ(v, a, b, r, col, fill='none', op=1):
    out.append('<circle cx="%s" cy="%s" r="%s" fill="%s" fill-opacity="%s" stroke="%s" stroke-width="1.3"/>' % (
        f(v.X(a)), f(v.Y(b)), f(r * v.sc), fill, op, col))
def txt(x, y, t, col='#222', anchor='start', size=13, bold=False):
    out.append('<text x="%s" y="%s" fill="%s" text-anchor="%s" font-size="%s"%s>%s</text>' % (
        f(x), f(y), col, anchor, size, ' font-weight="bold"' if bold else '', e(t)))
def T_(v, a, b, t, dx=0, dy=0, **k): txt(v.X(a) + dx, v.Y(b) + dy, t, **k)

txt(40, 40, 'K017　前面の爪掛け位置（STEP2 2-5）', size=18, bold=True)
txt(40, 62, '作成 %s　CSP単体。前面のドライバ・ポート位置は写真からの目安（寸法未確認）。単位cm' % TS, size=12)

# ---------- 前面図（局所、傾きなしで正対） ----------
FV = V(60, 120, -3, 19, 16)
txt(60, 105, '前面（正対して見た図。傾きなし）', size=14, bold=True)
rect(FV, 0, 0, W, H, col=RED, w=1.6, fill='#fdf0ee')
# 空き領域（ドライバ外周・ポートにかからない範囲）
wl0 = WOOF[0][0] - WOOF[0][2]; wr1 = WOOF[1][0] + WOOF[1][2]
for (a0, a1) in [(0, PORTS[0][0]), (PORTS[1][1], W)]:
    rect(FV, a0, 0, a1, H, col=GRN, w=0, fill=GRN, op=0.35)
for (a0, a1) in [(PORTS[0][0], PORTS[0][1]), (PORTS[1][0], PORTS[1][1])]:
    rect(FV, a0, 0, a1, PW[0], col=GRN, w=0, fill=GRN, op=0.35)
    rect(FV, a0, PW[1], a1, H, col=GRN, w=0, fill=GRN, op=0.35)
for (a0, a1) in [(PORTS[0][1], wl0), (wr1, PORTS[1][0])]:
    rect(FV, a0, 0, a1, H, col=GRN, w=0, fill=GRN, op=0.35)
for (x0, wc, r) in WOOF: circ(FV, x0, wc, r, RED)
circ(FV, TWT[0], TWT[1], TWT[2], RED)
for (a0, a1) in PORTS: rect(FV, a0, PW[0], a1, PW[1], col=RED, fill=RED, op=0.6)
T_(FV, PORTS[0][1], PW[1], 'ポート高さ %.1f' % (PW[1] - PW[0]), dx=4, dy=-60, col=RED)
T_(FV, 0, 0, '左端の空き x=0〜%.1f（ポート部を除く）' % wl0, dy=20, col=GRN)
T_(FV, W, 0, '右端の空き x=%.1f〜57.1' % wr1, dy=20, anchor='end', col=GRN)
T_(FV, PORTS[0][0], PW[0], 'ポート下 %.1f' % PW[0], dx=-2, dy=36, anchor='end', col=GRN)
T_(FV, PORTS[0][0], H, 'ポート上 %.1f' % (H - PW[1]), dx=-2, dy=-6, anchor='end', col=GRN)
T_(FV, W / 2, H, '上辺（P3側・上角）', dy=-8, anchor='middle')
T_(FV, W / 2, 0, '下辺（P1側・下角＝最下点）', dy=40, anchor='middle')
T_(FV, 0, 0, '緑：ドライバ外周・ポートにかからない範囲（写真からの目安）', dy=60, col=GRN)
T_(FV, 0, 0, 'グリル（前面全体を覆う）の取付方法は資料なし', dy=80, col='#444')

# ---------- 側面図（CSP基準） ----------
SV = V(1180, 120, -6, 20, 13)
txt(1100, 105, '側面図（左がSC側、右がLP側）。チルト24°・収納時', size=14, bold=True)
poly(SV, [dh(0, 0), dh(D, 0), dh(D, H), dh(0, H)], fill='#f2f2f2')
poly(SV, [dh(D, 0), dh(D, H)], col=RED, w=4, close=False)
# 爪（下角）：底面の下 a、前面の前 b、前面を高さ k まで
k = 4.0
clawL = [dh(D - 3, 0), dh(D, 0), dh(D, k), dh(D + G, k), dh(D + G, -G), dh(D - 3, -G)]
poly(SV, clawL, col=ORG, fill=ORG, op=0.4, w=1.4)
clawU = [dh(D - 3, H), dh(D, H), dh(D, H - k), dh(D + G, H - k), dh(D + G, H + G), dh(D - 3, H + G)]
poly(SV, clawU, col=GRN, fill=GRN, op=0.4, w=1.4)
def hl(v, col, lab, dash=None):
    poly(SV, [(-6, v), (28, v)], col=col, w=1.1, dash=dash, close=False); T_(SV, 28, v, lab, dx=6, dy=4, col=col)
hl(TOP, K, 'P2（最上点）＝h=270に対応')
poly(SV, [(-6, P1h), (28, P1h)], col=GRY, w=1.1, dash='6 3', close=False); T_(SV, -6, P1h, 'P1（最下点）', dx=-6, dy=4, anchor='end', col=GRY)
hl(TOP - 25, BLU, '許される最下点＝h=245に対応', dash='6 3')
pl = dh(D + G, -G)
out.append('<circle cx="%s" cy="%s" r="4" fill="%s"/>' % (f(SV.X(pl[0])), f(SV.Y(pl[1])), ORG))
T_(SV, *dh(D + G, 0), '爪（下角）', dx=10, dy=10, col=ORG)
T_(SV, *dh(D + G, H), '爪（上角）', dx=10, dy=-4, col=GRN)
T_(SV, *dh(0, 0), 'P0', dx=-8, dy=4, anchor='end')
T_(SV, *dh(0, H), 'P2', dx=-8, dy=-4, anchor='end')
T_(SV, *P3, 'P3', dx=-26, dy=-8)
T_(SV, *dh(D, 0), 'P1', dx=-24, dy=14)
T_(SV, -6, TOP - 25, '(爪の厚さは模式、%g で図示)' % G, dy=40, col='#444')

# ---------- 式 ----------
EX, EY = 60, 560
txt(EX, EY, '■ 爪の厚さが収納時の高さ条件（K015式①、すき間%.2f）に効く量（計算、余裕寸法0）' % MARGIN, bold=True, size=14)
L = [
    ('爪（下角）：底面の下の厚さ a、前面の前の厚さ b', ORG),
    ('　最下点がP1から下がる量 ＝ %.3f·a + %.3f·b　→　%.3f·a + %.3f·b ≦ %.2f' % (c, s, c, s, MARGIN), ORG),
    ('　例：a=b=1 で %.2f（すき間を超える）。K016の底面部分支持の板と同じく、最下点に直接効く' % (c + s), ORG),
    ('爪（上角）：上面の上の厚さ a′、前面の前の厚さ b′', GRN),
    ('　上角P3の高さは最上点P2より %.2f 低い → a′·%.3f − b′·%.3f ≦ %.2f までは最上点が上がらない' % (TOP - P3[1], c, s, TOP - P3[1]), GRN),
    ('　奥行（K015式②、余裕10.74）には b′·%.3f + a′·%.3f が効く' % (c, s), GRN),
    ('どちらも前面の空き（左右両端）の範囲に置く前提。ポート開口の近くに物を置いたときの音への影響は資料なし', '#444'),
]
for i, (t, col) in enumerate(L): txt(EX + 10, EY + 24 + i * 20, t, col=col)

Wc, Hc = 1880, 740
svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" font-family="Noto Sans CJK JP, Hiragino Sans, Meiryo, sans-serif">' % (Wc, Hc, Wc, Hc),
       '<rect width="100%" height="100%" fill="white"/>'] + out + ['</svg>']
open(sys.argv[1], 'w', encoding='utf-8').write('\n'.join(svg))
print('margin %.2f  P3h %.2f  TOP-P3 %.2f  wl0 %.1f wr1 %.1f' % (MARGIN, P3[1], TOP - P3[1], wl0, wr1))
