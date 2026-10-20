# -*- coding: utf-8 -*-
"""weapon_client_raw.py —— 武器面板值 → **客户端原值** 的唯一换算表。

为什么要这份表（根因，2026-10-04）
================================
`#36 WEAPON_BATTLE_DETAIL` / `#37 WEAPON_SETTING` 里存的**不是** wiki/机库显示的数字，
而是**客户端运行时对象里的原值**。机库白字由原值乘出来，`sub_59A070` 把表里的值
**原样**写进武器对象（`+1936 = POWER`，PNG 见 `datatables/01-列注释/36-36-WEAPON_BATTLE_DETAIL.md` §3）。

服务端读侧已经按「原值」写死了（`serverv/internal/store/battle_params.go`）：

    // panelPowerFromClientRaw: 原值 80 在客户端显示 800，伤害层仍按 800 做 ceiling(威力/10)
    v := int64(raw) * 10

⇒ 表里必须存**原值**；存成面板值会让 `DamageFor` 再乘 10 ⇒ 每把武器伤害 ×10
（`TestSimDBWeaponArsenalTTK` 的"一发秒杀一切"哨就是为这类口径腐蚀立的）。

换算出处（全部来自 IDA 实测，不是拟合）
====================================
| 属性 | 机库白字公式 | 表里存什么 |
|---|---|---|
| 威力 | `trunc(原值×10 + 0.4)` | 原值 = 面板/10 |
| 集弹性能 | `trunc((500 − 原值)×_STAB_K + 0.4)` | `原值/100`（见 `_STAB_K`） |
| 连射速度 | `trunc((2 − 原值)×_RAPID_K + 0.4)` | 原值 |
| 装填性能 | `trunc((10 − 原值)×100 + 0.4)` | 原值 |
| 锁定 | `trunc(原值×0.01×1000 + 0.4)` | 原值 |
| 射程距离 / 红锁距离 | —（不走这套） | **原样**（世界单位，读侧直接与 `hit_distance` 比） |

⚠️ 面板→原值的反解**不总是存在**：白字步长是 10，wiki 偶尔给 5 的倍数（如 65、89）。
那些是**同表其它列串进来的值**（列错位），不是真威力；调用方应先按 wiki 表头逐列取值
（见 `gen_weapon_set_wiki.py`），再进这张表。本模块对无解的值取**最近可表示**的原值。

⚠️ 回复/补给系 6 个类别（12/43/38/24/36/53）在**消费端**取负，**表里写正值** ——
换算与符号正交，本模块只管换算。
"""
import re
import struct

# ── IDA 实测常量（原样搬，改动会让真库口径漂移）────────────────────────────
_F_500 = struct.unpack("<f", bytes.fromhex("0000FA43"))[0]
_F_0002 = struct.unpack("<f", bytes.fromhex("6F12033B"))[0]
_F_1000 = struct.unpack("<f", bytes.fromhex("00007A44"))[0]
_F_2 = struct.unpack("<f", bytes.fromhex("00000040"))[0]
_F_0526 = struct.unpack("<f", bytes.fromhex("A2BC063F"))[0]
_F_1500 = struct.unpack("<f", bytes.fromhex("0080BB44"))[0]
_F_10 = struct.unpack("<f", bytes.fromhex("00002041"))[0]
_F_001 = struct.unpack("<f", bytes.fromhex("0AD7233C"))[0]
_F_04 = struct.unpack("<f", bytes.fromhex("CDCCCC3E"))[0]
_STAB_K = _F_0002 * _F_1000
_RAPID_K = _F_0526 * _F_1500

# 面板数字（可能带括号强化档 `800(880)` / 多段 `28/168`）⇒ 取第一档整数。
_TIER = re.compile(r"^\s*(-?\d+(?:\.\d+)?)")


def first_tier(v):
    """`800(880)` → '800'；`28/168` → '28'；`-` / 空 / 非数字 → ''。"""
    m = _TIER.match(str(v or "").strip().replace(",", "").replace("，", ""))
    return m.group(1) if m else ""


