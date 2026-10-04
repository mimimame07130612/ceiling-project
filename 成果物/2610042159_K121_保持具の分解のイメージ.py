#!/usr/bin/env python3
# K121 保持具（案3：K120）の分解のイメージ。部屋もCSPも描かない（F7 d）。保持具はCSPの傾き24°を戻した向き（CSP基準の局所座標）で、斜投影の見取り図
# 局所座標（cm）：x＝CSP左端0〜右端57.1、u＝背面0→前面21.4（LP側）、w＝底面0→上面17。Cの位置は K118 の値を局所座標に直したもの
# 部品の寸法・形材の断面・ボルトは仮。分解の向き・量は見やすさのため
import math, subprocess, html
TS = subprocess.run(['date','+%y%m%d%H%M'],capture_output=True,text=True,env={'TZ':'Asia/Tokyo'}).stdout.strip()
e = html.escape
c24, s24 = math.cos(math.radians(24)), math.sin(math.radians(24))
def loc(d, h): return (d*c24 - h*s24, d*s24 + h*c24)
CLu, CLw = loc(4.23, 3.415); CRu, CRw = loc(22.23, 3.415)
S = 7.5; OX, OY = 330, 640; k = 0.55; ang = math.radians(32)
def P(x, u, w): return (OX + (x + u*k*math.cos(ang))*S, OY - (w + u*k*math.sin(ang))*S)
o = []
def box(x0,x1,u0,u1,w0,w1,col,op=0.55,off=(0,0,0),lab=None,lp=None):
    x0+=off[0]; x1+=off[0]; u0+=off[1]; u1+=off[1]; w0+=off[2]; w1+=off[2]
    faces = [[(x0,u0,w1),(x1,u0,w1),(x1,u1,w1),(x0,u1,w1)], [(x0,u0,w0),(x1,u0,w0),(x1,u0,w1),(x0,u0,w1)], [(x1,u0,w0),(x1,u1,w0),(x1,u1,w1),(x1,u0,w1)]]
    for i, f in enumerate(faces):
        pts = ' '.join('%.1f,%.1f' % P(*q) for q in f)
        o.append(f'<polygon points="{pts}" fill="{col}" fill-opacity="{op*(1.0,0.75,0.55)[i]:.2f}" stroke="#333" stroke-width="0.8"/>')
    if lab:
        X, Y = P(*(lp if lp else ((x0+x1)/2, u0, w1)))
        o.append(f'<text x="{X:.1f}" y="{Y-6:.1f}" font-size="13" font-weight="bold" fill="#000" text-anchor="middle">{e(lab)}</text>')
def arrow(a, b):
    (x1,y1),(x2,y2) = P(*a), P(*b)
    o.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#888" stroke-width="1" stroke-dasharray="4 3"/>')
PL, AN, RB, BR, CL = '#B4B2A9', '#85B7EB', '#444441', '#E6A23C', '#D85A30'
# CSPの位置（描かない）を示す枠の代わりに、四隅の小さな印だけ
for q in [(0,0,0),(57.1,0,0),(0,21.4,0),(57.1,21.4,0),(0,0,17),(57.1,0,17),(0,21.4,17),(57.1,21.4,17)]:
    X, Y = P(*q); o.append(f'<circle cx="{X:.1f}" cy="{Y:.1f}" r="2" fill="#999"/>')
X, Y = P(28.5, 10.7, 8.5); o.append(f'<text x="{X:.1f}" y="{Y:.1f}" font-size="12" fill="#999" text-anchor="middle">（ここにCSPが入る：灰色の点は外形の角。CSPの図はK120）</text>')
# ① 底板（寸法切りの平板）＋ゴム帯
box(0,57.1,0.45,15,-0.6,-0.3, PL, off=(0,0,-9), lab='① 底板', lp=(28.5,15,-0.3))
for u0 in (1.0,10.0): box(0,57.1,u0,u0+3,-0.3,0, RB, 0.8, off=(0,0,-5))
arrow((28.5,7.5,-0.3-9),(28.5,7.5,-0.6))
# ② 左側板・③ 右側板（右は厚1.0、C′のコの字の内板を兼ねる）
box(-0.6,-0.3,0,21.7,-0.6,17.6, PL, off=(-12,0,0), lab='② 左側板', lp=(-0.45,0,17.6))
box(57.1,58.1,0,21.7,-0.6,17.6, PL, off=(12,0,0), lab='③ 右側板（＝C′の内板）', lp=(57.6,0,17.6))
arrow((-12.3,10,8),(-0.45,10,8)); arrow((69.6,10,8),(57.6,10,8))
# ④ 底板受けのアングル×2（市販アングル）
for x0, x1, dx in ((-0.3,1.2,-6),(55.9,57.1,6)):
    box(x0,x1,0.45,15,-2.1,-0.6, AN, off=(dx,0,-9), lab=None)
