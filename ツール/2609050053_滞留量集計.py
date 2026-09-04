# 滞留量集計
# 用途 : bash_log.tsv から滞留量の総合計・生存量・行数を算出する
# 使用 : python3 滞留量集計.py <申告時点のターン番号>
# 入力 : /home/claude/bash_log.tsv  5列 TSV
#        ターン番号 / 発生元 / 終了コード / 出力バイト数 / コマンド文バイト数
# 出力 : 標準出力に「滞留量 生存量 行数」を空白区切りで1行
# 仕様 : 滞留量 = Σ (出力バイト + コマンド文バイト) x (申告ターン - 発生ターン + 1)
#        生存量 = Σ (出力バイト + コマンド文バイト)   経過ターン数を乗じない
#        台帳が無いときは 0 を返さずエラー終了する
import sys, csv, os
L = '/home/claude/bash_log.tsv'
if len(sys.argv) < 2:
    sys.exit('usage: python3 滞留量集計.py <turn>')
if not os.path.exists(L):
    sys.exit('ledger not found: ' + L)
t = int(sys.argv[1])
tot = al = n = 0
for r in csv.reader(open(L, encoding='utf-8'), delimiter='\t'):
    if len(r) < 5:
        continue
    b = int(r[3]) + int(r[4])
    tot += b * (t - int(r[0]) + 1)
    al += b
    n += 1
print(tot, al, n)
