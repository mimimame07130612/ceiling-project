import subprocess,sys,os,glob
T1=sorted(glob.glob('/home/claude/*_T001_*.py'))[-1]
tgt=sys.argv[1];args=sys.argv[2:]
out='/tmp/t004out.txt'
f=open(out,'w')
r=subprocess.run(['python3',tgt]+args,stdout=f)
f.close()
sys.stdout.write(open(out,encoding='utf-8',errors='replace').read())
subprocess.run(['python3',T1,'log',os.path.basename(tgt),str(r.returncode),out,' '.join(sys.argv)],capture_output=True)
