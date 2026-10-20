# -*- coding: utf-8 -*-
"""生成全表对账报告 -> datatables/17-读表真值全表对账.md

数据来源（全部可复现）：
  _out_emu_readers.py     -> _out_emu_readers.json    Unicorn 真跑 77 个 reader 的真值（列号/写偏移）
  _emu_datadep.py         -> _out_emu_datadep.txt     读列数是否依赖数据（74/77 结构性固定）
  _sweep_verdict.py       -> _out_sweep_verdict.json  与 schema 的读集/内存序对账
  _sweep_width_db.py      -> _out_sweep_width_db.json 与 cfg.* 物理列 / raw_csv 行宽的对账
"""
import io
import json
import os
import sys
from collections import Counter

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
verdict = json.load(open(os.path.join(HERE, "_out_sweep_verdict.json"), encoding="utf-8"))
width = {r["table"]: r for r in json.load(open(os.path.join(HERE, "_out_sweep_width_db.json"), encoding="utf-8"))}
emu = json.load(open(os.path.join(HERE, "_out_emu_readers.json"), encoding="utf-8"))
bytable = verdict["by_table"]

L = []
A = L.append

A("# 17 读表真值全表对账（Unicorn 仿真 vs schema vs 下发 CSV）")
A("")
A("> 复现：`python datatables/_emu_readers.py` → `_emu_datadep.py` → `_sweep_verdict.py` → `_sweep_width_db.py` → `_sweep_report.py`")
A("")
A("## 0. 方法与口径")
A("")
A("1. **真值来源**：Unicorn 32 位跑 `GundamOnline_CHINA_v15.exe` 里 77 个 cfg 逐行读表函数，")
A("   钩住四个 CSV 取列助手（`sub_BBB370` int / `sub_BBB470` float / `sub_BBB4F0`、`sub_456D90` 字符串）")
A("   与枚举转换器，把列号换成唯一标记值再记录 `(写偏移, 标记)` ⇒ 列号来自**真实执行**，")
A("   绕开静态常量传播（可穿透循环展开/指针差技巧）。")
A("2. **静态交叉验证**：`_reader_pushconsts.py` 抽调用点前压栈的立即数列号，与仿真逐条比对一致：")
A("   `sub_58C440`(PLAY_BONUS_REWARD) = `0,1,2,3,4,5,6,7,9`（跳列 8、读列 9）。")
A("3. **越界列语义**（决定危害等级）：`sub_456D90` 反编译")
A("   `if (a3 < (this[29]-this[28])/28) 取该列 else 输出空串` ⇒ **列号 ≥ 行宽 → 空串 → atoi/atof = 0**：")
A("   不崩、不读脏数据；「我们 CSV 比 reader 读的窄」= **这些字段恒为 0（数值缺失）**。")
A("4. **下发链路**：客户端拿到的 CSV = `meta.cfg_manifest.raw_csv`（`cfg.DBStore.ReadFile` 原样下发）；")
A("   GM 改行后 `SyncTableManifest` → `ExportTableRawCSV` 按 `cfg.{表}` **物理列重拼** ⇒ ")
A("   「DB 列数」与「raw_csv 行宽」都必须 ≥ reader 读到的列数。")
A("5. **「读列数是否依赖数据」实验**（`_emu_datadep.py`）：把所有字符串列改回**空串**再跑一遍，")
A("   与返回标记串相比 —— **74/77 个 reader 读集完全不变**（读列数是硬编码的），")
A("   只有 `QUEST`/`ITEM` 变化（它们本来就在仿真失败名单里）⇒ §2/§3 的「读到的列数」是真值，")
A("   不是「读到空列为止」的假象。")
A("6. **结构性佐证**（IDA 反编译，可逐条复查）：")
A("   - `sub_56EA00` AI_PARAM：列游标 `v36` **按引用**传给 `sub_56E890`(吃 5 列)/`sub_56E220`(每块吃 25 列，")
A("     `(*a4)++` 逐个前移)/`sub_56E3F0`(吃 4 列)，三块带 + 头尾 ⇒ 总列数 **127，与数据无关**。")
A("   - `sub_59E170` MISSION_EXTRULE：`v11=6; do{4 列}while(--v13); while(--v23=2)` ⇒ 固定 8 列（列 6..13）。")
A("")
A("## 1. 总览")
A("")
cnt = Counter(v[0] for v in bytable.values())
empty = [r for r in width.values() if r.get("disposition") == "DOWNLOAD" and not r["raw_fields"]]
narrow = [r for r in width.values()
          if r.get("disposition") == "DOWNLOAD" and r["raw_fields"] and r["reader_read_max"]
          and not r["emu_err"] and r["raw_fields"] < r["reader_read_max"]]
