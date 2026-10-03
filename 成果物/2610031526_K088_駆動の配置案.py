# K088 駆動（台形ねじ）の配置案（左側、正面断面と側面の部分詳細、STEP4 4-3）
# 部屋を含まない部分詳細（F7 d）。梁は描かない（梁の側面・下面・掘込面の位置を破線で示すだけ）。
# 配置案：台形ねじ軸をレールの下（h≈259.2）に、レールと平行に置く。ナットは丸ナット（フランジなし）を受け金具に入れ、受け金具はブロックの下側のフランジに下から留める。
#   ねじ軸はLP側の端で支持ユニット（固定側）→カップリング→モーター、SC側の端は支持ユニット（支持側）。
# 寸法（すべて仮）：
#   架台 鋼板厚8（x=89.5〜90.3）、THK HSR20C：レール幅20・高さ18、ブロック 高さM=30・幅63・長さ74・ブロック下面はレール取付面から4（K=26）。
#   リンク（25角）中心 x=94.75、Bのピン h=265（K085）。梁のねじ頭 径11.2・高さ4（仮）、下の列 h=257（K086 M2）。
#   台形ねじ Tr12（軸径1.2）、丸ナット 外径2.2・長さ3.0（一般的な寸法の目安、モノタロウの品番の寸法で要確認）。
#   支持ユニット 3×3×2.5（d方向2.5、仮）、カップリング 径2.5・長さ2.5（仮）、モーター 5.7角・長さ8（減速機付きを想定、仮）。
# 位置：B使用 d=105.83、B収納 d=151.25、レール580 d=99.54〜157.54（K087）。
import subprocess, math
TS=subprocess.run(['date','+%y%m%d%H%M'],capture_output=True,text=True,env={'TZ':'Asia/Tokyo'}).stdout.strip()
PL0,PL1=89.5,90.3; RH=1.8; KB=0.4; MH=3.0; BW=6.3; HB=265.0; RW=2.0; LK=2.5; XL=94.75
XS,HS=92.0,259.2; RS=0.6; RN=1.1; HLO=257.0; HR=0.56; HH=0.4
Bu,Bs=105.83,151.25; R0,R1=99.54,157.54; NL=3.0
SUP=(R1+0.5,R1+3.0); CPL=(SUP[1]+0.2,SUP[1]+2.7); MOT=(CPL[1]+0.2,CPL[1]+8.2); SUP0=(R0-3.0,R0-0.5)
chk=[('ナット外周と架台の面（x方向）',round((XS-RN)-PL1,2)),
     ('ナット外周と下の列のねじ頭（角）',round(math.hypot(XS-(PL1+HH),HS-(HLO+HR))-RN,2)),
     ('ナットの上端とブロックの下端（受け金具の入る高さ）',round((HB-BW/2)-(HS+RN),2)),
     ('ナットの外周とリンク（x方向）',round((XL-LK/2)-(XS+RN),2)),
     ('モーターの下端と梁の下面（h=254.5）',round((HS-2.85)-254.5,2)),
     ('LP側の上のねじ（d=156.45）頭と支持ユニット',round(SUP[0]-(156.45+HR),2)),
     ('下の列のねじ（B収納+5、d=156.25）頭と支持ユニット',round(SUP[0]-(156.25+HR),2)),
     ('SC側の上のねじ（d=100.63）頭と支持ユニット（SC側）',round((100.63-HR)-SUP0[1],2)),
     ('架台のLP側の端（今 d=166.0）とモーターの端',round(166.0-MOT[1],2))]
