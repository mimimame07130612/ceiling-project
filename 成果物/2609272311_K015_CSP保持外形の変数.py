# K015 CSP保持外形の変数（STEP2 2-5）
# CSP単体（チルト24°）の三面図に、保持具が外形に足す量（6方向の変数）と、面ごとの制約を示す。
# 入力：A01-001（W57.1・D21.4・H17.0）、A02-002（チルト24°、LP側を下げる）、A02-003、A00-001（h=245）、
#       A02-001（掘込面h=270）、A02-005（収納帯）、D01-010・D01-011、GH/参考資料 SONIK写真・取説、依頼主情報（底面）
# 座標：CSP基準の相対座標。P0＝SC側下角を原点、x＝CSP左端（LPから見て左）を0。単位cm。
# 使い方：python3 本ファイル <出力svgパス>
import math, sys, html
W, D, H, T = 57.1, 21.4, 17.0, math.radians(24)
c, s = math.cos(T), math.sin(T)
TS = '2609272311'
e = html.escape

def dh(u, w):  # 局所(u:背面→前面, w:底面→上面) → (d, h)
    return (u * c + w * s, -u * s + w * c)

# ---- 制約式の係数（計算） ----
BD = D * c + H * s          # 外接奥行 26.46
BH = D * s + H * c          # 外接高さ 24.23
H_AVAIL = 270 - 245         # 収納時の高さ方向の空き（A02-001、A00-001）
D_AVAIL = 82.7 - 45.5       # 収納帯の奥行（掘込み前壁〜118°配光境界、A02-005）
X_AVAIL = 170 - 89.5        # 設置エリア幅

S = 10
out = []
K, RED, PUR, GRN, GRY, BLU = '#333333', '#C0392B', '#6A5FD0', '#2E9E6B', '#8a857a', '#2C6FB0'
def f(n): return ('%.1f' % n).rstrip('0').rstrip('.')
class V:
    def __init__(s_, ox, oy, u0, u1, v0, v1, vdown):
        s_.ox, s_.oy, s_.u0, s_.u1, s_.v0, s_.v1, s_.vd = ox, oy, u0, u1, v0, v1, vdown
    def X(s_, u): return s_.ox + (u - s_.u0) * S
    def Y(s_, v): return s_.oy + ((v - s_.v0) * S if s_.vd else (s_.v1 - v) * S)
def poly(v, pts, col=K, w=1.4, fill='none', op=1, dash=None, close=True):
    tag = 'polygon' if close else 'polyline'
    out.append('<%s points="%s" fill="%s" fill-opacity="%s" stroke="%s" stroke-width="%s"%s/>' % (
        tag, ' '.join('%s,%s' % (f(v.X(a)), f(v.Y(b))) for a, b in pts), fill, op, col, w,
        ' stroke-dasharray="%s"' % dash if dash else ''))
def ell(v, cu, cv, rx, ry, col, w=1.2, fill='none', op=1):
    out.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="%s" fill-opacity="%s" stroke="%s" stroke-width="%s"/>' % (
        f(v.X(cu)), f(v.Y(cv)), f(rx * S), f(ry * S), fill, op, col, w))
def txt(x, y, t, col='#222', anchor='start', size=12, bold=False):
    out.append('<text x="%s" y="%s" fill="%s" text-anchor="%s" font-size="%s"%s>%s</text>' % (
        f(x), f(y), col, anchor, size, ' font-weight="bold"' if bold else '', e(t)))
def T_(v, a, b, t, dx=0, dy=0, **k): txt(v.X(a) + dx, v.Y(b) + dy, t, **k)
def arrow(v, a0, b0, a1, b1, col=GRN):
    out.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="1.3" marker-end="url(#ag)"/>' % (
        f(v.X(a0)), f(v.Y(b0)), f(v.X(a1)), f(v.Y(b1)), col))

G = 3.0  # 変数の模式表示量（値ではない）
# 写真からの目安位置（寸法未確認）
WOOF = [(15.3, 8.3, 7.2), (41.7, 8.3, 7.2)]; TWT = (28.6, 7.8, 5.0)
PORTS = [(3.6, 5.3), (51.4, 53.2)]; PORT_W = (4.8, 11.9)
TERM = (23.2, 32.6, 4.8, 12.8)