narrow.sort(key=lambda r: r["raw_fields"] - r["reader_read_max"])
local = [t for t, r in width.items() if "本地" in str(r["csv_path"])]
A(f"- `cfg.*` 表 **{len(width)}** 张（`AUTOEXEC` 是 SCRIPT，无 reader）")
A(f"- 读集与 schema 一致且内存序可核对：**{cnt['OK']}** 张；读集一致（内存序不可比）：**{cnt['READSET-OK']}** 张")
A(f"- ★ 读集由**静态反汇编**背书（仿真结构性失败）：**{cnt['STATIC-OK']}** 张")
A(f"- 读集有差异：**{cnt['READSET-DIFF']}** 张；仿真不完整：**{cnt['EMU-PARTIAL']}** 张")
A(f"- ★ 下发文件为空的 DOWNLOAD 表：**{len(empty)}** 张 ／ ★ 行宽不足：**{len(narrow)}** 张 ／ 本地表：**{len(local)}** 张")
A("")
A("## 2. ★ 行宽不足：reader 读到的列数 > 我们下发的行宽")
A("")
A("客户端会**稳定读到 0**（§0.3）。§0.5 排除了「读到空列为止」假象，§0.6 用 IDA 逐条验证了固定列数 ⇒ ")
A("**我们的 CSV/DB 真的比客户端读的窄**：这些字段在客户端恒为 0；若原版 CSV 那些列有真值，则与官服行为不一致。")
A("")
A("| 表 | raw_csv 行宽 | DB 列 | reader 实际读到 | schema 记录(声明读) | 缺 | csv_path |")
A("|---|---|---|---|---|---|---|")
for r in narrow:
    A(f"| `{r['table']}` | {r['raw_fields']} | {r['db_cols']} | **{r['reader_read_max']}** | "
      f"{r['schema_defined']}({r['schema_declared']}) | {r['reader_read_max'] - r['raw_fields']} | {r['csv_path']} |")
