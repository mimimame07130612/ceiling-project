# K048 姿勢保持の案（STEP4 4-2、水平・鉛直版スコットラッセル）
# ロッドBCは水平から約7°→57°まで回る。CSP（チルト24°）の姿勢を保つ方法の候補4案を、機構だけの側面図(d-h)で並べる。
# 部屋は描かない（F7 d）。幾何は K046 と同じ：a=50、O=(61.73,268)、C=CSP中心（鉛直移動、収納h=255.885→使用h=183.725）。
# CSP外形は csp.py（A01-001・A02-002）の収納姿勢の角座標を平行移動して使う。
# 入力：K046/K047、A01-001、A02-002、D01-001（掘込面h=270・梁下面h=254.5）
import math, subprocess, html
TS=subprocess.run(['date','+%y%m%d%H%M'],capture_output=True,text=True,env={'TZ':'Asia/Tokyo'}).stdout.strip()
OUT='/mnt/user-data/outputs/%s_K048_姿勢保持の案.svg'%TS
a=50.0; O=(61.73,268.0); CS_H=255.885; STROKE=72.16; t0=268-CS_H
CSP0=[(48.50,252.47),(68.05,243.77),(74.96,259.30),(55.41,268.00)]   # P0,P1,P3,P2（収納）
def pose(s):
    oc=t0+STROKE*s; C=(O[0],O[1]-oc); ph=math.asin(oc/(2*a)); B=(O[0]+2*a*math.cos(ph),O[1]); A=((B[0]+C[0])/2,(B[1]+C[1])/2)
    return ph,A,B,C
def cspoly(C): dv=C[1]-CS_H; return [(p[0],p[1]+dv) for p in CSP0]
# ---- 描画 ----
S=2.3; PW,PH=(200-38)*S,(276-160)*S; GX,GY=40,150
out=[]; e=html.escape
def T(x,y,s,c='#222',size=11,anchor='start',bold=False):
    out.append('<text x="%.1f" y="%.1f" fill="%s" font-size="%s" text-anchor="%s"%s>%s</text>'%(x,y,c,size,anchor,' font-weight="bold"' if bold else '',e(s)))
class P:
    def __init__(s,ox,oy): s.ox,s.oy=ox,oy
    def X(s,d): return s.ox+(d-38)*S
    def Y(s,h): return s.oy+(276-h)*S
    def ln(s,pts,c,w=1.5,dash=False,op=1):
        out.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="%s" stroke-opacity="%s"%s/>'%(' '.join('%.1f,%.1f'%(s.X(p[0]),s.Y(p[1])) for p in pts),c,w,op,' stroke-dasharray="5 3"' if dash else ''))
    def pg(s,pts,c,op=0.15,w=1.0):
        out.append('<polygon points="%s" fill="%s" fill-opacity="%s" stroke="%s" stroke-width="%s"/>'%(' '.join('%.1f,%.1f'%(s.X(p[0]),s.Y(p[1])) for p in pts),c,op,c,w))
    def pt(s,p,c,r=2.6,ring=False):
        out.append('<circle cx="%.1f" cy="%.1f" r="%s" fill="%s" stroke="%s" stroke-width="1.2"/>'%(s.X(p[0]),s.Y(p[1]),r,'white' if ring else c,c))
    def ci(s,p,rc,c,w=1.2):
        out.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="%s" stroke-width="%s"/>'%(s.X(p[0]),s.Y(p[1]),rc*S,c,w))
    def t(s,p,txt,c='#222',dx=4,dy=-4,size=10,anchor='start'): T(s.X(p[0])+dx,s.Y(p[1])+dy,txt,c,size,anchor)
    def frame(s,title,sub):
        out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="none" stroke="#999" stroke-width="0.8"/>'%(s.ox-8,s.oy-42,PW+16,PH+50))
        T(s.ox,s.oy-26,title,bold=True,size=13); T(s.ox,s.oy-10,sub,'#555',10)
        s.ln([(38,270),(200,270)],'#555',1.4); s.t((200,270),'掘込面h=270','#555',-2,-4,9,'end')
        s.ln([(38,254.5),(200,254.5)],'#8a857a',1.0,True); s.t((200,254.5),'梁下面h=254.5','#8a857a',-2,12,9,'end')
        s.ln([(45.5,270),(45.5,250),(38,250)],'#555',1.4)
