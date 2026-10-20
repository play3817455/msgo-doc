# -*- coding: utf-8 -*-
"""gen_msma_truth.py —— 生成「机体族」三张表的真值（只填有依据的列）。

产出（就地覆盖 server/datafiles/lounge/...，先备份 .bak_truth）：
  msma/msma_model.csv        ← ★col0 = モデルID（客户端 sub_571BF0 用它拼 chara/ 路径）
  msma/msma_settings.csv     ← col0 = 練度ID；col1 = モデルID；col5 = 日文名
  msma/msma_rental.csv       ← 与 settings 同构（同读取器 sub_582390）⇒ 同口径

依据（每条都可追溯）：
  A. names/练度ID-モデルID-全集.csv  ← 351 条，モデルID 全部通过 chara目录-ID清单(1646) 校验
  B. GundamOnline/unpackdat/settings/favms_ok_list.csv ← 700 行名册（練度ID + 日文名），去重后 696
  C. reverse-login-chain/detail/M01 §7.6 / P219：msma_model 的 col0 **必须是モデルID**（不是練度ID）
  D. P219/P221：msma_settings 的 col1 = モデルID（sub_A86810 从记录 +32/+36 取它拼资源路径）

★ 不填的列（诚实标注）：
  - msma_model 的 col1..67：**无来源**（chara/ 全是模型/贴图/动画资源；codex 数值属"参数"，不在本表）
  - msma_settings 的数值列（col4/col6/col7/col8/col9..；含疑为"地形适性"的 col9/10/11）：
    列↔语义**只解出形式**（见 05-76表填写规格总表 §三），**与 codex 字段的对应尚未双证** ⇒ 不填
  - 越界列读作 0/空串，不报错不崩 ⇒ 只写到真正要设的列即可

用法：
  python datatables/gen_msma_truth.py            # 生成（含备份 + 自检）
  python datatables/gen_msma_truth.py --check    # 只自检现有文件
"""
import io
import os
import shutil
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
NAMES = os.path.join(HERE, "names")
GAME = os.path.join(ROOT, "机动战士敢达Online", "GundamOnline")
FAVMS = os.path.join(GAME, "unpackdat", "settings", "favms_ok_list.csv")
SHIP = os.path.join(ROOT, "server", "datafiles", "lounge", "msma")

# ★★2026-09-18（P235）：`msma_model.csv` 的真结构（`sub_571380` 反编译逐列实证 ✓，见 M01 §3）：
#	col0  → a4+0      **u64 = 行键 = 練度ID**（★不是モデルID ✗）
#	col71 → a4+0x1B4  **モデルID 低 32**
#	col72 → a4+0x1B8  **モデルID 高 32**
#   ⇒ 本表必须写到 **col72**（73 列）✓
#	✗ 旧版按"col0 = モデルID"生成 ⇒ 客户端拿練度ID（1124102）**查不到行** ⇒
#	  机体对象建不出来 ⇒ 「我的机体」**一台都不显示**（2026-09-18 实测 ✓）
MODEL_COLS = 73       # ★写到 col72（含）⇒ 73 列；col73..76 越界读作空，无害 ✓
MODEL_MID_LO = 71     # モデルID 低 32 → a4+0x1B4
MODEL_MID_HI = 72     # モデルID 高 32 → a4+0x1B8
SET_COLS = 6          # 写到 col5
NAME_COL = 5


def rows(path):
    L = io.open(path, encoding="utf-8", errors="replace").read().splitlines()
    return [x for x in L if x.strip() and not x.lstrip().startswith("#")]


def cell(line, i):
    p = line.split(",")
    return p[i].strip() if i < len(p) else ""


def load_map():
    """練度ID → モデルID（来自 build_model_id_map.py 的产物）。"""
    p = os.path.join(NAMES, "练度ID-モデルID-全集.csv")
    m = {}
    for l in rows(p):
        ms, mid = cell(l, 0), cell(l, 1)
        if ms.isdigit() and mid.isdigit():
            m[ms] = mid
    return m


