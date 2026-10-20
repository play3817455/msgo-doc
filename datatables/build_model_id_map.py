# -*- coding: utf-8 -*-
"""build_model_id_map.py —— 合并所有「練度ID → モデルID」来源，产出全集并用权威清单校验。

来源（datatables/names/）：
  模型号映射-初版.csv   列：練度ID, 机体名, 打包值(第69列), 目录, 内部代号, 匹配方式, 相似度
  模型号映射-自动.csv   列：練度ID, モデルID, 机体名, 代号, 分数, 来源
  模型号映射-补充.csv   列：練度ID, モデルID, 机体名, 代号, 资源目录, 来源
  模型号映射-合并.csv   列：練度ID, モデルID, 机体名, 来源
  模型号映射-人工.csv   列：練度ID, 日文名, 模型打包值, 资源目录, 内部代号, 中文名, 来源
  机体总表.csv         列33 = 模型打包值, 列35 = 模型来源

校验：chara目录-ID清单.csv（1646 个权威 モデルID）
产出：names/练度ID-モデルID-全集.csv（附来源 + 是否通过权威校验）
用法：python datatables/build_model_id_map.py [--check]
"""
import io
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
NAMES = os.path.join(HERE, "names")
OUT = os.path.join(NAMES, "练度ID-モデルID-全集.csv")


def rows(path):
    L = io.open(path, encoding="utf-8", errors="replace").read().splitlines()
    return [x for x in L if x.strip() and not x.lstrip().startswith("#")]


def cell(line, i):
    p = line.split(",")
    return p[i].strip() if i < len(p) else ""


def load_authoritative():
    """权威 モデルID 集合（chara目录-ID清单.csv 第 0 列）。"""
    p = os.path.join(NAMES, "chara目录-ID清单.csv")
    return set(cell(l, 0) for l in rows(p) if cell(l, 0).isdigit())


def harvest():
    """返回 {練度ID: (モデルID, 来源, 优先级)}；优先级大者胜。"""
    out = {}

    def put(ms, mid, src, pri):
        ms, mid = ms.strip(), mid.strip()
        if not (ms.isdigit() and mid.isdigit() and len(mid) == 9):
            return
        if ms not in out or out[ms][2] <= pri:
            out[ms] = (mid, src, pri)

    specs = [
        ("模型号映射-人工.csv", 0, 2, "人工", 50),
        ("模型号映射-合并.csv", 0, 1, "合并", 45),
        ("模型号映射-补充.csv", 0, 1, "补充", 40),
        ("模型号映射-自动.csv", 0, 1, "自动", 30),
        ("模型号映射-初版.csv", 0, 2, "初版", 20),
        # ★页面（ms_match.html 手工对照）优先级最高：它是人工逐台看图定下来的，
        #   生成器 = datatables/apply_ms_pairs.py（全量重写，本文件不手工改）
        ("模型号映射-页面.csv", 0, 1, "页面", 55),
    ]
    for fn, i_ms, i_mid, tag, pri in specs:
        p = os.path.join(NAMES, fn)
        if not os.path.exists(p):
            continue
        n = 0
        for l in rows(p):
            before = len(out)
            put(cell(l, i_ms), cell(l, i_mid), tag, pri)
            if len(out) > before:
                n += 1
        print("  %-22s 新增 %4d" % (fn, n))

    p = os.path.join(NAMES, "机体总表.csv")
    if os.path.exists(p):
        n = 0
        for l in rows(p):
            before = len(out)
            put(cell(l, 0), cell(l, 33), "机体总表", 35)
            if len(out) > before:
                n += 1
        print("  %-22s 新增 %4d" % ("机体总表.csv", n))
    return out


def main():
    auth = load_authoritative()
    print("权威 モデルID 数（chara目录-ID清单）= %d" % len(auth))
    print("合并各来源：")
    m = harvest()
    good = sum(1 for v in m.values() if v[0] in auth)
    bad = len(m) - good
    print()
    print("★合并结果：練度ID→モデルID 共 %d 条" % len(m))
    print("  其中モデルID 通过权威校验 = %d" % good)
    print("  未通过权威校验（资源树里找不到该目录）= %d" % bad)
    from collections import Counter
    print("  来源分布 = %s" % dict(Counter(v[1] for v in m.values())))

    lines = ["#練度ID,モデルID,来源,权威校验,"]
    for ms in sorted(m, key=lambda x: (len(x), x)):
        mid, src, _pri = m[ms]
        lines.append("%s,%s,%s,%s," % (ms, mid, src, "OK" if mid in auth else "NOT_IN_TREE"))
    text = "\r\n".join(lines) + "\r\n"
    if "--check" in sys.argv:
        print("(--check: 不写文件)")
        return 0
    io.open(OUT, "w", encoding="utf-8", newline="").write(text)
    print("已写 %s（%d 行数据）" % (OUT, len(lines) - 1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
