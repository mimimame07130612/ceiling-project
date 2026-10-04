#!/usr/bin/env python3
# K103 d_max=165に収めるための逆算（部屋を含まない図：F7 d）
# 入力：K101（2610040124版）の内訳、A06-001（O h=265、C 収納h=252.885・使用h=180.725、使用φ=57.4°）、A03-006（ストローク72.16）
# 目標：d_max=165（依頼主の目安。梁エリア前端45.5から約120）。機構のdが最大になるのは収納時（Bが最も遠い）。
import math, subprocess, html
TS = subprocess.run(['date','+%y%m%d%H%M'],capture_output=True,text=True,env={'TZ':'Asia/Tokyo'}).stdout.strip()
e = html.escape
OL, DD, BLK, DRV, TGT = 52.0, 18.0, 3.7, 19.3, 165.0
Oh, Cs, Cu = 265.0, 252.885, 180.725
drop_s, drop_u = Oh-Cs, Oh-Cu            # 12.115, 84.275
def BO(phiu):                            # O→B収納 の水平距離（CSPの収納・使用の高さとOの高さは今のまま）
    L = drop_u/math.sin(math.radians(phiu)); return math.sqrt(L*L-drop_s*drop_s), L
base, _ = BO(57.4)
rows = []   # (名前, 左端, 右端, 説明)
def ends(phiu=57.4, dd=DD, drv=DRV):
    b = 99.25 + (BO(phiu)[0]-base)   # K101・A06-001の値（99.25）に差分を足す（幾何の丸めで0.05ずれるため）
    return OL+b+BLK+drv, OL+dd+b+BLK+drv
rows.append(('現状（K100）', *ends(), 'K101'))
rows.append(('①駆動の列をBより奥に出さない', *ends(drv=0), 'モーター・ねじの支持をBより奥（LP側）に置かない配置。−19.3'))
rows.append(('②左右のずらしΔdをなくす', *ends(dd=0), '姿勢保持を配置β（Δd=18）以外で行う。右だけ−18'))
for p in (70, 75, 80):
    rows.append((f'③使用時のφを{p}°にする', *ends(phiu=p), f'リンク長2a={BO(p)[1]:.1f}。O→B収納 −{base-BO(p)[0]:.1f}'))
rows.append(('①＋②', *ends(dd=0, drv=0), ''))
rows.append(('①＋③75°', *ends(phiu=75, drv=0), ''))
rows.append(('②＋③80°', *ends(phiu=80, dd=0), ''))
W, H = 1200, 160+len(rows)*44+300
X0, D0, S = 330, 140.0, 13.0
def X(d): return X0+(d-D0)*S
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="Noto Sans CJK JP, sans-serif">',
     f'<rect width="{W}" height="{H}" fill="#fff"/>',
     '<text x="20" y="30" font-size="18" font-weight="bold">K103　d_max=165 に収めるための逆算（収納時の機構の端）</text>',
     f'<text x="20" y="50" font-size="11" fill="#555">作成 {TS}　部屋を含まない図（F7 d）。CSPの収納・使用の位置とOの高さ（h=265）は今のまま。単位cm。目標165は依頼主の目安</text>',
     '<text x="20" y="68" font-size="11" fill="#555">このスコットラッセルではBが最も奥へ出るのは収納時。動作中・使用時の端は収納時より手前</text>']
y0 = 110
for d in range(140, 201, 5):
    o.append(f'<line x1="{X(d)}" y1="{y0-14}" x2="{X(d)}" y2="{y0+len(rows)*44}" stroke="#eee"/>')
    o.append(f'<text x="{X(d)}" y="{y0-18}" font-size="10" text-anchor="middle">{d}</text>')
