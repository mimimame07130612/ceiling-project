#!/bin/bash
# token-ledger installer
cat > /usr/local/bin/cmd1 <<'C1EOF'
#!/bin/bash
# cmd1 — セッション開始時に1回だけ実行。台帳を生成する。
# 使い方: cmd1 [発生元=バイト数]...
#   例: cmd1 ci=1500
#   ナレッジベース(/mnt/project)と添付(/mnt/user-data/uploads)は
#   cmd2 が自動実測するので、ここで指定する必要はない。
D=/home/claude/.tl
mkdir -p "$D"
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
# cmd2 — 各ターン冒頭で実行。ターンを進め S(n-1) を表示。
#   S(n-1)=Σ[k=1..n-1](n-k)*f(k)   f(k)=kターン目の新規増分バイト数
#   /mnt/project と /mnt/user-data/uploads の新規/変更分を自動計上する。
#   ただしテキスト形式のみ。バイナリ(xlsx/docx/zip等)はコンテキストに入らず、
#   PDF/画像は画像ブロックとして入る(妥協点b)ため除外し skip= に件数だけ出す。
#   除外分を計上したい場合は cmd4 で手動追加する。
#   出力: T=<ターン> S=<S(n-1)> nb=<前ターン非bash件数> [new=<自動計上>] [skip=<除外>]
D=/home/claude/.tl
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
    e="${p##*.}"; e=$(echo "$e" | tr 'A-Z' 'a-z')
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
NR>1 { f[$1]+=$4+$5; if($1==n-1 && $2!="bash") nb++ }
END{ for(k=1;k<n;k++) s+=(n-k)*f[k]
     if(v=="-v") for(k=1;k<n;k++) printf "f(%d)=%d\n",k,f[k]
     printf "T=%d S=%d nb=%d", n, s, nb+0
     if(nw>0) printf " new=%d", nw
     if(sk>0) printf " skip=%d", sk
     printf "\n" }' "$D/ledger.csv"
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
chmod +x /usr/local/bin/cmd[1-4]
echo ok
