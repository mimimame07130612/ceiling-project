# K053 左右同期の案の力の比較（STEP4 4-2→4-4入口、姿勢保持案1・配置β）
# 片側（左）だけを駆動したとき、右側の荷重を左から右へ渡すために同期部材が受け持つ力を、収納→使用で比べる。
# 力学（水平・鉛直版スコットラッセル、OA=AB=AC=a、φ＝ロッドBCとBのすべる水平線の角＝OAの水平からの角）：
#   Cの高さ h=268−2a·sinφ、Bの位置 =O+2a·cosφ。仮想仕事より、Cの鉛直荷重Pを支えるのに
#   Bに要る水平力 F_B=P·cotφ、Oに要るトルク T_O=P·2a·cosφ。
# 案：参考K051（B–B′直結）＝F_B。S2（O軸連結）＝軸のねじりトルクT_O、平行リンクの力 F=T_O/(r·sinμ)
#   （クランクをOAと同じ向き：sinμ=sinφ、OAに直角：sinμ=cosφ）。
#   S1（保持具の枠だけ、右は駆動なし）＝右のBが自由なので右側は荷重を持てない → 左が全荷重＋x方向のずれによるロール（d軸回り）のモーメント。
#   S3（左右別モーター）＝通常は各側がP·cotφを駆動。片側停止時の力はモーターの出力で決まるため、ここでは計算できない（4-4）。
# 入力：A04-006（荷重ケース）、A04-008（W上限150N）、A01-001、K051/K052（x=110.9・168.0、CSP中心x=139.45、a=50）
import math, csv, io, subprocess
TS=subprocess.run(['date','+%y%m%d%H%M'],capture_output=True,text=True,env={'TZ':'Asia/Tokyo'}).stdout.strip()
OUT='/mnt/user-data/outputs/%s_K053_左右同期の案の力の比較.csv'%TS
a=0.50; W=150.0; CAT=5*9.81*2; CS_H=255.885; STROKE=72.16; t0=268-CS_H
XL,XR,XC=110.9,168.0,139.45
LC={'LC1 常時':W/2,'LC2 猫が右端':W/2+CAT,'LC3 地震(KV=1.0)':W/2*2}
buf=io.StringIO(); w=csv.writer(buf)
w.writerow(['■ K053 左右同期の案の力の比較。W=150N（A04-008上限）、右側の荷重P＝LC1 75N／LC2 173N（猫98Nが右のリンク面の真上）／LC3 150N。単位 N・N·m。a=50cm'])
w.writerow(['第1表 片側（左）駆動で、右側の荷重Pを同期部材が渡すときの力'])
w.writerow(['荷重ケース','s(0収納,1使用)','φ(°)','右側P','参考K051 B–B′直結の力','S2 軸トルク','S2 平行リンク力 r=8・OAと同向き','S2 平行リンク力 r=4.2・OAに直角','S2 平行リンク力 r=8・OAに直角'])
rows=[]
for lc,P in LC.items():
    for s in (0,0.25,0.5,0.75,1):
        oc=(t0+STROKE*s)/100; ph=math.asin(oc/(2*a)); T=P*2*a*math.cos(ph)
        r_=[lc,s,'%.1f'%math.degrees(ph),'%.0f'%P,'%.0f'%(P/math.tan(ph)),'%.1f'%T,
            '%.0f'%(T/(0.08*math.sin(ph))),'%.0f'%(T/(0.042*math.cos(ph))),'%.0f'%(T/(0.08*math.cos(ph)))]
        w.writerow(r_); rows.append(r_)
w.writerow([])
w.writerow(['第2表 S1（枠だけ、右は駆動なし）：右側は荷重を持てず、左側が全荷重とロールモーメントを持つ（行程によらず一定）'])
w.writerow(['荷重ケース','左側の鉛直荷重','ロールモーメント（左リンク面まわり）','内訳'])
m1=W*(XC-XL)/100
w.writerow(['LC1 常時','%.0f'%W,'%.1f'%m1,'W×(139.45−110.9)=150×0.2855'])
w.writerow(['LC2 猫が右端','%.0f'%(W+CAT),'%.1f'%(m1+CAT*(XR-XL)/100),'＋猫98N×(168.0−110.9)'])
w.writerow(['LC3 地震(KV=1.0)','%.0f'%(2*W),'%.1f'%(2*m1),'2W×0.2855'])
w.writerow([])
w.writerow(['第3表 参考：駆動側が出す水平力（B）'])
w.writerow(['s','φ(°)','左右とも駆動（各側 W/2·cotφ）','片側駆動（W·cotφ）'])
for s in (0,0.25,0.5,0.75,1):
    oc=(t0+STROKE*s)/100; ph=math.asin(oc/(2*a))
    w.writerow([s,'%.1f'%math.degrees(ph),'%.0f'%(W/2/math.tan(ph)),'%.0f'%(W/math.tan(ph))])
w.writerow([])
w.writerow(['参考：A04-007 取付部・リンクは片側1200N以上、保持具は1800N以上（安全率込みの目安）'])
open(OUT,'w',encoding='utf-8-sig').write(buf.getvalue()); print(OUT); print(buf.getvalue())
