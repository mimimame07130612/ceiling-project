# K046 水平・鉛直版リンクの干渉（STEP4 4-2、直線版スコットラッセル：Bは水平、Cは鉛直）
# 直線版（OA=AB=AC=a、O=経路の延長上 h=268、Bは経路に直角な直線上をすべる）のリンク・レール・CSPを、
# 収納→使用の全行程で障害物（天井端・掘込前壁・掘込面・SCケース・投射光上端面・視線上端）に当てる。
# 計算表 K047 を同時に出力する。使用位置は鉛直移動のため d1=48.5（収納と同じ）、最下点は光束上端面との間2から h=171.61。
# 入力：A03-004〜006（wR=0で作図）、A01-001、A01-003、A02-002、A00-004、D01-001、D05-001、K039/K040の機構の置き方
import json, math, subprocess, glob, csv, io
TS=subprocess.run(['date','+%y%m%d%H%M'],capture_output=True,text=True,env={'TZ':'Asia/Tokyo'}).stdout.strip()
N44='K046_水平鉛直版リンクの干渉'; N45='K047_水平鉛直版リンクの干渉計算表'
CSP=sorted(glob.glob('*_csp.py'))[-1]; SAN=sorted(glob.glob('*_sanmen.py'))[-1]
OUTJ='/mnt/user-data/outputs/%s_%s.json'%(TS,N44); OUTS='/mnt/user-data/outputs/%s_%s.svg'%(TS,N44)
OUTC='/mnt/user-data/outputs/%s_%s.csv'%(TS,N45)
XC=139.45; D1S,HS=48.5,243.77; D1U,HU=48.5,171.61
subprocess.run(['python3',CSP,'json','-o','/tmp/c.json','--pose','収納,%s,%s,%s'%(XC,D1S,HS),'--pose','使用,%s,%s,%s'%(XC,D1U,HU)],check=True,capture_output=True)
C0=json.load(open('/tmp/c.json',encoding='utf-8'))
side=[it['p'] for it in C0['items'] if it['t']=='poly']
cs=[sum(p[0] for p in side[0])/4,sum(p[1] for p in side[0])/4]
cu=[sum(p[0] for p in side[1])/4,sum(p[1] for p in side[1])/4]
L=math.hypot(cu[0]-cs[0],cu[1]-cs[1]); uc=((cu[0]-cs[0])/L,(cu[1]-cs[1])/L)
us=(-uc[1],uc[0]) if -uc[1]>0 else (uc[1],-uc[0])
HO=268.0; t0=(HO-cs[1])/(-uc[1]); O=(cs[0]-uc[0]*t0,HO)
def pose(a,s):
    ocd=t0+L*s; phi=math.asin(ocd/(2*a)); Cp=(O[0]+uc[0]*ocd,O[1]+uc[1]*ocd)
    ob=2*a*math.cos(phi); Bp=(O[0]+us[0]*ob,O[1]+us[1]*ob); Ap=((Bp[0]+Cp[0])/2,(Bp[1]+Cp[1])/2)
    return phi,Ap,Bp,Cp
def csp_poly(s):
    d1=D1S+(D1U-D1S)*s; hl=HS+(HU-HS)*s
    return [[p[0]+(d1-D1S),p[1]+(hl-HS)] for p in side[0]]
# ---- 幾何 ----
def dps(p,a,b):
    ax,ay=b[0]-a[0],b[1]-a[1]; t=max(0,min(1,((p[0]-a[0])*ax+(p[1]-a[1])*ay)/(ax*ax+ay*ay)))
    return math.hypot(p[0]-a[0]-t*ax,p[1]-a[1]-t*ay)
def cross(a,b,c,d):
    f=lambda p,q,r:(q[0]-p[0])*(r[1]-p[1])-(q[1]-p[1])*(r[0]-p[0])
    return f(a,b,c)*f(a,b,d)<0 and f(c,d,a)*f(c,d,b)<0
def dss(a,b,c,d):
    if cross(a,b,c,d): return 0.0
    return min(dps(a,c,d),dps(b,c,d),dps(c,a,b),dps(d,a,b))
def edges(poly): return [(poly[i],poly[(i+1)%len(poly)]) for i in range(len(poly))]
def inside(p,poly):
    n=0
    for a,b in edges(poly):
        if (a[1]>p[1])!=(b[1]>p[1]) and p[0]<a[0]+(p[1]-a[1])*(b[0]-a[0])/(b[1]-a[1]): n+=1
    return n%2==1
