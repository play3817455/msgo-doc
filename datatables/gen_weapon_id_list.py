# -*- coding: utf-8 -*-
"""
gen_weapon_id_list.py —— 从**客户端本地表**里挖出"武器ID 全清单"，源出 `datatables/names/武器ID清单.csv`。

用途：#36 `item/weapon_battle_detail.csv`（WEAPON_BATTLE_DETAIL）与 #37 `item/weapon_settings.csv`（WEAPON_SETTING）
      都是**以武器ID 为键**的表（#36 的键是字符串形式的武器ID）。本脚本把本地能挖到的真实武器ID汇总成键清单，
      供将来填内容时用（见 `01-列注释/36-36-WEAPON_BATTLE_DETAIL.md`）。

来源（本地，可核）：
  unpackdat/settings/weapon_visual_customize.csv  第 0 列  = 武器ID
  unpackdat/settings/msma_mesh_customize.csv      第 1 列  = 武器ID
  unpackdat/settings/msma_visual_customize.csv    第 1 列  = 武器ID
  unpackdat/settings/weapon_wrestle.csv           第 0 列  = アイテムID（近战武器，7 位）
  unpackdat/item/**                              目录名（资源族）里出现的 9 位武器ID

用法：python gen_weapon_id_list.py
"""
import glob
import io
import os
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SETTINGS = os.path.join(ROOT, 'unpackdat', 'settings')
OUT = os.path.join(HERE, 'names', '武器ID清单.csv')

# (文件, 列号, 说明)  —— 列号按"去掉 # 表头行后"的 0 基位置
SOURCES = [
    ('weapon_visual_customize.csv', 0, '武器视觉定制表'),
    ('msma_mesh_customize.csv', 1, '机体网格定制表'),
    ('msma_visual_customize.csv', 1, '机体视觉定制表'),
    ('weapon_wrestle.csv', 0, '近战武器表(アイテムID)'),
]


def read_rows(path):
    t = open(path, 'rb').read().decode('utf-8', 'replace')
    return [l for l in t.replace('\r\n', '\n').split('\n') if l.strip()]


def main():
    found = {}   # id -> set(来源)
    for fn, col, label in SOURCES:
        p = os.path.join(SETTINGS, fn)
        if not os.path.exists(p):
            print('缺失', fn)
            continue
        n = 0
        for l in read_rows(p):
            s = l.strip()
            if s.startswith('#') or s.startswith('#'):
                continue
            f = s.split(',')
            if len(f) <= col:
                continue
            v = f[col].strip()
            if v.isdigit():
                found.setdefault(v, set()).add(label)
                n += 1
        print('%-32s 取到 %d 行' % (fn, n))

    keys = sorted(found, key=lambda x: (len(x), x))
    lines = [
        '#武器ID,来源,位数,备注,',
        '# ===== 武器ID 全清单（从客户端本地表挖掘，供 #36 WEAPON_BATTLE_DETAIL / #37 WEAPON_SETTING 作键）=====',
        '# 说明：#36 的 CSV 三列为 `属性名, 键, 值`，键为**字符串**（见 01-列注释/36-36-WEAPON_BATTLE_DETAIL.md）。',
        '#       本清单 = 本地可核的真实武器ID，共 %d 个；数字位数是判断"哪种ID体系"的重要线索。' % len(keys),
        '# 生成：python datatables/gen_weapon_id_list.py',
    ]
    for k in keys:
        src = '|'.join(sorted(found[k]))
        lines.append('%s,%s,%d,%s,' % (k, src, len(k), ''))
    with open(OUT, 'wb') as f:
        f.write(('\r\n'.join(lines) + '\r\n').encode('utf-8'))
    print('写入 %s：%d 个武器ID' % (OUT, len(keys)))
    by_len = {}
    for k in keys:
        by_len[len(k)] = by_len.get(len(k), 0) + 1
    print('位数分布：', dict(sorted(by_len.items())))
    for k in keys[:8]:
        print('   ', k, sorted(found[k]))
    return 0


if __name__ == '__main__':
    sys.exit(main())
