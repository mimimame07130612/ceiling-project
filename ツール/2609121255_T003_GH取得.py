import sys, os, glob, subprocess

folder = sys.argv[1]
part = sys.argv[2]
num = sys.argv[3] if len(sys.argv) > 3 else ''
ex = sys.argv[4] if len(sys.argv) > 4 else ''

roots = sorted(glob.glob('/tmp/ceiling-project-*'))
if not roots:
    print('NO_ARCHIVE 5-10 not executed')
    raise SystemExit(1)
root = roots[0]

cands = []
for dp, dn, fn in os.walk(root):
    if folder and folder not in dp:
        continue
    for f in fn:
        if part in f:
            cands.append(os.path.join(dp, f))
if not cands:
    print('NOT_FOUND', folder, part)
    raise SystemExit(1)
p = sorted(cands, key=lambda q: os.path.basename(q))[-1]
lines = open(p, encoding='utf-8-sig').read().split('\n')
print(os.path.basename(p))


def blankish(s):
    return s.strip(' \u3000,\t') == ''


def is_head(i):
    if lines[i].startswith('#'):
        return True
    if blankish(lines[i]) or len(lines[i]) > 40:
        return False
    return i == 0 or blankish(lines[i - 1])


heads = [i for i in range(len(lines)) if is_head(i)]

if num == '?':
    body = '\n'.join('%d %s' % (i + 1, lines[i][:32]) for i in heads)
elif num:
    st = None
    for j, i in enumerate(heads):
        if lines[i].lstrip('#').strip().startswith(num):
            st = i
            en = len(lines)
            if lines[i].startswith('#'):
                lv = len(lines[i]) - len(lines[i].lstrip('#'))
                for k in heads[j + 1:]:
                    if lines[k].startswith('#') and len(lines[k]) - len(lines[k].lstrip('#')) <= lv:
                        en = k
                        break
            elif j + 1 < len(heads):
                en = heads[j + 1]
            break
    if st is None:
        print('NO_SECTION', num)
        raise SystemExit(1)
    print('RANGE %d-%d' % (st + 1, en))
    body = '\n'.join(lines[st:en])
else:
    body = '\n'.join(lines)

nb = len(body.encode())
print(nb)
t1 = sorted(glob.glob('/home/claude/*T001*.py'))[-1]
alive = int(subprocess.run(['python3', t1, 'report'],
                           capture_output=True, text=True).stdout.split()[1])
print(alive)
if ex or nb <= alive:
    print(body)
