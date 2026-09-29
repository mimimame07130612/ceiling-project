# K035 荷重の組み合わせと安全率の参考値（STEP3 3-6）
# 設計に使う荷重ケース（常時・猫・地震）と、必要な強さ（荷重×安全率）を、保持具・リンクの質量mhを変数にして示す。
# 入力：A01-001（7.90kg）、A04-001（猫5kg、起票予定）、D04-003（片側で全荷重）、A04-004（150N、起票予定）
# 参考：建築設備耐震設計・施工指針2014 設計用水平震度 KH=Z·Ks、上層階の Ks＝S2.0／A1.5／B1.0、鉛直は水平の1/2（東京消防庁資料、斉木電気設備の解説）
#       クレーン等安全規則 玉掛け用ワイヤロープの安全係数6以上（第213条）、つりチェーン4以上（第213条の2、条件あり）
#       衝撃係数2：力が急に加わる場合（落下高さ0）の静的な値に対する倍率（材料力学の基本）
# 使い方：python3 本ファイル <出力svgパス> <タイムスタンプ>
import sys, html
TS = sys.argv[2]
g = 9.81; Wc = 7.90 * g; Wk = 5.0 * g
e = html.escape; out = []
K, RED, GRN, GRY, BLU, ORG, PUR = '#333333', '#C0392B', '#2E9E6B', '#8a857a', '#2C6FB0', '#D35400', '#6A5FD0'
def f(n, d=1): return ('%.*f' % (d, n))
def txt(x, y, t, col='#222', anchor='start', size=13, bold=False):
    out.append('<text x="%s" y="%s" fill="%s" text-anchor="%s" font-size="%s"%s>%s</text>' % (x, y, col, anchor, size, ' font-weight="bold"' if bold else '', e(t)))
txt(40, 40, 'K035　荷重の組み合わせと安全率の参考値（STEP3 3-6）', size=18, bold=True)
txt(40, 62, '作成 %s　W＝CSP＋保持具・リンク（mh）の重さ。D04-003により、片側のリンク・取付部はこの全荷重を1系統で持つ。mhは未定のため0kgと5kgで例示' % TS, size=12)
y = 100
txt(40, y, '■ 荷重ケース', size=14, bold=True)
cols = [40, 250, 560, 740, 920]
for c_, h_ in zip(cols, ['ケース', '中身', '鉛直（N）mh=0 / 5kg', '水平（N）mh=0 / 5kg', '根拠']): txt(c_, y + 26, h_, size=12, bold=True)
cases = []
def row(i, name, desc, v0, v5, h0, h5, src, col='#222'):
    yy = y + 50 + i * 24
    for c_, s_ in zip(cols, [name, desc, '%s / %s' % (f(v0), f(v5)), '%s / %s' % (f(h0), f(h5)) if h0 is not None else '—', src]): txt(c_, yy, s_, size=12, col=col)
W5 = Wc + 5 * g
row(0, 'LC1 常時', 'W', Wc, W5, None, None, 'A01-001')
row(1, 'LC2 猫が飛び乗る', 'W＋猫×衝撃係数2', Wc + 2 * Wk, W5 + 2 * Wk, None, None, 'A04-001。係数2は落下高さ0の値', col=RED)
for i, (ks, cls) in enumerate([(1.0, 'B'), (1.5, 'A'), (2.0, 'S')]):
    kh = ks; kv = kh / 2
    row(2 + i, 'LC3 地震（クラス%s）' % cls, 'W×(1＋KV)、W×KH　KH=%s' % f(kh), Wc * (1 + kv), W5 * (1 + kv), Wc * kh, W5 * kh, '設備耐震指針 上層階 Z=1.0')
y2 = y + 50 + 5 * 24 + 20
for i, t_ in enumerate([
 '・LC2の衝撃係数2は「高さ0から急に乗った」ときの値。実際に跳び乗ると、乗る高さと受ける側のたわみで大きくなる（上限は資料なし）',
 '・LC3の震度は建築設備の指針の上層階の値（Z＝地域係数は最大1.0として計算）。この装置が上層階・中間階・1階のどれに当たるかは未確認。猫と地震は同時に考えない',
]): txt(40, y2 + i * 20, t_, size=12)
y3 = y2 + 70
txt(40, y3, '■ 必要な強さ（最大の荷重×安全率）の例：mh=0 / 5kg', size=14, bold=True)
vmax0 = max(Wc + 2 * Wk, Wc * 2.0); vmax5 = max(W5 + 2 * Wk, W5 * 2.0)
cols2 = [40, 330, 560]
for c_, h_ in zip(cols2, ['安全率', '必要な強さ（鉛直・N）', '参考']): txt(c_, y3 + 26, h_, size=12, bold=True)
for i, (sf, ref) in enumerate([(4, 'つりチェーンの安全係数（クレーン則 第213条の2、条件あり）'), (6, '玉掛け用ワイヤロープの安全係数（クレーン則 第213条）')]):
    yy = y3 + 50 + i * 24
    for c_, s_ in zip(cols2, [str(sf), '%s / %s' % (f(vmax0 * sf, 0), f(vmax5 * sf, 0)), ref]): txt(c_, yy, s_, size=12)
y4 = y3 + 50 + 2 * 24 + 20
txt(40, y4, '■ 気づいたこと', size=14, bold=True)
for i, t_ in enumerate([
 '・最大の鉛直荷重は猫（LC2）と地震クラスS（LC3）が同じくらい。mh=0なら猫、mhが重くなるとクラスSの地震のほうが大きくなる',
 '・A04-004（相手にかかる力150N以下）との関係：下降中に下の物に乗る重さは W＝(7.90＋mh)×9.81。150N以下にするには mh≦%s kg（動く部分の質量）' % f(150 / g - 7.90),
 '・梁へのねじの引き抜き：規準の耐力式はJIS規格のねじを指定の条件で使った場合だけに当てはまり、市販のねじは製品ごとの試験値で確認されているのが現状',
 '　→ ねじは試験値（メーカー公表値）のある製品を選び、その値で確認する（STEP6）。1本抜けても持つ本数にする（D04-003）',
]): txt(40, y4 + 26 + i * 20, t_, size=12)
Wd, Hd = 1300, y4 + 130
svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" font-family="Noto Sans CJK JP, Hiragino Sans, Meiryo, sans-serif">' % (Wd, Hd, Wd, Hd),
       '<rect width="100%" height="100%" fill="white"/>'] + out + ['</svg>']
open(sys.argv[1], 'w', encoding='utf-8').write('\n'.join(svg))
print(Wc, Wc + 2 * Wk, vmax0, vmax5, 150 / g - 7.9)
