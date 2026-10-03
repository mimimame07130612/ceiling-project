# K095 駆動まわりの実寸配置（修正案：支持側なし・ナットをLP側へ3cm・スペーサー0.5）（左側の部分詳細、STEP4 4-3）
# K094からの変更（依頼主了承）：(1) 支持側サポートユニットGBF10をなくし、ねじ軸は固定側GBK10だけで支える（SC側の端は自由端）。
#   (2) ナットをBからLP側へ3cmずらしてブロックに付ける。(3) GBK10とモーターを架台の面から0.5浮かせる（スペーサー、仮）。
# 部屋を含まない部分詳細（F7 d）。梁は描かず、梁の側面（x=89.5）・下面（h=254.5）・掘込面（h=270）を破線で示すだけ。
# 寸法（根拠）：モーター PKP268D42A2（56.4角、L=92.5、軸φ8：オリエンタルモーター V-228）、固定側サポートユニット GBK10（THK BK10互換：L25・B60・H39・軸高さ22、
#   モノタロウ掲載のBK10寸法）、支持側 GBF10（同、L20とする：仮）、ねじ Tr14×3、ナット 外径22・長さ30（仮）、カップリング 外径25・長さ25（仮）、
#   モーター取付板 厚10（仮）、レール HSR20 580、ブロック HSR20C（K087）。リンク（25角）は K085 の幾何（O d=52.0・h=265、a=50）。
import subprocess, math
TS=subprocess.run(['date','+%y%m%d%H%M'],capture_output=True,text=True,env={'TZ':'Asia/Tokyo'}).stdout.strip()
PF=90.3; SP=0.5; AX=PF+SP+2.2; HS=259.2; NOFF=3.0           # ねじ軸 x（BK10の軸高さ22）、h
O=(52.0,265.0); a=50.0
def pose(ph):
    p=math.radians(ph); B=(O[0]+2*a*math.cos(p),O[1]); C=(O[0],O[1]-2*a*math.sin(p)); A=((B[0]+C[0])/2,(B[1]+C[1])/2); return A,B,C
R0,R1=99.54,157.54; Bu,Bs=105.83,151.25
BK=(158.0,160.5); BF=None; SCR0=105.0; CP=(161.0,163.5); MB=(164.0,165.0); MO=(165.0,174.25)
NUT_R=1.1; NUT_L=3.0; MOT=5.64
# すき間の計算
def seg_dist(p,a_,b_):
    ax,ay=a_; bx,by=b_; px,py=p; dx,dy=bx-ax,by-ay; t=max(0,min(1,((px-ax)*dx+(py-ay)*dy)/(dx*dx+dy*dy))); return math.hypot(px-(ax+t*dx),py-(ay+t*dy))
Ast,Bst,Cst=pose(7.0); Aus,Bus,Cus=pose(57.4)
# BF10（d97〜99、h256.2〜262.2、x〜94.2）と収納時のリンク（x 93.5〜96）：dh方向の最短距離（リンクの中心線から矩形まで）−リンクの半幅
def rect_seg_gap(r,s0,s1):
    d0,d1,h0,h1=r; best=1e9
    for k in range(201):
        t=k/200; p=(s0[0]+(s1[0]-s0[0])*t, s0[1]+(s1[1]-s0[1])*t)
        dx=max(d0-p[0],0,p[0]-d1); dy=max(h0-p[1],0,p[1]-h1); best=min(best,math.hypot(dx,dy))
    return best-1.25
nut_u=(Bus[0]+NOFF-NUT_L/2,Bus[0]+NOFF+NUT_L/2,HS-NUT_R,HS+NUT_R); nut_s=(Bst[0]+NOFF-NUT_L/2,Bst[0]+NOFF+NUT_L/2,HS-NUT_R,HS+NUT_R)
g3=min(rect_seg_gap(nut_u,Bus,Cus),rect_seg_gap(nut_u,O,Aus)); g4=min(rect_seg_gap(nut_s,Bst,Cst),rect_seg_gap(nut_s,O,Ast))
scr_end=(SCR0-0.2,SCR0,HS-0.7,HS+0.7); g5=min(rect_seg_gap(scr_end,O,Ast),rect_seg_gap(scr_end,Bst,Cst))
chk=[('使用時のナット（B＋3cm）とリンク（d-h面内、x方向は93.5〜94.1で重なる）',round(g3,2)),
     ('収納時のナット（B＋3cm）とリンク（同上）',round(g4,2)),
     ('ねじ軸のSC側の端（d=105、x 92.3〜93.7）と収納時のリンク（d-h面内）',round(g5,2)),
     ('モーターの角と梁の側面（x方向）',round((AX-MOT/2)-89.5,2)),
     ('ナットの外周と架台の面（x方向）',round((AX-NUT_R)-PF,2)),
     ('ナットの外周とリンクの面（x方向、負＝x方向では重なる）',round(93.5-(AX+NUT_R),2)),
     ('ナットの上端とブロックの下端（h方向）',round((265-3.15)-(HS+NUT_R),2)),
     ('収納時のナットのLP側の端とGBK10（d方向）',round(BK[0]-(Bst[0]+NOFF+NUT_L/2),2)),
     ('モーターの後端の位置 d（架台の端 d≈165 から片持ち）',round(MO[1],2))]
