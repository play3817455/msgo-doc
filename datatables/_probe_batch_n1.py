# -*- coding: utf-8 -*-
"""n1 批次体检：CHARA_PARAM / CHARA_MODEL / MSMA_RENTAL / MSMA_MODULE / MSMA_BREAKUP。

只读。逐表打印：
  ① schema JSON 的列数 / csv_index 域 / 空洞 / 重复；
  ② meta.cfg_table_def 是否与 schema JSON 同版本（updated_at + 列数）；
  ③ cfg."<表>" 行数 与 种子 CSV 行数（下发件对账面）。
"""
import io
import json
import os

import psycopg

ROOT = r"f:\9ymsgo\9you"
DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")

# 表名 -> (schema json 相对路径, 种子 CSV 相对路径)
TABLES = {
    "CHARA_PARAM": ("db_design/schema/cfg/tables/CHARA_PARAM.json",
                    "server/datafiles/lounge/msma/msma_settings.csv"),
    "CHARA_MODEL": ("db_design/schema/cfg/tables/CHARA_MODEL.json",
                    "server/datafiles/lounge/msma/msma_model.csv"),
    "MSMA_RENTAL": ("db_design/schema/cfg/tables/MSMA_RENTAL.json",
                    "server/datafiles/lounge/msma/msma_rental.csv"),
    "MSMA_MODULE": ("db_design/schema/cfg/tables/MSMA_MODULE.json",
                    "server/datafiles/lounge/msma/msma_module.csv"),
    "MSMA_BREAKUP": ("db_design/schema/cfg/tables/MSMA_BREAKUP.json",
                     "server/datafiles/lounge/msma/msma_breakup.csv"),
}


def csv_rows(rel):
    p = os.path.join(ROOT, rel)
    if not os.path.exists(p):
        return None
    n = 0
    with io.open(p, encoding="utf-8", errors="replace") as f:
        for line in f:
            s = line.strip()
            if s and not s.startswith("#"):
                n += 1
    return n


def main():
    with psycopg.connect(DSN) as c:
        cur = c.cursor()
        for name, (schema_rel, seed_rel) in TABLES.items():
            print("=" * 72)
            print("## %s" % name)
            sp = os.path.join(ROOT, schema_rel)
            cols = []
            if os.path.exists(sp):
                d = json.load(io.open(sp, encoding="utf-8"))
                cols = d.get("columns") or []
                idxs = [c_.get("csv_index") for c_ in cols]
                seen = {}
                dup = []
                for i in idxs:
                    seen[i] = seen.get(i, 0) + 1
                dup = [k for k, v in seen.items() if v > 1]
                holes = []
                if idxs:
                    lo, hi = min(idxs), max(idxs)
                    holes = [i for i in range(lo, hi + 1) if i not in seen]
                print("  schema: 列数=%d  csv_index %s..%s  空洞=%s  重复=%s"
                      % (len(cols), min(idxs) if idxs else "-",
                         max(idxs) if idxs else "-", holes[:20], dup[:10]))
                print("  schema: asm_reader=%s status=%s purpose=%s"
                      % (d.get("asm_reader"), d.get("asm_status"),
                         (d.get("purpose") or "")[:60]))
            else:
                print("  schema: 缺文件 %s" % schema_rel)

            try:
                cur.execute(
                    "select column_defs, updated_at from meta.cfg_table_def where table_name=%s",
                    (name,),
                )
                row = cur.fetchone()
                if row is None:
                    print("  db.meta: 无行")
                else:
                    defs, updated = row
                    if isinstance(defs, str):
                        defs = json.loads(defs)
                    print("  db.meta: 列数=%d updated_at=%s" % (len(defs), updated))
            except Exception as e:  # noqa: BLE001
                print("  db.meta: ERR %s" % e)

            try:
                cur.execute('select count(*) from cfg."%s"' % name)
                print("  db.cfg : 行数=%d" % cur.fetchone()[0])
            except Exception as e:  # noqa: BLE001
                print("  db.cfg : ERR %s" % e)

            n = csv_rows(seed_rel)
            print("  seed   : %s -> %s 行" % (seed_rel, "缺" if n is None else n))


if __name__ == "__main__":
    main()