A("")
A("> 补数据必须补 DB 与 `raw_csv` 两处（`server/datafiles/lounge/**` 只是 bootstrap 种子，只改不生效）。")
A("")
A("> **已修（2026-10-05）**：`PLAY_BONUS_REWARD` 9→10、`PLAYER_NAVI` 17→19、`BUFF` 9→12、")
A("> `MODULE_DEVELOP` 7→13、`MISSION_EXTRULE` 6→14 已按 reader 真读列补齐（含 gap 列），")
A("> 四处同步（schema / GM schema / 种子 / 库+manifest）与验收细节见 **附录 A**（`datatables/17-addendum-补列宽.md`）。")
A("")
A("> **已修（2026-10-05 第二批）**：`QUEST` 行宽 **5 → 25**（reader 真读 `csv24`，旧 schema 把 `push 18h` 记成了 csv4）、")
A("> `WEAPON_SETTING` 15 列 `gap → confirmed`、`MISSION_COOP` `col8 gap → confirmed`（+56 bit2）+ `col5/6/7` `asm_va` 回正一格，")
A("> 见 **附录 B**（`datatables/17-addendum-QUEST宽表.md`）。")
A("")
A("> **已修（2026-10-05 第三批）**：`WEAPON_BATTLE_DETAIL` 行宽 **3 → 9**、`MSMA_BATTLE_DETAIL` 行宽 **3 → 16**")
A("> ——两张表是**回调分派式属性长表**（`sub_A47BC0` 只读 col0，值列由**子表 vtable[0]** 按属性名读，")
A("> 上限分别 col8 / col15）；本批同时消掉 `WEAPON_BATTLE_DETAIL` 的列漂移 WARN，")
A("> 见 **附录 C**（`datatables/17-addendum-属性长表值槽.md`）。")
A("")
A("> **已修（2026-10-05 第四批）**：`BEGINNER_CHALLENGE` 行宽 **6 → 16**、`CHALLENGE_HIGHSCORE` 行宽 **10 → 28**")
A("> ——两张奖励窄表（`sub_570420` / `sub_578630`，结构 = 前导字段 + **固定块循环**；列号与内存偏移逐条")
A("> 由静态反汇编取出），本批同时把全库 `ADD COLUMN` 遗留的 **901 格 `NULL` 归一为 `''`**，")
A("> 见 **附录 D**（`datatables/17-addendum-窄表读列宽.md`）。")
A("")
A("> **已修（2026-10-05 第五批）**：`ITEM_PART` 行宽 **21 → 50**（= 16 前导 + 8 组×3 + 2 尾 + 8 余量）")
A("> ——这张表是**光标式**（8 组顺序消费 CSV，组内列数随参数名而变：`MS_BOOST_GAUGE_RECOV` 组多占 1 列），")
A("> 旧 schema 把 8 组当成单组、把尾列钉死在 csv19/20，")
A("> 见 **附录 E**（`datatables/17-addendum-ITEM_PART光标槽位.md`）。")
A("")
A("> **已修（2026-10-05 第六批）**：`MODULE_BONUS` 行宽 **6 → 41**（= 1 键列 csv1 + 8 组 × {A,B,V}，列步长 5）")
A("> ——旧 schema 只声明了**循环的第 1 组**（csv2/4/5），真实读集是 `csv {5k-3, 5k-1, 5k}` 共 25 列（16 个缝列不读）；")
A("> 本批同时确证 **A>0 才算有效槽**（`sub_5A2A30`/`sub_5A2AF0`）与 **索引键在 csv1**（vtable[5] `sub_5A2A10`），")
A("> 见 **附录 F**（`datatables/17-addendum-MODULE_BONUS组槽.md`）。")
A("")
A("> **已修（2026-10-05 第七批）**：`COMMANDER_NPC` 行宽 **13 → 50**（7 前导 + 4 槽消耗 + 3 槽冷却")
A("> + 12 组 ×{值, 类型名} + 1 尾列；**11 个缝列**）、`MISSION_XWAR_BANPICK` 行宽 **4 → 43**")
A("> （`3 前导 + 40 个 Ban 机体槽`；★**读列数随 `csv2` 变化**：`3 + min(csv2,40)`，43 是上界）、")
A("> `AI_PARAM` 行宽 **45 → 127**（固定头 + 三个同构距离带块 `{3 u8 + 22 float}`×3 + 尾段；")
A("> 旧 `csv19`/`csv22` 两个 gap 是**静态扫描假象** —— 列游标 `v36` 按引用传给 `sub_56E890`/`sub_56E220`/`sub_56E3F0`）")
A("> ⇒ ★**全库偏窄清单归零**，")
A("> 见 **附录 G**（`datatables/17-addendum-第7批缝列与带块.md`）。")
A("")
A("> ⚠️ **口径提醒**：本表的筛选带 `not r['emu_err']` ⇒ **仿真失败（EMU-PARTIAL）的表被静默排除**，")
A("> 于是「仿真跑不完」会伪装成「行宽没问题」。`QUEST` 就是这样**从未出现在本表**却真实偏窄 20 列的例子。")
A("> 核对 EMU-PARTIAL 表的行宽，必须另走 `raw_fields < schema_defined` 或静态反汇编（见附录 B.1）。")
A("")
A("## 3. ★ 声明 DOWNLOAD 但库里 0 行（功能空转）")
A("")
A("`raw_csv` 也没有数据行 ⇒ 客户端下到**空表**，这些功能拿不到任何行。")
A("注意：这些表的 **DB 列宽已 ≥ reader 读到的列数**（下表最后一列 ✓），所以一旦补上数据行，行宽是够的；")
A("它们缺的是**数据本身**，不是列结构。")
A("")
A("| 表 | DB 列 | DB 行数 | raw_csv 行数 | reader 读到 | 列宽够? | csv_path |")
A("|---|---|---|---|---|---|---|")
for r in sorted(empty, key=lambda x: x["table"]):
    rm = r["reader_read_max"]
    A(f"| `{r['table']}` | {r['db_cols']} | {r['db_rows']} | {r['raw_rows']} | {rm} | "
      f"{'✓' if (not rm or (r['db_cols'] or 0) >= rm) else '✗'} | {r['csv_path']} |")