for c in chk: print(c)
# ---- 描画 ----
o=[]; W_,H_=1300,1120
def T(x,y,s,c='#222',an='start',sz=12,b=False): o.append('<text x="%.1f" y="%.1f" font-size="%d" fill="%s" text-anchor="%s"%s>%s</text>'%(x,y,sz,c,an,' font-weight="bold"' if b else '',s))
# 側面
S=6.5; D0,D1,H0,H1=40,180,250,272; OX,OY=50,170
gx=lambda d:OX+(d-D0)*S; gy=lambda h:OY+(H1-h)*S
def R2(d0,d1,h0,h1,f,st,op=1,dash=False): o.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" fill-opacity="%s" stroke="%s"%s/>'%(gx(d0),gy(h1),(d1-d0)*S,(h1-h0)*S,f,op,st,' stroke-dasharray="5,3"' if dash else ''))
def L2(p,q,c,w,dash=False,op=1): o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%.1f" stroke-opacity="%s"%s/>'%(gx(p[0]),gy(p[1]),gx(q[0]),gy(q[1]),c,w,op,' stroke-dasharray="6,4"' if dash else ''))
T(OX,OY-30,'(1) 側面（+x方向を見る、d-h）：左の架台','#111','start',13,True)
for h in (254.5,270): L2((D0,h),(D1,h),'#aaa',1,True)
T(gx(D1),gy(270)-4,'掘込面 h=270','#999','end',10); T(gx(D1),gy(254.5)+12,'梁の下面 h=254.5','#999','end',10)
for d in range(40,181,10): T(gx(d),gy(H0)+14,str(d),'#777','middle',10)
R2(46,166.0,254.5,270,'#5F5E5A','#5F5E5A',0.12)
R2(R0,R1,264,266,'#555','#222',0.7)
for b in (Bu,Bs): R2(b-3.7,b+3.7,261.85,268.15,'#D85A30','#8a3a1d',0.35); R2(b+NOFF-NUT_L/2,b+NOFF+NUT_L/2,HS-NUT_R,HS+NUT_R,'#9b6fc0','#5b2f80',0.7)
R2(SCR0,BK[1]+1.0,HS-0.7,HS+0.7,'#bbb','#555',0.9)
R2(BK[0],BK[1],HS-3.0,HS+3.0,'#888','#333',0.7)
R2(CP[0],CP[1],HS-1.25,HS+1.25,'#aaa','#333',0.7); R2(MB[0],MB[1],HS-3.5,HS+3.5,'#666','#333',0.7); R2(MO[0],MO[1],HS-MOT/2,HS+MOT/2,'#E6A23C','#a06b10',0.5)
o.append('<clipPath id="sideclip"><rect x="%.1f" y="%.1f" width="%.1f" height="%.1f"/></clipPath><g clip-path="url(#sideclip)">'%(gx(D0),gy(H1),(D1-D0)*S,(H1-H0)*S))
for (A_,B_,C_),col,lab in (((Ast,Bst,Cst),'#2C6FB0','収納'),((Aus,Bus,Cus),'#1D9E75','使用')):
    L2(O,A_,col,2.5*S*0.9,False,0.45); L2(B_,C_,col,2.5*S*0.9,False,0.45)
