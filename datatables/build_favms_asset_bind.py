# -*- coding: utf-8 -*-
"""build_favms_asset_bind.py —— 把 favms_ok_list.csv 里的机体ID 绑定到客户端资源坐标。

为什么需要它
  · favms_ok_list.csv（unpackdat/settings/，700 行）= 客户端「可持有机体」清单，
    本文件只有 練度ID(7 位) + 日文名，不含任何资源信息；
  · 客户端资源坐标 = モデルID(9 位) = A(1)+B(2)+C(4)+NN(2) ⇒ chara/0A/B/C/
    （IDA 实证：sub_49D170 拼路径、sub_473390 拆十进制位）；
  · 两套编号之间没有算法关系，只能查表绑定。

数据源（优先级从高到低）
  0. ★人工核对导出的权威 JSON★（默认 iconmatch/data/ms_final.json，其次 Downloads/ms_wiki_pairs.json）
     —— 「モデルID ↔ WIKI 机体名 ↔ 練度ID」的最终结论，其余来源一律只作它的兜底/线索。
  1. names/练度ID-モデルID-全集.csv       6 源合并，附权威校验列
  2. names/机体总表.csv      col33 模型打包值（按練度ID）
  3. server/datafiles/lounge/msma/msma_settings.csv  col0=練度ID → col1=モデルID（服务端真值表）
  4. names/机体总表.csv      col34 模型目录 → 反推モデルID（取同 (B,C) 目录里最小 NN）

校验
  names/chara目录-ID清单.csv（1646 个权威 モデルID ↔ 资源目录/模型文件）

产出（同一内容，两份）
  · datatables/names/favms_ok_list-资源绑定.csv   完整版（含来源/校验 + 关联资源）
  · viewer/ms_bind.csv                            viewer 启动时直接读

★为什么第 0 源最关键★
  旧表（msma_settings / 模型号映射-自动 / 机体总表 …）会串行、会错配：实测 576 台人工结论里
  有 342 台的 モデルID 和旧绑定表不一致（“货不对板”）。本脚本现在先读人工核对的 JSON，
  把它当唯一权威；旧表只在「JSON 还没结论」的机体上兜底，且来源列会写明是线索。

viewer/ms_bind.csv 列（前 8 列沿用旧口径，viewer 只认前 4 列；后 6 列是本次新增的关联信息）：
  練度ID,机体名,モデルID,资源目录,模型文件,目录形态数,来源,校验,WIKI名,类型,阵营,大图标,小图标,备注

用法
  python datatables/build_favms_asset_bind.py
  python datatables/build_favms_asset_bind.py "F:\\somewhere\\ms_wiki_pairs.json"   # 指定权威导出
"""
import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
NAMES = os.path.join(HERE, "names")

FAVMS = os.path.join(ROOT, "机动战士敢达Online", "GundamOnline", "unpackdat", "settings", "favms_ok_list.csv")
OUT_NAMES = os.path.join(NAMES, "favms_ok_list-资源绑定.csv")
OUT_VIEWER = os.path.join(ROOT, "viewer", "ms_bind.csv")

# ★人工核对导出的权威表★：先 iconmatch/data/ms_final.json（已清洗），再仓库内副本，
# 最后 Downloads 的原始导出。三者实测 576 条 lid↔mid 完全一致（0 冲突）。
AUTH_CANDIDATES = [
    os.path.join(ROOT, "iconmatch", "data", "ms_final.json"),
    os.path.join(NAMES, "ms_wiki_pairs.json"),
    r"F:\Users\xxm38\Downloads\ms_wiki_pairs.json",
]
# 图标（大/小）文件名 = <前缀>0<モデルID>.dds；前缀 d=半身大图 s=列表小图（interface/icon/item/<d|s>/）
ICON_BIG = "interface/icon/item/d/d0%s.dds"
ICON_SMALL = "interface/icon/item/s/s0%s.dds"

COLS = ["練度ID", "机体名", "モデルID", "资源目录", "模型文件", "目录形态数", "来源", "校验",
        "WIKI名", "类型", "阵营", "大图标", "小图标", "备注"]
