# -*- coding: utf-8 -*-
import csv, collections, io, sys, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

def rd(p):
    with open(p, encoding="utf-8", errors="replace") as f:
        return [r for r in csv.reader(f.read().replace("\r\n", "\n").split("\n"))
                if r and any(x.strip() for x in r)]

def keyset(p, kc=1):
    out = collections.Counter()
    for r in rd(p):
        if r[0].lstrip("\ufeff").startswith("#"):
            continue
        if len(r) > kc:
            out[r[kc].strip()] += 1
    return out

CUR = r"server\datafiles\lounge\item\weapon_battle_detail.csv"
A = r"server\datafiles\lounge\item\weapon_battle_detail.csv.bak_purge20261004_234510"
B = r"server\datafiles\lounge\item\weapon_battle_detail.csv.bak_purge20261004_234525"
a, b, c = keyset(A), keyset(B), keyset(CUR)
print("原始(234510, %d B) 键 %d 行 %d" % (os.path.getsize(A), len(a), sum(a.values())))
print("中间(234525, %d B) 键 %d 行 %d" % (os.path.getsize(B), len(b), sum(b.values())))
print("当前(        %d B) 键 %d 行 %d" % (os.path.getsize(CUR), len(c), sum(c.values())))
print()
print("Δ 原始→中间：删键 %d，删行 %d" % (len(set(a) - set(b)), sum(a.values()) - sum(b.values())))
print("Δ 中间→当前：删键 %d，删行 %d" % (len(set(b) - set(c)), sum(b.values()) - sum(c.values())))
print()
print("原始里有、当前没有的键（前若干，按长度分桶）：")
gone = set(a) - set(c)
print("  共 %d 个；长度分布 %s" % (len(gone), dict(sorted(collections.Counter(len(k) for k in gone).items()))))
print("  含 2840151？%s   含 02840151？%s" % ("2840151" in gone, "02840151" in gone))
print("  当前 CSV 仍有 2840151？ %s" % ("2840151" in c))
print("  原始 CSV 有 02840151 吗？ %s" % ("02840151" in a))
print()
print("原始 CSV 键长分布 %s" % dict(sorted(collections.Counter(len(k) for k in a).items())))
print("当前 CSV 键长分布 %s" % dict(sorted(collections.Counter(len(k) for k in c).items())))
