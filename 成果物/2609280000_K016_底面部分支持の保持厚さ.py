# K016 底面部分支持の保持厚さ（STEP2 2-5）
# チルト24°のCSP底面を、P0（SC側下角）から支持率rの範囲だけ厚さt下の板で支える場合の、t下の上限を求める。
# 入力：A01-001（D21.4・H17.0）、A02-002（24°）、A02-003（収納時チルト維持）、A00-001（h=245）、A02-001（h=270）
# 座標：CSP基準の相対座標（P0を原点、d・h）。単位cm。
# 使い方：python3 本ファイル <出力svgパス>
import math, sys, html
D, H, T = 21.4, 17.0, math.radians(24)
c, s = math.cos(T), math.sin(T)
TS = '2609280000'
AV = 270 - 245                       # 収納時に使える高さ
def dh(u, w): return (u * c + w * s, -u * s + w * c)
TOP = dh(0, H)[1]                    # P2（最上点）15.53
P1 = dh(D, 0)[1]                     # P1（最下点）−8.70
LOW = TOP - AV                       # 許される最下点 −9.47
def tmax(r):   return (-r * D * s - LOW) / c        # すき間0.77も使った上限
def tfree(r):  return (1 - r) * D * s / c            # 最下点P1を下げない上限
CGd = dh(D / 2, H / 2)[0]            # 均質と仮定した重心のd

rows = [(r, tfree(r), tmax(r), dh(r * D, 0)[0]) for r in (0.5, 0.6, 0.7, 0.8, 0.9, 1.0)]

S = 12
e = html.escape
out = []
K, RED, GRN, GRY, BLU, ORG = '#333333', '#C0392B', '#2E9E6B', '#8a857a', '#2C6FB0', '#D35400'
def f(n): return ('%.1f' % n).rstrip('0').rstrip('.')
OX, OY, U0, V1 = 170, 130, -6, 20
def X(u): return OX + (u - U0) * S
def Y(v): return OY + (V1 - v) * S
def poly(pts, col=K, w=1.4, fill='none', op=1, dash=None, close=True):
    tag = 'polygon' if close else 'polyline'
    out.append('<%s points="%s" fill="%s" fill-opacity="%s" stroke="%s" stroke-width="%s"%s/>' % (
        tag, ' '.join('%s,%s' % (f(X(a)), f(Y(b))) for a, b in pts), fill, op, col, w,
        ' stroke-dasharray="%s"' % dash if dash else ''))
def txt(x, y, t, col='#222', anchor='start', size=13, bold=False):
    out.append('<text x="%s" y="%s" fill="%s" text-anchor="%s" font-size="%s"%s>%s</text>' % (
        f(x), f(y), col, anchor, size, ' font-weight="bold"' if bold else '', e(t)))
def T_(a, b, t, dx=0, dy=0, **k): txt(X(a) + dx, Y(b) + dy, t, **k)
def hline(v, col, lab, dash=None):
    poly([(-6, v), (28, v)], col=col, w=1.2, dash=dash, close=False); T_(28, v, lab, dx=6, dy=4, col=col)

txt(40, 40, 'K016　底面部分支持の保持厚さ（STEP2 2-5）', size=18, bold=True)
txt(40, 62, '作成 %s　側面図（左がSC側、右がLP側）。CSP単体・チルト24°・収納時（A02-003）。座標はCSP基準（P0原点）。単位cm' % TS, size=12)
txt(40, 82, '例示：支持率 r=0.7（P0から底面の70%%）、t下=%.2f（すき間0.77も使い切った上限）' % tmax(0.7), size=12, col=GRN)

