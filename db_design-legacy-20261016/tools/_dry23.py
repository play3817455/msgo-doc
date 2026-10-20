"""只读诊断：批次 23 的 15 条 IMPORTED 命令，逐条报「六项 check 哪一项取不到证据」+ 差异。"""
import io
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
TOOLS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(TOOLS)
sys.path.insert(0, TOOLS)
import verify_commands_ida as V  # noqa: E402

VERIFY = os.path.join(ROOT, "schema", "commands", "_verify")
CMD_DIR = os.path.join(ROOT, "schema", "commands")

batch = json.load(io.open(os.path.join(CMD_DIR, "_meta", "batch_23.json"), encoding="utf-8"))
tally = {}
for t in batch["targets"]:
    cid = t["id"]
    raw = os.path.join(VERIFY, "_raw", cid + ".json")
    cmd = json.load(io.open(os.path.join(CMD_DIR, cid + ".json"), encoding="utf-8"))
    sl = V.Slice(json.load(io.open(raw, encoding="utf-8")))
    res = V.analyze(sl, cmd)
    ch = res["checks"]
    none_keys = [k for k in V.SIX_CHECKS if ch.get(k) is None]
    ms = res["mismatches"]
    for k in none_keys:
        tally[k] = tally.get(k, 0) + 1
    print("=" * 100)
    print("%s  status=%s  none=%s  mismatches=%d" % (cid, res["status"], none_keys, len(ms)))
    for k in none_keys:
        if k == "capacity":
            print("   [capacity]      未命中分配器指纹；模型 capacity=%s" % cmd.get("capacity"))
        elif k == "closer":
            print("   [closer]        窗口内未找到闭合点；模型 closer_va=%s" % cmd.get("closer_va"))
        elif k == "dispatch_slot":
            print("   [dispatch_slot] 未找到去向虚表调用；模型 dispatch_slot=%s dispatch_va=%s"
                  % (cmd.get("dispatch_slot"), cmd.get("dispatch_va")))
        elif k == "field_window":
            print("   [field_window]  %s" % ch.get("field_window"))
        elif k == "primitive_widths":
            pw = ch.get("primitive_widths") or {}
            print("   [primitive_widths] zero_load=%s" % pw.get("zero_load"))
        elif k == "log_strings":
            print("   [log_strings]   无日志串")
    for m in ms:
        print("   MISMATCH %-18s model=%s asm=%s %s"
              % (m.get("check"), str(m.get("model"))[:40], str(m.get("asm"))[:40],
                 (m.get("note") or "")[:80]))
    for n in res.get("notes") or []:
        print("   note[%s] %s" % (n.get("check"), (n.get("note") or "")[:110]))
print()
print("六项缺项统计:", tally)
