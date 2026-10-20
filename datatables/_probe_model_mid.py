# -*- coding: utf-8 -*-
"""CHARA_MODEL col0(モデルID) vs CHARA_PARAM col1(モデルID) 对账。只读。"""
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SEED = os.path.join(ROOT, "server", "datafiles", "lounge", "msma")


def rows(name):
    with open(os.path.join(SEED, name), "rb") as f:
        raw = f.read()
    if raw.startswith(b"\xef\xbb\xbf"):
        raw = raw[3:]
    return [l.rstrip() for l in raw.decode("utf-8", "replace").replace("\r\n", "\n").split("\n")
            if l.strip() and not l.lstrip().startswith("#")]


cp = rows("msma_settings.csv")
mod = rows("msma_model.csv")
cp_lid = [r.split(",")[0].strip() for r in cp]
cp_mid = [r.split(",")[1].strip() if len(r.split(",")) > 1 else "" for r in cp]
mod_key = [r.split(",")[0].strip() for r in mod]

cp_mid_set = {m for m in cp_mid if m}
print("CHARA_PARAM 行 %d ／ col1(モデルID) 非空 %d ／ 唯一 %d" % (len(cp), len(cp_mid_set), len(cp_mid_set)))
print("CHARA_MODEL 行 %d ／ 唯一键 %d ／ 位数分布 %s"
      % (len(mod), len(set(mod_key)),
         sorted({len(k) for k in set(mod_key)})))
print()
mk = set(mod_key)
print("CHARA_MODEL ⊂ CHARA_PARAM col1 ?", mk <= cp_mid_set)
print("CHARA_MODEL - col1 : %d %s" % (len(mk - cp_mid_set), sorted(mk - cp_mid_set)[:10]))
print("col1 - CHARA_MODEL : %d" % len(cp_mid_set - mk))
print()
print("CHARA_MODEL 键位数分布:", {n: sum(1 for k in mk if len(k) == n) for n in {len(k) for k in mk}})
