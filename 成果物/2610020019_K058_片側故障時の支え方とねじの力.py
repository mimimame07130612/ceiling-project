# K058 片側故障時の支え方とねじの力（STEP4 4-3、K057の続き）
# 依頼主判断：片側の故障と地震は同時に考えない（(イ)）。これにより片側全荷重のケースは LC1・LC2 だけになる。
# (ア1) 水平のまま保つ：残った側が全荷重をCSP重心で受ける（ねじりを含む）。K057の「片側全荷重」と同じ計算。
# (ア2) 傾いてもよい：残った側の保持具がd方向の軸まわりに自由に回れるとし、CSPは重心が軸の真下に来るまで傾いて止まる。
#        残った側は全荷重を鉛直にC点（リンク面上）で受け、ねじりは生じない。止まるまでの揺れの衝撃を見るため、静的値と×2（仮、A04-006の衝撃係数2に倣う）を併記。
#        軸の位置はリンク面上のC点（仮）。CSPの傾く角度・周りとの当たりは未検討。
# 参考：両側で支える状態の LC3（地震）。片側故障と同時に考えないため、(ア)のどちらを選んでも残る。
# その他の前提・計算方法は K057 と同じ（ねじ2列 h=258・266.5、各列k本、1本抜けの最悪値×安全率4、固定部品3.0kg/片側は仮）。
import math, csv, json, subprocess, importlib.util
TS=subprocess.run(['date','+%y%m%d%H%M'],capture_output=True,text=True,env={'TZ':'Asia/Tokyo'}).stdout.strip()
src=open('/tmp/k057.py',encoding='utf-8').read().split('rows=[]')[0]
exec(src)
def worst(s,k,loads_list):
    scr=screws(s,k); r=[0,0,0,0]
    for loads in loads_list:
        t,v=solve(scr,loads,s); t1=v1=0
        for j in range(len(scr)):
            a,b=solve(scr[:j]+scr[j+1:],loads,s); t1=max(t1,a); v1=max(v1,b)
        r=[max(r[0],t),max(r[1],v),max(r[2],t1),max(r[3],v1)]
    return r
rows=[]
for sn,s in SIDES.items():
    Pfix=((s['xb']+s['xl'])/2,(s['d0']+s['d1'])/2,262.0)
    for pos in ('収納','使用'):
        gd,gh=G_CSP[pos]; hC=H_C[pos]
        cases=[]
        for lc in ('LC1','LC2'):
            Wl=W+(CAT if lc=='LC2' else 0)
            cases.append(('(ア1) 水平のまま保つ',lc,'',[[((XC,gd,gh),(0,0,-Wl)),(Pfix,(0,0,-MF))]]))
            for fac in (1,2):
                cases.append(('(ア2) 傾いてもよい',lc,'静的' if fac==1 else '揺れ×2（仮）',[[((s['xl'],s['Od'],hC),(0,0,-fac*Wl)),(Pfix,(0,0,-MF))]]))
        Wl=W*share[sn]
        cases.append(('参考：両側・地震','LC3','±d・±x の最悪',[[((s['xl'],s['Od'],hC),(hx*2*Wl,hd*2*Wl,-2*Wl)),(Pfix,(hx*2*MF,hd*2*MF,-2*MF))] for hx,hd in ((1,0),(-1,0),(0,1),(0,-1))]))
        for cname,lc,note,L in cases:
            for k in (2,3,4):
                t,v,t1,v1=worst(s,k,L)
                rows.append([sn,pos,cname,lc,note,2*k,round(t),round(v),round(t1),round(v1),round(t1*SF),round(v1*SF)])
out='/mnt/user-data/outputs/%s_K058_片側故障時の支え方とねじの力.csv'%TS
with open(out,'w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f)
    w.writerow(['K058 片側故障時の支え方とねじの力（ねじ1本あたり、N）'])
    w.writerow(['依頼主判断：片側の故障と地震は同時に考えない。(ア1) 水平のまま保つ＝全荷重がCSP重心（ねじり含む）。(ア2) 傾いてもよい＝残った側のC点で鉛直に全荷重（ねじりなし）、揺れの衝撃×2は仮'])
    w.writerow(['その他の前提はK057と同じ。W=%.1fN、猫5kg×2、固定部品3.0kg/片側（仮）。必要耐力＝1本抜けの最悪値×安全率4'%W])
    w.writerow([])
    w.writerow(['側','位置','条件','荷重ケース','備考','ねじ本数','引抜き','せん断','引抜き(1本抜け)','せん断(1本抜け)','必要引抜き耐力','必要せん断耐力'])
    w.writerows(rows)
print(out)
for r in rows:
    if r[5]==6: print(r)
