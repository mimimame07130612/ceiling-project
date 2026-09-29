# K039 リンク長とBの収納位置（STEP4 4-1、Bが逃げられるかの確認）
# スコットラッセルは O・スライダ直線・取付点Cの直線がすべてO上で直交する。B収納の位置がリンク長aでどう動くかを見る。
# 側面図：B収納の軌跡（a=45〜60）＋選定例a=50の全リンク・スライダ軌道、配光118°断面、梁下面h=254.5
# 正面図：CSP・配光118°・左右リンクのx位置（x=110.9/168.0、wR=0）
# 入力：A03-004〜006（wR=0で作図）、A01-001、A02-002、D00-005・A00-006・A02-001、D00-007（梁下面h=254.5＝D01-001由来）、D04-001・D04-002
import json, math, subprocess, glob
TS = subprocess.run(['date','+%y%m%d%H%M'],capture_output=True,text=True,env={'TZ':'Asia/Tokyo'}).stdout.strip()  # 作図時 2609292235
NAME='K039_リンク長とBの収納位置'
CSP=sorted(glob.glob('*_csp.py'))[-1]; SAN=sorted(glob.glob('*_sanmen.py'))[-1]
OUTJ='/mnt/user-data/outputs/%s_%s.json'%(TS,NAME); OUTS='/mnt/user-data/outputs/%s_%s.svg'%(TS,NAME)
subprocess.run(['python3',CSP,'json','-o','c.json','--pose','収納,139.45,48.5,243.77','--pose','使用,139.45,33,168.51'],check=True,capture_output=True)
C=json.load(open('c.json',encoding='utf-8'))
side=[it['p'] for it in C['items'] if it['t']=='poly']
cs=[sum(p[0] for p in side[0])/4,sum(p[1] for p in side[0])/4]
cu=[sum(p[0] for p in side[1])/4,sum(p[1] for p in side[1])/4]
L=math.hypot(cu[0]-cs[0],cu[1]-cs[1])
uc=((cu[0]-cs[0])/L,(cu[1]-cs[1])/L)
us=(-uc[1],uc[0]) if -uc[1]>0 else (uc[1],-uc[0])
HO=268.0; t0=(HO-cs[1])/(-uc[1]); O=(cs[0]-uc[0]*t0,HO)
r2=lambda p:[round(p[0],2),round(p[1],2)]
def Bpt(dist): return (O[0]+us[0]*dist,O[1]+us[1]*dist)
def pose(a,ocd):
    phi=math.asin(ocd/(2*a)); Cp=(O[0]+uc[0]*ocd,O[1]+uc[1]*ocd)
    Bp=Bpt(2*a*math.cos(phi)); Ap=((Bp[0]+Cp[0])/2,(Bp[1]+Cp[1])/2)
    return phi,Ap,Bp,Cp
RYO=254.5  # 梁下面
XL,LX,LD,R0,TN=110.9,129.65,[130,175,220],5.7,math.tan(math.radians(59)); dx=LX-XL
items=list(C['items'])
# 配光（側面）
for dL in LD:
    pl,pr=[],[]
    for k in range(0,61):
        h=270-k*0.5; r=R0+(270-h)*TN
        if r>dx:
            w=math.sqrt(r*r-dx*dx); pr.append([round(dL+w,2),h]); pl.append([round(dL-w,2),h])
    items.append(dict(t='poly',view='side',p=pl+pr[::-1],color='#BA7517',fill='#BA7517',op=0.16,w=1.0))
# 配光（正面）
for xL in (LX,220.65):
    wb=R0+30*TN
    items.append(dict(t='poly',view='front',p=[[round(xL-R0,2),270],[round(xL+R0,2),270],[round(xL+wb,2),240],[round(xL-wb,2),240]],color='#BA7517',fill='#BA7517',op=0.13,w=1.0))
# 梁下面ライン（側面）
items.append(dict(t='line',view='side',p=[[40,RYO],[330,RYO]],color='#8a857a',w=1.2,dash=True))
# スライダ直線（延長）
sl0=Bpt(35); sl1=Bpt(110)
items.append(dict(t='line',view='side',p=[r2(sl0),r2(sl1)],color='#555555',w=1.0,dash=True))
items.append(dict(t='text',view='side',p=r2(sl1),s='Bのすべる直線',dx=4,dy=14,color='#555555'))
# 経路（延長）
items.append(dict(t='line',view='side',p=[r2((O[0]-uc[0]*3,O[1]-uc[1]*3)),r2((cu[0]+uc[0]*10,cu[1]+uc[1]*10))],color='#999999',w=1.0,dash=True))
# B収納の軌跡（aスイープ）
rows=[]
for a in (45,48,50,52,55,60):
    ph_s,_,Bs,_=pose(a,t0); ph_u,_,Bu,_=pose(a,t0+L)
    items.append(dict(t='pt',view='side',p=r2(Bs),color='#2E9E6B',r=3.2))
    if a in (45,60):
        items.append(dict(t='text',view='side',p=r2(Bs),s='a=%d'%a,dx=(-4 if a==45 else 4),dy=(-6 if a==45 else 14),color='#2E9E6B',anchor=('end' if a==45 else 'start')))
    rows.append((a,math.degrees(ph_s),math.degrees(ph_u),90-math.degrees(ph_u),Bs[0],Bs[1],Bu[0],Bu[1],
                 2*a*math.cos(ph_s)-2*a*math.cos(ph_u)))
