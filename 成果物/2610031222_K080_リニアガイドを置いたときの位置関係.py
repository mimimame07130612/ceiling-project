# K080 リニアガイド（重荷重用H24・2ブロック）を置いたときの左右の位置関係（正面図の部分詳細、STEP4 4-3）
# 部屋を含まない部分詳細図（F7 d）。梁は描かず、梁の側面の位置（左 x=89.5・右 x=170）を座標の目盛りとして示すだけにする。
# 寸法（仮・カタログ値）：ミスミ 重荷重用リニアガイド SXR24（標準ブロック）H=24・W=34・L1=57、レール幅W1=15（ミスミ カタログ P1-575/577）。
#   レールの高さはH1から 12.5mm（仮）、ブロックの下面はレール取付面から 4mm（K=20から仮）。B（ピン）の高さ h=265（K077の依頼主条件）。
#   架台：鋼板厚8（左 x=89.5〜90.3、右 169.2〜170）。リンク：鋼角パイプ25×25（K079の概算、仮）、ブロック上面とのすき間0.2（仮）。
#   CSP：今の位置 x=110.9〜168.0（wR=0）。リンクの内側の面とCSPの間のすき間0.5（仮）。
#   横柱 SF-20・20 は h=268〜270・262〜264 の帯で示す（dの位置は正面図では重なる）。
import subprocess
TS=subprocess.run(['date','+%y%m%d%H%M'],capture_output=True,text=True,env={'TZ':'Asia/Tokyo'}).stdout.strip()
H=2.4; RH=1.25; KB=0.4; BW=3.4; RW=1.5; LK=2.5; GAP=0.2; CL=0.5; HB=265.0
L=dict(face=89.5,pl=90.3,s=+1); R=dict(face=170.0,pl=169.2,s=-1)
def parts(S):
    s=S['s']; p=S['pl']
    rail=sorted([p,p+s*RH]); blk=sorted([p+s*KB,p+s*H]); lk_in=p+s*(H+GAP); lk=sorted([lk_in,lk_in+s*LK]); c=(lk[0]+lk[1])/2
    return rail,blk,lk,c
rl,bl,ll,cl=parts(L); rr,br,lr,cr=parts(R)
csp_edge_need=lr[0]-CL; shift=168.0-csp_edge_need
print('左リンク中心',round(cl,2),'右リンク中心',round(cr,2),'右リンク内面',round(lr[0],2),'CSP右端の上限',round(csp_edge_need,2),'CSPを左へ',round(shift,2))
# 描画
X0,X1,Y0,Y1=84,182,236,274; SC=11.0; ML=40; MT=150
def X(x): return ML+(x-X0)*SC
def Y(h): return MT+(Y1-h)*SC
Wd=int(ML+(X1-X0)*SC+40); Ht=int(MT+(Y1-Y0)*SC+170)
o=[]
def rect(x0,x1,h0,h1,fill,stroke='#333',op=1,dash=False,w=1):
    o.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" fill-opacity="%s" stroke="%s" stroke-width="%s"%s/>'%(X(min(x0,x1)),Y(max(h0,h1)),abs(x1-x0)*SC,abs(h1-h0)*SC,fill,op,stroke,w,' stroke-dasharray="5,3"' if dash else ''))
def line(x0,h0,x1,h1,c='#333',w=1,dash=False):
    o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"%s/>'%(X(x0),Y(h0),X(x1),Y(h1),c,w,' stroke-dasharray="5,3"' if dash else ''))
def text(x,h,s,c='#222',anchor='start',size=12,dy=0):
    o.append('<text x="%.1f" y="%.1f" fill="%s" font-size="%d" text-anchor="%s">%s</text>'%(X(x),Y(h)+dy,c,size,anchor,s))
# 目盛り
for x in range(85,182,5):
    line(x,Y0,x,Y0+0.4,'#999'); text(x,Y0,str(x),'#777','middle',10,14)
for h in range(240,272,5):
    line(X0,h,X0+0.4,h,'#999'); text(X0,h,str(h),'#777','end',10,4)
