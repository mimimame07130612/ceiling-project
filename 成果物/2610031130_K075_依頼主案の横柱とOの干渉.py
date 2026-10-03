# K075 依頼主案（O移動・横柱3本）の干渉の確認（STEP4 4-3）
# 依頼主案：① O を h=266・d=50 に（右 O′ は d=68：左右の差18を保つ、依頼主回答）。② 左右の架台の間に横柱 SF-20・20（20×20、アルミ）を3本：
#   (h=269, d=47)・(h=269, d=53)・(h=263, d=47)。③ 架台（板厚8）の上に鉄板 T=10 を重ねてOの支点を立てる（鉄板の大きさは未回答のため描かない）。
# 機構（リンク・CSP）は、K062の配置を d−2.73・h−2 だけ平行移動したもの（CSPも一緒に2下がる場合）。CSPを今の高さのままにする場合は、CSPの外形だけ d−2.73 で重ねる（紫破線、リンクは未設計）。
# Oの軸受けの大きさは未定のため、O・O′のまわりに半径2の円（仮）を描く。架台は板厚0.8（左 x=89.5〜90.3、右 169.2〜170）、横柱は x=90.3〜169.2。
import json,subprocess,glob,copy
SAN=sorted(glob.glob('/home/claude/ceiling-project/ツール/*_sanmen.py'))[-1]
J=json.load(open(sorted(glob.glob('/mnt/user-data/outputs/2610020103_K062*.json'))[-1],encoding='utf-8'))
DD,DH=-2.73,-2.0
items=[]
def sh(it):
    it=copy.deepcopy(it); v=it.get('view'); p=it['p']
    def f(u,w):
        if v=='side': return [round(u+DD,2),round(w+DH,2)]
        if v=='plan': return [u,round(w+DD,2)]
        if v=='front': return [u,round(w+DH,2)]
    if it['t'] in ('line','poly'): it['p']=[f(*q) for q in p]
    elif it['t'] in ('pt','text','circle'): it['p']=f(*p)
    elif it['t']=='rect':
        a=f(p[0],p[1]); b=f(p[2],p[3]); it['p']=a+b
    return it
for k,it in enumerate(J['items']):
    if k in (6,7,8,19,20,21,50,51,52): continue
    if it['t']=='text' and k==41: continue
    items.append(sh(it))
# CSPを今の高さのまま（d−2.73のみ）
c2=copy.deepcopy(J['items'][2]); c2['p']=[[round(u+DD,2),w] for u,w in c2['p']]; c2.update(color='#8E44AD',fill='none',op=0,dash=True,w=1.2); items.append(c2)
# 架台（板厚0.8）
FR='#5F5E5A'
for xb0,xb1,d1,dash in ((89.5,90.3,165.99,False),(169.2,170.0,183.99,True)):
    items.append(dict(t='rect',view='plan',p=[xb0,46.0,xb1,d1],color=FR,fill=FR,op=0.6,w=1.2))
    items.append(dict(t='rect',view='front',p=[xb0,254.5,xb1,270],color=FR,fill=FR,op=0.6,w=1.2))
    items.append(dict(t='rect',view='side',p=[46.0,254.5,d1,270],color=FR,fill='none',op=0,w=1.0,dash=dash))
# 横柱 SF-20・20
PC='#E67E22'
for h,d in ((269,47),(269,53),(263,47)):
    items.append(dict(t='box3',p=[90.3,169.2,d-1,d+1,h-1,h+1],color=PC,fill=PC,op=0.55,w=1.2))
    items.append(dict(t='text',view='side',p=[d,h],s='(柱 h=%d,d=%d)'%(h,d),dx=0,dy=-10 if h==269 and d==53 else 14,anchor='start' if d==53 else 'end',color=PC))
# 軸受けの仮の大きさ
for d,lab in ((50.0,'O'),(68.0,'O′')):
    items.append(dict(t='circle',view='side',p=[d,266.0],r=2.0,color='#111',fill='none',dash=True,w=1.0))
J['items']=items
J['legend']=[l for l in J['legend'] if '横材' not in l['text']]+[
 dict(text='橙：横柱 SF-20・20（20×20、依頼主案、3本）',color=PC,kind='band'),
 dict(text='紫破線：CSP 収納（高さは今のまま、dだけ移動した場合）',color='#8E44AD',dash=True,kind='line'),
 dict(text='黒破線の円：Oの軸受けの仮の大きさ（半径2）',color='#111',dash=True,kind='ring')]
J['title_note']=['STEP4 4-3 依頼主案の干渉確認：O を h=266・d=50、O′ を h=266・d=68 に移し（機構とCSPは d−2.73・h−2 の平行移動）、左右の架台（板厚8）の間に横柱 SF-20・20 を3本（h=269・d=47、h=269・d=53、h=263・d=47）。',
 '紫破線はCSPの高さを今のまま（dだけ−2.73）にした場合の収納時の外形（リンクは未設計）。鉄板T=10（③）は大きさ未定のため描いていない。',
 '前提はすべて仮：軸受けの大きさ（半径2）、架台 左x=89.5〜90.3・右169.2〜170、横柱 x=90.3〜169.2、リンク面 左x=92.0・右x=168.0、wR=0。']
J['src']=J.get('src',[])+['K071','依頼主案（SF-20・20 ミスミ/モノタロウ）']
json.dump(J,open('/mnt/user-data/outputs/2610031130_K075_依頼主案の横柱とOの干渉.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
subprocess.run(['python3',SAN,'--zuban','K075','--title','依頼主案の横柱とOの干渉','-o','/mnt/user-data/outputs/{ts}_K075_依頼主案の横柱とOの干渉.svg','/mnt/user-data/outputs/2610031130_K075_依頼主案の横柱とOの干渉.json'],check=True)