def _trunc(x):
    return int(x) if x >= 0 else -int(-x)


def _best(lo, hi, score):
    """在 [lo,hi] 上找让 score(x) 最接近 0 的 x（端点必扫）。"""
    bx, be = None, None
    steps = 4000
    for i in range(steps + 1):
        x = lo + (hi - lo) * i / steps
        e = abs(score(x))
        if be is None or e < be:
            bx, be = x, e
            if e == 0:
                break
    return bx


def power_raw(panel):
    """威力：面板 → 原值（机库白字 = trunc(|原值|×10+0.4)）。

    有符号：回复系取负（符号由调用方决定，wiki 面板一般给正值）。
    """
    n = int(float(panel))
    sign = -1 if n < 0 else 1
    mag = abs(n)
    raw = int(round(mag / 10.0))
    best = raw
    for cand in range(max(0, raw - 2), raw + 3):
        if abs(cand * 10 - mag) < abs(best * 10 - mag):
            best = cand
    return "0" if best == 0 and n == 0 else str(sign * best)


def stability_raw(panel):
    """集弹性能 → 原值（输出 = 内存值/100，读侧 6 位小数）。"""
    target = int(float(panel))
    guess = _F_500 - (target + 0.1) / _STAB_K
    mem = _best(guess - 2, guess + 2, lambda m: _trunc((_F_500 - m) * _STAB_K + _F_04) - target)
    return "%.6f" % (mem / 100.0)


def rapid_raw(panel):
    """连射速度 → 原值（`#36 RAPIDDELAY`；`COOLTIME` 同值）。"""
    target = int(float(panel))
    guess = _F_2 - (target - _F_04) / _RAPID_K
    x = _best(guess - 0.05, guess + 0.05, lambda v: _trunc((_F_2 - v) * _RAPID_K + _F_04) - target)
    return "%.6f" % x


def reload_raw(panel):
    """装填性能 → 原值（`#36 RELOAD`）。"""
    target = int(float(panel))
    guess = _F_10 - (target - _F_04) / 100.0
    x = _best(guess - 0.05, guess + 0.05, lambda v: _trunc((_F_10 - v) * 100.0 + _F_04) - target)
    return "%.6f" % x


def lockon_raw(panel):
    """锁定 → 原值（`#36 LOCKON_CAM`）。"""
    target = int(float(panel))
    guess = target / 10.0
    x = _best(guess - 0.2, guess + 0.2,
              lambda v: _trunc(float(v) * _F_001 * _F_1000 + _F_04) - target)
    return "%.6f" % x


# ── RAPIDDELAY：原值域 + 原值 → 机库白字的反算 ───────────────────────────────
#
# ★`RAPIDDELAY` 与上面几项**不同**：服务端 §6.3 的 T5 冷却要用**連射速度（白字）**，
# 而表里存的是原值 ⇒ 读侧必须能反算（`serverv/internal/store/battle_params.go::rapidDisplayFromClientRaw`
# 是 Go 侧的孪生，两边改动必须同步）。
#
# 白字公式的出处是 **IDA 实测**：机库属性面板取白字的分支 `sub_80F1A0`（`0x80F1A0`），
# `case 4`（属性位掩码 4 = 連射速度）：
#
#     uint = trunc( (flt_E0E780 − 原值) × flt_E0EA50 × flt_D74FA8 × flt_E0E78C + flt_D73338 )
#
#     flt_E0E780 @0x00E0E780 = 2.0f       flt_E0EA50 @0x00E0EA50 = 0.5263158f (= 10/19)
#     flt_D74FA8 @0x00D74FA8 = 150.0f     flt_E0E78C @0x00E0E78C = 10.0f
#     flt_D73338 @0x00D73338 = 0.4f
#
# ⇒ 有效比例 = 0.5263158 × 150 × 10 = 789.4737，正是 `_RAPID_K`（本模块把 `150 × 10`
#    折成了 `_F_1500 = 1500`）。同函数 `case 1`（威力）= `|原值| × 10`、`case 8`（射程）
#    = `原值 × 0.1 × 10`，与真库 `POWER = 面板/10` / `RANGE` 原样都对得上 ⇒ 取法无误。
#
# 真库实测：`#36 RAPIDDELAY` 的 19 个取值档位与 wiki「連射速度」**19/19 精确回代**
# （0.110657↔1491 … 0.399457↔1263、1.391257↔480、1.999257↔0）。
_RAPID_SCALE = _F_0526 * _F_1500          # 789.4737
RAPID_RAW_LO = 0.05                       # 域下界（真库最小 0.110657）
RAPID_RAW_HI = 2.01                       # 域上界（真库最大 1.999257；白字 0 ⇒ 不校验 T5）