def d_seg_poly(a,b,poly):
    if inside(a,poly) or inside(b,poly): return 0.0
    return min(dss(a,b,c,d) for c,d in edges(poly))
# 障害物（側面図 d-h）
SCC=[[20.5,236.5],[33.9,236.5],[33.9,250],[20.5,250]]
OBS={
 '天井端(h=250,d=0〜45.5)':('seg',[(0,250),(45.5,250)]),
 '掘込前壁(d=45.5)':('seg',[(45.5,250),(45.5,270)]),
 '掘込面(h=270)':('seg',[(45.5,270),(302.5,270)]),
 'SCケース':('poly',SCC),
}
PJ=(305,217); SCT=(25,161); EYE=(270,100)
def below_line(p,a,b):   # 境界線(a→b)より下にいる量（+で侵入）と上側のすき間
    h=a[1]+(p[0]-a[0])*(b[1]-a[1])/(b[0]-a[0]); ang=math.atan2(b[1]-a[1],b[0]-a[0])
    return (p[1]-h)*math.cos(ang)
def clr_boundary(segpts,a,b,dmin):
    v=[]
    for p in segpts:
        if dmin<=p[0]<=max(a[0],b[0]): v.append(below_line(p,a,b))
    return min(v) if v else None
def sample(a,b,n=20): return [(a[0]+(b[0]-a[0])*i/n,a[1]+(b[1]-a[1])*i/n) for i in range(n+1)]
def clear_all(parts):
    res={}
    for nm,(k,g) in OBS.items():
        m=1e9
        for a,b in parts:
            m=min(m,dss(a,b,*g) if k=='seg' else d_seg_poly(a,b,g))
        res[nm]=m
    pts=[q for a,b in parts for q in sample(a,b)]
    res['投射光上端面']=clr_boundary(pts,SCT,PJ,25)
    res['視線上端']=clr_boundary(pts,SCT,EYE,25)
    return res
AS=(45,50,55,60); NS=41
rows=[]; summ={}
for a in AS:
    worst={}
    for i in range(NS):
        s=i/(NS-1); phi,Ap,Bp,Cp=pose(a,s)
        parts={'OAリンク':[(O,Ap)],'ロッドBC':[(Bp,Cp)],'CSP本体':edges(csp_poly(s))}
        for pn,segs in parts.items():
            r=clear_all(segs)
            for k,v in r.items():
                if v is None: continue
                key=(pn,k)
                if key not in worst or v<worst[key][0]: worst[key]=(v,s)
        rows.append([a,round(s,3),round(math.degrees(phi),1),round(2*math.degrees(phi) if phi<math.pi/4 else 180-2*math.degrees(phi),1),
                     round(Ap[0],1),round(Ap[1],1),round(Bp[0],1),round(Bp[1],1),round(Cp[0],1),round(Cp[1],1)])
    # レール（固定）
    _,_,Bu,_=pose(a,1); _,_,Bs,_=pose(a,0)
    ob_u=math.hypot(Bu[0]-O[0],Bu[1]-O[1]); ob_s=math.hypot(Bs[0]-O[0],Bs[1]-O[1])
    R0=(O[0]+us[0]*(ob_u-6),O[1]+us[1]*(ob_u-6)); R1=(O[0]+us[0]*(ob_s+6),O[1]+us[1]*(ob_s+6))
    r=clear_all([(R0,R1)])
    for k,v in r.items():
        if v is not None: worst[('Bレール(固定)',k)]=(v,None)
    summ[a]=(worst,R0,R1)
# ---- 計算表 K045 ----
buf=io.StringIO(); w=csv.writer(buf)
w.writerow(['■ K047 水平・鉛直版リンクの干渉計算表（STEP4 4-2）。O=(d=%.2f,h=%.2f)固定、Cの経路は水平から%.2f°、Bのすべる直線はLP側へ%.2f°下がる。wR=0で作図'%(O[0],O[1],math.degrees(math.atan2(-uc[1],-uc[0]) if uc[0]<0 else math.atan2(-uc[1],uc[0])),math.degrees(math.atan2(-us[1],us[0])))])
w.writerow(['第1表 部品ごとの最小クリアランス（全行程41姿勢、単位cm。負は侵入）'])
w.writerow(['リンク長a','部品','障害物','最小クリアランス','発生位置s（0=収納,1=使用）'])
for a in AS:
    for (pn,k),(v,s) in sorted(summ[a][0].items()):
        w.writerow([a,pn,k,'%.2f'%v,'-' if s is None else '%.3f'%s])
