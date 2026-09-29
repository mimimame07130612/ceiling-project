#!/usr/bin/env python3
# sanmen.py — 三面図ベースコマンド（セッション01 作成）
# 改訂 2609291226（セッション05）：ファイル名にプレフィクスを付加（F7 e）、使い方の記載を更新。描画の内容は変更なし。
# K001「部屋三面図」をベース図として描き、その上に機器・軌跡などの重ね描き(JSON)を追記した三面図SVGを出力する。
#
# 使い方:
#   python3 YYMMDDhhmm_sanmen.py --zuban K002 --title 図題 -o '/mnt/user-data/outputs/{ts}_K002_本体名.svg' [重ね描き.json ...]
#   ・GH/ツールにあるプレフィクスの最も大きいものを使う（F3、F7 e）。他のツールとは import で連携せず、コマンドとして呼ぶ。
#   ・CSPを重ねるときは、重ね描きJSONを YYMMDDhhmm_csp.py で生成して渡す（F7 c）。
#   ・{ts} は本コマンド内で TZ=Asia/Tokyo date +%y%m%d%H%M により1回だけ取得した値に置き換わる（F3）。図中の作成日時も同じ値。
#   ・重ね描きを渡さなければ K001 と同じ図になる（--zuban K001 --title 部屋三面図）。
#
# 配置（依頼主指定）:  凡例 | 平面図 / 側面図 | 正面図
#   平面図 x-d（−h方向に見下ろす、SC側が上）、側面図 d-h（+x方向を見る、左壁側から）、正面図 x-h（−d方向を見る、LP側からSC側）
#   カーテンは平面図のみ表示。視聴位置は LLP（左）・RLP（右）と表記。
#
# 重ね描きJSONの形式:
#   {"title_note": ["ヘッダに追加する注記行", ...],
#    "legend": [{"text": "…", "color": "#…", "dash": false, "kind": "line|dot|ring|band"}],
#    "src": ["出典", ...],
#    "items": [
#      3D部品（三面すべてに自動投影）:
#        {"t":"box3",  "p":[x0,x1,d0,d1,h0,h1], "color","fill","op","w","dash", "label":"文字"}
#        {"t":"line3", "p":[[x,d,h],...], "color","w","dash", "label"}
#        {"t":"pt3",   "p":[x,d,h], "color","r"(px),"ring":bool, "label"}
#      2D部品（1面だけに描く。"view":"plan"|"side"|"front"、座標は各面の(横,縦)cm）:
#        {"t":"line"|"poly", "view", "p":[[u,v],...], ...}  {"t":"rect","view","p":[u0,v0,u1,v1],...}
#        {"t":"circle","view","p":[u,v],"r"(cm)}  {"t":"text","view","p":[u,v],"s":"文字","dx","dy","anchor","color"}
#    ]}
#   "dash": true は仮設定・仮設定を含む計算値（破線）。文字側は ( ) を付けて渡す。
import html, json, argparse, subprocess
ap = argparse.ArgumentParser()
ap.add_argument('-o', required=True); ap.add_argument('--zuban', required=True); ap.add_argument('--title', required=True)
ap.add_argument('parts', nargs='*')
A = ap.parse_args()
TS = subprocess.run(['date', '+%y%m%d%H%M'], capture_output=True, text=True, env={'TZ': 'Asia/Tokyo'}).stdout.strip()
OUT = A.o.replace('{ts}', TS)
PARTS = [json.load(open(p, encoding='utf-8')) for p in A.parts]
e = html.escape

