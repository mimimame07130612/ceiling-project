import sys,os
L=os.environ.get('BASH_LOG','/home/claude/bash_log.tsv')
TPL="{ python3  ; } 2>/tmp/e; tail -3 /tmp/e"
ADH="{ cat >  <<'EOF'\nEOF\npython3  ; } 2>/tmp/e; tail -3 /tmp/e"
def rows():
    if not os.path.exists(L): return []
    return [l.rstrip('\n').split('\t') for l in open(L) if l.strip()]
def add(r): open(L,'a').write('\t'.join(str(x) for x in r)+'\n')
def sz(p): return os.path.getsize(p) if p and os.path.exists(p) else 0
def cur():
    v=[int(x[0]) for x in rows() if x and x[0].isdigit()]
    return max(v) if v else 1
c=sys.argv[1] if len(sys.argv)>1 else 'report'
if c=='open':
    n=sum(1 for x in rows() if len(x)>1 and x[1]=='TURN_OPEN')+1
    add([n,'TURN_OPEN',0,len(str(n))+1,len(TPL)+len(' '.join(sys.argv))])
    print(n)
elif c=='log':
    a=sys.argv[2:]
    if len(a)<=2:
        add([cur(),a[0],0,sz(a[1] if len(a)>1 else ''),0])
    else:
        src,rc,out,call=a[0],a[1],a[2],a[3]
        scr=a[4] if len(a)>4 else ''
        cb=(len(ADH)+len(scr)*3+sz(scr)) if scr else (len(TPL)+len(call))
        add([cur(),src,rc,sz(out),cb])
else:
    r=rows(); n=cur(); t=0; ob=0; cb=0; u={}
    for x in r:
        if len(x)>4 and x[0].isdigit():
            o=int(x[3]); q=int(x[4]); ob+=o; cb+=q; t+=(o+q)*(n-int(x[0])+1)
            if o==0 and q==0: u[x[1]]=u.get(x[1],0)+1
    print(t,ob+cb,len(r))
    print(' '.join(k+':'+str(v) for k,v in sorted(u.items())) or 'なし')
