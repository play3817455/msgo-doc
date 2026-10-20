# -*- coding: utf-8 -*-
"""一次性取证：524 个域外键在 sidecar 里是「整行缺席」还是「行在但 col12 空」。"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import psycopg  # noqa: E402
import weapon_client_raw as RAW  # noqa: E402
import fix_rapid_delay_units as F  # noqa: E402

# 注意：`fix_rapid_delay_units` 导入时已把 sys.stdout 重包成 utf-8；
# 这里**不要**再包一层（会把底层 buffer 被 GC 关掉）。

src = F.sidecar_rapid()
rows = F.read_db()
by_key = {}
for k, attr, val, rid in rows:
    by_key.setdefault(F.norm_key(k), []).append((attr, val, rid))
out_keys = [k for k, rs in by_key.items()
            if k not in src and not all(RAW.rapid_is_raw_domain(v) for a, v, _ in rs if a == "RAPIDDELAY")]

raw_side = F.rd(F.SIDE)
head = raw_side[0] if raw_side else []
side_keys = {}
for r in raw_side[1:]:
    if len(r) > 1 and r[1].strip():
        side_keys[F.norm_key(r[1])] = r

absent = [k for k in out_keys if k not in side_keys]
present_empty_col12 = [k for k in out_keys if k in side_keys and not (len(side_keys[k]) > 12 and side_keys[k][12].strip())]
present_col12_real = [k for k in out_keys if k in side_keys and len(side_keys[k]) > 12 and side_keys[k][12].strip()]

print("域外键 %d：sidecar 整行缺席 %d / 行在但 col12 空 %d / 行在且 col12 有值 %d"
      % (len(out_keys), len(absent), len(present_empty_col12), len(present_col12_real)))
print()
print("sidecar 表头 col10..col17: %s" % (head[10:18] if len(head) > 17 else head))
print()
print("—— 缺席样例（键, 库值）——")
for k in absent[:8]:
    v = [v for a, v, _ in by_key[k] if a == "RAPIDDELAY"]
    print("   %s  RAPIDDELAY=%s" % (k, v))
print("—— 行在但 col12 空 样例（整行）——")
for k in present_empty_col12[:5]:
    r = side_keys[k]
    print("   %s  col3=%r col10..col17=%s" % (k, r[2] if len(r) > 2 else "", r[10:18]))
print("—— 行在且 col12 有值（= 疑似键形不一致，必须查）——")
for k in present_col12_real[:20]:
    print("   %s  col12=%r  库=%s" % (k, side_keys[k][12], [v for a, v, _ in by_key[k] if a == "RAPIDDELAY"]))