# ---- 部屋.xlsx Sheet1 ----
X_AREA_L, X_AREA_R, X_B1_OFS, B_PITCH, B_W, X_FWALL_R = 45.5, 305.5, 33.5, 91, 10.5, 273
D_AREA_F, D_AREA_B, D_RWALL = 45.5, 302.5, 348
H_CEIL, H_AREA, B_H = 250, 270, 15.5
LED_DIA, LED_X, LED_D = 11.4, [129.65, 220.65], [45.5 + o for o in (84.5, 129.5, 174.5)]
LP_X, LP_D, LP_H = [132.5, 205.5], 270, 100
C1 = dict(x=(10, 254), d=14, h=(2, 227)); C2 = dict(x=14, d=(17, 174), h=(2, 227))
# ---- A00-003 / A00-004（仮設定） ----
SC_X, SC_D, SC_HC = 146, 25, 98.75
PJ_X, PJ_D, PJ_H = 146, 305, 217
# ---- SC製品寸法図 EP-100HM-MRW1-WF204（mm→cm） ----
IMG_W, IMG_H, UP_MASK, CASE_H, CASE_L, CASE_D, FAB_OFS = 221.4, 124.5, 75.5, 13.5, 256.1, 13.4, 4.5
# ---- 派生 ----
B_L = [X_AREA_L + X_B1_OFS + i * B_PITCH for i in range(3)]
H_BLOW = H_AREA - B_H
IMG_X0, IMG_X1 = SC_X - IMG_W / 2, SC_X + IMG_W / 2
IMG_H0, IMG_H1 = SC_HC - IMG_H / 2, SC_HC + IMG_H / 2
CASE_BOT = IMG_H1 + UP_MASK; CASE_TOP = CASE_BOT + CASE_H
CASE_X0, CASE_X1 = SC_X - CASE_L / 2, SC_X + CASE_L / 2
CASE_DB = SC_D - FAB_OFS; CASE_DF = CASE_DB + CASE_D
LP_XC = sum(LP_X) / 2

S = 1.6          # px/cm
FS = 11
K, GRAY, AMB, CUR, LPC, PJC, SCC, AREA = '#333333', '#8a857a', '#BA7517', '#5B8DB8', '#6A5FD0', '#D85A30', '#111111', '#2E9E6B'
DASH = '6 3'
out = []

class View:
    def __init__(s, ox, oy, umin, umax, vmin, vmax, vdown):
        s.ox, s.oy, s.umin, s.umax, s.vmin, s.vmax, s.vdown = ox, oy, umin, umax, vmin, vmax, vdown
        s.w = (umax - umin) * S; s.h = (vmax - vmin) * S
    def X(s, u): return s.ox + (u - s.umin) * S
    def Y(s, v): return s.oy + ((v - s.vmin) * S if s.vdown else (s.vmax - v) * S)

def f(n): return ('%.1f' % n).rstrip('0').rstrip('.')
def st(c, w=1.2, dash=False): return 'stroke="%s" stroke-width="%s"%s' % (c, w, ' stroke-dasharray="%s"' % DASH if dash else '')
def line(V, pts, c=K, w=1.2, dash=False):
    out.append('<polyline points="%s" fill="none" %s/>' % (' '.join('%s,%s' % (f(V.X(u)), f(V.Y(v))) for u, v in pts), st(c, w, dash)))
def rect(V, u0, v0, u1, v1, c=K, w=1.0, fill='none', op=0.3, dash=False):
    x0, x1 = sorted([V.X(u0), V.X(u1)]); y0, y1 = sorted([V.Y(v0), V.Y(v1)])
    out.append('<rect x="%s" y="%s" width="%s" height="%s" fill="%s" fill-opacity="%s" %s/>' % (f(x0), f(y0), f(x1 - x0), f(y1 - y0), fill, op, st(c, w, dash)))
def circ(V, u, v, rcm=None, rpx=None, c=K, fill=None, op=1, w=1.0, dash=False):
    r = rcm * S if rcm else rpx
    out.append('<circle cx="%s" cy="%s" r="%s" fill="%s" fill-opacity="%s" %s/>' % (f(V.X(u)), f(V.Y(v)), f(r), fill or 'none', op, st(c, w, dash)))
def text(x, y, s, c='#222', anchor='start', size=FS, bold=False, rot=None):
    tr = ' transform="rotate(%s %s %s)"' % (rot, f(x), f(y)) if rot else ''
    out.append('<text x="%s" y="%s" fill="%s" text-anchor="%s" font-size="%s"%s%s>%s</text>' % (
        f(x), f(y), c, anchor, size, ' font-weight="bold"' if bold else '', tr, e(s)))
def T(V, u, v, s, dx=0, dy=0, **k): text(V.X(u) + dx, V.Y(v) + dy, s, **k)
def axes(V, un, vn, note):
    x0, y0 = V.X(0), V.Y(0)
    out.append('<circle cx="%s" cy="%s" r="3.5" fill="none" stroke="#000"/>' % (f(x0), f(y0)))
    ar = 'marker-end="url(#ar)"'
    out.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="#000" stroke-width="1" %s/>' % (f(x0), f(y0), f(x0 + 40), f(y0), ar))
    y2 = y0 + 40 if V.vdown else y0 - 40
    out.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="#000" stroke-width="1" %s/>' % (f(x0), f(y0), f(x0), f(y2), ar))
    text(x0 + 44, y0 + 4, '+' + un, '#000')
    text(x0 + 4, y2 + (12 if V.vdown else -4), '+' + vn, '#000')
    text(x0 - 6, y0 + (-6 if V.vdown else 16), 'O', '#000', anchor='end')

