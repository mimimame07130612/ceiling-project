# K018 収納姿勢の比較 A（水平に戻す）／B（チルト維持・h=245をΔ下げる）（STEP2 2-5）
# 保持の基本形：底面の部分支持板（K016：P0から支持率r、厚さt下）＋前面上角の爪（K017：上面側a′、前面側b′）。
# 収納時の高さ条件（h=245〜270）と奥行条件（収納帯 d=45.5〜配光118°境界）から、必要なΔを求める。
# 入力：A01-001、A02-002、A02-003、A00-001（h=245、交渉可）、A02-001（h=270）、A00-006（118°）、D00-005・D00-006（照明）、
#       A02-005（収納帯）、K015、K016、K017
# 使い方：python3 本ファイル <出力svgパス>
import math, sys, html
D, H, T = 21.4, 17.0, math.radians(24)
c, s = math.cos(T), math.sin(T)
TS = '2609280017'
TAN59 = math.tan(math.radians(59)); LED_R = 11.4 / 2; LED_D = 130
def dh(u, w): return (u * c + w * s, -u * s + w * c)
TOP = dh(0, H)[1]
def band(delta):                       # 収納下端 h=245−Δ での配光境界（d方向）と収納帯の奥行
    edge = LED_D - ((270 - (245 - delta)) * TAN59 + LED_R)
    return edge, edge - 45.5
def dB(r, t): return max(0.0, (r * D * s + t * c) - (25 - TOP))
def dA(t, a): return max(0.0, H + t + a - 25)
def extB(t, a, b): return (dh(D, H)[0] + b * c + a * s) + t * s
def extA(b): return D + b

e = html.escape
out = []
K, RED, GRN, GRY, BLU, ORG, PUR = '#333333', '#C0392B', '#2E9E6B', '#8a857a', '#2C6FB0', '#D35400', '#6A5FD0'
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

# 例示値（値ではなく図示用）
r0, t0, a0, b0 = 0.7, 2.0, 1.0, 1.0

txt(40, 40, 'K018　収納姿勢の比較：A 水平に戻す／B チルト維持（STEP2 2-5）', size=18, bold=True)
txt(40, 62, '作成 %s　保持の基本形＝底面の部分支持板（K016）＋前面上角の爪（K017）。側面図（左がSC側、右がLP側）。単位cm' % TS, size=12)
txt(40, 82, '(図は例示：r=%.1f、t下=%g、爪 a′=%g・b′=%g。数値の比較は右の表)' % (r0, t0, a0, b0), size=12, col='#444')

def hlines(v, u0, u1):
    for hv, lab, col, dsh in [(270, '掘込面 h=270', K, None), (250, '天井面 h=250（d<45.5）', GRY, '3 3'), (245, '収納下限 h=245（A00-001）', BLU, '6 3')]:
        poly(v, [(u0, hv), (u1, hv)], col=col, w=1.1, dash=dsh, close=False)
        T_(v, u1, hv, lab, dx=6, dy=4, col=col)

# ---------- A：水平（下面をh=245に置く） ----------
VA = V(60, 150, -6, 274, 11)
txt(60, 130, 'A：収納時だけ水平に戻す（動作中に24°回転）', size=14, bold=True)
base = 245 + t0
poly(VA, [(0, base), (D, base), (D, base + H), (0, base + H)], fill='#f2f2f2')
poly(VA, [(D, base), (D, base + H)], col=RED, w=4, close=False)
poly(VA, [(0, 245), (r0 * D, 245), (r0 * D, base), (0, base)], col=GRN, fill=GRN, op=0.35)
poly(VA, [(D - 3, base + H), (D - 3, base + H + a0), (D + b0, base + H + a0), (D + b0, base + H - 4), (D, base + H - 4), (D, base + H)], col=GRN, fill=GRN, op=0.35)
hlines(VA, -6, 30)
T_(VA, D / 2, base + H / 2, 'CSP（水平）', anchor='middle')
T_(VA, 0, 245, '支持板 t下', dx=-6, dy=-2, anchor='end', col=GRN)
T_(VA, D + b0, base + H + a0, '爪 a′ が高さに効く', dx=6, dy=-6, col=GRN)
T_(VA, 0, 245, '高さ ＝ 17 + t下 + a′ ≦ 25 + Δ', dy=36)
T_(VA, 0, 245, '例示：17+2+1＝20 → すき間5（Δ=0）', dy=56, col='#444')

