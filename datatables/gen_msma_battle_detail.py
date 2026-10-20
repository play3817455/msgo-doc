# -*- coding: utf-8 -*-
"""
gen_msma_battle_detail.py —— 生成 `msma/msma_battle_detail.csv`（MSMA_BATTLE_DETAIL，表ID 34，下载序 34）的**内容**。

★ 本表 = **机体战斗明细的"属性→值"长表**：CSV 三列 = `属性名, 键, 值`
  （结构由 `sub_A47BC0` / `sub_A5D270` / 词表 `off_D7A298` / 分派 `sub_57BB70` 实测，详见
   `01-列注释/34-34-MSMA_BATTLE_DETAIL.md`）。

  col0 = 属性名（★必须原样写★，取值见下表）
  col1 = 键（**字符串**；本批按"練度ID 的十进制字符串"落 —— ⚠️ 假设，见文件头注释）
  col2 = 值（**类型随属性而异**：u32 或 float）

填的 6 个属性（值与 codex 真值对应；对应依据见 06-UI语义字典与参数绑定攻关.md §七）：
  MAX_HP         ← codex.armor      (u32)   → 面板「装甲」
  MOVE           ← codex.speed      (float) → 面板「最高速度」
  BOOST_GAUGEMAX ← codex.boost      (u32)   → 面板「喷射容量」
  BOOST_GAUGEHEAL← codex.boost_cd   (float) → 面板「喷射蓄力」
  COST           ← codex.cost       (u32)   → COST
  WARP_TIME      ← codex.return_val (u32)   → 面板「紧急返回性能」

不填：RESPAWN_TIME / ENERGY / BOOST_SPEED / JUMP（语义或列数未定 ⇒ 不猜）。
数据来源：`datatables/names/机体名对照表.csv`（練度ID ↔ codex 中文名）+ `unpackdat/codex/data/units.json`。

用法：python gen_msma_battle_detail.py [--check]
"""
import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BRIDGE = os.path.join(HERE, 'names', '机体名对照表.csv')
CODEX = os.path.join(ROOT, 'unpackdat', 'codex', 'data', 'units.json')
OUT = os.path.join(ROOT, 'server', 'datafiles', 'lounge', 'msma', 'msma_battle_detail.csv')

# (col0 属性名, codex 字段, 值类型)  —— 顺序 = 写入顺序
ATTRS = [
    ('MAX_HP', 'armor', 'int'),
    ('MOVE', 'speed', 'float'),
    ('BOOST_GAUGEMAX', 'boost', 'int'),
    ('BOOST_GAUGEHEAL', 'boost_cd', 'float'),
    ('COST', 'cost', 'int'),
    ('WARP_TIME', 'return_val', 'int'),
]


def load_bridge():
    """練度ID → codex 中文名（只取已配对的）"""
    out = []
    if not os.path.exists(BRIDGE):
        return out
    for i, line in enumerate(open(BRIDGE, encoding='utf-8-sig').read().splitlines()):
        if i == 0 or not line.strip():
            continue
        p = line.split(',')
        if len(p) >= 3 and p[0].strip() and p[2].strip():
            out.append((p[0].strip(), p[2].strip()))
    return out


def fmt(v, kind):
    if kind == 'float':
        return '%.6f' % float(v)
    return str(int(v))


