# -*- coding: utf-8 -*-
"""apply_msma_module_align.py —— `MSMA_MODULE`（#53 / `msma/msma_module.csv`）键域收敛

═════════════════════════ 病（2026-10-05 n1 体检 · 用户选 A）═════════════════════════
本表是**统一占位**：全部行的 payload 逐字节相同（`_probe_module_gap.py`：payload 形态数 = 1）：

    ,4011301,,4011501,,4011503,,4011601,,4011701,,4011901,,4012001,,4012201,,4011301,,4011501,,

键集 = `names/机体总表.csv`(700) − 34（`_probe_module_src.py`），相对**权威键域**
`CHARA_PARAM`(698) 双向偏差：

  缺 34 台    ：`#4` 有、本表无 ⇒ `sub_57EAE0` 返回 null ⇒ 10 槽全 0 ⇒ **装不了模块**
  反向多 2 台 ：`1147052 ガーベラ・テトラ改` / `1155051 Zプラス（テスト機カラー）`
                —— 是 `favms_ok_list.csv` 里被 `#` **停用**的项，`#4` 已收敛到 698 后本表没跟改

键域权威性（IDA，2026-10-05）：`sub_623DE0` 里同一个 `*(_DWORD *)v24`（机体行首 = `col0`）
既查 `sub_57EAE0`（本表）又查 `sub_581200`（CHARA_PARAM）⇒ **本表查键 == `CHARA_PARAM` 行键 == 練度ID**。

⇒ 收敛口径：**本表 698 行，键集与 `CHARA_PARAM` 逐键相同**，payload 沿用现有统一占位
（补的 34 行 = "往占位里加占位"，不引入任何新语义）。

═════════════════════════ 账 ═════════════════════════════
  种子 666 行 → 698 行（−2 停用 + 34 补齐）
  35 张表…不，本脚本**只动这一张**；库侧交给 cfgsync 的 `-recreate`：

    cd serverv
    go run ./tools/cfgsync -schema-dir ../db_design/schema/cfg/tables \
        -bootstrap-csv ../server/datafiles/lounge -recreate MSMA_MODULE -migrate=false

  `-recreate` 会 DROP + 按 CSV 重建 + 重建 `meta.cfg_manifest`（`SyncAll` 末尾必然 exportManifest），
  `ORDER BY _row_id` ⇒ 导出序 == 种子序 ⇒ 种子与库导出可逐字节对账。

安全
====
- 默认**干跑**；`--apply` 才写。
- 写前备份种子 → `msma_module.csv.bak_align<stamp>`（`_bak_*` 已在 `.gitignore` 之外的常规命名）。
- 写后自检：行数 698 / 键集 == `CHARA_PARAM` / payload 单一形态 / 无 BOM / 全 CRLF。

用法
====
  python datatables/apply_msma_module_align.py            # 干跑
  python datatables/apply_msma_module_align.py --apply    # 写种子
"""
import csv
import datetime
import io
import os
import shutil
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

import psycopg

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
MSMA = os.path.join(ROOT, "server", "datafiles", "lounge", "msma")
SEED = os.path.join(MSMA, "msma_module.csv")
PARAM = os.path.join(MSMA, "msma_settings.csv")
DROP = ["1147052", "1155051"]
RB_DIR = os.path.join(HERE, "_rollback")
DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")


def dump_db_table(stamp):
    """把 cfg."MSMA_MODULE" 整表（含 _row_id）导出到 _rollback/，供回滚。"""
    with psycopg.connect(DSN) as c:
        cur = c.cursor()
        cur.execute(
            "select ordinal_position, column_name from information_schema.columns "
            "where table_schema='cfg' and table_name='MSMA_MODULE' order by ordinal_position")
        cols = [n for _, n in cur.fetchall()]
        cur.execute('select * from cfg."MSMA_MODULE" order by _row_id')
        rows = cur.fetchall()
    os.makedirs(RB_DIR, exist_ok=True)
    p = os.path.join(RB_DIR, "%s_MSMA_MODULE_full.csv" % stamp)
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        w = csv.writer(f)
        w.writerow(cols)
        w.writerows([["" if v is None else str(v) for v in r] for r in rows])
    return p, cols, len(rows)


def read_rows(path):
    """(原文本, 行列表[含 \\r\\n], 数据行行号列表, 键) —— 按 \\r\\n 切，LF-only 也能读。"""
    with open(path, "rb") as f:
        raw = f.read()
    if raw.startswith(b"\xef\xbb\xbf"):
        raise SystemExit("!! 种子带 BOM：%s" % path)
    text = raw.decode("utf-8")
    lines = text.replace("\r\n", "\n").split("\n")
    idx, keys = [], []
    for i, ln in enumerate(lines):
        if not ln.strip() or ln.lstrip().startswith("#"):
            continue
        idx.append(i)
        keys.append(ln.split(",", 1)[0].strip())
    return text, lines, idx, keys