for c in chk: print(c)
o=[]; W_,H_=1250,1330
def T(x,y,s,c='#222',a='start',sz=12,b=False): o.append('<text x="%.1f" y="%.1f" font-size="%d" fill="%s" text-anchor="%s"%s>%s</text>'%(x,y,sz,c,a,' font-weight="bold"' if b else '',s))
# ---- 正面断面（x-h）
S1=30; X0,H1=87.5,271.5; OX,OY=60,170
def fx(x): return OX+(x-X0)*S1
def fy(h): return OY+(H1-h)*S1
def R(x0,x1,h0,h1,fill,st,op=1,dash=False):
    o.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" fill-opacity="%s" stroke="%s"%s/>'%(fx(min(x0,x1)),fy(max(h0,h1)),abs(x1-x0)*S1,abs(h1-h0)*S1,fill,op,st,' stroke-dasharray="5,3"' if dash else ''))
def C(x,h,r,fill,st,dash=False): o.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="%s"%s/>'%(fx(x),fy(h),r*S1,fill,st,' stroke-dasharray="4,2"' if dash else ''))
def Lf(x0,h0,x1,h1,c='#999',dash=True): o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s"%s/>'%(fx(x0),fy(h0),fx(x1),fy(h1),c,' stroke-dasharray="5,3"' if dash else ''))
T(OX,OY-40,'(1) 正面断面（LP側からSC側を見る、x-h）：Bの位置で切った断面','#111','start',13,True)
for h in (254.5,270): Lf(X0,h,98.5,h)
T(fx(98.5),fy(270)-4,'掘込面 h=270','#999','end',10); T(fx(98.5),fy(254.5)+12,'梁の下面 h=254.5','#999','end',10)
Lf(89.5,252.5,89.5,271.5); T(fx(89.5)-4,fy(271.5)+10,'梁1の側面 x=89.5','#999','end',10)
for x in range(88,99): Lf(x,252.2,x,252.5,'#999',False); T(fx(x),fy(252.2)+14,str(x),'#777','middle',10)
for h in range(255,272,5): T(fx(X0)-4,fy(h)+4,str(h),'#777','end',10)
R(PL0,PL1,254.5,270,'#5F5E5A','#333',0.6)
R(PL1,PL1+RH,HB-RW/2,HB+RW/2,'#555','#222',0.8)
R(PL1+KB,PL1+MH,HB-BW/2,HB+BW/2,'#D85A30','#8a3a1d',0.45)
R(XL-LK/2,XL+LK/2,HB-LK/2,HB+LK/2,'#1D9E75','#0f5f45',0.45); C(XL,HB,0.25,'#111','#111')
R(PL1,PL1+HH,HLO-HR,HLO+HR,'#fff','#111')
R(XS-RN+0.1,XS+RN,HS+RN,HB-BW/2,'none','#7b4aa0',1,True)
C(XS,HS,RN,'#9b6fc0','#5b2f80'); C(XS,HS,RS,'#ddd','#333')
T(fx(XS),fy(HS-RN)+14,'(台形ねじ Tr12・丸ナット φ22)','#5b2f80','middle',11)
T(fx(XS+RN)+4,fy(HB-BW/2)+18,'(受け金具：ブロック下側のフランジに下から留める)','#7b4aa0','start',11)
T(fx(PL1+MH)+4,fy(HB+BW/2)-4,'(ブロック HSR20C 幅63)','#8a3a1d','start',11)
T(fx(XL+LK/2)+4,fy(HB)+4,'(リンク25角・Bのピン)','#0f5f45','start',11)
T(fx(PL1+HH)+4,fy(HLO)+14,'(梁のねじ 下の列 h=257)','#111','start',11)
# ---- 側面（d-h）
S2=6.0; D0,D1,H0,HH1=95,180,252,271; OX2,OY2=60,860
def gx(d): return OX2+(d-D0)*S2
def gy(h): return OY2+(HH1-h)*S2
def R2(d0,d1,h0,h1,fill,st,op=1,dash=False):
    o.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" fill-opacity="%s" stroke="%s"%s/>'%(gx(d0),gy(h1),(d1-d0)*S2,(h1-h0)*S2,fill,op,st,' stroke-dasharray="5,3"' if dash else ''))