r, t = 0.7, tmax(0.7)
poly([dh(0, 0), dh(D, 0), dh(D, H), dh(0, H)], fill='#f2f2f2')
poly([dh(D, 0), dh(D, H)], col=RED, w=4, close=False)
poly([dh(0, 0), dh(r * D, 0), dh(r * D, -t), dh(0, -t)], col=GRN, fill=GRN, op=0.3, w=1.6)
hline(TOP, K, 'P2（最上点）＝掘込面h=270に対応')
poly([(-6, P1), (28, P1)], col=GRY, w=1.2, dash='6 3', close=False); T_(-6, P1, 'P1（CSP最下点）', dx=-6, dy=4, anchor='end', col=GRY)
hline(LOW, BLU, '許される最下点＝h=245に対応（P2−25）', dash='6 3')
pc = dh(r * D, -t)
out.append('<circle cx="%s" cy="%s" r="4" fill="%s"/>' % (f(X(pc[0])), f(Y(pc[1])), GRN))
T_(pc[0], pc[1], '板の最下点', dx=-8, dy=18, anchor='end', col=GRN)
T_(*dh(0, 0), 'P0', dx=-8, dy=-4, anchor='end')
T_(*dh(D, 0), 'P1', dx=6, dy=16)
T_(*dh(0, H), 'P2', dx=-8, dy=-6, anchor='end')
T_(*dh(D, H / 2), '前面', dx=10, col=RED)
T_(*dh(0, -t), '支持板（0.7D=%.1f）' % (r * D), dx=-8, dy=4, anchor='end', col=GRN)
# 重心（均質仮定）
cg = dh(D / 2, H / 2)
out.append('<circle cx="%s" cy="%s" r="5" fill="none" stroke="%s" stroke-width="2"/>' % (f(X(cg[0])), f(Y(cg[1])), ORG))
poly([cg, (cg[0], LOW - 3)], col=ORG, w=1.2, dash='3 3', close=False)
pe = dh(r * D, 0)
poly([pe, (pe[0], LOW - 3)], col=GRN, w=1.2, dash='3 3', close=False)
T_(cg[0], LOW - 3, '(重心 d=%.2f)' % CGd, dx=-4, dy=16, anchor='end', col=ORG)
T_(pe[0], LOW - 3, '支持端 d=%.2f' % pe[0], dx=4, dy=16, col=GRN)
T_(*cg, '(重心・均質仮定)', dx=8, dy=-6, col=ORG)
# 下り方向
T_(*dh(D, 0), '↘ 底面の下り方向（LP側・前面側）', dx=14, dy=-40, col=BLU)

# 表
TX, TY = 900, 150
txt(TX, TY, '■ 支持率 r と t下 の上限（計算、余裕寸法0）', bold=True, size=14)
hdr = ['支持率 r', 'P1を下げない上限', 'すき間0.77も使う上限', '支持端 d']
cw = [80, 150, 170, 90]
y = TY + 30
x = TX
for h_, w_ in zip(hdr, cw): txt(x, y, h_, bold=True); x += w_
for r_, a, b, pd in rows:
    y += 22; x = TX
    for v, w_ in zip(['%.1f' % r_, '%.2f' % a, '%.2f' % b, '%.2f' % pd], cw):
        txt(x, y, v, col=GRN if abs(r_ - 0.7) < 1e-9 else '#222'); x += w_
y += 34
for i, t_ in enumerate([
        '式：t下 ≦ ((1−r)·D·sin24° + 0.77) / cos24°',
        '　　r=1.0（全面）で0.84 → K015の式①（t前=t後=t上=0）と一致',
        '　　「P1を下げない上限」＝(1−r)·D·tan24°。板の最下点がP1と同じ高さになる厚さ',
        '前提：板は底面に沿ってP0から始まる。t上・t前・t後・t左・t右は0',
        '重心：CSPの質量分布の資料はないため、均質と仮定した参考位置',
        '　　r=0.7のとき、支持端と重心（均質仮定）のd方向の差は%.2f' % (dh(0.7 * D, 0)[0] - CGd),
        '底面は24°傾いているため、板の上のCSPには下り方向（LP側）への力がかかる']):
    txt(TX, y + i * 20, t_, col='#444' if t_.startswith('　') else '#222')

Wc, Hc = 1480, 640
svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" font-family="Noto Sans CJK JP, Hiragino Sans, Meiryo, sans-serif">' % (Wc, Hc, Wc, Hc),
       '<rect width="100%" height="100%" fill="white"/>'] + out + ['</svg>']
open(sys.argv[1], 'w', encoding='utf-8').write('\n'.join(svg))
for r_ in rows: print(['%.2f' % v for v in r_])
print('CGd %.2f' % CGd)
