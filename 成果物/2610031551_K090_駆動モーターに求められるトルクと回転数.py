# K090 駆動モーターに求められるトルクと回転数（STEP4 4-3、Tr14×3）
# 機構（水平・鉛直版スコットラッセル、a=50）：Bの位置 xB=2a·cosφ、Cの高さの変化 hC=2a·sinφ（φ：収納7.0°〜使用57.4°）。
# 仮想仕事より、Bを押す力 F＝Wside·cotφ（Wside：片側が受ける上下の力）。Wside＝75N（LC1、K067：収納615N・使用48Nと整合）。
# 回し方：(A) Bを一定の速さで動かす（60秒）、(B) CSPを一定の速さで上下させる（60秒）。
# ねじ Tr14×3：有効径12.5、リード3、リード角4.37°。トルク T＝F·d2/2·tan(λ+ρ')、ρ'は μ=0.15（仮、厳しい側）で8.83°。安全率2（仮、駆動の余裕）。
import math, csv, subprocess
TS=subprocess.run(['date','+%y%m%d%H%M'],capture_output=True,text=True,env={'TZ':'Asia/Tokyo'}).stdout.strip()
a=50.0; p0,p1=math.radians(7.0),math.radians(57.4); WS=75.0; d2=12.5; L=3.0; lam=math.radians(4.37); rho=math.radians(8.83); SF=2.0; TT=60.0
SB=2*a*(math.cos(p0)-math.cos(p1))*10   # mm
SH=2*a*(math.sin(p1)-math.sin(p0))*10   # mm
vB=SB/TT; vH=SH/TT
rows=[]
for k in range(0,11):
    p=p0+(p1-p0)*k/10
    F=WS/math.tan(p); T=F*SF*(d2/1000)/2*math.tan(lam+rho)
    rpmA=vB/L*60; vCA=vB/math.tan(p)
    vBB=vH*math.tan(p); rpmB=vBB/L*60
    rows.append([round(math.degrees(p),1),round(F),round(F*SF),round(T,2),round(rpmA),round(vCA,1),round(rpmB),round(vH,1),round(T*rpmA*2*math.pi/60,1),round(T*rpmB*2*math.pi/60,1)])
for r in rows: print(r)
print('Bの移動量',round(SB,1),'mm  CSPの上下',round(SH,1),'mm')
out='/mnt/user-data/outputs/%s_K090_駆動モーターに求められるトルクと回転数.csv'%TS
with open(out,'w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f)
    w.writerow(['K090 駆動モーターに求められるトルクと回転数（Tr14×3、片側、常時LC1、μ=0.15・安全率2は仮）'])
    w.writerow(['Bの移動 %.1fmm、CSPの上下 %.1fmm、動作時間60秒（S3 e)の上限）。(A) Bを一定の速さ、(B) CSPを一定の速さ。F＝Wside·cotφ、Wside=75N（K067と整合）。'%(SB,SH)])
    w.writerow(['ねじの軸受け・ガイドの摩擦、加減速のトルクは含まない。'])
    w.writerow([])
    w.writerow(['φ（°、7.0=収納・57.4=使用）','Bを押す力 N','×安全率2 N','必要トルク N·m','(A) 回転数 rpm','(A) CSPの上下の速さ mm/s','(B) 回転数 rpm','(B) CSPの上下の速さ mm/s','(A) 出力 W','(B) 出力 W'])
    w.writerows(rows)
print(out)
