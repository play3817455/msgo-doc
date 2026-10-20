# -*- coding: utf-8 -*-
"""
build_model_map.py —— ★「練度ID → モデルID」可信映射合成器（P206，2026-09-17 深夜）

背景（用户指路 ✓）
════════════════════════════════════════════════════════════════════════
用户原话：「还有那个 **txt 的 id 经过算法就能对应上资源** 的，之前已经研究过了」✓
⇒ 对应链路（旧档实证 ✓）：
     `練度ID(7位, = msma_model.csv col0 = 主键 u64)`
        → **col71(低32) + col72(高32)** = 模型打包值（9位 モデルID）
        → `sub_571BF0` 喂 **`sub_473390` 解码路径**
        → 资源目录 = **`chara/01/{v[1:3]}/{v[3:7]}`**（`docs/MEMORY.md:10395` ✓ 40 条真值吻合 38 ✓）
        → 硬门槛：目录下必须有 **`Camera_Hangar.csv`**（P202 定案 ✓ 696 台里只有 71 台过 ✓）
参照：`datatables/01-列注释/05-5-CHARA_MODEL.md`（★第 71/72 列，非 69 ✗）

问题（本次体检实测 ✓）
════════════════════════════════════════════════════════════════════════
`server/datafiles/lounge/msma/msma_model.csv`（696 行 × 73 列）：
    · **只有 col0 和 col71 非空** ✓；col71 仅 **256 行**有值 ✗ ⇒ **440 行模型打包值 = 0** ✗
    · 已填入的 256 个值来自 **模糊匹配**（`模型号映射-自动.csv` 分数制 ✓）⇒ **含错值** ✗
    · ⇒ 客户端拿到空/错模型号 ⇒ 解码路径失败 ⇒ `wcslen(NULL)` ⇒ **~1GB 无限重试卡死** ✓

本工具做什么
════════════════════════════════════════════════════════════════════════
把 `datatables/names/` 下各来源**按可信度排序**合成 練度ID → モデルID：
    ① 人工（60 条，人工校对 ✓）> ② 补充（134 ✓ 带资源目录 ✓）> ③ 合并（111 ✓）> ④ 自动（311，**模糊** ✗ 最低）
并**逐个验证**资源目录真存在（`unpackdat/chara/{目录}/Camera_Hangar.csv` ✓）——
    ★只采纳"验证通过"的映射；验证不过 = 不采纳（宁缺勿错 ✗，项目铁律不猜 ✓）

用法
════════════════════════════════════════════════════════════════════════
    python datatables/build_model_map.py              # 只体检 + 报告（不动文件 ✓）
    python datatables/build_model_map.py --apply      # 写回 msma_model.csv（自动 .bak 备份 ✓）
报告：`datatables/names/_model_map_report.txt` ✓
"""
import csv
import io
import os
import shutil
import sys
from datetime import datetime

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAMES = os.path.join(REPO, "datatables", "names")
TARGET = os.path.join(REPO, "server", "datafiles", "lounge", "msma", "msma_model.csv")
REPORT = os.path.join(NAMES, "_model_map_report.txt")
ROSTER = os.path.join(REPO, "unpackdat", "settings", "favms_ok_list.csv")
CHARA = os.path.join(REPO, "unpackdat", "chara")

# 来源优先级：(标签, 文件, ID列, 模型号列, 资源目录列)
SOURCES = [
    ("人工", "模型号映射-人工.csv", 0, 1, 3),
    ("补充", "模型号映射-补充.csv", 0, 1, 4),
    ("合并", "模型号映射-合并.csv", 0, 1, None),
    ("自动", "模型号映射-自动.csv", 0, 1, None),
]

out = []


def p(s=""):
    out.append(s)
    print(s)


def read_rows(path):
    raw = open(path, "rb").read()
    for enc in ("utf-8-sig", "utf-8", "utf-16", "cp932"):
        try:
            text = raw.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    return list(csv.reader(io.StringIO(text)))


def model_dir(v):
    return "chara/01/%s/%s" % (v[1:3], v[3:7])


def dir_ok(d):
    d = (d or "").strip()
    if not d.startswith("chara/"):
        return False
    return os.path.exists(os.path.join(REPO, "unpackdat", d.replace("/", os.sep), "Camera_Hangar.csv"))


def mid_ok(v):
    v = (v or "").strip()
    return len(v) == 9 and v.isdigit() and dir_ok(model_dir(v))


