# -*- coding: utf-8 -*-
"""按模型的 asm_verification.batch 重建 _meta/batch_1.json 与「批次-1-清单.md」。

背景：batch_1.json 是 `verify_commands_ida.py plan` 的产物（工作清单），同日被两次
重新 plan 覆盖（先被改写成「下一批 50 条」，又被 `--redo` 列表覆盖），原始清单已不可
原样恢复。**成员事实仍在模型里**（`asm_verification.batch == 1`）与切片目录
（`_verify/_raw/`、`_verify/`）里，故按模型重建，并注明是重建件。
"""
import json
from pathlib import Path

META = Path("db_design/schema/commands/_meta")
CMD = Path("db_design/schema/commands")

rows = []
for p in sorted(CMD.glob("*.json")):
    d = json.loads(p.read_text(encoding="utf-8"))
    av = d.get("asm_verification") or {}
    if av.get("batch") == 1 and "fields" in d:
        rows.append({
            "id": d["id"],
            "opcode": d["opcode"],
            "status": av.get("status"),
            "verified_at": av.get("verified_at"),
            "extractor": av.get("extractor"),
        })

note = ("原始 plan 清单被同日两次重新 plan 覆盖，无法原样恢复；本文件按各模型的 "
        "asm_verification.batch == 1 重建。原始 emit 的切片仍在 schema/commands/_verify/_raw/ "
        "与 _verify/ 下，逐个命令可复算。批次 1 的 ingest/apply 结论已在模型里。")

out = {
    "batch": 1,
    "created": "2026-09-22",
    "restored_from_models": "2026-09-22",
    "size": len(rows),
    "criteria": {"proto": None, "direction": None, "only": None, "min_score": None},
    "note": note,
    "targets": [{"id": r["id"], "opcode": r["opcode"], "status": r["status"]} for r in rows],
}
(META / "batch_1.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

lines = ["# 批次 1 复核清单（按模型重建）", "",
         "> 原始 `plan` 清单被同日两次重新 plan 覆盖，无法原样恢复；成员按各模型的 "
         "`asm_verification.batch == 1` 重建。切片见 `schema/commands/_verify/_raw/`。",
         "", "共 **%d** 条。" % len(rows), "",
         "| # | 命令 | opcode | 状态 | 复核日期 |", "|---|---|---|---|---|"]
for i, r in enumerate(rows, 1):
    lines.append("| %d | <code>%s</code> | %s | %s | %s |"
                 % (i, r["id"], r["opcode"], r["status"], r["verified_at"] or "—"))
(META / "批次-1-清单.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print("重建 batch_1.json / 批次-1-清单.md：%d 条" % len(rows))
