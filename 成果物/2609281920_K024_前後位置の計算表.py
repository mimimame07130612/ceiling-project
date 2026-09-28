# K024 前後位置（STEP2 2-2）の計算表
# 前提：K018のB（チルト24°維持）、右限・振りなし、余裕寸法 m=2（c1〜c4、仮）、保持具＝底面支持板（r=0.7、t下）＋前面上角の爪（K017）。
# 使用位置：D02-002（dはできるだけ小さく）→ 背面側の最後端とSC幕面の間を8（A02-004）とする最小のd1。支持板は背面より 0.407·t下 後ろに出る。
# 収納位置：K013の方法（一直線の平行移動、天井端・SCケースを m だけ太らせる）で、ワンモーション移動が成立する最小の収納d1。
# 上角の爪は背面側・下側に出ないため、この計算には効かない（前側は配光境界まで余裕、K022のc5）。
# 使い方：python3 本ファイル <出力csvパス>
import math, sys, csv
CD, CH, T = 21.4, 17.0, math.radians(24); c, s = math.cos(T), math.sin(T)
M, R = 2.0, 0.7
def dh(u, w): return (u*c + w*s, -u*s + w*c)
hu = lambda d: 161 + (d - 25) * 56 / 280
TAN59 = math.tan(math.radians(59)); light_d = lambda h: 130 - 5.7 - (270 - h) * TAN59
def edges(P):
    o = []
    for i in range(len(P)):
        a, b = P[i], P[(i+1) % len(P)]
        for k in range(41): o.append((a[0]+(b[0]-a[0])*k/40, a[1]+(b[1]-a[1])*k/40))
    return o
def hit(p):
    d, h = p
    return (d < 45.5+M-1e-9 and h > 250-M+1e-9) or (20.5-M < d < 33.9+M and 236.5-M < h < 250)
def inside(pt, P):
    sg = [(P[(i+1) % 4][0]-P[i][0])*(pt[1]-P[i][1])-(P[(i+1) % 4][1]-P[i][1])*(pt[0]-P[i][0]) for i in range(4)]
    return all(x >= -1e-9 for x in sg) or all(x <= 1e-9 for x in sg)
CORN = [(45.5+M, 250-M), (33.9+M, 236.5-M)]
def case(tp):
    BOX = [dh(0, 0), dh(CD, 0), dh(CD, CH), dh(0, CH)]
    PLATE = [dh(0, 0), dh(R*CD, 0), dh(R*CD, -tp), dh(0, -tp)] if tp > 0 else []
    parts = [BOX] + ([PLATE] if PLATE else [])
    pts = BOX + PLATE
    low_rel = min(p[1] for p in pts); top_rel = max(p[1] for p in pts); rear_rel = min(p[0] for p in pts)
    delta = max(0.0, (top_rel - low_rel) - (25 - M)); low_s = 245 - delta
    du = round(33 - rear_rel, 2)                      # SC幕面とのすき間8
    def place(P, d1, lh): return [(d1+a, lh-low_rel+b) for a, b in P]
    lu = max(hu(du+a) + M - (b - low_rel) for P in parts for a, b in edges(P))
    def bad(ds):
        for k in range(801):
            t = k/800; d1 = ds+(du-ds)*t; lh = low_s+(lu-low_s)*t
            for P in parts:
                Q = place(P, d1, lh)
                if any(hit(p) for p in edges(Q)): return True
                if t > 0 and any(inside(cn, Q) for cn in CORN): return True
        return False
    ds = 45.5
    while bad(ds): ds = round(ds + 0.1, 1)
    ds_max = min(light_d(h) - M - a for P in parts for a, b in edges(P) for h in [low_s - low_rel + b])
    baf = (du + (dh(CD, 0)[0] + dh(CD, CH)[0]) / 2, lu - low_rel + (dh(CD, 0)[1] + dh(CD, CH)[1]) / 2)
    el = math.degrees(math.atan((baf[1] - 100) / (270 - baf[0])))
    return [tp, round(delta, 2), round(low_s, 2), du, round(lu, 2), ds, round(ds_max, 1), round(ds - du, 1), round(low_s - lu, 2), round(baf[0], 1), round(el, 1)]
rows = [case(0.0), case(1.0), case(2.0), case(2.86)]
with open(sys.argv[1], 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.writer(f)
    w.writerow(['K024 前後位置の計算表（STEP2 2-2）　チルト24°維持・右限・振りなし・余裕2（仮）　単位cm・度'])
    w.writerow(['保持具：底面支持板 r=0.7、厚さ t下（P0から支持）。上角の爪はこの計算に効かない'])
    w.writerow(['支持板 t下', 'Δ（h=245の下げ量）', '収納最下点h', '使用d1（最小）', '使用最下点h', '収納d1の下限（ワンモーション）', '収納d1の上限（配光境界−2）', '前後移動量', '鉛直ストローク', '使用時バッフル中心d', 'LP目への仰角'])
    w.writerows(rows)
    w.writerow([])
    w.writerow(['使用d1：支持板が背面より 0.407·t下 後ろに出るため、SC幕面とのすき間8を保つ最小のd1が大きくなる'])
for r in rows: print(r)
