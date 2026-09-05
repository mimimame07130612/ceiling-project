import sys,os,glob,subprocess
R='/tmp/gh'; U='https://github.com/mimimame07130612/ceiling-project.git'
if not os.path.isdir(R): subprocess.run(['git','clone','--depth','1','-q',U,R],capture_output=True)
def t1():
    c=sorted(glob.glob('/home/claude/*T001*.py'))
    return c[-1] if c else None
folder=sys.argv[1]; part=sys.argv[2]; num=sys.argv[3] if len(sys.argv)>3 else ''
d=os.path.join(R,folder)
c=sorted([f for f in os.listdir(d) if part in f])
if not c:
    print('NOTFOUND'); sys.exit(1)
f=c[-1]
s=open(os.path.join(d,f),encoding='utf-8-sig').read()
if num:
    nx=str(int(num)+1); a=[]; fl=0
    for l in s.split('\n'):
        if l.startswith(num+' ') or l.startswith(num+','): fl=1
        elif l.startswith(nx+' ') or l.startswith(nx+','): fl=0
        if fl: a.append(l)
    s='\n'.join(a)
b=len(s.encode())
p=t1(); sei=0
if p:
    r=subprocess.run(['python3',p,'report'],capture_output=True,text=True).stdout.split()
    if len(r)>1: sei=int(r[1])
out=[f,str(b),str(sei)]
if b<=sei: out.append(s)
else: out.append('OVER_SEIZONRYO')
o='\n'.join(out)
print(o)
open('/tmp/t3out.txt','w').write(o)
if p: subprocess.run(['python3',p,'log','T003','0','/tmp/t3out.txt',' '.join(sys.argv)],capture_output=True)
