# K028 CSPの左右の支持と設置エリア幅の関係（M03-008見直し用）
# 片側（左）だけで支える場合のモーメントと、両側で支える場合に必要な左右の空きを正面図で示す。
# 入力：A01-001（W57.1、7.90kg）、D01-009（梁1内面x=89.5、梁2内面x=170）、梁下面h=254.5、掘込面h=270、
#       A00-001（h=243.77）、A03-003（余裕2）、A03-004（中心x=139.45）、LP中央x=169（部屋.xlsx）
# リンクの幅wは未定（STEP4）のため変数として扱う。CSPの重心は左右中央と仮定（資料なし）。
# 使い方：python3 本ファイル <出力svgパス> <タイムスタンプ>
import sys, html
TS = sys.argv[2]
W, M, G = 57.1, 7.90, 9.81
XB1, XB2, HB, HT, HC, LOW, TOP, LPC, C = 89.5, 170.0, 254.5, 270.0, 250.0, 243.77, 268.0, 169.0, 2.0
AREA = XB2 - XB1
e = html.escape; out = []
K, RED, GRN, GRY, BLU, ORG, PUR = '#333333', '#C0392B', '#2E9E6B', '#8a857a', '#2C6FB0', '#D35400', '#6A5FD0'
def f(n): return ('%.2f' % n).rstrip('0').rstrip('.')
class V:
    def __init__(s, ox, oy, u0, v1, sc): s.ox, s.oy, s.u0, s.v1, s.sc = ox, oy, u0, v1, sc
    def X(s, u): return s.ox + (u - s.u0) * s.sc
    def Y(s, v): return s.oy + (s.v1 - v) * s.sc
def rect(v, x0, x1, h0, h1, col=K, fill='none', op=1, w=1.2, dash=None):
    out.append('<rect x="%s" y="%s" width="%s" height="%s" fill="%s" fill-opacity="%s" stroke="%s" stroke-width="%s"%s/>' % (
        f(v.X(x0)), f(v.Y(h1)), f((x1 - x0) * v.sc), f((h1 - h0) * v.sc), fill, op, col, w, ' stroke-dasharray="%s"' % dash if dash else ''))
def line(v, a, b, col=K, w=1.2, dash=None):
    out.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s"%s/>' % (
        f(v.X(a[0])), f(v.Y(a[1])), f(v.X(b[0])), f(v.Y(b[1])), col, w, ' stroke-dasharray="%s"' % dash if dash else ''))
def txt(x, y, t, col='#222', anchor='start', size=13, bold=False):
    out.append('<text x="%s" y="%s" fill="%s" text-anchor="%s" font-size="%s"%s>%s</text>' % (
        f(x), f(y), col, anchor, size, ' font-weight="bold"' if bold else '', e(t)))
def T_(v, a, b, t, dx=0, dy=0, **k): txt(v.X(a) + dx, v.Y(b) + dy, t, **k)
def room(v):
    for a0, a1, lab in [(79, XB1, '梁1'), (XB2, 180.5, '梁2')]:
        rect(v, a0, a1, HB, HT, col=GRY, fill=GRY, op=0.6); T_(v, (a0 + a1) / 2, 262, lab, anchor='middle', size=11, bold=True)
    line(v, (75, HT), (185, HT), w=2)
    line(v, (75, HB), (185, HB), col=GRY, dash='6 3', w=0.8)
    line(v, (75, LOW), (185, LOW), col=BLU, dash='6 3', w=0.8)
    line(v, (LPC, 238), (LPC, 272), col=PUR, dash='2 3', w=1)
    T_(v, LPC, 238, 'LP中央 169', dy=12, dx=3, col=PUR, size=10)
def csp(v, xc):
    rect(v, xc - W / 2, xc + W / 2, LOW, TOP, fill='#e8e8e8'); T_(v, xc, 257, 'CSP 中心x=%s' % f(xc), anchor='middle', size=11)
    T_(v, xc, 253, 'LP中央とのずれ %s' % f(LPC - xc), anchor='middle', size=11, col=PUR)
def arrow_down(v, x, h0, h1, col):
    line(v, (x, h0), (x, h1), col=col, w=2)
    out.append('<polygon points="%s,%s %s,%s %s,%s" fill="%s"/>' % (f(v.X(x) - 5), f(v.Y(h1) - 8), f(v.X(x) + 5), f(v.Y(h1) - 8), f(v.X(x)), f(v.Y(h1)), col))

