#!/bin/bash
# token-ledger installer
cat > /usr/local/bin/cmd1 <<'C1EOF'
#!/bin/bash
# cmd1 — セッション開始時に1回だけ実行。台帳を生成する。
# 使い方: cmd1 [発生元=バイト数]...   例: cmd1 ci=1500
#   -f を付けるとバックアップを無視して新規作成する。
#   会話に紐づく退避領域に台帳が残っていれば自動復元する（コンテナ再作成からの復帰）。
#   ナレッジベースと添付は cmd2 が自動実測するので指定不要。
D=/home/claude/.tl; B=/mnt/user-data/outputs/.tl
mkdir -p "$D"
if [ "$1" = "-f" ]; then shift; rm -rf "$B"; fi
if [ -f "$B/ledger.csv" ]; then
  cp "$B/ledger.csv" "$D/ledger.csv"; cp "$B/turn" "$D/turn" 2>/dev/null || echo 0 > "$D/turn"
  cp "$B/seen" "$D/seen" 2>/dev/null || : > "$D/seen"
  echo "restored T=$(cat "$D/turn")"; exit 0
fi
echo "turn,source,exit,out,cmd" > "$D/ledger.csv"
echo 0 > "$D/turn"; : > "$D/seen"
for a in "$@"; do
  s="${a%%=*}"; b="${a##*=}"
  case "$b" in ''|*[!0-9]*) echo "cmd1: 不正: $a" >&2; continue;; esac
  echo "1,$s,0,$b,0" >> "$D/ledger.csv"
done
echo "ledger ready"
C1EOF
cat > /usr/local/bin/cmd2 <<'C2EOF'
#!/bin/bash
# cmd2 — 各ターン冒頭で実行。ターンを進め、ひとつ前のターンまでの状況を表示。
#   T   = 現在のターン数 n
#   F   = f(n-1)  直前ターン単体の滞留量
#   S   = S(n-1) = Σ[k=1..n-1](n-k)*f(k)  累計滞留量
#   err = 直前ターンで終了コードが非0だった件数
#   A   = 現在の常駐量 Σf(k)（バイト）。1ターン進めるときの再送コスト。cmd5の判定閾値。
#   nb  = 直前ターンの非bash計上件数（記入漏れ検知用）
#   /mnt/project と /mnt/user-data/uploads の新規/変更分を自動計上（テキスト形式のみ）。
#   バイナリ・PDF・画像は除外し skip= に件数のみ表示。必要なら cmd4 で手動追加。
#   cmd2 -v で f(k) の内訳
D=/home/claude/.tl; B=/mnt/user-data/outputs/.tl
[ -f "$D/ledger.csv" ] || { echo "no ledger; run cmd1" >&2; exit 1; }
n=$(( $(cat "$D/turn") + 1 )); echo "$n" > "$D/turn"
TXT='txt|md|markdown|csv|tsv|html|htm|xml|json|yaml|yml|svg|sh|bash|py|js|mjs|ts|jsx|tsx|css|scss|sql|ini|conf|cfg|toml|log|tex|c|h|cpp|hpp|java|rb|go|rs|php|pl|r|lua|swift|kt|bat|ps1|env|gitignore|dockerfile|make|mk'
new=0; skip=0
scan(){ [ -d "$1" ] || return
  while IFS='|' read -r p sz mt; do
    [ -n "$p" ] || continue
    k="$p|$sz|$mt"
    grep -qxF "$k" "$D/seen" 2>/dev/null && continue
    echo "$k" >> "$D/seen"
    e=$(echo "${p##*.}" | tr 'A-Z' 'a-z')
    if echo "$e" | grep -qxE "$TXT"; then
      echo "$n,$2,0,$sz,0" >> "$D/ledger.csv"; new=$((new+1))
    else
      echo "$n,${2}-skip,0,0,0" >> "$D/ledger.csv"; skip=$((skip+1))
    fi
  done < <(find "$1" -type f -printf '%p|%s|%T@\n' 2>/dev/null)
}
scan /mnt/project kb
scan /mnt/user-data/uploads upload
awk -F, -v n="$n" -v v="$1" -v nw="$new" -v sk="$skip" '
NR>1 { f[$1]+=$4+$5; a+=$4+$5
       if($1==n-1){ if($3+0!=0) er++; if($2!="bash") nb++ } }
END{ for(k=1;k<n;k++) s+=(n-k)*f[k]
     if(v=="-v") for(k=1;k<n;k++) printf "f(%d)=%d\n",k,f[k]
     printf "T=%d F=%d A=%d S=%d err=%d nb=%d", n, f[n-1]+0, a+0, s, er+0, nb+0
     if(nw>0) printf " new=%d", nw
     if(sk>0) printf " skip=%d", sk
     printf "\n" }' "$D/ledger.csv"
