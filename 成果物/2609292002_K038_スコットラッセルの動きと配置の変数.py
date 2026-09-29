# K038 スコットラッセルの動きと配置の変数（STEP4 4-1）
# 側面図（d-h）に、STEP2のCSP収納・使用位置、必要な一直線の経路、スコットラッセル機構の例（a=45）、
# リンクを置く面（x=110.9、左リンクの内側）での照明配光118°の断面を重ねる。
# 入力：A03-004・A03-005・A03-006（wR=0で作図）、A01-001、A02-002、D00-005・A00-006・A02-001（配光）、D01-009、D04-002
# 例の条件（検討用の仮の値で、決定ではない）：取付点C＝CSP側面の断面の中心、固定の回転中心O h=268、a=OA=AB=AC=45
# 使い方：python3 本ファイル（同じフォルダに YYMMDDhhmm_csp.py・YYMMDDhhmm_sanmen.py の最新版を置く）
import json, math, subprocess, glob, sys
TS = subprocess.run(['date', '+%y%m%d%H%M'], capture_output=True, text=True, env={'TZ': 'Asia/Tokyo'}).stdout.strip()  # 作図時 2609292002
NAME = 'K038_スコットラッセルの動きと配置の変数'
CSP = sorted(glob.glob('*_csp.py'))[-1]; SAN = sorted(glob.glob('*_sanmen.py'))[-1]
OUTJ = '/mnt/user-data/outputs/%s_%s.json' % (TS, NAME); OUTS = '/mnt/user-data/outputs/%s_%s.svg' % (TS, NAME)

# ---- CSP（csp.py） ----
subprocess.run(['python3', CSP, 'json', '-o', 'csp_k038.json', '--pose', '収納,139.45,48.5,243.77',
                '--pose', '使用,139.45,33,168.51'], check=True, capture_output=True)
C = json.load(open('csp_k038.json', encoding='utf-8'))
# 側面の断面の中心（4隅の平均）
side = [it['p'] for it in C['items'] if it['t'] == 'poly']
cs = [sum(p[0] for p in side[0]) / 4, sum(p[1] for p in side[0]) / 4]
cu = [sum(p[0] for p in side[1]) / 4, sum(p[1] for p in side[1]) / 4]
L = math.hypot(cu[0] - cs[0], cu[1] - cs[1])                      # 76.84（A03-006）
uc = ((cu[0] - cs[0]) / L, (cu[1] - cs[1]) / L)                   # 経路の向き（下・SC側）
us = (-uc[1], uc[0]) if -uc[1] > 0 else (uc[1], -uc[0])           # スライダの向き（経路に直角、LP側）
ang_path = math.degrees(math.atan2(-uc[1], -uc[0]))               # 経路の水平からの角
ang_rail = math.degrees(math.atan2(-us[1], us[0]))                # スライダの下り角

# ---- 例：O h=268、a=45 ----
HO, a = 268.0, 45.0
t0 = (HO - cs[1]) / (-uc[1]); O = (cs[0] - uc[0] * t0, HO)
def pose(dist):             # OC=dist のときの A,B,C（C=O+dist·uc、B=O+2a cosφ·us）
    phi = math.asin(dist / (2 * a))
    Cp = (O[0] + uc[0] * dist, O[1] + uc[1] * dist)
    Bp = (O[0] + us[0] * 2 * a * math.cos(phi), O[1] + us[1] * 2 * a * math.cos(phi))
    Ap = ((Bp[0] + Cp[0]) / 2, (Bp[1] + Cp[1]) / 2)
    return phi, Ap, Bp, Cp
P1 = pose(t0); P2 = pose(t0 + L)
amin = (t0 + L) / 2
r2 = lambda p: [round(p[0], 2), round(p[1], 2)]

# ---- 配光118°の断面（左リンク内側の面 x=110.9） ----
XL, LX, LD, R0, TN = 110.9, 129.65, [130, 175, 220], 5.7, math.tan(math.radians(59))
dx = LX - XL
hs = [270 - k * 0.5 for k in range(0, 61)]
items = list(C['items'])
for dL in LD:
    pts_r, pts_l = [], []
    for h in hs:
        r = R0 + (270 - h) * TN
        if r > dx:
            w = math.sqrt(r * r - dx * dx); pts_r.append([round(dL + w, 2), h]); pts_l.append([round(dL - w, 2), h])
    items.append(dict(t='poly', view='side', p=pts_l + pts_r[::-1], color='#BA7517', fill='#BA7517', op=0.18, w=1.0))
h_top = 270 - (dx - R0) / TN
# ---- 正面図の配光118°（照明のx位置 129.65・220.65、h=270→240。K005と同じ描き方） ----
FB, FT = 240.0, 270.0
for xL in (LX, 220.65):
    wt = R0; wb = R0 + (FT - FB) * TN
    items.append(dict(t='poly', view='front',
                      p=[[round(xL - wt, 2), FT], [round(xL + wt, 2), FT],
                         [round(xL + wb, 2), FB], [round(xL - wb, 2), FB]],
                      color='#BA7517', fill='#BA7517', op=0.15, w=1.0))
