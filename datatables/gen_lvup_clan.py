# -*- coding: utf-8 -*-
"""
gen_lvup_clan.py —— 生成 `growth/lvup_clan.csv`（表ID 15，下载序 15）的**内容**。

产出：`server/datafiles/lounge/growth/lvup_clan.csv`（服务器实际下发的 CSV）

★ 本脚本只做"有内容"这一步（见 `03-还原进度.md` 三阶段：列已注释 → 有内容 → 数值已校准）。
★ 与 #1/#2/#4/#5 那些"有真实资料源"的表不同：`LVUP_CLAN` 的**官方数值没有任何外部来源**
  （客户端只从服务端下载这张表，仓库里没有官服导出；`datatables/02-资料源.md` 的三条腿
  ——`unpackdat/settings`、资源族、codex——都不含氏族成长曲线）。
  所以本表按 `04-填充日志.md` 的规则**给"静态范围内的占位曲线"并把假设写在明面上**，
  **不假称是官服还原**；运营要改数值，改下面 `need()` 一个函数重跑即可
  （或直接走 GM 的「全服配置 / 玩法模块」页改这一列）。

为什么必须给 col1（每级所需经验）填数，而不是像 P286 批量那样"只填主键"：
  1. **等级推不出来**：`internal/store/clan_exp.go` 的 `LoadClanLevelNeed` 跳过 `need <= 0`
     的行（非正需求会让累计需求倒退），全 0 ⇒ 可用行 0 条 ⇒ `ClanLevelForExp` 返回 0
     ⇒ `CS-0x6CF9` 投经验后氏族**永远停在 1 级**（等级链白做）。
  2. **界面显示不出**：客户端 `sub_63D060` 用 `need[L] + exp − cum[L]` 算"段内进度"、
     `cum[L] − exp` 算"升下一级还差"（cum = 逐级累加，`sub_579B40`）。need 全 0 ⇒ cum 全 0
     ⇒ "还差"变成 `0 − exp`（u32 上是个天文数字）。
  3. **不能空表**：`04-填充日志.md` 的 P286 口径「不允许空表」；本表当时漏填（详见日志补记）。

列语义（`01-列注释/15-15-LVUP_CLAN.md`；读取函数 `sub_579960`，后处理 `sub_579B40`）：

  csv 0  clan_level     u8   → 行 +8   主键，等级（**1 起，没有 0 级那一行**）
  csv 1  member_cap     u32  → 行 +0   ★**每级所需经验**（不是人数上限，见下"两处改名"）
  csv 2  (gap)              读表跳过 ⇒ 留空 0
  csv 3  mechanic_level enum → 行 +24  部队机械师等级档 MECHANIC_LV0..10
  csv 4  exp_base       u32  → 行 +12  升级经验基数
  csv 5  exp_increment  u32  → 行 +16  升级经验增量（读表另存 `-(col4+col5)` 于行 +20）
  csv 6  rokaku_level   enum → 行 +28  着陆平台等级档 ROKAKU_LV0..5
  csv 7  gp_bonus       u32  → 行 +32  部队 GP 加成
  csv 8  shop_level     enum → 行 +36  部队商店等级档 SHOP_LV0..21
  csv 9  deck_cost_level enum → 行 +40 卡组 COST 上限档 DECKCOST_LV0..5（★档位，不是费用值）
  csv 10 bonus_gp       u32  → 行 +44  等级奖励 GP
  csv 11 discount_level enum → 行 +48  商店折扣档 DISCOUNT_LV0..10
  csv 12 extra_param    u32  → 行 +52  扩展参数

两处改名（本表历史注记的两个坑，都不改列名、只改释义，避免 cfg 表结构漂移）：
  - `member_cap`（csv 1）**不是成员上限**：读表 `sub_579960` @`0x5799a4` 把它写进行内 +0，
    `sub_579B40` 逐级累加成累计需求（`row[+4] = row[+0] + 上一行 row[+4]`），客户端
    `sub_63D060` @`0x63d130` 再拿 `cinfo.exp` 与它做差 —— 只有"经验"能这么算。
    队伍人数上限**不在本表**，是本服常量 `store.ClanMemberCap = 50`。
  - `deck_cost_level`（csv 9）只是 0..5 的**档位名**（枚举转换器 `sub_579500` 就是
    `DECKCOST_LV0..5 → 0..5` 的查表），线上真正的编队费用上限另有出处
    （客户端 `app+0x6F198`，由服务端 `SC-0x68D7` 下发的那一格）⇒ 本表给不出费用值。

★ 本批**只填 col0 与 col1**，其余列留空（读作 0）：
  - 四个"档位"列（col3/col6/col8/col9/col11）的**等级↔档位映射表官方未知**
    （客户端拿它们做反查，`sub_578BB0(table, 档位列, 值)` 返回命中的等级行），
    凭空给一套映射会造出"1 级氏族就有高档商店"这类说不清的界面；
  - col4/col5（exp_base/exp_increment）读表另存 `-(col4+col5)` 于行 +20，
    消费方未取证 ⇒ 留 0 不误导；
  - col7/col10/col12（GP 加成 / 等级奖励 GP / 扩展参数）属**经济数值**，没有来源 ⇒ 留 0。
  这些列都能在 GM「全服配置」或「玩法模块」页逐行改（cfg 表在库里是唯一维护入口）。

用法：
  python gen_lvup_clan.py            # 生成
  python gen_lvup_clan.py --check    # 只做方言自检，不写文件
"""
import io
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, 'server', 'datafiles', 'lounge', 'growth', 'lvup_clan.csv')

