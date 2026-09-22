#!/usr/bin/env python3
# zuwaku.py — 図枠コマンド（出力ルール O7-7）
# 部品JSON（heya.py や図ごとの重ね描き）を受け取り、O7-1〜O7-4 の図枠つき SVG を出力する。
# 使い方:
#   python3 zuwaku.py -o 出力.svg --view dh --title 図題 [--zuban K001] [--proj 投影の説明]
#                     [--range umin umax vmin vmax] 部品1.json [部品2.json ...]
#   --view : dh=側面図(d横, h縦) / xh=正面図(x横, h縦) / xd=上面図(x横, d縦・下向き+)
#   --zuban: 保管する図のみ指定（O7-3(1)）。省略時は「図番なし（チャット表示）」
#   作成日時は本コマンド内で TZ=Asia/Tokyo date により1回だけ取得する（F4）。
#   -o に {ts} を書くとプレフィクス YYMMDDhhmm に置き換わり、図中の作成日時と一致する。
# 部品JSONの形式:
#   {"legend":[{"text":..,"color":..,"dash":bool}], "src":[出典..],
#    "items":[{"t":"line"|"poly"|"rect"|"pt"|"circle"|"text", "p":座標(cm), "cls":"kakutei"|"kari",
#              "color":線色, "fill":塗り色, "op":塗り不透明度, "r":半径, "s":文字, "anchor":..,"dx":px,"dy":px}]}
#   座標は各ビューの (横軸, 縦軸) の cm 値。cls=kakutei は実線、kari は破線（O7-4）。
#   仮置き値の文字は部品側で ( ) を付けて渡す。
import argparse, json, subprocess, html

VIEWS = {
    'dh': dict(u='d', v='h', vdown=False, proj='+x方向を見た側面図（左壁側から）'),
    'xh': dict(u='x', v='h', vdown=False, proj='−d方向を見た正面図（LP側からSC側を見る）'),
    'xd': dict(u='x', v='d', vdown=True,  proj='上面図（−h方向に見下ろす。SC側が上）'),
}
W = 680; L = 50; R = 630; TOP = 78; FS = 12; LH = 18
DASH = '5 3'

ap = argparse.ArgumentParser()
ap.add_argument('-o', required=True)
ap.add_argument('--view', required=True, choices=VIEWS)
ap.add_argument('--title', required=True)
ap.add_argument('--zuban', default='')
ap.add_argument('--proj', default='')
ap.add_argument('--range', nargs=4, type=float)
ap.add_argument('parts', nargs='+')
a = ap.parse_args()
V = VIEWS[a.view]
parts = [json.load(open(p, encoding='utf-8')) for p in a.parts]
items = [it for p in parts for it in p.get('items', [])]

def pts(it):
    p = it['p']
    if it['t'] in ('pt', 'circle', 'text'): return [p]
    if it['t'] == 'rect': return [p[:2], p[2:]]
    return p
if a.range:
    umin, umax, vmin, vmax = a.range
else:
    allp = [q for it in items for q in pts(it)]
    umin = min(q[0] for q in allp + [[0, 0]]); umax = max(q[0] for q in allp)
    vmin = min(q[1] for q in allp + [[0, 0]]); vmax = max(q[1] for q in allp)
    pu = (umax - umin) * 0.03; pv = (vmax - vmin) * 0.03
    umin -= pu; umax += pu; vmin -= pv; vmax += pv
s = (R - L) / (umax - umin)
H_draw = (vmax - vmin) * s
def X(u): return L + (u - umin) * s
def Y(v): return TOP + ((v - vmin) * s if V['vdown'] else (vmax - v) * s)
def f(n): return ('%.2f' % n).rstrip('0').rstrip('.')
e = lambda t: html.escape(str(t))

out = []
def stroke(it, w=1.0):
    c = it.get('color', '#333333')
    d = ' stroke-dasharray="%s"' % DASH if it.get('cls', 'kakutei') == 'kari' else ''
    return 'stroke="%s" stroke-width="%s"%s' % (c, it.get('w', w), d)
