# -*- coding: utf-8 -*-
"""_probe_manifest_payload.py —— 直接解析**下发用的 manifest 字节**（只读）

`_probe_manifest_after.py` 报 "manifest #1 引用 1626 把武器 / 其中 1 把无 #37 行"，
与真库的 0 断引用不符 ⇒ 查清是解析假象还是真断链。
本脚本不依赖任何启发式：直接读 `meta.cfg_manifest.raw_csv`，按
"行首非 # 且非空" 判定数据行，再做引用对账。
"""
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import psycopg

DSN = "postgresql://postgres:admin123@127.0.0.1:5432/msgo"


def payload(cur, name):
    cur.execute("SELECT raw_csv FROM meta.cfg_manifest WHERE file = %s", (name,))
    row = cur.fetchone()
    if not row:
        raise SystemExit("manifest 无 %s" % name)
    return row[0].decode("utf-8", "replace")


def data_rows(text):
    out = []
    for i, ln in enumerate(text.split("\r\n")):
        if not ln.strip() or ln.lstrip().startswith("#"):
            continue
        out.append((i, ln))
    return out


with psycopg.connect(DSN) as conn:
    cur = conn.cursor()
    t1 = payload(cur, "MSMA_WEAPONSET")
    t37 = payload(cur, "WEAPON_SETTING")

rows1 = data_rows(t1)
rows37 = data_rows(t37)
print("manifest #1  数据行 %d" % len(rows1))
print("manifest #37 数据行 %d" % len(rows37))

k37 = set()
for _, ln in rows37:
    k37.add(ln.split(",")[0].strip())

used = []
for i, ln in rows1:
    parts = ln.split(",")
    if len(parts) < 3:
        used.append((i, ln, "", "列数不足"))
        continue
    used.append((i, ln, parts[2].strip(), ""))

miss = [x for x in used if x[2] not in k37]
print()
print("manifest #1 引用不到的武器：%d" % len(miss))
for i, ln, w, why in miss:
    print("  line %d  weapon=%r  %s" % (i, w, why))
    print("    %r" % ln[:140])

ids = {w for _, _, w, _ in used if w}
print()
print("去重武器数 %d ／ 命中 #37 的 %d" % (len(ids), len(ids & k37)))

# 行首几行是什么
print()
print("manifest #1 前 6 个非空行：")
for i, ln in [(i, l) for i, l in [(i, l) for i, l in enumerate(t1.split("\r\n")) if l.strip()][:6]]:
    print("  [%d] %r" % (i, ln[:120]))