text(X0,Y0,'x（cm）','#777','start',10,30)
# 梁の側面の位置（目盛りとしてのみ）・掘込面
for x in (89.5,170.0): line(x,250,x,272,'#999',1,True)
text(89.5,272,'梁1の側面 x=89.5','#777','end',11,-4); text(170,272,'梁2の側面 x=170','#777','start',11,-4)
line(X0,270,X1,270,'#bbb',1,True); text(X1,270,'掘込面 h=270','#999','end',10,-4)
# 横柱の帯
for h0,h1 in ((268,270),(262,264)): rect(90.3,169.2,h0,h1,'#E67E22','#E67E22',0.18,True)
text(130,269,'(横柱 SF-20・20 h=268〜270)','#C0611B','middle',11,4); text(130,263,'(横柱 SF-20・20 h=262〜264)','#C0611B','middle',11,4)
# CSP（今の位置）と必要な位置
rect(110.9,168.0,241.77,266.0,'#2C6FB0','#2C6FB0',0.10,True); text(139.45,244,'(CSP 今の位置 x=110.9〜168.0)','#2C6FB0','middle',11)
rect(110.9-shift,168.0-shift,241.77,266.0,'none','#8E44AD',0,True,1.4); text(139.45-shift,240.5,'(CSP 右のリンクをかわす位置：左へ%.1f)'%shift,'#8E44AD','middle',11)
for S,rail,blk,lk,c in ((L,rl,bl,ll,cl),(R,rr,br,lr,cr)):
    rect(S['face'],S['pl'],254.5,270,'#5F5E5A','#5F5E5A',0.6)
    rect(rail[0],rail[1],HB-RW/2,HB+RW/2,'#555','#222',0.9)
    rect(blk[0],blk[1],HB-BW/2,HB+BW/2,'#D85A30','#8a3a1d',0.5)
    rect(lk[0],lk[1],HB-LK/2,HB+LK/2,'#1D9E75','#0f5f45',0.5)
    o.append('<circle cx="%.1f" cy="%.1f" r="3" fill="#111"/>'%(X(c),Y(HB)))
# 今のリンク面
for x in (92.0,168.0): line(x,240,x,268,'#1D9E75',1.2,True)
text(92.0,240,'(今のリンク面 x=92.0)','#1D9E75','start',10,14); text(168.0,240,'(今のリンク面 x=168.0)','#1D9E75','end',10,14)
# 寸法の注記
text(cl,258,'(左リンク中心 x=%.2f)'%cl,'#0f5f45','start',11)
text(cr,258,'(右リンク中心 x=%.2f)'%cr,'#0f5f45','end',11)
text(cr,255.5,'(右リンク内面 x=%.2f／CSP右端は%.2f以下)'%(lr[0],csp_edge_need),'#8E44AD','end',11)
# 凡例・注記
leg=[('#5F5E5A','架台（鋼板厚8）'),('#555','レール（W1=15、高さ12.5：仮）'),('#D85A30','ブロック（H24・W34：ミスミ SXR24）'),('#1D9E75','リンク（角パイプ25×25：仮）、●＝Bのピン h=265'),('#E67E22','横柱 SF-20・20（帯で表示）'),('#2C6FB0','CSP 今の位置（破線）'),('#8E44AD','CSP 右のリンクをかわす位置（破線）')]
for i,(c,t) in enumerate(leg):
    yy=Ht-150+i*18; o.append('<rect x="%d" y="%d" width="14" height="10" fill="%s" fill-opacity="0.6"/>'%(ML,yy-9,c)); o.append('<text x="%d" y="%d" font-size="12" fill="#222">%s</text>'%(ML+20,yy,t))
note=['K080 リニアガイド（重荷重用H24・2ブロック）を置いたときの位置関係（正面図の部分詳細、LP側からSC側を見る、x-h）　作成 %s'%TS,
 '部屋を含まない部分詳細（F7 d）。梁は描かず、側面の位置を破線の目盛りで示す。前提はすべて仮：ブロックとリンクのすき間0.2、リンクとCSPのすき間0.5、B h=265（K077）。',
 '数値の根拠：K079（必要MC≧152N·m・MA≧77N·m）、ミスミ 重荷重用 H24 2ブロック密着 MC=196・MA=184.5N·m（参考値）。']
for i,t in enumerate(note): o.append('<text x="%d" y="%d" font-size="%d" fill="#111"%s>%s</text>'%(ML,30+i*20,14 if i==0 else 12,' font-weight="bold"' if i==0 else '',t))
svg='<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" font-family="Noto Sans CJK JP, Yu Gothic, sans-serif"><rect width="100%%" height="100%%" fill="white"/>%s</svg>'%(Wd,Ht,Wd,Ht,''.join(o))
out='/mnt/user-data/outputs/%s_K080_リニアガイドを置いたときの位置関係.svg'%TS
open(out,'w',encoding='utf-8').write(svg); print(out)