T(OX2,OY2-30,'(2) 側面（+x方向を見る、d-h）：左の架台のLP側','#111','start',13,True)
for h in (254.5,270): o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#aaa" stroke-dasharray="5,3"/>'%(gx(D0),gy(h),gx(D1),gy(h)))
for d in range(95,181,5): T(gx(d),gy(H0)+14,str(d),'#777','middle',10)
R2(D0,166.0,254.5,270,'#5F5E5A','#5F5E5A',0.12); R2(166.0,MOT[1]+1,254.5,270,'none','#5F5E5A',0,True)
T(gx(MOT[1]+1),gy(254.5)+26,'(架台を延ばす範囲)','#5F5E5A','end',10)
R2(R0,R1,HB-RW/2,HB+RW/2,'#555','#222',0.7)
for b in (Bu,Bs): R2(b-3.7,b+3.7,HB-BW/2,HB+BW/2,'#D85A30','#8a3a1d',0.4); R2(b-NL/2,b+NL/2,HS-RN,HS+RN,'#9b6fc0','#5b2f80',0.6)
R2(SUP0[0],R1+3.0,HS-RS,HS+RS,'#bbb','#555',0.9)
R2(SUP0[0],SUP0[1],HS-1.5,HS+1.5,'#888','#333',0.6); R2(SUP[0],SUP[1],HS-1.5,HS+1.5,'#888','#333',0.6)
R2(CPL[0],CPL[1],HS-1.25,HS+1.25,'#aaa','#333',0.6); R2(MOT[0],MOT[1],HS-2.85,HS+2.85,'#E6A23C','#a06b10',0.5)
for d,h in ((100.63,267.6),(156.45,267.6),(100.83,257),(110.83,257),(146.25,257),(156.25,257)):
    o.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#fff" stroke="#111"/>'%(gx(d),gy(h),HR*S2))
T(gx((SUP0[0]+SUP0[1])/2),gy(HS+1.5)-4,'(支持ユニット)','#333','middle',10); T(gx((SUP[0]+SUP[1])/2),gy(HS+1.5)-4,'(支持ユニット)','#333','middle',10)
T(gx((MOT[0]+MOT[1])/2),gy(HS+2.85)-4,'(モーター 5.7角・減速機付き 仮)','#a06b10','middle',10)
T(gx(Bu),gy(HB+BW/2)-4,'(B使用)','#8a3a1d','middle',10); T(gx(Bs),gy(HB+BW/2)-4,'(B収納)','#8a3a1d','middle',10)
# 数値
yy=OY2+(HH1-H0)*S2+50
T(OX2,yy,'すき間（cm、負は重なり）','#111','start',12,True)
for i,(k,v) in enumerate(chk): T(OX2,yy+18*(i+1),'%s：%.2f'%(k,v),'#C0392B' if v<0.5 else '#222','start',11)
note=['K088 駆動（台形ねじ）の配置案（左側の部分詳細）　作成 %s'%TS,
 '部屋を含まない部分詳細（F7 d）。前提はすべて仮：台形ねじTr12・丸ナット・支持ユニット・カップリング・モーターの寸法は一般的な目安で、モノタロウの品番では未確認。',
 '数値の根拠：K085・K086・K087（リンク面、B・O・ねじの位置、レール580）、THKカタログ HSR20C。右側は同じ配置をd方向に+18ずらしたものになる。']
for i,t in enumerate(note): T(40,30+i*20,t,'#111','start',14 if i==0 else 12,i==0)
svg='<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" font-family="Noto Sans CJK JP, Yu Gothic, sans-serif"><rect width="100%%" height="100%%" fill="white"/>%s</svg>'%(W_,H_,W_,H_,''.join(o))
out='/mnt/user-data/outputs/%s_K088_駆動の配置案.svg'%TS
open(out,'w',encoding='utf-8').write(svg); print(out)
