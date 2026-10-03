# K059 片側の部品1個の破断とCSPの動き（STEP4 4-3、単一故障の確認）
# 左側の機構の部品（短リンクOA・長リンクBAC・支点O/A/B/C）を1個ずつ破断させ、残りで釣り合う位置と左右の分担を求める。右側は健全。
# モデル（側面 d-h 面に投影した2次元、仮）：
#   ・右のC′は健全な右機構に固定され、ピン（x軸まわりに回れる）。CSP（保持具込みの剛体）はC′まわりの回転（ピッチ）1自由度を持つ。
#   ・左のCはCSP上でC′から d方向に−18（Δd、K049配置β）。CSP重心はcsp.pyの断面の図心。荷重はLC1 W=(7.90+7.4)×9.81。
#   ・左の駆動（ねじ・キャリッジ）は健全でBの位置は動かない。駆動の破損は別の故障点（K030 F5：落下止めで対応）。
#   ・面外（x方向）のねじり（ロール）は扱わない。部品どうし・周囲との当たりは考えない。
# 破断ごとの残り：
#   (a) O・OA・A：ロッドBCがB・Cのピンだけで残る（2力部材）。CSPの回転はこれで止まり、位置は変わらない。
#   (b) B・ロッドのB–A間：O–A–Cの2本の鎖が残る。鎖が伸び切る（|OC|=100）まではCSPを止められない。
#   (c) C・ロッドのA–C間：左はCSPから切り離される。
import math, json, csv, subprocess
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
plt.rcParams['font.family']='Noto Sans CJK JP'
TS=subprocess.run(['date','+%y%m%d%H%M'],capture_output=True,text=True,env={'TZ':'Asia/Tokyo'}).stdout.strip()
NAME='K059_片側の部品1個の破断とCSPの動き'
g=9.81; W=(7.90+7.4)*g; a=50.0; CS=255.885; ST=72.16; t0=268-CS; DL,DR=52.73,70.73
prof=[i['p'] for i in json.load(open('/tmp/c56.json',encoding='utf-8'))['items'] if i['t']=='poly' and i['view']=='side']
def cen(P):
    A=cx=cy=0
    for i in range(len(P)):
        x0,y0=P[i]; x1,y1=P[(i+1)%len(P)]; c=x0*y1-x1*y0; A+=c; cx+=(x0+x1)*c; cy+=(y0+y1)*c
    return cx/(3*A), cy/(3*A)
def pose(Od,s):
    oc=t0+ST*s; C=(Od,268-oc); ph=math.asin(oc/(2*a)); B=(Od+2*a*math.cos(ph),268.0); A=((B[0]+C[0])/2,(B[1]+C[1])/2)
    return dict(O=(Od,268.0),A=A,B=B,C=C,phi=math.degrees(ph))
def rot(p,c,t):
    x,y=p[0]-c[0],p[1]-c[1]; return (c[0]+x*math.cos(t)-y*math.sin(t), c[1]+x*math.sin(t)+y*math.cos(t))
