# K013 斜め一直線移動の干渉判定表（STEP1 1-4 補足）
# CSP（側面図断面、チルト24°）を収納位置→使用位置へ一直線に平行移動したとき、固定物（天井 d<45.5・h>250、SCケース d=20.5〜33.9・h=236.5〜250）に当たるか
# 入力：A01-001、A02-002〜004、A00-001、A01-003、D01-001（掘込面前端d=45.5、天井h=250）、K011
import csv, math, sys
CD, CH, T = 21.4, 17.0, math.radians(24); c, s = math.cos(T), math.sin(T)
Q = [(0, 0), (CD*c, -CD*s), (CD*c+CH*s, -CD*s+CH*c), (CH*s, CH*c)]
hu = lambda d: 161 + (d - 25) * 56 / 280
def poly(d1, h0): return [(d1+a, h0+b) for a, b in Q]
def edges(P):
    pts = []
    for i in range(4):
        a, b = P[i], P[(i+1) % 4]
        for k in range(21): pts.append((a[0]+(b[0]-a[0])*k/20, a[1]+(b[1]-a[1])*k/20))
    return pts
def hit(p):
    d, h = p
    if d < 45.5 - 1e-9 and h > 250 + 1e-9: return '天井'
    if 20.5 < d < 33.9 and 236.5 < h < 250: return 'SCケース'
    return None
def inside(pt, P):   # 凸四角形内判定（固定物の角が断面内に入る場合）
    sg = []
    for i in range(4):
        a, b = P[i], P[(i+1) % 4]
        sg.append((b[0]-a[0])*(pt[1]-a[1]) - (b[1]-a[1])*(pt[0]-a[0]))
    return all(x >= -1e-9 for x in sg) or all(x <= 1e-9 for x in sg)
CORNERS = [((45.5, 250), '天井端'), ((33.9, 236.5), 'SCケース角')]
def check(ds, du):
    h0s = 245 + CD*s; h0u = hu(du + CD*c) + CD*s
    for k in range(401):
        t = k / 400; P = poly(ds + (du-ds)*t, h0s + (h0u-h0s)*t)
        for p in edges(P):
            r = hit(p)
            if r: return r, round(t, 3)
        for pt, nm in CORNERS:
            if inside(pt, P) and not (nm == '天井端' and t == 0): return nm, round(t, 3)
    return None, None
DS = [45.5, 46, 47, 48, 50, 52, 54, 56.2]; DU = [33, 35, 40, 45.5]
rows = []
for du in DU:
    r = [du]
    for ds in DS:
        res, t = check(ds, du)
        r.append('OK' if not res else 'NG(%s t=%.2f)' % (res, t))
    rows.append(r); print(r)
# 使用d1ごとに成立する最小の収納d1（0.1刻み）
mins = []
for du in DU:
    ds = 45.5
    while ds <= 56.2 + 1e-9 and check(ds, du)[0]: ds = round(ds + 0.1, 1)
    h0s = 245 + CD*s; h0u = hu(du + CD*c) + CD*s
    ang = math.degrees(math.atan2(h0s - h0u, ds - du)) if ds <= 56.2 else None
    mins.append([du, ds if ds <= 56.2 else '成立なし', round(ds - du, 1), round(h0s - h0u, 1), round(ang, 1) if ang else '-'])
    print(mins[-1])
out = '/mnt/user-data/outputs/%s_K013_斜め移動干渉判定表.csv' % sys.argv[1]
with open(out, 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.writer(f)
    w.writerow(['K013 斜め一直線移動の干渉判定表（STEP1 1-4 補足）　CSPチルト24°の断面を平行移動　余裕寸法0　単位cm・度'])
    w.writerow(['固定物：天井（d<45.5、h>250）、SCケース（d=20.5〜33.9、h=236.5〜250）。動作中の視線・光束・配光への干渉は判定対象外'])
    w.writerow(['使用d1＼収納d1'] + DS); w.writerows(rows)
    w.writerow([])
    w.writerow(['使用d1', '成立する最小の収納d1', '前後移動量', '鉛直移動量', '移動方向の水平からの角度'])
    w.writerows(mins)
