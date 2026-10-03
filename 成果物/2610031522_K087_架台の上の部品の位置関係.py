# K087 架台の上の部品の位置関係（側面図の部分詳細、左右の架台、STEP4 4-3）
# 部屋を含まない部分詳細（F7 d）。梁は描かず、梁の下面（h=254.5）と掘込面（h=270）を破線の目盛りで示すだけにする。
# 描くもの（すべて仮）：架台（鋼板厚8、h=254.5〜270、左 d=46〜166.0・右 d=46〜184.0）、THK HSR20C レール580（幅20、h=264〜266、Bの動く範囲の中央に置く）、
#   ブロック（長さ74・幅63、h=261.85〜268.15）の使用位置・収納位置と動く範囲、梁のねじ M2（K086、頭径11.2：若井産業 Xポイントビス）、
#   Oのピロボール PHS8EC（球の外径22、IKO）、モーター（K056の仮の箱 8×8、d方向にd−0.73）。
# 位置：O 左52.0・右70.0（h=265）、B使用 左105.83・右123.83、B収納 左151.25・右169.25（K086）。
import subprocess
TS=subprocess.run(['date','+%y%m%d%H%M'],capture_output=True,text=True,env={'TZ':'Asia/Tokyo'}).stdout.strip()
HB=265.0; RL=58.0; BL=7.4; BW=6.3; RW=2.0; HR=0.56; HLO,HUP=257.0,267.6
S={'左':dict(O=52.0,Bu=105.83,Bs=151.25,d1=165.99,mot=(157.99-0.73,165.99-0.73)),
   '右':dict(O=70.0,Bu=123.83,Bs=169.25,d1=183.99,mot=(175.99-0.73,183.99-0.73))}
for sn,s in S.items():
    c=(s['Bu']+s['Bs'])/2; s['rail']=(c-RL/2,c+RL/2); s['zone']=(s['Bu']-BL/2,s['Bs']+BL/2)
    z0,z1=s['zone']; o=s['O']
    s['scr']=[(o,HUP),(o,HLO),(z0-1.5,HUP),(z1+1.5,HUP),(s['Bu']-5,HLO),(s['Bu']+5,HLO),(s['Bs']-5,HLO),(s['Bs']+5,HLO)]
    s['chk']=[('レールのLP側の端とモーター',round(s['mot'][0]-s['rail'][1],2)),
              ('LP側の上のねじ（頭）とモーター',round(s['mot'][0]-(z1+1.5+HR),2)),
              ('SC側の上のねじ（頭）とブロックが動く範囲',round(z0-(z0-1.5+HR),2)),
              ('上のねじ（頭の下端）とレールの上端',round((HUP-HR)-(HB+RW/2),2)),
              ('下のねじ（頭の上端）とブロックの下端',round((HB-BW/2)-(HLO+HR),2)),
              ('ピロボール（球の上端）と掘込面',round(270-(HB+1.1),2))]
    print(sn,s['rail'],s['zone'],s['chk'])
D0,D1,H0,H1=40,190,250,272; SC=7.0; ML=50; PT=[150,150+(H1-H0)*SC+190]
Wd=int(ML+(D1-D0)*SC+40); Ht=int(PT[1]+(H1-H0)*SC+260)
o=[]
def X(d): return ML+(d-D0)*SC
def Y(p,h): return PT[p]+(H1-h)*SC
def rect(p,d0,d1,h0,h1,fill,stroke,op=1,dash=False,w=1):
    o.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" fill-opacity="%s" stroke="%s" stroke-width="%s"%s/>'%(X(min(d0,d1)),Y(p,max(h0,h1)),abs(d1-d0)*SC,abs(h1-h0)*SC,fill,op,stroke,w,' stroke-dasharray="5,3"' if dash else ''))
def circ(p,d,h,r,fill,stroke,dash=False):
    o.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="%s"%s/>'%(X(d),Y(p,h),r*SC,fill,stroke,' stroke-dasharray="4,2"' if dash else ''))
def line(p,d0,h0,d1,h1,c,w=1,dash=False):
    o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"%s/>'%(X(d0),Y(p,h0),X(d1),Y(p,h1),c,w,' stroke-dasharray="5,3"' if dash else ''))
def text(p,d,h,s,c='#222',a='start',sz=11,dy=0,x=None):
    o.append('<text x="%.1f" y="%.1f" font-size="%d" fill="%s" text-anchor="%s">%s</text>'%(X(d) if x is None else x,Y(p,h)+dy,sz,c,a,s))
