#!/usr/bin/env python3
# K117 保持具の形（案1）。CSPは csp.py（solo）で描き、その上に保持具を重ねる（F7 c：CSPは csp.py で描く。ツールは import せずコマンドで呼ぶ）
# 重ねる座標は csp.py solo と同じ作図規則（S=8、余白6、P0原点のCSP基準の相対座標 cm、x＝CSP左端0）で計算する。
# 入力：A01-001（H17.0×W57.1×D21.4）、A02-002（チルト24°）、A03-001（底面の部分支持板 P0側から0.7D、厚さ≦2.86、背面より後ろに出さない、前面上角の爪）、
#   D04-004（外れる向きすべてを形で拘束）、K112（収納 C h=245.885、C 左d=52・右d=70、CSP P0 d=47.77・h=242.47）、A06-004（リンク面 左95.55・右163.95、CSP左端104.6・右端161.7）、
#   A06-003（C′：コの字で両持ち、ブッシュ間隔35）。板厚・材質（アルミ板 厚3）は仮
import math, subprocess, re, html, glob, os
e = html.escape
T0 = '/home/claude/ceiling-project/ツール/2609291226_csp.py'
r = subprocess.run(['python3', T0, 'solo', '--zuban', 'K117', '--title', '保持具の形（案1）', '-o', '/mnt/user-data/outputs/{ts}_K117_保持具の形_案1.svg'], capture_output=True, text=True)
out = r.stdout.strip().split('wrote ')[-1].strip()
W_, D_, H_ = 57.1, 21.4, 17.0; tl = math.radians(24); c, s = math.cos(tl), math.sin(tl)
dh = lambda u, w: (u*c + w*s, -u*s + w*c)
dmin, dmax, hmin, hmax = 0.0, D_*c + H_*s, -D_*s, H_*c
S, mg = 8, 6
PLx = lambda x: 90 + (x + mg)*S; PLy = lambda d: 190 + (d - (dmin - mg))*S
FRoy = 190 + (dmax - dmin + 2*mg)*S + 70
FRx = PLx; FRy = lambda h: FRoy + ((hmax + mg) - h)*S
SDox = 90 + (W_ + 2*mg)*S + 90
SDx = lambda d: SDox + (d - (dmin - mg))*S; SDy = FRy
# 部屋座標→CSP基準（収納時）
P0d, P0h, xL = 47.77, 242.47, 104.6
rd = lambda d: d - P0d; rh = lambda h: h - P0h; rx = lambda x: x - xL
CL = (rx(95.55), rd(52.0), rh(245.885)); CR = (rx(163.95), rd(70.0), rh(245.885))
AL, PN, BR, K = '#7F77DD', '#333', '#E6A23C', '#c0392b'
add = []
def poly(pts, col, op=0.35, dash=True):
    add.append(f'<polygon points="{" ".join(f"{a:.1f},{b:.1f}" for a, b in pts)}" fill="{col}" fill-opacity="{op}" stroke="{col}" stroke-width="1.4" {"stroke-dasharray=\"5 3\"" if dash else ""}/>')
def rect(x0, y0, x1, y1, col, op=0.35): poly([(x0,y0),(x1,y0),(x1,y1),(x0,y1)], col, op)
def txt(x, y, t, col='#222', a='start', fs=11): add.append(f'<text x="{x:.1f}" y="{y:.1f}" fill="{col}" text-anchor="{a}" font-size="{fs}">{e(t)}</text>')
t = 0.3   # 板厚（仮）
# --- 側面（d-h）：底板（u=0.45〜0.7D、w=-0.3〜0）、爪（上面 u=19.4〜21.4、前面 w=15〜17 を回り込む）、側板の外形、Cピン
bot = [dh(0.45, 0), dh(0.7*D_, 0), dh(0.7*D_, -t), dh(0.45, -t)]
poly([(SDx(d), SDy(h)) for d, h in bot], AL, 0.6)
claw = [dh(D_-2.0, H_+t), dh(D_+t, H_+t), dh(D_+t, H_-2.0), dh(D_, H_-2.0), dh(D_, H_), dh(D_-2.0, H_)]
poly([(SDx(d), SDy(h)) for d, h in claw], AL, 0.6)
def hull(p):
    p=sorted(set(p)); cr=lambda o,a,b:(a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0]); lo=[]; up=[]
    for q in p:
        while len(lo)>=2 and cr(lo[-2],lo[-1],q)<=0: lo.pop()
        lo.append(q)
    for q in reversed(p):
        while len(up)>=2 and cr(up[-2],up[-1],q)<=0: up.pop()
        up.append(q)
    return lo[:-1]+up[:-1]