# ================= 上面図 (x右, d下) =================
SD_W = (360 + 12) * S
NOTES = [n for P in PARTS for n in P.get('title_note', [])]
PL = View(70 + SD_W + 90, 150 + 20 * len(NOTES), -12, 335, -12, 360, True)
text(PL.ox, PL.oy - 18, '平面図（−h方向に見下ろす。上がSC側、下がLP側）', bold=True, size=13)
V = PL
line(V, [[0, D_RWALL], [0, 0], [X_FWALL_R, 0]], w=2.2)                       # 左壁・前壁
line(V, [[X_FWALL_R, 0], [X_FWALL_R, -10]], w=2.2)
line(V, [[0, D_RWALL], [320, D_RWALL]], w=2.2)                                # 後壁
T(V, 320, D_RWALL, '後壁の右端位置は未確認', dx=0, dy=16, anchor='end', c='#666')
T(V, 312, 70, 'x>273：', c='#666')
T(V, 312, 70, '壁なし', dy=14, c='#666')
T(V, 312, 70, 'オープン', dy=28, c='#666')
T(V, 312, 70, 'スペース', dy=42, c='#666')
rect(V, B_L[0] + B_W, D_AREA_F, B_L[1], D_AREA_B, c=AREA, w=0, fill=AREA, op=0.13)  # 設置エリア
rect(V, X_AREA_L, D_AREA_F, X_AREA_R, D_AREA_B, w=1.2)                        # 梁領域
for b in B_L: rect(V, b, D_AREA_F, b + B_W, D_AREA_B, c=GRAY, fill=GRAY, op=0.55, w=0.8)
for x in LED_X:
    for d in LED_D: circ(V, x, d, rcm=LED_DIA / 2, c=AMB, fill=AMB, op=0.55)
line(V, [[C1['x'][0], C1['d']], [C1['x'][1], C1['d']]], c=CUR, w=1.6)
line(V, [[C2['x'], C2['d'][0]], [C2['x'], C2['d'][1]]], c=CUR, w=1.6)
rect(V, CASE_X0, CASE_DB, CASE_X1, CASE_DF, c=SCC, fill='#dddddd', op=0.6, dash=True)
line(V, [[IMG_X0, SC_D], [IMG_X1, SC_D]], c=SCC, w=3, dash=True)
for x in LP_X: circ(V, x, LP_D, rpx=4, c=LPC, fill=LPC)
line(V, [[LP_XC, LP_D - 7], [LP_XC, LP_D + 7]], c=LPC, w=1.4)
circ(V, PJ_X, PJ_D, rpx=4.5, c=PJC, fill='white', w=2, dash=False)
for i, b in enumerate(B_L): T(V, b + B_W / 2, D_AREA_F, '梁%d' % (i + 1), dy=-5, anchor='middle', bold=True)
T(V, (B_L[0] + B_W + B_L[1]) / 2, 108, '設置エリア', anchor='middle', c=AREA, bold=True)
T(V, (B_L[0] + B_W + B_L[1]) / 2, 108, 'x=89.5〜170', dy=14, anchor='middle', c=AREA)
T(V, X_AREA_R, D_AREA_B, '梁領域 x=45.5〜305.5 / d=45.5〜302.5', dy=16, anchor='end')
T(V, CASE_X1, (CASE_DB+CASE_DF)/2, '(SCケース・映像面)', dx=4, dy=4)
T(V, LP_X[0], LP_D, 'LLP x=132.5', dx=-7, dy=4, anchor='end', c=LPC)
T(V, LP_X[1], LP_D, 'RLP x=205.5', dx=7, dy=4, c=LPC)
T(V, LP_XC, LP_D, '中央169', dy=22, anchor='middle', c=LPC)
T(V, PJ_X, PJ_D, '(PJレンズ d=305)', dx=-8, dy=4, anchor='end', c=PJC)
T(V, C2['x'], 110, 'カーテン2', dx=5, c=CUR, rot=90)
T(V, 200, C1['d'], 'カーテン1', dy=12, c=CUR)
T(V, 0, D_RWALL, 'd=348', dx=4, dy=-5)
axes(V, 'x', 'd', '')

