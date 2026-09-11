"""T005 図枠ライブラリ

出力ルール7-1〜7-6を満たす図の共通要素をSVG断片として返す。
機構や部屋の形状は生成しない。形状は呼び出し側が描く。
"""

VIEW_W = 680

ARROW_DEF = ('<defs><marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" '
             'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
             '<path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke" '
             'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>'
             '</marker></defs>')


def _t(x, y, s, cls="ts", anchor=None):
    a = ' text-anchor="%s"' % anchor if anchor else ""
    return '<text class="%s" x="%g" y="%g"%s>%s</text>' % (cls, x, y, a, s)


def header(title, created, projection, unit="cm", fig_no=None,
           x=40, y=26, scale_note="本図は非スケール"):
    """7-2 および 7-3(1)(2)(3)。

    fig_no は保管する図にのみ渡す。チャット表示のみの図では省略する。
    """
    if not title or not created or not projection:
        raise ValueError("7-3 図題と作成日時と投影は省略できない")
    head = title if fig_no is None else "%s\u3000%s" % (fig_no, title)
    out = [_t(x, y, head, "th")]
    out.append(_t(x, y + 20,
                  "作成日時：%s\u3000／\u3000投影：%s" % (created, projection)))
    note = "単位：%s" % unit
    if scale_note:
        note += "（%s）" % scale_note
    out.append(_t(x, y + 38, note))
    return "\n".join(out)


def axes(ox, oy, d_len=84, h_len=52, d_label="d", h_label="h",
         x_note="x は紙面手前が (+)"):
    """7-1 座標系の軸記号。原点の定義は legend の origins で併記する。"""
    s = ['<circle cx="%g" cy="%g" r="3" fill="var(--p)"/>' % (ox, oy)]
    s.append('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="var(--p)" '
             'stroke-width="1" marker-end="url(#arrow)"/>'
             % (ox, oy, ox + d_len, oy))
    s.append('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="var(--p)" '
             'stroke-width="1" marker-end="url(#arrow)"/>'
             % (ox, oy, ox, oy - h_len))
    s.append(_t(ox + d_len + 8, oy + 4, d_label, "th"))
    s.append(_t(ox + 6, oy - h_len - 2, h_label, "th"))
    if x_note:
        s.append(_t(ox, oy + 20, x_note))
    return "\n".join(s)


def dim(x1, y1, x2, y2, label, fixed, offset=0, anchor=None):
    """7-3(4) および 7-4 の寸法線。

    fixed=True で実線と通常表記。fixed=False で破線と括弧付き表記。
    区分の指定は省略できない。括弧は本関数が付ける。
    """
    if not isinstance(fixed, bool):
        raise ValueError("7-4 確定か仮置きかの区分を bool で渡すこと")
    if label[:1] in ("(", "\uff08"):
        raise ValueError("7-4 括弧は fixed=False のとき本関数が付ける")
    dash = "" if fixed else ' stroke-dasharray="6 4"'
    text = label if fixed else "(%s)" % label
    cls = "t" if fixed else "ts"
    s = ['<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="var(--p)" '
         'stroke-width="1"%s/>' % (x1, y1, x2, y2, dash)]
    if x1 == x2:
        for yy in (y1, y2):
            s.append('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="var(--p)" '
                     'stroke-width="1"/>' % (x1 - 6, yy, x1 + 6, yy))
        tx = x1 - 8 + offset
        ty = (y1 + y2) / 2.0
        an = anchor or "end"
    else:
        for xx in (x1, x2):
            s.append('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="var(--p)" '
                     'stroke-width="1"/>' % (xx, y1 - 6, xx, y1 + 6))
        tx = (x1 + x2) / 2.0
        ty = y1 - 8 + offset
        an = anchor or "middle"
    s.append(_t(tx, ty, text, cls, an))
    return "\n".join(s)


def leader(x1, y1, x2, y2, label=None, anchor="start"):
    """引出線。label を渡すと終点の脇に注記を置く。"""
    s = ['<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="var(--t)" '
         'stroke-width="0.5" stroke-dasharray="4 4"/>' % (x1, y1, x2, y2)]
    if label:
        s.append(_t(x2 + 6, y2 + 4, label, "ts", anchor))
    return "\n".join(s)


def unknown(x, y, what, anchor=None):
    """7-6 未測定や不明の箇所を空白にせず明示する。"""
    return _t(x, y, "未確定：%s" % what, "ts", anchor)


def legend(lines, y, x=40, origins=None, unknowns=None, step=20):
    """7-3(5) の凡例。7-4 の線種の説明を先頭に必ず置く。

    戻り値は (svg断片, 最終行のy)。
    """
    rows = ["実線・通常表記＝確定値\u3000／\u3000破線・括弧付き＝未確定値"]
    rows += list(lines)
    if origins:
        rows += list(origins)
    if unknowns:
        rows.append("未確定：" + "\u3000".join(unknowns))
    out = [_t(x, y, "凡例", "th")]
    for i, r in enumerate(rows):
        out.append(_t(x, y + step * (i + 1), r))
    return "\n".join(out), y + step * len(rows)


def sources(rows, y, x=40, step=20):
    """7-5 出典の併記。rows は (項番, 内容) の並び。

    戻り値は (svg断片, 最終行のy)。
    """
    if not rows:
        raise ValueError("7-5 出典が無いときは本関数を呼ばない")
    out = [_t(x, y, "出典", "th")]
    for i, r in enumerate(rows):
        out.append(_t(x, y + step * (i + 1), "%s：%s" % (r[0], r[1])))
    return "\n".join(out), y + step * len(rows)


def svg(height, body, title, desc):
    """SVG全体を組み立てる。title と desc は省略できない。"""
    if not title or not desc:
        raise ValueError("title と desc は省略できない")
    return ('<svg width="100%%" viewBox="0 0 %d %g" role="img">'
            '<title>%s</title><desc>%s</desc>\n%s\n%s\n</svg>'
            % (VIEW_W, height, title, desc, ARROW_DEF, body))
