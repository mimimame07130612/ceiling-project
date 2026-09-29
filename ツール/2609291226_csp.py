#!/usr/bin/env python3
# csp.py — CSP（センタースピーカー）作図ツール（セッション05 作成）
# CSPの位置・チルトから外形を計算し、①sanmen.py に渡す重ね描きJSON、または ②CSP単体の三面図SVG を出力する（F7 c）。
# 部屋は描かない。sanmen.py とは import で連携せず、出力したJSONをコマンドで渡す（F7 e）。
#
# 入力とした確定事項・前提条件（数値が確定事項ファイルと食い違う場合は確定事項ファイルを正とする。F7 f）
#   A01-001 CSP外形 H17.0×W57.1×D21.4（仮設定）／A02-002 チルト24°、LP側を下げる（仮設定）／D03-003 水平の振りなし
#
# 角の呼び方（K015・K017と同じ。側面図＝d-h面）
#   P0：SC側下角（背面・下）＝外接のSC側端（d最小）。 P1：LP側下角（前面・下）＝最下点。
#   P2：SC側上角（背面・上）＝最上点。            P3：LP側上角（前面・上）。  前面（バッフル）＝P1–P3の面（LP側）。
#   チルト0〜90°未満では、P0がd最小・P1がh最小・P2がh最大になる。
#
# 使い方:
#  ① 重ね描きJSON（部屋の三面図に重ねる）
#     python3 YYMMDDhhmm_csp.py json -o 出力.json --pose 名前,x中心,d1,h最下点[,色] [--pose ...] [--tilt 24] [--corners] [--solid]
#       x中心：CSP左右中心のx。d1：P0のd。h最下点：P1のh。色は#rrggbb（省略時は順に青・赤・緑・紫）。
#       続けて python3 YYMMDDhhmm_sanmen.py --zuban Kxxx --title 図題 -o '...' 出力.json [他のJSON ...]
#       --corners：側面図にP0〜P3を点と文字で示す。 --solid：実線で描く（既定は破線＝仮設定を含む値。A01-001が仮設定のため）。
#  ② CSP単体の三面図
#     python3 YYMMDDhhmm_csp.py solo --zuban Kxxx --title 図題 -o '/mnt/user-data/outputs/{ts}_Kxxx_本体名.svg' [--tilt 24]
#       CSP基準の相対座標（P0原点、x=CSP左端0）。{ts} は本コマンド内で TZ=Asia/Tokyo date +%y%m%d%H%M により取得した値に置き換わる（F3）。
#  いずれも、計算した外形の数値（外接奥行・外接高さ・各角の座標）を標準出力に表示する。
import argparse, json, math, subprocess, html

W, D, H = 57.1, 21.4, 17.0          # A01-001
TILT_DEF = 24.0                     # A02-002
COLORS = ['#2C6FB0', '#C0392B', '#2E9E6B', '#6A5FD0']

def shape(tilt_deg):
    """CSP基準（P0原点）の側面の角 (d, h) と外接寸法。局所 u：背面→前面、w：底面→上面。"""
    t = math.radians(tilt_deg); c, s = math.cos(t), math.sin(t)
    dh = lambda u, w: (u * c + w * s, -u * s + w * c)
    P = {'P0': dh(0, 0), 'P1': dh(D, 0), 'P2': dh(0, H), 'P3': dh(D, H)}
    dmin = min(p[0] for p in P.values()); dmax = max(p[0] for p in P.values())
    hmin = min(p[1] for p in P.values()); hmax = max(p[1] for p in P.values())
    return P, (dmin, dmax, hmin, hmax)

def place(tilt, xc, d1, hlow):
    """部屋座標での角と外接範囲。d1＝P0のd、hlow＝最下点のh。"""
    P, (dmin, dmax, hmin, hmax) = shape(tilt)
    od, oh = d1 - P['P0'][0], hlow - hmin
    Q = {k: (v[0] + od, v[1] + oh) for k, v in P.items()}
    return Q, (xc - W / 2, xc + W / 2, dmin + od, dmax + od, hmin + oh, hmax + oh)

def r2(v): return round(v, 2)
def report(name, Q, box, tilt):
    x0, x1, d0, d1, h0, h1 = box
    print('[%s] チルト%g°  x=%.2f〜%.2f  d=%.2f〜%.2f（外接奥行%.2f）  h=%.2f〜%.2f（外接高さ%.2f）' % (
        name, tilt, x0, x1, d0, d1, d1 - d0, h0, h1, h1 - h0))
    print('   ' + '  '.join('%s(d=%.2f, h=%.2f)' % (k, *Q[k]) for k in ('P0', 'P1', 'P2', 'P3')))