COLS=[(0,'#2C6FB0','収納'),(0.5,'#999999','中間'),(1,'#C0392B','使用')]
def base(p,s,col,rail=True):
    ph,A,B,C=pose(s)
    p.pg(cspoly(C),col,0.12 if s!=0.5 else 0.05)
    p.ln([O,A],col,2.4); p.ln([B,C],col,1.6,True)
    for q in (A,B,C): p.pt(q,col)
    return ph,A,B,C
def rail(p,x0=110,x1=167): p.ln([(x0,268),(x1,268)],'#111',3); p.pt(O,'#111',4,True); p.t(O,'O','#111',-6,-6,10,'end')
panels=[]
# 案1 二重スコットラッセル（dずらし）
DD=12.0
p=P(GX,GY+30); p.frame('案1　二重スコットラッセル（d方向にΔd=12ずらした同形の機構を並べる）','Bは1台のキャリッジで共有。C・C′の2点でCSPを持つ → 2点が常に水平に並ぶので姿勢一定')
rail(p,110,180); O2=(O[0]+DD,O[1]); p.pt(O2,'#111',4,True); p.t(O2,"O′",'#111',4,-6,10)
for s,col,tag in COLS:
    ph,A,B,C=base(p,s,col)
    A2=(A[0]+DD,A[1]); B2=(B[0]+DD,B[1]); C2=(C[0]+DD,C[1])
    p.ln([O2,A2],col,1.6); p.ln([B2,C2],col,1.0,True); p.pt(C2,col); p.ln([C,C2],col,3)
    p.ln([B,B2],col,4.5,op=0.5)
p.t(pose(1)[3],'C(使)','#C0392B',-6,14,10,'end'); p.t((pose(1)[3][0]+DD,pose(1)[3][1]),"C′",'#C0392B',4,14,10)
p.t((pose(0)[2][0]+6,268),'Bキャリッジ(B・B′)','#111',0,-8,10)
panels.append(p)
# 案2 平行リンク（二段の平行四辺形）
E=5.0
p=P(GX+PW+50,GY+30); p.frame('案2　二段の平行リンク（OA・ACそれぞれに平行なリンクを添える）','O′=O−(0,5)固定。A側の三角板とC側の板が平行移動 → CSPを固定した板は回らない')
rail(p); O2=(O[0],O[1]-E); p.pt(O2,'#111',3.4,True); p.t(O2,"O′",'#111',-6,10,10,'end')
for s,col,tag in COLS:
    ph,A,B,C=base(p,s,col)
    A2=(A[0],A[1]-E); C2=(C[0],C[1]-E)
    p.ln([O2,A2],col,1.4); p.ln([A2,C2],col,1.4); p.ln([A,A2],col,3); p.ln([C,C2],col,3); p.pt(A2,col,2); p.pt(C2,col,2)
p.t((pose(0)[3][0],pose(0)[3][1]-E),'C′(収) h=%.1f'%(CS_H-E),'#2C6FB0',6,12,10)
panels.append(p)
# 案3 ベルト（プーリー1:1）
R=3.0
p=P(GX,GY+30+PH+80); p.frame('案3　ベルト（歯付き）による平行保持（プーリー1:1）','O固定プーリー→A二連プーリー→Cプーリー。CプーリーにCSPを固定 → 回らない（卓上ライトと同じ）')
rail(p)
for s,col,tag in COLS:
    ph,A,B,C=base(p,s,col)
    for q in (O,A,C): p.ci(q,R,col)
    for (u,v) in ((O,A),(A,C)):
        dx,dy=v[0]-u[0],v[1]-u[1]; L=math.hypot(dx,dy); nx,ny=-dy/L*R,dx/L*R
        p.ln([(u[0]+nx,u[1]+ny),(v[0]+nx,v[1]+ny)],col,0.9); p.ln([(u[0]-nx,u[1]-ny),(v[0]-nx,v[1]-ny)],col,0.9)
