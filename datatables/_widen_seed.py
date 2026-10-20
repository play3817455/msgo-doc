# -*- coding: utf-8 -*-
"""把 5 张窄表的种子 CSV 行宽补到「客户端 reader 真读列数」（与 schema/cfg 表一致）。

- 只**追加空字段**，不动既有字段值（例：PLAY_BONUS_REWARD col4=65535 崩溃哨兵保持在索引 4）；
- 每个种子补一行 reader 映射注释（与 MODULE 种子同款：csvN→+off / 不读的列）；
- 行尾风格沿用原文件（LF / CRLF 各自保留）；
- 原文件先备份到 datatables/_backup_seeds/<相对路径>。
"""
import io
import json
import os
import shutil
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SCHEMA = os.path.join(ROOT, "db_design", "schema", "cfg", "tables")
SEED_ROOT = os.path.join(ROOT, "server", "datafiles", "lounge")
BACKUP = os.path.join(HERE, "_backup_seeds")

TABLES = ["PLAY_BONUS_REWARD", "PLAYER_NAVI", "BUFF", "MODULE_DEVELOP", "MISSION_EXTRULE"]
STAMP = "★2026-10-05 补列宽"

log = []


def emit(s=""):
    print(s)
    log.append(s)


for t in TABLES:
    spec = json.load(open(os.path.join(SCHEMA, t + ".json"), encoding="utf-8"))
    cols = sorted(spec["columns"], key=lambda c: c["csv_index"])
    width = max(c["csv_index"] for c in cols) + 1
    reads, skips = [], []
    for c in cols:
        if c.get("status") == "gap":
            skips.append(str(c["csv_index"]))
        else:
            off = c.get("memory_offset")
            reads.append(f"{c['csv_index']}" + (f"→+{off}" if off is not None else "→(不落内存)"))
    note = (
        f"# 表ID {spec.get('table_id','?')}｜CSV {width} 列（csv 0..{width-1}）｜reader "
        f"{spec.get('asm_reader')} 按**绝对列号**取值：{'、'.join(reads)}"
        + (f"；csv {'、'.join(skips)} 不读" if skips else "")
        + f"｜{STAMP}：本表旧种子行宽不足，已补空列到 {width} 列（补列为占位 0；"
          f"缺列时客户端 sub_456D90 越界返回 \"\" ⇒ atoi 0，行为等价）"
    )

    rel = spec["csv_path"]
    path = os.path.join(SEED_ROOT, *rel.split("/"))
    raw = open(path, "rb").read()
    crlf = raw.count(b"\r\n") > 0
    nl = "\r\n" if crlf else "\n"
    text = raw.decode("utf-8")
    # 统一按 \n 处理，写出时再还原行尾
    lines = text.replace("\r\n", "\n").split("\n")
    trailing_empty = lines and lines[-1] == ""

    bdir = os.path.join(BACKUP, *rel.split("/"))
    os.makedirs(os.path.dirname(bdir), exist_ok=True)
    shutil.copyfile(path, bdir)

    out, inserted, grew = [], False, 0
    for ln in lines:
        body = ln.rstrip("\r")
        stripped = body.strip()
        if stripped.startswith("#"):
            out.append(body)
            continue
        if stripped == "":
            if body != "":
                out.append(body)
            continue
        if not inserted:
            out.append(note)
            inserted = True
        fields = body.strip().split(",")
        while fields and fields[-1] == "":
            fields.pop()
        if len(fields) < width:
            grew += 1
            fields += [""] * (width - len(fields))
        out.append(",".join(fields) + ",")
    if trailing_empty:
        out.append("")
    new = nl.join(out)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(new)
    emit(f"[{t}] {os.path.relpath(path, ROOT)}：行宽 → {width} 列（改 {grew} 行；注释行{'已' if inserted else '未'}插入）")

emit()
emit(f"备份目录：{os.path.relpath(BACKUP, ROOT)}")
open(os.path.join(HERE, "_out_widen_seed.txt"), "w", encoding="utf-8").write("\n".join(log) + "\n")
