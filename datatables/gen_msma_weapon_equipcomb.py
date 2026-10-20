# -*- coding: utf-8 -*-
"""
gen_msma_weapon_equipcomb.py —— 生成 `msma/msma_weapon_equipcomb.csv`（表ID 2，下载序 2）的**内容**。

产出：`server/datafiles/msma_msma_weapon_equipcomb.csv`

★ 设计要点：本表的三个类别列**从 `msma_weapon_set.csv` 派生**（同一 col0 组内出现的武器类别去重）
  ⇒ 两张表天然自洽；等武器的射击/EX 池补上后，重跑本脚本即可自动跟随，不会脱节。

列语义（`sub_5859B0` 反编译实测；行结构 = **24 字节**，由消费方 `sub_836D10` 的 `row += 6 dwords` 实证）：
  col0  = 组合规则ID（主键；与 CHARA_PARAM 行的 +396 字段同键空间）
  col2  = ★裁定方式★ 枚举 `sub_585580`，**5 个字面量**：
            FIXED / CATEGORY_COMBINATION / ID_COMBINATION / PERMIT_ID_COMBINATION / REQUIRED_ID_COMBINATION
  col3  = 武器类别 A（枚举 `sub_585FD0`，28 值 → 行 +4）
  col4  = 武器类别 B（同上 → 行 +8）
  col5  = 武器类别 C（同上 → 行 +0xC）
  col6  = u32（→ 行 +0x10，语义未定）
  col8  = u32（→ 行 +0x14，语义未定）
  col10 = ★地区开关★（`sub_5854E0` 返回 2 = CHINA ⇒ 插入；1 = JAPAN ⇒ **整行丢弃**）
          —— 与 `msma_weapon_set.csv` 的 col28 同一机制（旧列注释把它写成"0 个可选值的枚举"是**错的**）

用法：
  python gen_msma_weapon_equipcomb.py
  python gen_msma_weapon_equipcomb.py --check
"""
import io
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATAFILES = os.path.join(ROOT, 'server', 'datafiles', 'lounge', 'msma')  # ★时机层 lounge=大厅登录期；类别层 msma=机体
SRC = os.path.join(DATAFILES, 'msma_weapon_set.csv')            # 派生源（同目录，已是"有内容"状态）
OUT = os.path.join(DATAFILES, 'msma_weapon_equipcomb.csv')

REGION = 'CHINA'          # col10：CHINA ⇒ 保留
COLS = 11                 # 列号 0..10
MODE = 'CATEGORY_COMBINATION'   # col2：按**类别**裁定（与武器组按类别登记一致）
FALLBACK_CLASS = 'WRESTLE'      # 组内没解析到类别时的兜底（= 当前武器池的类别）


def read_rows(path):
    if not os.path.exists(path):
        return []
    out = []
    for l in open(path, encoding='utf-8', newline='').read().split('\r\n'):
        if l and not l.startswith('#'):
            out.append(l.split(','))
    return out


def build():
    groups = {}
    order = []
    for f in read_rows(SRC):
        if len(f) < 6:
            continue
        key, cls = f[0].strip(), (f[5] or '').strip()
        if not key:
            continue
        if key not in groups:
            groups[key] = []
            order.append(key)
        if cls and cls not in groups[key]:
            groups[key].append(cls)
    rows = []
    for key in order:
        cls = (groups[key] or [FALLBACK_CLASS])[:3]
        while len(cls) < 3:
            cls.append(cls[-1])
        rows.append((key, cls))
    return rows


def render(rows):
    head = [
        '#ID,,,,,,,,地区,',
        '# ===== msma/msma_weapon_equipcomb.csv （表ID 2 / 下载序 2 / CMSMAWeaponEquipCombTable / 读取函数 sub_5859B0）=====',
        '# 用途：武器装备**组合规则**——某组合ID下"哪些武器类别可以/必须搭配"。消费方 sub_836D10（装备界面）',
        '#       用"机体 CHARA_PARAM 行 +372（= col38 練度ID）"作键取本表全部行，逐行比对玩家已装武器的【ID】与【类别】⇒ 触发界面提示。',
        '# 列语义（静态实测，详见 datatables/01-列注释/02-2-MSMA_WEAPON_EQUIPCOMB.md）：',
        '#   col0  = 组合规则ID（主键）',
        '#   col2  = 裁定方式（枚举 sub_585580，5 值：FIXED / CATEGORY_COMBINATION / ID_COMBINATION /',
        '#            PERMIT_ID_COMBINATION / REQUIRED_ID_COMBINATION）',
        '#   col3/col4/col5 = 三个武器类别（枚举 sub_585FD0，28 值；行 +4/+8/+0xC）',
        '#   col6、col8     = 数值（行 +0x10/+0x14，语义未定）⇒ 本批留 0',
        '#   col10 = ★地区开关：CHINA ⇒ 插入；JAPAN ⇒ 整行静默丢弃（与 weapon_set 的 col28 同机制）',
        '# ★本表内容由 msma_msma_weapon_set.csv 派生（同 col0 组内武器类别去重）⇒ 两表自洽；武器池变更后重跑本脚本。',
        '# ⚠️ 假设：col0 与 msma_weapon_set.csv 同一编号空间（練度ID）；裁定方式统一取 CATEGORY_COMBINATION',
        '#          （其余 4 值 FIXED / ID_COMBINATION / PERMIT_ID_COMBINATION / REQUIRED_ID_COMBINATION 未用）。',
        '# 生成：python datatables/gen_msma_weapon_equipcomb.py（%d 行）' % len(rows),
    ]
    lines = list(head)
    for key, cls in rows:
        f = [''] * COLS
        f[0] = key
        f[2] = MODE
        f[3], f[4], f[5] = cls[0], cls[1], cls[2]
        f[6] = '0'
        f[8] = '0'
        f[10] = REGION
        lines.append(','.join(f) + ',')
    return '\r\n'.join(lines) + '\r\n'


def self_check(text):
    b = text.encode('utf-8')
    ok = True
    if b.startswith(b'\xef\xbb\xbf'):
        print('!! 带 BOM'); ok = False
    if b.count(b'\n') != b.count(b'\r\n'):
        print('!! 存在非 CRLF 换行'); ok = False
    body = [x for x in text.split('\r\n') if x and not x.startswith('#')]
    bad = [x for x in body if not x.endswith(',')]
    if bad:
        print('!! %d 行缺尾逗号，例: %r' % (len(bad), bad[0][:60])); ok = False
    if not body:
        print('!! 无数据行'); ok = False
    print('自检：BOM 无 ✓ / CRLF ✓ / UTF-8 ✓ / 尾逗号 ✓' if ok else '自检：失败 ✗')
    print('数据行 %d，注释行 %d' % (len(body), text.count('\r\n#') + 1))
    return ok


def main():
    rows = build()
    if not rows:
        print('!! 派生源为空：%s（请先跑 gen_msma_weapon_set.py）' % SRC)
        return 1
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
    print('派生源 %s → %d 组' % (os.path.basename(SRC), len(rows)))
    print('已写 %s' % OUT)
    self_check(text)
    print('前 3 行数据：')
    for l in [x for x in text.split('\r\n') if x and not x.startswith('#')][:3]:
        print('   ' + l)
    return 0


if __name__ == '__main__':
    sys.exit(main())