w.writerow([]); w.writerow(['第2表 姿勢ごとのリンク位置（φ：Bでのロッドとすべる直線の角、μ：伝達角＝∠OABの補角の小さい方）'])
w.writerow(['リンク長a','s','φ(°)','μ(°)','A_d','A_h','B_d','B_h','C_d','C_h'])
for r_ in rows: w.writerow(r_)
w.writerow([]); w.writerow(['第3表 収納時・使用時の機構の位置（梁下面h=254.5との比較）'])
w.writerow(['リンク長a','収納 A_h','収納 B_h','収納 C_h','収納の機構最下点h','梁下面からの余裕','使用φ(°)','使用の余裕(90°−φ)','収納μ(°)','B収納d','B使用d','レール長(両端+6)'])
for a in AS:
    ps,As,Bs,Cs=pose(a,0); pu,Au,Bu,Cu=pose(a,1); _,R0,R1=summ[a]
    lo=min(As[1],Bs[1],Cs[1],O[1])
    w.writerow([a,'%.2f'%As[1],'%.2f'%Bs[1],'%.2f'%Cs[1],'%.2f'%lo,'%.2f'%(lo-254.5),'%.1f'%math.degrees(pu),'%.1f'%(90-math.degrees(pu)),'%.1f'%(2*math.degrees(ps)),'%.1f'%Bs[0],'%.1f'%Bu[0],'%.1f'%math.hypot(R1[0]-R0[0],R1[1]-R0[1])])
open(OUTC,'w',encoding='utf-8-sig').write(buf.getvalue())
# ---- 図 K044（a=50） ----
A_SEL=50
items=[]
for it in C0['items']:
    if it['t']=='poly' and it['view']=='side': it2=dict(it); it2['op']=0.12; items.append(it2)
    if it['t'] in ('rect',): items.append(it)
r2=lambda p:[round(p[0],2),round(p[1],2)]
# 障害物
items.append(dict(t='poly',view='side',p=SCC,color='#7B4FA0',fill='#7B4FA0',op=0.2,w=1.4))
items.append(dict(t='text',view='side',p=[27,243],s='SCケース',anchor='middle',color='#7B4FA0'))
items.append(dict(t='line',view='side',p=[list(SCT),list(PJ)],color='#D85A30',w=1.2,dash=True))
items.append(dict(t='text',view='side',p=[200,193],s='投射光上端面',color='#D85A30'))
items.append(dict(t='line',view='side',p=[list(SCT),list(EYE)],color='#6A5FD0',w=1.2,dash=True))
items.append(dict(t='text',view='side',p=[150,130],s='視線上端',color='#6A5FD0'))
items.append(dict(t='line',view='side',p=[[40,254.5],[330,254.5]],color='#8a857a',w=1.0,dash=True))
items.append(dict(t='text',view='side',p=[330,254.5],s='梁下面h=254.5（リンクのxは梁の外）',dx=-2,dy=12,anchor='end',color='#8a857a'))
# 途中姿勢（薄い灰）
for i in range(1,8):
    s=i/8; _,Ap,Bp,Cp=pose(A_SEL,s)
    items.append(dict(t='line',view='side',p=[r2(O),r2(Ap)],color='#aaaaaa',w=1.0))
    items.append(dict(t='line',view='side',p=[r2(Bp),r2(Cp)],color='#aaaaaa',w=1.0))
    items.append(dict(t='poly',view='side',p=[r2(q) for q in csp_poly(s)],color='#aaaaaa',fill='none',op=0,w=0.6))
# Aの軌跡（円弧）
items.append(dict(t='line',view='side',p=[r2(pose(A_SEL,i/40)[1]) for i in range(41)],color='#2E9E6B',w=1.0,dash=True))
for s,col,tag in ((0,'#2C6FB0','収'),(1,'#C0392B','使')):
    _,Ap,Bp,Cp=pose(A_SEL,s)
    items.append(dict(t='line',view='side',p=[r2(O),r2(Ap)],color=col,w=2.6))
    items.append(dict(t='line',view='side',p=[r2(Bp),r2(Cp)],color=col,w=1.8,dash=True))
    for q,nm in ((Ap,'A'),(Bp,'B'),(Cp,'C')):
        items.append(dict(t='pt',view='side',p=r2(q),color=col,r=3.0))
        items.append(dict(t='text',view='side',p=r2(q),s='%s(%s)'%(nm,tag),dx=5,dy=(13 if tag=='収' else 13),color=col))
