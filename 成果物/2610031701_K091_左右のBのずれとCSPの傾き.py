# K091 左右のBのずれ（同期のずれ）が機構とCSPに与える影響（STEP4 4-3）
# K085・K086の構成（P2、リンク面 左94.75・右164.75、CSPは剛体、CとC′は d方向に Δd=180mm 離れ、Cのピンはx軸まわりに自由）で、
#   右のBだけをレール方向に 1mm 動かしたときの応答を立体骨組み（K086のモデル）で求めた。
# 結果：機構に力（こじれ）はほとんど生じない（駆動の反力 0.0002N/mm 以下）。代わりに、右のC′だけが上下し、CSPが x軸まわりに回る（前後に傾く＝ピッチが変わる）。
#   これは姿勢保持の仕組み（CとC′の高さの差でCSPの傾きを決める、配置β Δd=18）そのもので、左右のずれはCSPの傾きの誤差として現れる。
# 傾きの誤差（解析式）：C′の上下 Δh＝δB·cotφ、CSPの傾きの変化 Δθ＝Δh／Δd（Δd=180mm）。立体骨組みの結果（収納 8.193mm/mm、使用 0.639mm/mm）と一致。
import math, csv, subprocess
TS=subprocess.run(['date','+%y%m%d%H%M'],capture_output=True,text=True,env={'TZ':'Asia/Tokyo'}).stdout.strip()
DD=180.0
rows=[]
for ph in (7.0,10.0,15.0,20.0,30.0,40.0,50.0,57.4):
    c=1/math.tan(math.radians(ph)); dth=math.degrees(c/DD)
    rows.append([ph,round(c,3),round(dth,3),round(1.0/dth,2),round(0.5/dth,2)])
    print(rows[-1])
out='/mnt/user-data/outputs/%s_K091_左右のBのずれとCSPの傾き.csv'%TS
with open(out,'w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f)
    w.writerow(['K091 左右のBのずれ（1mm あたり）が CSPの傾き（前後、x軸まわり）に与える影響'])
    w.writerow(['立体骨組み（K086のモデル）で右のBだけを1mm動かした結果：機構の力はほぼ0（駆動の反力0.0002N/mm以下）、C′の上下 収納8.193mm・使用0.639mm、CSPはx軸まわりに回る。'])
    w.writerow(['解析式：Δh＝δB·cotφ、Δθ＝Δh/Δd（Δd=180mm）。傾きの許容値は未定（例として1°・0.5°の場合の許容ずれを示す）。'])
    w.writerow([])
    w.writerow(['φ °（7.0=収納、57.4=使用）','C′の上下 mm（Bのずれ1mmあたり）','CSPの傾きの変化 °（1mmあたり）','傾き1°までに許されるBのずれ mm','傾き0.5°までに許されるBのずれ mm'])
    w.writerows(rows)
print(out)