# ================= 正面図 (x右, h上) =================
FR = View(PL.ox, PL.oy + PL.h + 70, -12, 335, -10, 285, False)
text(FR.ox, FR.oy - 18, '正面図（−d方向を見る。LP側からSC側）', bold=True, size=13)
V = FR
line(V, [[-12, 0], [335, 0]], w=2.2)
line(V, [[0, 0], [0, H_CEIL], [X_AREA_L, H_CEIL], [X_AREA_L, H_AREA], [X_AREA_R, H_AREA], [X_AREA_R, H_CEIL], [335, H_CEIL]], w=2.2)
line(V, [[X_FWALL_R, 0], [X_FWALL_R, H_CEIL]], c='#999', w=1)
T(V, X_FWALL_R, 120, '前壁右端 x=273', dx=4, c='#666')
rect(V, B_L[0] + B_W, H_BLOW - 12, B_L[1], H_AREA, c=AREA, w=0, fill=AREA, op=0.13)
for b in B_L: rect(V, b, H_BLOW, b + B_W, H_AREA, c=GRAY, fill=GRAY, op=0.55, w=0.8)
for x in LED_X: rect(V, x - LED_DIA / 2, H_AREA - 1.5, x + LED_DIA / 2, H_AREA, c=AMB, fill=AMB, op=1)
rect(V, CASE_X0, CASE_BOT, CASE_X1, CASE_TOP, c=SCC, fill='#dddddd', op=0.6, dash=True)
rect(V, IMG_X0, IMG_H0, IMG_X1, IMG_H1, c=SCC, w=1.8, fill='#ffffff', op=0.7, dash=True)
circ(V, SC_X, SC_HC, rpx=2.5, c=SCC, fill=SCC)
for x in LP_X: circ(V, x, LP_H, rpx=4, c=LPC, fill=LPC)
line(V, [[LP_XC, LP_H - 7], [LP_XC, LP_H + 7]], c=LPC, w=1.4)
circ(V, PJ_X, PJ_H, rpx=4.5, c=PJC, fill='white', w=2)
for i, b in enumerate(B_L): T(V, b + B_W / 2, H_AREA, '梁%d' % (i + 1), dy=-5, anchor='middle', bold=True)
T(V, 0, H_CEIL, '天井 h=250', dx=4, dy=-5)
T(V, X_AREA_R, H_AREA, '掘込面 h=270', dx=4, dy=4)
T(V, X_AREA_R, H_BLOW, '梁下面 h=254.5', dx=4, dy=12)
T(V, CASE_X0, CASE_BOT, '(SCケース h=236.5〜250)', dx=4, dy=13)
T(V, SC_X, IMG_H1, '(SC映像面 h=36.5〜161)', dy=16, anchor='middle')
T(V, SC_X, SC_HC, '(中心 x=146 h=98.75)', dy=-22, anchor='middle')
T(V, LP_X[0], LP_H, 'LLP', dx=-7, dy=4, anchor='end', c=LPC)
T(V, LP_X[1], LP_H, 'RLP', dx=7, dy=4, c=LPC)
T(V, LP_XC, LP_H, '目 h=100', dy=22, anchor='middle', c=LPC)
T(V, PJ_X, PJ_H, '(PJレンズ h=217)', dx=9, dy=4, c=PJC)
T(V, 330, 180, '右側 開放', anchor='end', c='#666')
axes(V, 'x', 'h', '')

