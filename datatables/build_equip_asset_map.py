# -*- coding: utf-8 -*-
"""build_equip_asset_map.py —— 从**资源包**生成「装备ID ↔ 资源ID」映射表。

资源包（unpackdat/item/，实测 11791 文件 / 1445 个含武器模型的目录）：
    item/<类2位>/<号4或6位>/model/EM_<类>_<号>_<NN>.dxg   ← ★EM_ 就是武器/装备本体
    item/<类2位>/<号>/{attr/EZ_*.vra, tex/ET_*.dds, anim/EA_*.mrb}

★装备ID ↔ 资源ID 的换算（IDA `sub_596290` 十进制拆位 + 实测）
    · 类 = ID 首位（补零 2 位）              1040101 → item/01/...
    · 号 = ID 末 4 位（4 位号模板）          1040101 → …/0101/
    · 6 位号模板（少数目录，65 个号）：号 = ID[1:7]   200110001 → item/02/001100
    · 中间段（如 7 位 ID 的 "04"）是"实例/子类段"，**不进路径**（同一资源可被多个 ID 指向）
  实测命中：weapon_set 266 个武器ID → 264 命中；图标池 1391 命中；物品ID全集 3351 自洽。

产出
  names/装备ID-资源ID映射表.csv   一行一个装备ID（资源坐标 / EM模型 / 属性 / 贴图 / 名称 / 来源）
  names/装备资源-无ID目录.csv     资源包里存在、但没有任何已知 ID 指向的目录（缺口）
用法：python datatables/build_equip_asset_map.py
"""
import collections
import io
import os
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
UD = os.path.join(ROOT, "机动战士敢达Online", "GundamOnline", "unpackdat")
ITEM_DIR = os.path.join(UD, "item")
SETTINGS = os.path.join(UD, "settings")
ICON_DIR = os.path.join(UD, "interface", "icon", "item", "d")
SERVER = os.path.join(ROOT, "server", "datafiles", "lounge", "msma")
SERVER_ITEM = os.path.join(ROOT, "server", "datafiles", "lounge", "item")

OUT_MAP = os.path.join(HERE, "names", "装备ID-资源ID映射表.csv")
OUT_GAP = os.path.join(HERE, "names", "装备资源-无ID目录.csv")
OUT_WEAPONS = os.path.join(ROOT, "viewer", "ms_weapons.csv")   # viewer 用：練度ID → 武器ID → item 资源
BIND = os.path.join(ROOT, "viewer", "ms_bind.csv")             # 練度ID → モデルID（用于给武器行标依据）
OUT_ITEM_BIND = os.path.join(ROOT, "viewer", "item_bind.csv")  # viewer 用：item 资源 → 代表装备ID
OUT_ITEM_NAMES = os.path.join(ROOT, "viewer", "item_names.csv")  # viewer 用：装备ID → 名称（item/item.csv col0/col2）

HEAD_MAP = ("#装备ID,名称,类型,资源ID,资源类,资源号,模板,模型EM数,模型EM,属性EZ,贴图ET数,动画EA数,"
            "资源存在,来源,")


def rows(path):
    if not os.path.exists(path):
        return []
    L = io.open(path, encoding="utf-8-sig", errors="replace").read().splitlines()
    return [x for x in L if x.strip() and not x.lstrip().startswith("#")]