def rapid_is_raw_domain(v):
    """`v` 是不是合法的 `RAPIDDELAY` 客户端原值（= 白字算得出来）。

    域外的一律**不是** `rapid_raw` 的产物，只有两种来路：
      · 白字刻度的值（`1263..1491`、`480`）——旧管线直接把 wiki 显示值写进了原值列；
      · 错列残渣（`200..5000` 的射程/装填/锁定期/效果范围、以及负数）。
    真库实测：`1237` 行里恰好 `713` 行在域内（709 行 = `rapid_raw(wiki 連射)` 精确命中
    + 4 行现役短号），另外 `524` 行全在域外。
    """
    return is_raw_domain("RAPIDDELAY", v)


# ── 原值域哨（集弹 / 装填 / 锁定）─────────────────────────────────────────────
#
# ★为什么这三项也要哨（C4，2026-10-05）
# 真库实测（只统计 sidecar 真实武器号的 `#36` 行）：三项都**两簇分立**，
# 低簇 = `*_raw()` 的产物，高簇 = 旧管线把**面板白字直接写进原值列**的残渣：
#
#   STABILITY   真值簇 −0.003 … 2.29701（71 种，全是 `×.×9701`）／残渣簇 350 … 27500（159 键）
#   RELOAD      真值簇  0.394 … 9.494     ／残渣簇 400 … 5000             （350 键）
#   LOCKON_CAM  真值簇 59.96 … 99.9601    ／残渣簇 740 … 4167             （ 15 键）
#
# 上界取**换算函数的像上界**（不是拟合值），与残渣簇地板之间留 ≥100 倍的间隔：
#   · `stability_raw(面板≥0)` ⇒ mem ≤ 500 ⇒ 输出 ≤ 5.0（`_F_500` 就是 mem 的天花板）
#   · `reload_raw(面板≥0)`    ⇒ 10 − 面板/100 ⇒ 输出 ≤ 10.0
#   · `lockon_raw(面板≥0)`    ⇒ 面板/10，无自然上界 ⇒ 取**维基「锁定」面板域的像**
#     （实测面板 160..2917 ⇒ 原值 16..291.7；残渣簇地板 740 与之间隔 2.5 倍）
# 下界 −0.01 是为了容下 `集弹性能` 面板 980 的边界行（真库实测 −0.00299 = 面板 980.4）。
STABILITY_RAW_LO, STABILITY_RAW_HI = -0.01, 5.0
RELOAD_RAW_LO, RELOAD_RAW_HI = -0.01, 10.0
LOCKON_RAW_LO, LOCKON_RAW_HI = 0.0, 300.0

# 属性 → (下界, 上界)；不在表里的属性 = 本模块不校验（射程/红锁距离是世界单位，原样写）。
RAW_DOMAIN = {
    "RAPIDDELAY": (RAPID_RAW_LO, RAPID_RAW_HI),
    "COOLTIME": (RAPID_RAW_LO, RAPID_RAW_HI),          # 与 RAPIDDELAY 同值同域
    "STABILITY": (STABILITY_RAW_LO, STABILITY_RAW_HI),
    "RELOAD": (RELOAD_RAW_LO, RELOAD_RAW_HI),
    "LOCKON_CAM": (LOCKON_RAW_LO, LOCKON_RAW_HI),
}


