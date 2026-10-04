#!/usr/bin/env python3
# K101 d寸法の内訳（部屋を含まない図：F7 d）
# 入力：A06-001（O左d=52・右d=70、a=50、収納φ=7.0°、使用φ=57.4°、B 左使用105.83・収納151.25）、A00-002（配置β Δd=18）、
#       A06-007（HSR20C 長さ74）、A06-008（ナットはBからLP側へ3cm、GBK10）、A06-009（PKP268 L=92.5）、A03-004（CSP d1=47.77、外接奥行26.46）、
#       A03-006（ストローク72.16）、K100の機構JSON（2610032002版）の部品座標
import math, subprocess, html
TS = subprocess.run(['date','+%y%m%d%H%M'],capture_output=True,text=True,env={'TZ':'Asia/Tokyo'}).stdout.strip()
e = html.escape
a, ps, pu, OL, DD = 50.0, 7.0, 57.4, 52.0, 18.0
L2 = 2*a*math.cos(math.radians(ps))          # 99.25
BLK = 7.4/2                                   # ブロック半長
# K100機構JSONの左側の座標（ブロック端154.95→GBK10 158.0〜160.5→カップリング161.0〜163.5→取付板164.0〜165.0→モーター165.0〜174.25）
DRV = [('ナットの逃げ',3.05,'#d9c9a6','A06-008：ナットをBからLP側へ3cm'),
       ('GBK10',2.5,'#B07A1F','A06-008'),('すき間',0.5,'#eee',''),
       ('カップリング',2.5,'#c9a05a','A06-008（仮）'),('すき間',0.5,'#eee',''),
       ('取付板',1.0,'#8a6a2a','A06-005'),('モーター',9.25,'#E6A23C','A06-009：PKP268 L=92.5')]
SW = 0.0
W, H = 1180, 640
X0, D0, S = 70, 40.0, 5.6
def X(d): return X0 + (d-D0)*S
o = []
o.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="Noto Sans CJK JP, sans-serif">')
o.append(f'<rect width="{W}" height="{H}" fill="#fff"/>')
o.append(f'<text x="20" y="30" font-size="18" font-weight="bold">K101　d寸法の内訳（収納時、機構のLP側の端まで）</text>')
o.append(f'<text x="20" y="50" font-size="11" fill="#555">作成 {TS}　部屋を含まない図（F7 d）。K100（2610032002版）の配置。破線枠・( )は仮設定を含む値。単位cm</text>')
# 目盛り
ya = 560
o.append(f'<line x1="{X(D0)}" y1="{ya}" x2="{X(200)}" y2="{ya}" stroke="#333"/>')
for d in range(40, 201, 10):
    o.append(f'<line x1="{X(d)}" y1="{ya}" x2="{X(d)}" y2="{ya+6}" stroke="#333"/>')
    o.append(f'<text x="{X(d)}" y="{ya+20}" font-size="11" text-anchor="middle">{d}</text>')
o.append(f'<text x="{X(200)+8}" y="{ya+4}" font-size="12">d</text>')
def seg(d0, d1, y, h, fill, txt=None, dash=True, tc='#000', fs=11):
    o.append(f'<rect x="{X(d0):.1f}" y="{y}" width="{(d1-d0)*S:.1f}" height="{h}" fill="{fill}" stroke="#333" stroke-width="0.8" {"stroke-dasharray=\"4 2\"" if dash else ""}/>')
    if txt: o.append(f'<text x="{(X(d0)+X(d1))/2:.1f}" y="{y+h/2+4}" font-size="{fs}" text-anchor="middle" fill="{tc}">{e(txt)}</text>')
def lab(d, y, s, anchor='middle', c='#222', fs=11):
    o.append(f'<text x="{X(d):.1f}" y="{y}" font-size="{fs}" text-anchor="{anchor}" fill="{c}">{e(s)}</text>')