o.append(f'<line x1="{X(TGT)}" y1="{y0-14}" x2="{X(TGT)}" y2="{y0+len(rows)*44}" stroke="#c0392b" stroke-width="2"/>')
o.append(f'<text x="{X(TGT)+4}" y="{y0-30}" font-size="12" fill="#c0392b">目標 d=165</text>')
for i,(nm,l,r,note) in enumerate(rows):
    y = y0+i*44
    if i in (1,6): o.append(f'<line x1="20" y1="{y-8}" x2="{W-20}" y2="{y-8}" stroke="#bbb"/>')
    o.append(f'<text x="20" y="{y+12}" font-size="12" font-weight="bold">{e(nm)}</text>')
    o.append(f'<text x="20" y="{y+27}" font-size="10" fill="#555">{e(note)}</text>')
    for k,(v,c) in enumerate(((l,'#2E9E6B'),(r,'#2C6FB0'))):
        yy = y+4+k*14
        ok = v <= TGT
        o.append(f'<line x1="{X(140)}" y1="{yy}" x2="{X(v)}" y2="{yy}" stroke="{c}" stroke-width="8" opacity="0.7"/>')
        o.append(f'<text x="{X(v)+6}" y="{yy+4}" font-size="11" fill="{"#000" if ok else "#c0392b"}">{"左" if k==0 else "右"} {v:.2f}{"" if ok else f"（+{v-TGT:.2f}）"}</text>')
# φ使用 と O→B収納 の関係
yg = y0+len(rows)*44+40
o.append(f'<text x="20" y="{yg}" font-size="13" font-weight="bold">③の中身：使用時のφと O→B収納の距離（CSPの位置・Oの高さ固定）</text>')
gx0, gy0, gw, gh = 80, yg+30, 520, 180
ph0, ph1, v0, v1 = 55, 90, 80, 102
def gx(p): return gx0+(p-ph0)/(ph1-ph0)*gw
def gy(v): return gy0+gh-(v-v0)/(v1-v0)*gh
o.append(f'<rect x="{gx0}" y="{gy0}" width="{gw}" height="{gh}" fill="none" stroke="#333"/>')
for p in range(55, 91, 5): o.append(f'<text x="{gx(p)}" y="{gy0+gh+15}" font-size="10" text-anchor="middle">{p}°</text>')
for v in range(80, 103, 5): o.append(f'<text x="{gx0-6}" y="{gy(v)+4}" font-size="10" text-anchor="end">{v}</text>')
pts = ' '.join(f'{gx(p):.1f},{gy(BO(p)[0]):.1f}' for p in [55+i*0.5 for i in range(71)])
o.append(f'<polyline points="{pts}" fill="none" stroke="#2E9E6B" stroke-width="2"/>')
for p in (57.4, 70, 75, 80, 90):
    v = BO(p)[0]; o.append(f'<circle cx="{gx(p):.1f}" cy="{gy(v):.1f}" r="3" fill="#2E9E6B"/>')
    o.append(f'<text x="{gx(p)+5:.1f}" y="{gy(v)-6:.1f}" font-size="10">{v:.1f}</text>')
o.append(f'<text x="{gx0+gw/2}" y="{gy0+gh+32}" font-size="11" text-anchor="middle">使用時のφ（現状57.4°）</text>')
nt = ['O→B収納 ＝ √(L²−12.115²)、L＝2a＝84.275÷sinφ使用',
      '（12.115＝Oと収納時のCの高さの差、84.275＝Oと使用時のCの高さの差）',
      'φ使用を大きくする（使用時にリンクを立てる）ほど短くなるが、90°でも83.4（−15.9）が限り',
      'φ使用を大きくしたときの力・干渉（使用時にBがOに近づく）は未確認',
      '②の「配置β以外の姿勢保持」の具体の形は未検討（D06-003〜D06-005は却下済み）',
      '①の「Bより奥に出さない駆動」の具体の形は未検討']
for i,s in enumerate(nt): o.append(f'<text x="640" y="{gy0+14+i*20}" font-size="11">{e(s)}</text>')
o.append('</svg>')
open(f'/mnt/user-data/outputs/{TS}_K103_dmax165への逆算.svg','w',encoding='utf-8').write('\n'.join(o))
print(TS); [print(r) for r in rows]
