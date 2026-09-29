# K039 スライダ関節Bの収納位置のO位置・リンク長a依存（計算表）STEP4 4-1
# スコットラッセルで、固定点Oの高さとリンク長aを振ったとき、収納時のB（スライダ関節）が
# 梁下面h=254.5・配光118°から逃げられるかを調べる。取付点C＝CSP側面の断面の中心（例）。
# 入力：A03-004・A03-005・A03-006（経路）、A01-001、A02-002、A00-005（梁下面）、D00-005・A00-006・A02-001（配光）
import math, csv, subprocess, glob, json
TS = subprocess.run(['date','+%y%m%d%H%M'],capture_output=True,text=True,env={'TZ':'Asia/Tokyo'}).stdout.strip()
CSP = sorted(glob.glob('*_csp.py'))[-1]
subprocess.run(['python3',CSP,'json','-o','_c.json','--pose','収納,139.45,48.5,243.77','--pose','使用,139.45,33,168.51'],check=True,capture_output=True)
C=json.load(open('_c.json',encoding='utf-8'))
side=[it['p'] for it in C['items'] if it['t']=='poly']
cs=[sum(p[0] for p in side[0])/4, sum(p[1] for p in side[0])/4]
cu=[sum(p[0] for p in side[1])/4, sum(p[1] for p in side[1])/4]
L=math.hypot(cu[0]-cs[0],cu[1]-cs[1])
uc=((cu[0]-cs[0])/L,(cu[1]-cs[1])/L)
us=(-uc[1],uc[0])                      # Bのガイド方向（LP側・下）
BEAM=254.5                             # 梁下面 A00-005/K027
# 配光：左リンク面x=110.9での配光下端h_top
XL,LX,R0,TN=110.9,129.65,5.7,math.tan(math.radians(59)); dx=LX-XL
h_top=270-(dx-R0)/TN
def row(Oh,a):
    t0=(Oh-cs[1])/(-uc[1]); O=(cs[0]-uc[0]*t0, Oh)
    amin=(t0+L)/2
    if a<amin: return None
    OBs=math.sqrt(max(0,4*a*a-t0*t0)); OBu=math.sqrt(max(0,4*a*a-(t0+L)**2))
    B=(O[0]+us[0]*OBs, O[1]+us[1]*OBs)
    phi_u=math.degrees(math.asin(min(1,(t0+L)/(2*a))))
    return dict(Oh=Oh,a=round(a,1),amin=round(amin,2),t0=round(t0,2),
                Bd=round(B[0],1),Bh=round(B[1],1),
                梁下=('○ h≧254.5' if B[1]>=BEAM else '× h<254.5(下に出る)'),
                配光=('○ 外' if B[1]>=h_top else '× 内(h<%.1f)'%h_top),
                ガイド長=round(OBs-OBu,1), 使用φ=round(phi_u,1))
rows=[]
for Oh in (256,260,264,268,270):
    t0=(Oh-cs[1])/(-uc[1]); amin=(t0+L)/2
    for da in (0.1,3,10,20):
        r=row(Oh,amin+da)
        if r: rows.append(r)
print('cs(収納C)=(%.2f,%.2f) L=%.2f 配光下端h_top=%.1f 梁下面=%.1f'%(cs[0],cs[1],L,h_top,BEAM))
hdr=['Oh','a','amin','t0','Bd','Bh','梁下','配光','ガイド長','使用φ']
w=max(len(str(r['Bh'])) for r in rows)
for r in rows: print('Oh=%d a=%5.1f(下限%5.2f) t0=%5.2f  B(d=%5.1f,h=%5.1f) 梁下%-14s 配光%-11s ガイド長%4.1f 使用φ%4.1f°'%(
    r['Oh'],r['a'],r['amin'],r['t0'],r['Bd'],r['Bh'],r['梁下'],r['配光'],r['ガイド長'],r['使用φ']))
# csv（BOM付utf-8）
out='/mnt/user-data/outputs/%s_K039_B収納位置のOa依存.csv'%TS
with open(out,'w',encoding='utf-8-sig',newline='') as f:
    wr=csv.writer(f)
    wr.writerow(['K039 スライダ関節Bの収納位置のO位置・a依存'])
    wr.writerow(['取付点C＝CSP側面の断面の中心（例）。収納C=(%.2f,%.2f)（d,h）、経路長L=%.2f、Bのガイドは経路直交でLP側へ%.2f°下がる'%(cs[0],cs[1],L,math.degrees(math.atan2(-us[1],us[0])))])
    wr.writerow(['梁下面 h=254.5（K027/A00-005）、配光118°の下端 h=%.1f（左リンク面x=110.9、A00-006/A02-001）'%h_top])
    wr.writerow([])
    wr.writerow(['O高さOh','リンク長a','a下限(=使用OC/2)','収納OC=t0','収納B d','収納B h','梁下面判定','配光判定','ガイド往復長','使用時φ(90°で伸切)'])
    for r in rows: wr.writerow([r['Oh'],r['a'],r['amin'],r['t0'],r['Bd'],r['Bh'],r['梁下'],r['配光'],r['ガイド長'],r['使用φ']])
print('wrote',out)