# CSP行
yc = 95
lab(D0, yc-8, 'CSP（収納時の外接）', 'start', '#444', 12)
seg(47.77, 47.77+26.46, yc, 22, '#d6e6f5', '(47.77〜74.23)')
rows = [('左側', OL, 0.0, 150), ('右側', OL+DD, DD, 300)]
for name, O, dd, y0 in rows:
    lab(D0, y0-30, f'{name}', 'start', '#000', 14)
    d = OL
    seg(D0, OL, y0, 26, '#f3f3f3', None, dash=False)
    lab((D0+OL)/2, y0+17, '(O左 d=52)', fs=10)
    if dd:
        seg(OL, O, y0, 26, '#f4c7c3', '配置β Δd=18'); 
    seg(O, O+L2, y0, 26, '#cfe3cf', f'2a·cosφ収納 = 100×cos7.0° = {L2:.2f}  （O→B収納）')
    b = O+L2
    seg(b, b+BLK, y0, 26, '#2C6FB0', None); 
    d = b+BLK
    for nm, w, c, _ in DRV:
        seg(d, d+w, y0, 26, c, None); d += w
    end = d
    o.append(f'<line x1="{X(end)}" y1="{y0-14}" x2="{X(end)}" y2="{y0+30}" stroke="#c0392b" stroke-dasharray="3 3"/>')
    o.append(f'<line x1="{X(end)}" y1="{ya-10}" x2="{X(end)}" y2="{ya}" stroke="#c0392b" stroke-width="2"/>')
    lab(end, ya-14, f'{end:.2f}', c='#c0392b', fs=10)
    lab(end+0.5, y0-16, f'端 d={end:.2f}', 'start', '#c0392b', 12)
    # 小さい部品の注記
    lab(b+BLK/2, y0+44, 'ブロック半長3.7', fs=10)
    lab(b+BLK+(end-b-BLK)/2, y0+58, f'駆動の列 {end-b-BLK:.2f}（ナット逃げ3.05・GBK10 2.5・カップリング2.5・取付板1.0・モーター9.25・すき間1.0）', fs=10)
    # B の移動範囲（使用〜収納）
    bu = O + (105.83-OL)   # A06-001の値（B使用 左105.83、右は+18）
    yb = y0+86
    o.append(f'<line x1="{X(bu)}" y1="{yb}" x2="{X(b)}" y2="{yb}" stroke="#2C6FB0" stroke-width="2"/>')
    for q in (bu, b): o.append(f'<circle cx="{X(q)}" cy="{yb}" r="3" fill="#2C6FB0"/>')
    lab(bu, yb+15, f'B使用 {bu:.2f}', fs=10); lab(b, yb+15, f'B収納 {b:.2f}', fs=10)
    lab((bu+b)/2, yb-7, f'Bの動く範囲 {b-bu:.2f}', c='#2C6FB0', fs=10)
# 内訳の式
yt = 440
txt = [
 '右側の端 192.25 ＝ O左 52.0（CSPの真上：Cは鉛直に下降）＋ Δd 18（配置β）＋ 2a·cosφ収納 99.25 ＋ ブロック半長 3.7 ＋ 駆動の列 19.3',
 '　・2a·cosφ収納 は内訳の約半分。2a＝ストローク÷(sinφ使用−sinφ収納)＝72.16÷(sin57.4°−sin7.0°)＝100.1。φ収納が小さい（ほぼ水平にたたむ）ほどBは遠くへ出る',
 '　・CSPのLP側の端（74.23）から機構の端まで：左 100.0、右 118.0',
 '　・駆動の列 19.3 はBの延長線上にモーターを一直線に並べた配置（A06-008・A06-009）による',
]
for i, s in enumerate(txt):
    o.append(f'<text x="20" y="{yt+i*22}" font-size="12">{e(s)}</text>')
o.append('</svg>')
open(f'/mnt/user-data/outputs/{TS}_K101_d寸法の内訳.svg','w',encoding='utf-8').write('\n'.join(o))
print(TS)