# ================= 側面図 (d右, h上) =================
SD = View(70, FR.oy, -12, 360, -10, 285, False)
text(SD.ox, SD.oy - 18, '側面図（+x方向を見る。左壁側から）', bold=True, size=13)
V = SD
line(V, [[-12, 0], [360, 0]], w=2.2)
line(V, [[0, 0], [0, H_CEIL], [D_AREA_F, H_CEIL], [D_AREA_F, H_AREA], [D_AREA_B, H_AREA], [D_AREA_B, H_CEIL], [D_RWALL, H_CEIL], [D_RWALL, 0]], w=2.2)
rect(V, D_AREA_F, H_BLOW, D_AREA_B, H_AREA, c=GRAY, fill=GRAY, op=0.4, w=0.8)
for d in LED_D: rect(V, d - LED_DIA / 2, H_AREA - 1.5, d + LED_DIA / 2, H_AREA, c=AMB, fill=AMB, op=1)
rect(V, CASE_DB, CASE_BOT, CASE_DF, CASE_TOP, c=SCC, fill='#dddddd', op=0.6, dash=True)
line(V, [[SC_D, CASE_BOT], [SC_D, IMG_H1]], c=SCC, w=0.8, dash=True)
line(V, [[SC_D, IMG_H0], [SC_D, IMG_H1]], c=SCC, w=3, dash=True)
circ(V, LP_D, LP_H, rpx=4, c=LPC, fill=LPC)
circ(V, PJ_D, PJ_H, rpx=4.5, c=PJC, fill='white', w=2)
T(V, 174, H_BLOW, '梁（梁1〜3が重なる） h=254.5〜270', dy=14, anchor='middle')
T(V, D_AREA_F, H_AREA, 'd=45.5', dy=-5, anchor='middle')
T(V, D_AREA_B, H_AREA, 'd=302.5', dy=-5, anchor='middle')
T(V, SC_D, 130, '(SC映像面 d=25)', dx=6)
T(V, SC_D, 115, '(ケース d=20.5〜33.9)', dx=6)
T(V, LP_D, LP_H, 'LLP・RLP 目 d=270 h=100', dx=-8, dy=-8, anchor='end', c=LPC)
T(V, PJ_D, PJ_H, '(PJレンズ d=305 h=217)', dx=-8, dy=-8, anchor='end', c=PJC)
T(V, D_RWALL, H_CEIL, 'd=348', dx=-4, dy=-5, anchor='end')
axes(V, 'd', 'h', '')

# ================= 重ね描き =================
VIEWS = {'plan': (PL, 0, 1), 'front': (FR, 0, 2), 'side': (SD, 1, 2)}   # 3D(x,d,h)→各面(横,縦)の成分番号
def draw2(V, it, pts):
    c = it.get('color', K); dash = it.get('dash', False); w = it.get('w', 1.4)
    t = it['t']
    if t in ('line', 'line3'): line(V, pts, c=c, w=w, dash=dash)
    elif t == 'poly':
        out.append('<polygon points="%s" fill="%s" fill-opacity="%s" %s/>' % (' '.join('%s,%s' % (f(V.X(u)), f(V.Y(v))) for u, v in pts), it.get('fill', 'none'), it.get('op', 0.25), st(c, w, dash)))
    elif t in ('rect', 'box3'): rect(V, pts[0][0], pts[0][1], pts[1][0], pts[1][1], c=c, w=w, fill=it.get('fill', 'none'), op=it.get('op', 0.3), dash=dash)
    elif t == 'circle': circ(V, pts[0][0], pts[0][1], rcm=it['r'], c=c, fill=it.get('fill'), op=it.get('op', 0.3), w=w, dash=dash)
    elif t == 'pt' or t == 'pt3':
        if it.get('ring'): circ(V, pts[0][0], pts[0][1], rpx=it.get('r', 4.5), c=c, fill='white', w=2)
        else: circ(V, pts[0][0], pts[0][1], rpx=it.get('r', 4), c=c, fill=c)
    elif t == 'text': T(V, pts[0][0], pts[0][1], it['s'], dx=it.get('dx', 0), dy=it.get('dy', 0), anchor=it.get('anchor', 'start'), c=it.get('color', '#222'))
    if it.get('label') and t != 'text':
        u = max(p[0] for p in pts) if t in ('rect', 'box3') else pts[0][0]
        v = max(p[1] for p in pts) if t in ('rect', 'box3') else pts[0][1]
        T(V, u, v, it['label'], dx=4, dy=-4, c=c)
for P in PARTS:
    for it in P.get('items', []):
        t = it['t']
        if t.endswith('3'):
            for V, a, b in VIEWS.values():
                if t == 'box3':
                    q = it['p']; lo = [q[0], q[2], q[4]]; hi = [q[1], q[3], q[5]]
                    pts = [[lo[a], lo[b]], [hi[a], hi[b]]]
                elif t == 'pt3': pts = [[it['p'][a], it['p'][b]]]
                else: pts = [[p[a], p[b]] for p in it['p']]
                draw2(V, it, pts)
        else:
            V = VIEWS[it['view']][0]; p = it['p']
            pts = [p[:2], p[2:]] if t == 'rect' else ([p] if t in ('circle', 'pt', 'text') else p)
            draw2(V, it, pts)

