# -*- coding: utf-8 -*-
"""apply_msma_module_cleanup.py —— `MSMA_MODULE`（#53 / `msma/msma_module.csv`）收尾

═════════════════════════════ 病（2026-10-05 n1 体检）═════════════════════════════
`msma/msma_module.csv` 现有 **668 行**，其中 **2 行是脏键**：

    0            ,,4011301,,…,4011501,     ← 練度ID 里不存在 0
    101286001    ,,4011301,,…,4011501,     ← 这是「モデルID」，不是練度ID

两行 payload 与真行 `1124102` **逐字节相同**（`_probe_module_dirty.py` 实测），
即复制粘贴残渣。客户端**永远查不中**它们（查键域见下），属清尾项
（`04-填充日志.md` 2026-09-28「遗留②」已登记）。

★★ 键域确证（IDA，2026-10-05，本轮补）= **練度ID** ★★
  ① `sub_623DE0`（机体运行时对象 ctor）：
       v45 = sub_57EAE0(*(_DWORD *)v24);          // v24 = 机体行指针
       if ( v45 ) qmemcpy(this + 48, v45 + 4, 0x28);   // 拷 10 dword = 10 个槽
     而同一个 `*(_DWORD *)v24`（= 行首 dword = `col0`）在**同一函数里**被拿去查
     `dword_11E3F14`（= CHARA_PARAM）：
       v39 = this[2];  j = v39;  sub_581200((_DWORD *)(dword_11E3F14 + 4), &v51, &j);
     ⇒ **MSMA_MODULE 的查键 == CHARA_PARAM 的行键 == 練度ID**（不是モデルID）。
  ② `sub_7DAAC0`（机库 UI）也只在 `*(row+4*n) > 0` 时才用第 n 个槽 ⇒ **0 = 不可用** ✓

⇒ 删掉这 2 行（666 行真键），不改任何真行的值。

★★ 附带修（2026-10-05）：**行尾符 LF → CRLF** ★★
  本表是全库**唯一一张成规模违规**的 LF-only 种子（670 个裸 LF / 0 个 CRLF），
  而填写规则明写「UTF-8 无 BOM + **CRLF**」，其余 81 张种子（含 `#36`/`#37`）都已合规。
  全树扫描（`_probe_lineendings_all.py`）：80 个文件带裸 LF，其中 **76 个是 4 行占位骨架**
  （`server/datafiles/<prefix>_<name>.csv` 的旧拷件，不被下发链读），
  真正有内容的只有 4 个：本表（668 行）、`lounge/module/module.csv`（9 行）、
  `lounge/reward/play_bonus_reward.csv`（~72 行）、`lounge/develop/mechanic_msma.csv`（4 行）。
  客户端解析器容忍 LF（这几张表线上都在用）⇒ **严重度低**，但会破坏「种子 == 库导出」的逐字节对账，
  故随本次一并归一。

 ⚠️ 覆盖缺口（**只报不改**）：`CHARA_PARAM` 698 键 － `MSMA_MODULE` 666 真键 = **缺 32 台**
  （另有 `1147052`/`1155051` 是 MSMA_MODULE 独有、CHARA_PARAM 没有的反向 2 个）。
  缺行的后果 = 那 32 台 `sub_57EAE0` 返回 null ⇒ 模块槽全 0（**装不了模块**）。
  没有来源就不补（项目铁律）；先记账。

═════════════════════════════ 账 ═════════════════════════════════
  种子 668 行 → 666 行 ；库同（写后自检）
  666 + 2 脏 = 668 ✓

安全
====
- 默认**干跑**；`--apply` 才写。
- 写前把整张 `cfg."MSMA_MODULE"` 导出 `_rollback/<stamp>_MSMA_MODULE_full.csv`，
  种子备份 `msma_module.csv.bak_cleanup<stamp>`。
- 库写入单事务 + 写后自检，不过就 ROLLBACK。

用法
====
  python datatables/apply_msma_module_cleanup.py            # 干跑
  python datatables/apply_msma_module_cleanup.py --apply    # 写库 + 改种子
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
SEED = os.path.join(ROOT, "server", "datafiles", "lounge", "msma", "msma_module.csv")
RB_DIR = os.path.join(HERE, "_rollback")
DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")
TABLE = "MSMA_MODULE"
DIRTY = ["0", "101286001"]


def read_seed():
    """行尾符无关的读法（★本表当前是 LF-only，见 docstring「附带修」）。"""
    with open(SEED, encoding="utf-8", newline="") as fh:
        raw = fh.read()
    crlf = raw.count("\r\n")
    lf_only = raw.count("\n") - crlf
    lines = raw.replace("\r\n", "\n").split("\n")
    data = [l for l in lines if l.strip() and not l.startswith("#")]
    return raw, lines, data, crlf, lf_only


def main():
    apply = "--apply" in sys.argv
    raw, lines, data, crlf, lf_only = read_seed()
    keys = [l.split(",")[0].strip() for l in data]
    print("=== 种子 ===")
    print("  %s" % os.path.relpath(SEED, ROOT))
    print("  行 %d ／ 唯一键 %d ／ CRLF %d ／ 裸LF %d" % (len(data), len(set(keys)), crlf, lf_only))
    if lf_only:
        print("  ⚠ 本表行尾符是 **LF-only**（填写规则要求 CRLF）⇒ 随本次一并归一为 CRLF")
    hit = [k for k in DIRTY if k in keys]
    print("  脏键命中：%s" % hit)
    if set(hit) != set(DIRTY):
        print("  ⚠ 脏键与预期不符（预期 %s）⇒ 先人工看一眼" % DIRTY)

    with psycopg.connect(DSN) as conn:
        cur = conn.cursor()
        cur.execute(
            "select ordinal_position, column_name from information_schema.columns "
            "where table_schema='cfg' and table_name=%s order by ordinal_position",
            (TABLE,),
        )
        dbcols = [n for _, n in cur.fetchall()]
        cur.execute('select %s from cfg."%s"' % (", ".join('"%s"' % c for c in dbcols), TABLE))
        allrows = cur.fetchall()
        cur.execute('select count(*) from cfg."%s"' % TABLE)
        n0 = cur.fetchone()[0]
        cur.execute(
            'select count(*) from cfg."%s" where btrim(%s) in (%s)'
            % (TABLE, '"%s"' % dbcols[1], ", ".join("'%s'" % k for k in DIRTY))
        )
        ndirty = cur.fetchone()[0]

    print()
    print("=== 库 ===")
    print("  行 %d ／ 列 %d ／ 脏键行 %d" % (n0, len(dbcols), ndirty))
    print("  写后应达：%d 行（-%d）" % (n0 - ndirty, ndirty))

    # 覆盖缺口（只报不改）：CHARA_PARAM 有、MSMA_MODULE 没有的键
    cur2 = psycopg.connect(DSN)
    c2 = cur2.cursor()
    c2.execute('select btrim(msma_id) from cfg."CHARA_PARAM"')
    cp = {r[0] for r in c2.fetchall()}
    c2.execute('select btrim(msma_id) from cfg."%s"' % TABLE)
    mm = {r[0] for r in c2.fetchall()}
    c2.execute('select count(*) from cfg."MSMA_BATTLE_DETAIL"')
    miss = sorted(cp - mm)
    print()
    print("=== 覆盖缺口（只报不改）===")
    print("  CHARA_PARAM %d 键 ／ MSMA_MODULE %d 键 ／ 缺 %d"
          % (len(cp), len(mm), len(miss)))
    print("  缺的前 10 个：%s" % miss[:10])
    extra = sorted(mm - cp)
    print("  MSMA_MODULE 独有 %d 个：%s" % (len(extra), extra[:10]))
    cur2.close()

    if not apply:
        print()
        print("★ 干跑：加 --apply 写入。")
        return 0

    os.makedirs(RB_DIR, exist_ok=True)
    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    rb = os.path.join(RB_DIR, "%s_%s_full.csv" % (stamp, TABLE))
    with open(rb, "w", encoding="utf-8", newline="\n") as f:
        w = csv.writer(f)
        w.writerow(dbcols)
        w.writerows([["" if v is None else str(v) for v in r] for r in allrows])
    seed_bak = SEED + ".bak_cleanup" + stamp
    shutil.copy2(SEED, seed_bak)
    print()
    print("回滚件 → %s（%d 行 × %d 列）" % (os.path.relpath(rb, ROOT), len(allrows), len(dbcols)))
    print("种子备份 → %s" % os.path.relpath(seed_bak, ROOT))

    with psycopg.connect(DSN) as conn:
        cur = conn.cursor()
        try:
            cur.execute(
                'delete from cfg."%s" where btrim(%s) in (%s)'
                % (TABLE, '"%s"' % dbcols[1], ", ".join("'%s'" % k for k in DIRTY))
            )
            print("  库已删：%d 行（期望 %d）" % (cur.rowcount, ndirty))
            if cur.rowcount != ndirty:
                raise AssertionError("删除行数不符")
            cur.execute('select count(*) from cfg."%s"' % TABLE)
            n1 = cur.fetchone()[0]
            cur.execute(
                'select count(*) from cfg."%s" where btrim(%s) in (%s)'
                % (TABLE, '"%s"' % dbcols[1], ", ".join("'%s'" % k for k in DIRTY))
            )
            still = cur.fetchone()[0]
            if still or n1 != n0 - ndirty:
                raise AssertionError("写后自检不过：脏行残留 %d ／ 行 %d" % (still, n1))
            print("  自检：脏行残留 %d ／ 行 %d  ✓" % (still, n1))
            conn.commit()
            print("★ 已提交")
        except Exception as e:  # noqa: BLE001
            conn.rollback()
            print("✗ 失败已 ROLLBACK：%s" % e)
            raise

    kept = [l for l in lines
            if not (l.strip() and not l.startswith("#") and l.split(",")[0].strip() in DIRTY)]
    # ★行尾符归一为 CRLF（本表原本是 LF-only）；保留末尾空行外的原始行序
    while kept and kept[-1] == "":
        kept.pop()
    with open(SEED, "w", encoding="utf-8", newline="") as f:
        f.write("\r\n".join(kept) + "\r\n")
    _, _, data2, crlf2, lf2 = read_seed()
    print("  种子已写：%d → %d 行（-%d）／CRLF %d 裸LF %d"
          % (len(data), len(data2), len(data) - len(data2), crlf2, lf2))

    print()
    print("下一步（否则客户端看不到）：")
    print("  cd serverv; go run ./tools/cfgsync -schema-dir ../db_design/schema/cfg/tables"
          " -export-only -migrate=false")
    return 0


if __name__ == "__main__":
    sys.exit(main())