def is_raw_domain(attr, v):
    """`v` 是不是 `attr` 的合法客户端原值。

    无域定义的属性（`POWER`/`RANGE`/`HIGH_LOCKON`）返回 `True` = 不校验：
    它们的原值列与白字同量纲（威力 ×10 / 世界单位），没有可分簇的域。
    """
    d = RAW_DOMAIN.get(attr)
    if d is None:
        return True
    try:
        f = float(v)
    except (TypeError, ValueError):
        return False
    return d[0] <= f <= d[1]



def rapid_display(raw):
    """`RAPIDDELAY` 客户端原值 → 机库「連射速度」白字（`sub_80F1A0` case 4 的逐字复刻）。

    返回 `0` = 算不出来（域外 / 白字 ≤ 0）⇒ 与"表里没有这一行"同解：
    调用方据此**不校验 T5**（放行）。失败方向永远偏向放行，绝不误杀合法连射。
    """
    try:
        f = float(raw)
    except (TypeError, ValueError):
        return 0
    if f <= 0 or f >= _F_2:
        return 0
    v = (_F_2 - f) * _RAPID_SCALE + _F_04
    return int(v) if v > 0 else 0


# ── sidecar 列号 → (#36 属性名, 换算函数) ────────────────────────────────
# 列号见 `names/武器分配明细.csv` 表头（= wiki 武器模板列序）。
#   None 的函数 = **原样写**（射程距离 / 红锁距离：世界单位，读侧不做换算）。
SIDECAR_36 = (
    (10, "POWER", power_raw),
    (11, "STABILITY", stability_raw),
    (12, "RAPIDDELAY", rapid_raw),
    (13, "RANGE", None),
    (14, "RELOAD", reload_raw),
    (16, "LOCKON_CAM", lockon_raw),
    (17, "HIGH_LOCKON", None),
)

# RAPIDDELAY 与 COOLTIME 一对（`sub_59A070` 两个子表；14 处实测两者同值）。
COOLTIME_TWIN = "RAPIDDELAY"

# `#36` 里由**本口径管线**产出的全部属性名 = `SIDECAR_36` 的 7 项 + COOLTIME 孪生。
# ★"整族重写"的族清单唯一出处（生成器 `gen_weapon_tables_wiki.FAM36` 与写库脚本
#   `apply_weapon_tables_db.py` 都用它）：sidecar 有行的键，这几族一律**先清后建**，
#   否则 CSV 里已被净化、库里还留着的面板刻度残渣会永远存续（C4）。
FAMILIES_36 = tuple([a for _, a, _ in SIDECAR_36] + ["COOLTIME"])

# ── 列号**回退链**（属性 → 备用 sidecar 列号，按序取第一个有值的）────────────
#
# ★RELOAD 的第二来源 = col15「装填时间」（C4，2026-10-05）。
#   维基**老页面表头写「装填時間」、新页面写「装填性能」**，指的是同一个白字（同量纲、可互换），
#   实测 sidecar 1625 行里这两列**严格互斥**：
#
#       col14（装填性能）有值 930 ／ col15（装填时间）有值 540 ／ 两者都有 **0** ／ 都空 155
#       col14 面板域 50..960（换算后在域内 930/930）
#       col15 面板域 200..900（换算后在域内 **540/540**）
#
#   ⚠️ 不回退的后果：这 540 个键**产不出 RELOAD 行** ⇒ 老管线直接写在原值列的
#      面板刻度（`740`×104 / `760`×51 / `860`×50 …）在库里**永驻**（C4 残渣 350 行、
#      读侧拿 `RELOAD=860` 当"原值" ⇒ 装填时间离谱）。
SIDECAR_36_FALLBACK = {
    "RELOAD": (15,),
}


def attr_value(attr, panel):
    """面板数字 → (写入 #36 的字符串, attr_value_2)。"""
    fn = dict((a, f) for _, a, f in SIDECAR_36)[attr]
    if fn is None:
        s = str(panel)
        return s if "." in s else s + ".000000", ""
    if attr == "POWER":
        return fn(panel), ""
    if attr == "STABILITY":
        v = fn(panel)
        return v, v
    return fn(panel), ""