def scan_assets():
    """枚举资源包 → {(类, 号): {model:[], attr:[], tex:n, anim:n}}"""
    res = {}
    if not os.path.isdir(ITEM_DIR):
        return res
    for cat in sorted(os.listdir(ITEM_DIR)):
        p1 = os.path.join(ITEM_DIR, cat)
        if not os.path.isdir(p1):
            continue
        for num in sorted(os.listdir(p1)):
            p2 = os.path.join(p1, num)
            if not os.path.isdir(p2):
                continue
            e = res.setdefault((cat, num), {"model": [], "attr": [], "tex": 0, "anim": 0})
            for kind, pref, key in (("model", "EM_", "model"), ("attr", "EZ_", "attr"),
                                    ("tex", "ET_", None), ("anim", "EA_", None)):
                p3 = os.path.join(p2, kind)
                if not os.path.isdir(p3):
                    continue
                for f in sorted(os.listdir(p3)):
                    if key == "model" and f.upper().startswith(pref):
                        e["model"].append(f)
                    elif key == "attr" and f.upper().startswith(pref):
                        e["attr"].append(f)
                    elif kind == "tex":
                        e["tex"] += 1
                    elif kind == "anim":
                        e["anim"] += 1
    return res


def load_ids():
    """合并所有「装备ID」来源 → {id: {name, type, src:set}}。真值源先入，名称优先真值。"""
    ids = {}

    def add(iid, src, name="", typ="", name_priority=False):
        iid = str(iid).strip()
        if not (iid.isdigit() and 4 <= len(iid) <= 15):
            return
        e = ids.setdefault(iid, {"name": "", "type": "", "src": set()})
        e["src"].add(src)
        if name and (not e["name"] or name_priority):
            e["name"] = name
        if typ and not e["type"]:
            e["type"] = typ

    # ① 真值：近接格闘武器表（8 把，名字最可靠）
    for l in rows(os.path.join(SETTINGS, "weapon_wrestle.csv")):
        c = l.split(",")
        add(c[0], "wrestle真值", c[1] if len(c) > 1 else "", "WEAPON", True)
    # ② 真值：武器视觉定制表（武器ID + 机体名备注）
    for l in rows(os.path.join(SETTINGS, "weapon_visual_customize.csv")):
        c = l.split(",")
        add(c[0], "visual真值", "", "WEAPON")
    # ③ 真值：机体网格定制表（モデルID, 武器ID, …）
    for l in rows(os.path.join(SETTINGS, "msma_mesh_customize.csv")):
        c = l.split(",")
        if len(c) > 1:
            add(c[1], "mesh真值", c[5].lstrip("#") if len(c) > 5 else "", "WEAPON", True)
    # ④ 服务端真值：#1 MSMA_WEAPONSET col2 = 武器ID
    for l in rows(os.path.join(SERVER, "msma_weapon_set.csv")):
        c = l.split(",")
        if len(c) > 2:
            add(c[2], "weapon_set")
    # ⑤ #65 ITEM 表（ID + 名称 + 类型）
    for l in rows(os.path.join(SERVER_ITEM, "item.csv")):
        c = l.split(",")
        add(c[0], "ITEM表", c[2] if len(c) > 2 else "", c[4] if len(c) > 4 else "")
    # ⑥ 图标池（interface/icon/item/d/d<ID 补零>.dds）—— UI 按物品ID 取图标
    if os.path.isdir(ICON_DIR):
        for f in os.listdir(ICON_DIR):
            m = re.match(r"^d[0-9]+", f)
            if m:
                v = m.group(0)[1:].lstrip("0")
                add(v, "图标池")
    # ⑦ 既有枚举产物
    for l in rows(os.path.join(HERE, "names", "物品ID全集.csv")):
        c = l.split(",")
        add(c[0], "物品ID全集")
    return ids


VALID_CATS = set()


def res_candidates(iid):
    """给出候选资源坐标。类段可以是 1 位（01~09）或 2 位（10~20）；
    号段 = 末 4 位（4 位号模板）或紧跟类段的 6 位（6 位号模板）。调用方取第一个存在的。"""
    out = []
    for clen in (1, 2):
        if len(iid) < clen + 4:
            continue
        cat = iid[:clen].zfill(2) if clen == 1 else iid[:2]
        if cat not in VALID_CATS:
            continue
        out.append((cat, iid[-4:], "%d位类/4位号" % clen))
        if len(iid) >= clen + 6:
            out.append((cat, iid[clen:clen + 6], "%d位类/6位号" % clen))
    return out


