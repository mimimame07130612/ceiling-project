#!/usr/bin/env python3
# heya.py — 部屋コマンド（出力ルール O7-7）
# 部屋を描く部品JSONを出力する。図枠は zuwaku.py が付ける。
# 使い方: python3 heya.py dh|xh|xd -o 出力.json
# 寸法の正は DB/与件/部屋.xlsx（Sheet1）。以下は同シートの値の転記で、行番号を併記する。
# SC・PJは確定事項ファイルの前提条件（仮設定）と 与件/機器一覧.csv による。
import argparse, json

# ---- 部屋.xlsx Sheet1 の転記 ----
X_AREA_L   = 45.5    # 左右方向1 あらわし梁領域の左端
X_AREA_R   = 305.5   # 左右方向2 あらわし梁領域の右端
X_B1_OFS   = 33.5    # 左右方向3 梁領域の左端から1本目梁左端
B_PITCH    = 91      # 左右方向4 梁設置ピッチ
B_W        = 10.5    # 左右方向5 梁の横幅
X_FWALL_R  = 273     # 左右方向7 設置エリア前面壁右端
D_AREA_F   = 45.5    # 前後方向1 あらわし梁領域の前端
D_AREA_B   = 302.5   # 前後方向2 あらわし梁領域の後端
D_RWALL    = 348     # 前後方向3 設置エリア後面壁奥行寸法
H_CEIL     = 250     # 高さ方向1 天井高さ
H_AREA     = 270     # 高さ方向2 あらわし梁領域の高さ
B_H        = 15.5    # 高さ方向4 あらわし梁の高さ
LED_DIA    = 11.4    # 照明1 直径
LED_X      = [129.65, 220.65]              # 照明2,3 左右方向 列1・列2
LED_D_OFS  = [84.5, 129.5, 174.5]          # 照明4,6,7 梁エリア前端からの距離
LP_X       = [132.5, 205.5]; LP_D = 270; LP_H = 100   # 視聴位置
C1 = dict(x=(10, 254), d=14, h=(2, 227))              # カーテン1
C2 = dict(x=14, d=(17, 174), h=(2, 227))              # カーテン2
# ---- 機器一覧.csv / 確定事項ファイル ----
SC_W, SC_H = 221.4, 124.5                  # 機器一覧 イメージサイズ
SC_X, SC_D, SC_HC = 146, 25, 98.75         # A00-003（仮設定・h=98.75に改訂承認済）
PJ_X, PJ_D, PJ_H = 146, 305, 217           # A00-004（仮設定）
# ---- 参考資料/スクリーン/…/479_EP-100HM-MRW1-WF204_draw.pdf（製品寸法図, mm→cm）----
CASE_L, CASE_H, CASE_D = 256.1, 13.5, 13.4 # ケース全長・高さ・奥行
UP_MASK = 75.5                             # 上マスク（ケース下面→イメージ上端）
DROP = 222.3                               # ケース上面→下パイプ下端
FAB_W = 238.0                              # 幕幅（マスク込み）
FAB_OFS = 4.5                              # ケース背面→幕面
# ケース上面の高さは仮定（天井付け h=250）。A00-003 とは別に図面から逆算する
CASE_TOP = H_CEIL
LP_XC = 169                                # D01-001

# ---- 派生値 ----
B_L = [X_AREA_L + X_B1_OFS + i * B_PITCH for i in range(3)]   # 梁左端 79, 170, 261
H_BLOW = H_AREA - B_H                                          # 梁下面 254.5
LED_D = [D_AREA_F + o for o in LED_D_OFS]                      # 130, 175, 220
SC_X0, SC_X1 = SC_X - SC_W / 2, SC_X + SC_W / 2
SC_H0, SC_H1 = SC_HC - SC_H / 2, SC_HC + SC_H / 2
CASE_BOT = CASE_TOP - CASE_H; CASE_B = SC_D - FAB_OFS; CASE_F = CASE_B + CASE_D
CASE_X0, CASE_X1 = SC_X - CASE_L / 2, SC_X + CASE_L / 2
FAB_X0, FAB_X1 = SC_X - FAB_W / 2, SC_X + FAB_W / 2; FAB_BOT = CASE_TOP - DROP

