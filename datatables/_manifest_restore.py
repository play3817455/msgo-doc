# -*- coding: utf-8 -*-
"""cfgsync 会把**未提供 bootstrap CSV 的表**的表头换成兜底表头 —— 按快照精确复原。

规则：
  * 目标表（TARGET）：数据行是新的（正确），表头改用**种子文件**的注释块（含新增的 reader 映射行）；
  * 其余被兜底表头覆盖的表：整行按快照逐字节复原（它们的数据行没变，只有表头被换掉）；
  * 未变化的表：不动。
  （2026-10-05：本次只重建 QUEST，故 TARGET 缩为 ["QUEST"]。）

不重跑 cfgsync -bootstrap-csv 的原因：那会对 6 张当前为空的表触发 importCSVFile，
凭空灌进 64 行占位行（空表是有意的），副作用不可控。
"""
import hashlib
import io
import json
import os
import pickle
import sys

import psycopg

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SCHEMA = os.path.join(ROOT, "db_design", "schema", "cfg", "tables")
SEED_ROOT = os.path.join(ROOT, "server", "datafiles", "lounge")
DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")
TARGET = ["QUEST"]  # 本次重建/补列宽的表（表头用种子注释块，数据行用 cfgsync 新产物）

old = pickle.load(open(os.path.join(HERE, "_out_manifest_snapshot.pkl"), "rb"))


def extract_csv_header(raw: bytes) -> bytes:
    """复刻 cfg.ExtractCSVHeader：取开头的 # 注释行（跳过空行），CRLF 连接。"""
    lines = []
    for line in raw.decode("utf-8", "replace").split("\n"):
        line = line.rstrip("\r")
        s = line.strip()
        if s.startswith("#"):
            lines.append(line)
            continue
        if s == "":
            continue
        break
    return "\r\n".join(lines).encode("utf-8")


def data_block(raw: bytes) -> bytes:
    """返回 raw 中第一条非注释、非空行起的全部字节（含行尾）。按字节扫描，不解析字段。"""
    pos = 0
    while pos < len(raw):
        end = raw.find(b"\r\n", pos)
        if end < 0:
            return b""
        s = raw[pos:end].strip()
        if s and not s.startswith(b"#"):
            return raw[pos:]
        pos = end + 2
    return b""


log = []


def emit(s=""):
    print(s)
    log.append(s)


with psycopg.connect(DSN) as c, c.cursor() as cur:
    cur.execute("SELECT file, raw_csv, header_text FROM meta.cfg_manifest")
    now = {r[0]: (r[1], r[2]) for r in cur.fetchall()}

    restored, relabeled = [], []
    for f, (raw, htxt) in sorted(now.items()):
        if f not in old:
            continue
        o_raw, o_sha, o_rc, o_htxt = old[f][3], old[f][1], old[f][2], old[f][4]
        if f in TARGET:
            spec = json.load(open(os.path.join(SCHEMA, f + ".json"), encoding="utf-8"))
            seed = os.path.join(SEED_ROOT, *spec["csv_path"].split("/"))
            head = extract_csv_header(open(seed, "rb").read())
            new_raw = head + b"\r\n" + data_block(raw or b"")
            sha = hashlib.sha256(new_raw).hexdigest()
            cur.execute(
                "UPDATE meta.cfg_manifest SET raw_csv=%s, header_text=%s, sha256=%s WHERE file=%s",
                (new_raw, head.decode("utf-8"), sha, f))
            relabeled.append((f, len(raw or b""), len(new_raw), len(head.split(b"\r\n"))))
            continue
        if (raw or b"") == (o_raw or b"") and (htxt or "") == (o_htxt or ""):
            continue
        cur.execute(
            "UPDATE meta.cfg_manifest SET raw_csv=%s, header_text=%s, sha256=%s, row_count=%s WHERE file=%s",
            (o_raw, o_htxt, o_sha, o_rc, f))
        restored.append(f)

emit(f"目标 5 表表头改用种子注释块：")
for f, b0, b1, hl in relabeled:
    emit(f"   {f:20s} raw {b0}B → {b1}B，表头 {hl} 行")
emit(f"其余按快照逐字节复原：{len(restored)} 张")
emit("   " + ", ".join(restored))
open(os.path.join(HERE, "_out_manifest_restore.txt"), "w", encoding="utf-8").write("\n".join(log) + "\n")
