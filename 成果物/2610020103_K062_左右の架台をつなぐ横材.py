# K062 左右の架台をつなぐ横材（STEP4 4-3、地震の左右揺れ対策 案1）
# K056の重ね描きJSON（2610012215_K056_梁への架台の取付け.json）に、横材（仮 断面4×6、x=90.5〜169、d≈52〜58、h≈264〜270）を追加して sanmen.py で描く。
# 数値の根拠：K061（地震の左右揺れと横材）、K060（片側故障後のねじの力）。前提はすべて仮。
import json,subprocess,glob
SAN=sorted(glob.glob('/home/claude/ceiling-project/ツール/*_sanmen.py'))[-1]
J=json.load(open(sorted(glob.glob('/mnt/user-data/outputs/*K056*.json'))[-1],encoding='utf-8'))
TC='#8E44AD'
J['items'].append(dict(t='box3',p=[90.5,169.0,46.0,50.0,264.0,270.0],color=TC,fill=TC,op=0.45,w=1.4,dash=True))
J['items'].append(dict(t='text',view='plan',p=[130,52],s='(横材 d≈46〜50)',dx=0,dy=-6,anchor='middle',color=TC))
J['items'].append(dict(t='text',view='front',p=[130,270],s='(横材 h≈264〜270)',dx=0,dy=-6,anchor='middle',color=TC))
J['legend'].append(dict(text='紫：左右の架台をつなぐ横材（案1、仮 4×6）',color=TC,kind='band'))
J['title_note']=['STEP4 4-3 地震の左右揺れ対策 案1：左右の架台（K056）をSC側の端で横材（紫、仮 断面4×6、x=90.5〜169、d≈46〜50、h≈264〜270）でつなぎ、1つの枠にする。左の架台はd=46まで延ばす（仮）。',
 'K061：使用位置・地震（KH=2.0）でねじ6本/片側・1本抜け×4の必要引抜き耐力が 左2,702→301、右4,485→281 N に下がる。片側故障後のねじり（K060）も枠で受ける（引抜き5N以下、確認値）。',
 '収納時CSPの上角（h≥264でd≥53.6）・左Oの軸受け（d≥50.73）・照明（d=130）に当たらない位置。掘込前壁との間0.5、左軸受けとの間0.73。前提はすべて仮：横材と架台は剛、横材はSC側の端の1本のみ（LP側の端は照明d=175に近い）。リンク面 左x=92.0・右x=168.0、wR=0。']
J['src']=J.get('src',[])+['K057','K060','K061']
json.dump(J,open('/tmp/k062.json','w',encoding='utf-8'),ensure_ascii=False)
subprocess.run(['python3',SAN,'--zuban','K062','--title','左右の架台をつなぐ横材','-o','/mnt/user-data/outputs/{ts}_K062_左右の架台をつなぐ横材.svg','/tmp/k062.json'],check=True)