def build():
    best = {}            # 練度ID -> (モデルID, 来源)
    stat = []
    for label, fname, icol, imv, idir in SOURCES:
        path = os.path.join(NAMES, fname)
        n = take = 0
        if not os.path.exists(path):
            stat.append((label, fname, 0, 0))
            continue
        for r in read_rows(path):
            if not r or r[0].lstrip().startswith("#"):
                continue
            key = r[icol].strip()
            if not key.isdigit():
                continue
            n += 1
            if key in best:
                continue                      # 已被更高优先级的源采纳 ✓
            mv = r[imv].strip() if len(r) > imv else ""
            if not (len(mv) == 9 and mv.isdigit()):
                continue
            # 验证：优先用该行自带的资源目录（更权威 ✓），否则用算法推的目录 ✓
            ok = dir_ok(r[idir]) if (idir is not None and len(r) > idir) else False
            if not ok:
                ok = dir_ok(model_dir(mv))
            if not ok:
                continue                      # 目录不存在 ⇒ 不采纳 ✗（宁缺勿错 ✓）
            best[key] = (mv, label)
            take += 1
        stat.append((label, fname, n, take))
    return best, stat


def main():
    apply = "--apply" in sys.argv
    p("=" * 100)
    p("★「練度ID → モデルID」可信映射合成  (%s)" % datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    p("=" * 100)

    roster = sorted(set(r[0].strip() for r in read_rows(ROSTER) if r and r[0].strip().isdigit()))
    p("")
    p("名册（favms_ok_list.csv）= %d 台唯一練度ID" % len(roster))

    best, stat = build()
    p("")
    p("【各来源采纳】（只采纳\"资源目录验证通过\"的 ✓）")
    for label, fname, n, take in stat:
        p("   %-4s %-26s 行%-6d 采纳 %-5d" % (label, fname, n, take))

    cov = [m for m in roster if m in best]
    p("")
    p("【覆盖】名册 %d 台 ⇒ 可信映射 **%d 台**（%.1f%%）｜仍无映射 = **%d 台** ✗"
      % (len(roster), len(cov), 100.0 * len(cov) / max(1, len(roster)), len(roster) - len(cov)))

    # 当前表状态 + 冲突
    cur = {}
    ncols = 0
    for r in read_rows(TARGET):
        if r and r[0].strip().isdigit():
            ncols = max(ncols, len(r))
            if len(r) > 71 and r[71].strip():
                cur[r[0].strip()] = r[71].strip()
    p("")
    p("【现状】%s" % os.path.relpath(TARGET, REPO))
    p("   col71 已有值 %d / %d 行 ✗；最大列数 %d" % (len(cur), len(roster), ncols))
    conflict = [(k, cur[k], best[k][0], best[k][1]) for k in best if k in cur and cur[k] != best[k][0]]
    p("   ★与可信映射**不一致** %d 个（我们写错的值 ✗）" % len(conflict))
    for k, a, b, lb in sorted(conflict)[:14]:
        p("      %-9s 我们=%-10s 应为=%-10s (%s)  我们目录%s" % (k, a, b, lb, "✓" if mid_ok(a) else "✗"))
    if len(conflict) > 14:
        p("      … 另 %d 个" % (len(conflict) - 14))

    badcur = [k for k in cur if not mid_ok(cur[k])]
    p("   ★现有值里\"目录不存在\"的 %d 个 ✗（这些行一旦被读 ⇒ 崩 ✓）" % len(badcur))

    if apply:
        shutil.copy2(TARGET, TARGET + ".bak2")
        p("")
        p("【写入】备份 → %s.bak2" % os.path.relpath(TARGET, REPO))
        rows = read_rows(TARGET)
        fixed = added = kept = 0
        new = []
        for r in rows:
            if not r or not r[0].strip().isdigit():
                new.append(r)
                continue
            key = r[0].strip()
            while len(r) <= 71:
                r.append("")
            if key in best:
                mv = best[key][0]
                if r[71].strip() and r[71].strip() != mv:
                    fixed += 1
                elif not r[71].strip():
                    added += 1
                else:
                    kept += 1
                r[71] = mv
            new.append(r)
        with open(TARGET, "w", encoding="utf-8", newline="") as fh:
            w = csv.writer(fh, lineterminator="\r\n")
            for r in new:
                w.writerow(r)
        p("   col71：新增 %d ｜ 纠正 %d ｜ 保持 %d ｜ 仍空 %d" %
          (added, fixed, kept, len([r for r in new if r and r[0].strip().isdigit() and not r[71].strip()])))

    os.makedirs(NAMES, exist_ok=True)
    open(REPORT, "w", encoding="utf-8").write("\n".join(out))
    p("")
    p("报告 → %s" % os.path.relpath(REPORT, REPO))
    if not apply:
        p("（未改文件 ✓ 要落盘加 `--apply` ✓）")


if __name__ == "__main__":
    main()