K = '#444444'; GRAY = '#9a9890'; AMB = '#BA7517'; CUR = '#5B8DB8'; LPC = '#7F77DD'; PJC = '#D85A30'
it = []
def add(**k): it.append(k)
def T(p, s, **k): add(t='text', p=p, s=s, **k)

ap = argparse.ArgumentParser(); ap.add_argument('view', choices=['dh', 'xh', 'xd']); ap.add_argument('-o', required=True)
ap.add_argument('--omit', nargs='*', default=[], help='省く部品: curtain, sc(ケース・幕)')
A = ap.parse_args(); v = A.view

if v == 'dh':
    add(t='line', p=[[0, 0], [D_RWALL, 0]], color=K)
    add(t='line', p=[[0, 0], [0, H_CEIL], [D_AREA_F, H_CEIL], [D_AREA_F, H_AREA], [D_AREA_B, H_AREA],
                     [D_AREA_B, H_CEIL], [D_RWALL, H_CEIL], [D_RWALL, 0]], color=K)
    add(t='rect', p=[D_AREA_F, H_BLOW, D_AREA_B, H_AREA], color=GRAY, fill=GRAY, op=0.3, w=0.5)
    for d in LED_D:
        add(t='rect', p=[d - LED_DIA / 2, H_AREA - 1.5, d + LED_DIA / 2, H_AREA], color=AMB, fill=AMB, op=1)
    add(t='line', p=[[C1['d'], C1['h'][0]], [C1['d'], C1['h'][1]]], color=CUR, tag='curtain')
    add(t='rect', p=[C2['d'][0], C2['h'][0], C2['d'][1], C2['h'][1]], color=CUR, w=0.6, tag='curtain')
    add(t='rect', p=[CASE_B, CASE_BOT, CASE_F, CASE_TOP], cls='kari', color='#111111', fill='#dddddd', op=0.6, tag='sc')
    add(t='line', p=[[SC_D, CASE_BOT], [SC_D, FAB_BOT]], cls='kari', color='#111111', w=0.6, tag='sc')
    add(t='line', p=[[SC_D, SC_H0], [SC_D, SC_H1]], cls='kari', color='#111111', w=3)
    add(t='pt', p=[LP_D, LP_H], color=LPC, r=3.5)
    add(t='pt', p=[PJ_D, PJ_H], color=PJC, r=3.5)
    T([0, H_CEIL], 'h=250', dx=4, dy=-5)
    T([D_AREA_B, H_AREA], '梁領域 h=270', anchor='end', dy=-5)
    T([D_AREA_B, H_BLOW], '梁下面 h=254.5', anchor='end', dx=-4, dy=-5)
    T([SC_D, 110], '(SC映像面 上端%g)' % SC_H1, dx=6)
    T([LP_D, LP_H], 'LP目 h=100', dx=8, dy=4)
    T([PJ_D, PJ_H], 'PJレンズ(d=305 h=217)', anchor='end', dx=-8, dy=-8)
    T([D_AREA_F, 0], '45.5', anchor='middle', dy=14)
    T([D_AREA_B, 0], '302.5', anchor='middle', dy=14)
elif v == 'xh':
    XR = X_AREA_R + 20
    add(t='line', p=[[0, 0], [XR, 0]], color=K)
    add(t='line', p=[[0, 0], [0, H_CEIL], [X_AREA_L, H_CEIL], [X_AREA_L, H_AREA], [X_AREA_R, H_AREA],
                     [X_AREA_R, H_CEIL], [XR, H_CEIL]], color=K)
    for b in B_L:
        add(t='rect', p=[b, H_BLOW, b + B_W, H_AREA], color=GRAY, fill=GRAY, op=0.5, w=0.5)
    for x in LED_X:
        add(t='rect', p=[x - LED_DIA / 2, H_AREA - 1.5, x + LED_DIA / 2, H_AREA], color=AMB, fill=AMB, op=1)
    add(t='rect', p=[C1['x'][0], C1['h'][0], C1['x'][1], C1['h'][1]], color=CUR, w=0.6, tag='curtain')
    add(t='line', p=[[C2['x'], C2['h'][0]], [C2['x'], C2['h'][1]]], color=CUR, tag='curtain')
    add(t='rect', p=[CASE_X0, CASE_BOT, CASE_X1, CASE_TOP], cls='kari', color='#111111', fill='#dddddd', op=0.6, tag='sc')
    add(t='rect', p=[FAB_X0, FAB_BOT, FAB_X1, CASE_BOT], cls='kari', color='#111111', w=0.6, tag='sc')
    add(t='rect', p=[SC_X0, SC_H0, SC_X1, SC_H1], cls='kari', color='#111111', w=1.5)
    T([CASE_X1, CASE_BOT], '(SCケース 天井付け仮定)', anchor='end', dy=14)
    for x in LP_X: add(t='pt', p=[x, LP_H], color=LPC, r=3)
    add(t='line', p=[[LP_XC, LP_H - 6], [LP_XC, LP_H + 6]], color=LPC)
    add(t='pt', p=[PJ_X, PJ_H], color=PJC, r=3.5)
    T([XR, H_CEIL], '右側 壁なし', anchor='end', dy=-6)
    for i, b in enumerate(B_L):
        T([b + B_W / 2, H_AREA], '梁%d' % (i + 1), anchor='middle', dy=-6)
    T([SC_X, SC_H1], '(SC映像面)', anchor='middle', dy=16)
    T([LP_XC, LP_H], 'LP中心 x=169', anchor='middle', dy=22)
    T([PJ_X, PJ_H], '(PJレンズ h=217)', dx=8, dy=4)
    T([0, H_CEIL], 'h=250', dx=4, dy=-5)
