# K100 成立する形の全体三面図（収納・使用）（STEP4 4-3）
# 部屋は sanmen.py（F7 a）、CSPは csp.py（F7 c）で描き、機構・架台・駆動の部品はこのスクリプトで重ね描きJSONを作る（F7 b）。
# 構成（K099までで強度が成立した形、すべて仮）：
#   P2（Oは球面滑り軸受、面外のモーメントはBのリニアガイド HSR20C で受ける）、リンク 平鋼25×40（長リンク B–A–C は架台側、OAはその外側に重ねる）、
#   O 左d=52.0・右d=70.0（h=265）、a=50、収納φ=7.0°・使用φ=57.4°、リンク面 左x=95.55（OA 98.05）・右x=163.95（OA 161.45）、
#   CSP中心x=133.15（左へ6.3）、収納 d1=47.77・最下点h=240.77、使用 最下点h=168.61、
#   架台 鋼板厚8（左 x=89.5〜90.3・d=47〜165、右 x=169.2〜170・d=65〜183）、レール580、台形ねじTr14×3（固定側GBK10のみ、h=257.4）、
#   ナット（B＋3cm）、カップリング、モーター PKP268D42A2（架台の端から片持ち）、Bのブラケット、Oの外側の受け金具、Cの保持具。梁のねじ M2（8本/片側）。
import json, math, subprocess, glob
SAN=sorted(glob.glob('/home/claude/ceiling-project/ツール/*_sanmen.py'))[-1]
a=50.0; HO=265.0
ST,US='#2C6FB0','#2E9E6B'; FIX='#5F5E5A'; DRV='#B07A1F'; MOT='#E6A23C'
items=[]
def box(p,color,op=0.35,dash=True,fill=None): items.append(dict(t='box3',p=[round(v,2) for v in p],color=color,fill=fill or color,op=op,w=1.0,dash=dash))
def pose(Od,ph):
    p=math.radians(ph); B=(Od+2*a*math.cos(p),HO); C=(Od,HO-2*a*math.sin(p)); A=((B[0]+C[0])/2,(B[1]+C[1])/2); return A,B,C
def bar_poly(p,q,w=4.0):
    dx,dy=q[0]-p[0],q[1]-p[1]; L=math.hypot(dx,dy); nx,ny=-dy/L*w/2,dx/L*w/2
    return [[round(p[0]+nx,2),round(p[1]+ny,2)],[round(q[0]+nx,2),round(q[1]+ny,2)],[round(q[0]-nx,2),round(q[1]-ny,2)],[round(p[0]-nx,2),round(p[1]-ny,2)]]
SIDE={'左':dict(s=+1,face=89.5,O=52.0,d0=47.0,d1=165.0),'右':dict(s=-1,face=170.0,O=70.0,d0=65.0,d1=183.0)}
def X(sd,u):   # 梁の側面からの距離 u（cm）を x に
    return SIDE[sd]['face']+SIDE[sd]['s']*u
def xr(sd,u0,u1):
    x0,x1=X(sd,u0),X(sd,u1); return (min(x0,x1),max(x0,x1))