p.t(O,'固定プーリー','#111',8,14,10)
panels.append(p)
# 案4 重力による吊り下げ
p=P(GX+PW+50,GY+30+PH+80); p.frame('案4　重力による吊り下げ（Cは自由回転のピン）','CSPはC回りに自由。重心がCの真下に来る向きで止まる → チルトは重心位置で決まる')
rail(p)
for s,col,tag in COLS:
    ph,A,B,C=base(p,s,col)
    G=(C[0],C[1]-4); p.ln([C,G],col,1.0,True); p.pt(G,col,3.2,True)
    if s==1:
        p.t(G,'重心G（Cの真下）','#C0392B',6,12,10)
        for k in (-1,1):
            ang=math.radians(8*k); pts=[(C[0]+(q[0]-C[0])*math.cos(ang)-(q[1]-C[1])*math.sin(ang),C[1]+(q[0]-C[0])*math.sin(ang)+(q[1]-C[1])*math.cos(ang)) for q in cspoly(C)]
            p.pg(pts,'#C0392B',0.0,0.6)
        p.t((C[0]+20,C[1]+2),'発停で揺れる（±8°の例）','#C0392B',0,0,10)
panels.append(p)
# ---- ヘッダ・凡例・表 ----
W=int(GX*2+PW*2+50+20); H=int(GY+30+2*(PH+80)+260)
hdr=['K048　姿勢保持の案（STEP4 4-2、水平・鉛直版スコットラッセル）　作成 20%s/%s/%s %s:%s　単位cm　側面図(d-h)、左がSC側'%(TS[0:2],TS[2:4],TS[4:6],TS[6:8],TS[8:10]),
 '共通：a=50、O=(61.73,268)、Bは水平(h=268)、Cは鉛直（CSP中心、収納h=255.9→使用h=183.7）。ロッドBCの水平からの角は収納7.0°→使用57.4°、OAは逆向きに同じだけ回る。',
 '青＝収納・灰＝中間・赤＝使用。太線＝OA、破線＝ロッドBC。部品は線（太さ0）で描いた概念図で、寸法（Δd・オフセット5・プーリー径6）は仮の値。']
for i,hh in enumerate(hdr): T(GX,26+i*18,hh,'#111' if i==0 else '#333',13 if i==0 else 11,bold=(i==0))
rows=[('','姿勢の正確さ','追加部品','一部品が壊れたとき','収納時に梁下面より下に出るもの','気になる点'),
('案1 二重SR','幾何的に厳密','機構1組ぶん（O′・リンク2本）','残る1組で吊れる（ただし姿勢は保てない）','なし（K046と同じ）','Bキャリッジが2点をまたぐ。O′も梁間に取付'),
('案2 平行リンク','幾何的に厳密','リンク2本・板2枚・固定点O′','CSPは落ちないが回る','C′(h=250.9)が梁下面より3.6下','A側・C側の板が増える。平行四辺形はつぶれる角に注意'),
('案3 ベルト','ベルトの伸びぶん誤差','プーリー4・ベルト2・張り調整','ベルト切れでCSPが回る（落ちない）','なし','張りの管理・摩耗粉（S3 h）'),
('案4 重力吊り','重心で決まる／揺れる','ほぼなし（ダンパーが要る）','—','なし','発停で揺れる＝急動作（S3 a）。チルト24°は重心位置しだい')]
ty=GY+30+2*(PH+80)+20; cw=[110,120,190,230,210,340]
for r_i,r in enumerate(rows):
    x=GX
    for c_i,c in enumerate(r):
        T(x,ty+r_i*22,c,'#111' if r_i==0 else '#333',11,bold=(r_i==0 or c_i==0)); x+=cw[c_i]
    out.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="#ccc"/>'%(GX,ty+r_i*22+7,GX+sum(cw),ty+r_i*22+7))
T(GX,ty+5*22+10,'表は図から読める事実の整理（評価は依頼主と相談して決める）。','#666',10)
W=max(W,GX+sum(cw)+20)
svg='<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" font-family="sans-serif"><rect width="100%%" height="100%%" fill="white"/>%s</svg>'%(W,H,W,H,''.join(out))
open(OUT,'w',encoding='utf-8').write(svg); print(OUT)
# 確認用の数値
for s in (0,0.5,1):
    ph,A,B,C=pose(s); print('s=%.1f rod角=%.1f° A=(%.1f,%.1f) B=(%.1f,%.1f) C=(%.1f,%.1f)'%(s,math.degrees(ph),*A,*B,*C))