def main():
    apply = "--apply" in sys.argv

    text, lines, idx, keys = read_rows(SEED)
    _, plines, pidx, pkeys = read_rows(PARAM)
    param_keys = list(pkeys)
    param_set = set(pkeys)

    payloads = {lines[i].split(",", 1)[1] for i in idx}
    print("=== 种子 %s ===" % os.path.relpath(SEED, ROOT))
    print("  数据行 %d ／ 唯一键 %d ／ 不同 payload 形态 %d" % (len(idx), len(set(keys)), len(payloads)))
    if len(payloads) != 1:
        raise SystemExit("!! payload 不是单一形态 ⇒ 本脚本的前提不成立，先人工看")
    sample = lines[idx[0]]
    suffix = sample[len(sample.split(",", 1)[0]):]   # 含「键后第 1 个逗号」起的全部内容
    print("  payload（键后全量）= %r" % suffix)

    present = set(keys)
    drop_hit = [k for k in DROP if k in present]
    missing = [k for k in param_keys if k not in present]
    extra = sorted(present - param_set)
    print()
    print("=== 收敛账 ===")
    print("  CHARA_PARAM 键 %d" % len(param_keys))
    print("  应删（停用项）%d ：%s" % (len(drop_hit), drop_hit))
    print("  应补（缺口）  %d ：%s" % (len(missing), missing))
    print("  反向多余      %d ：%s" % (len(extra), extra))
    if sorted(drop_hit) != sorted(DROP):
        print("  ⚠ 应删集合与预期不符（预期 %s）⇒ 先人工看一眼" % DROP)
    if sorted(extra) != sorted(DROP):
        print("  ⚠ 反向多余 != 应删集合 ⇒ 有别的偏差，先人工看")
    want_n = len(present) - len(drop_hit) + len(missing)
    print("  写后行数 = %d − %d + %d = %d（目标 %d）"
          % (len(present), len(drop_hit), len(missing), want_n, len(param_keys)))

    drop_pos = {i for i in idx if lines[i].split(",", 1)[0].strip() in DROP}
    keep_idx = [i for i in idx if i not in drop_pos]
    new_lines = ["%s%s" % (k, suffix) for k in missing]

    # 只摘掉被删的数据行；注释行/空行原样保留，新行插在最后一个数据行之后
    out = [ln for i, ln in enumerate(lines) if i not in drop_pos]
    last_line = lines[max(keep_idx)]
    pos = next(i for i, ln in enumerate(out) if ln is last_line) + 1
    out = out[:pos] + new_lines + out[pos:]

    while out and out[-1] == "":
        out.pop()
    body = [l for l in out if l.strip() and not l.lstrip().startswith("#")]
    newkeys = [l.split(",", 1)[0].strip() for l in body]
    print()
    print("=== 自检 ===")
    ok = True
    n_cmt_before = sum(1 for l in lines if l.lstrip().startswith("#"))
    n_cmt_after = sum(1 for l in out if l.lstrip().startswith("#"))
    if n_cmt_after != n_cmt_before:
        print("  ✗ 注释行 %d → %d（应原样保留）" % (n_cmt_before, n_cmt_after)); ok = False
    if out[0] != lines[0]:
        print("  ✗ 首行（表头注释）被改动"); ok = False
    if len(body) != want_n:
        print("  ✗ 数据行 %d != %d" % (len(body), want_n)); ok = False
    if set(newkeys) != param_set or len(newkeys) != len(set(newkeys)):
        print("  ✗ 键集 != CHARA_PARAM 或 有重复"); ok = False
    if {l.split(",", 1)[1] for l in body} != payloads:
        print("  ✗ payload 形态被破坏"); ok = False
    if len(newkeys) != len(param_keys):
        print("  ✗ 行数 %d != CHARA_PARAM %d" % (len(newkeys), len(param_keys))); ok = False
    print("  行 %d ／ 唯一键 %d ／ payload 单一 %s"
          % (len(body), len(set(newkeys)), "✓" if ok else "✗"))
    print("  键集 == CHARA_PARAM :", set(newkeys) == param_set)
    if not ok:
        raise SystemExit("✗ 自检失败，未写")

    if not apply:
        print()
        print("★ 干跑：加 --apply 写种子。")
        print("  新增的前 5 行预览：")
        for l in new_lines[:5]:
            print("    " + l)
        return 0

    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    bak = SEED + ".bak_align" + stamp
    rb, rbcols, rbn = dump_db_table(stamp)
    shutil.copy2(SEED, bak)
    print()
    print("库表回滚件 → %s（%d 行 × %d 列，含 _row_id）"
          % (os.path.relpath(rb, ROOT), rbn, len(rbcols)))
    print("种子备份 → %s" % os.path.relpath(bak, ROOT))
    with open(SEED, "wb") as f:
        f.write(("\r\n".join(out) + "\r\n").encode("utf-8"))
    _, l2, i2, k2 = read_rows(SEED)
    with open(SEED, "rb") as f:
        b = f.read()
    print("  已写：数据行 %d ／ 键 %d ／ BOM %s ／ 裸LF %d"
          % (len(i2), len(set(k2)), b.startswith(b"\xef\xbb\xbf"),
             b.count(b"\n") - b.count(b"\r\n")))
    print()
    print("下一步（库 + manifest）：")
    print("  cd serverv && go run ./tools/cfgsync -schema-dir ../db_design/schema/cfg/tables \\")
    print("      -bootstrap-csv ../server/datafiles/lounge -recreate MSMA_MODULE -migrate=false")
    return 0


if __name__ == "__main__":
    sys.exit(main())
