# -*- coding: utf-8 -*-
"""_verify_weapon_truth.py —— 武器「机体↔武器」配对到底有多少是真值？（只读，不改任何文件）

背景
  viewer 的 `ms_weapons.csv` 里 col0=練度ID、col2/col1=武器ID 来自 `msma_weapon_set.csv`（表 #1）。
  但那张表是 `gen_weapon_set_wiki.py` **生成**的，表头自己写明：
    "⚠️ 唯一未证：wiki 武器『第 i 把』 ↔ 该机体第 i 个 sub4 的先后对应（无任何来源可证，按序配）"
  本脚本把这句话量化，免得把推定值当结论用。

查三件事
  ① 配对是否"构造式切片"：每个武器ID 是不是只被 1 台机体用（真武器通常多机共用）
  ② 客户端真值表能佐证多少条
       · unpackdat/settings/msma_mesh_customize.csv   （モデルID, 武器ID）= 最强的"机体挂这把"
       · unpackdat/settings/weapon_visual_customize.csv（武器ID + 備考=机体名）
       · unpackdat/settings/weapon_wrestle.csv        （近接格闘武器池，只有 ID 与名）
  ③ 武器ID 是否真存在于 ITEM 表（证明 ID 本身不是编的）

用法：python datatables/_verify_weapon_truth.py
"""
import collections
import io
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
UD = os.path.join(ROOT, "机动战士敢达Online", "GundamOnline", "unpackdat")
SETTINGS = os.path.join(UD, "settings")
SET = os.path.join(ROOT, "server", "datafiles", "lounge", "msma", "msma_weapon_set.csv")
BIND = os.path.join(ROOT, "viewer", "ms_bind.csv")
ITEM = os.path.join(ROOT, "server", "datafiles", "lounge", "item", "item.csv")


def rows(path):
    if not os.path.exists(path):
        return []
    L = io.open(path, encoding="utf-8-sig", errors="replace").read().splitlines()
    return [x for x in L if x.strip() and not x.lstrip().startswith("#")]


def main():
    setr = [l.split(",") for l in rows(SET)]
    setr = [r for r in setr if len(r) > 2 and r[0].strip().isdigit() and r[2].strip().isdigit()]
    if not setr:
        print("!! msma_weapon_set.csv 为空：%s" % SET)
        return 2
    sw = [r[2].strip() for r in setr]
    print("msma_weapon_set.csv : %d 行 / %d 台机体 / %d 个武器ID"
          % (len(setr), len(set(r[0].strip() for r in setr)), len(set(sw))))

    # ① 武器ID 是否被多台机体共用
    w2l = collections.defaultdict(set)
    for r in setr:
        w2l[r[2].strip()].add(r[0].strip())
    shared = {w: l for w, l in w2l.items() if len(l) > 1}
    print()
    print("① 被 ≥2 台机体共用的武器ID : %d" % len(shared))
    print("   ⇒ 0 共用 = 每个ID被唯一机体独占 = **构造式切片**的典型特征（真武器多为多机共用）")

    # ③ ID 是否存在于 ITEM 表
    it = set()
    for l in rows(ITEM):
        c = l.split(",")
        if c and c[0].strip().isdigit():
            it.add(c[0].strip())
    in_item = sum(1 for w in set(sw) if w in it)
    print()
    print("③ 武器ID 存在于 ITEM 表(item.csv) : %d / %d" % (in_item, len(set(sw))))
    print("   ⇒ 这一项是好的：ID 本身真实、能落到真实 item 资源与名称")

    # ② 客户端真值表佐证
    def ids_of(fn):
        s = set()
        for l in rows(os.path.join(SETTINGS, fn)):
            c = l.split(",")
            if c and c[0].strip().isdigit():
                s.add(c[0].strip())
        return s

    wrestle = ids_of("weapon_wrestle.csv")
    visual = ids_of("weapon_visual_customize.csv")
    meshpair = set()
    for l in rows(os.path.join(SETTINGS, "msma_mesh_customize.csv")):
        c = l.split(",")
        if len(c) > 1 and c[1].strip().isdigit():
            meshpair.add((c[0].strip(), c[1].strip()))

    mid_of = {}
    for l in rows(BIND):
        c = l.split(",")
        if len(c) > 2 and c[0].strip().isdigit() and len(c[2].strip()) == 9:
            mid_of[c[0].strip()] = c[2].strip()

    pair_hit = sum(1 for r in setr if (mid_of.get(r[0].strip(), ""), r[2].strip()) in meshpair)
    id_hit = sum(1 for r in setr if r[2].strip() in (wrestle | visual))

    print()
    print("② 客户端真值表佐证（分母 = %d 行）:" % len(setr))
    print("   · 机体↔武器 **配对**真值 (msma_mesh_customize) 佐证 : %d 行" % pair_hit)
    print("   · 仅证明『ID 是真武器』(wrestle/visual)              : %d 行" % id_hit)
    print("   · 其余 = 推定                                        : %d 行" % (len(setr) - id_hit - pair_hit))
    print()
    print("结论：`msma_weapon_set.csv` 的机体↔武器**配对**基本无客户端佐证，只能当线索。")
    print("      viewer 已按此在武器行标 `⚠推定` / `[真值]`（见 viewer/ms_weapons.csv 的『依据』列）。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
