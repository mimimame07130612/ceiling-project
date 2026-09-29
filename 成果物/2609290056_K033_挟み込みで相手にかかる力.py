# K033 挟み込み・衝突で相手にかかる力（STEP3 3-4）
# 下降中に下の物に当たる場合と、上昇中に上の物を挟む場合で、相手にかかる力と駆動側の負荷の変わり方を示す。
# 参考値：挟み込み点の静的な力の上限として広く使われる150N（Mewes, Int. J. Occup. Saf. Ergon. の論文要旨）
#         動力ゲート EN 12453:2017 の挟み込みの力の上限400N（calibrate.co.uk）
# 入力：A01-001（7.90kg）、A04-001（猫5kg、起票予定）。保持具・リンクの質量は未定のため含まない。
# 使い方：python3 本ファイル <出力svgパス> <タイムスタンプ>
import sys, html
TS = sys.argv[2]
g = 9.81; Wc = 7.90 * g; Wk = 5.0 * g
e = html.escape; out = []
K, RED, GRN, GRY, BLU, ORG, PUR = '#333333', '#C0392B', '#2E9E6B', '#8a857a', '#2C6FB0', '#D35400', '#6A5FD0'
def f(n, d=1): return ('%.*f' % (d, n)).rstrip('0').rstrip('.')
def txt(x, y, t, col='#222', anchor='start', size=13, bold=False):
    out.append('<text x="%s" y="%s" fill="%s" text-anchor="%s" font-size="%s"%s>%s</text>' % (x, y, col, anchor, size, ' font-weight="bold"' if bold else '', e(t)))
def rect(x, y, w, h, col=K, fill='none', op=1, dash=None):
    out.append('<rect x="%s" y="%s" width="%s" height="%s" fill="%s" fill-opacity="%s" stroke="%s" stroke-width="1.5"%s/>' % (x, y, w, h, fill, op, col, ' stroke-dasharray="%s"' % dash if dash else ''))
def arr(x1, y1, x2, y2, col, w=3):
    out.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s" marker-end="url(#m%s)"/>' % (x1, y1, x2, y2, col, w, col[1:]))
txt(40, 40, 'K033　挟み込み・衝突で相手にかかる力（STEP3 3-4）', size=18, bold=True)
txt(40, 62, '作成 %s　概念図。W＝CSPの重さ %s N（7.90kg）。保持具・リンクの重さは未定のため含まない。F駆動＝駆動がCSPを押す力（向きは図の矢印）' % (TS, f(Wc)), size=12)
# パネル1 下降
txt(60, 100, '① 下降中に、下の物（頭・手）に当たる', size=14, bold=True)
rect(120, 140, 200, 60, fill='#e8e8e8'); txt(220, 175, 'CSP', anchor='middle', bold=True)
arr(220, 200, 220, 250, RED); txt(232, 235, 'W（重さ）', col=RED, size=12)
arr(300, 110, 300, 138, BLU); txt(308, 125, 'F駆動（下向きに押す場合）', col=BLU, size=12)
out.append('<ellipse cx="220" cy="285" rx="45" ry="32" fill="#f6e0c8" stroke="%s"/>' % K); txt(220, 290, '頭・手', anchor='middle')
NOTES1 = [
 '相手にかかる力 ＝ W ＋ 下向きのF駆動',
 '・駆動が押さなくても、重さWは全部相手に乗る',
 '・駆動から見ると、重さを相手が支えるので',
 '　負荷が「減る」 → 検出は負荷の減少（抜け）',
 '・Wは保持具・リンクを含めると%s Nより大きい' % f(Wc),
]
for i, t_ in enumerate(NOTES1): txt(60, 350 + i * 21, t_, size=12, bold=(i == 0))
# パネル2 上昇
txt(560, 100, '② 上昇中に、上の物（猫・手）を天井との間に挟む', size=14, bold=True)
out.append('<line x1="580" y1="130" x2="880" y2="130" stroke="%s" stroke-width="4"/>' % K); txt(890, 135, '掘込面・梁', size=12)
out.append('<ellipse cx="730" cy="160" rx="45" ry="26" fill="#f6e0c8" stroke="%s"/>' % K); txt(730, 165, '猫・手', anchor='middle')
rect(630, 188, 200, 60, fill='#e8e8e8'); txt(730, 223, 'CSP', anchor='middle', bold=True)
arr(810, 300, 810, 250, BLU); txt(820, 285, 'F駆動（上向き）', col=BLU, size=12)
arr(700, 248, 700, 290, RED); txt(640, 280, 'W', col=RED, size=12)
NOTES2 = [
 '相手にかかる力 ＝ F駆動 − W',
 '・駆動は重さを持ち上げたうえで、さらに押す',
 '・駆動から見ると負荷が「増える」 → 検出は負荷の増加（過負荷）',
 '・猫が上に乗ったまま上がる（H13）のはこちら',
]
for i, t_ in enumerate(NOTES2): txt(560, 350 + i * 21, t_, size=12, bold=(i == 0))
# 力の比較
BX, BY = 60, 500
txt(BX, BY, '■ 力の大きさの比較（N）', size=14, bold=True)
items = [('CSPの重さ W', Wc, GRY), ('猫 5kg の重さ', Wk, PUR), ('CSP＋猫', Wc + Wk, GRY), ('挟み込みの静的な力の上限（多くの規格）', 150, GRN), ('動力ゲートの挟み込みの上限（EN 12453）', 400, ORG)]
sc = 1.2
for i, (lab, v, col) in enumerate(items):
    y = BY + 20 + i * 30
    txt(BX + 300, y + 16, lab, anchor='end', size=12)
    out.append('<rect x="%s" y="%s" width="%s" height="20" fill="%s" fill-opacity="0.7"/>' % (BX + 310, y + 2, v * sc, col))
    txt(BX + 316 + v * sc, y + 17, f(v) + ' N', size=12)
yy = BY + 20 + len(items) * 30 + 20
for i, t_ in enumerate([
 '・下降の向き（①）では、CSPの重さそのものが相手にかかる。重さだけなら150Nより小さいが、保持具・リンクの重さと、駆動が下向きに押す力しだいで越える',
 '・検出の向きが上昇と下降で逆（①は負荷の減少、②は負荷の増加）。検出のしかたは両方向で別に考える必要がある',
 '・スコットラッセルでは、CSPにかかる力と駆動の力の比がリンクの角度で変わる。同じ力でも、位置によって駆動側で見える負荷の変化が違う（感度が変わる）→ STEP4',
]): txt(BX, yy + i * 21, t_, size=12)
Wd, Hd = 1180, yy + 80
svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" font-family="Noto Sans CJK JP, Hiragino Sans, Meiryo, sans-serif">' % (Wd, Hd, Wd, Hd),
       '<defs>' + ''.join('<marker id="m%s" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="%s"/></marker>' % (c[1:], c) for c in (RED, BLU)) + '</defs>',
       '<rect width="100%" height="100%" fill="white"/>'] + out + ['</svg>']
open(sys.argv[1], 'w', encoding='utf-8').write('\n'.join(svg))
