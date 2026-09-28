# K020 左右位置と振り角の計算表（STEP2 2-1＋2-3）
# 入力：A01-001（W57.1）、A02-002（チルト24°→平面外接奥行26.46）、A02-006・K011（使用d1=33のバッフル中心d=56.0）、
#       D01-008（LLP x=132.5、RLP x=205.5、中央169）、D01-009（梁1内面x=89.5、梁2内面x=170）
# 前提：保持具の左右の厚さ t左・t右＝0、余裕寸法0。振りの回転中心は平面外接の中心。目の位置 d=270。
# 使い方：python3 本ファイル <出力csvパス>
import csv, math, sys
W, BD, BAF, LPD = 57.1, 26.46, 56.0, 270
XL, XR, LLP, RLP, MID = 89.5, 170, 132.5, 205.5, 169
def hw(th): return W / 2 * math.cos(th) + BD / 2 * math.sin(th)
def ang(x, tx): return math.degrees(math.atan((tx - x) / (LPD - BAF)))
def solve(f, a, b):
    for _ in range(60):
        m = (a + b) / 2
        if f(a) * f(m) <= 0: b = m
        else: a = m
    return (a + b) / 2
th = lambda x: math.atan((MID - x) / (LPD - BAF))
lo = solve(lambda x: x - hw(th(x)) - XL, 100, 132); hi = solve(lambda x: x + hw(th(x)) - XR, 132, 150)
rows = []
for x in (XL + W / 2, round(lo, 2), 125, LLP, 135, round(hi, 2), XR - W / 2):
    t = th(x); h = hw(t)
    rows.append([round(x, 2), round(MID - x, 2), round(ang(x, LLP), 2), round(ang(x, MID), 2), round(ang(x, RLP), 2),
                 round(x - W / 2, 2), round(x + W / 2, 2), round(x - h, 2), round(x + h, 2),
                 ('可（接する）' if min(x - h - XL, XR - x - h) < 0.05 else '可') if (x - h >= XL - 0.05 and x + h <= XR + 0.05) else '不可（梁に当たる）'])
with open(sys.argv[1], 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.writer(f)
    w.writerow(['K020 左右位置と振り角の計算表（STEP2 2-1＋2-3）　余裕寸法0の幾何限界値　単位cm・度'])
    w.writerow(['入力：A01-001、A02-002、A02-006・K011（使用d1=33、バッフル中心d=56.0）、D01-008、D01-009。t左・t右＝0。振りの回転中心は平面外接の中心'])
    w.writerow(['振らない場合の中心x範囲：%.2f〜%.2f。LP中央へ振る場合の中心x範囲：%.2f〜%.2f' % (XL + W / 2, XR - W / 2, lo, hi)])
    w.writerow(['CSP中心x', 'LP中央とのずれ', 'LLPへの角度', 'LP中央への角度（振り角）', 'RLPへの角度',
                '振らない時 左端x', '振らない時 右端x', '中央へ振った時 左端x', '中央へ振った時 右端x', '中央へ振った時 梁1・梁2内面との判定'])
    w.writerows(rows)
    w.writerow([])
    w.writerow(['角度：CSP正面（+d方向）から右（+x）が正。t左・t右を足すと、中心xの範囲は左限が+t左、右限が−t右だけ狭まる'])
for r in rows: print(r)
print(lo, hi)
