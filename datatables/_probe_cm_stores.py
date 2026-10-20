# -*- coding: utf-8 -*-
"""看 CHARA_MODEL 仿真里 offset>=0x160 的写点/助手调用顺序（临时探针）"""
import io, json, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(HERE, "_out_emu_readers.json"), encoding="utf-8"))["sub_571380"]
print("stores with off>=0x160:")
for s in d["stores"]:
    if s["off"] is not None and 0x160 <= s["off"] <= 0x1B0:
        print("   ", s)
print("\ncall seq (n) around the tail:")
print([c["n"] for c in d["calls"]])
print("\nretry/abi:", d["abi"], d.get("retry"))
for m in d["modes"]:
    print("mode", m["mode"], "err", m["err"], "obs", len(m["observed"]))