side = hull(bot+claw+[(CL[1]+a_, CL[2]+b_) for a_ in (-2.5,2.5) for b_ in (-2.5,2.5)]+[(CR[1]+a_, CR[2]+b_) for a_ in (-2.5,2.5) for b_ in (-2.5,2.5)])
poly([(SDx(d), SDy(h)) for d, h in side], AL, 0.15)
for (xx, dd, hh), lab in ((CL, 'C（左）'), (CR, 'C′（右）')):
    add.append(f'<circle cx="{SDx(dd):.1f}" cy="{SDy(hh):.1f}" r="5" fill="{PN}"/>')
    txt(SDx(dd)+8, SDy(hh)-6, f'{lab} ({dd:.2f}, {hh:.2f})', PN)
txt(SDx(-5), SDy(-12.5), '紫：保持具（底板・爪と、側板の外形＝底板・爪・Cのピンを包む範囲）', AL)
# --- 正面（x-h）：底板（全幅）、左右の側板、左のつなぎ板（側板→左リンクのコの字）、右はC′保持具の内板が側板を兼ねる
ylo, yhi = hmin - 0.3, hmax + 0.3
rect(FRx(-t), FRy(yhi), FRx(0), FRy(ylo), AL, 0.6)            # 左側板
rect(FRx(W_), FRy(yhi), FRx(W_+1.0), FRy(ylo), AL, 0.6)       # 右側板（厚1.0＝C′保持具の内板、K098）
rect(FRx(-t), FRy(dh(0.45,0)[1]), FRx(W_+1.0), FRy(dh(0.7*D_,-t)[1]), AL, 0.6)     # 底板（傾いているので正面では帯 h=0〜-6.4 に見える）
# 左：コの字（ブッシュ間隔35 → 板中心 x=CL±1.75、厚1.0）と、側板までのつなぎ板（厚1.0、Cの高さ±3）
for xc_ in (CL[0]-1.75, CL[0]+1.75): rect(FRx(xc_-0.5), FRy(CL[2]+3), FRx(xc_+0.5), FRy(CL[2]-3), BR, 0.7)
rect(FRx(CL[0]+2.25), FRy(CL[2]+3), FRx(-t), FRy(CL[2]-3), K, 0.35)
txt(FRx(CL[0]), FRy(CL[2]+3)-6, '左Cのコの字', BR, 'middle')
txt(FRx((CL[0]+2.25-t)/2), FRy(CL[2]-3)+16, f'つなぎ板 {abs(-t-(CL[0]+2.25)):.2f}', K, 'middle')
rect(FRx(CR[0]-0.75-1.75), FRy(CR[2]+3), FRx(CR[0]-0.75-0.75), FRy(CR[2]-3), BR, 0.0)
rect(FRx(CR[0]+1.75-0.5), FRy(CR[2]+3), FRx(CR[0]+1.75+0.5), FRy(CR[2]-3), BR, 0.7)
for (xx, dd, hh) in (CL, CR): add.append(f'<line x1="{FRx(xx-3):.1f}" y1="{FRy(hh):.1f}" x2="{FRx(xx+3):.1f}" y2="{FRy(hh):.1f}" stroke="{PN}" stroke-width="3"/>')
txt(FRx(CR[0]), FRy(CR[2]+3)-6, '右C′のコの字（内板＝右側板）', BR, 'middle')
# OA（左）の面 x=96.8〜99.3 を正面に示す
rect(FRx(rx(96.8)), FRy(yhi+2), FRx(rx(99.3)), FRy(ylo), '#2E9E6B', 0.12); txt(FRx(rx(98.05)), FRy(yhi+2)-4, 'OAの面', '#2E9E6B', 'middle')
# --- 平面（x-d）：左右のCの位置と側板
for (xx, dd, hh) in (CL, CR):
    add.append(f'<circle cx="{PLx(xx):.1f}" cy="{PLy(dd):.1f}" r="5" fill="{PN}"/>')