o.append('</g>')
T(gx(SCR0),gy(HS-0.7)+12,'(ねじ軸のSC側の端：支持なし)','#555','middle',10)
T(gx(BK[0]),gy(HS+3.0)-4,'(固定側GBK10)','#333','middle',10)
T(gx((MO[0]+MO[1])/2),gy(HS+MOT/2)-4,'(モーター56.4角×92.5)','#a06b10','middle',10)
T(gx(70),gy(255.5),'(青：収納時のリンク／緑：使用時のリンク)','#2C6FB0','start',10)
# 正面断面（モーター位置）と（GBF10位置）
S2=22; X0,X1=88,98; HH0,HH1=252,271
for k,(ttl,oy) in enumerate((('(2) 正面断面：モーターの位置（d≈170）','m'),('(3) 正面断面：使用時のナットの位置（d≈109）','b'))):
    ox=60+k*620; oy2=430
    fx=lambda x,ox=ox:ox+(x-X0)*S2; fy=lambda h:oy2+(HH1-h)*S2
    T(ox,oy2-30,ttl,'#111','start',13,True)
    def R(x0,x1,h0,h1,f,st,op=1,dash=False): o.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" fill-opacity="%s" stroke="%s"%s/>'%(fx(x0),fy(h1),(x1-x0)*S2,(h1-h0)*S2,f,op,st,' stroke-dasharray="5,3"' if dash else ''))
    o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#999" stroke-dasharray="5,3"/>'%(fx(89.5),fy(HH1),fx(89.5),fy(HH0)))
    T(fx(89.5)-4,fy(HH1)+10,'梁の側面 x=89.5','#999','end',10)
    for h in (254.5,270): o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#bbb" stroke-dasharray="5,3"/>'%(fx(X0),fy(h),fx(X1),fy(h)))
    for x in range(88,99): T(fx(x),fy(HH0)+14,str(x),'#777','middle',10)
    for h in (255,260,265,270): T(fx(X0)-4,fy(h)+4,str(h),'#777','end',10)
    if ttl.startswith('(2)'):
        R(AX-MOT/2,AX+MOT/2,HS-MOT/2,HS+MOT/2,'#E6A23C','#a06b10',0.5)
        R(PF-0.8,PF,254.5,270,'none','#5F5E5A',0,True)
        T(fx(PF)+4,fy(268),'(架台はモーターの下まで延ばせない：破線)','#5F5E5A','start',10)
        o.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#ddd" stroke="#333"/>'%(fx(AX),fy(HS),0.4*S2))
        T(fx(AX),fy(HS-MOT/2)+16,'(モーター56.4角、軸 x=%.1f・h=%.1f)'%(AX,HS),'#a06b10','middle',11)
    else:
        R(89.5,PF,254.5,270,'#5F5E5A','#333',0.6)
        R(PF,PF+1.8,264,266,'#555','#222',0.8)
        R(PF+0.4,PF+3.0,261.85,268.15,'#D85A30','#8a3a1d',0.4)
        o.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#9b6fc0" stroke="#5b2f80"/>'%(fx(AX),fy(HS),NUT_R*S2))
        o.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#ddd" stroke="#333"/>'%(fx(AX),fy(HS),0.7*S2))
        R(93.5,96.0,263.75,266.25,'#1D9E75','#0f5f45',0.3,True)
        T(fx(96.0)+4,fy(265)+4,'(リンク：Bのピン付近、d≈106。ナットはd≈109)','#0f5f45','start',10)
        T(fx(AX+NUT_R)+4,fy(HS)+4,'(ナット φ22、軸 x=%.1f)'%AX,'#5b2f80','start',10)
yy=900
T(50,yy,'すき間（cm、負は重なり）','#111','start',12,True)
for i,(k,v) in enumerate(chk): T(50,yy+18*(i+1),'%s：%.2f'%(k,v),'#C0392B' if v<0.5 else '#222','start',11)
note=['K095 駆動まわりの実寸配置（修正案：支持側なし・ナットをLP側へ3cm・スペーサー0.5、左側の部分詳細）　作成 %s'%TS,
 '部屋を含まない部分詳細（F7 d）。寸法：PKP268D42A2（V-228）、BK10互換（モノタロウ掲載寸法）。ナット外径22・カップリング外径25・取付板厚10・スペーサー0.5は仮。支持側サポートユニットは置かない。',
 '数値の根拠：K085（リンク面・機構の幾何）、K086（Bの位置）、K087（レール・ブロック）。右側は同じ配置をd方向に+18ずらしたもの。']
for i,t in enumerate(note): T(40,30+i*20,t,'#111','start',14 if i==0 else 12,i==0)
svg='<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" font-family="Noto Sans CJK JP, Yu Gothic, sans-serif"><rect width="100%%" height="100%%" fill="white"/>%s</svg>'%(W_,H_,W_,H_,''.join(o))
out='/mnt/user-data/outputs/%s_K095_駆動まわりの実寸配置_修正案.svg'%TS
open(out,'w',encoding='utf-8').write(svg); print(out)