# ================= 凡例（左上） =================
LX, LY = 40, 40
txt(LX, LY, 'K015　CSP保持外形の変数（STEP2 2-5）', size=18, bold=True)
txt(LX, LY + 22, '作成 %s　CSP単体・チルト24°（A02-002）。座標はCSP基準の相対値（P0＝SC側下角を原点）。単位cm' % TS, size=12)
L = [
    ('CSP外形 W57.1×D21.4×H17.0（A01-001）', K, None),
    ('前面（バッフル）：保持具で覆えない面', RED, None),
    ('背面の端子（ケーブル接続が必要）', PUR, None),
    ('(保持外形：各方向に t を足した外形。線の位置は模式、t=%gで図示)' % G, GRN, '6 3'),
]
for i, (t, col, dash) in enumerate(L):
    y = LY + 56 + i * 22
    out.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2.4"%s/>' % (
        LX, y - 4, LX + 34, y - 4, col, ' stroke-dasharray="%s"' % dash if dash else ''))
    txt(LX + 42, y, t)
y = LY + 56 + 4 * 22 + 12
txt(LX, y, '■ 変数（保持具がCSP外形に足す量）', bold=True, size=13)
for i, t in enumerate(['t上：上面の外側　　t下：底面の外側　　t前：前面の外側　　t後：背面の外側',
                       't左・t右：左右側面の外側（LPから見た左右）',
                       '※ 上下前後はCSPの面に対する向き（24°傾いた向き）で定義']):
    txt(LX + 10, y + 20 + i * 18, t)
y += 20 + 3 * 18 + 16
txt(LX, y, '■ 面ごとの事実', bold=True, size=13)
FACTS = ['前面：ウーファー2・ツイーター1・バスレフポート2（両端）。音の出口が端まである（写真・取説）',
         '背面：端子1か所（中央付近）（写真）',
         '底面：ねじ穴なし、ゴム足のみ（依頼主情報。資料では未確認）',
         '上面：資料なし（写真に写っていない）',
         '側面：写真では付属物なし',
         '本体加工不可（D01-010）、取付手段なし（D01-011）',
         '※ ドライバ・ポート・端子の位置は写真からの目安（寸法未確認）']
for i, t in enumerate(FACTS): txt(LX + 10, y + 20 + i * 18, t, col='#444' if t.startswith('※') else '#222')
y += 20 + len(FACTS) * 18 + 16
txt(LX, y, '■ 保持外形が満たす式（余裕寸法0、計算）', bold=True, size=13)
kh1, kh2 = s, c
EQ = [
    '① 収納時の高さ（チルト24°維持）：%.3f(t前+t後) + %.3f(t上+t下) ≦ %.2f' % (s, c, H_AVAIL - BH),
    '　　［掘込面h=270 − 下限h=245 − 外接高さ%.2f］' % BH,
    '　　参考：収納時だけ水平に戻す場合（A02-003で変更可）：t上+t下 ≦ %.1f' % (H_AVAIL - H),
    '② 収納時の奥行（収納帯d=45.5〜82.7）：%.3f(t前+t後) + %.3f(t上+t下) ≦ %.2f' % (c, s, D_AVAIL - BD),
    '　　［ワンモーション移動の条件（d1≧46.2、K013）は外形が変わると再計算が必要］',
    '③ 左右（設置エリア幅80.5）：t左 + t右 ≦ %.1f　［x位置は2-1で決定］' % (X_AVAIL - W),
    '※ 機構本体の収納空間はこの外形とは別に必要（A00-001は機構も含む。STEP4）']
for i, t in enumerate(EQ): txt(LX + 10, y + 20 + i * 18, t, col='#444' if t.startswith(('　', '※')) else '#222')

