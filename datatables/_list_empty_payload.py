# -*- coding: utf-8 -*-
"""列出「声明 DOWNLOAD 但 manifest 里没有/空 raw_csv」的表 -> datatables/_out_empty_payload.txt"""
import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
rows = json.load(open(os.path.join(HERE, "_out_sweep_width_db.json"), encoding="utf-8"))
print(f"{'表':28s} {'disp':10s} {'raw_rows':>8s} {'raw_fields':>10s} {'db':>4s} {'local?':>6s} csv_path")
for r in sorted(rows, key=lambda x: x["table"]):
    if r["raw_fields"] in (None, 0):
        print(f"{r['table']:28s} {str(r['disposition']):10s} {str(r['raw_rows']):>8s} {str(r['raw_fields']):>10s} "
              f"{str(r['db_cols']):>4s} {'Y' if '本地' in str(r['csv_path']) else '':>6s} {r['csv_path']}")