txt(40, 40, 'K028　CSPの左右の支持と設置エリア幅の関係（M03-008の見直し）', size=18, bold=True)
txt(40, 62, '作成 %s　正面図（LP側から−d方向を見る）・収納時・単位cm。設置エリア x=89.5〜170（幅80.5）。リンク幅 w は未定（STEP4）のため変数。重心は左右中央と仮定（資料なし）' % TS, size=12)
SC_, U0, V1 = 6.2, 75, 274
# A：現状（左だけ）
xa = XB2 - C - W / 2
va = V(40, 110, U0, V1, SC_)
txt(40, 100, 'A　現状：左側だけで支える（A03-002・A03-004）', size=14, bold=True)
room(va); csp(va, xa)
wl = xa - W / 2 - C - XB1
rect(va, XB1 + C, xa - W / 2, LOW, TOP, col=GRN, fill=GRN, op=0.25, dash='4 3')
T_(va, (XB1 + xa - W / 2) / 2, 246, '左の空き', anchor='middle', col=GRN, size=10)
T_(va, (XB1 + xa - W / 2) / 2, 244.6, f(wl), anchor='middle', col=GRN, size=10)
arrow_down(va, xa, 250, 245.5, RED)
arm = W / 2
Mo = M * G * arm / 100
T_(va, xa, 241, '左側面での曲げモーメント 約 %.1f N·m（7.90kg×9.81×%s cm、保持具の質量は含まない）' % (Mo, f(arm)), anchor='middle', col=RED, size=11)
T_(va, xa, 239.3, '＋左右の重さの偏りでCSPが右下がりに傾こうとする（たわみ量はリンクの剛性しだい＝STEP4）', anchor='middle', col=RED, size=11)

# B：両側に同じ幅 w
wmax = (AREA - W - 4 * C) / 2
vb = V(40, 450, U0, V1, SC_)
txt(40, 440, 'B　両側で支える：左右に同じ幅 w（例 w=%s＝上限）' % f(wmax), size=14, bold=True)
room(vb)
xb = XB2 - C - wmax - C - W / 2
csp(vb, xb)
for a0 in (xb - W / 2 - C - wmax, xb + W / 2 + C):
    rect(vb, a0, a0 + wmax, LOW, TOP, col=ORG, fill=ORG, op=0.3, dash='4 3')
T_(vb, xb + W / 2 + C + wmax / 2, 246, 'w', anchor='middle', col=ORG, bold=True)
T_(vb, xb - W / 2 - C - wmax / 2, 246, 'w', anchor='middle', col=ORG, bold=True)
T_(vb, xb, 241, '条件：57.1 + 2w + 余裕2×4 ≦ 80.5 → w ≦ %s' % f(wmax), anchor='middle', col=ORG, size=11)

# 表
NX, NY = 830, 110
txt(NX, NY, '■ 右側にリンク（幅w、両側に余裕2）を置く場合', bold=True, size=14)
hdr = ['右のw', '右の空き(w+4)', 'CSP中心x', 'LP中央とのずれ', '左の空き(余裕2除く)']
cols = [NX, NX + 70, NX + 180, NX + 270, NX + 390]
for c_, h_ in zip(cols, hdr): txt(c_, NY + 28, h_, size=12, bold=True)
rows = []
for w in [0, 2, 4, 6, 7.7, 10, 12, 15]:
    g = (w + 2 * C) if w > 0 else C
    xc = XB2 - g - W / 2
    left = xc - W / 2 - C - XB1
    rows.append((w, g, xc, LPC - xc, left))
for i, (w, g, xc, dv, left) in enumerate(rows):
    y = NY + 52 + i * 22
    col = RED if left < 0 else ('#222' if w else GRY)
    for c_, v_ in zip(cols, [f(w) if w else '0（現状）', f(g), f(xc), f(dv), f(left) + (' ×' if left < 0 else '')]): txt(c_, y, v_, size=12, col=col)
yy = NY + 52 + len(rows) * 22 + 16
NOTES = [
    '・右にリンクを置く分だけCSPが左に寄り、LP中央とのずれは w+2 増える',
    '・左右とも同じ幅wなら w≦%s。左右の空きを使い切る' % f(wmax),
    '・左の空きは右のwを使った残り。左のリンク幅もここに入る必要がある',
    '・リンクの幅wは機構しだいで、いまは値がない（STEP4）',
    '・梁下面より下（h=243.77〜254.5）は梁がないので右に出せる（K027）',
    '　→ 右のリンクを梁下面より下だけに収められるならCSPは寄せたまま',
    '　　ただし収まるかどうかは機構の形しだい（STEP4）',
]
for i, t_ in enumerate(NOTES): txt(NX, yy + i * 21, t_, size=12)
Wc, Hc = 1400, 800
svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" font-family="Noto Sans CJK JP, Hiragino Sans, Meiryo, sans-serif">' % (Wc, Hc, Wc, Hc),
       '<rect width="100%" height="100%" fill="white"/>'] + out + ['</svg>']
open(sys.argv[1], 'w', encoding='utf-8').write('\n'.join(svg))
print('Mo', Mo, 'wmax', wmax, 'wl', wl); [print(r) for r in rows]
