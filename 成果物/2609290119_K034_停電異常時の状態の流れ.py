# K034 停電・異常時の状態の流れ（STEP3 3-5）
# 通常の4状態と、異常停止・停電停止の2状態、その間の移り変わりを示す。決めていない所を①〜③で示す。
# 入力：K029版2（H17〜H21）、K032版2（S01〜S07）、D04-003（電気が切れても効く落下止め）、A04-004（150Nで停止・反転）
# 使い方：python3 本ファイル <出力svgパス> <タイムスタンプ>
import sys, html
TS = sys.argv[2]
e = html.escape; out = []
K, RED, GRN, GRY, BLU, ORG, PUR = '#333333', '#C0392B', '#2E9E6B', '#8a857a', '#2C6FB0', '#D35400', '#6A5FD0'
def txt(x, y, t, col='#222', anchor='start', size=13, bold=False):
    out.append('<text x="%s" y="%s" fill="%s" text-anchor="%s" font-size="%s"%s>%s</text>' % (x, y, col, anchor, size, ' font-weight="bold"' if bold else '', e(t)))
def box(cx, cy, w, h, t, sub, col, fill):
    out.append('<rect x="%s" y="%s" width="%s" height="%s" rx="10" fill="%s" stroke="%s" stroke-width="2"/>' % (cx - w / 2, cy - h / 2, w, h, fill, col))
    txt(cx, cy - 4, t, anchor='middle', bold=True, size=14); txt(cx, cy + 15, sub, anchor='middle', size=11, col='#555')
def arr(x1, y1, x2, y2, col=K, dash=None, lab=None, lx=0, ly=0, la='middle'):
    out.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="2" marker-end="url(#m%s)"%s/>' % (x1, y1, x2, y2, col, col[1:], ' stroke-dasharray="%s"' % dash if dash else ''))
    if lab: txt((x1 + x2) / 2 + lx, (y1 + y2) / 2 + ly, lab, col=col, anchor=la, size=11)
def mark(x, y, n):
    out.append('<circle cx="%s" cy="%s" r="13" fill="%s"/>' % (x, y, ORG)); txt(x, y + 5, n, col='white', anchor='middle', bold=True, size=13)
txt(40, 40, 'K034　停電・異常時の状態の流れ（STEP3 3-5）', size=18, bold=True)
txt(40, 62, '作成 %s　灰の枠＝通常の状態、赤の枠＝止まっている異常の状態。どの止まっている状態でも、落下止め（D04-003）がCSPを保持する。橙の①〜③はまだ決めていない所' % TS, size=12)
N = '#f4f4f4'
box(180, 170, 200, 60, '収納（停止）', '天井付近', GRY, N)
box(520, 170, 200, 60, '下降中', '2cm/s以下', GRY, N)
box(860, 170, 200, 60, '使用（停止）', 'SCの前', GRY, N)
box(520, 330, 200, 60, '上昇中', '2cm/s以下', GRY, N)
arr(280, 160, 418, 160, lab='下降の指令', ly=-8); arr(620, 160, 758, 160, lab='端点（S02）', ly=-8)
arr(860, 200, 622, 318, lab='上昇の指令', lx=40, ly=0, la='start'); arr(418, 330, 180, 202, lab='端点（S01）', lx=-40, ly=10, la='end')
box(360, 520, 260, 64, '異常停止', '検出で停止（反転はS03のみ）', RED, '#fbe9e7')
box(760, 520, 260, 64, '停電停止', '電気が切れた位置で止まる', RED, '#fbe9e7')
arr(500, 202, 380, 486, col=RED); txt(330, 420, '検出 S03〜S06', col=RED, anchor='end', size=11); arr(520, 362, 420, 486, col=RED)
arr(560, 202, 720, 486, col=RED, dash='5 3', lab='停電', lx=10, la='start'); arr(560, 362, 740, 486, col=RED, dash='5 3')
# 復帰
arr(360, 553, 360, 640, col=ORG); mark(385, 600, '②')
box(360, 675, 260, 60, '再開の操作', '人が確認してから／自動で', ORG, '#fdf1e6')
arr(760, 553, 760, 640, col=ORG, lab='復電', lx=10, la='start'); mark(735, 600, '③')
box(760, 675, 260, 60, '復電後の待機', '勝手に動かない（H19）', ORG, '#fdf1e6')
arr(890, 555, 1010, 640, col=ORG, dash='3 3'); mark(965, 590, '①')
box(1070, 675, 220, 60, '手で動かす', '電気なしで収納へ戻す（H18）', ORG, '#fdf1e6')
arr(230, 645, 180, 202, col=ORG, dash='3 3', lab='収納へ戻す', lx=-10, la='end')
NX, NY = 40, 760
txt(NX, NY, '■ 決めること', bold=True, size=14)
for i, t_ in enumerate([
 '① 途中で止まって電気が戻らないとき、手で収納位置まで戻せるようにするか（H18：頭の高さ・SCと干渉する位置で止まっている場合）',
 '　候補：戻せるようにする（手回し・落下止めを手で解除する等。解除そのものが落下の危険になる）／戻せなくてよい（復電を待つ）',
 '② 異常停止のあと、どうやって再開するか',
 '　候補：人が確認して再開の操作をする／原因がなくなったら自動で再開する。どの向き（収納／使用）へ動かすか',
 '③ 復電したあと、どうするか',
 '　候補：何もしないで待つ（次の指令を待つ）／自動で収納位置へ戻る。停電中に出ていた指令は捨てる（H19）',
]): txt(NX, NY + 26 + i * 21, t_, size=12, bold=t_[0] in '①②③')
Wd, Hd = 1220, NY + 170
svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" font-family="Noto Sans CJK JP, Hiragino Sans, Meiryo, sans-serif">' % (Wd, Hd, Wd, Hd),
       '<defs>' + ''.join('<marker id="m%s" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="%s"/></marker>' % (c[1:], c) for c in (K, RED, ORG)) + '</defs>',
       '<rect width="100%" height="100%" fill="white"/>'] + out + ['</svg>']
open(sys.argv[1], 'w', encoding='utf-8').write('\n'.join(svg))