# 等级范围：客户端满级判定是 `level + 1 >= 50`（`CClanExpUseWindow` 的 `sub_929820`），
# 即 49 级是最后一档能升级的等级 ⇒ 表里必须覆盖 **1..50**（50 级自己那一行用于显示
# "50 级段内还差多少"）。
LV_MIN, LV_MAX = 1, 50

COLS = 13  # csv 列号 0..12


def need(level):
    """从 `level` 级升到 `level+1` 级所需的氏族经验（csv col1）。

    ★ 本服口径的**占位曲线**（无官方来源，可整体替换）：
        need(L) = 10 · L · (L + 10)
      ⇒ 1 级 110 / 10 级 2 000 / 25 级 8 750 / 49 级 28 910 / 50 级 30 000
      ⇒ 1→50 级累计 556 750
    选它的理由：单调递增、低等级便宜（新氏族能立刻看到进度条动）、高等级贵
    （拉长养成），且是闭式公式 ⇒ 改常数即可重算，不用手改 50 行。
    客户端与 `store.ClanLevelForExp` 都**只读这张表**，换曲线不需要改代码。
    """
    return 10 * level * (level + 10)


def build_rows():
    return [(lv, need(lv)) for lv in range(LV_MIN, LV_MAX + 1)]


def render(rows):
    # 表头口径与仓库里"有内容"的表一致（见 `msma/msma_weapon_set.csv`）：
    # 第一行 = 列名行（`#` + 表头），第二行 = `# ===== 表标识 =====`，之后才是说明。
    head = [
        '#clan_level,member_cap,reserved_u32_2,mechanic_level,exp_base,exp_increment,'
        'rokaku_level,gp_bonus,shop_level,deck_cost_level,bonus_gp,discount_level,extra_param',
        '# ===== growth/lvup_clan.csv （表ID 15 / 下载序 15 / CLvupClanTable / 读取函数 sub_579960）=====',
        '# 部队（Clan）等级成长表。逐级累计需求 sub_579B40；消费方 sub_63D060（氏族模型 +752 段内进度、',
        '# +756 升下一级还差、+760 当前经验）。等级列从 1 起，没有 0 级那一行。',
        '#   col0  clan_level       u8   主键，等级（1..%d）' % LV_MAX,
        '#   col1  member_cap      u32  ★每级所需经验★（列名是历史误名，见下）',
        '#   col2  reserved_u32_2  —    读表跳过（gap）⇒ 留空',
        '#   col3  mechanic_level  enum 部队机械师等级档 MECHANIC_LV0..10',
        '#   col4  exp_base        u32  升级经验基数',
        '#   col5  exp_increment   u32  升级经验增量（读表另存 -(col4+col5) 于行 +20）',
        '#   col6  rokaku_level    enum 着陆平台等级档 ROKAKU_LV0..5',
        '#   col7  gp_bonus        u32  部队 GP 加成',
        '#   col8  shop_level      enum 部队商店等级档 SHOP_LV0..21',
        '#   col9  deck_cost_level enum 卡组 COST 上限档 DECKCOST_LV0..5（★档位名，不是费用值）',
        '#   col10 bonus_gp        u32  等级奖励 GP',
        '#   col11 discount_level  enum 商店折扣档 DISCOUNT_LV0..10',
        '#   col12 extra_param     u32  扩展参数',
        '#⚠️ col1（"每级所需经验"）是**本服占位曲线** need(L)=10*L*(L+10)，**非官服还原**（官服数值无来源，',
        '#   见 datatables/02-资料源.md 的三条腿都不含氏族成长）。改曲线改 datatables/gen_lvup_clan.py 的',
        '#   need() 重跑，或在 GM 的「全服配置 / 玩法模块」页逐行改（cfg 表是库里唯一维护入口）。',
        '#   列名 member_cap 是历史误名：读表写进行内 +0，sub_579B40 把它逐级累加当"本级所需经验"，',
        '#   客户端再拿 cinfo.exp 与累计值做差算进度 ⇒ 只有"经验"能这么算。队伍人数上限是本服常量',
        '#   store.ClanMemberCap = 50，与这张表无关。',
        '#⚠️ 其余列本批留空（= 0）：档位列（col3/6/8/9/11）的等级↔档位映射官方未知（客户端拿它们做反查，',
        '#   sub_578BB0），凭空给会造出"1 级氏族就有高档商店"这类说不清的界面；col4/col5 经 sub_63D060 核对',
        '#   本链不读（它只用行 +0 与 +4）；col7/10/12 属经济数值无来源。留 0 不误导。',
        '#⚠️ 等级必须**连续覆盖**服务端能发出的等级：客户端按等级查本表，查不到就 `v4=0` 再解引用（sub_63D060',
        '#   @0x63D130 是空指针读）⇒ 发送超出本表的等级会让客户端崩。客户端满级判定 level+1 >= 50',
        '#   （CClanExpUseWindow / sub_929820）⇒ 表覆盖 1..50。',
        '#生成：python datatables/gen_lvup_clan.py（等级 %d..%d，共 %d 行，1→%d 级累计 %d 经验）'
        % (LV_MIN, LV_MAX, len(rows), LV_MAX, sum(n for _, n in rows)),
    ]
    lines = list(head)
    for lv, n in rows:
        f = [''] * COLS
        f[0] = str(lv)
        f[1] = str(n)
        lines.append(','.join(f) + ',')
    return '\r\n'.join(lines) + '\r\n'


