# 室内三面図生成スクリプト
# 作成日時：2026年9月4日 06:21
# 出典：確定事項ファイル D00-001〜038 / 部屋.xlsx
# 注意：冒頭の定義部は確定事項ファイルの写しである。再生成の前に定義部と
#       確定事項ファイルを突き合わせること（最初に読むこと 6-6）。
# 使用法：python3 室内三面図.py YYMMDDhhmm 'YYYY年M月D日 HH:MM' F006 F007 F008

import sys
ts, dt = sys.argv[1], sys.argv[2]
FN = sys.argv[3:6]
assert len(FN)==3

# ===== 確定値（確定事項ファイル D00） =====
ROOM_X=(0.0,273.0)      # D00-001
ROOM_D=(0.0,348.0)      # D00-002
CEIL=250.0              # D00-003
REC_H=270.0             # D00-004
REC_X=(45.5,305.5)      # D00-005
REC_D=(45.5,302.5)      # D00-005
BEAM=[(79.0,89.3,'D00-006','梁1'),(170.0,180.3,'D00-007','梁2'),(261.0,271.3,'D00-008','梁3')]
BEAM_H=15.5             # D00-009
BEAM_BOT=254.5          # D00-010
LP_X=[(132.5,'D00-012'),(205.5,'D00-013')]
LP_D=270.0; LP_H=100.0
# ===== 部屋.xlsx（確定事項ファイル未登録） =====
C1_D=14.0; C1_X=(10.0,254.0); CUR_H=(2.0,227.0)
C2_X=14.0; C2_D=(17.0,174.0)
# ===== 仮置き（U05-001 暫定値） =====
SCX,SCD,SCH=146.0,20.0,100.0
SCW,SCHT=221.4,124.5
SC_X=(SCX-SCW/2,SCX+SCW/2); SC_H=(SCH-SCHT/2,SCH+SCHT/2)
PJX,PJD,PJH=146.0,305.0,217.0
AREA=(89.3,170.0)

# ===== CSP設置位置（D00-028〜038） =====
CSPW,CSPD,CSPH=57.1,21.4,17.0
CSP_D=(45.5,66.9)
CSP_USE=(171.3,188.3)
CSP_STO=(253.0,270.0)
CSPXC=141.45
CSP_X=(CSPXC-CSPW/2,CSPXC+CSPW/2)
LIMF=lambda q:162.25+0.19211*(q-20.0)
CSPF='#f3ecf7'; CSPG='#eef5ee'

FIX='#2b2b2b'; PROV='#c0392b'; AREAC='#e8a33d'; BEAMC='#b9a179'; CURC='#4a7fb5'
S=1.5

def esc(t): return t.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