mkdir -p "$B" 2>/dev/null && cp "$D/ledger.csv" "$D/turn" "$D/seen" "$B/" 2>/dev/null
C2EOF
cat > /usr/local/bin/cmd3 <<'C3EOF'
#!/bin/bash
# cmd3 — bashコマンドのラッパ。実行し、台帳に自動記載する。
# 使い方: cmd3 'コマンド文字列'
#   コマンド文バイト数・終了コード・出力バイト数を実測して記載し、出力をそのまま表示する。
D=/home/claude/.tl
[ -f "$D/ledger.csv" ] || { echo "cmd3: 台帳なし。先に cmd1 を実行" >&2; exit 1; }
c="$1"
cb=$(printf '%s' "$c" | wc -c)
o=$(eval "$c" 2>&1); rc=$?
ob=$(printf '%s\n' "$o" | wc -c)
[ -z "$o" ] && ob=0
t=$(cat "$D/turn")
printf '%s,bash,%s,%s,%s\n' "$t" "$rc" "$ob" "$cb" >> "$D/ledger.csv"
[ -n "$o" ] && printf '%s\n' "$o"
exit $rc
C3EOF
cat > /usr/local/bin/cmd4 <<'C4EOF'
#!/bin/bash
# cmd4 — bashを経由しない経路の手動計上。
# 使い方: cmd4 <発生元> <バイト数> [ターン番号]
#   例: cmd4 dropbox 8432          現在のターンに計上
#       cmd4 dropbox 8432 4        4ターン目に遡って計上（記入漏れの訂正）
D=/home/claude/.tl
[ -f "$D/ledger.csv" ] || { echo "cmd4: 台帳なし。先に cmd1 を実行" >&2; exit 1; }
s="$1"; b="$2"; t="${3:-$(cat "$D/turn")}"
[ -n "$s" ] && [ -n "$b" ] || { echo "cmd4: 発生元とバイト数が必要" >&2; exit 1; }
case "$b" in ''|*[!0-9]*) echo "cmd4: バイト数が不正: $b" >&2; exit 1;; esac
echo "$t,$s,0,$b,0" >> "$D/ledger.csv"
echo "logged: T$t $s ${b}B"
C4EOF
cat > /usr/local/bin/cmd5 <<'C5EOF'
#!/bin/bash
# cmd5 — GitHubから該当範囲だけを、サイズ判定つきで取得する。
# 使い方: cmd3 'cmd5 <フォルダ> <ファイル名片> [見出し番号|?] [ex]'
#   見出し番号省略 = 全文 / ? = 見出し一覧 / ex = サイズ超過でも強制取得
#   判定: 抽出バイト数 nb <= 現在の常駐量 A なら自動取得。
#         超過時は本文を出さず nb と A だけ返すので、承認後に ex を付けて再実行する。
#   必ず cmd3 経由で呼ぶこと（出力バイト数が台帳に記載される）。
D=/home/claude/.tl
[ -f "$D/ledger.csv" ] || { echo "cmd5: 台帳なし。先に cmd1 を実行" >&2; exit 1; }
REPO="${TL_REPO:-mimimame07130612/ceiling-project}"
BR="${TL_BRANCH:-main}"
N="${REPO##*/}"
R=$(ls -d /tmp/$N-* 2>/dev/null | head -1)
if [ -z "$R" ]; then
  curl -sL "https://codeload.github.com/$REPO/tar.gz/refs/heads/$BR" -o /tmp/$N.tgz || { echo "cmd5: 取得失敗" >&2; exit 1; }
  tar xzf /tmp/$N.tgz -C /tmp || { echo "cmd5: 展開失敗" >&2; exit 1; }
  R=$(ls -d /tmp/$N-* 2>/dev/null | head -1)
fi
[ -n "$R" ] || { echo "cmd5: アーカイブなし" >&2; exit 1; }
TL_ROOT="$R" python3 - "$@" <<'PY'
import sys, os, glob, csv
folder = sys.argv[1] if len(sys.argv) > 1 else ''
part   = sys.argv[2] if len(sys.argv) > 2 else ''
num    = sys.argv[3] if len(sys.argv) > 3 else ''
ex     = sys.argv[4] if len(sys.argv) > 4 else ''
root = os.environ['TL_ROOT']
cands = []
for dp, dn, fn in os.walk(root):
    if folder and folder not in dp: continue
    for f in fn:
        if part in f: cands.append(os.path.join(dp, f))
if not cands:
    print('NOT_FOUND', folder, part); raise SystemExit(1)
p = sorted(cands, key=lambda q: os.path.basename(q))[-1]
lines = open(p, encoding='utf-8-sig').read().split('\n')
print(os.path.basename(p))
def blankish(s): return s.strip(' \u3000,\t') == ''
def is_head(i):
    if lines[i].startswith('#'): return True
    if blankish(lines[i]) or len(lines[i]) > 40: return False
    return i == 0 or blankish(lines[i-1])
heads = [i for i in range(len(lines)) if is_head(i)]
if num == '?':
    body = '\n'.join('%d %s' % (i+1, lines[i][:32]) for i in heads)
elif num:
    st = None
    for j, i in enumerate(heads):
        if lines[i].lstrip('#').strip().startswith(num):
            st = i; en = len(lines)
            if lines[i].startswith('#'):
                lv = len(lines[i]) - len(lines[i].lstrip('#'))
                for k in heads[j+1:]:
                    if lines[k].startswith('#') and len(lines[k])-len(lines[k].lstrip('#')) <= lv:
                        en = k; break
            elif j+1 < len(heads): en = heads[j+1]
            break
    if st is None:
        print('NO_SECTION', num); raise SystemExit(1)
    print('RANGE %d-%d' % (st+1, en))
    body = '\n'.join(lines[st:en])
else:
    body = '\n'.join(lines)
nb = len(body.encode())
alive = 0
with open('/home/claude/.tl/ledger.csv') as fh:
    for r in csv.DictReader(fh):
        alive += int(r['out']) + int(r['cmd'])
print('nb=%d A=%d' % (nb, alive))
if ex or nb <= alive:
    print(body)
else:
    print('HOLD 承認後に ex を付けて再実行')
PY
C5EOF
chmod +x /usr/local/bin/cmd[1-5]
echo ok
