# -*- coding: utf-8 -*-
"""apply_seed_sync_round2.py —— 把 6 张"种子落后"的种子按**库的当前导出**回导（`16-` §8 的 S1）

═══════════════════ 为什么 ═══════════════════
`cfgsync -recreate <表>` = DROP + 按 schema 建表 + **只从种子 CSV 灌**，
而它是 `cfgsync` 唯一推荐的"修列漂移"手法（`sync_db.go` 的 WARN 串）。
下列 6 张表的 ① 已经不是 ② 的忠实快照，`-recreate` 会**静默回滚**（半径见 `16-` §7）：

  #37 WEAPON_SETTING      种子 34 列 vs 库 148 列 ⇒ 丢 19776 格（11 个 #36 连接键 + ammo_type_id）
  #65 ITEM                库 +559 行（名称/图标注册号）
  #34 MSMA_BATTLE_DETAIL  库 +86 行 + WARP_TIME 那批值（409→16）
  #4  CHARA_PARAM         10 台机体在种子里是残行（缺 payload/armor/9 个 battle 键）
  #19 MECHANIC_WEAPON     BUILDUP_GREATEST 行 9 格 success_rate='100'（键也与种子不同）
  #40 BUILDUP_WEAPON      buildup_id=1 的 slot_3..5/7..10_enabled='10'（清了面板就空）

═══════════════════ 怎么写 ═══════════════════
数据源 = **`meta.cfg_manifest.raw_csv`**（= 库的导出 = 客户端实际收到的字节；
`16-` §5 已证 ② ≡ ③）。逐字复制它的数据行，**只换数据区**：

    [种子原有注释头（原样，含 `# ★…` 标记）] + [manifest 的数据行] + CRLF

⇒ 保留注释头、UTF-8 **无 BOM**、**全 CRLF**、数据行内容与库逐字节相同。

⚠️ **唯一的例外**：`#4 CHARA_PARAM` 的 `csv_index=89`（`max_speed_base`）**强制留空** ——
   该列在库里是 586 行"陈旧残值"（只有 {10,20,30,40,50}，量纲不是速度），
   `04-填充日志.md` §11.3 那次"换绑"已把种子清空、`store/battle_params.go` 也**不读它**
   ⇒ 方向是"**库该清、不是种子该填**"，所以回导时把这一格按种子的既有口径留空。

安全
====
- 默认**干跑**；`--apply` 才写。
- 写前逐表备份 `*.bak_seedsync<stamp>`。
- 写后自检（不过就报错、不留半成品）：
    ① 数据行数 == manifest 行数；
    ② 非空数据行集合 == manifest 非空行集合（`#4` 放宽为"把 col89 抹空后相同"）；
    ③ 无 BOM、裸 LF 数 == 0；
    ④ 注释行数与写前相同。
- 只写种子文件，**不动库、不动 manifest**（所以无需再 `-export-only`）。

用法
====
  python datatables/apply_seed_sync_round2.py                 # 干跑（全部 6 张）
  python datatables/apply_seed_sync_round2.py --only ITEM     # 只干跑一张
  python datatables/apply_seed_sync_round2.py --apply         # 写种子
"""
import datetime
import io
import os
import shutil
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

import psycopg

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
LOUNGE = os.path.join(ROOT, "server", "datafiles", "lounge")
DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")

# (表ID, 种子相对路径, 说明, 要强制留空的 csv_index 集合)
TABLES = [
    ("WEAPON_SETTING", "item/weapon_settings.csv", "种子 34 列 → 库 148 列", ()),
    ("ITEM", "item/item.csv", "库 +559 行", ()),
    ("MSMA_BATTLE_DETAIL", "msma/msma_battle_detail.csv", "库 +86 行 + WARP_TIME 值", ()),
    ("CHARA_PARAM", "msma/msma_settings.csv", "10 台残行（col89 留空）", (89,)),
    ("MECHANIC_WEAPON", "develop/mechanic_weapon.csv", "BUILDUP_GREATEST 行", ()),
    ("BUILDUP_WEAPON", "develop/buildup_weapon.csv", "buildup_id=1 的 slot_*", ()),
]


def split_seed(path):
    """(注释头行列表, 原数据行数) —— 头部 = 首个数据行之前的所有行（原样）。"""
    with open(path, "rb") as f:
        raw = f.read()
    bom = raw.startswith(b"\xef\xbb\xbf")
    txt = raw[3:].decode("utf-8") if bom else raw.decode("utf-8")
    lines = txt.replace("\r\n", "\n").split("\n")
    first = None
    for i, l in enumerate(lines):
        if l.strip() and not l.lstrip().startswith("#"):
            first = i
            break
    if first is None:
        raise SystemExit("!! %s 里没有数据行" % path)
    head = lines[:first]
    ndata = sum(1 for l in lines[first:] if l.strip() and not l.lstrip().startswith("#"))
    after_cmt = [l for l in lines[first:] if l.lstrip().startswith("#")]
    if after_cmt:
        raise SystemExit("!! %s 的数据区之后还有 %d 行注释 ⇒ 写法要改，先人工看" % (path, len(after_cmt)))
    return head, ndata, bom


def norm(x):
    """比较用归一：去掉行尾连续空字段（manifest 与种子的尾逗号惯例不同，导入时都会被剥掉）。"""
    s = x.rstrip()
    while s.endswith(","):
        s = s[:-1]
    return s


