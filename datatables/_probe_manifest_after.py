# -*- coding: utf-8 -*-
"""_probe_manifest_after.py —— 重导后复核：`meta.cfg_manifest` 是否 ≡ 真库。

覆盖 15- 文档 §0.1 / §11.1 的三张表，以及本轮收敛的 #1 MSMA_WEAPONSET。
只报告，不写。
"""
import hashlib
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import psycopg

DSN = "postgresql://postgres:admin123@127.0.0.1:5432/msgo"
TABLES = [("MSMA_WEAPONSET", None), ("WEAPON_BATTLE_DETAIL", None),
          ("WEAPON_SETTING", None), ("ITEM", None), ("BUILDUP_WEAPON", None)]


def main():
    with psycopg.connect(DSN) as conn:
        cur = conn.cursor()
        print("%-22s %8s %8s %6s %s" % ("表", "manifest", "真库", "sha", "判定"))
        for tbl, _ in TABLES:
            cur.execute("select raw_csv, row_count, sha256 from meta.cfg_manifest where file=%s", (tbl,))
            row = cur.fetchone()
            if row is None:
                print("%-22s %s" % (tbl, "(manifest 无此表)"))
                continue
            raw, mrows, msha = row
            raw_b = raw if isinstance(raw, bytes) else raw.encode("utf-8")
            cur.execute('select count(*) from cfg."%s"' % tbl)
            dbrows = cur.fetchone()[0]
            sha = hashlib.sha256(raw_b).hexdigest()
            ok = (mrows == dbrows) and (sha == msha)
            print("%-22s %8s %8d %6s %s"
                  % (tbl, mrows, dbrows, ("✓" if sha == msha else "✗"), ("✓ 一致" if ok else "✗ 不一致")))
        print()
        print("=== #1 MSMA_WEAPONSET 内容抽查（前 3 行 + 尾部）===")
        cur.execute("select raw_csv from meta.cfg_manifest where file='MSMA_WEAPONSET'")
        raw = cur.fetchone()[0]
        raw = raw if isinstance(raw, str) else raw.decode("utf-8", "replace")
        lines = [l for l in raw.replace("\r\n", "\n").split("\n") if l.strip()]
        for l in lines[:3]:
            print("   %s" % l)
        print("   ...")
        for l in lines[-2:]:
            print("   %s" % l)
        data = [l for l in lines if not l.lstrip().startswith("#")]
        groups = {l.split(",")[0].strip() for l in data}
        ids = {l.split(",")[2].strip() for l in data if len(l.split(",")) > 2}
        print("   数据行 %d ／ 组 %d ／ 武器 %d ／ 号长 %s"
              % (len(data), len(groups), len(ids),
                 sorted({len(i) for i in ids})))

        print()
        print("=== 断引用复核（manifest 内自洽）===")
        cur.execute("select raw_csv from meta.cfg_manifest where file='WEAPON_SETTING'")
        w37 = cur.fetchone()[0]
        w37 = w37 if isinstance(w37, str) else w37.decode("utf-8", "replace")
        keys37 = {l.split(",")[0].strip() for l in
                  w37.replace("\r\n", "\n").split("\n") if l.strip() and not l.startswith("#")}
        miss = ids - keys37
        print("   manifest #1 引用 %d 把武器 ／ 其中 manifest #37 无行 %d" % (len(ids), len(miss)))
        print("   manifest #37 键 %d" % len(keys37))


if __name__ == "__main__":
    main()
