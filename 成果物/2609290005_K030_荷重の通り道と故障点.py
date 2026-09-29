# K030 荷重の通り道と落下につながる故障点（STEP3 3-2）
# CSPの重さが梁まで流れる経路（左右2系統＋駆動）をブロック図で示し、落下につながる故障点F1〜F6と、
# 故障点ごとの対策の考え方の候補を並べる。方式は選ばない（STEP4の機構しだいのため）。
# 入力：K029版2（H01・H02・H05・H17・H23）、A03-001、D04-001、A00-002、A00-005、A01-001、A04-001（猫5kg、起票予定）
# 使い方：python3 本ファイル <出力svgパス> <タイムスタンプ>
import sys, html
TS = sys.argv[2]
e = html.escape; out = []
K, RED, GRN, GRY, BLU, ORG, PUR = '#333333', '#C0392B', '#2E9E6B', '#8a857a', '#2C6FB0', '#D35400', '#6A5FD0'
def box(x, y, w, h, t, col=K, fill='#f4f4f4', size=13, sub=None):
    out.append('<rect x="%d" y="%d" width="%d" height="%d" rx="6" fill="%s" stroke="%s" stroke-width="1.5"/>' % (x, y, w, h, fill, col))
    out.append('<text x="%d" y="%d" text-anchor="middle" font-size="%d" fill="#222" font-weight="bold">%s</text>' % (x + w / 2, y + (h / 2 + 5 if not sub else h / 2 - 3), size, e(t)))
    if sub: out.append('<text x="%d" y="%d" text-anchor="middle" font-size="11" fill="#555">%s</text>' % (x + w / 2, y + h / 2 + 14, e(sub)))
def arr(x1, y1, x2, y2, col=K, w=2, dash=None):
    out.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="%s" marker-end="url(#a%s)"%s/>' % (x1, y1, x2, y2, col, w, col[1:], ' stroke-dasharray="%s"' % dash if dash else ''))
def txt(x, y, t, col='#222', anchor='start', size=13, bold=False):
    out.append('<text x="%d" y="%d" fill="%s" text-anchor="%s" font-size="%d"%s>%s</text>' % (x, y, col, anchor, size, ' font-weight="bold"' if bold else '', e(t)))
def fp(x, y, lab):
    out.append('<circle cx="%d" cy="%d" r="15" fill="%s"/>' % (x, y, RED))
    txt(x, y + 5, lab, col='white', anchor='middle', size=12, bold=True)

txt(40, 40, 'K030　荷重の通り道と落下につながる故障点（STEP3 3-2）', size=18, bold=True)
txt(40, 62, '作成 %s　スコットラッセル（A00-002）・両側支持（D04-001）を前提にした概念図。部品の形・駆動方式は未定（STEP4）。矢印は重さが流れる向き（下から上へ）' % TS, size=12)

# 梁
box(60, 90, 640, 44, '梁1・梁2（構造材、M6までのねじ止め：A00-005）', col=GRY, fill='#e6e3dc')
# 取付部
box(60, 180, 290, 50, '左の取付部（ブラケット＋ねじ）', sub='→梁1')
box(410, 180, 290, 50, '右の取付部（ブラケット＋ねじ）', sub='→梁2')
# リンク
box(60, 280, 290, 60, '左リンク（腕・ピン）', sub='スコットラッセル')
box(410, 280, 290, 60, '右リンク（腕・ピン）', sub='スコットラッセル')
# 保持具
box(160, 395, 440, 50, '保持具（両側のリンクと接続）')
# CSP
box(160, 490, 440, 60, 'CSP 7.90kg（＋猫5kg：H23）', sub='底面の部分支持板＋前面上角の爪（A03-001）', fill='#e8e8e8')
# 駆動
box(760, 280, 220, 60, '駆動（モーター・伝達）', sub='リンクの入力部を動かす／止める', col=BLU, fill='#eaf1f8')
box(760, 180, 220, 50, '駆動の取付部', col=BLU, fill='#eaf1f8')
for x in (205, 555):
    pass