_,R0,R1=summ[A_SEL]
items.append(dict(t='line',view='side',p=[r2(R0),r2(R1)],color='#111',w=3.2))
items.append(dict(t='text',view='side',p=r2(R1),s='Bレール(固定)',dx=4,dy=4,color='#111'))
items.append(dict(t='pt',view='side',p=r2(O),color='#111',r=5,ring=True))
items.append(dict(t='text',view='side',p=r2(O),s='O 固定(d=%.1f,h=268)'%O[0],dx=8,dy=-12,color='#111'))
# 最小クリアランスの注記
W50=summ[A_SEL][0]
def g(pn,k): return W50[(pn,k)][0]
# 正面図：左右リンクx
for xx,nm,col in ((110.9,'左リンク x=110.9','#2C6FB0'),(168.0,'右リンク x=168.0','#C0392B')):
    items.append(dict(t='line',view='front',p=[[xx,165],[xx,270]],color=col,w=1.4,dash=True))
    items.append(dict(t='text',view='front',p=[xx,205],s=nm,dx=(-4 if xx<140 else 4),anchor=('end' if xx<140 else 'start'),color=col))
items.append(dict(t='text',view='front',p=[169,262],s='梁2内面まで2',dx=2,color='#C0392B'))
def mn(pn): 
    v=[(vv[0],k) for (p,k),vv in W50.items() if p==pn]; return min(v)
notes=[
 'STEP4 4-2（直線版スコットラッセル・水平鉛直版）：a=OA=AB=AC=50、O=(d=%.1f,h=268)固定、Bは水平（h=268）にすべり、Cは鉛直に下がる。CSPは真下に降りる（使用d1=48.5、最下点h=171.61）。青＝収納・赤＝使用・灰＝途中7姿勢。太実線＝OAリンク、破線＝ロッドBC、黒太＝Bレール。'%O[0],
 '全行程41姿勢の最小クリアランス（a=50）：OAリンク %.1f（%s）／ロッドBC %.1f（%s）／Bレール %.1f（%s）／CSP本体 %.1f（%s）。数値はK047。'%(mn('OAリンク')+mn('ロッドBC')+mn('Bレール(固定)')+mn('CSP本体')),
 'リンク・レールは部品を線（太さ0）として判定。部品の太さ・スライダの大きさ・保持具はまだ入っていない（すき間はこの値から太さの半分ずつ減る）。',
 '収納時はA・B・Cとも梁下面h=254.5より上（第3表）。使用位置はA03-005（d1=33）よりLP側へ15.5・上へ3.1。'+' 正面図：左右リンクのx位置（wR=0で作図）。右リンクと梁2内面の間は2（c3）。wRが決まるとCSPごと左へ寄る（A03-004）。',
]
ov=dict(title_note=notes,legend=C0['legend']+[
  dict(text='青／赤：OAリンク（収納／使用）　破線：ロッドBC',color='#2C6FB0',kind='line'),
  dict(text='灰：途中姿勢（リンク・CSP）／緑破線：Aの軌跡',color='#aaaaaa',kind='line'),
  dict(text='黒太：Bレール（固定）',color='#111',kind='line'),
  dict(text='紫：SCケース／橙破線：投射光上端面／青紫破線：視線上端',color='#7B4FA0',kind='band')],
  src=['A03-004〜006','A01-001','A01-003','A02-002','A00-004','D01-001','D05-001'],items=items)
json.dump(ov,open(OUTJ,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
subprocess.run(['python3',SAN,'--zuban','K046','--title','水平鉛直版リンクの干渉','-o',OUTS,OUTJ],check=True)
print(TS)
for a in AS:
    print('--- a=%d'%a)
    for (pn,k),(v,s) in sorted(summ[a][0].items(), key=lambda x:x[1][0])[:8]: print('  %s ↔ %s : %.2f  s=%s'%(pn,k,v,s))
print('O',O,'uc',uc,'us',us,'t0',t0,'L',L)