rows=[]; figdata=[]
for si,pos in enumerate(('収納','使用')):
    L=pose(DL,si); R=pose(DR,si); Cp=R['C']; C=L['C']; G=cen(prof[si]); P=prof[si]
    # (a) ロッドBCが2力部材：CSPの釣り合い（W at G、左はBC方向の軸力T at C、右C′は力Fd,Fh、モーメントなし）
    ux,uy=(L['B'][0]-C[0])/100,(L['B'][1]-C[1])/100      # CからBへの単位ベクトル（引張でCSPを引く向き）
    # C′まわりのモーメント：r_C×(T u) + r_G×(0,−W) = 0
    rC=(C[0]-Cp[0],C[1]-Cp[1]); rG=(G[0]-Cp[0],G[1]-Cp[1])
    T=-(rG[0]*(-W))/(rC[0]*uy-rC[1]*ux)
    Fd=-T*ux; Fh=W-T*uy
    rows.append([pos,'(a) O・OA・A','動かない（ロッドBCが2力部材で残る）','0.0','%.0f'%T,'%.0f'%(T*uy),'%.0f'%Fh,'%.0f'%Fd,'左ロッドの角度 %.1f°'%L['phi']])
    # 健全時の参考（左右のC点の鉛直分担：C′まわりのモーメント）
    VL=-(rG[0]*(-W))/rC[0]
    # (c) 左切り離し：CSPはC′まわりに回り、重心がC′の真下に来て止まる
    th_c=math.atan2(rG[0],-rG[1])  # 重心をC′真下へ回す角度（反時計回り正）
    th_c=-(math.atan2(rG[1],rG[0])+math.pi/2)
    th_c=(th_c+math.pi)%(2*math.pi)-math.pi
    rows.append([pos,'(c) C・ロッドのA–C間','CSPがC′まわりに回る（重心がC′の真下で止まる）','%.1f'%math.degrees(th_c),'0','0','%.0f'%W,'0','当たりは考えない'])
    # (b) 鎖O–A–C：|OC|≦100の範囲で重心が最も下がる角度（伸び切れば鎖が止める）
    best=None
    for k in range(-3600,3601):
        t=math.radians(k/10); Cn=rot(C,Cp,t)
        if math.hypot(Cn[0]-L['O'][0],Cn[1]-L['O'][1])>100: continue
        Gn=rot(G,Cp,t)
        # 回転を始めの位置から連続にたどる（0から外へ）ため、|t|が小さい側から到達可能な範囲を使う
        if best is None or Gn[1]<best[1]-1e-9: best=(t,Gn[1])
    # 連続性：0から増やす・減らす両方向で、鎖が伸び切るか重心最下点に達するまで
    def sweep(sg):
        t=0.0; h=rot(G,Cp,0)[1]
        while True:
            t2=t+sg*math.radians(0.1); Cn=rot(C,Cp,t2)
            if math.hypot(Cn[0]-L['O'][0],Cn[1]-L['O'][1])>100: return t,True
            h2=rot(G,Cp,t2)[1]
            if h2>h: return t,False
            t,h=t2,h2
            if abs(t)>2*math.pi: return t,False
    # 重心が下がる向きに回る
    sg=1 if rot(G,Cp,math.radians(0.1))[1]<rot(G,Cp,0)[1] else -1
    tb,caught=sweep(sg)
    if caught:
        Cn=rot(C,Cp,tb); Gn=rot(G,Cp,tb)
        ux2,uy2=(L['O'][0]-Cn[0])/100,(L['O'][1]-Cn[1])/100
        rC2=(Cn[0]-Cp[0],Cn[1]-Cp[1]); rG2=(Gn[0]-Cp[0],Gn[1]-Cp[1])
        T2=-(rG2[0]*(-W))/(rC2[0]*uy2-rC2[1]*ux2); Fh2=W-T2*uy2; Fd2=-T2*ux2
        rows.append([pos,'(b) B・ロッドのB–A間','CSPがC′まわりに回り、鎖O–A–Cが伸び切って止まる','%.1f'%math.degrees(tb),'%.0f'%T2,'%.0f'%(T2*uy2),'%.0f'%Fh2,'%.0f'%Fd2,'止まるまでは自由に揺れる'])
    else:
        rows.append([pos,'(b) B・ロッドのB–A間','鎖が伸び切る前に重心がC′の真下に来る＝(c)と同じ','%.1f'%math.degrees(tb),'0','0','%.0f'%W,'0','鎖は効かない'])
    figdata.append((pos,L,R,G,P,Cp,th_c,tb,caught,VL))