# 選定例 a=50 の全リンク
A_SEL=50
for ocd,col,tag in ((t0,'#2C6FB0','収'),(t0+L,'#C0392B','使')):
    ph,Ap,Bp,Cp=pose(A_SEL,ocd)
    items.append(dict(t='line',view='side',p=[r2(O),r2(Ap)],color=col,w=2.0,dash=(tag=='使')))
    items.append(dict(t='line',view='side',p=[r2(Bp),r2(Cp)],color=col,w=2.0,dash=(tag=='使')))
    for q,nm in ((Ap,'A'),(Bp,'B'),(Cp,'C')):
        items.append(dict(t='pt',view='side',p=r2(q),color=col,r=3.0))
# レール（B使用〜B収納をカバー）
_,_,Bu50,_=pose(A_SEL,t0+L); _,_,Bs50,_=pose(A_SEL,t0)
items.append(dict(t='line',view='side',p=[r2(Bpt(2*A_SEL*math.cos(pose(A_SEL,t0+L)[0])-6)),r2(Bpt(2*A_SEL*math.cos(pose(A_SEL,t0)[0])+6))],color='#111111',w=3.2))
items.append(dict(t='text',view='side',p=r2(Bs50),s='B収納(a=50)',dx=4,dy=16,color='#111111'))
items.append(dict(t='pt',view='side',p=r2(O),color='#111111',r=4.5,ring=True))
items.append(dict(t='text',view='side',p=r2(O),s='O(固定 h=268)',dx=6,dy=-8,color='#111111'))
# 正面図：左右リンクのx（wR=0）
for xx,nm,col in ((110.9,'左リンク x=110.9','#2C6FB0'),(168.0,'右リンク x=168.0','#C0392B')):
    items.append(dict(t='line',view='front',p=[[xx,240],[xx,270]],color=col,w=1.6,dash=True))
    items.append(dict(t='text',view='front',p=[xx,240],s=nm,dx=2,dy=16,color=col,anchor='middle'))
notes=[
 'STEP4 4-1：Bを配光・梁下面より上へ逃がせるかの確認。スコットラッセルは OB²+OC²=(2a)²（O・スライダ・Cの直線がO上で直交）。',
 'OC 収納%.2f→使用%.2f。B収納の位置＝Oからスライダ方向に OB=√((2a)²−OC収納²)。収納時のOBは常に≒2a（最大）で、aを増やすほどBは遠く（+d）・低く（−h）なる。' % (t0,t0+L),
 '緑：B収納の軌跡（a=45〜60）。いちばん上でも a=45 で d=%.0f・h=%.0f。梁下面h=254.5より下、かつ左の配光断面の中。aを大きくすると使用時φは90°から離れて安全になるが、Bはさらに下がる（トレードオフ）。' % (pose(45,t0)[2][0],pose(45,t0)[2][1]),
 '結論：この構成（Cを取付点、Oを天井付近h=268）ではBは逃げられない。B収納は必ず梁下面より下・配光内に来る。梁下面より下は可（D04-002、部分はみ出し可）。配光内はA00-006（前提条件・交渉可）に抵触。',
 '選定例 a=50：使用時φ=%.1f°（90°まで%.1f°の余裕）、B収納 d=%.0f・h=%.0f、レール長≒%.0f。最終aは駆動力（4-4、φが90°に近いほど不利）を見て決める。青＝収納・赤＝使用のリンク。黒太線＝Bのレール。' % (
     rows[2][2],rows[2][3],rows[2][4],rows[2][5],abs(rows[2][8])),
 '正面図：左右リンクのx位置（x=110.9／168.0、wR=0）。右リンク(x=168)は左右の配光の谷にあるが、h≒250より下で左照明の配光に入る。',
]
ov=dict(title_note=notes,legend=C['legend']+[
    dict(text='緑：B収納の軌跡（リンク長a=45〜60）',color='#2E9E6B',kind='dot'),
    dict(text='黒 太線：Bのレール（選定例 a=50）',color='#111111',kind='line'),
    dict(text='青／赤：選定例a=50のリンク（収納／使用）',color='#2C6FB0',dash=True,kind='line'),
    dict(text='灰 破線：スライダ直線・取付点Cの経路',color='#555555',dash=True,kind='line'),
    dict(text='黄 帯：配光118°（側面＝x=110.9断面、正面＝x方向の広がり）',color='#BA7517',kind='band'),
    dict(text='灰 破線：梁下面 h=254.5',color='#8a857a',dash=True,kind='line')],
    src=C['src']+['A03-004〜006','D00-005','A00-006','A02-001','D01-001','D04-002'],items=items)
json.dump(ov,open(OUTJ,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
subprocess.run(['python3',SAN,'--zuban','K039','--title','リンク長とBの収納位置','-o',OUTS,OUTJ],check=True)
# 表（K040）
import csv,io
hdr=['リンク長a','収納φ(°)','使用φ(°)','使用の余裕(90°−φ)','B収納d','B収納h','B使用d','B使用h','レール長']
buf=io.StringIO(); w=csv.writer(buf); w.writerow(hdr)
for r in rows: w.writerow([r[0]]+['%.1f'%x for x in r[1:4]]+['%.1f'%x for x in r[4:8]]+['%.1f'%abs(r[8])])
open('/mnt/user-data/outputs/%s_K040_リンク長の検討表.csv'%TS,'w',encoding='utf-8-sig').write(buf.getvalue())
print(TS); print('\n'.join(notes)); print(buf.getvalue())
