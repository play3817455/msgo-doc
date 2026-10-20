# -*- coding: utf-8 -*-
"""_verify_bind_sweep.py —— 全量核对 viewer/ms_bind.csv 的绑定是否「货对板」且资源确实存在。

核对 6 件事（每台绑定的机体）：
  1. モデルID 与人工核对权威 JSON 是否一致（不一致 = 货不对板，必须 0）
  2. chara/0A/B/C 资源目录是否真实存在
  3. 模型文件（.dxg/.mrb/.vra 至少其一）是否在磁盘上
  4. 机体大图 d0<mid>.dds / 小图 s0<mid>.dds 是否命中
  5. 配色图 c0<mid>_*.dds 有几张
  6. 机体挂的武器（viewer/ms_weapons.csv）整套资源目录是否 ok

只读，不改任何文件。
"""
import io
import json
import os
import re
import sys
from collections import Counter, defaultdict

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
NAMES = os.path.join(HERE, "names")
DATA = os.path.join(ROOT, "机动战士敢达Online", "GundamOnline", "unpackdat")
BIND = os.path.join(ROOT, "viewer", "ms_bind.csv")
WEAP = os.path.join(ROOT, "viewer", "ms_weapons.csv")
ICON_DIR = os.path.join(DATA, "interface", "icon", "item")
COLOR_DIR = os.path.join(DATA, "interface", "icon", "color")

AUTH_CANDIDATES = [
    os.path.join(ROOT, "iconmatch", "data", "ms_final.json"),
    os.path.join(NAMES, "ms_wiki_pairs.json"),
    r"F:\Users\xxm38\Downloads\ms_wiki_pairs.json",
]


def rows(path):
    if not os.path.exists(path):
        return []
    L = io.open(path, encoding="utf-8-sig", errors="replace").read().splitlines()
    return [x for x in L if x.strip() and not x.lstrip().startswith("#")]


def cell(line, i):
    p = line.split(",")
    return p[i].strip() if i < len(p) else ""


def load_auth():
    by_lid, by_mid, used = {}, {}, ""
    for path in AUTH_CANDIDATES:
        if not os.path.exists(path):
            continue
        d = json.load(io.open(path, encoding="utf-8-sig"))
        pairs = d.get("pairs")
        if isinstance(pairs, dict):
            for mid, v in pairs.items():
                lid = (v.get("lid") or "").strip()
                if lid:
                    by_lid[lid] = mid
                by_mid[mid] = lid
        elif isinstance(pairs, list):
            for p in pairs:
                mid = (p.get("mid") or "").strip()
                lid = (p.get("lid") or "").strip()
                if lid:
                    by_lid[lid] = mid
                if mid:
                    by_mid[mid] = lid
        if by_lid:
            used = path
            break
    return by_lid, by_mid, used


def mid_to_dir(mid):
    if len(mid) != 9 or not mid.isdigit():
        return ""
    return "chara/0%s/%s/%s" % (mid[0], mid[1:3], mid[3:7])


def has_model_file(dirpath):
    """该机体目录下 model/ 有没有 .dxg / .mrb / .vra。返回形态数。"""
    md = os.path.join(DATA, dirpath.replace("/", os.sep), "model")
    if not os.path.isdir(md):
        return 0
    n = 0
    for fn in os.listdir(md):
        if fn.lower().endswith((".dxg", ".mrb", ".vra")):
            n += 1
    return n


def icon_exists(sub, name):
    return os.path.exists(os.path.join(ICON_DIR, sub, name))


def color_icons(mid):
    if not os.path.isdir(COLOR_DIR):
        return 0
    pfx = "c0%s_" % mid
    return sum(1 for fn in os.listdir(COLOR_DIR) if fn.lower().startswith(pfx))


