# -*- coding: utf-8 -*-
"""MSMA_MODULE 666 键的溯源假设检验。只读。"""
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")


def col0(rel):
    with open(os.path.join(ROOT, rel.replace("/", os.sep)), "rb") as f:
        raw = f.read()
    if raw.startswith(b"\xef\xbb\xbf"):
        raw = raw[3:]
    s = set()
    for ln in raw.decode("utf-8", "replace").replace("\r\n", "\n").split("\n"):
        if not ln.strip() or ln.lstrip().startswith("#"):
            continue
        s.add(ln.split(",", 1)[0].strip())
    return s


mm = col0("server/datafiles/lounge/msma/msma_module.csv")
cp = col0("server/datafiles/lounge/msma/msma_settings.csv")
body = col0("datatables/names/机体总表.csv")          # 700
roster = col0("gow_wiki/favms_ok_list.csv")            # 696 (comment-stripped)
bridge = col0("datatables/names/练度ID-モデルID-全集.csv")  # 593

print("mm", len(mm), "cp", len(cp), "总表", len(body), "roster", len(roster), "bridge", len(bridge))
print("mm ⊆ 总表 :", mm <= body)
print("mm ⊆ cp   :", mm <= cp)
print("mm == 总表∩roster :", mm == (body & roster))
print("mm == 总表∩mm? n/a")
print("总表 - roster    :", sorted(body - roster))
print("mm - roster      :", sorted(mm - roster))
print("roster - mm      :", len(roster - mm))
print("mm ∩ bridge      :", len(mm & bridge))
print("mm == 总表∩(roster∪bridge):", mm == (body & (roster | bridge)))
miss = cp - mm
print()
print("cp-mm 中在 roster 里的 :", len(miss & roster))
print("cp-mm 中在 bridge 里的 :", len(miss & bridge))
print("cp-mm 中既不在 roster 也不在 bridge:", sorted(miss - roster - bridge))
print()
print("body - mm (总表有、mm 无) n=%d :" % len(body - mm), sorted(body - mm))