X, Y = P(-6, 15, -11.1); o.append(f'<text x="{X:.1f}" y="{Y+16:.1f}" font-size="13" font-weight="bold" text-anchor="middle">④ 底板受けアングル×2</text>')
# ⑤ 爪（市販アングル、外せる）＋⑥ 爪の取付金具×2
box(0,57.1,21.4,23.7,15.0,17.6, AN, off=(0,6,8), lab='⑤ 爪（アングル、ボルトで外せる）', lp=(28.5,21.4,17.6))
box(0,57.1,21.4,21.7,15.0,17.0, RB, 0.8, off=(0,3,4))
for x0, x1 in ((-0.3,1.7),(55.1,57.1)): box(x0,x1,19.0,23.7,13.0,17.6, AN, 0.7, off=(0,6,8))
arrow((28.5,23.7+6,17.6+8),(28.5,21.7,17))
X, Y = P(57.1, 29.7, 21.6); o.append(f'<text x="{X+8:.1f}" y="{Y:.1f}" font-size="12" text-anchor="start">⑥ 爪の取付金具×2（側板にボルト）</text>')
# ⑦ 後ろの折り返し×2（小さなアングル）
for x0, x1 in ((-0.3,3.0),(54.1,57.4)): box(x0,x1,-0.6,-0.3,6,10, CL, 0.8, off=(0,-10,0))
X, Y = P(0, -10.6, 10); o.append(f'<text x="{X:.1f}" y="{Y-8:.1f}" font-size="13" font-weight="bold" text-anchor="start">⑦ 後ろの折り返し×2（小アングル）</text>')
# ⑧ 左のつなぎ板＋左のコの字（平板2枚＋スペーサー、ボルト）
off8 = (-22, 0, 0)
box(-6.8,-0.6,CLu-3,CLu+3,CLw-3,CLw+3, BR, 0.6, off=off8)
for xc in (-9.05-1.75, -9.05+1.75): box(xc-0.5,xc+0.5,CLu-3,CLu+3,CLw-3,CLw+3, BR, 0.85, off=off8)
X, Y = P(-9.05-22, CLu-3, CLw+3); o.append(f'<text x="{X:.1f}" y="{Y-8:.1f}" font-size="13" font-weight="bold" text-anchor="middle">⑧ 左つなぎ板＋左コの字</text>')
arrow((-0.6-22,CLu,CLw),(-0.6-12,CLu,CLw))
# ⑨ 右のコの字の外板（平板＋スペーサー）
xc = 59.35+1.75; box(xc-0.5,xc+0.5,CRu-3,CRu+3,CRw-3,CRw+3, BR, 0.85, off=(22,0,0))
X, Y = P(xc+22, CRu-3, CRw+3); o.append(f'<text x="{X:.1f}" y="{Y-8:.1f}" font-size="13" font-weight="bold" text-anchor="middle">⑨ 右コの字の外板</text>')
arrow((xc+22,CRu,CRw),(58.1+12,CRu,CRw))
# 部品表
rows = [('①','底板','アルミ板 厚3','寸法切り（オーダー）＋自分で穴あけ'),('②','左側板','アルミ板 厚3','寸法切り（外形が多角形のためレーザー等）＋穴あけ'),
 ('③','右側板＝C′の内板','アルミ板 厚10','寸法切り＋ブッシュ穴は業者（精度）'),('④','底板受け×2','市販アルミアングル','長さ切り（自分で切れないため購入時に切断）＋穴・タップ'),
 ('⑤','爪','市販アルミアングル','同上。ボルトで外せる＝CSPの出し入れ口'),('⑥','爪の取付金具×2','市販の小さなL金具 or アングル','穴あけ'),
 ('⑦','後ろの折り返し×2','市販アングルの短片','長さ切り＋穴あけ'),('⑧','左つなぎ板＋左コの字','アルミ板 厚10・平板＋スペーサー','寸法切り＋ブッシュ穴は業者'),
 ('⑨','右コの字の外板','アルミ板 厚10＋スペーサー','同上'),('－','ゴム板','市販ゴムシート','カッターで切って貼る'),('－','ボルト・ナット','市販','')]
y0 = 860
o.append(f'<text x="30" y="{y0}" font-size="14" font-weight="bold">部品の種類（すべて仮）　曲げ・溶接なし：平らな板（寸法切り）＋市販のアングル＋ボルトで組む</text>')
for i, r in enumerate(rows):
    o.append(f'<text x="30" y="{y0+24+i*20}" font-size="12">{e(r[0])}　{e(r[1])}：{e(r[2])}　→　{e(r[3])}</text>')
o.append(f'<text x="30" y="{y0+24+len(rows)*20+12}" font-size="12" fill="#555">組む順（イメージ）：②③と①を④でつなぐ → ⑦を側板に付ける → CSPを前上から入れる → ⑤⑥の爪を付けて閉じる → ⑧⑨でリンクのCにつなぐ</text>')
H = y0 + 24 + len(rows)*20 + 40
svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1300 {H}" width="1300" height="{H}" font-family="Noto Sans CJK JP, sans-serif">', f'<rect width="1300" height="{H}" fill="#fff"/>',
 '<text x="20" y="30" font-size="18" font-weight="bold">K121　保持具（案3：K120）の分解のイメージ</text>',
 f'<text x="20" y="50" font-size="11" fill="#555">作成 {TS}　部屋もCSPも描かない見取り図（F7 d）。CSPの傾き24°を戻した向きで表示（x：左右、奥行：背面→前面、高さ：底→上）。寸法・断面・ボルトはすべて仮。単位cm</text>',
 '<text x="20" y="68" font-size="11" fill="#555">色：灰＝寸法切りの板、青＝市販アングル、橙＝つなぎ・コの字（厚板）、赤＝後ろの折り返し、黒＝ゴム板</text>'] + o + ['</svg>']
open(f'/mnt/user-data/outputs/{TS}_K121_保持具の分解のイメージ.svg','w',encoding='utf-8').write('\n'.join(svg))
print(TS, CLu, CLw, CRu, CRw)