for p,sn in enumerate(('左','右')):
    s=S[sn]
    text(p,D0,H1,'%s側の架台（+x方向を見る側面図、d-h）'%sn,'#111','start',13,-10)
    for h in (254.5,270): line(p,D0,h,D1,h,'#aaa',1,True)
    text(p,D1,270,'掘込面 h=270','#999','end',10,-3); text(p,D1,254.5,'梁の下面 h=254.5','#999','end',10,12)
    for d in range(40,191,10): line(p,d,H0,d,H0+0.3,'#999'); text(p,d,H0,str(d),'#777','middle',9,12)
    for h in (255,260,265,270): text(p,D0,h,str(h),'#777','end',9,3,X(D0)-4)
    rect(p,46,s['d1'],254.5,270,'#5F5E5A','#5F5E5A',0.12)
    rect(p,s['zone'][0],s['zone'][1],HB-BW/2,HB+BW/2,'#D85A30','#D85A30',0.08,True)
    rect(p,s['rail'][0],s['rail'][1],HB-RW/2,HB+RW/2,'#555','#222',0.7)
    for b,lab in ((s['Bu'],'使用'),(s['Bs'],'収納')):
        rect(p,b-BL/2,b+BL/2,HB-BW/2,HB+BW/2,'#D85A30','#8a3a1d',0.45)
        o.append('<circle cx="%.1f" cy="%.1f" r="3" fill="#111"/>'%(X(b),Y(p,HB))); text(p,b,HB+BW/2,'(B %s d=%.1f)'%(lab,b),'#8a3a1d','middle',10,-4)
    rect(p,s['mot'][0],s['mot'][1],258,266,'#E6A23C','#a06b10',0.35,True); text(p,(s['mot'][0]+s['mot'][1])/2,258,'(モーター 仮)','#a06b10','middle',10,13)
    circ(p,s['O'],HB,1.1,'#1D9E75','#0f5f45'); text(p,s['O'],HB+1.1,'(O ピロボール φ22)','#0f5f45','middle',10,-4)
    for d,h in s['scr']: circ(p,d,h,HR,'#fff','#111')
    yb=Y(p,H0)+30
    for i,(k,v) in enumerate(s['chk']):
        o.append('<text x="%d" y="%.1f" font-size="11" fill="%s">%s：%s</text>'%(ML,yb+i*15,'#C0392B' if v<0.5 else '#222',k,('%.2f'%v)+('（重なり）' if v<0 else '')))
leg=[('#5F5E5A','架台（鋼板厚8）'),('#555','レール THK HSR20 580（幅20）'),('#D85A30','ブロック HSR20C（長さ74・幅63）、破線＝動く範囲、●＝Bのピン'),('#E6A23C','モーター（K056の仮の箱、位置未定）'),('#1D9E75','Oのピロボール IKO PHS8EC（球の外径22）'),('#111','○＝梁のねじ M2（K086、頭径11.2）')]
for i,(c,t) in enumerate(leg):
    yy=Ht-110+i*17; o.append('<rect x="%d" y="%d" width="14" height="10" fill="%s" fill-opacity="0.6"/>'%(ML,yy-9,c)); o.append('<text x="%d" y="%d" font-size="12">%s</text>'%(ML+20,yy,t))
note=['K087 架台の上の部品の位置関係（側面図の部分詳細）　作成 %s'%TS,
 '部屋を含まない部分詳細（F7 d）。梁は描かず、梁の下面と掘込面を破線で示す。前提はすべて仮：レール580は動く範囲の中央、モーターは位置未定の仮の箱。',
 '数値の根拠：K086（ねじ配置M2、O・Bの位置）、THKカタログ HSR20C、IKO PHS8EC、若井産業 Xポイントビス。図の下の数字はすき間（cm、負は重なり）。']
for i,t in enumerate(note): o.append('<text x="%d" y="%d" font-size="%d"%s>%s</text>'%(ML,30+i*20,14 if i==0 else 12,' font-weight="bold"' if i==0 else '',t))
svg='<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" font-family="Noto Sans CJK JP, Yu Gothic, sans-serif"><rect width="100%%" height="100%%" fill="white"/>%s</svg>'%(Wd,Ht,Wd,Ht,''.join(o))
out='/mnt/user-data/outputs/%s_K087_架台の上の部品の位置関係.svg'%TS
open(out,'w',encoding='utf-8').write(svg); print(out)
