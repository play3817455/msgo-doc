# -*- coding: utf-8 -*-
import sys, io, os
sys.path.insert(0, r"datatables")
out = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
import purge_unreachable_weapon_keys as P
ok = P.legit_ids()
print("可达域 %d" % len(ok), file=out)
for k in ["2840151", "02840151", "1010401", "01010401", "2711603", "02711603",
          "3010101", "03010101", "4840201", "04840201", "12160101", "10101"]:
    print("  is_legit(%-10s) = %-6s  (lstrip0=%-9s in ok: %s)"
          % (k, P.is_legit(k, ok), k.lstrip("0"), k.lstrip("0") in ok), file=out)
out.flush()