# ================= ヘッダ・凡例 =================
now = '20%s年%d月%d日 %s:%s' % (TS[0:2], int(TS[2:4]), int(TS[4:6]), TS[6:8], TS[8:10])
W = int(FR.ox + FR.w + 50)
hdr = ['<text x="30" y="34" font-size="18" font-weight="bold" fill="#000">%s　%s</text>' % (e(A.title), e(A.zuban)),
       '<text x="30" y="58" font-size="12" fill="#000">作成 %s ／ 単位 cm ／ 座標系 D00-001〜003（x:左壁内面0→右+、d:前壁内面0→LP側+、h:床0→上+）</text>' % e(now),
       '<text x="30" y="78" font-size="12" fill="#000">SC・CSP・PJは未設置・未調達（計画段階）。SC・PJの位置は前提条件（仮設定）による。梁3の見守りカメラは位置未計測のため不記載。</text>'] + ['<text x="30" y="%d" font-size="12" fill="#000">%s</text>' % (98 + 20 * i, e(n)) for i, n in enumerate(NOTES)]
LX = SD.ox; LY = PL.oy + 10
leg = [(K, False, 2.2, '黒 太線：壁・床・天井（部屋.xlsx）'),
       (GRAY, False, 6, '灰：梁（梁1・梁2・梁3）'),
       (AMB, False, 6, '黄：照明'),
       (AREA, False, 8, '緑：設置エリア（梁1–梁2間）'),
       (CUR, False, 2, '青：カーテン（平面図のみ表示）'),
       (SCC, True, 2, '破線・( )付き：仮設定、または仮設定を含む計算値'),
       (SCC, True, 3, '　SC：A00-003＋製品寸法図、ケースは天井付け'),
       (LPC, False, 0, '紫●：視聴位置 LLP（左）・RLP（右）、目の高さ'),
       (PJC, True, 0, '朱○：PJレンズ中心（A00-004）')]
KIND = {'line': lambda l: (l.get('color', K), l.get('dash', False), l.get('w', 2)),
        'band': lambda l: (l.get('color', K), False, 8),
        'dot':  lambda l: (l.get('color', K), False, 0),
        'ring': lambda l: (l.get('color', K), True, 0)}
for P in PARTS:
    for l in P.get('legend', []):
        tup = KIND[l.get('kind', 'line')](l) + (l['text'],)
        if tup not in leg: leg.append(tup)
g = ['<text x="%s" y="%s" font-size="13" font-weight="bold" fill="#000">凡例</text>' % (f(LX), f(LY))]
for i, (c, d, w, t) in enumerate(leg):
    y = LY + 22 * (i + 1)
    if w: g.append('<line x1="%s" y1="%s" x2="%s" y2="%s" %s/>' % (f(LX), f(y - 4), f(LX + 30), f(y - 4), st(c, w, d)))
    elif d: g.append('<circle cx="%s" cy="%s" r="4.5" fill="white" stroke="%s" stroke-width="2"/>' % (f(LX + 15), f(y - 4), c))
    else: g.append('<circle cx="%s" cy="%s" r="4" fill="%s"/>' % (f(LX + 15), f(y - 4), c))
    g.append('<text x="%s" y="%s" font-size="12" fill="#000">%s</text>' % (f(LX + 40), f(y), e(t)))
y = LY + 22 * (len(leg) + 2)
SRC = ['出典：部屋.xlsx（Sheet1）、確定事項ファイル（D00-001〜004、A00-003、A00-004）、',
       '　　　SC製品寸法図 EP-100HM-MRW1-WF204（オーエスエム）、',
       '　　　依頼主回答（セッション01：SC天井付け、x>273は壁なし、LP h=100は目の高さ）']
ext = [x for P in PARTS for x in P.get('src', [])]
if ext:
    SRC[-1] += '、'
    row = '　　　'
    for i, x in enumerate(ext):
        x += '、' if i < len(ext) - 1 else ''
        if len(row + x) > 46 and row.strip('　'): SRC.append(row); row = '　　　'
        row += x
    SRC.append(row)
for s_ in SRC:
    g.append('<text x="%s" y="%s" font-size="12" fill="#000">%s</text>' % (f(LX), f(y), e(s_))); y += 18
H = int(FR.oy + FR.h + 50)
svg = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" font-family="Hiragino Sans, Yu Gothic, Meiryo, Noto Sans CJK JP, Noto Sans CJK TC, sans-serif" font-size="%d">' % (W, H, W, H, FS),
       '<defs><marker id="ar" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#000"/></marker></defs>',
       '<rect x="0" y="0" width="%d" height="%d" fill="#ffffff"/>' % (W, H)] + hdr + out + g + ['</svg>']
open(OUT, 'w', encoding='utf-8').write('\n'.join(svg) + '\n')
print('wrote', OUT, W, H)