class Fig:
    def __init__(self,w0,w1,v0,v1,ml,mt,mr,mb,flipv):
        self.w0,self.w1,self.v0,self.v1=w0,w1,v0,v1
        self.ml,self.mt,self.flipv=ml,mt,flipv
        self.W=int((w1-w0)*S)+ml+mr; self.H=int((v1-v0)*S)+mt+mb
        self.o=[]
    def px(self,x): return self.ml+(x-self.w0)*S
    def py(self,v):
        return self.mt+(self.v1-v)*S if self.flipv else self.mt+(v-self.v0)*S
    def add(self,s): self.o.append(s)
    def rect(self,x1,x2,v1,v2,fill='none',stroke=FIX,sw=1.2,dash=None,op=1):
        a,b=self.px(x1),self.px(x2); c,d=self.py(v1),self.py(v2)
        x,y=min(a,b),min(c,d); w,h=abs(b-a),abs(d-c)
        ds=' stroke-dasharray="%s"'%dash if dash else ''
        self.add('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" fill-opacity="%s" stroke="%s" stroke-width="%s"%s/>'%(x,y,w,h,fill,op,stroke,sw,ds))
    def line(self,x1,v1,x2,v2,stroke=FIX,sw=1.2,dash=None,op=1):
        ds=' stroke-dasharray="%s"'%dash if dash else ''
        self.add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s" stroke-opacity="%s"%s/>'%(self.px(x1),self.py(v1),self.px(x2),self.py(v2),stroke,sw,op,ds))
    def txt(self,x,v,t,fs=10,fill=FIX,anc='start',dx=0,dy=0,w='normal'):
        self.add('<text x="%.1f" y="%.1f" font-family="sans-serif" font-size="%s" font-weight="%s" fill="%s" text-anchor="%s">%s</text>'%(self.px(x)+dx,self.py(v)+dy,fs,w,fill,anc,esc(t)))
    def ptxt(self,px,py,t,fs=10,fill=FIX,anc='start',w='normal'):
        self.add('<text x="%.1f" y="%.1f" font-family="sans-serif" font-size="%s" font-weight="%s" fill="%s" text-anchor="%s">%s</text>'%(px,py,fs,w,fill,anc,esc(t)))
    def dot(self,x,v,r=3,fill=FIX):
        self.add('<circle cx="%.1f" cy="%.1f" r="%s" fill="%s"/>'%(self.px(x),self.py(v),r,fill))
    def hdim(self,x1,x2,ypx,lab,col=FIX,dash=None):
        a,b=self.px(x1),self.px(x2)
        ds=' stroke-dasharray="%s"'%dash if dash else ''
        self.add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="0.8"%s/>'%(a,ypx,b,ypx,col,ds))
        for p in (a,b):
            self.add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="0.8"/>'%(p,ypx-3,p,ypx+3,col))
        self.ptxt((a+b)/2,ypx-4,lab,9,col,'middle')
    def vdim(self,v1,v2,xpx,lab,col=FIX,dash=None):
        a,b=self.py(v1),self.py(v2)
        ds=' stroke-dasharray="%s"'%dash if dash else ''
        self.add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="0.8"%s/>'%(xpx,a,xpx,b,col,ds))
        for p in (a,b):
            self.add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="0.8"/>'%(xpx-3,p,xpx+3,p,col))
        self.add('<text x="%.1f" y="%.1f" font-family="sans-serif" font-size="9" fill="%s" text-anchor="middle" transform="rotate(-90 %.1f %.1f)">%s</text>'%(xpx-4,(a+b)/2,col,xpx-4,(a+b)/2,esc(lab)))
    def out(self,fno,title,proj,legend,notes):
        h=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d">'%(self.W,self.H,self.W,self.H)]
        h.append('<rect width="%d" height="%d" fill="#ffffff"/>'%(self.W,self.H))
        h.append('<defs><pattern id="hatch" width="7" height="7" patternTransform="rotate(45)" patternUnits="userSpaceOnUse"><line x1="0" y1="0" x2="0" y2="7" stroke="%s" stroke-width="2.2" stroke-opacity="0.45"/></pattern>'%AREAC)
        h.append('<marker id="ar" markerWidth="9" markerHeight="9" refX="8" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6 z" fill="%s"/></marker></defs>'%FIX)
        h.append('<text x="18" y="26" font-family="sans-serif" font-size="16" font-weight="bold" fill="%s">%s  %s</text>'%(FIX,fno,esc(title)))
        h.append('<text x="18" y="44" font-family="sans-serif" font-size="10" fill="#555">%s</text>'%esc(proj))
        h.append('<text x="%d" y="26" font-family="sans-serif" font-size="10" fill="#555" text-anchor="end">作成日時：%s</text>'%(self.W-18,dt))
        h.append('<text x="%d" y="44" font-family="sans-serif" font-size="11" font-weight="bold" fill="%s" text-anchor="end">単位：cm</text>'%(self.W-18,FIX))
        b=list(self.o)
        y=self.H-len(legend)*13-len(notes)*12-22
        b.append('<line x1="18" y1="%.1f" x2="%d" y2="%.1f" stroke="#bbb" stroke-width="0.8"/>'%(y-10,self.W-18,y-10))
        b.append('<text x="18" y="%.1f" font-family="sans-serif" font-size="10" font-weight="bold" fill="%s">凡例</text>'%(y+1,FIX))
        for i,(c,t) in enumerate(legend):
            b.append('<text x="60" y="%.1f" font-family="sans-serif" font-size="9.5" fill="%s">%s</text>'%(y+1+i*13,c,esc(t)))
        for i,t in enumerate(notes):
            b.append('<text x="18" y="%.1f" font-family="sans-serif" font-size="9" fill="#555">%s</text>'%(y+len(legend)*13+6+i*12,esc(t)))
        return '\n'.join(h+b)+'\n</svg>\n'

