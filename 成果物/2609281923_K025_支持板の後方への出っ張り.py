# K025 支持板の後方への出っ張り（STEP2 2-2 説明図）
# チルト24°のCSP底面に、底面と直角な厚さ t下 の支持板を付けると、支持板の後端がP0よりSC側へ t下·sin24° 出ることを示す。
# 入力：A01-001、A02-002（24°）、A02-004（SC幕面とのすき間8）、K016、K024
# 使い方：python3 本ファイル <出力svgパス>
import math, sys, html
D, H, T = 21.4, 17.0, math.radians(24)
c, s = math.cos(T), math.sin(T)
TS = '2609281923'
TP, R = 2.86, 0.7
def dh(u, w): return (u * c + w * s, -u * s + w * c)
e = html.escape; out = []
K, RED, GRN, GRY, BLU, ORG, MAG = '#333333', '#C0392B', '#2E9E6B', '#8a857a', '#2C6FB0', '#D35400', '#C8307A'
def f(n): return ('%.2f' % n).rstrip('0').rstrip('.')
class V:
    def __init__(s_, ox, oy, u0, v1, sc): s_.ox, s_.oy, s_.u0, s_.v1, s_.sc = ox, oy, u0, v1, sc
    def X(s_, u): return s_.ox + (u - s_.u0) * s_.sc
    def Y(s_, v): return s_.oy + (s_.v1 - v) * s_.sc
def pl(v, pts, col=K, w=1.4, fill='none', op=1, dash=None, close=True):
    tag = 'polygon' if close else 'polyline'
    out.append('<%s points="%s" fill="%s" fill-opacity="%s" stroke="%s" stroke-width="%s"%s/>' % (
        tag, ' '.join('%s,%s' % (f(v.X(a)), f(v.Y(b))) for a, b in pts), fill, op, col, w,
        ' stroke-dasharray="%s"' % dash if dash else ''))
def txt(x, y, t, col='#222', anchor='start', size=14, bold=False):
    out.append('<text x="%s" y="%s" fill="%s" text-anchor="%s" font-size="%s"%s>%s</text>' % (
        f(x), f(y), col, anchor, size, ' font-weight="bold"' if bold else '', e(t)))
def T_(v, a, b, t, dx=0, dy=0, **k): txt(v.X(a) + dx, v.Y(b) + dy, t, **k)
def dot(v, p, col):
    out.append('<circle cx="%s" cy="%s" r="4.5" fill="%s"/>' % (f(v.X(p[0])), f(v.Y(p[1])), col))

txt(40, 40, 'K025　支持板の後方への出っ張り（STEP2 2-2 説明図）', size=18, bold=True)
txt(40, 62, '作成 %s　側面図（左がSC側、右がLP側）。CSP基準の相対座標（P0原点）。単位cm。支持板は t下=%.2f、r=%.1f（K024の上限）で図示' % (TS, TP, R), size=12)

# ---------- 左：全体 ----------
A = V(80, 110, -12, 20, 13)
txt(80, 100, '① 全体（使用位置の近く）', size=15, bold=True)
SC = -1.16 - 8   # 支持板後端からすき間8のSC幕面（相対）
pl(A, [(SC, -12), (SC, 20)], col=K, w=3, close=False); T_(A, SC, 18, 'SC幕面', dx=-6, anchor='end')
pl(A, [dh(0, 0), dh(D, 0), dh(D, H), dh(0, H)], fill='#eeeeee')
pl(A, [dh(D, 0), dh(D, H)], col=RED, w=4, close=False)
pl(A, [dh(0, 0), dh(R * D, 0), dh(R * D, -TP), dh(0, -TP)], col=GRN, fill=GRN, op=0.35, w=1.6)
pl(A, [dh(0, H), dh(0, -TP - 2)], col=BLU, w=1.2, dash='5 3', close=False)
T_(A, *dh(0, -TP - 2), '背面をそのまま下に延ばした線', dx=-6, dy=14, anchor='end', col=BLU, size=12)
dot(A, dh(0, 0), K); T_(A, *dh(0, 0), 'P0（背面の最後端）', dx=10, dy=4, size=13)
dot(A, dh(0, -TP), MAG); T_(A, *dh(0, -TP), '支持板の後端', dx=10, dy=16, col=MAG, size=13)
T_(A, *dh(D / 2, H / 2), 'CSP（24°）', anchor='middle')
T_(A, *dh(R * D / 2, -TP / 2), '支持板', dy=4, anchor='middle', col=GRN, size=13)
# ズーム枠
zx0, zy0, zx1, zy1 = -3.2, -4.2, 2.2, 1.6
pl(A, [(zx0, zy0), (zx1, zy0), (zx1, zy1), (zx0, zy1)], col=ORG, w=1.2, dash='3 3')
T_(A, zx1, zy1, '②で拡大', dx=4, dy=-4, col=ORG, size=12)