rect(PLx(-t), PLy(0), PLx(0), PLy(dmax), AL, 0.6); rect(PLx(W_), PLy(0), PLx(W_+1.0), PLy(dmax), AL, 0.6)
rect(PLx(CL[0]+2.25), PLy(CL[1]-3), PLx(-t), PLy(CL[1]+3), K, 0.35)
txt(PLx(CL[0]), PLy(CL[1])-10, '左C d=52', PN, 'middle'); txt(PLx(CR[0]), PLy(CR[1])-10, '右C′ d=70', PN, 'middle')
# --- 注記
mass = {'底板 57.1×(0.7D)×厚0.3': 57.1*0.7*D_*0.3*2.7e-3, '側板 2枚（概略 22×18×0.3）': 2*22*18*0.3*2.7e-3, '爪 57.1×4×0.3': 57.1*4*0.3*2.7e-3,
        '左のつなぎ板・コの字（厚1.0、概略）': (6.8*6 + 2*6*6)*1.0*2.7e-3, '右のコの字の外板（厚1.0）': 6*6*1.0*2.7e-3}
notes = ['形（案1）の要点：', '・下：底板（A03-001、P0側から0.7D）。前（LP側への滑り）・上：前面上角の爪（P3側）。左右：側板。',
 '・左右のC・C′の高さは同じ（h=245.885、収納）、dは左52・右70（Δd=18）。右はC′保持具の内板（x=161.7〜162.7）がそのまま右側板（K098の積み重ね）',
 f'・左は左リンクの面（x=95.55）とCSP左端（104.6）の間が離れているため、側板からコの字までのつなぎ板（x方向 {abs(-t-(CL[0]+2.25)):.2f}）が要る。OAの面（x=96.8〜99.3）を横切る（当たらないかは未確認）',
 '・後ろ（SC側）への外れ：背面より後ろに出せない（A03-001。収納時 P0 d=47.77 と前壁側の限界 47.5 の差は0.27）ため、形で止める手段が未決（D04-004が未達）',
 '・質量の目安（アルミ、厚さは仮）：' + '、'.join(f'{k} {v:.2f}kg' for k, v in mass.items()) + f'　合計 約{sum(mass.values()):.2f}kg（ねじ・ブッシュ別）。予算 約3.8kg（K116）',
 '・未検討：グリルの有無（爪の形）、保持具の安全率（A04-007 の保持具の値は未見直し）、底板と側板・爪のつなぎ方、CSPの出し入れの手順']
svg = open(out, encoding='utf-8').read()
m = re.search(r'viewBox="0 0 (\d+) (\d+)" width="(\d+)" height="(\d+)"', svg); Wd, Hd = int(m.group(1)), int(m.group(2)); Hn = Hd + 200
svg = svg.replace(m.group(0), f'viewBox="0 0 {Wd} {Hn}" width="{Wd}" height="{Hn}"').replace(f'<rect x="0" y="0" width="{Wd}" height="{Hd}" fill="#ffffff"/>', f'<rect x="0" y="0" width="{Wd}" height="{Hn}" fill="#ffffff"/>')
for i, n in enumerate(notes): txt(40, Hd - 40 + i*22, n, '#222', 'start', 12)
svg = svg.replace('</svg>', '\n'.join(add) + '\n</svg>')
svg = svg.replace('（csp.py で作図）', '（CSPは csp.py で作図、保持具はK117のpyで重ね描き）。保持具：A03-001、D04-004、A06-003、A06-004、K112、K116')
open(out, 'w', encoding='utf-8').write(svg)
print(out, CL, CR, sum(mass.values()))