# ================= 平面図（右上） =================
PX = 720
PL = V(PX, 110, -8, 66, -10, 38, True)
txt(PX, 90, '平面図（−h方向に見下ろす。上がSC側、下がLP側）', size=14, bold=True)
# 上から見える面：背面（d=0〜H s）、上面（d=H s〜BD）
dP2 = H * s; dP3 = BD
poly(PL, [(0, 0), (W, 0), (W, dP2), (0, dP2)], fill='#eeeeee')
poly(PL, [(0, dP2), (W, dP2), (W, dP3), (0, dP3)], fill='#f7f7f7')
poly(PL, [(TERM[0], TERM[2] * s), (TERM[1], TERM[2] * s), (TERM[1], TERM[3] * s), (TERM[0], TERM[3] * s)], col=PUR, fill=PUR, op=0.35)
T_(PL, W / 2, dP2 / 2, '背面（端子）', dy=4, anchor='middle', col=PUR)
T_(PL, W / 2, (dP2 + dP3) / 2, '上面（資料なし）', dy=4, anchor='middle')
T_(PL, W, 0, 'SC側', dx=8, dy=4); T_(PL, W, dP3, 'LP側', dx=8, dy=4)
# 保持外形（外接の平面投影）
env_d0 = min(dh(-G, -G)[0], dh(-G, H + G)[0]); env_d1 = max(dh(D + G, -G)[0], dh(D + G, H + G)[0])
poly(PL, [(-G, env_d0), (W + G, env_d0), (W + G, env_d1), (-G, env_d1)], col=GRN, dash='6 3', w=1.6)
arrow(PL, 0, dP3 / 2, -G, dP3 / 2); T_(PL, -G, dP3 / 2, 't左', dx=-4, dy=-6, anchor='end', col=GRN)
arrow(PL, W, dP3 / 2 + 5, W + G, dP3 / 2 + 5); T_(PL, W + G, dP3 / 2 + 5, 't右', dx=4, dy=-6, col=GRN)
T_(PL, 0, dP3, 'W57.1', dy=34, col=K)
T_(PL, 0, dP3, '外接奥行 %.2f（チルト24°）' % BD, dy=52)
T_(PL, -8, -10, 'x→（LPから見て右）', dy=-4, col='#666')

# ================= 側面図（左下） =================
SY = 640
SV = V(60, SY + 30, -14, 40, -16, 26, False)
txt(40, SY + 10, '側面図（左壁側から+x方向を見る。左がSC側、右がLP側）', size=14, bold=True)
P = [dh(0, 0), dh(D, 0), dh(D, H), dh(0, H)]   # P0 P1 P3 P2
poly(SV, P, fill='#f2f2f2')
poly(SV, [P[1], P[2]], col=RED, w=4, close=False)
poly(SV, [dh(0, TERM[2]), dh(0, TERM[3])], col=PUR, w=5, close=False)
envP = [dh(-G, -G), dh(D + G, -G), dh(D + G, H + G), dh(-G, H + G)]
poly(SV, envP, col=GRN, dash='6 3', w=1.6)
# 変数の矢印
def mid(a, b): return ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
m_top = mid(dh(0, H), dh(D, H)); arrow(SV, *m_top, *dh(D / 2, H + G)); T_(SV, *dh(D / 2, H + G), 't上', dx=6, dy=-4, col=GRN)
m_bot = mid(dh(0, 0), dh(D, 0)); arrow(SV, *m_bot, *dh(D / 2, -G)); T_(SV, *dh(D / 2, -G), 't下', dx=-6, dy=14, anchor='end', col=GRN)
m_fr = dh(D, H / 2); arrow(SV, *m_fr, *dh(D + G, H / 2)); T_(SV, *dh(D + G, H / 2), 't前', dx=8, dy=4, col=GRN)
m_re = dh(0, H / 2); arrow(SV, *m_re, *dh(-G, H / 2)); T_(SV, *dh(-G, H / 2), 't後', dx=-8, dy=4, anchor='end', col=GRN)
T_(SV, *dh(0, 0), 'P0（SC側下角）', dx=-6, dy=18, anchor='end')
T_(SV, *dh(D, 0), 'P1（最下点）', dx=4, dy=18)
T_(SV, *dh(0, H), 'P2（最上点）', dx=-6, dy=-8, anchor='end')
T_(SV, *mid(P[1], P[2]), '前面（覆えない）', dx=14, dy=34, col=RED)
T_(SV, *dh(0, TERM[3]), '端子', dx=-14, dy=-6, anchor='end', col=PUR)
T_(SV, *m_top, '上面', dx=-36, dy=-4)
T_(SV, *dh(0, 0), '底面（ゴム足のみ）', dx=-6, dy=36, anchor='end')
# 外接寸法
d_lo, d_hi = 0, BD; h_lo, h_hi = -D * s, H * c
poly(SV, [(d_lo, h_lo - 6), (d_hi, h_lo - 6)], col=GRY, w=1, close=False)
T_(SV, (d_lo + d_hi) / 2, h_lo - 6, '外接奥行 %.2f' % BD, dy=16, anchor='middle', col=GRY)
poly(SV, [(d_hi + 6, h_lo), (d_hi + 6, h_hi)], col=GRY, w=1, close=False)
T_(SV, d_hi + 6, (h_lo + h_hi) / 2, '外接高さ %.2f' % BH, dx=6, col=GRY)
T_(SV, *dh(D, H), 'チルト24°（LP側を下げる）', dx=30, dy=-30, col=BLU)
T_(SV, -14, -16, 'd→', dy=-4, col='#666'); T_(SV, -14, 26, '↑h', dy=14, col='#666')