A("")
A("## 4. schema 声明了 reader 根本不读的列（schema 高估 / reader 映射可疑）")
A("")
A("| 表 | schema 声明读 | 仿真实际读 | schema 有仿真无 |")
A("|---|---|---|---|")
for t, (vd, note, reader, reads) in sorted(bytable.items()):
    if vd != "READSET-DIFF" or "仿真有schema无=[]" not in note:
        continue
    miss = note.split("schema有仿真无=[")[1].split("]")[0]
    decl = width[t]["schema_declared"] if t in width else None
    A(f"| `{t}` | {decl} | {len([x for x in reads if x is not None])} | {miss[:200]} |")
A("")
A("## 5. 其余读集差异（读多也读少，多为「固定块循环」多实例）")
A("")
A("| 表 | reader | schema有仿真无 | 仿真有schema无 |")
A("|---|---|---|---|")
for t, (vd, note, reader, reads) in sorted(bytable.items()):
    if vd != "READSET-DIFF" or "仿真有schema无=[]" in note:
        continue
    miss = note.split("schema有仿真无=[")[1].split("]")[0] if "schema有仿真无=[" in note else ""
    extra = note.split("仿真有schema无=[")[1].split("]")[0] if "仿真有schema无=[" in note else ""
    A(f"| `{t}` | {reader} | {miss[:120]} | {extra[:200]} |")
A("")
A("## 6. 仿真不完整的表（EMU-PARTIAL：CRT 断言 / 指令上限截断；结论只取静态反汇编）")
A("")
A("| 表 | reader | 崩点 / 截断 | 截断前已请求列 |")
A("|---|---|---|---|")
for t, (vd, note, reader, reads) in sorted(bytable.items()):
    if vd != "EMU-PARTIAL":
        continue
    A(f"| `{t}` | {reader} | {note} | {reads} |")
A("")
A("> `Invalid memory mapping (UC_ERR_MAP)` = reader 在假参数下要访问未映射页（多为「目标 buffer 未分配」）；")
A("> `EMU-CUT(limit)` = 跑到指令上限（该表函数长 / 含 CRT 循环）；`UC_ERR_EXCEPTION` = 拿到的「伪指针」直接触发异常。")
A("> 这三类都不是「schema 错」，但**它们的读集不能由仿真背书** ⇒ 必须逐条 IDA 复核（本批 `QUEST`/`WEAPON_SETTING`/`MISSION_COOP` 即如此）。")
A("")
A("## 7. 本地表（不下发；客户端读自己那份，无需对账）")
A("")
A("  " + "  ".join(f"`{t}`" for t in sorted(local)))
A("")
A("## 8. 已核对一致的表")
A("")
ok = sorted(t for t, v in bytable.items() if v[0] in ("OK", "READSET-OK", "STATIC-OK"))
A(f"（{len(ok)} 张）" + "  ".join(f"`{t}`" for t in ok))
A("")
A("其中 `MSMA_BATTLE_DETAIL` / `WEAPON_BATTLE_DETAIL` 的读集由**静态反汇编**背书（见附录 C）：")
A("它们走**回调 vtable 分派**，仿真器没有那两个子表对象 ⇒ 必然 `UC_ERR_EXCEPTION`，")
A("**不是**「读集未知」，而是「仿真这条线结构上跑不通」。")
A("")
A("## 9. 与 #50 MODULE 的关系")
A("")
A("- `MODULE` 现判定 **OK**：读集 `{0,2,3,4,5,7,8,9}`、内存序 `+0/+20/+4/+8/+16/+12/+24/+28` 与 schema 完全一致，")
A("  下发 10 字段 = reader 读 8 列 + 2 个 gap 列 ✓（修复前 schema 少一列 ⇒ 后面 8 列整体错名）。")
A("- 全表扫描**未发现第二个同类「列名整体错位」**（`MISALIGN=0`）。")

text = "\n".join(L)
for add in ("17-addendum-补列宽.md", "17-addendum-QUEST宽表.md", "17-addendum-属性长表值槽.md",
            "17-addendum-窄表读列宽.md", "17-addendum-ITEM_PART光标槽位.md",
            "17-addendum-MODULE_BONUS组槽.md", "17-addendum-第7批缝列与带块.md"):
    p = os.path.join(HERE, add)
    if os.path.isfile(p):
        text += "\n" + open(p, encoding="utf-8").read().rstrip("\n")
out = os.path.join(HERE, "17-读表真值全表对账.md")
open(out, "w", encoding="utf-8").write(text + "\n")
print(text[:900])
print(f"\n...wrote {out} ({len(text)} chars, narrow={len(narrow)} empty={len(empty)})")