# ---- 経路・スライダ・リンク ----
ext = [r2((O[0] - uc[0] * 3, O[1] - uc[1] * 3)), r2((cu[0] + uc[0] * 8, cu[1] + uc[1] * 8))]
items.append(dict(t='line', view='side', p=ext, color='#555555', w=1.0, dash=True))
items.append(dict(t='line', view='side', p=[r2(O), r2(P1[2])], color='#6A5FD0', w=2.4, dash=True))   # スライダの通り道 O〜B（収納）
LB = {  # ラベル位置（収納：A,B,C／使用：A,B,C）
    ('収', 'A'): (0, -8, 'middle'), ('収', 'B'): (6, 16, 'start'), ('収', 'C'): (-6, -6, 'end'),
    ('使', 'A'): (-8, 0, 'end'),    ('使', 'B'): (7, 16, 'start'), ('使', 'C'): (8, 14, 'start')}
for (phi, Ap, Bp, Cp), col, tag in ((P1, '#2C6FB0', '収'), (P2, '#C0392B', '使')):
    items.append(dict(t='line', view='side', p=[r2(O), r2(Ap)], color=col, w=2.2, dash=True))   # リンクOA
    items.append(dict(t='line', view='side', p=[r2(Bp), r2(Cp)], color=col, w=2.2, dash=True))  # ロッドBC（A中点）
    for q, nm in ((Ap, 'A'), (Bp, 'B'), (Cp, 'C')):
        items.append(dict(t='pt', view='side', p=r2(q), color=col, r=3.2))
        dx, dy, an = LB[(tag, nm)]
        items.append(dict(t='text', view='side', p=r2(q), s='%s(%s)' % (nm, tag), dx=dx, dy=dy, anchor=an, color=col))
items.append(dict(t='pt', view='side', p=r2(O), color='#111111', r=4.5, ring=True))
items.append(dict(t='text', view='side', p=r2(O), s='O(固定 h=268)', dx=8, dy=-8, color='#111111'))
notes = [
 'STEP4 4-1：スコットラッセル機構（OA=AB=AC=a、Bが直線上をすべるとCはBの直線に直角な直線上を動く）をSTEP2の配置にあてはめた例。例の値は決定ではない。',
 '必要な経路：水平から%.2f°（SC側へ前15.5・下75.26、距離%.2f。A03-006）→ Bのすべる直線は経路に直角で、LP側へ%.2f°下がる。' % (ang_path, L, ang_rail),
 '例（取付点C＝CSP側面の断面の中心、O h=268、a=45）：OC 収納%.2f→使用%.2f、φ %.1f°→%.1f°。Bの収納位置 d=%.1f h=%.1f（Oからの距離%.1f）。この条件で a≧%.2f。' % (
     t0, t0 + L, math.degrees(P1[0]), math.degrees(P2[0]), P1[2][0], P1[2][1], 2 * a * math.cos(P1[0]), amin),
 '黄（側面図）：左リンク内側の面 x=110.9 での配光118°の断面。この面では h≦%.1f で配光に入る（照明3灯 d=130・175・220）。黄（正面図）：配光118°をx方向に広げた線（照明x=129.65・220.65、K005と同じ）。' % h_top,
 '配光の見方：正面図＝配光がx方向に広がる範囲、側面図＝配光がd方向に広がる範囲。両方に重なって初めて実際に配光の中に入る。収納時は機器・CSPが配光に入らないこと（A00-006、交渉可）。',
 '例のB（収納 x=110.9・d=151.5・h=250）は、正面図でも側面図でも黄に重なる＝配光の中。実際にO・照明x=129.65/d=175からの距離で確かめても、h=250での円錐半径39.0に対し距離30.1で中に入る。',
 'Cの点は一直線に動くが、ロッドBCはφの分だけ回る（例では約%.0f°）。CSPの姿勢をどう保つかは別に決める必要がある。' % (math.degrees(P2[0] - P1[0])),
]
ov = dict(title_note=notes, legend=C['legend'] + [
    dict(text='灰 破線：取付点Cの一直線の経路（延長を含む）', color='#555555', dash=True, kind='line'),
    dict(text='紫 太破線：Bのすべる直線（O〜収納時のB）', color='#6A5FD0', dash=True, kind='line'),
    dict(text='青／赤 破線：リンクOA・BC（収納／使用、例 a=45）', color='#2C6FB0', dash=True, kind='line'),
    dict(text='黄 帯：配光118°の断面（x=110.9の面、側面図）', color='#BA7517', kind='band')],
    src=C['src'] + ['A03-004〜006', 'D00-005', 'A00-006', 'A02-001'], items=items)
json.dump(ov, open(OUTJ, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
subprocess.run(['python3', SAN, '--zuban', 'K038', '--title', 'スコットラッセルの動きと配置の変数', '-o', OUTS, OUTJ], check=True)
print('\n'.join(notes)); print('O', r2(O), 'A1', r2(P1[1]), 'B1', r2(P1[2]), 'A2', r2(P2[1]), 'B2', r2(P2[2]), 'C2', r2(P2[3]))
for aa in (45, 50, 60, 70):
    ph1 = math.asin(t0 / (2 * aa)); ph2 = math.asin((t0 + L) / (2 * aa)); b = 2 * aa * math.cos(ph1)
    print('a=%d φ%.1f→%.1f B収納 d=%.1f h=%.1f' % (aa, math.degrees(ph1), math.degrees(ph2), O[0] + us[0] * b, O[1] + us[1] * b))