# ---------- 右：拡大 ----------
B = V(620, 130, -3.6, 2.2, 62)
txt(620, 100, '② P0まわりの拡大', size=15, bold=True)
pl(B, [dh(0, 0), dh(3.6, 0), dh(3.6, 2.0), dh(0, 2.0)], fill='#eeeeee', w=1.6)
pl(B, [dh(0, 0), dh(3.6, 0), dh(3.6, -TP), dh(0, -TP)], col=GRN, fill=GRN, op=0.3, w=1.6)
pl(B, [dh(0, 2.0), dh(0, -TP - 0.6)], col=BLU, w=1.4, dash='5 3', close=False)
P0 = dh(0, 0); PC = dh(0, -TP)
pl(B, [(P0[0], P0[1]), (P0[0], PC[1])], col=GRY, w=1.2, dash='2 3', close=False)
pl(B, [(PC[0], PC[1]), (P0[0], PC[1])], col=MAG, w=3, close=False)
pl(B, [(P0[0], P0[1]), (PC[0], PC[1])], col=K, w=2.5, close=False)
dot(B, P0, K); dot(B, PC, MAG)
T_(B, *P0, 'P0', dx=10, dy=-6, size=15, bold=True)
T_(B, *PC, '支持板の後端', dx=-12, dy=-8, anchor='end', col=MAG, size=15)
mid = ((P0[0] + PC[0]) / 2, (P0[1] + PC[1]) / 2)
T_(B, *mid, '支持板の厚さ t下', dx=-14, dy=0, anchor='end', size=14)
T_(B, *mid, '（底面に直角＝24°傾いている）', dx=-14, dy=20, anchor='end', size=12, col='#444')
T_(B, (P0[0] + PC[0]) / 2, PC[1], 't下·sin24° ＝ %.2f' % (TP * s), dy=34, anchor='middle', col=MAG, size=15, bold=True)
T_(B, (P0[0] + PC[0]) / 2, PC[1], '（SC側へ出る量）', dy=54, anchor='middle', col=MAG, size=13)
T_(B, P0[0], (P0[1] + PC[1]) / 2, 't下·cos24° ＝ %.2f（下へ出る量）' % (TP * c), dx=10, col=GRY, size=13)
T_(B, *dh(1.8, 1.0), 'CSP', anchor='middle', size=14)
T_(B, *dh(2.2, -TP / 2), '支持板', anchor='middle', col=GRN, size=14)

# ---------- 説明 ----------
NX, NY = 80, 610
L = ['■ なぜSC側に出るのか',
     '　・CSPはLP側を下げて24°傾いているので、背面（SC側の面）は真上ではなく、上がLP側に倒れている',
     '　・支持板は底面にぴったり付くので、厚さの向きは底面に直角＝背面と同じ向き（24°傾いた向き）になる',
     '　・支持板の後端を背面にそろえると、後端は「背面をそのまま下に延ばした線」の上に来る',
     '　・この線は下に行くほどSC側に寄っているので、厚さ t下 の分だけ下がった後端は、P0よりSC側に出る',
     '　　出る量 ＝ t下·sin24° ＝ 0.407·t下（t下=2.86 なら 1.16）',
     '■ 何に効くのか',
     '　・使用位置で、SC幕面に一番近い点がP0ではなく支持板の後端になる',
     '　・SC幕面とのすき間8（A02-004）を守るには、使用d1を 0.407·t下 だけLP側へ出す必要がある（K024）']
for i, t_ in enumerate(L): txt(NX, NY + i * 22, t_, bold=t_.startswith('■'), size=14)
Hc = NY + len(L) * 22 + 20
svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="%d" viewBox="0 0 1100 %d" font-family="Noto Sans CJK JP, Hiragino Sans, Meiryo, sans-serif">' % (Hc, Hc),
       '<rect width="100%" height="100%" fill="white"/>'] + out + ['</svg>']
open(sys.argv[1], 'w', encoding='utf-8').write('\n'.join(svg))
print(TP * s, TP * c)
