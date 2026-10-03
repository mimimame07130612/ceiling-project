# K054 駆動点ごとの必要トルクと速度の概算（STEP4 4-4入口、水平・鉛直版スコットラッセル、姿勢保持案1・配置β）
# 摩擦なしの概算。仮想仕事より Bの水平力 F_B=P·cotφ、Oのトルク T_O=P·2a·cosφ、Cの速度/Bの速度=cotφ。
# ねじ駆動のモーター側トルク T=F·L/(2πη)（台形ねじ L=2mm η=0.35、ボールねじ L=5mm η=0.9、いずれも仮）。
# 入力：A04-006、A04-008（W=150N）、K053、動作時間60秒（S3 e）
import math, csv, io, subprocess
TS=subprocess.run(['date','+%y%m%d%H%M'],capture_output=True,text=True,env={'TZ':'Asia/Tokyo'}).stdout.strip()
OUT='/mnt/user-data/outputs/%s_K054_駆動点ごとのトルクと速度の概算.csv'%TS
a=0.5;W=150;CS=268-255.885;ST=72.16;CAT=98.1
ph=lambda s:math.asin((CS+ST*s)/100/(2*a))
B0=2*a*math.cos(ph(1));B1=2*a*math.cos(ph(0));vB=(B1-B0)*100/60
buf=io.StringIO();w=csv.writer(buf)
w.writerow(['■ K054 駆動点ごとの必要トルクと速度の概算（摩擦なし）。Bの移動%.1fcm、Cの移動%.2fcm、60秒、平均仕事率 %.1fW'%((B1-B0)*100,ST,W*ST/60/100)])
w.writerow(['第1表 収納時（φ=%.1f°）の必要値'%math.degrees(ph(0))])
w.writerow(['駆動のしかた','荷重ケース','受け持つ荷重P(N)','Bの水平力(N)','台形ねじL2 モーター側(N·m)','ボールねじL5 モーター側(N·m)','O軸で駆動したときのトルク(N·m)'])
for nm,cases in (('片側駆動（1台）',(('LC1',W),('LC2',W+CAT))),('左右独立（各1台、右側）',(('LC1',W/2),('LC2 猫が右端',W/2+CAT)))):
    for lc,P in cases:
        F=P/math.tan(ph(0))
        w.writerow([nm,lc,'%.0f'%P,'%.0f'%F,'%.2f'%(F*0.002/(2*math.pi*0.35)),'%.2f'%(F*0.005/(2*math.pi*0.9)),'%.1f'%(P*2*a*math.cos(ph(0)))])
w.writerow([]);w.writerow(['第2表 Bを一定速度(%.2fcm/s)で動かしたときのCSPの速さ'%vB])
w.writerow(['s','φ(°)','Cの速度/Bの速度','Cの速さ(cm/s)'])
for s in (0,0.1,0.25,0.5,0.75,1):
    w.writerow([s,'%.1f'%math.degrees(ph(s)),'%.2f'%(1/math.tan(ph(s))),'%.2f'%(vB/math.tan(ph(s)))])
open(OUT,'w',encoding='utf-8-sig').write(buf.getvalue());print(OUT);print(buf.getvalue())