# ---------- B：チルト維持 ----------
VB = V(620, 150, -6, 274, 11)
txt(620, 130, 'B：チルト24°維持（必要ならh=245をΔ下げる）', size=14, bold=True)
low_rel = min(dh(D, 0)[1], dh(r0 * D, -t0)[1])
off = 245 - low_rel
def dhB(u, w): p = dh(u, w); return (p[0], p[1] + off)
poly(VB, [dhB(0, 0), dhB(D, 0), dhB(D, H), dhB(0, H)], fill='#f2f2f2')
poly(VB, [dhB(D, 0), dhB(D, H)], col=RED, w=4, close=False)
poly(VB, [dhB(0, 0), dhB(r0 * D, 0), dhB(r0 * D, -t0), dhB(0, -t0)], col=GRN, fill=GRN, op=0.35)
poly(VB, [dhB(D - 3, H), dhB(D, H), dhB(D, H - 4), dhB(D + b0, H - 4), dhB(D + b0, H + a0), dhB(D - 3, H + a0)], col=GRN, fill=GRN, op=0.35)
hlines(VB, -6, 30)
T_(VB, *dhB(D / 2, H / 2), 'CSP（24°）', anchor='middle')
T_(VB, *dhB(0, -t0), '支持板 t下', dx=-6, dy=4, anchor='end', col=GRN)
T_(VB, *dhB(D + b0, H + a0), '爪（上角）', dx=6, dy=0, col=GRN)
T_(VB, -6, 245, '最下点 ＝ P1 と 支持板の角 の低い方', dy=36)
T_(VB, -6, 245, '例示：最上点 h=%.2f（掘込面まで %.2f）→ Δ=0' % (TOP - low_rel + 245, 270 - (TOP - low_rel + 245)), dy=56, col='#444')

# ---------- 表 ----------
TX, TY = 1180, 130
txt(TX, TY, '■ 必要なΔ（h=245からの下げ量、計算、余裕寸法0）', bold=True, size=14)
hdr = ['t下', 'B r=0.5', 'B r=0.7', 'B r=1.0', "A a′=0", "A a′=1"]
cw = [60, 80, 80, 80, 80, 80]
y = TY + 28; x = TX
for h_, w_ in zip(hdr, cw): txt(x, y, h_, bold=True); x += w_
for t in (1, 2, 3, 4, 5, 6, 8):
    y += 21; x = TX
    vals = ['%g' % t] + ['%.2f' % dB(r, t) for r in (0.5, 0.7, 1.0)] + ['%.2f' % dA(t, a) for a in (0, 1)]
    for v, w_ in zip(vals, cw):
        txt(x, y, v, col=('#222' if v in ('0.00',) or x == TX else ORG)); x += w_
y += 30
txt(TX, y, '■ 収納帯の奥行（配光118°の境界がΔで前に出る）', bold=True, size=14)
for i, dl in enumerate((0, 1, 2, 3, 5)):
    ed, wd = band(dl)
    txt(TX + 10, y + 22 + i * 20, 'Δ=%g：配光境界 d=%.1f、収納帯の奥行 %.1f' % (dl, ed, wd))
y += 22 + 5 * 20 + 14
txt(TX, y, '■ 保持外形の奥行（収納帯に入る必要がある）', bold=True, size=14)
LL = ['B：26.46 + t下·%.3f + b′·%.3f + a′·%.3f（例示 %.1f）' % (s, c, s, extB(t0, a0, b0)),
      'A：21.4 + b′（例示 %.1f）' % extA(b0),
      '※ ワンモーション移動の条件（d1≧46.2、K013）は外形が変わるため再計算が必要']
for i, t_ in enumerate(LL): txt(TX + 10, y + 22 + i * 20, t_, col='#444' if t_.startswith('※') else '#222')
y += 22 + 3 * 20 + 14
txt(TX, y, '■ 式', bold=True, size=14)
LL = ['B：Δ ＝ max(0, r·D·sin24° + t下·cos24° − %.2f)　［%.2f＝D·sin24°＋すき間0.77］' % (25 - TOP, 25 - TOP),
      '　　上角の爪はΔに効かない（K017）',
      'A：Δ ＝ max(0, 17 + t下 + a′ − 25)　水平では上角の爪の a′ が高さに効く',
      '　　動作中に24°回転させる機構が必要（複雑さはSTEP4の方式による）',
      '共通：保持具と昇降機構をつなぐ部分の外形は含まない（左右の余裕 23.4、K015式③）']
for i, t_ in enumerate(LL): txt(TX + 10, y + 22 + i * 20, t_, col='#444' if t_.startswith('　') else '#222')

Wc, Hc = 1880, 700
svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" font-family="Noto Sans CJK JP, Hiragino Sans, Meiryo, sans-serif">' % (Wc, Hc, Wc, Hc),
       '<rect width="100%" height="100%" fill="white"/>'] + out + ['</svg>']
open(sys.argv[1], 'w', encoding='utf-8').write('\n'.join(svg))
for t in (1, 2, 3, 4, 5, 6, 8): print(t, ['%.2f' % dB(r, t) for r in (0.5, 0.7, 1.0)], ['%.2f' % dA(t, a) for a in (0, 1)])
for dl in (0, 1, 2, 3, 5): print(dl, ['%.1f' % v for v in band(dl)])
print('extB', extB(t0, a0, b0), 'topB', TOP - min(dh(D, 0)[1], dh(r0 * D, -t0)[1]))
