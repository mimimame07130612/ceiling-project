# K060 片側故障後に残った側のねじの力（STEP4 4-3、K059の続き）
# 片側の一重故障（6部品＋架台＋架台のねじ、駆動系は落下止めで別扱い）が起きたあと、残った側の架台を梁に止めるねじ1本の力を求める。
# 故障の結果（K059）：
#   ・(c) C・ロッドA–C間・架台の破断（収納時は(b) B・ロッドB–A間も同じ）：全荷重が残った側へ移り、CSPは残った側のCまわりに90°回ってぶら下がる。
#       回り切った最下点での振り子の力を見る。動的係数 f＝1＋2r²/(k²＋r²)（静止から放した剛体振り子の最下点、軸の力/重さ）。
#       r＝回転軸から重心まで9（Δd/2）、k＝CSPの断面の回転半径（仮、CSP外形の箱で近似）。荷重は残った側のリンク面（C点）に鉛直、
#       CSP重心のx位置（139.45）がリンク面から離れているぶんのねじり（ロール）を含めるため、力の作用点はx=139.45、d＝残った側のC、h＝C。
#   ・(a) O・OA・Aの破断：分担は健全時と同じ（左右のてこ比）。収納時はロッドが寝ているため、壊れた側のロッドが残った側のCを
#       d方向に押す（K059：LC1で615N、荷重に比例させる）。使用時48N。
#   ・(b) 使用時：鎖が58.5°で止まり、残った側84N（K059）。(c)に包含されるため別に計算しない。
#   ・架台のねじ1本の破断：K057「両側」の1本抜けと同じ（参考に再掲）。
# 安全率（故障後）と「1本抜け」を重ねるかは未決のため、組み合わせを並べる（安全率1.0・1.5・2.0、参考に4）。
# その他の前提・計算方法はK057と同じ（ねじ2列×各列k本、固定部品3.0kg/片側は仮、弾性分布）。地震は重ねない（依頼主判断）。
import math, csv, subprocess, json
TS=subprocess.run(['date','+%y%m%d%H%M'],capture_output=True,text=True,env={'TZ':'Asia/Tokyo'}).stdout.strip()
exec(open('/tmp/k057.py',encoding='utf-8').read().split('rows=[]')[0])
# 動的係数
hb,db=17.0,21.4   # CSP外形の断面（H×D、A01-001）で回転半径を近似（仮）
k2=(hb**2+db**2)/12; r=9.0; FDYN=1+2*r*r/(k2+r*r)
HF={'収納':615.0,'使用':48.0}   # K059（LC1）の壊れた側ロッドが残った側Cを押す水平力
def resp(s,k,loads):
    scr=screws(s,k); t,v=solve(scr,loads,s); t1=v1=0
    for j in range(len(scr)):
        a,b=solve(scr[:j]+scr[j+1:],loads,s); t1=max(t1,a); v1=max(v1,b)
    return t,v,t1,v1
rows=[]
for sn,s in SIDES.items():   # sn＝残った側
    Pfix=((s['xb']+s['xl'])/2,(s['d0']+s['d1'])/2,262.0)
    for pos in ('収納','使用'):
        hC=H_C[pos]
        for lc in ('LC1','LC2'):
            Wl=W+(CAT if lc=='LC2' else 0)
            cases=[('(c) 全荷重が移り、揺れて止まる（収納時の(b)を含む）','動的係数%.2f'%FDYN,[((XC,s['Od'],hC),(0,0,-FDYN*Wl)),(Pfix,(0,0,-MF))]),
                   ('(a) O・OA・Aの破断','押す力 %.0fN'%(HF[pos]*Wl/W),[((s['xl'],s['Od'],hC),(0,-HF[pos]*Wl/W,-share[sn]*Wl)),(Pfix,(0,0,-MF))]),
                   ('(a) 同上（押す向き逆）','',[((s['xl'],s['Od'],hC),(0,HF[pos]*Wl/W,-share[sn]*Wl)),(Pfix,(0,0,-MF))]),
                   ('参考：架台のねじ1本の破断（両側、K057）','',[((s['xl'],s['Od'],hC),(0,0,-share[sn]*Wl)),(Pfix,(0,0,-MF))])]
            for cname,note,L in cases:
                for k in (3,4):
                    t,v,t1,v1=resp(s,k,L)
                    rows.append([sn,pos,lc,cname,note,2*k,round(t),round(v),round(t1),round(v1)])
out='/mnt/user-data/outputs/%s_K060_片側故障後に残った側のねじの力.csv'%TS
SFs=(1.0,1.5,2.0,4.0)
with open(out,'w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f)
    w.writerow(['K060 片側故障後に残った側のねじの力（ねじ1本あたり、N）'])
    w.writerow(['故障の結果はK059。全荷重が移る場合はCSPが90°回って止まる最下点の力（動的係数%.2f、r=9・k=%.1f、仮）。ねじり（ロール）を含めるため作用点x=139.45。地震は重ねない。'%(FDYN,math.sqrt(k2))])
    w.writerow(['ねじ2列（h=258・266.5）×各列k本、固定部品3.0kg/片側（仮）。W=%.1fN、LC2は猫5kg×2。必要耐力＝値×安全率（故障後の安全率は未決のため並記）'%W])
    w.writerow([])
    w.writerow(['残った側','位置','荷重ケース','破断する部品','備考','ねじ本数','引抜き','せん断','引抜き(1本抜け)','せん断(1本抜け)']+['必要引抜き 1本抜けなし×%.1f'%x for x in SFs]+['必要引抜き 1本抜けあり×%.1f'%x for x in SFs])
    for r_ in rows: w.writerow(r_+[round(r_[6]*x) for x in SFs]+[round(r_[8]*x) for x in SFs])
print(out, 'FDYN=%.2f'%FDYN)
# 要約：側・ねじ本数ごとの最大
import collections
M=collections.defaultdict(lambda:[0,0,0,0])
for r_ in rows:
    if r_[3].startswith('参考'): continue
    key=(r_[0],r_[5]); m=M[key]; M[key]=[max(m[0],r_[6]),max(m[1],r_[8]),max(m[2],r_[7]),max(m[3],r_[9])]
for kk,v in sorted(M.items()): print(kk,v)
for r_ in rows:
    if r_[5]==6 and r_[2]=='LC2': print(r_)
