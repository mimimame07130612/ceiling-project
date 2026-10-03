# K055 Oの高さと収納時の力（STEP4 4-3、水平・鉛直版スコットラッセル、左右独立駆動の仮前提）
# Oの高さh_O（Bのすべる水平線もh_O）を変えたときの、収納時のφ・Bの水平力・CSPの速さの比・O回りの余地を比べる。
# 力のつり合い（摩擦なし）：Cに鉛直荷重P → Bの水平力 F_B=P·cotφ。架台側の反力は、Oに水平 −F_B（＋鉛直）、ねじの受けに +F_B。
#   OとねじのRを1枚の架台に載せれば、F_Bは架台の中で打ち消し合い、梁のねじには鉛直荷重とモーメントだけが行く。
# 入力：A04-006、A04-007、A04-008（W=150N）、A01-001、A00-001（収納下端243.77→C=255.885）、D01-001（梁下面254.5・掘込面270）、K046・K053・K054
import math, csv, io, subprocess
TS=subprocess.run(['date','+%y%m%d%H%M'],capture_output=True,text=True,env={'TZ':'Asia/Tokyo'}).stdout.strip()
OUT='/mnt/user-data/outputs/%s_K055_Oの高さと収納時の力.csv'%TS
CS_H=255.885; ST=72.16; P1=75.0; P2=75.0+98.1
buf=io.StringIO(); w=csv.writer(buf)
w.writerow(['■ K055 Oの高さと収納時の力（片側あたり、左右独立駆動の仮前提、摩擦なし、安全率をかける前）。P：LC1 75N／LC2 173N（猫が片側の真上）'])
w.writerow(['a','O・レールの高さh_O','掘込面までの余地(270−h_O)','梁下面までの余地(h_O−254.5)','OC収納','収納φ(°)','使用φ(°)','cotφ収納（Cの速さ/Bの速さ）','Bの水平力 LC1','Bの水平力 LC2','Bの移動量','Oとねじ受けにかかる水平力 LC2×安全率4'])
for a in (45,50):
    for hO in (258,260,262,264,266,268):
        oc=hO-CS_H; ps=math.asin(oc/(2*a)); pu=math.asin((oc+ST)/(2*a))
        Bm=2*a*(math.cos(ps)-math.cos(pu)); c=1/math.tan(ps)
        w.writerow([a,hO,'%.1f'%(270-hO),'%.1f'%(hO-254.5),'%.2f'%oc,'%.1f'%math.degrees(ps),'%.1f'%math.degrees(pu),'%.1f'%c,'%.0f'%(P1*c),'%.0f'%(P2*c),'%.1f'%Bm,'%.0f'%(4*P2*c)])
w.writerow([]); w.writerow(['参考：A04-007 取付部・リンクは片側1200N以上（鉛直荷重から決めた値）。A04-002の平均速度1.28〜2.0cm/sは旧経路（一直線76.84）での値で、水平・鉛直版のストローク72.16では60秒→1.20cm/s'])
open(OUT,'w',encoding='utf-8-sig').write(buf.getvalue()); print(OUT); print(buf.getvalue())
