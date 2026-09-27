# K009 チルト24°時の使用位置・ストローク計算表（STEP1 1-4）
# 入力：A01-001（CSP D21.4・H17.0）、A02-002（チルト24°、h_d2<h_d1）、A00-004・A01-003（光束上端面）、A00-001（収納下限h=245）、A00-006（配光118°）、A02-001
import csv, math, sys
CD, CH, T = 21.4, 17.0, math.radians(24)
c, s = math.cos(T), math.sin(T)
# 側面図断面：P0=SC側下角(d1,h0) P1=LP側下角 P2=SC側上角 P3=LP側上角
P = {'P0': (0, 0), 'P1': (CD*c, -CD*s), 'P2': (CH*s, CH*c), 'P3': (CD*c+CH*s, -CD*s+CH*c)}
BD = max(p[0] for p in P.values()); BHlo = P['P1'][1]; BHhi = P['P2'][1]
hu = lambda d: 161 + (d - 25) * 56 / 280
H_STO, F0, F1 = 245, 45.5, 82.7
h0_sto = H_STO - BHlo                                   # 収納時：最下点P1をh=245に置く
print('外接 奥行%.2f 高さ%.2f  収納時 最下点245 最上点%.2f' % (BD, BHhi - BHlo, h0_sto + BHhi))
rows = []
for d1 in (25, 30, 35, 40, 45.5, 50, 56.2):
    hP1 = hu(d1 + P['P1'][0])                           # 最下点P1を光束上端面に置く（余裕0）
    h0 = hP1 - BHlo
    bc = (d1 + (P['P1'][0] + P['P3'][0]) / 2, h0 + (P['P1'][1] + P['P3'][1]) / 2)   # バッフル（LP側面）中心
    ang = math.degrees(math.atan((bc[1] - 100) / (270 - bc[0])))
    dhit = bc[0] + (bc[1] - 100) / math.tan(T)
    note = '収納候補F直下（鉛直移動のみ）' if d1 >= F0 else '収納位置d1=45.5から前へ%.1f移動' % (F0 - d1)
    rows.append([d1, round(d1 + BD, 1), round(hP1, 1), round(h0 + BHhi, 1), round(H_STO - hP1, 1),
                 '%.1f,%.1f' % bc, round(ang, 1), round(dhit, 1), note])
    print(rows[-1])
out = '/mnt/user-data/outputs/%s_K009_チルト時使用位置計算表.csv' % sys.argv[1]
with open(out, 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.writer(f)
    w.writerow(['K009 チルト24°時の使用位置・ストローク計算表（STEP1 1-4）　余裕寸法0の幾何限界値　単位cm・度'])
    w.writerow(['入力：A01-001、A02-002（チルト24°）、A00-004・A01-003（光束上端面 h=161+(d−25)×56/280）、A00-001、A00-006（118°）、A02-001'])
    w.writerow(['CSP外接：奥行%.2f・高さ%.2f。収納時（チルト維持と仮置き）：最下点h=245、最上点h=%.2f（掘込面h=270）' % (BD, BHhi - BHlo, h0_sto + BHhi)])
    w.writerow(['SC側下角 d1', 'LP側端 d（外接）', '最下点h（LP側下角＝光束上端面）', '最上点h（SC側上角）', 'ストローク（245−最下点）', 'バッフル中心 d,h', 'LP目への仰角', '軸（下向き24°）がh=100に達するd', '備考'])
    w.writerows(rows)