def cmd_json(a):
    items, legend = [], []
    for i, ps in enumerate(a.pose):
        f_ = ps.split(',')
        name = f_[0]; xc, d1, hl = map(float, f_[1:4])
        col = f_[4] if len(f_) > 4 else COLORS[i % len(COLORS)]
        Q, box = place(a.tilt, xc, d1, hl); report(name, Q, box, a.tilt)
        x0, x1, dd0, dd1, h0, h1 = map(r2, box)
        dash = not a.solid
        st = dict(color=col, fill=col, op=0.15, w=1.4, dash=dash)
        items += [dict(t='rect', view='plan', p=[x0, dd0, x1, dd1], **st),
                  dict(t='rect', view='front', p=[x0, h0, x1, h1], **st),
                  dict(t='poly', view='side', p=[[r2(Q[k][0]), r2(Q[k][1])] for k in ('P0', 'P1', 'P3', 'P2')],
                       **dict(st, op=0.18))]
        if a.corners:
            for k in ('P0', 'P1', 'P2', 'P3'):
                items.append(dict(t='pt', view='side', p=[r2(Q[k][0]), r2(Q[k][1])], color=col, r=3))
                items.append(dict(t='text', view='side', p=[r2(Q[k][0]), r2(Q[k][1])], s=k, dx=4, dy=-4, color=col))
        legend.append(dict(text='%s：CSP %s（チルト%g°）' % ('破線' if dash else '実線', name, a.tilt),
                           color=col, dash=dash, kind='line'))
    out = dict(legend=legend, src=['A01-001', 'A02-002', 'D03-003'], items=items)
    json.dump(out, open(a.o, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('wrote', a.o)

def cmd_solo(a):
    TS = subprocess.run(['date', '+%y%m%d%H%M'], capture_output=True, text=True, env={'TZ': 'Asia/Tokyo'}).stdout.strip()
    OUT = a.o.replace('{ts}', TS)
    P, (dmin, dmax, hmin, hmax) = shape(a.tilt)
    report('CSP単体（P0原点）', P, (0, W, dmin, dmax, hmin, hmax), a.tilt)
    e = html.escape; S = 8; out = []
    K, RED, GRY = '#333333', '#C0392B', '#8a857a'
    def f(n): return ('%.1f' % n).rstrip('0').rstrip('.')
    class V:
        def __init__(s, ox, oy, u0, u1, v0, v1, vdown): s.ox, s.oy, s.u0, s.u1, s.v0, s.v1, s.vd = ox, oy, u0, u1, v0, v1, vdown
        def X(s, u): return s.ox + (u - s.u0) * S
        def Y(s, v): return s.oy + ((v - s.v0) * S if s.vd else (s.v1 - v) * S)
    def poly(v, pts, col=K, fill='#dfe9f3', dash=True):
        out.append('<polygon points="%s" fill="%s" stroke="%s" stroke-width="1.6"%s/>' % (
            ' '.join('%s,%s' % (f(v.X(u)), f(v.Y(w))) for u, w in pts), fill, col, ' stroke-dasharray="6 3"' if dash else ''))
    def ln(v, pts, col=RED, w=3):
        out.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="%s"/>' % (
            ' '.join('%s,%s' % (f(v.X(u)), f(v.Y(w_))) for u, w_ in pts), col, w))
    def txt(x, y, t, col='#222', anchor='start', size=12, bold=False):
        out.append('<text x="%s" y="%s" fill="%s" text-anchor="%s" font-size="%s"%s>%s</text>' % (
            f(x), f(y), col, anchor, size, ' font-weight="bold"' if bold else '', e(t)))
    def T(v, u, w, t, dx=0, dy=0, **k): txt(v.X(u) + dx, v.Y(w) + dy, t, **k)
    BD, BH = dmax - dmin, hmax - hmin
    mg = 6
    PL = V(90, 190, -mg, W + mg, dmin - mg, dmax + mg, True)                    # 平面図 x-d（SC側が上）
    FR = V(90, PL.oy + (BD + 2 * mg) * S + 70, -mg, W + mg, hmin - mg, hmax + mg, False)   # 正面図 x-h（LP側から見る）
    SD = V(PL.ox + (W + 2 * mg) * S + 90, FR.oy, dmin - mg, dmax + mg, hmin - mg, hmax + mg, False)  # 側面図 d-h（左壁側から）
    for v, nm in ((PL, '平面図（x-d、見下ろし。SC側が上）'), (FR, '正面図（x-h、LP側からSC側を見る）'), (SD, '側面図（d-h、左壁側から見る。右がLP側）')):
        txt(v.X(v.u0), v.oy - 14, nm, bold=True, size=13)
    # 平面図
    poly(PL, [(0, dmin), (W, dmin), (W, dmax), (0, dmax)])
    T(PL, 0, dmin, 'P0側（SC側） d=%s' % f(dmin), dy=-6); T(PL, 0, dmax, 'LP側 d=%.2f' % dmax, dy=18)
    T(PL, W, (dmin + dmax) / 2, '外接奥行 %.2f' % BD, dx=8, dy=4)
    T(PL, W / 2, dmax, 'W %s' % f(W), dy=36, anchor='middle')
    # 正面図
    poly(FR, [(0, hmin), (W, hmin), (W, hmax), (0, hmax)])
    T(FR, W, hmax, '最上点（P2） h=%.2f' % hmax, dx=8, dy=4); T(FR, W, hmin, '最下点（P1） h=%.2f' % hmin, dx=8, dy=4)
    T(FR, W, (hmin + hmax) / 2, '外接高さ %.2f' % BH, dx=8, dy=4)
    T(FR, W / 2, hmin, 'W %s（x=0〜%s）' % (f(W), f(W)), dy=22, anchor='middle')
    # 側面図
    poly(SD, [P[k] for k in ('P0', 'P1', 'P3', 'P2')])
    ln(SD, [P['P1'], P['P3']])
    T(SD, *P['P0'], 'P0 SC側下角 (%.2f, %.2f)' % P['P0'], dx=-6, dy=16, anchor='end')
    T(SD, *P['P1'], 'P1 最下点 (%.2f, %.2f)' % P['P1'], dx=6, dy=16)
    T(SD, *P['P2'], 'P2 最上点 (%.2f, %.2f)' % P['P2'], dx=-6, dy=-8, anchor='end')
    T(SD, *P['P3'], 'P3 LP側上角 (%.2f, %.2f)' % P['P3'], dx=6, dy=-8)
    mid = ((P['P1'][0] + P['P3'][0]) / 2, (P['P1'][1] + P['P3'][1]) / 2)
    T(SD, *mid, '前面（バッフル）', dx=10, dy=4, col=RED)
    Wd = int(SD.X(SD.u1) + 260); Hd = int(FR.Y(FR.v0) + 120)
    hdr = [('%s　%s' % (a.title, a.zuban), 18, True),
           ('作成 20%s年%d月%d日 %s:%s ／ 単位 cm ／ CSP基準の相対座標（P0＝SC側下角を原点、x＝CSP左端を0、d：LP側+、h：上+）' % (
               TS[0:2], int(TS[2:4]), int(TS[4:6]), TS[6:8], TS[8:10]), 12, False),
           ('CSP外形 H%s×W%s×D%s（A01-001、仮設定）、チルト%g°・LP側を下げる（A02-002、仮設定）。破線：仮設定を含む値。赤：前面（バッフル）' % (
               f(H), f(W), f(D), a.tilt), 12, False),
           ('出典：A01-001、A02-002、D03-003（csp.py で作図）', 12, False)]
    head = ['<text x="40" y="%d" font-size="%d" fill="#000"%s>%s</text>' % (36 + 22 * i, sz, ' font-weight="bold"' if b else '', e(t))
            for i, (t, sz, b) in enumerate(hdr)]
    svg = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" font-family="Hiragino Sans, Yu Gothic, Meiryo, Noto Sans CJK JP, sans-serif" font-size="12">' % (Wd, Hd, Wd, Hd),
           '<rect x="0" y="0" width="%d" height="%d" fill="#ffffff"/>' % (Wd, Hd)] + head + out + ['</svg>']
    open(OUT, 'w', encoding='utf-8').write('\n'.join(svg) + '\n')
    print('wrote', OUT)

ap = argparse.ArgumentParser(); sub = ap.add_subparsers(dest='mode', required=True)
j = sub.add_parser('json'); j.add_argument('-o', required=True); j.add_argument('--pose', action='append', required=True)
j.add_argument('--tilt', type=float, default=TILT_DEF); j.add_argument('--corners', action='store_true'); j.add_argument('--solid', action='store_true')
s_ = sub.add_parser('solo'); s_.add_argument('-o', required=True); s_.add_argument('--zuban', required=True); s_.add_argument('--title', required=True)
s_.add_argument('--tilt', type=float, default=TILT_DEF)
A = ap.parse_args()
cmd_json(A) if A.mode == 'json' else cmd_solo(A)