for it in items:
    t = it['t']
    if t == 'line' or t == 'poly':
        ps = ' '.join('%s,%s' % (f(X(u)), f(Y(v))) for u, v in it['p'])
        if t == 'line':
            out.append('<polyline points="%s" fill="none" %s/>' % (ps, stroke(it)))
        else:
            out.append('<polygon points="%s" fill="%s" fill-opacity="%s" %s/>' % (
                ps, it.get('fill', 'none'), it.get('op', 0.25), stroke(it)))
    elif t == 'rect':
        u0, v0, u1, v1 = it['p']
        x0, x1 = sorted([X(u0), X(u1)]); y0, y1 = sorted([Y(v0), Y(v1)])
        out.append('<rect x="%s" y="%s" width="%s" height="%s" fill="%s" fill-opacity="%s" %s/>' % (
            f(x0), f(y0), f(x1 - x0), f(y1 - y0), it.get('fill', 'none'), it.get('op', 0.25), stroke(it)))
    elif t == 'circle':
        u, v = it['p']
        out.append('<circle cx="%s" cy="%s" r="%s" fill="%s" fill-opacity="%s" %s/>' % (
            f(X(u)), f(Y(v)), f(it['r'] * s), it.get('fill', 'none'), it.get('op', 0.25), stroke(it)))
    elif t == 'pt':
        u, v = it['p']
        out.append('<circle cx="%s" cy="%s" r="%s" fill="%s" stroke="none"/>' % (
            f(X(u)), f(Y(v)), it.get('r', 3), it.get('color', '#333333')))
    elif t == 'text':
        u, v = it['p']
        out.append('<text x="%s" y="%s" text-anchor="%s" fill="%s">%s</text>' % (
            f(X(u) + it.get('dx', 0)), f(Y(v) + it.get('dy', 0)), it.get('anchor', 'start'),
            it.get('color', '#222222'), e(it['s'])))

# 軸と原点（O7-1）
ax = []
x0 = X(0) if umin <= 0 <= umax else L
y0 = Y(0) if vmin <= 0 <= vmax else (TOP if V['vdown'] else TOP + H_draw)
ax.append('<circle cx="%s" cy="%s" r="3" fill="none" stroke="#000"/>' % (f(x0), f(y0)))
ax.append('<text x="%s" y="%s" fill="#000">O（%s=0, %s=0）</text>' % (f(x0 + 6), f(y0 + 30 if not V['vdown'] else y0 - 6), V['u'], V['v']))
ax.append('<text x="%s" y="%s" text-anchor="end" fill="#000">+%s →</text>' % (R, f(TOP + H_draw + 16), V['u']))
ax.append('<text x="%s" y="%s" fill="#000">+%s %s</text>' % (8, f(TOP + H_draw - 4 if V['vdown'] else TOP + 12), V['v'], '↓' if V['vdown'] else '↑'))

# ヘッダ（O7-3(1)(2)(3)、O7-2）
ts = subprocess.run(['date', '+%y%m%d%H%M'], capture_output=True, text=True,
                    env={'TZ': 'Asia/Tokyo'}).stdout.strip()
now = '20%s年%d月%d日 %s:%s' % (ts[0:2], int(ts[2:4]), int(ts[4:6]), ts[6:8], ts[8:10])  # F4: プレフィクスと同じ値
a.o = a.o.replace('{ts}', ts)
zb = a.zuban if a.zuban else '図番なし（チャット表示）'
hd = ['<text x="%d" y="24" font-weight="bold" fill="#000">%s　%s</text>' % (L, e(a.title), e(zb)),
      '<text x="%d" y="44" fill="#000">作成 %s／%s／単位 cm</text>' % (L, e(now), e(a.proj or V['proj']))]

# 凡例（O7-3(5)、O7-4、O7-5）
lg = [('#000', False, '実線・通常表記：確定（与件・カタログ・確定事項）'),
      ('#000', True, '破線・( )表記：仮置き、または仮置きを含む計算値')]
seen = set(x[2] for x in lg)
for p in parts:
    for l in p.get('legend', []):
        if l['text'] not in seen:
            seen.add(l['text']); lg.append((l.get('color', '#000'), l.get('dash', False), l['text']))
src = []
for p in parts:
    for s_ in p.get('src', []):
        if s_ not in src: src.append(s_)
ly = TOP + H_draw + 52
leg = ['<text x="%d" y="%s" font-weight="bold" fill="#000">凡例</text>' % (L, f(ly))]
for i, (c, d, t) in enumerate(lg):
    yy = ly + LH * (i + 1)
    leg.append('<line x1="%d" y1="%s" x2="%d" y2="%s" stroke="%s" stroke-width="1.5"%s/>' % (
        L, f(yy - 4), L + 28, f(yy - 4), c, ' stroke-dasharray="%s"' % DASH if d else ''))
    leg.append('<text x="%d" y="%s" fill="#000">%s</text>' % (L + 36, f(yy), e(t)))
yy = ly + LH * (len(lg) + 1)
leg.append('<text x="%d" y="%s" fill="#000">出典：%s</text>' % (L, f(yy), e('、'.join(src) if src else 'なし')))
Htot = int(yy + 20)

svg = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" font-family="Hiragino Sans, Yu Gothic, Meiryo, Noto Sans CJK JP, Noto Serif CJK JP, sans-serif" font-size="%d">' % (W, Htot, W, Htot, FS),
       '<rect x="0" y="0" width="%d" height="%d" fill="#ffffff"/>' % (W, Htot)]
svg += hd + out + ax + leg + ['</svg>']
open(a.o, 'w', encoding='utf-8').write('\n'.join(svg) + '\n')
print('wrote %s (%d x %d)' % (a.o, W, Htot))
