# K050 二重スコットラッセルのずらし量の計算表（STEP4 4-2、姿勢保持案1）
# 取付点C・C′はCSP中心の高さ(h=255.885)の水平線上で、CSP側面の外形内（弦23.43：d=50.02〜73.44）に置く。
# 配置α：C=CSP中心、C′=C+Δd（Δd≦11.7）。配置β：CSP中心の両側に±Δd/2（Δd≦23.4）。
# 各配置で、2組の機構（O-A-B-C／O′-A′-B′-C′）を41姿勢で障害物に当て、リンクどうしの側面図上の交差も調べる。
import math, csv, io, json, subprocess
a=50.0; CS_H=255.885; STROKE=72.16; t0=268-CS_H; DC=61.73
CSP0=[(48.50,252.47),(68.05,243.77),(74.96,259.30),(55.41,268.00)]
CH_L,CH_R=50.02,73.44
def pose(Od,s):
    oc=t0+STROKE*s; C=(Od,268-oc); ph=math.asin(oc/(2*a)); B=(Od+2*a*math.cos(ph),268.0); A=((B[0]+C[0])/2,(B[1]+C[1])/2)
    return ph,A,B,C
def cspoly(s): dv=-STROKE*s; return [(p[0],p[1]+dv) for p in CSP0]
def dps(p,a_,b):
    ax,ay=b[0]-a_[0],b[1]-a_[1]; t=max(0,min(1,((p[0]-a_[0])*ax+(p[1]-a_[1])*ay)/(ax*ax+ay*ay)))
    return math.hypot(p[0]-a_[0]-t*ax,p[1]-a_[1]-t*ay)
def crs(a_,b,c,d):
    f=lambda p,q,r:(q[0]-p[0])*(r[1]-p[1])-(q[1]-p[1])*(r[0]-p[0])
    return f(a_,b,c)*f(a_,b,d)<0 and f(c,d,a_)*f(c,d,b)<0
def dss(a_,b,c,d): return 0.0 if crs(a_,b,c,d) else min(dps(a_,c,d),dps(b,c,d),dps(c,a_,b),dps(d,a_,b))
SCC=[(20.5,236.5),(33.9,236.5),(33.9,250),(20.5,250)]
OBS={'掘込前壁(d=45.5)':[((45.5,250),(45.5,270))],'天井端(h=250)':[((0,250),(45.5,250))],
     'SCケース':[(SCC[i],SCC[(i+1)%4]) for i in range(4)]}
light=lambda d:161+(d-25)*56/280
CONF=[('α',6),('α',9),('α',11.7),('β',12),('β',18),('β',23)]
rows=[]; detail={}
for cf,dd in CONF:
    d1,d2=(DC,DC+dd) if cf=='α' else (DC-dd/2,DC+dd/2)
    mins={}; cross_pairs=set()
    def upd(k,v,s):
        if k not in mins or v<mins[k][0]: mins[k]=(v,s)
    for i in range(41):
        s=i/40; P1=pose(d1,s); P2=pose(d2,s)
        L={'OA':(( d1,268),P1[1]),'BC':(P1[2],P1[3]),"O′A′":((d2,268),P2[1]),"B′C′":(P2[2],P2[3])}
        for nm,(p,q) in L.items():
            for on,segs in OBS.items():
                upd((nm,on),min(dss(p,q,*g) for g in segs),s)
            lv=min(q_[1]-light(q_[0]) for q_ in (p,q,((p[0]+q[0])/2,(p[1]+q[1])/2)) if q_[0]>=25)
            upd((nm,'投射光上端面(鉛直)'),lv,s)
        for n1,n2 in (('OA',"B′C′"),('BC',"O′A′"),('OA',"O′A′"),('BC',"B′C′")):
            v=dss(*L[n1],*L[n2]); upd((n1+'↔'+n2,'リンクどうし'),v,s)
    ps,_,Bs,_=pose(d2,0); pu,_,Bu,_=pose(d1,1)
    rail=(pose(d2,0)[2][0]+6)-(pose(d1,1)[2][0]-6)
    detail[(cf,dd)]=mins
    lk=min(v for (n,o),(v,s) in mins.items() if o!='リンクどうし')
    lkn=[ (n,o) for (n,o),(v,s) in mins.items() if o!='リンクどうし' and v==lk][0]
    rows.append([cf,dd,'%.2f'%d1,'%.2f'%d2,'%.2f'%(d1-45.5),'%.2f'%(CH_R-d2 if cf=='α' else min(d1-CH_L,CH_R-d2)),
        '%.2f'%lk,'%s↔%s'%lkn,
        '%.2f'%mins[('OA↔B′C′','リンクどうし')][0],'%.2f'%mins[('BC↔O′A′','リンクどうし')][0],
        '%.2f'%mins[('OA↔O′A′','リンクどうし')][0],'%.2f'%mins[('BC↔B′C′','リンクどうし')][0],
        '%.1f'%(pose(d1,1)[2][0]-6),'%.1f'%(pose(d2,0)[2][0]+6),'%.1f'%rail])
hdr=['配置','Δd','O・C のd','O′・C′ のd','Oと掘込前壁(d=45.5)の間','C/C′とCSP外形の余裕',
     '障害物との最小クリアランス','その組合せ','OA↔B′C′ 最小','BC↔O′A′ 最小','OA↔O′A′ 最小','BC↔B′C′ 最小','レール左端d','レール右端d','レール長']
buf=io.StringIO(); w=csv.writer(buf)
w.writerow(['■ K050 二重スコットラッセルのずらし量（STEP4 4-2、姿勢保持案1）。a=50、O・O′はh=268、Bキャリッジ共有。側面図(d-h)で線（太さ0）として判定。0は側面図で交差＝別のx面に置く必要あり'])
w.writerow(hdr)
for r in rows: w.writerow(r)
TS=subprocess.run(['date','+%y%m%d%H%M'],capture_output=True,text=True,env={'TZ':'Asia/Tokyo'}).stdout.strip()
open('/tmp/k050_rows.json','w').write(json.dumps({'ts':TS,'hdr':hdr,'rows':rows}))
print(buf.getvalue())
open('/tmp/k050.csv','w',encoding='utf-8-sig').write(buf.getvalue())