def load_roster():
    """練度ID → 日文名（favms_ok_list.csv，兜底 2 处缺逗号 + 去重 4 处重复 ⇒ 696）。"""
    out, seen = [], set()
    for line in io.open(FAVMS, encoding="utf-8", errors="replace").read().splitlines():
        line = line.lstrip("\ufeff")
        if not line.strip() or line.lstrip()[0] == "#":
            continue
        parts = line.split(",")
        if len(parts) >= 2 and parts[0].strip().isdigit():
            pair = (parts[0].strip(), parts[1].strip())
        else:
            head = ""
            for ch in line:
                if ch.isdigit():
                    head += ch
                else:
                    break
            if not head or head == line:
                continue
            pair = (head, line[len(head):].lstrip(".．・ "))
        if pair[0] in seen:
            continue
        seen.add(pair[0])
        out.append(pair)
    return out


def check(text, tag):
    b = text.encode("utf-8")
    ok = True
    if b.startswith(b"\xef\xbb\xbf"):
        print("!![%s] 带 BOM" % tag); ok = False
    if b.count(b"\n") != b.count(b"\r\n"):
        print("!![%s] 存在非 CRLF 换行" % tag); ok = False
    body = [x for x in text.split("\r\n") if x and not x.startswith("#")]
    if body and [x for x in body if not x.endswith(",")]:
        print("!![%s] 数据行缺尾逗号" % tag); ok = False
    if not body:
        print("!![%s] 无数据行" % tag); ok = False
    print("[%s] 自检 %s  数据行=%d" % (tag, "✓" if ok else "✗", len(body)))
    return ok


def write_and_backup(rel, text, tag):
    out = os.path.join(SHIP, rel)
    if os.path.exists(out):
        bak = out + ".bak_truth"
        if not os.path.exists(bak):
            shutil.copy(out, bak)
            print("  备份 → %s" % os.path.basename(bak))
    io.open(out, "w", encoding="utf-8", newline="").write(text)
    print("  写入 %s" % out)