def main():
    auth_lid, auth_mid, used = load_auth()
    print("权威 JSON = %d 条（%s）" % (len(auth_lid), used or "未找到"))
    if not os.path.isdir(DATA):
        print("!! 解包目录不存在：%s" % DATA)
        return 3

    binds = []
    for l in rows(BIND):
        binds.append({
            "lid": cell(l, 0), "name": cell(l, 1), "mid": cell(l, 2), "dir": cell(l, 3),
            "model": cell(l, 4), "src": cell(l, 6), "chk": cell(l, 7), "wiki": cell(l, 8),
        })
    bound = [b for b in binds if b["mid"]]
    print("ms_bind.csv = %d 行，其中已绑定 %d" % (len(binds), len(bound)))

    weapons = defaultdict(list)   # lid -> [(wid, dir, existsFlag), ...]
    for l in rows(WEAP):
        weapons[cell(l, 0)].append((cell(l, 1), cell(l, 3), cell(l, 4)))

    mismatch = []          # 与权威 JSON 不一致
    dir_missing = []       # 资源目录不存在
    model_missing = []     # 目录在但 model 文件没了
    no_big = []
    no_small = []
    no_color = []
    no_weapon_dir = 0
    n_weap_units = 0
    color_counts = Counter()
    model_forms = Counter()
    wids = set()
    wid_icon = {}

    for b in bound:
        lid, mid, d = b["lid"], b["mid"], b["dir"] or mid_to_dir(b["mid"])
        if lid in auth_lid and auth_lid[lid] != mid:
            mismatch.append((lid, auth_lid[lid], mid))
        dfull = os.path.join(DATA, d.replace("/", os.sep)) if d else ""
        if not dfull or not os.path.isdir(dfull):
            dir_missing.append((lid, mid, d))
            continue
        nf = has_model_file(d)
        if nf == 0:
            model_missing.append((lid, mid, d))
        else:
            model_forms[nf] += 1
        if not icon_exists("d", "d0%s.dds" % mid):
            no_big.append((lid, mid))
        if not icon_exists("s", "s0%s.dds" % mid):
            no_small.append((lid, mid))
        nc = color_icons(mid)
        color_counts[nc] += 1
        if nc == 0:
            no_color.append((lid, mid))
        # 武器目录（col3=资源ID，col4=Y/N 是否存在）
        if weapons.get(lid):
            n_weap_units += 1
        for wid, wdir, wexist in weapons.get(lid, []):
            if wdir and not os.path.isdir(os.path.join(DATA, wdir.replace("/", os.sep))):
                no_weapon_dir += 1
            if wid:
                wids.add(wid)
                if wid not in wid_icon:
                    hit = False
                    for k in (wid, wid.zfill(7)):
                        if icon_exists("d", "d0%s.dds" % k) or icon_exists("s", "s0%s.dds" % k):
                            hit = True
                            break
                    wid_icon[wid] = hit

    print()
    print("=== 对账结果 ===")
    print("① 与权威 JSON 冲突（货不对板）: %d" % len(mismatch))
    for x in mismatch[:20]:
        print("    %s 权威=%s 本表=%s" % x)
    print("② 资源目录缺失: %d" % len(dir_missing))
    for x in dir_missing[:20]:
        print("    %s mid=%s dir=%s" % x)
    print("③ 目录在但模型文件缺: %d" % len(model_missing))
    for x in model_missing[:20]:
        print("    %s mid=%s %s" % x)
    print("④ 缺机体大图 d0<mid>.dds: %d" % len(no_big))
    print("   例: %s" % ", ".join("%s/%s" % (lid, mid) for lid, mid in no_big[:12]))
    print("⑤ 缺机体小图 s0<mid>.dds: %d" % len(no_small))
    print("   例: %s" % ", ".join("%s/%s" % (lid, mid) for lid, mid in no_small[:12]))
    print("⑥ 缺配色图 c0<mid>_*: %d （客户端数据事实：多数机体没有涂装图标，非绑定错误）" % len(no_color))
    print("   例: %s" % ", ".join("%s/%s" % (lid, mid) for lid, mid in no_color[:12]))
    print("⑦ 模型形态数分布: %s" % dict(sorted(model_forms.items())))
    print("⑧ 配色图张数分布: %s" % dict(sorted(color_counts.items())))
    print("⑨ 挂武器的机体: %d 台；武器整套目录缺失项: %d" % (n_weap_units, no_weapon_dir))
    wh = sum(1 for v in wid_icon.values() if v)
    miss_w = sorted(w for w, v in wid_icon.items() if not v)
    print("⑩ 武器图标（按唯一武器ID）: %d / %d (%.1f%%); 缺: %s" % (
        wh, len(wid_icon), 100.0 * wh / max(1, len(wid_icon)), ",".join(miss_w)))

    ok_all = (not mismatch and not dir_missing and not model_missing)
    print()
    print("结论: %s" % ("全部绑定资源到位 ✔" if ok_all else "存在待处理项 ✘"))
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main())