out='/mnt/user-data/outputs/%s_%s.csv'%(TS,NAME)
with open(out,'w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f)
    w.writerow(['K059 片側の部品1個の破断とCSPの動き（左側が破断、右側は健全、LC1 W=%.1fN）'%W])
    w.writerow(['側面d-h面の2次元モデル（仮）。CSPは右C′まわりのピッチ回転のみ。駆動は健全。面外のねじり・当たりは扱わない。健全時の左C点の鉛直分担：収納 %.0fN・使用 %.0fN'%(figdata[0][9],figdata[1][9])])
    w.writerow([])
    w.writerow(['位置','破断する部品','CSPの動き','CSPの回転角(°)','左の残り部材の軸力(N)','左が持つ鉛直力(N)','右C′の鉛直力(N)','右C′の水平力 d方向(N)','備考'])
    w.writerows(rows)
# 図
fig,axs=plt.subplots(2,3,figsize=(17,11))
titles=['(a) O・OA・Aが破断','(b) B・ロッドB–A間が破断','(c) C・ロッドA–C間が破断']
for i,(pos,L,R,G,P,Cp,th_c,tb,caught,VL) in enumerate(figdata):
    for j in range(3):
        ax=axs[i][j]
        ax.axhline(268,color='#999',lw=0.8,ls=':'); ax.axhline(254.5,color='#bbb',lw=0.8,ls=':')
        ax.add_patch(Polygon(P,closed=True,fc='#2C6FB0',alpha=0.10,ec='#2C6FB0',ls='--'))
        ax.plot(*zip(R['O'],R['A']),color='#888',lw=2); ax.plot(*zip(R['B'],R['C']),color='#888',lw=2)
        ax.plot(*R['C'],'o',color='#555',ms=6)
        if j==0:
            ax.plot(*zip(L['B'],L['C']),color='#C0392B',lw=3); ax.plot(*zip(L['O'],L['A']),color='#C0392B',lw=1.5,ls=':')
            Pn=P; Cn=L['C']; txt='位置は変わらない\nロッドBCが2力部材'
        else:
            t=tb if j==1 else th_c
            Pn=[rot(p,Cp,t) for p in P]; Cn=rot(L['C'],Cp,t)
            if j==1:
                if caught:
                    Am=((L['O'][0]+Cn[0])/2,(L['O'][1]+Cn[1])/2)
                    ax.plot(*zip(L['O'],Am,Cn),color='#C0392B',lw=3)
                txt='%.0f°回って%s'%(abs(math.degrees(t)),'鎖が伸び切って止まる' if caught else '重心がC′の真下で止まる\n（鎖は効かない）')
            else: txt='%.0f°回って\n重心がC′の真下で止まる'%abs(math.degrees(t))
            ax.add_patch(Polygon(Pn,closed=True,fc='#C0392B',alpha=0.18,ec='#C0392B'))
        ax.plot(*Cn,'o',color='#C0392B',ms=6); ax.plot(*L['O'],'s',color='k',ms=5); ax.plot(*L['B'],'s',color='k',ms=5)
        ax.set_title('%s（%s）'%(titles[j],pos),fontsize=11)
        ax.text(0.02,0.04,txt,transform=ax.transAxes,fontsize=10,bbox=dict(fc='w',ec='#ccc'))
        ax.set_xlim(185,-5); ax.set_ylim(120,280); ax.set_aspect('equal'); ax.grid(alpha=0.25)
        ax.set_xlabel('d（← LP側　SC側 →）'); ax.set_ylabel('h')
fig.suptitle('K059 片側の部品1個の破断とCSPの動き（左側が破断・右側は健全、側面図、作成 %s）\n'
 '青破線：破断前のCSP／赤：破断後のCSPと左に残る部材／灰：右の機構（健全）、●C′／■左のO・B。2次元モデル（仮）、当たり・面外のねじりは扱わない'%TS,fontsize=11)
plt.tight_layout(rect=(0,0,1,0.94))
svg='/mnt/user-data/outputs/%s_%s.svg'%(TS,NAME); fig.savefig(svg); fig.savefig('/tmp/k059.png',dpi=80)
for r in rows: print(r)