else:
    XR = X_AREA_R + 20
    add(t='line', p=[[0, D_RWALL], [0, 0], [X_FWALL_R, 0]], color=K)
    add(t='line', p=[[0, D_RWALL], [XR, D_RWALL]], color=K)
    add(t='rect', p=[X_AREA_L, D_AREA_F, X_AREA_R, D_AREA_B], color=K, w=0.6)
    for b in B_L:
        add(t='rect', p=[b, D_AREA_F, b + B_W, D_AREA_B], color=GRAY, fill=GRAY, op=0.5, w=0.5)
    for x in LED_X:
        for d in LED_D:
            add(t='circle', p=[x, d], r=LED_DIA / 2, color=AMB, fill=AMB, op=0.6)
    add(t='line', p=[[C1['x'][0], C1['d']], [C1['x'][1], C1['d']]], color=CUR, tag='curtain')
    add(t='line', p=[[C2['x'], C2['d'][0]], [C2['x'], C2['d'][1]]], color=CUR, tag='curtain')
    add(t='rect', p=[CASE_X0, CASE_B, CASE_X1, CASE_F], cls='kari', color='#111111', fill='#dddddd', op=0.6, tag='sc')
    add(t='line', p=[[SC_X0, SC_D], [SC_X1, SC_D]], cls='kari', color='#111111', w=3)
    for x in LP_X: add(t='pt', p=[x, LP_D], color=LPC, r=3)
    add(t='line', p=[[LP_XC, LP_D - 6], [LP_XC, LP_D + 6]], color=LPC)
    add(t='pt', p=[PJ_X, PJ_D], color=PJC, r=3.5)
    T([X_FWALL_R, 0], '前面壁右端 x=273', anchor='end', dy=-6)
    T([XR, D_RWALL], '右側 壁なし（隣接空間へ開放）', anchor='end', dy=-6)
    for i, b in enumerate(B_L):
        T([b + B_W / 2, D_AREA_F], '梁%d' % (i + 1), anchor='middle', dy=-6)
    T([SC_X, SC_D], '(SC映像面)', anchor='middle', dy=16)
    T([LP_XC, LP_D], 'LP中心 x=169', anchor='middle', dy=20)
    T([PJ_X, PJ_D], '(PJレンズ)', dx=8, dy=4)

legend = [dict(text='黒：部屋（壁・床・天井）', color=K), dict(text='灰：梁', color=GRAY),
          dict(text='黄：照明', color=AMB),
          dict(text='紫：LP', color=LPC), dict(text='朱：PJ', color=PJC)]
src = ['部屋.xlsx', '機器一覧.csv', 'スクリーン製品寸法図', 'A00-003', 'A00-004', 'D01-001']
if 'curtain' not in A.omit: legend.insert(3, dict(text='青：カーテン', color=CUR))
it = [i for i in it if i.pop('tag', None) not in A.omit]
json.dump(dict(items=it, legend=legend, src=src), open(A.o, 'w', encoding='utf-8'), ensure_ascii=False)
print('wrote', A.o, len(it), 'items')
