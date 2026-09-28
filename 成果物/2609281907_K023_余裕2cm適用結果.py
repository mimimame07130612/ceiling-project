# K023 余裕寸法 一律2cm（c1〜c4）を適用した配置とストローク（STEP2 2-4）
# 右限・振りなし・チルト24°維持（K018のB）のCSP単体（保持具の厚さ0）に、余裕 m=2（依頼主指定・仮）を適用する。
# c1：最上点と掘込面の間 2 → h=245 を Δ 下げる。c2：天井端・掘込み前壁、SCケースを2だけ太らせてワンモーション判定（K013の方法）。
# c3：梁2内面との間 2。c4：光束上端面との間 2。c5：配光境界との間 2（参考）。
# 入力：A01-001、A02-002〜006、A00-001、A00-006、A01-003・A00-004、D01-001、D01-009、K011、K013、K018、K020〜K022
# 使い方：python3 本ファイル <出力svgパス> <出力csvパス>
import math, sys, html, csv
CD, CH, T = 21.4, 17.0, math.radians(24); c, s = math.cos(T), math.sin(T)
W = 57.1; M = 2.0; TS = '2609281907'
Q = [(0, 0), (CD*c, -CD*s), (CD*c+CH*s, -CD*s+CH*c), (CH*s, CH*c)]
hu = lambda d: 161 + (d - 25) * 56 / 280
DELTA = (CD*s + CH*c) - (25 - M)
LOW_S = 245 - DELTA
def poly_(d1, h0): return [(d1+a, h0+b) for a, b in Q]
def edges(P):
    pts = []
    for i in range(4):
        a, b = P[i], P[(i+1) % 4]
        for k in range(41): pts.append((a[0]+(b[0]-a[0])*k/40, a[1]+(b[1]-a[1])*k/40))
    return pts
def hit(p):
    d, h = p
    if d < 45.5 + M - 1e-9 and h > 250 - M + 1e-9: return '天井'
    if 20.5 - M < d < 33.9 + M and 236.5 - M < h < 250: return 'SCケース'
    return None
def inside(pt, P):
    sg = [(P[(i+1) % 4][0]-P[i][0])*(pt[1]-P[i][1]) - (P[(i+1) % 4][1]-P[i][1])*(pt[0]-P[i][0]) for i in range(4)]
    return all(x >= -1e-9 for x in sg) or all(x <= 1e-9 for x in sg)
CORNERS = [((45.5 + M, 250 - M), '天井端'), ((33.9 + M, 236.5 - M), 'SCケース角')]
def h0u(du): return hu(du + CD*c) + M + CD*s
def check(ds, du):
    h0s = LOW_S + CD*s
    for k in range(801):
        t = k / 800; P = poly_(ds + (du-ds)*t, h0s + (h0u(du)-h0s)*t)
        for p in edges(P):
            if hit(p): return True
        for pt, nm in CORNERS:
            if inside(pt, P) and not (nm == '天井端' and t == 0): return True
    return False
TAN59 = math.tan(math.radians(59))
light_d = lambda h: 130 - 5.7 - (270 - h) * TAN59
DS_MAX = light_d(LOW_S) - M - CD*c
rows = []
for du in (33, 35, 40):
    ds = 45.5 + M
    while ds <= DS_MAX and check(ds, du): ds = round(ds + 0.1, 1)
    low_u = hu(du + CD*c) + M
    baf = (du + (Q[1][0] + Q[2][0]) / 2, low_u + CD*s + (Q[1][1] + Q[2][1]) / 2)
    el = math.degrees(math.atan((baf[1] - 100) / (270 - baf[0])))
    rows.append([du, ds, round(low_u, 2), round(low_u + CD*s + CH*c, 2), round(LOW_S - low_u, 2), round(ds - du, 1), round(el, 1)])