arr(380, 490, 380, 447)
arr(260, 395, 205, 342); arr(500, 395, 555, 342)
arr(205, 280, 205, 232); arr(555, 280, 555, 232)
arr(205, 180, 205, 136); arr(555, 180, 555, 136)
arr(760, 310, 702, 310, col=BLU, dash='5 3'); arr(700, 318, 758, 318, col=BLU, dash='5 3')
arr(870, 180, 870, 150, col=BLU); out.append('<line x1="870" y1="150" x2="702" y2="112" stroke="%s" stroke-width="2"/>' % BLU)
txt(725, 300, '入力部', col=BLU, anchor='middle', size=11)
txt(725, 360, '重さで押し返す力', col=BLU, anchor='middle', size=11)
# 故障点
fp(150, 520, 'F1'); fp(140, 420, 'F2'); fp(40, 310, 'F3'); fp(40, 205, 'F4'); fp(1000, 300, 'F5'); fp(1000, 205, 'F4'); fp(1000, 335, 'F6')

# 表
NX, NY = 40, 600
txt(NX, NY, '■ 故障点と、落下を防ぐ考え方の候補（方式はまだ選ばない）', bold=True, size=14)
cols = [NX, NX + 50, NX + 330, NX + 520]
for c_, h_ in zip(cols, ['点', '故障すると', '関係する危険事象', '考え方の候補']): txt(c_, NY + 28, h_, size=12, bold=True)
T = [
 ('F1', 'CSPが保持具から滑る・外れる', 'H02、H23', '形で囲って拘束する／CSPを抱える補助ベルト（本体加工不可：D01-010）'),
 ('F2', '保持具・保持具とリンクの接続が壊れる', 'H01、H23', '安全率（3-6）／保持具から梁へ直接つなぐ別の経路（ワイヤ等）'),
 ('F3', '片側のリンク（腕・ピン）が壊れる', 'H01、H09', '片側だけでも全荷重を持てる強さにする（2系統の冗長）／安全率'),
 ('F4', '取付ねじが抜ける・緩む（駆動も同じ）', 'H01、H04、H16', '本数を増やして1本抜けても持つ／安全率／点検（STEP6）'),
 ('F5', '駆動の伝達が切れる（ねじ・ベルト・歯車）', 'H05', 'リンクが自重でつぶれて急降下 → 自己保持（逆に回らない伝達）／ブレーキ／落下速度で止まる装置'),
 ('F6', '電気が切れて止めておけない', 'H17', '電気がないと効くブレーキ（無励磁作動）／自己保持'),
]
for i, r in enumerate(T):
    y = NY + 52 + i * 24
    for c_, v_ in zip(cols, r): txt(c_, y, v_, size=12, col=RED if c_ == NX else '#222', bold=(c_ == NX))
y = NY + 52 + len(T) * 24 + 18
for i, t_ in enumerate([
 '・スコットラッセルでは、CSPの重さが入力部を押し返す力になる。駆動が止めておけないとリンクがつぶれて下がる（F5・F6）',
 '・左右2系統（D04-001）は、片側で全荷重を持てる強さにすれば、F3・F4に対して冗長になる。持てなければ冗長にはならない',
 '・F1とF2は左右に共通の1系統。ここが壊れると、左右のリンクが健全でも落ちる',
]): txt(NX, y + i * 21, t_, size=12)
Wc, Hc = 1240, 880
svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" font-family="Noto Sans CJK JP, Hiragino Sans, Meiryo, sans-serif">' % (Wc, Hc, Wc, Hc),
       '<defs>' + ''.join('<marker id="a%s" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="%s"/></marker>' % (c[1:], c) for c in (K, BLU)) + '</defs>',
       '<rect width="100%" height="100%" fill="white"/>'] + out + ['</svg>']
open(sys.argv[1], 'w', encoding='utf-8').write('\n'.join(svg))
