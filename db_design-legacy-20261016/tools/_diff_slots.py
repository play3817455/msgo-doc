"""对照重抽前后的静态槽表，只报告「新增 / 丢失」的槽。

用途：改抽取器后必须能一眼看出「补了哪些」和「有没有把原来对的抽丢」。
丢失是回归信号，除非能解释清楚（例如误报被正确剔除）。
"""
import json
import pathlib

META = pathlib.Path(__file__).resolve().parents[1] / "schema" / "_meta"
BEFORE = META / "_slots_before_20260924"

new_all, old_all = {}, {}
for p in sorted(META.glob("ida_memory_slots_batch*.json")):
    new_all.update(json.loads(p.read_text(encoding="utf-8")))
for p in sorted(BEFORE.glob("ida_memory_slots_batch*.json")):
    old_all.update(json.loads(p.read_text(encoding="utf-8")))


def slots_of(entry):
    """用展开后的 slots（审计的视角）；缺失时退回 segments 的起点。"""
    if entry.get("slots"):
        return set(int(x) for x in entry["slots"])
    return {int(seg["offset"]) for seg in entry.get("segments", [])}


total_added = total_lost = 0
for name in sorted(set(old_all) | set(new_all)):
    o, n = slots_of(old_all.get(name, {})), slots_of(new_all.get(name, {}))
    added, lost = sorted(n - o), sorted(o - n)
    if not added and not lost:
        continue
    total_added += len(added)
    total_lost += len(lost)
    fn = new_all.get(name, old_all.get(name, {})).get("function", "?")
    print(f"{name:22s} {fn:14s} +{added}  -{lost}")

print(f"\n合计 新增槽 {total_added} 个 / 丢失槽 {total_lost} 个")

# 丢失槽 = 回归信号，单独列出来方便逐条核
print("\n--- 丢失槽明细（需逐条确认是误报剔除还是回归）---")
for name in sorted(set(old_all) & set(new_all)):
    o, n = slots_of(old_all[name]), slots_of(new_all[name])
    lost = sorted(o - n)
    if lost:
        print(f"{name:22s} -{lost}")
