# -*- coding: utf-8 -*-
"""
gen_mech_data.py —— 以《机体总表》（中日对照表为准）批量生成机体数据表。

当前生成：
  ① `server/datafiles/lounge/msma/msma_battle_detail.csv`（= #34 MSMA_BATTLE_DETAIL）
     三列 `属性名,键,值`；13 张子表的 col0 词表（IDA 实测）里取含义已定案的 6 个：
        MAX_HP          ← codex.armor      （面板「装甲」）
        MOVE            ← codex.speed      （面板「最高速度」，float）
        BOOST_GAUGEMAX  ← codex.boost      （面板「喷射容量」）
        BOOST_GAUGEHEAL ← codex.boost_cd   （面板「喷射蓄力」，float）
        COST            ← codex.cost
        WARP_TIME       ← codex.return_val （面板「紧急返回性能」）
     键 = 練度ID（与 msma_model.csv / msma_settings.csv 行键同一套）
  不填：RESPAWN_TIME / ENERGY / BOOST_SPEED / JUMP（列数或语义未定案 ⇒ 按项目铁律不猜）
        其中「装备搭载量」对应 codex.payload，但它在 BOOST_SPEED 复合子表里的落点未逐列核实 ⇒ 暂不填 ⚠️

输入：`datatables/names/机体总表.csv`（由 build_mech_master.py 生成）
用法：python datatables/gen_mech_data.py [--dry]
"""
import io
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
MASTER = os.path.join(HERE, 'names', '机体总表.csv')
OUTDIR = os.path.join(ROOT, 'server', 'datafiles', 'lounge', 'msma')
OUT = os.path.join(OUTDIR, 'msma_battle_detail.csv')

# 属性名 → (总表列名, 是否 float)
ATTRS = [('MAX_HP', 'cx_armor', False),
         ('MOVE', 'cx_speed', True),
         ('BOOST_GAUGEMAX', 'cx_boost', False),
         ('BOOST_GAUGEHEAL', 'cx_boost_cd', True),
         ('COST', 'cx_cost', False),
         ('WARP_TIME', 'cx_return', False)]


def main():
    dry = '--dry' in sys.argv
    raw = open(MASTER, encoding='utf-8').read().splitlines()
    hdr = [x.lstrip('#').rstrip(',') for x in raw if x.startswith('#')][0].split(',')
    rows = [l.rstrip(',').split(',') for l in raw if l.strip() and not l.startswith('#')]
    ix = {h: i for i, h in enumerate(hdr)}
    print('总表 %d 行；列：%s…' % (len(rows), hdr[:6]))

    lines = ['#属性名,键,值,',
             '# ===== msma/msma_battle_detail.csv（MSMA_BATTLE_DETAIL / 表ID 34 / 下载序 34）=====',
             '# 三列长表：col0=属性名（选 13 张子表之一）｜col1=键（練度ID）｜col2=值',
             '# col0 词表（IDA 实测 off_D7A298）：RESPAWN_TIME=1 WARP_TIME=2 COST=3 MAX_HP=4 ENERGY=5',
             '#   MOVE=6 BOOST_GAUGEMAX=7 BOOST_GAUGEHEAL=8 BOOST_SPEED=9 JUMP=10',
             '# 值列类型：MOVE / BOOST_GAUGEHEAL 是 float（子表 sub_BBB470），其余整型（sub_BBB370）',
             '# 数据来源：unpackdat/codex/data/units.json（经《中日对照表》按 wiki 页名 join）',
             '# 面板对应：MAX_HP=装甲｜MOVE=最高速度｜BOOST_GAUGEMAX=喷射容量｜BOOST_GAUGEHEAL=喷射蓄力｜',
             '#           COST=COST｜WARP_TIME=紧急返回性能；「装备搭载量」= payload 落点未核实 ⇒ 暂不填,',
             '# 不填：RESPAWN_TIME / ENERGY / BOOST_SPEED / JUMP（列数或语义未定 ⇒ 不猜）,',]
    n, skipped = 0, 0
    for r in rows:
        rid = r[ix['練度ID']].strip()
        if not rid:
            continue
        got = [(a, r[ix[c]].strip()) for a, c, _ in ATTRS]
        if not any(v for _, v in got):
            skipped += 1
            continue
        for a, v in got:
            if not v:
                continue
            isf = dict((x, fl) for x, _, fl in ATTRS)[a]
            lines.append('%s,%s,%s,' % (a, rid, ('%.6f' % float(v)) if isf else v))
            n += 1
    print('生成行 %d（有值的机体 %d 台；无 codex 数值而跳过 %d 台）' % (n, len(rows) - skipped, skipped))
    if dry:
        print('（--dry，未写盘）')
        return 0
    os.makedirs(OUTDIR, exist_ok=True)
    open(OUT, 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
    print('已写 %s（%d 字节）' % (OUT, os.path.getsize(OUT)))
    print('\n=== 自检 ===')
    allrows = [l for l in lines if not l.startswith('#')]
    print('  数据行 %d；属性分布 %s' % (len(allrows),
                                      {a: len([1 for l in allrows if l.startswith(a + ',')]) for a, _, _ in ATTRS}))
    for l in allrows[:6]:
        print('   ', l)
    return 0


if __name__ == '__main__':
    sys.exit(main())
