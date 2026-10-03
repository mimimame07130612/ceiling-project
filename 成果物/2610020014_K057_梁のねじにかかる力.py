# K057 梁のねじにかかる力（STEP4 4-3、K056の架台配置、仮設定）
# 架台（梁の内側面の板）を梁にねじ止めしたとき、ねじ1本にかかる引抜き力（梁から離す向き）と、せん断力（板の面内）を求める。
# 前提（仮）：架台 h=254.5〜270、ねじ2列（h=258・266.5）×各列k本（板の端から5に等間隔）。リンク面 左x=92.0・右x=168.0、梁面 左x=89.5・右x=170。
#   左 O/C d=52.73、右 O′/C′ d=70.73。CSP中心 x=139.45（wR=0）。C点 収納h=255.885・使用h=183.725。
#   荷重（A04-006）：W=(7.90＋7.4)×9.81。LC1 W、LC2 W＋5kg×2×9.81、LC3 鉛直2W＋水平2W（±d・±xのどちらか一方）。
#   架台に載る固定部品（架台・軸受け・レール・ねじ・モーター）の質量 m_fix=3.0kg/片側（仮、未選定）。地震時は同じ係数をかける。
#   分担ケース：「両側」＝左右がCSP中心のx位置でてこ比に分担し、C点に作用。「片側全荷重」＝D04-003（片側が壊れても落ちない）で、全荷重がCSP重心に作用し、片側の機構がねじり・曲げも受け持つ。
# 計算：架台を剛体、ねじを弾性ばねとした線形分布（引抜き：板面に垂直、せん断：板面内）。圧縮側は接触でなく、ねじで受ける扱い（引抜きは安全側に大きめ）。
# 1本抜け（A04-009）：全ねじについて1本ずつ外し、最大値をとる。必要耐力＝最大値×安全率4（A04-007）。
import math, csv, json, subprocess
TS=subprocess.run(['date','+%y%m%d%H%M'],capture_output=True,text=True,env={'TZ':'Asia/Tokyo'}).stdout.strip()
g=9.81; W=(7.90+7.4)*g; CAT=5*2*g; MF=3.0*g; SF=4
H_C={'収納':255.885,'使用':183.725}
prof=[i['p'] for i in json.load(open('/tmp/c56.json',encoding='utf-8'))['items'] if i['t']=='poly' and i['view']=='side']
def cen(P):
    A=cx=cy=0
    for i in range(len(P)):
        x0,y0=P[i]; x1,y1=P[(i+1)%len(P)]; c=x0*y1-x1*y0; A+=c; cx+=(x0+x1)*c; cy+=(y0+y1)*c
    return cx/(3*A), cy/(3*A)
G_CSP={'収納':cen(prof[0]),'使用':cen(prof[1])}
SIDES={'左':dict(xl=92.0,xb=89.5,Od=52.73,d0=48.73,d1=165.99,sgn=+1),'右':dict(xl=168.0,xb=170.0,Od=70.73,d0=66.73,d1=183.99,sgn=-1)}
XC=139.45
share={'左':(168.0-XC)/76.0,'右':(XC-92.0)/76.0}
def screws(s,k):
    ds=[s['d0']+5+(s['d1']-s['d0']-10)*i/(k-1) for i in range(k)]
    return [(d,h) for d in ds for h in (258.0,266.5)]
def solve(scr,loads,s):
    # loads: list of (point(x,d,h), force(Fx,Fd,Fh))  板面x=xb、梁は sgn側（左：−x側に梁 → 梁から離す向き＝+x）
    n=len(scr); dc=sum(d for d,h in scr)/n; hc=sum(h for d,h in scr)/n
    F=[0,0,0]; M=[0,0,0]
    for (x,d,h),f in loads:
        r=(x-s['xb'],d-dc,h-hc)
        for i in range(3): F[i]+=f[i]
        M[0]+=r[1]*f[2]-r[2]*f[1]; M[1]+=r[2]*f[0]-r[0]*f[2]; M[2]+=r[0]*f[1]-r[1]*f[0]
    # 引抜き：梁から離れる向きの力 Fout = Fx*sgn（左：梁は−x側にある → +xが離れる向き）
    off=s['sgn']; Idd=sum((d-dc)**2 for d,h in scr); Ihh=sum((h-hc)**2 for d,h in scr)
    T=[]; V=[]
    for d,h in scr:
        Dd,Dh=d-dc,h-hc
        # 板が受ける x力 Fx、モーメント Md(=M[1])・Mh(=M[2]) をねじのx方向力で釣り合わせる（Σ Dh·S=−Md, Σ −Dd·S=−Mh）
        S=-F[0]/n - M[1]*Dh/Ihh + M[2]*Dd/Idd   # ねじから板へのx方向の力
        T.append(max(0.0,-S*off*-1) if False else S*off)  # 引抜き力（正＝ねじが板を梁へ引き戻す＝ねじに引張）
        Ip=Idd+Ihh
        vd=-F[1]/n + M[0]*Dh/Ip; vh=-F[2]/n - M[0]*Dd/Ip
        V.append(math.hypot(vd,vh))
    return max(T),max(V)