def main():
    print("!! gen_msma_truth.py 已停用（2026-09-28）")
    print("   本脚本只填 col0/col1/col5，会把 gen_msma_machine.py 写好的数值列**清空** ⇒ 不再允许直接跑。")
    print("   ★现行生成器：python datatables/gen_msma_machine.py")
    print("   （确需重跑旧口径：设环境变量 MSMA_ALLOW_LEGACY=1）")
    if os.environ.get("MSMA_ALLOW_LEGACY") != "1":
        return 2
    m = load_map()
    roster = load_roster()
    check_only = "--check" in sys.argv
    print("映射 %d 条 ｜ 名册 %d 台 ｜ 可填模型的机体 = %d"
          % (len(m), len(roster), sum(1 for ms, _n in roster if ms in m)))

    # ---------- 1) msma_model.csv（col0 = 練度ID；col71/col72 = モデルID 低/高）----------
    n_model = sum(1 for ms, _n in roster if ms in m)
    head = [
        "#ID,",
        "# ===== msma/msma_model.csv （CHARA_MODEL / 表ID 5 / 下载序 5 / CCharaTable / 读取函数 sub_571380）=====",
        "# ★★★ 行键 col0 = **練度ID（7 位）**；モデルID 在 **col71(低32) + col72(高32)**",
        "#   `sub_571380` 反编译逐列实证（M01 §3 ✓）：`*(_QWORD*)a4 = sub_BBB3F0(a1,0)` ⇒ col0→a4+0 是 **u64 行键**；",
        "#   `col71 → a4+0x1B4`、`col72 → a4+0x1B8` ✓",
        "# ✗ 旧版写成「col0 = モデルID」⇒ 客户端按練度ID(1124102) 查不到行 ⇒ 机体对象建不出来",
        "#   ⇒ 「我的机体」**一台都不显示**（2026-09-18 实测 ✓ P235）",
        "# 数据来源：datatables/names/练度ID-モデルID-全集.csv（351 条，モデルID 全部通过 chara目录-ID清单(1646) 校验）",
        "# 规则：モデルID = A(1)*1e8 + B(2)*1e6 + C(4)*100 + NN(2)；资源 = chara/01/<B>/<C>/（A 决定前缀 MSZ_/MAZ_/BSZ_/…）",
        "# 当前 = **只下发能确证模型的机体**（共 " + str(n_model) + " 行）⇒ 其余机体不出现（但**不影响已有机体显示** ✓）",
        "# ⚠️ col1..col70 一律留空：无来源（chara/ 只含模型/贴图/动画，不含机体参数）",
        "# 生成：python datatables/gen_msma_truth.py",
    ]
    lines = list(head)
    for ms, _name in roster:
        mid = m.get(ms)
        if not mid:
            continue
        v = int(mid)
        f = [""] * MODEL_COLS
        f[0] = ms                                     # ★行键 = 練度ID
        f[MODEL_MID_LO] = str(v & 0xFFFFFFFF)         # モデルID 低 32
        f[MODEL_MID_HI] = str((v >> 32) & 0xFFFFFFFF) # モデルID 高 32（9 位十进制 ⇒ 恒 0 ✓）
        lines.append(",".join(f) + ",")
    text = "\r\n".join(lines) + "\r\n"
    if not check_only:
        print("\n[1] msma_model.csv")
        write_and_backup("msma_model.csv", text, "model")
    check(text, "model")

    # ---------- 2) msma_settings.csv ----------
    head = [
        "#模型ID（=練度ID）,,,,,名称,",
        "# ===== msma/msma_settings.csv （CHARA_PARAM / 表ID 4 / 下载序 4 / CCharaParamTable / 读取函数 sub_582390）=====",
        "# 本表 = ★机体参数主表★。行键 col0 = 練度ID（7 位）；col1 = モデルID（9 位，客户端 sub_A86810 用它拼 chara/ 路径）",
        "# 已填（全部有依据）：",
        "#   col0 ← 練度ID（favms_ok_list.csv，696 个唯一 ID）",
        "#   col1 ← モデルID（names/练度ID-モデルID-全集.csv，351 台，全部通过权威校验）",
        "#   col5 ← 機体名（favms_ok_list.csv 日文原名）",
        "# ⚠️ 其余 61 列留空：列↔语义只解出形式（内存偏移见 05-76表填写规格总表 §三），与 codex 字段的对应尚未双证 ⇒ 不猜",
        "# 生成：python datatables/gen_msma_truth.py",
    ]
    lines = list(head)
    filled = 0
    for ms, name in roster:
        f = [""] * SET_COLS
        f[0] = ms
        f[1] = m.get(ms, "")
        f[NAME_COL] = name.replace(",", "・")
        if f[1]:
            filled += 1
        lines.append(",".join(f) + ",")
    text = "\r\n".join(lines) + "\r\n"
    if not check_only:
        print("\n[2] msma_settings.csv（col1 填到 %d 台）" % filled)
        write_and_backup("msma_settings.csv", text, "settings")
    check(text, "settings")

    # ---------- 3) msma_rental.csv（与 settings 同构）----------
    lines = [l.replace("msma_settings.csv", "msma_rental.csv") for l in head]
    for ms, name in roster:
        if ms not in m:
            continue
        f = [""] * SET_COLS
        f[0] = ms
        f[1] = m[ms]
        f[NAME_COL] = name.replace(",", "・")
        lines.append(",".join(f) + ",")
    text = "\r\n".join(lines) + "\r\n"
    if not check_only:
        print("\n[3] msma_rental.csv")
        write_and_backup("msma_rental.csv", text, "rental")
    check(text, "rental")
    return 0


if __name__ == "__main__":
    sys.exit(main())
