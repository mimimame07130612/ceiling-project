# K031 動作速度の範囲（STEP3 3-3）
# 片道時間と平均速度の関係、速度ごとの運動エネルギー・すき間が閉じるまでの時間・停止までに進む距離を示す。
# 入力：S3 e（60秒以内）、A03-006（鉛直75.26・前後15.5）、A01-001（7.90kg）、A04-001（猫5kg、起票予定）、A03-003（すき間2）
# 参考：市販プロジェクター昇降装置 EE-401H の昇降速度 20mm/s（value-press.com 2006年発表資料）
#       ISO 13854（旧EN 349）押しつぶし防止の最小すき間：指25mm、手100mm、胴500mm（BG ETEM資料ほか）
# 使い方：python3 本ファイル <出力svgパス> <タイムスタンプ>
import sys, html, math
TS = sys.argv[2]
L = math.hypot(75.26, 15.5); M = 7.90 + 5.0
e = html.escape; out = []
K, RED, GRN, GRY, BLU, ORG, PUR = '#333333', '#C0392B', '#2E9E6B', '#8a857a', '#2C6FB0', '#D35400', '#6A5FD0'
def f(n, d=2): return ('%.*f' % (d, n)).rstrip('0').rstrip('.')
def txt(x, y, t, col='#222', anchor='start', size=13, bold=False):
    out.append('<text x="%s" y="%s" fill="%s" text-anchor="%s" font-size="%s"%s>%s</text>' % (f(x), f(y), col, anchor, size, ' font-weight="bold"' if bold else '', e(t)))
def line(x1, y1, x2, y2, col=K, w=1.2, dash=None):
    out.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s"%s/>' % (f(x1), f(y1), f(x2), f(y2), col, w, ' stroke-dasharray="%s"' % dash if dash else ''))
txt(40, 40, 'K031　動作速度の範囲（STEP3 3-3）', size=18, bold=True)
txt(40, 62, '作成 %s　一直線の移動距離 %s cm（A03-006）。等速で動くと仮定（加減速は含まない）。荷重はCSP 7.90kg＋猫5kg＝%s kg' % (TS, f(L), f(M)), size=12)
# グラフ
X0, Y0, GW, GH = 110, 110, 620, 380
vmin, vmax, tmax = 0, 8, 80
def X(v): return X0 + (v - vmin) / (vmax - vmin) * GW
def Y(t): return Y0 + GH - t / tmax * GH
out.append('<rect x="%s" y="%s" width="%s" height="%s" fill="%s" fill-opacity="0.12"/>' % (X(0), Y0, X(L / 60) - X(0), GH, RED))
txt(X(0.64), Y(74), 'S3 e 不可', col=RED, anchor='middle', size=12, bold=True)
txt(X(0.64), Y(70), '（60秒超）', col=RED, anchor='middle', size=11)
line(X0, Y0 + GH, X0 + GW, Y0 + GH); line(X0, Y0, X0, Y0 + GH)
for v in range(0, 9):
    line(X(v), Y0 + GH, X(v), Y0 + GH + 5); txt(X(v), Y0 + GH + 20, str(v), anchor='middle', size=12)
    if v: line(X(v), Y0, X(v), Y0 + GH, col='#e5e5e5', w=1)
for t in range(0, 81, 10):
    line(X0 - 5, Y(t), X0, Y(t)); txt(X0 - 9, Y(t) + 4, str(t), anchor='end', size=12)
    if t: line(X0, Y(t), X0 + GW, Y(t), col='#e5e5e5', w=1)
txt(X0 + GW / 2, Y0 + GH + 42, '平均速度（cm/s）', anchor='middle', size=13)
txt(X0 - 30, Y0 - 12, '片道時間（秒）', size=13)
line(X0, Y(60), X0 + GW, Y(60), col=RED, dash='6 3'); txt(X0 + GW - 4, Y(60) - 6, '60秒（S3 e）', col=RED, anchor='end', size=12)
pts = ' '.join('%s,%s' % (f(X(v)), f(Y(L / v))) for v in [0.97 + i * 0.02 for i in range(0, 352)] if L / v <= tmax)
out.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="2.5"/>' % (pts, BLU))
for v, lab, col in [(L / 60, '下限 %s cm/s（60秒）' % f(L / 60), RED), (2.0, '市販PJ昇降装置 EE-401H 2.0 cm/s（%s秒）' % f(L / 2.0, 1), GRN)]:
    out.append('<circle cx="%s" cy="%s" r="5" fill="%s"/>' % (f(X(v)), f(Y(L / v)), col))
    txt(X(v) + 10, Y(L / v) + (-8 if col == RED else 18), lab, col=col, size=12, bold=True)
# 表
NX, NY = 790, 110
txt(NX, NY, '■ 速度ごとの目安', bold=True, size=14)
cols = [NX, NX + 80, NX + 160, NX + 270, NX + 400]
for c_, h_ in zip(cols, ['速度', '片道時間', '運動エネルギー', 'すき間10→2cm', '0.5秒で進む距離']): txt(c_, NY + 28, h_, size=12, bold=True)
txt(cols[2], NY + 44, '（%s kg）' % f(M), size=10, col=GRY); txt(cols[3], NY + 44, 'が閉じるまで', size=10, col=GRY); txt(cols[4], NY + 44, '（反応時間の例）', size=10, col=GRY)
for i, v in enumerate([L / 60, 2.0, 3.0, 5.0, 8.0]):
    y = NY + 68 + i * 24
    E = 0.5 * M * (v / 100) ** 2
    for c_, s_ in zip(cols, [f(v) + ' cm/s', f(L / v, 1) + ' 秒', '%.4f J' % E, f(8 / v, 1) + ' 秒', f(v * 0.5, 2) + ' cm']): txt(c_, y, s_, size=12, col=RED if i == 0 else '#222')
yy = NY + 68 + 5 * 24 + 14
N = [
 '・運動エネルギーはどの速度でもごく小さい（参考：1kgを1cm落とすと約0.1J）。',
 '　ぶつかったときの危険は、勢いより「止まらずに押し続ける力」で決まる → 3-4（過負荷で停止）',
 '・すき間が閉じるまでの時間と、止まるまでに進む距離は速度に比例する。',
 '　遅いほど猫や手が逃げる時間があり、検出してから止まるまでの行き過ぎも小さい',
 '・反応時間0.5秒は例示。実際の値は制御と駆動で決まる（STEP4・STEP5）',
 '',
 '■ 気づいたこと（3-4・STEP4へ）',
 '・収納時のすき間は2cm（A03-003）。押しつぶしを防ぐ最小すき間は',
 '　指25mm・手100mm（ISO 13854）。2cmは指が入って挟まれる大きさ',
 '　→ 速度では解決しない。挟み込み検出／カバー／すき間の見直しのどれかが必要',
]
for i, t_ in enumerate(N): txt(NX, yy + i * 21, t_, size=12, bold=t_.startswith('■'))
Wc, Hc = 1380, 580
svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" font-family="Noto Sans CJK JP, Hiragino Sans, Meiryo, sans-serif">' % (Wc, Hc, Wc, Hc),
       '<rect width="100%" height="100%" fill="white"/>'] + out + ['</svg>']
open(sys.argv[1], 'w', encoding='utf-8').write('\n'.join(svg))