def render(pairs, units):
    head = [
        '#属性名,键,值,',
        '# ===== msma/msma_battle_detail.csv （MSMA_BATTLE_DETAIL / 表ID 34 / 下载序 34 / CMSMABattleDetailTables / 读取 sub_A47BC0）=====',
        '# 本表 = ★机体战斗明细的"属性→值"长表★：一个容器装 13 张子表，col0 的属性名决定进哪张子表。',
        '#   结构实测：sub_A47BC0 读 col0 → sub_57BD40 查词表 off_D7A298 → sub_57BB70 按编号 1..10 分派到子表；',
        '#             子表再读 col1（★字符串键★）与 col2（值；每个子表自带取列函数 sub_BBB370=整型 / sub_BBB470=浮点）。',
        '# ★col0 词表（名 → 子表编号）：',
        '#   RESPAWN_TIME=1  WARP_TIME=2  COST=3  MAX_HP=4  ENERGY=5',
        '#   MOVE=6  BOOST_GAUGEMAX=7  BOOST_GAUGEHEAL=8  BOOST_SPEED=9  JUMP=10',
        '#   （SHOT/LOCKON/RELOAD 三张子表不在本词表 ⇒ 由别的表喂）',
        '# 本次填 6 个属性（值取自 codex 真实机体数值）：',
        '#   MAX_HP(u32)←armor    MOVE(float)←speed   BOOST_GAUGEMAX(u32)←boost',
        '#   BOOST_GAUGEHEAL(float)←boost_cd          COST(u32)←cost           WARP_TIME(u32)←return_val',
        '#   不填：RESPAWN_TIME / ENERGY / BOOST_SPEED / JUMP（语义或列数未定 ⇒ 不猜）',
        '# ⚠️ 假设（col1 键）：已证"键是字符串"（sub_A5D270 读 col1 为字符串；机体侧 对象+436 同为 std::string），',
        '#   但未证内容 ⇒ 本批按"練度ID 的十进制字符串"落。若实际不是，改 gen_msma_battle_detail.py 里一处即可重跑。',
        '# 来源：datatables/names/机体名对照表.csv（練度ID↔codex 中文名，当前配对率 61.6%）+ unpackdat/codex/data/units.json',
        '# 生成：python datatables/gen_msma_battle_detail.py（机体 %d 台 × %d 属性 = %d 行）' % (len(pairs), len(ATTRS), len(pairs) * len(ATTRS)),
    ]
    lines = list(head)
    n = 0
    for key, cn in pairs:
        u = units.get(cn)
        if not u:
            continue
        for attr, field, kind in ATTRS:
            v = u.get(field)
            if v in (None, ''):
                continue
            lines.append('%s,%s,%s,' % (attr, key, fmt(v, kind)))
            n += 1
    return '\r\n'.join(lines) + '\r\n', n


def self_check(text):
    b = text.encode('utf-8')
    ok = True
    if b.startswith(b'\xef\xbb\xbf'):
        print('!! 带 BOM'); ok = False
    if b.count(b'\n') != b.count(b'\r\n'):
        print('!! 存在非 CRLF 换行'); ok = False
    body = [x for x in text.split('\r\n') if x and not x.startswith('#')]
    if [x for x in body if not x.endswith(',')]:
        print('!! 数据行缺尾逗号'); ok = False
    if [x for x in body if len(x.split(',')) < 4]:
        print('!! 数据行字段数不足（应为 3 列 + 尾逗号）'); ok = False
    if not body:
        print('!! 无数据行'); ok = False
    print('自检：BOM 无 ✓ / CRLF ✓ / UTF-8 ✓ / 尾逗号 ✓ / 3 列 ✓' if ok else '自检：失败 ✗')
    print('数据行 %d，注释行 %d' % (len(body), text.count('\r\n#') + 1))
    return ok


def main():
    pairs = load_bridge()
    units = {u['name']: u for u in json.load(open(CODEX, encoding='utf-8'))['units']}
    text, n = render(pairs, units)
    if '--check' in sys.argv:
        if os.path.exists(OUT):
            self_check(open(OUT, encoding='utf-8', newline='').read())
        else:
            print('目标文件不存在')
        return 0
    with open(OUT, 'wb') as f:
        f.write(text.encode('utf-8'))
    print('桥表机体 %d 台 → 写入 %d 行 → %s' % (len(pairs), n, OUT))
    self_check(text)
    for l in [x for x in text.split('\r\n') if x and not x.startswith('#')][:6]:
        print('   ' + l)
    return 0


if __name__ == '__main__':
    sys.exit(main())