def main():
    res = scan_assets()
    VALID_CATS.update(cat for cat, _num in res)
    weapons = {k: v for k, v in res.items() if v["model"]}
    print("资源包：item 目录 %d 个（类号 %s），其中含武器模型(EM_) %d 个" % (
        len(res), ",".join(sorted(VALID_CATS)), len(weapons)))

    ids = load_ids()
    print("装备ID 来源合并：%d 个" % len(ids))

    recs = []
    hit, miss = 0, 0
    covered = set()
    for iid in sorted(ids, key=lambda x: (len(x), x)):
        pick = None
        for cat, num, tmpl in res_candidates(iid):
            if (cat, num) in res:
                pick = (cat, num, tmpl)
                break
        e = ids[iid]
        if pick:
            hit += 1
            cat, num, tmpl = pick
            a = res[(cat, num)]
            covered.add((cat, num))
            recs.append(((cat, num, iid),
                         "%s,%s,%s,item/%s/%s,%s,%s,%s,%d,%s,%s,%d,%d,Y,%s," % (
                             iid, e["name"], e["type"], cat, num, cat, num, tmpl,
                             len(a["model"]), "|".join(a["model"]), "|".join(a["attr"]),
                             a["tex"], a["anim"], "|".join(sorted(e["src"])))))
        else:
            miss += 1
            cat = "%02d" % int(iid[0])
            recs.append((("zz", "zz", iid),
                         "%s,%s,%s,item/%s/%s,%s,%s,-,0,,,,0,0,N,%s," % (
                             iid, e["name"], e["type"], cat, iid[-4:], cat, iid[-4:],
                             "|".join(sorted(e["src"])))))
    print("★已知装备ID→资源 命中 %d / %d（未命中 %d，多为机体/道具类 ID）" % (hit, len(ids), miss))

    # ★按用户要求「根据资源包生成」：没有被任何已知 ID 指向的武器目录，用骨架 ID 兜住
    skel = 0
    for (cat, num) in sorted(weapons):
        if (cat, num) in covered:
            continue
        a = res[(cat, num)]
        head = str(int(cat))               # 类去前导零
        if len(num) == 6:
            # 6 位号模板（IDA 分支A：ID ≥ 1e10；类=(ID/1e10)%100、号=(ID/1e4)%1e6）
            # 逆运算：ID = 类*1e10 + 号*1e4 + 101（末 4 位 = NN(01) + 变体(01)）
            base = int(cat) * 10 ** 10 + int(num) * 10 ** 4 + 101
            cands = [str(base + k) for k in range(100)]
        else:
            # 4 位号：<类2位><子类04><号4位>（与真值 1040101 同形），冲突则末位递增
            base = int(cat + "04" + num)
            cands = [str(base + k) for k in range(100)] + [head + num]
        for sid in cands:
            if sid in ids:
                continue                   # 该 ID 已有其它归属，不抢
            recs.append(((cat, num, sid),
                         "%s,,,item/%s/%s,%s,%s,骨架,%d,%s,%s,%d,%d,Y,%s," % (
                             sid, cat, num, cat, num, len(a["model"]),
                             "|".join(a["model"]), "|".join(a["attr"]), a["tex"], a["anim"],
                             "资源包反推")))
            covered.add((cat, num))
            skel += 1
            break
    print("  资源包反推（骨架 ID）补齐 %d 个目录" % skel)

    recs.sort(key=lambda x: x[0])
    text = "\r\n".join([HEAD_MAP] + [r[1] for r in recs]) + "\r\n"
    io.open(OUT_MAP, "w", encoding="utf-8", newline="").write(text)
    print("  已写 %s（%d 行）" % (OUT_MAP, len(recs)))

    # 资源侧缺口：有 EM 模型但没有任何已知 ID 指向
    gaps = sorted(k for k in weapons if k not in covered)
    gl = ["#资源ID,资源类,资源号,模型EM数,模型EM,属性EZ,贴图ET数,"]
    for cat, num in gaps:
        a = res[(cat, num)]
        gl.append("item/%s/%s,%s,%s,%d,%s,%s,%d," % (
            cat, num, cat, num, len(a["model"]), "|".join(a["model"]),
            "|".join(a["attr"]), a["tex"]))
    io.open(OUT_GAP, "w", encoding="utf-8", newline="").write("\r\n".join(gl) + "\r\n")
    print("  武器资源目录被 ID 覆盖 %d / %d，缺口 %d → %s" % (
        len(weapons) - len(gaps), len(weapons), len(gaps), OUT_GAP))

    # ── viewer 用：机体（練度ID）→ 武器（武器ID → item 资源），取自表 #1 MSMA_WEAPONSET
    #
    # ★★可信度说明（2026-10-01 复核）★★
    #   本表 col0 = 練度ID、col2 = 武器ID 直接来自 `msma_weapon_set.csv`（表 #1）。
    #   但那张表本身是 `gen_weapon_set_wiki.py` **生成**的：武器ID = "2"+練度ID[1:5]+sub4，
    #   sub4 从 `item/02` 池里按 練度ID[5] 分桶后**切片**取，wiki 武器名**按序**铺上去。
    #   该脚本自己在表头写明：**"wiki 武器第 i 把 ↔ 该机体第 i 个 sub4" 的先后对应无来源可证**。
    #   实测（`datatables/_verify_weapon_truth.py`）：
    #     · 1625 个武器ID **每个只被 1 台机体用**（互不共享 = 构造式切片的特征）；
    #     · 客户端三张真值表（weapon_wrestle / weapon_visual_customize / msma_mesh_customize）
    #       只佐证了其中 **7 个**。⇒ 机体↔武器 的**配对**属推定，不是结论。
    #   因此本表加 `依据` 列，把「ID 是真的、但配对没证实」如实写出来，viewer 照它标 ⚠推定。
    item_name = {}
    ip = os.path.join(ROOT, "server", "datafiles", "lounge", "item", "item.csv")
    if os.path.exists(ip):
        for line in io.open(ip, encoding="utf-8-sig", errors="replace"):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            c = line.split(",")
            if len(c) >= 3 and c[0].strip().isdigit() and c[2].strip() and c[0].strip() not in item_name:
                item_name[c[0].strip()] = c[2].strip().replace(",", " ")

    # 客户端真值表 → 武器ID 集合（证明"这个ID是真武器"）
    truth_id = set()
    for rel in ("weapon_wrestle.csv", "weapon_visual_customize.csv"):
        for l in rows(os.path.join(UD, "settings", rel)):
            c = l.split(",")
            if c and c[0].strip().isdigit():
                truth_id.add(c[0].strip())
    # 客户端真值表 → (モデルID, 武器ID) 配对（证明"这台机体挂这把武器"）★最强依据
    truth_pair = set()
    for l in rows(os.path.join(UD, "settings", "msma_mesh_customize.csv")):
        c = l.split(",")
        if len(c) > 1 and c[1].strip().isdigit():
            truth_pair.add((c[0].strip(), c[1].strip()))
    mid_of = {}
    for l in rows(BIND):
        c = l.split(",")
        if len(c) > 2 and c[0].strip().isdigit() and len(c[2].strip()) == 9:
            mid_of[c[0].strip()] = c[2].strip()

    def basis_of(lid, wid):
        if (mid_of.get(lid, ""), wid) in truth_pair:
            return "真值"
        if wid in truth_id:
            return "真值ID"
        return "推定"

    wl = ["#練度ID,武器ID,槽位,资源ID,资源存在,模型EM,属性EZ,武器名,依据,"]
    nw = 0
    n_basis = collections.Counter()
    for l in rows(os.path.join(SERVER, "msma_weapon_set.csv")):
        c = l.split(",")
        if len(c) < 7:
            continue
        ms, wid, slot, en = c[0].strip(), c[2].strip(), c[4].strip(), c[6].strip()
        if not (ms.isdigit() and wid.isdigit()) or en == "0":
            continue
        pick = None
        for cat, num, _t in res_candidates(wid):
            if (cat, num) in res:
                pick = (cat, num)
                break
        bz = basis_of(ms, wid)
        n_basis[bz] += 1
        nm = item_name.get(wid, "")
        if pick:
            a = res[pick]
            wl.append("%s,%s,%s,item/%s/%s,Y,%s,%s,%s,%s," % (
                ms, wid, slot, pick[0], pick[1], "|".join(a["model"]), "|".join(a["attr"]),
                nm, bz))
        else:
            wl.append("%s,%s,%s,,N,,,,%s,%s," % (ms, wid, slot, nm, bz))
        nw += 1
    io.open(OUT_WEAPONS, "w", encoding="utf-8", newline="").write("\r\n".join(wl) + "\r\n")
    print("  已写 %s（%d 条 机体→武器）" % (OUT_WEAPONS, nw))
    print("    依据分布 = %s（★推定 = 配对未证实，非 0 就说明这张表只能当线索）"
          % dict(n_basis))

    # ── viewer 用：item 资源目录 → 代表装备ID（viewer 把「全部武器模型」一并列出时贴 ID 用）
    by_dir = collections.defaultdict(list)
    for iid in ids:
        for cat, num, _t in res_candidates(iid):
            if (cat, num) in res:
                by_dir[(cat, num)].append(iid)
                break
    prefer = ("wrestle真值", "weapon_set", "ITEM表", "visual真值", "mesh真值", "图标池")

    def _rank(iid):
        src = "|".join(ids[iid]["src"])
        return (0 if any(p in src for p in prefer) else 1, len(iid), iid)

    il = ["#资源ID,装备ID,候选ID数,模型EM,属性EZ,来源,"]
    n_item = 0
    for (cat, num) in sorted(res):
        a = res[(cat, num)]
        if not a["model"]:
            continue
        lst = by_dir.get((cat, num), [])
        if lst:
            rep = sorted(lst, key=_rank)[0]
            src_txt = "|".join(sorted(ids[rep]["src"]))
        else:   # 没有已知 ID 的目录也要列（viewer 得能把武器模型渲出来）
            rep = str(int(cat)) + num
            src_txt = "资源包反推"
        il.append("%s,%s,%s,%d,%s,%s,%s," % (
            "item/%s/%s" % (cat, num), rep, len(lst), len(a["model"]),
            "|".join(a["model"]), "|".join(a["attr"]), src_txt))
        n_item += 1
    io.open(OUT_ITEM_BIND, "w", encoding="utf-8", newline="").write("\r\n".join(il) + "\r\n")
    print("  已写 %s（%d 条 item 资源→装备ID）" % (OUT_ITEM_BIND, n_item))

    # ── viewer 用：装备ID → 名称。来源 = item/item.csv（表ID 65 CItemTable，col2 = 名称）
    ip = os.path.join(ROOT, "server", "datafiles", "lounge", "item", "item.csv")
    nl = ["#ID,名称,"]
    n_name = 0
    if os.path.exists(ip):
        for line in io.open(ip, encoding="utf-8-sig", errors="replace"):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            c = line.split(",")
            if len(c) < 3 or not c[0].strip() or not c[2].strip():
                continue
            nl.append("%s,%s," % (c[0].strip(), c[2].strip().replace(",", " ")))
            n_name += 1
    io.open(OUT_ITEM_NAMES, "w", encoding="utf-8", newline="").write("\r\n".join(nl) + "\r\n")
    print("  已写 %s（%d 条 ID→名称）" % (OUT_ITEM_NAMES, n_name))
    return 0


if __name__ == "__main__":
    sys.exit(main())
