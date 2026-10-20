# -*- coding: utf-8 -*-
"""按**族**抽出"纯 S→C 推送"的入口，写 `_case_addrs.txt` 供 `dump_case_calls.py` 用。

为什么需要它：`lobby_inventory.md` 末尾 `<details>` 里列了 **139 条纯推送**（客户端从不请求、
只能服务端主动推 ✓）。它们**按族成批**出现（pilot 17 / dailycup 9 / party 7 / msma 6 …）
⇒ 一次侦察**整族** = 一次 IDA 调用量出十几条结构 ✓✓（比逐条查快一个数量级 ✓）

用法：
    python dump_family_pushes.py pilot          # 只列**未实现**(✗)的
    python dump_family_pushes.py pilot all      # 连已实现的也列
    python dump_family_pushes.py                # 不带参数 = 打印全族统计

输出：`reverse-login-chain/tools/_case_addrs.txt`（每行 `0xADDR # 0xID 名字`）
     然后跑 `dump_case_calls.py`（IDA 侧）即可。

★列名：| 名字 | ID | 客户端 entry | Go 有线? |
"""
import collections
import io
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

MD = r"F:\9ymsgo\9you\server\docs\lobby_inventory.md"
OUT = r"F:\9ymsgo\9you\reverse-login-chain\tools\_case_addrs.txt"
ROW = re.compile(
    r"^\|\s*`([^`]+)`\s*\|\s*`(0x[0-9A-Fa-f]+)`\s*\|\s*`(0xb[0-9a-f]+)`\s*\|\s*([\u2713\u2717])\s*\|",
    re.M,
)


def load():
    t = open(MD, encoding="utf-8").read()
    return ROW.findall(t[t.find("<details>"):])


def main():
    rows = load()
    fam = collections.defaultdict(list)
    for n, hid, e, g in rows:
        fam[n.split("_")[0]].append((n, hid, e, g))

    if len(sys.argv) < 2:
        print("纯推送 %d 条，%d 族；未实现：\n" % (len(rows), len(fam)))
        for k in sorted(fam, key=lambda x: -len(fam[x])):
            miss = sum(1 for r in fam[k] if r[3] == "\u2717")
            print("  %-16s 共 %2d，未实现 %2d" % (k, len(fam[k]), miss))
        return

    wants = [a for a in sys.argv[1:] if a != "all"]
    only_missing = "all" not in sys.argv
    pick = []
    for want in wants:
        pick += [r for r in fam.get(want, []) if r[3] == "\u2717" or not only_missing]
    if not pick:
        print("族 %s：没有匹配（已实现完 / 族名打错？）" % ",".join(wants))
        return
    print("族 %s：取 %d 条 ⇒ 写入 %s" % ("+".join(wants), len(pick), OUT))
    with open(OUT, "w", encoding="utf-8") as fh:
        for n, hid, e, g in pick:
            fh.write("%s  # %s %s\n" % (e.upper(), hid, n))
    for n, hid, e, g in pick:
        print("   %-42s %-8s entry=%s" % (n, hid, e))


if __name__ == "__main__":
    main()
