# K071 架台・ねじ（案(D3)）・横材・モーターの配置（STEP4 4-3）
# K062の重ね描きJSONをもとに、(1) 右の架台を d=46 まで延ばし（仮、K068で置いた条件）、左の架台の描画も d=46 からに直し（K062の注記どおり）、
# (2) 梁のねじ（案(D3)：O・B使用位置・B収納位置の d±5 に h=257・268 の上下2本ずつ＝12本/片側）を描き、
# モーター・レールとの位置関係、ねじの端あき（梁の下面 h=254.5、掘込面 h=270）を見る。数値の根拠：K070。前提はすべて仮。
import json,subprocess,glob
SAN=sorted(glob.glob('/home/claude/ceiling-project/ツール/*_sanmen.py'))[-1]
J=json.load(open(sorted(glob.glob('/mnt/user-data/outputs/2610020103_K062*.json'))[-1],encoding='utf-8'))
it=J['items']
it[6]['p']=[89.5,46.0,90.5,165.99]; it[8]['p']=[46.0,254.5,165.99,270]
it[19]['p']=[169.0,46.0,170,183.99]; it[21]['p']=[46.0,254.5,183.99,270]
SC='#000000'; SCR_R='#555555'
def around(c): return [c-5,c+5]
SCR={'左':around(52.73)+around(106.56)+around(151.98),'右':around(70.73)+around(124.56)+around(169.98)}
for sn,ds in SCR.items():
    xb=89.5 if sn=='左' else 170.0
    for d in ds:
        for h in (257.0,268.0):
            it.append(dict(t='pt',view='side',p=[round(d,2),h],color=SC if sn=='左' else SCR_R,r=2.2,ring=(sn=='右')))
        it.append(dict(t='pt',view='plan',p=[xb,round(d,2)],color=SC if sn=='左' else SCR_R,r=1.8,ring=(sn=='右')))
# モーター（側面図）
it.append(dict(t='rect',view='side',p=[157.99,258,165.99,266],color='#D85A30',fill='#D85A30',op=0.35,w=1.0))
it.append(dict(t='rect',view='side',p=[175.99,258,183.99,266],color='#D85A30',fill='none',op=0,w=1.0,dash=True))
# 寸法の文字（側面図）
it.append(dict(t='text',view='side',p=[30,257],s='(ねじ h=257：梁の下面から2.5)',dx=0,dy=4,anchor='end',color=SC))
it.append(dict(t='text',view='side',p=[30,268],s='(ねじ h=268：掘込面から2)',dx=0,dy=-2,anchor='end',color=SC))
it.append(dict(t='text',view='side',p=[150,238],s='(B収納まわりのねじ 左d≈147〜157 / モーター 左d≈158〜166：すき間約1)',dx=0,dy=0,anchor='start',color='#D85A30'))
J['legend']+= [dict(text='黒点：梁のねじ 左（案(D3) 12本/片側、仮）',color=SC,kind='dot'),
               dict(text='灰の輪：梁のねじ 右（案(D3) 12本/片側、仮）',color=SCR_R,kind='ring')]
J['title_note']=['STEP4 4-3 架台とねじの配置：梁のねじを案(D3)（O・B使用位置・B収納位置のd±5に、h=257・268の上下2本ずつ、12本/片側、仮）とした配置。右の架台もd=46まで延ばし（仮）、横材（紫、d≈46〜50）を左右の架台に取り付ける。',
 'K070：使用位置・地震（KH=2.0）で1本抜け×4の必要引抜き耐力 最大2,297N（右、ks=20,000）。ねじ長45の下限3.63kN（K063）に対し余裕あり、ねじ長30の下限1.82kNには不足のおそれ。',
 '未確認：ねじの端あき・間隔の規定（d方向の間隔10、梁の下面から2.5、掘込面から2）、ねじのばねks。B収納位置まわりのねじはモーター（橙）のすぐ横（すき間約1）。前提はすべて仮：リンク面 左x=92.0・右x=168.0、wR=0。']
J['src']=J.get('src',[])+['K068','K070']
json.dump(J,open('/mnt/user-data/outputs/2610031002_K071_架台とねじの配置.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
subprocess.run(['python3',SAN,'--zuban','K071','--title','架台とねじの配置','-o','/mnt/user-data/outputs/{ts}_K071_架台とねじの配置.svg','/mnt/user-data/outputs/2610031002_K071_架台とねじの配置.json'],check=True)