HEAD = "#" + ",".join(COLS) + ","
_LID_TYPE = {"1": "强袭", "2": "重击", "3": "支援", "4": "砲撃", "5": "狙击"}
_LID_FACTION = {"1": "联邦", "2": "吉翁"}


def clean(s):
    """CSV 单元格：去掉换行与逗号（viewer 是简单 split(',')）。"""
    return (s or "").replace("\r", " ").replace("\n", " ").replace(",", " ").strip()


def lid_type(lid):
    return _LID_TYPE.get(lid[1], "") if len(lid) == 7 else ""


def lid_faction(lid):
    return _LID_FACTION.get(lid[6], "") if len(lid) == 7 else ""


def load_auth(paths):
    """读人工核对导出 → {練度ID: rec}, {モデルID: rec}, 实际路径。
    rec = {mid, lid, wiki, type, faction, note, dir}。两种格式都认：
      · ms_final.json        {"pairs": {mid: {wiki,lid,lid_type,lid_faction,dir,note}}}
      · ms_wiki_pairs.json   {"pairs": [ {mid,wiki,lid,type,...} ]}
    """
    by_lid, by_mid, used = {}, {}, ""
    for path in paths:
        if not os.path.exists(path):
            continue
        try:
            d = json.load(io.open(path, encoding="utf-8-sig"))
        except Exception as e:
            print("  （读不了 %s：%s）" % (path, e))
            continue
        pairs = d.get("pairs")
        if isinstance(pairs, dict):
            for mid, v in pairs.items():
                lid = (v.get("lid") or "").strip()
                rec = {"mid": mid, "lid": lid, "wiki": v.get("wiki", ""),
                       "type": v.get("lid_type", ""), "faction": v.get("lid_faction", ""),
                       "note": v.get("note", ""), "dir": v.get("dir", "")}
                if lid:
                    by_lid[lid] = rec
                by_mid[mid] = rec
        elif isinstance(pairs, list):
            for p in pairs:
                mid = (p.get("mid") or "").strip()
                lid = (p.get("lid") or "").strip()
                rec = {"mid": mid, "lid": lid, "wiki": p.get("wiki", ""),
                       "type": p.get("lid_type", ""), "faction": p.get("lid_faction", ""),
                       "note": p.get("note", ""), "dir": p.get("dir", "")}
                if lid:
                    by_lid[lid] = rec
                if mid:
                    by_mid[mid] = rec
        if by_lid:
            used = path
            break
    return by_lid, by_mid, used


def rows(path):
    """读 CSV 数据行（跳过空行与 # 注释行），UTF-8（容忍 BOM）。"""
    if not os.path.exists(path):
        return []
    L = io.open(path, encoding="utf-8-sig", errors="replace").read().splitlines()
    return [x for x in L if x.strip() and not x.lstrip().startswith("#")]


def cell(line, i):
    p = line.split(",")
    return p[i].strip() if i < len(p) else ""


def split_mid(mid):
    """モデルID(9 位) → (A, B, C, NN)，非法返回 None。"""
    if len(mid) != 9 or not mid.isdigit():
        return None
    return mid[0], mid[1:3], mid[3:7], mid[7:9]


def mid_to_dir(mid):
    """モデルID → chara/0A/B/C（A 补前导 0，与 chara目录-ID清单.csv 口径一致）。"""
    sp = split_mid(mid)
    if not sp:
        return ""
    a, b, c, _nn = sp
    return "chara/0%s/%s/%s" % (a, b, c)


class Auth(object):
    """chara目录-ID清单.csv：权威 モデルID ↔ 资源目录/模型文件。"""

    def __init__(self, path):
        self.by_mid = {}   # mid -> (dir, model, nform)
        self.by_bc = {}    # (B, C) -> [mid...] 按 NN 升序
        for l in rows(path):
            mid = cell(l, 0)
            sp = split_mid(mid)
            if not sp:
                continue
            _a, b, c, nn = sp
            d = cell(l, 5)
            if not d:
                d = "chara/%s/%s/%s" % (cell(l, 1), b, c)
            self.by_mid[mid] = (d, cell(l, 6), cell(l, 7))
            self.by_bc.setdefault((b, c), []).append(mid)
        for k in self.by_bc:
            self.by_bc[k].sort(key=lambda m: (m[7:9], m))

    def pick(self, mid):
        """优先权威表的目录；否则按拆位拼。返回 (dir, model, nform)。"""
        if mid in self.by_mid:
            return self.by_mid[mid]
        d = mid_to_dir(mid)
        return (d, "", "") if d else ("", "", "")

    def from_dir(self, d):
        """资源目录 chara/01/24/1201 → 同 (B,C) 目录里 NN 最小的モデルID。"""
        parts = [p for p in d.replace("\\", "/").split("/") if p]
        if len(parts) < 4 or parts[0].lower() != "chara":
            return ""
        b, c = parts[-2], parts[-1]
        cands = self.by_bc.get((b, c))
        return cands[0] if cands else ""