def axes(f,lab1,lab2,d1,d2):
    ox,oy=f.px(0),f.py(0)
    f.add('<circle cx="%.1f" cy="%.1f" r="4" fill="none" stroke="%s" stroke-width="1.4"/>'%(ox,oy,FIX))
    f.add('<circle cx="%.1f" cy="%.1f" r="1.6" fill="%s"/>'%(ox,oy,FIX))
    for lab,(dx,dy) in ((lab1,d1),(lab2,d2)):
        f.add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1.4" marker-end="url(#ar)"/>'%(ox,oy,ox+dx,oy+dy,FIX))
        f.add('<text x="%.1f" y="%.1f" font-family="sans-serif" font-size="13" font-weight="bold" fill="%s">%s+</text>'%(ox+dx*1.06+(4 if dx>0 else -2),oy+dy*1.06+(14 if dy>0 else -4),FIX,lab))
    f.ptxt(ox-8,oy-10,'原点',9,FIX,'end')

LEG_BASE=[(FIX,'実線・通常表記 ＝ 確定値（確定事項ファイル D00-xxx を併記）'),
          (PROV,'破線・括弧付き表記 ＝ 推定・仮置き値（D00-030／D00-031の指定値およびCSPのx方向位置）'),
          (CURC,'青実線 ＝ 部屋.xlsx の実測値（確定事項ファイル未登録）'),
          (AREAC,'橙ハッチ ＝ 機器設置エリア（梁1と梁2の間／D00-032）')]

# ================= F001 平面図 =================
f=Fig(-38,316,-38,362,86,86,64,205,False)
f.rect(*REC_X,*REC_D,fill='#f4f0e6',stroke='none')
f.rect(*ROOM_X,*ROOM_D,fill='none',stroke=FIX,sw=2)
f.rect(*REC_X,*REC_D,fill='none',stroke=FIX,sw=1.2)
f.rect(AREA[0],AREA[1],REC_D[0],REC_D[1],fill='url(#hatch)',stroke=AREAC,sw=1.4)
for a,b,i,n in BEAM:
    f.rect(a,b,REC_D[0],REC_D[1],fill=BEAMC,stroke=FIX,sw=1,op=0.75)
    f.txt((a+b)/2,REC_D[0],n,9,'#5a4a2a','middle',0,-6)
    f.txt((a+b)/2,REC_D[1],i,8,'#5a4a2a','middle',0,12)
f.line(C1_X[0],C1_D,C1_X[1],C1_D,CURC,2.4)
f.txt(C1_X[0],C1_D,'カーテン1',9,CURC,'start',4,-6)
f.line(C2_X,C2_D[0],C2_X,C2_D[1],CURC,2.4)
f.add('<text x="%.1f" y="%.1f" font-family="sans-serif" font-size="9" fill="%s" transform="rotate(-90 %.1f %.1f)" text-anchor="middle">カーテン2</text>'%(f.px(C2_X)-6,f.py(sum(C2_D)/2),CURC,f.px(C2_X)-6,f.py(sum(C2_D)/2)))
f.line(SC_X[0],SCD,SC_X[1],SCD,PROV,2.6,'7,4')
f.txt(SC_X[0],SCD,'(SC 100型 幅221.4)',9.5,PROV,'start',0,14)
f.dot(SCX,SCD,3,PROV)
f.line(SCX,SCD,SCX,PJD,PROV,0.9,'2,4')
f.dot(PJX,PJD,4,PROV)
f.txt(PJX,PJD,'(PJ レンズ x=146 d=305)',9.5,PROV,'middle',0,32)
f.line(PJX,PJD,SC_X[0],SCD,PROV,0.8,'3,5',0.6)
f.line(PJX,PJD,SC_X[1],SCD,PROV,0.8,'3,5',0.6)
for x,i in LP_X:
    f.dot(x,LP_D,4,'#556677')
    f.txt(x,LP_D,'LP  '+i,9.5,'#334455','middle',0,-10)
f.hdim(0,273,f.py(ROOM_D[1])+34,'273  D00-001')
f.hdim(*REC_X,f.py(ROOM_D[1])+56,'45.5〜305.5  D00-005')
f.hdim(*AREA,f.py(ROOM_D[0])-18,'80.7 (89.3〜170.0)  設置エリア',AREAC)
f.hdim(BEAM[0][0],BEAM[1][0],f.py(ROOM_D[0])-40,'ピッチ 91.0')
f.vdim(0,348,f.px(0)-46,'348  D00-002')
f.vdim(REC_D[0],REC_D[1],f.px(0)-24,'45.5〜302.5  D00-005')
f.vdim(0,SCD,f.px(ROOM_X[1])+30,'(20)',PROV)
f.vdim(0,LP_D,f.px(ROOM_X[1])+52,'270  D00-012/013')
f.rect(CSP_X[0],CSP_X[1],CSP_D[0],CSP_D[1],CSPF,PROV,2.0,'7,4')
f.txt(CSPXC,CSP_D[1],'CSP',10,PROV,'middle',0,-7,'bold')
f.hdim(CSP_X[0],CSP_X[1],f.py(CSP_D[0])-16,'(57.1)  D00-028',PROV,'7,4')
f.vdim(CSP_D[0],CSP_D[1],f.px(CSP_X[0])-14,'21.4  D00-034')
f.txt(CSP_X[1],CSP_D[1],'(x=112.90〜170.00 中心141.45 上限値)',9,PROV,'end',0,16)
axes(f,'x','d',(74,0),(0,74))
open('/mnt/user-data/outputs/%s_%s_CSP設置位置平面図.svg'%(ts,FN[0]),'w',encoding='utf-8').write(
 f.out(FN[0],'CSP設置位置平面図','投影：−h方向を見た上面図（x−d平面）／原点を左上に置き x を右、d を下として描く',
 LEG_BASE+[('#556677','● ＝ 視聴位置 LP（D00-012／D00-013）')],
 ['注1：x=273 は仕切り壁ではなく壁が −d 方向へ折り返すコーナー（D00-001 備考）。あらわし梁領域はこれより右へ続く。',
  '注2：CSP・昇降機構の外形は未確定。本図には描いていない。',
  '注3：カーテンの寸法は部屋.xlsx の実測値だが確定事項ファイルに未登録のため D00 項番を併記できない。']))

# ================= F002 側面図 =================
f=Fig(-38,362,-30,300,90,86,64,205,True)
f.rect(REC_D[0],REC_D[1],CEIL,REC_H,fill='#f4f0e6',stroke='none')
f.line(*ROOM_D,0,0,FIX,2)
f.line(ROOM_D[0],0,ROOM_D[0],CEIL,FIX,2)
f.line(ROOM_D[1],0,ROOM_D[1],CEIL,FIX,2)
f.line(ROOM_D[0],CEIL,REC_D[0],CEIL,FIX,2)
f.line(REC_D[1],CEIL,ROOM_D[1],CEIL,FIX,2)
f.line(REC_D[0],CEIL,REC_D[0],REC_H,FIX,1.6)
f.line(REC_D[1],CEIL,REC_D[1],REC_H,FIX,1.6)
f.line(REC_D[0],REC_H,REC_D[1],REC_H,FIX,1.6)
f.txt(REC_D[0],CEIL,'垂れ壁',9,'#777','middle',0,14)
f.txt(REC_D[1],CEIL,'垂れ壁',9,'#777','middle',0,14)
f.rect(REC_D[0],REC_D[1],BEAM_BOT,REC_H,fill='url(#hatch)',stroke=AREAC,sw=1.4)
f.txt((REC_D[0]+REC_D[1])/2,BEAM_BOT,'設置エリア断面（x=146 は梁1・梁2の間のため梁は切られない）',9,'#9a6b1a','middle',0,16)
f.line(REC_D[0],BEAM_BOT,REC_D[1],BEAM_BOT,FIX,1.4,'6,3')
f.txt(REC_D[1],BEAM_BOT,'梁下面 h=254.5  D00-010',9,FIX,'end',-6,-5)
f.line(C1_D,CUR_H[0],C1_D,CUR_H[1],CURC,2.4)
f.txt(C1_D,CUR_H[1],'カーテン1',9,CURC,'middle',0,-6)
f.line(SCD,SC_H[0],SCD,SC_H[1],PROV,2.6,'7,4')
f.txt(SCD,SC_H[1],'(SC 高さ124.5)',9.5,PROV,'start',6,-5)
f.dot(SCD,SCH,3,PROV)
f.dot(PJD,PJH,4,PROV)
f.txt(PJD,PJH,'(PJ レンズ d=305 h=217)',9.5,PROV,'end',-8,-6)
f.line(PJD,PJH,SCD,SC_H[1],PROV,0.9,'3,5')
f.line(PJD,PJH,SCD,SC_H[0],PROV,0.9,'3,5')
f.txt(150,196,'(PJ 投射光路)',9,PROV,'middle',0,-4)
f.line(LP_D,LP_H,SCD,SC_H[1],'#556677',0.9,'1,4')
f.txt(150,128,'(LP 視線／SC上端)',9,'#556677','middle',0,-4)
f.line(LP_D,0,LP_D,LP_H,'#8899aa',1,'4,3')
f.dot(LP_D,LP_H,4,'#556677')
f.txt(LP_D,LP_H,'LP 眼高 h=100  D00-012/013',9.5,'#334455','middle',0,-10)
f.hdim(0,348,f.py(0)+34,'348  D00-002')
f.hdim(REC_D[0],REC_D[1],f.py(0)+56,'45.5〜302.5  D00-005')
f.hdim(SCD,PJD,f.py(REC_H)-26,'(投射距離 285.0)',PROV)
f.vdim(0,CEIL,f.px(0)-46,'250  D00-003')
f.vdim(0,REC_H,f.px(0)-24,'270  D00-004')
f.vdim(BEAM_BOT,REC_H,f.px(ROOM_D[1])+26,'15.5  D00-009')
f.vdim(SC_H[0],SC_H[1],f.px(0)+16,'(124.5)',PROV)
f.rect(CSP_D[0],CSP_D[1],CSP_USE[0],CSP_USE[1],CSPG,FIX,2.0)
f.txt((CSP_D[0]+CSP_D[1])/2,CSP_USE[1],'CSP 使用位置',9,FIX,'middle',0,-6)
f.rect(CSP_D[0],CSP_D[1],CSP_STO[0],CSP_STO[1],CSPG,FIX,2.0)
f.txt((CSP_D[0]+CSP_D[1])/2,CSP_STO[1],'CSP 収納位置',9,FIX,'middle',0,-6)
f.line(20.0,LIMF(20.0),300.0,LIMF(300.0),FIX,1.4,'2,3')
f.txt(300.0,LIMF(300.0),'干渉限界 D00-033',9,FIX,'end',0,-5)
f.vdim(CSP_USE[0],CSP_STO[0],f.px(CSP_D[1])+40,'81.7  D00-036')
f.vdim(CSP_USE[1],CSP_STO[0],f.px(CSP_D[1])+64,'64.7 水平時')
axes(f,'d','h',(74,0),(0,-74))
open('/mnt/user-data/outputs/%s_%s_CSP設置位置側面図.svg'%(ts,FN[1]),'w',encoding='utf-8').write(
 f.out(FN[1],'CSP設置位置側面図','投影：x=146 の断面を +x 方向に見た側面図（d−h平面）／d を右、h を上として描く',
 LEG_BASE[:3]+[(AREAC,'橙ハッチ ＝ 機器設置エリアの断面（梁下面〜掘り込み天井）'),('#556677','点線 ＝ LP から SC 上端への視線（仮置き値による）')],
 ['注1：x=146 は梁1（x=79.0〜89.3）と梁2（x=170.0〜180.3）の間にあたるため、本断面に梁は現れない。',
  '注2：カーテン2（x=14）は本断面より −x 側にあるため現れない。',
  '注3：CSP・昇降機構の外形および収納/下降ストロークは未確定。',
  '注4：PJ レンズ d=305 は梁領域後端 d=302.5 より 2.5 後方（垂れ壁より外）。']))

# ================= F003 正面図 =================
f=Fig(-38,316,-30,300,90,86,64,205,True)
f.rect(REC_X[0],REC_X[1],CEIL,REC_H,fill='#f4f0e6',stroke='none')
f.line(*ROOM_X,0,0,FIX,2)
f.line(ROOM_X[0],0,ROOM_X[0],CEIL,FIX,2)
f.line(ROOM_X[1],0,ROOM_X[1],CEIL,FIX,2)
f.line(ROOM_X[0],CEIL,REC_X[0],CEIL,FIX,2)
f.line(REC_X[0],CEIL,REC_X[0],REC_H,FIX,1.6)
f.line(REC_X[0],REC_H,REC_X[1],REC_H,FIX,1.6)
f.line(REC_X[1],CEIL,REC_X[1],REC_H,FIX,1.6)
f.line(ROOM_X[1],CEIL,REC_X[1],CEIL,FIX,1,'4,3')
f.rect(AREA[0],AREA[1],BEAM_BOT,REC_H,fill='url(#hatch)',stroke=AREAC,sw=1.4)
for a,b,i,n in BEAM:
    f.rect(a,b,BEAM_BOT,REC_H,fill=BEAMC,stroke=FIX,sw=1.1,op=0.85)
    f.txt((a+b)/2,REC_H,n,9,'#5a4a2a','middle',0,-6)
f.txt((AREA[0]+AREA[1])/2,BEAM_BOT,'設置エリア 80.7',9.5,'#9a6b1a','middle',0,15)
f.line(C1_X[0],CUR_H[1],C1_X[1],CUR_H[1],CURC,2.2)
f.line(C1_X[0],CUR_H[0],C1_X[0],CUR_H[1],CURC,1.4)
f.line(C1_X[1],CUR_H[0],C1_X[1],CUR_H[1],CURC,1.4)
f.txt(C1_X[0],CUR_H[1],'カーテン1 (x=10〜254 h=2〜227)',9,CURC,'start',4,-6)
f.line(C2_X,CUR_H[0],C2_X,CUR_H[1],CURC,2.4)
f.txt(C2_X,20,'カーテン2 (x=14)',9,CURC,'start',6,0)
f.rect(SC_X[0],SC_X[1],SC_H[0],SC_H[1],fill='#faeceb',stroke=PROV,sw=2.2,dash='7,4')
f.txt(SCX,SC_H[1],'(SC 100型 16:9  221.4 × 124.5)',10,PROV,'middle',0,-8)
f.dot(SCX,SCH,3.5,PROV)
f.txt(SCX,SCH,'(中心 x=146 h=100)',9,PROV,'middle',0,30)
f.dot(PJX,PJH,4,PROV)
f.txt(PJX,PJH,'(PJ レンズ x=146 h=217／d=305 奥)',9.5,PROV,'middle',0,-8)
f.line(PJX,PJH,SC_X[0],SC_H[1],PROV,0.8,'3,5',0.55)
f.line(PJX,PJH,SC_X[1],SC_H[1],PROV,0.8,'3,5',0.55)
for x,i in LP_X:
    f.dot(x,LP_H,3.2,'#556677')
    f.txt(x,LP_H,'LP %s (d=270 奥)'%i,8.5,'#334455','middle',0,-7)
f.hdim(0,273,f.py(0)+34,'273  D00-001')
f.hdim(*REC_X,f.py(0)+56,'45.5〜305.5  D00-005')
f.hdim(*AREA,f.py(REC_H)-40,'80.7  設置エリア（U05-004）',AREAC)
f.hdim(*SC_X,f.py(SC_H[0])+24,'(221.4)',PROV)
f.vdim(0,CEIL,f.px(0)-46,'250  D00-003')
f.vdim(0,REC_H,f.px(0)-24,'270  D00-004')
f.vdim(BEAM_BOT,REC_H,f.px(REC_X[1])+26,'15.5  D00-009')
f.vdim(SC_H[0],SC_H[1],f.px(SC_X[1])+18,'(124.5)',PROV)
f.rect(CSP_X[0],CSP_X[1],CSP_USE[0],CSP_USE[1],CSPF,PROV,2.0,'7,4')
f.txt(CSPXC,CSP_USE[1],'CSP 使用位置',9,PROV,'middle',0,-6)
f.rect(CSP_X[0],CSP_X[1],CSP_STO[0],CSP_STO[1],CSPF,PROV,2.0,'7,4')
f.txt(CSPXC,CSP_STO[1],'CSP 収納位置',9,PROV,'middle',0,-6)
f.line(SCX,CSP_STO[1],SCX,CSP_USE[0],PROV,1.0,'2,3')
f.hdim(CSPXC,SCX,f.py(CSP_USE[0])+24,'(4.55) SC中心とのズレ',PROV,'7,4')
axes(f,'x','h',(74,0),(0,-74))
open('/mnt/user-data/outputs/%s_%s_CSP設置位置正面図.svg'%(ts,FN[2]),'w',encoding='utf-8').write(
 f.out(FN[2],'CSP設置位置正面図','投影：−d 方向を見た正面図（x−h平面）／x を右、h を上として描く',
 LEG_BASE+[('#556677','● ＝ 視聴位置 LP の眼高（本図より d 方向奥）')],
 ['注1：PJ・LP は本投影面より奥（d 方向）にある要素を参考表示したもの。',
  '注2：x=273 より右のあらわし梁領域はコーナーの折り返しより奥に続く（D00-001 備考）。',
  '注3：CSP・昇降機構の外形および収納位置は未確定。',
  '注4：SC 中心 x=146 と設置エリア中心 x=129.65 は一致しない（差 16.35）。']))
print('ok')
