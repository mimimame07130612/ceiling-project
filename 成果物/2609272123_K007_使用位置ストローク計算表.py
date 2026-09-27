# K007 使用位置・ストローク計算表（STEP1 1-4）。入力：A01-001（CSP寸法）、A00-004、A01-003、A00-001、D00-005／A00-006改訂(118°)、A02-001(出光面h=270)
import csv, math
CD, CH = 21.4, 17.0            # CSP 奥行・高さ（A01-001）
hu = lambda d: 161 + (d - 25) * 56 / 280          # 光束上端面（K004）
hs = lambda d: 100 + (270 - d) * 61 / 245         # 視線上端面（K003）
H_STO, D_F0, D_F1 = 245, 45.5, 82.7               # 収納下限、収納候補F
rows = []
for d1 in (25, 30, 35, 40, 45.5, 50, 55, 61.3):
    d2 = d1 + CD
    hb = hu(d2)                                   # CSP下端の下限（光束上端面、CSPのLP側面で決まる）
    hc, dc = hb + CH / 2, d1 + CD / 2
    ang = math.degrees(math.atan((hc - 100) / (270 - dc)))
    inF = D_F0 <= d1 and d2 <= D_F1
    rows.append([d1, round(d2, 1), round(hb, 1), round(hs(d1), 1), round(H_STO - hb, 1), round(ang, 1),
                 '鉛直移動可（収納候補Fの直下）' if inF else ('梁領域より前（d<45.5）：収納候補Fから前へ %.1f の移動が必要' % (D_F0 - d1) if d1 < D_F0 else '')])
    print(rows[-1])
with open('/mnt/user-data/outputs/%s_K007_使用位置ストローク計算表.csv' % __import__('sys').argv[1], 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.writer(f)
    w.writerow(['K007 使用位置・ストローク計算表（STEP1 1-4）　余裕寸法0の幾何限界値　単位cm・度'])
    w.writerow(['入力：A01-001（CSP D21.4・H17.0）、A00-004、A01-003、A00-001（収納下限h=245）、A00-006（配光118°）、A02-001（出光面h=270）'])
    w.writerow(['CSP SC側面 d1', 'CSP LP側面 d2', 'CSP下端の下限h（光束上端面@d2）', '参考：視線上端面h@d1', 'ストローク（245−下端下限）', 'LP目→CSP中心の仰角', '備考'])
    w.writerows(rows)