def load_favms(path):
    """favms_ok_list.csv → [(練度ID, 机体名)]，保持文件顺序。"""
    out = []
    for l in rows(path):
        ms = cell(l, 0)
        if ms.isdigit():
            out.append((ms, cell(l, 1)))
    return out


def main():
    auth = Auth(os.path.join(NAMES, "chara目录-ID清单.csv"))
    favms = load_favms(FAVMS)
    print("favms_ok_list.csv   = %d 行" % len(favms))
    print("权威 モデルID 清单   = %d 条" % len(auth.by_mid))

    # ★权威 JSON★（argv[1] 可覆盖默认候选）
    auth_paths = ([sys.argv[1]] if len(sys.argv) > 1 else []) + AUTH_CANDIDATES
    auth_lid, auth_mid, auth_used = load_auth(auth_paths)
    print("人工核对权威 JSON    = %d 条（%s）" % (len(auth_lid), auth_used or "未找到！"))

    # {練度ID: (モデルID, 来源)}
    mid_of = {}

    def put(ms, mid, src):
        if not (ms.isdigit() and mid.isdigit() and len(mid) == 9):
            return False
        if ms in mid_of:
            return False
        mid_of[ms] = (mid, src)
        return True

    # 0. ★人工核对权威 JSON★ —— 优先级最高，命中即定案
    n = 0
    for lid, rec in sorted(auth_lid.items()):
        if put(lid, rec["mid"], "人工核对"):
            n += 1
    print("  0 人工核对 JSON（权威）           %4d" % n)

    # 1. 练度ID-モデルID-全集.csv（已合并 6 源 + 权威校验）
    n = 0
    for l in rows(os.path.join(NAMES, "练度ID-モデルID-全集.csv")):
        src = cell(l, 2) or "全集"
        if put(cell(l, 0), cell(l, 1), src if src != "机体总表" else "机体总表"):
            n += 1
    print("  1 练度ID-モデルID-全集.csv        %4d" % n)

    # 2. 机体总表.csv col33 模型打包值
    n = 0
    for l in rows(os.path.join(NAMES, "机体总表.csv")):
        if put(cell(l, 0), cell(l, 33), "机体总表"):
            n += 1
    print("  2 机体总表.csv(col33 打包值)      %4d" % n)

    # 3. msma_settings.csv col0 → col1（服务端真值表）
    msma = os.path.join(ROOT, "server", "datafiles", "lounge", "msma", "msma_settings.csv")
    n = 0
    for l in rows(msma):
        if put(cell(l, 0), cell(l, 1), "msma_settings"):
            n += 1
    print("  3 msma_settings.csv(col1)         %4d" % n)

    # 4. 机体总表.csv col34 模型目录 → 反推モデルID
    n = 0
    for l in rows(os.path.join(NAMES, "机体总表.csv")):
        ms = cell(l, 0)
        d = cell(l, 34)
        if ms in mid_of or not d:
            continue
        mid = auth.from_dir(d)
        if put(ms, mid, "目录反推"):
            n += 1
    print("  4 机体总表.csv(col34 目录反推)    %4d" % n)

    # 组装输出
    # 列：練度ID,机体名,モデルID,资源目录,模型文件,目录形态数,来源,校验,
    #     WIKI名,类型,阵营,大图标,小图标,备注   （前 8 列沿用旧口径，viewer 只认前 4 列）
    out = []
    for ms, name in favms:
        mid, src = mid_of.get(ms, ("", ""))
        rec = auth_lid.get(ms) or {}
        if mid:
            d, model, nform = auth.pick(mid)
            if rec.get("dir"):       # 权威 JSON 给了目录就以它为准（可能不在 chara目录-ID清单 里）
                d = rec["dir"]
            chk = "OK" if mid in auth.by_mid else "NOT_IN_TREE"
            if not model and d:
                # 目录存在但权威表没收（少见）：仍标注目录
                chk = "DIR_ONLY"
        else:
            d, model, nform, chk = "", "", "", "UNBOUND"
        wiki = clean(rec.get("wiki", ""))
        typ = clean(rec.get("type") or lid_type(ms))
        fac = clean(rec.get("faction") or lid_faction(ms))
        note = clean(rec.get("note", ""))
        big = ICON_BIG % mid if mid else ""
        small = ICON_SMALL % mid if mid else ""
        out.append((ms, clean(name), mid, d, model, nform, src, chk,
                    wiki, typ, fac, big, small, note))

    # 权威 JSON 有结论、但 favms_ok_list.csv 没收录的練度ID：照样补进来，
    # 否则 viewer 按 ID 查询会漏掉这几台（备注列标明来源，便于区分）。
    favms_ids = set(ms for ms, _ in favms)
    jp_name = {}
    for l in rows(os.path.join(NAMES, "机体名对照表.csv")):
        if cell(l, 0).isdigit() and cell(l, 0) not in jp_name:
            jp_name[cell(l, 0)] = cell(l, 1)
    extra = 0
    for lid, rec in sorted(auth_lid.items()):
        if lid in favms_ids:
            continue
        mid = rec["mid"]
        d, model, nform = auth.pick(mid)
        if rec.get("dir"):
            d = rec["dir"]
        chk = "OK" if mid in auth.by_mid else ("DIR_ONLY" if d else "NOT_IN_TREE")
        wiki = clean(rec.get("wiki", ""))
        note = clean(rec.get("note", ""))
        note = (note + " favms未收录").strip()
        out.append((lid, clean(jp_name.get(lid) or wiki), mid, d, model, nform, "人工核对", chk,
                    wiki, clean(rec.get("type") or lid_type(lid)),
                    clean(rec.get("faction") or lid_faction(lid)),
                    ICON_BIG % mid, ICON_SMALL % mid, note))
        extra += 1
    if extra:
        print("  + 权威 JSON 独有（favms 未收录）  %4d" % extra)

    bound = [r for r in out if r[2]]
    print()
    print("★绑定结果：%d / %d 台（%.1f%%）" % (len(bound), len(out), 100.0 * len(bound) / max(1, len(out))))
    print("  未绑定 = %d 台（favms 有 ID、但所有映射源都没有它的モデルID）" % (len(out) - len(bound)))
    ok = sum(1 for r in bound if r[7] == "OK")
    print("  其中通过 chara目录-ID清单 校验 = %d" % ok)
    from collections import Counter
    print("  来源分布 = %s" % dict(Counter(r[6] for r in bound)))

    # 与权威 JSON 对账：绑定的 モデルID 是否和人工结论一致（不一致的必须为 0）
    bad = [(r[0], auth_lid[r[0]]["mid"], r[2]) for r in bound
           if r[0] in auth_lid and auth_lid[r[0]]["mid"] != r[2]]
    have = sum(1 for lid in auth_lid if lid in mid_of)
    print("  与人工核对对账：覆盖 %d / %d，冲突 %d" % (have, len(auth_lid), len(bad)))
    for lid, am, bm in bad[:10]:
        print("    ⚠ %s 权威=%s 本表=%s" % (lid, am, bm))

    lines = [HEAD]
    for r in out:
        lines.append(",".join(str(x) for x in r) + ",")
    text = "\r\n".join(lines) + "\r\n"
    io.open(OUT_NAMES, "w", encoding="utf-8", newline="").write(text)
    io.open(OUT_VIEWER, "w", encoding="utf-8", newline="").write(text)
    print()
    print("已写 %s" % OUT_NAMES)
    print("已写 %s" % OUT_VIEWER)
    return 0


if __name__ == "__main__":
    sys.exit(main())