XC = 170 - M - W / 2
# ---------- CSV ----------
with open(sys.argv[2], 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.writer(f)
    w.writerow(['K023 余裕寸法 一律2cm（c1〜c4、依頼主指定・仮）の適用結果（STEP2 2-4）　CSP単体・右限・振りなし・チルト24°維持　単位cm・度'])
    w.writerow(['収納：h=245を%.2f下げる（Δ）→ 最下点 h=%.2f、最上点 h=%.2f（掘込面まで2）' % (DELTA, LOW_S, LOW_S + CD*s + CH*c)])
    w.writerow(['収納d1の範囲：%.1f（下表のワンモーション条件）〜 %.1f（配光境界との間2）' % (rows[0][1], DS_MAX)])
    w.writerow(['左右：中心x=%.2f、LP中央とのずれ %.2f（梁2内面との間2）' % (XC, 169 - XC)])
    w.writerow(['使用d1', 'ワンモーションが成立する最小の収納d1', '使用時 最下点h（光束上端面+2）', '使用時 最上点h', '鉛直ストローク', '前後移動量', 'LP目への仰角（バッフル中心）'])
    w.writerows(rows)
    w.writerow([])
    w.writerow(['保持具を付けた場合：底面支持板 r=0.7 は t下≦2.86 までΔが増えない（K016の「P1を下げない上限」）。支持板の後端がP0より0.407·t下だけ後ろに出るため、収納d1の下限が上がる'])
    w.writerow(['参考：収納時だけ水平に戻す案（K018のA）なら Δ=0 のまま t下+a′≦6（=25−2−17）'])
# ---------- SVG ----------
e = html.escape; out = []
K, RED, GRN, GRY, BLU, ORG, PUR, AMB, MAG = '#333333', '#C0392B', '#2E9E6B', '#8a857a', '#2C6FB0', '#D35400', '#6A5FD0', '#C8860A', '#C8307A'
def f(n): return ('%.1f' % n).rstrip('0').rstrip('.')
class V:
    def __init__(s_, ox, oy, u0, v1, sc): s_.ox, s_.oy, s_.u0, s_.v1, s_.sc = ox, oy, u0, v1, sc
    def X(s_, u): return s_.ox + (u - s_.u0) * s_.sc
    def Y(s_, v): return s_.oy + (s_.v1 - v) * s_.sc
def pl(v, pts, col=K, w=1.4, fill='none', op=1, dash=None, close=True):
    tag = 'polygon' if close else 'polyline'
    out.append('<%s points="%s" fill="%s" fill-opacity="%s" stroke="%s" stroke-width="%s"%s/>' % (
        tag, ' '.join('%s,%s' % (f(v.X(a)), f(v.Y(b))) for a, b in pts), fill, op, col, w,
        ' stroke-dasharray="%s"' % dash if dash else ''))
def txt(x, y, t, col='#222', anchor='start', size=13, bold=False):
    out.append('<text x="%s" y="%s" fill="%s" text-anchor="%s" font-size="%s"%s>%s</text>' % (
        f(x), f(y), col, anchor, size, ' font-weight="bold"' if bold else '', e(t)))
def T_(v, a, b, t, dx=0, dy=0, **k): txt(v.X(a) + dx, v.Y(b) + dy, t, **k)
txt(40, 40, 'K023　余裕寸法 一律2cm の適用結果（STEP2 2-4）', size=18, bold=True)
txt(40, 62, '作成 %s　部屋座標・単位cm。余裕 m=2（c1〜c4、依頼主指定・仮）。CSP単体・右限・振りなし・チルト24°維持。桃の帯＝余裕2' % TS, size=12)
SV = V(60, 110, 15, 276, 5.4)
txt(60, 100, '側面図（左がSC側、右がLP側）　使用d1=33 の組合せ', size=14, bold=True)
pl(SV, [(15, 270), (45.5, 270), (45.5, 250), (15, 250)], w=0, fill=GRY, op=0.2)
pl(SV, [(15, 250), (45.5, 250), (45.5, 270), (125, 270)], w=2, close=False)
pl(SV, [(15, 250 - M), (45.5 + M, 250 - M), (45.5 + M, 270 - M), (125, 270 - M)], col=MAG, w=1, dash='3 2', close=False)
pl(SV, [(20.5, 250), (33.9, 250), (33.9, 236.5), (20.5, 236.5)], col=GRY, fill=GRY, op=0.2)
pl(SV, [(20.5 - M, 250 - M), (33.9 + M, 250 - M), (33.9 + M, 236.5 - M), (20.5 - M, 236.5 - M)], col=MAG, w=1, dash='3 2')
T_(SV, 20.5, 236.5, 'SCケース', dy=20, col=GRY, size=11)
pl(SV, [(25, 161), (25, 236.5)], w=2.5, close=False)
pl(SV, [(25, hu(25)), (115, hu(115))], col=ORG, dash='6 3', close=False)
pl(SV, [(25, hu(25) + M), (115, hu(115) + M)], col=MAG, w=1, dash='3 2', close=False)
T_(SV, 104, hu(104), '光束上端面', dy=16, col=ORG, size=11)
pl(SV, [(light_d(243), 243), (light_d(270), 270)], col=AMB, dash='5 3', close=False)
pl(SV, [(light_d(243) - M, 243), (light_d(270) - M, 270)], col=MAG, w=1, dash='3 2', close=False)
T_(SV, light_d(262), 262, '配光境界', dx=8, col=AMB, size=11)
for hv, lab in [(245, 'h=245'), (LOW_S, 'h=%.2f（収納最下点）' % LOW_S)]:
    pl(SV, [(15, hv), (118, hv)], col=BLU, w=1, dash='6 3', close=False); T_(SV, 118, hv, lab, dx=4, dy=4 if hv < 245 else -2, col=BLU, size=11)
ds, du = rows[0][1], 33
PS = poly_(ds, LOW_S + CD*s); PU = poly_(du, h0u(du))
pl(SV, PS, col=BLU, fill=BLU, op=0.18); pl(SV, PU, col=RED, fill=RED, op=0.18)
for k in (0.25, 0.5, 0.75):
    pl(SV, poly_(ds + (du - ds) * k, LOW_S + CD*s + (h0u(du) - LOW_S - CD*s) * k), col=GRY, w=0.8, dash='2 3')
T_(SV, *PS[2], '収納 d1=%.1f' % ds, dx=6, col=BLU); T_(SV, *PU[2], '使用 d1=33', dx=6, col=RED)
T_(SV, 60, 205, '灰点線：一直線移動の途中', col=GRY, size=11)
FV = V(720, 110, 70, 276, 4.4)
txt(720, 100, '正面図（LP側から見る）', size=14, bold=True)
for a0, a1, lab in [(79, 89.5, '梁1'), (170, 180.5, '梁2')]:
    pl(FV, [(a0, 254.5), (a1, 254.5), (a1, 270), (a0, 270)], col=GRY, fill=GRY, op=0.6)
    T_(FV, (a0 + a1) / 2, 270, lab, dy=-4, anchor='middle', size=11)
pl(FV, [(168, 254.5), (168, 270)], col=MAG, w=1, dash='3 2', close=False)
pl(FV, [(70, 270), (200, 270)], w=2, close=False)
xl, xr = XC - W / 2, XC + W / 2
pl(FV, [(xl, LOW_S), (xr, LOW_S), (xr, LOW_S + 24.23), (xl, LOW_S + 24.23)], col=BLU, fill=BLU, op=0.18)
lu = rows[0][2]
pl(FV, [(xl, lu), (xr, lu), (xr, lu + 24.23), (xl, lu + 24.23)], col=RED, fill=RED, op=0.18)
pl(FV, [(169, 160), (169, 200)], col=PUR, w=1, dash='4 3', close=False); T_(FV, 169, 160, 'LP中央 x=169', dy=14, anchor='middle', col=PUR, size=11)
T_(FV, XC, LOW_S + 12, '中心x=%.2f' % XC, anchor='middle', col=BLU)
T_(FV, 168, 262, '梁2内面−2', dx=-4, anchor='end', col=MAG, size=11)
TX, TY = 60, 775
txt(TX, TY, '■ 結果（計算、CSP単体）', bold=True, size=14)
L = ['収納：h=245 を Δ=%.2f 下げる → 最下点 h=%.2f、最上点 h=%.2f。収納d1＝%.1f〜%.1f' % (DELTA, LOW_S, LOW_S + CD*s + CH*c, rows[0][1], DS_MAX),
     '左右：中心x=%.2f、LP中央とのずれ %.2f（余裕0のとき27.55）' % (XC, 169 - XC),
     '使用d1=33：最下点 h=%.2f、鉛直ストローク %.2f、前後移動 %.1f、LP目への仰角 %.1f°（余裕0のとき19.1°）' % (rows[0][2], rows[0][4], rows[0][5], rows[0][6]),
     '使用d1=35：収納d1≧%.1f、ストローク %.2f ／ 使用d1=40：収納d1≧%.1f、ストローク %.2f' % (rows[1][1], rows[1][4], rows[2][1], rows[2][4]),
     '保持具：支持板 r=0.7 は t下≦2.86 までΔが増えない。支持板の後端が 0.407·t下 だけ後ろに出る分、収納d1の下限が上がる',
     '参考：収納時だけ水平に戻す案（K018のA）なら、Δ=0 のまま t下+a′≦6']
for i, t_ in enumerate(L): txt(TX + 10, TY + 26 + i * 20, t_)
Hc = TY + 26 + len(L) * 20 + 20
svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="%d" viewBox="0 0 1400 %d" font-family="Noto Sans CJK JP, Hiragino Sans, Meiryo, sans-serif">' % (Hc, Hc),
       '<rect width="100%" height="100%" fill="white"/>'] + out + ['</svg>']
open(sys.argv[1], 'w', encoding='utf-8').write('\n'.join(svg))
for r in rows: print(r)