for sd,S in SIDE.items():
    dd=S['O']-52.0
    # 架台
    x0,x1=xr(sd,0,0.8); box([x0,x1,S['d0'],S['d1'],254.5,270],FIX,0.6,False)
    # レール
    x0,x1=xr(sd,0.8,2.6); box([x0,x1,99.54+dd,157.54+dd,264,266],'#555',0.7,True)
    # 固定側サポートユニット・カップリング・取付板・モーター（ねじ軸の中心 x：梁から3.5、h=257.4）
    x0,x1=xr(sd,1.3,5.2); box([x0,x1,158.0+dd,160.5+dd,254.4,260.4],DRV,0.6)
    x0,x1=xr(sd,2.25,4.75); box([x0,x1,161.0+dd,163.5+dd,256.15,258.65],DRV,0.5)
    x0,x1=xr(sd,0.8,6.5); box([x0,x1,164.0+dd,165.0+dd,253.9,261.0],DRV,0.6)
    x0,x1=xr(sd,0.68,6.32); box([x0,x1,165.0+dd,174.25+dd,254.58,260.22],MOT,0.55)
    # ねじ軸
    x0,x1=xr(sd,2.8,4.2); box([x0,x1,107.0+dd,160.5+dd,256.7,258.1],'#888',0.8)
    # Oの外側の受け金具（上から）と架台側のスペーサー
    x0,x1=xr(sd,0.8,10.8); box([x0,x1,S['O']-1.5,S['O']+1.5,266.5,269.5],FIX,0.6)
    x0,x1=xr(sd,9.8,10.8); box([x0,x1,S['O']-1.5,S['O']+1.5,263.5,269.5],FIX,0.6)
    for ph,col,lab in ((7.0,ST,'収納'),(57.4,US,'使用')):
        A_,B_,C_=pose(S['O'],ph)
        # ブロック・Bのブラケット・ナット
        x0,x1=xr(sd,1.2,3.8); box([x0,x1,B_[0]-3.7,B_[0]+3.7,261.85,268.15],col,0.35)
        x0,x1=xr(sd,3.8,4.8); box([x0,x1,B_[0]-3.7,B_[0]+3.7,262,268],col,0.5)
        x0,x1=xr(sd,2.4,4.6); box([x0,x1,B_[0]+1.5,B_[0]+4.5,256.3,258.5],'#9b6fc0',0.6)
        # リンク：長リンク B–A–C（梁から4.8〜7.3）、OA（7.3〜9.8）
        for (u0,u1),p,q in (((4.8,7.3),B_,C_),((7.3,9.8),(S['O'],HO),A_)):
            x0,x1=xr(sd,u0,u1)
            items.append(dict(t='poly',view='side',p=bar_poly(p,q)+[bar_poly(p,q)[0]],color=col,w=1.2,dash=True))
            items.append(dict(t='rect',view='plan',p=[x0,min(p[0],q[0]),x1,max(p[0],q[0])],color=col,fill=col,op=0.3,w=1.0,dash=True))
            items.append(dict(t='rect',view='front',p=[x0,min(p[1],q[1])-2,x1,max(p[1],q[1])+2],color=col,fill=col,op=0.3,w=1.0,dash=True))
        # Cの保持具（CSPの側面まで）
        csp_edge=133.15-28.55 if sd=='左' else 133.15+28.55
        if sd=='左': x0,x1=X(sd,3.8),csp_edge
        else: x0,x1=csp_edge,X(sd,3.8)
        box([min(x0,x1),max(x0,x1),C_[0]-2,C_[0]+2,C_[1]-3,C_[1]+3],col,0.45)
    # 梁のねじ（M2）
    o=S['O']; Bu=pose(o,57.4)[1][0]; Bs=pose(o,7.0)[1][0]; z0,z1=Bu-3.7,Bs+3.7
    for d,h in ((o,267.6),(o,257),(z0-1.5,267.6),(z1+1.5,267.6),(Bu-5,257),(Bu+5,257),(Bs-5,257),(Bs+5,257)):
        items.append(dict(t='pt',view='side',p=[round(d,2),h],color='#111',r=1.6,ring=(sd=='右')))
legend=[dict(text='青破線：収納時のリンク・ブロック・ナット・保持具（CSPは csp.py）',color=ST,dash=True,kind='line'),
        dict(text='緑破線：使用時のリンク・ブロック・ナット・保持具（CSPは csp.py）',color=US,dash=True,kind='line'),
        dict(text='灰：架台（鋼板厚8）・Oの外側の受け金具',color=FIX,kind='band'),
        dict(text='茶：駆動（台形ねじTr14×3・固定側GBK10・カップリング・取付板）',color=DRV,kind='band'),
        dict(text='橙：モーター PKP268D42A2（架台の端から片持ち）',color=MOT,kind='band'),
        dict(text='黒点・輪：梁のねじ M2 左・右（8本/片側、側面図）',color='#111',kind='dot')]
J=dict(items=items,legend=legend,
       title_note=['STEP4 4-3 強度が成立した形（K099）の全体：P2（Oは球面滑り軸受、面外のモーメントはBのリニアガイドHSR20Cで受ける）、平鋼リンク25×40、台形ねじ駆動（固定側のみ）、ステッピングモーター2台。',
                   'CSPは左へ6.3（中心x=133.15）、収納 d1=47.77・最下点h=240.77、使用 最下点h=168.61。O 左d=52.0・右d=70.0、h=265。前提はすべて仮（破線）。',
                   '強度の照合：K099（最小の余裕 ねじ1.48・ガイドMC1.81・リンク6.54・Oのピン4.08）。部品の位置：K094〜K098。'],
       src=['K085','K086','K096','K098','K099'])
json.dump(J,open('/tmp/k100_mech.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
subprocess.run(['python3',SAN,'--zuban','K100','--title','成立する形の全体（収納・使用）','-o','/mnt/user-data/outputs/{ts}_K100_成立する形の全体.svg','/tmp/k100_mech.json','/tmp/k100_csp.json'],check=True)