def self_check(text):
    b = text.encode('utf-8')
    ok = True
    if b.startswith(b'\xef\xbb\xbf'):
        print('!! 带 BOM')
        ok = False
    if b.count(b'\n') != b.count(b'\r\n'):
        print('!! 存在非 CRLF 换行')
        ok = False
    body = [x for x in text.split('\r\n') if x and not x.startswith('#')]
    bad = [x for x in body if not x.endswith(',')]
    if bad:
        print('!! %d 行缺尾逗号，例: %r' % (len(bad), bad[0][:60]))
        ok = False
    if not body:
        print('!! 无数据行')
        ok = False
    # 主键唯一 + 每级经验单调递增（客户端按等级升序遍历，曲线必须单调）
    keys, needs = [], []
    for line in body:
        f = line.split(',')
        keys.append(int(f[0]))
        needs.append(int(f[1]))
    if keys != sorted(set(keys)):
        print('!! 主键不唯一或未升序')
        ok = False
    if any(needs[i] >= needs[i + 1] for i in range(len(needs) - 1)):
        print('!! 每级所需经验不是严格递增（累计需求会失真）')
        ok = False
    print('自检：BOM 无 ✓ / CRLF ✓ / UTF-8 ✓ / 尾逗号 ✓' if ok else '自检：失败 ✗')
    print('数据行 %d（等级 %d..%d），注释行 %d'
          % (len(body), keys[0], keys[-1], text.count('\r\n#') + 1))
    return ok


def main():
    rows = build_rows()
    text = render(rows)
    if '--check' in sys.argv:
        if os.path.exists(OUT):
            # ★必须 newline='' 读，否则 Python 通用换行会把 CRLF 折成 LF ⇒ 自检误判
            self_check(open(OUT, encoding='utf-8', newline='').read())
        else:
            print('目标文件不存在')
        return 0
    with open(OUT, 'wb') as f:
        f.write(text.encode('utf-8'))
    print('已写 %s' % OUT)
    self_check(text)
    print('前 3 行 / 后 3 行数据：')
    for l in [x for x in text.split('\r\n') if x and not x.startswith('#')][:3]:
        print('   ' + l)
    for l in [x for x in text.split('\r\n') if x and not x.startswith('#')][-3:]:
        print('   ' + l)
    return 0


if __name__ == '__main__':
    sys.exit(main())
