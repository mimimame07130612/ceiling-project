import os,re,shutil,subprocess,sys
ROOT="/tmp/ceiling-project-main"
DST="/home/claude"
d=os.path.join(ROOT,"ツール")
best={}
for f in os.listdir(d):
    m=re.search(r"T\d{3}",f); p=re.match(r"(\d{10})_",f)
    if m and p:
        k=m.group(0)
        if k not in best or p.group(1)>best[k][0]: best[k]=(p.group(1),f)
saved=[]
for k in sorted(best):
    shutil.copy(os.path.join(d,best[k][1]),os.path.join(DST,best[k][1])); saved.append(best[k][1])
t1=[f for f in saved if "T001" in f][0]
turn=subprocess.run([sys.executable,os.path.join(DST,t1),"open"],capture_output=True,text=True).stdout.strip()
ts=subprocess.run(["bash","-c","TZ=Asia/Tokyo date +%y%m%d%H%M"],capture_output=True,text=True).stdout.strip()
print(turn,ts)
for s in saved: print(s)
