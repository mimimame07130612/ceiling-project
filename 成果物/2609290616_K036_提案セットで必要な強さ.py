# K036 提案セットでの必要な強さ（STEP3 3-6）
# K035の提案セット（地震クラスS、猫の衝撃係数2、安全率 全体4・保持具6、mh≦7.4kg）を当てはめたとき、
# 部品ごとに必要な強さを荷重の通り道（K030）の上に示す。mhは上限の7.4kgとして計算（重いほど厳しい側）。
# 入力：K035、K030、A01-001、A04-001、D04-003
# 使い方：python3 本ファイル <出力svgパス> <タイムスタンプ>
import sys, html
TS = sys.argv[2]
g = 9.81; mc, mk, mh = 7.90, 5.0, 150 / 9.81 - 7.90
W = (mc + mh) * g
V = max(W + 2 * mk * g, W * 2.0); Hh = W * 2.0
S1, S2 = 4, 6
e = html.escape; out = []
K, RED, GRN, GRY, BLU, ORG = '#333333', '#C0392B', '#2E9E6B', '#8a857a', '#2C6FB0', '#D35400'
def kgf(n): return n / g
def txt(x, y, t, col='#222', anchor='start', size=13, bold=False):
    out.append('<text x="%s" y="%s" fill="%s" text-anchor="%s" font-size="%s"%s>%s</text>' % (x, y, col, anchor, size, ' font-weight="bold"' if bold else '', e(t)))
def box(x, y, w, h, t, col=K, fill='#f4f4f4'):
    out.append('<rect x="%s" y="%s" width="%s" height="%s" rx="6" fill="%s" stroke="%s" stroke-width="1.5"/>' % (x, y, w, h, fill, col))
    txt(x + w / 2, y + h / 2 + 5, t, anchor='middle', bold=True)
def tag(x, y, lines, col):
    out.append('<rect x="%s" y="%s" width="330" height="%s" rx="6" fill="white" stroke="%s" stroke-width="2"/>' % (x, y, 10 + 20 * len(lines), col))
    for i, l in enumerate(lines): txt(x + 10, y + 22 + i * 20, l, col=col if i == 0 else '#222', size=12, bold=(i == 0))
txt(40, 40, 'K036　提案セットで必要になる強さ（STEP3 3-6）', size=18, bold=True)
txt(40, 62, '作成 %s　動く部分の重さ W＝(CSP 7.90kg＋保持具・リンク %.1fkg)×9.81＝%.0f N（mhは上限で計算）' % (TS, mh, W), size=12); txt(40, 80, '最大の荷重：鉛直 %.0f N（%.1f kgf）・水平 %.0f N（%.1f kgf）＝地震クラスS（猫LC2は鉛直 %.0f N）' % (V, kgf(V), Hh, kgf(Hh), W + 2 * mk * g), size=12)
box(60, 105, 520, 40, '梁1・梁2', col=GRY, fill='#e6e3dc')
box(60, 180, 240, 44, '左の取付部（ねじ）'); box(340, 180, 240, 44, '右の取付部（ねじ）')
box(60, 270, 240, 44, '左リンク'); box(340, 270, 240, 44, '右リンク')
box(160, 360, 320, 44, '保持具'); box(160, 440, 320, 44, 'CSP', fill='#e8e8e8')
tag(640, 105, ['取付部（片側だけで全部持つ）', '鉛直 %.0f N（%.0f kgf）以上' % (V * S1, kgf(V * S1)), '水平 %.0f N（%.0f kgf）以上' % (Hh * S1, kgf(Hh * S1)), 'ねじが1本抜けても残りで上の値'], BLU)
tag(640, 230, ['リンク（片側だけで全部持つ）', '鉛直 %.0f N（%.0f kgf）以上' % (V * S1, kgf(V * S1)), '水平 %.0f N（%.0f kgf）以上' % (Hh * S1, kgf(Hh * S1)), '安全率4'], BLU)
tag(640, 360, ['保持具（左右共通の1系統）', '鉛直 %.0f N（%.0f kgf）以上' % (V * S2, kgf(V * S2)), '水平 %.0f N（%.0f kgf）以上' % (Hh * S2, kgf(Hh * S2)), '安全率6'], RED)
for y1, y2 in [(360, 314), (270, 224), (180, 140)]:
    for x in (180, 460):
        out.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="2"/>' % (x, y1, x, y2, K))
out.append('<line x1="320" y1="440" x2="320" y2="404" stroke="%s" stroke-width="2"/>' % K)
NY = 530
txt(40, NY, '■ ねじ1本あたりに必要な強さ（取付部1か所の鉛直、1本抜けた残りで持つ場合の単純な割り算）', size=14, bold=True)
for i, n in enumerate([2, 3, 4]):
    txt(60, NY + 28 + i * 22, 'ねじ%d本 → 残り%d本で %.0f N → 1本あたり %.0f N（%.0f kgf）' % (n, n - 1, V * S1, V * S1 / (n - 1), kgf(V * S1 / (n - 1))), size=12)
txt(60, NY + 28 + 3 * 22 + 6, '※実際にはねじの位置と力の向き（引き抜き／せん断）で1本ごとの負担が変わる。STEP4・STEP6で取付部の形が決まってから確かめる', size=12, col=GRY)
txt(40, NY + 140, '■ 身近なものとの比べ', size=14, bold=True)
txt(60, NY + 166, '・取付部とリンクは、片側だけで体重60kgの大人2人ぶん（約%.0f kgf）がぶら下がっても壊れない強さが目安' % kgf(V * S1), size=12)
txt(60, NY + 188, '・保持具は、体重60kgの大人3人ぶん（約%.0f kgf）がぶら下がっても壊れない強さが目安' % kgf(V * S2), size=12)
Wd, Hd = 1020, NY + 220
svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" font-family="Noto Sans CJK JP, Hiragino Sans, Meiryo, sans-serif">' % (Wd, Hd, Wd, Hd),
       '<rect width="100%" height="100%" fill="white"/>'] + out + ['</svg>']
open(sys.argv[1], 'w', encoding='utf-8').write('\n'.join(svg))
print(mh, W, V, Hh, V * S1, kgf(V * S1), V * S2, kgf(V * S2))