rows=[]
for sn,s in SIDES.items():
    for pos in ('収納','使用'):
        gd,gh=G_CSP[pos]; hC=H_C[pos]
        Pfix=((s['xb']+s['xl'])/2,(s['d0']+s['d1'])/2,262.0)
        for mode in ('両側','片側全荷重'):
            for lc in ('LC1','LC2','LC3'):
                Wl=W+(CAT if lc=='LC2' else 0)
                if mode=='両側': P=(s['xl'],s['Od'],hC); Wl*=share[sn]
                else: P=(XC,gd,gh)
                kv=2.0 if lc=='LC3' else 1.0
                dirs=[(0,0)] if lc!='LC3' else [(1,0),(-1,0),(0,1),(0,-1)]
                for k in (2,3,4):
                    scr=screws(s,k); best=[0,0,0,0,'']
                    for hx,hd in dirs:
                        kh=2.0 if lc=='LC3' else 0.0
                        loads=[(P,(hx*kh*Wl,hd*kh*Wl,-kv*Wl)),(Pfix,(hx*kh*MF,hd*kh*MF,-kv*MF))]
                        t,v=solve(scr,loads,s)
                        t1=v1=0
                        for j in range(len(scr)):
                            a,b=solve(scr[:j]+scr[j+1:],loads,s); t1=max(t1,a); v1=max(v1,b)
                        tag='' if lc!='LC3' else ('±x' if hx else '±d')
                        if t1>best[2]: best[0],best[2],best[4]=t,t1,tag
                        best[1]=max(best[1],v); best[3]=max(best[3],v1)
                    rows.append([sn,pos,mode,lc,best[4],2*k,round(best[0]),round(best[1]),round(best[2]),round(best[3]),round(best[2]*SF),round(best[3]*SF)])
out='/mnt/user-data/outputs/%s_K057_梁のねじにかかる力.csv'%TS
with open(out,'w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f)
    w.writerow(['K057 梁のねじにかかる力（ねじ1本あたり、N）'])
    w.writerow(['前提（仮）：K056の架台配置。ねじ2列（h=258・266.5）×各列k本、板の端から5に等間隔。W=(7.90+7.4)×9.81=%.1fN、猫5kg×2、地震 鉛直2W＋水平2W（±d・±x）。固定部品3.0kg/片側（仮）。'%W])
    w.writerow(['両側＝CSP中心x=139.45のてこ比で分担（左%.3f・右%.3f）しC点に作用。片側全荷重＝D04-003、全荷重がCSP重心（収納 d=%.2f h=%.2f／使用 d=%.2f h=%.2f）に作用'%(share['左'],share['右'],*G_CSP['収納'],*G_CSP['使用'])])
    w.writerow(['引抜き＝板を梁から離す向き（ねじの引張）。1本抜け＝1本ずつ外した最悪値（A04-009）。必要耐力＝1本抜けの値×安全率4（A04-007）。ねじの圧縮側も弾性で扱う（引抜きは大きめに出る）'])
    w.writerow([])
    w.writerow(['側','位置','分担','荷重ケース','地震の向き','ねじ本数','引抜き','せん断','引抜き(1本抜け)','せん断(1本抜け)','必要引抜き耐力','必要せん断耐力'])
    w.writerows(rows)
print(out)
import collections
for r in rows:
    if r[5]==6: print(r)