# ================= 正面図（右下） =================
FV = V(PX, SY + 30, -8, 66, -14, 32, False)
txt(PX, SY + 10, '正面図（LP側から−d方向を見る）', size=14, bold=True)
hb0, hb1, ht1 = -D * s, -D * s + H * c, H * c    # 前面：P1〜P3、上面：P3〜P2
poly(FV, [(0, hb0), (W, hb0), (W, hb1), (0, hb1)], col=RED, w=1.6, fill='#fdf0ee')
poly(FV, [(0, hb1), (W, hb1), (W, ht1), (0, ht1)], fill='#f7f7f7')
def bh(w): return hb0 + w * c
for (x0, wc, r) in WOOF: ell(FV, x0, bh(wc), r, r * c, RED)
ell(FV, TWT[0], bh(TWT[1]), TWT[2], TWT[2] * c, RED)
for (x0, x1) in PORTS:
    poly(FV, [(x0, bh(PORT_W[0])), (x1, bh(PORT_W[0])), (x1, bh(PORT_W[1])), (x0, bh(PORT_W[1]))], col=RED, fill=RED, op=0.5)
T_(FV, W / 2, bh(H), '前面（バッフル）＝覆えない', dy=-4, anchor='middle', col=RED)
T_(FV, W / 2, ht1, '上面（見かけ高さ %.1f）' % (D * s), dy=-4, anchor='middle')
T_(FV, PORTS[0][0], bh(PORT_W[0]), 'ポート', dy=16, anchor='middle', col=RED)
T_(FV, PORTS[1][1], bh(PORT_W[0]), 'ポート', dy=16, anchor='middle', col=RED)
ev_lo = min(p[1] for p in envP); ev_hi = max(p[1] for p in envP)
poly(FV, [(-G, ev_lo), (W + G, ev_lo), (W + G, ev_hi), (-G, ev_hi)], col=GRN, dash='6 3', w=1.6)
arrow(FV, 0, (hb0 + ht1) / 2, -G, (hb0 + ht1) / 2); T_(FV, -G, (hb0 + ht1) / 2, 't左', dx=-4, dy=-6, anchor='end', col=GRN)
arrow(FV, W, (hb0 + ht1) / 2, W + G, (hb0 + ht1) / 2); T_(FV, W + G, (hb0 + ht1) / 2, 't右', dx=4, dy=-6, col=GRN)
T_(FV, 0, ev_lo, '前面は24°下向きのため、縦は%.1f倍に縮んで見える' % c, dy=22, col='#444')
T_(FV, 0, ev_lo, 'ドライバ・ポートの位置は写真からの目安', dy=40, col='#444')

Wc, Hc = 1520, 1180
svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" font-family="Noto Sans CJK JP, Hiragino Sans, Meiryo, sans-serif">' % (Wc, Hc, Wc, Hc),
       '<defs><marker id="ag" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="%s"/></marker></defs>' % GRN,
       '<rect width="100%" height="100%" fill="white"/>'] + out + ['</svg>']
open(sys.argv[1], 'w', encoding='utf-8').write('\n'.join(svg))
print('外接 奥行%.2f 高さ%.2f / ①余裕%.2f ②余裕%.2f ③余裕%.1f' % (BD, BH, H_AVAIL - BH, D_AVAIL - BD, X_AVAIL - W))
