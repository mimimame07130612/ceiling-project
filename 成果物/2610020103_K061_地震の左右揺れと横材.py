# K061 地震の左右揺れへの対策：左右の架台をつなぐ横材（STEP4 4-3）
# 使用位置で地震の左右揺れ（LC3、±x）を受けたときのねじ1本の引抜き力を、
#   (0) 現状：左右の架台がそれぞれ単独で梁にねじ止め
#   (1) 案1：左右の架台を横材でつなぎ、1つの剛な枠として両方の梁にねじ止め
# で比べる。横材は架台のSC側の端（d≈55、照明d=130を避ける）、掘込面の近く（h≈266〜270）に置く仮定。横材は剛（仮）。
# 地震の強さはA04-006の KH=2.0（上層階）のほか、1.5・1.0 でも計算（KVはKH/2とする：A04-006の比、仮）。
# 計算：架台（または枠）を剛体、ねじをばね（引抜き方向とせん断方向に同じばね定数、仮）として6自由度の釣り合いを解く。
#       ねじは押し込み側も弾性で扱う（K057と同じ）。1本抜け＝1本ずつ外した最悪値（A04-009、依頼主判断で重ねる）。安全率4（A04-007）。
# 荷重の分担・作用点はK057の「両側」と同じ（左右のてこ比でC点に作用、固定部品3.0kg/片側は仮）。
import math, csv, subprocess, numpy as np
TS=subprocess.run(['date','+%y%m%d%H%M'],capture_output=True,text=True,env={'TZ':'Asia/Tokyo'}).stdout.strip()
exec(open('/tmp/k057.py',encoding='utf-8').read().split('rows=[]')[0])
def scr3(sn,k):
    s=SIDES[sn]; out_=-1 if sn=='左' else +1   # 梁が板のどちら側か（左：梁はx<89.5 → 引きはがし=+x、ねじは梁へ−x向きに引く）
    return [((s['xb'],d,h),sn) for d,h in screws(s,k)]
def solve3(scrs,loads):
    # 剛体の6自由度：u=(ux,ud,uh,rx,rd,rh)。各ねじは点pで3方向のばね（k=1）。
    K=np.zeros((6,6)); F=np.zeros(6)
    ref=np.mean([p for p,_ in scrs],axis=0)
    def Bm(p):
        r=np.array(p)-ref
        # 変位 = u_t + rot × r
        return np.array([[1,0,0,0,r[2],-r[1]],[0,1,0,-r[2],0,r[0]],[0,0,1,r[1],-r[0],0]])
    for p,_ in scrs: B=Bm(p); K+=B.T@B
    for p,f in loads:
        r=np.array(p)-ref; f=np.array(f,float); F[:3]+=f; F[3:]+=np.cross(r,f)
    u=np.linalg.solve(K,F)
    res=[]
    for p,sn in scrs:
        dsp=Bm(p)@u   # ねじが受ける変位＝板の動き（ねじの力は −dsp）
        pull=dsp[0]*(1 if sn=='左' else -1)   # 板が梁から離れる量＝引抜き
        res.append((pull,math.hypot(dsp[1],dsp[2])))
    return res
def worst(scrs,loads):
    r0=solve3(scrs,loads); t1=v1=0
    for j in range(len(scrs)):
        r=solve3(scrs[:j]+scrs[j+1:],loads); t1=max(t1,max(a for a,b in r)); v1=max(v1,max(b for a,b in r))
    return max(a for a,b in r0),max(b for a,b in r0),t1,v1
TIE_D=48.0
rows=[]
for KH in (2.0,1.5,1.0):
    KV=KH/2
    for k in (3,4):
        best={}
        for hx in (1,-1):
            ld={}
            for sn,s in SIDES.items():
                Wl=W*share[sn]; Pfix=((s['xb']+s['xl'])/2,(s['d0']+s['d1'])/2,262.0)
                ld[sn]=[((s['xl'],s['Od'],H_C['使用']),(hx*KH*Wl,0,-(1+KV)*Wl)),(Pfix,(hx*KH*MF,0,-(1+KV)*MF))]
            # (0) 単独
            for sn in SIDES:
                r=worst(scr3(sn,k),ld[sn]); key=('(0) 現状（単独）',sn)
                best[key]=[max(x,y) for x,y in zip(best.get(key,[0]*4),r)]
            # (1) 横材でつないだ枠
            scrs=scr3('左',k)+scr3('右',k); r=worst(scrs,ld['左']+ld['右'])
            # 側ごとの最大を出すため個別に評価
            for sn in SIDES:
                r0=solve3(scrs,ld['左']+ld['右']); t=max(a for (a,b),(p,s_) in zip(r0,scrs) if s_==sn); v=max(b for (a,b),(p,s_) in zip(r0,scrs) if s_==sn)
                t1=v1=0
                for j in range(len(scrs)):
                    sub=scrs[:j]+scrs[j+1:]; rr=solve3(sub,ld['左']+ld['右'])
                    t1=max(t1,max(a for (a,b),(p,s_) in zip(rr,sub) if s_==sn)); v1=max(v1,max(b for (a,b),(p,s_) in zip(rr,sub) if s_==sn))
                key=('(1) 案1 横材でつなぐ',sn)
                best[key]=[max(x,y) for x,y in zip(best.get(key,[0]*4),(t,v,t1,v1))]
        for (cn,sn),v in best.items():
            rows.append([KH,cn,sn,2*k]+[round(x) for x in v]+[round(v[2]*4),round(v[3]*4)])
out='/mnt/user-data/outputs/%s_K061_地震の左右揺れと横材.csv'%TS
with open(out,'w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f)
    w.writerow(['K061 地震の左右揺れ（使用位置、両側で支える状態）と横材によるねじの力（ねじ1本あたり、N）'])
    w.writerow(['(0) 左右の架台が単独。(1) 左右の架台を横材（SC側端 d≈%.0f、剛・仮）でつないだ1つの枠。KVはKH/2（仮）。荷重の分担・作用点はK057の両側と同じ。'%TIE_D])
    w.writerow(['剛体＋ねじのばね（引抜き・せん断同じばね定数、仮）。押し込み側も弾性。1本抜けは重ねる（依頼主判断）。必要耐力＝1本抜けの値×安全率4'])
    w.writerow([])
    w.writerow(['KH','構成','側','ねじ本数(片側)','引抜き','せん断','引抜き(1本抜け)','せん断(1本抜け)','必要引抜き耐力','必要せん断耐力'])
    w.writerows(rows)
for r in rows: print(r)
print(out)