def manifest_lines(cur, table, blank_cols):
    """manifest.raw_csv 的数据行（去 \\r，尾随空行丢掉）；blank_cols 指定的格清空。

    行内容**逐字照抄**（= `formatCSVLine` 的产物：每行末尾一定有一个逗号）。
    与旧种子唯一的差别是"旧种子里多出来的那个尾逗号"被抹掉 —— 无副作用：
    `cfgsync` 导入时会剥掉连续的空尾字段（`sync_db.go` readCSVRows）。
    """
    cur.execute("select raw_csv from meta.cfg_manifest where file=%s", (table,))
    r = cur.fetchone()
    if not r or r[0] is None:
        raise SystemExit("!! manifest 里没有 %s" % table)
    raw = r[0]
    if isinstance(raw, (bytes, bytearray, memoryview)):
        raw = bytes(raw).decode("utf-8", "replace")
    out = []
    for ln in raw.replace("\r\n", "\n").split("\n"):
        s = ln.rstrip("\r")
        if not s.strip() or s.lstrip().startswith("#"):
            continue
        if blank_cols:
            f = s.split(",")
            for i in blank_cols:
                if i < len(f):
                    f[i] = ""
            s = ",".join(f)
        out.append(s)
    return out


def main():
    apply = "--apply" in sys.argv
    only = set()
    if "--only" in sys.argv:
        only = {x.strip().upper() for x in sys.argv[sys.argv.index("--only") + 1].split(",") if x.strip()}

    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    plan = []
    with psycopg.connect(DSN) as c:
        cur = c.cursor()
        for table, rel, note, blank in TABLES:
            if only and table not in only:
                continue
            path = os.path.join(LOUNGE, rel.replace("/", os.sep))
            head, ndata_old, bom = split_seed(path)
            new = manifest_lines(cur, table, blank)
            print("=" * 96)
            print("## %-20s %s   （%s）" % (table, rel, note))
            print("   注释头 %d 行 ／ 原数据行 %d ／ manifest 数据行 %d ／ BOM=%s"
                  % (len(head), ndata_old, len(new), bom))
            if blank:
                print("   ⚠ 强制留空 csv_index = %s" % (blank,))
            # 自检①：行数
            ok = True
            if not new:
                print("   ✗ manifest 数据行为 0"); ok = False
            # 自检②：与库导出逐行相同（blank 的表：抹空指定列后应相同）
            mb = [norm(x) for x in manifest_lines(cur, table, ())]
            nb = [norm(x) for x in new]
            if blank:
                mb = [norm(x) for x in manifest_lines(cur, table, blank)]
            if sorted(nb) != sorted(mb):
                d1 = len(set(nb) - set(mb))
                d2 = len(set(mb) - set(nb))
                print("   ✗ 数据行集合 != manifest 集合（差 %d/%d）" % (d1, d2)); ok = False
            # 与写前种子的差异（#4 应恰好只有"10 台残行"变）
            old_lines = []
            with open(path, "rb") as f:
                for ln in f.read().decode("utf-8", "replace").replace("\r\n", "\n").split("\n"):
                    if ln.strip() and not ln.lstrip().startswith("#"):
                        old_lines.append(norm(ln.rstrip("\r")))
            so, sn = set(old_lines), set(nb)
            gain = sn - so
            loss = so - sn
            print("   相对写前种子：新增 %d 行 ／ 消失 %d 行" % (len(gain), len(loss)))
            for x in sorted(gain)[:3]:
                print("      + %s" % x[:150])
            for x in sorted(loss)[:3]:
                print("      - %s" % x[:150])
            print("   自检：%s" % ("✓ 可写" if ok else "✗ 不过"))
            body = head + new
            while body and body[-1] == "":
                body.pop()
            nb_bytes = len(("\r\n".join(body) + "\r\n").encode("utf-8"))
            print("   文件体积：%d → %d 字节（%+.0f%%）"
                  % (os.path.getsize(path), nb_bytes,
                     (nb_bytes - os.path.getsize(path)) * 100.0 / max(1, os.path.getsize(path))))
            plan.append((table, rel, path, head, new, ok, stamp))

    if not apply:
        print()
        print("★ 干跑结束：加 --apply 才写种子（逐表备份 *.bak_seedsync%s）。" % stamp)
        return 0

    print()
    for table, rel, path, head, new, ok, stamp in plan:
        if not ok:
            raise SystemExit("✗ %s 自检不过，已中止（未写任何文件）" % table)
    for table, rel, path, head, new, ok, stamp in plan:
        shutil.copy2(path, path + ".bak_seedsync" + stamp)
        body = head + new
        while body and body[-1] == "":
            body.pop()
        with open(path, "wb") as f:
            f.write(("\r\n".join(body) + "\r\n").encode("utf-8"))
        raw = open(path, "rb").read()
        nd = sum(1 for l in raw.decode("utf-8").replace("\r\n", "\n").split("\n")
                 if l.strip() and not l.lstrip().startswith("#"))
        ncmt = sum(1 for l in raw.decode("utf-8").replace("\r\n", "\n").split("\n")
                   if l.lstrip().startswith("#"))
        print("  写入 %-20s 数据行 %5d ／ 注释行 %2d ／ BOM=%s ／ 裸LF=%d"
              % (table, nd, ncmt, raw.startswith(b"\xef\xbb\xbf"),
                 raw.count(b"\n") - raw.count(b"\r\n")))
    print()
    print("★ 完成。种子 ≡ 库导出 ⇒ `cfgsync … -recreate <这 6 张>` 从此安全。")
    print("  复核：python datatables/_scan_threeway_cells.py   （这 6 张应全部转 OK）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
