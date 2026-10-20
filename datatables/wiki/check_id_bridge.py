# -*- coding: utf-8 -*-
"""
check_id_bridge.py —— 系统性地找「本地 ID ↔ wiki 机体序号」的换算规律（**离线**，只用本地已囤数据）。

涉及三套 ID 空间：
  ① **練度ID**（7 位，如 1111011）—— `CHARA_PARAM`/`MSMA_RENTAL` 的键、`datatables/names/机体名对照表.csv` 第 0 列
  ② **モデルID**（9 位，如 184300101 / 101280501，个别 13 位）—— `CHARA_MODEL` 的模型ID、`msma_visual_customize` 第 0 列（★这列带 MS 名备注）
  ③ **武器ID**（9 位，如 213203402）—— `weapon_visual_customize` 第 0 列（★带 MS 名备注）
  ④ **wiki 机体序号**（6 位，如 210985 / 213952）—— 资料站每页 `|序号=`（★这是我们唯一能拿到"机体名"的官方号）

做法：把 ①②③ 各种"切片/整数变换"的结果去 ④ 的集合里查命中，命中率最高的那条就是换算规律。

用法：python check_id_bridge.py
"""
import io
import os
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
SET = os.path.join(ROOT, 'unpackdat', 'settings')
NAMES = os.path.join(ROOT, 'datatables', 'names')


def read_rows(path):
    out = []
    if not os.path.exists(path):
        return out
    for l in open(path, encoding='utf-8', errors='replace').read().splitlines():
        if l.strip() and not l.startswith('#'):
            out.append([c.strip() for c in l.split(',')])
    return out


def wiki_index():
    """wiki 序号 → (名称, 页面)"""
    name, page = {}, {}
    p = os.path.join(HERE, 'wiki_ms_stats.csv')
    for l in open(p, encoding='utf-8-sig').read().splitlines():
        if not l or l.startswith('#'):
            continue
        f = l.rstrip(',').split(',')
        if len(f) > 3 and f[2].isdigit():
            if f[3]:
                name.setdefault(f[2], f[3])
            page.setdefault(f[2], f[0])
    p = os.path.join(HERE, 'wiki_ms_weapons.csv')
    for l in open(p, encoding='utf-8-sig').read().splitlines():
        if not l or l.startswith('#'):
            continue
        f = l.rstrip(',').split(',')
        if len(f) > 1 and f[1].isdigit():
            page.setdefault(f[1], f[0])
    return name, page


def local_sets():
    out = {}
    # ① 練度ID（带机体名）
    m = {}
    p = os.path.join(NAMES, '机体名对照表.csv')
    for r in read_rows(p):
        if r and r[0].isdigit():
            m[r[0]] = r[1] if len(r) > 1 else ''
    out['練度ID'] = m
    # ② モデルID（带机体名）
    m = {}
    for r in read_rows(os.path.join(SET, 'msma_visual_customize.csv')):
        if r and r[0].isdigit():
            m[r[0]] = (r[7] if len(r) > 7 else '').lstrip('#')
    for r in read_rows(os.path.join(SET, 'msma_mesh_customize.csv')):
        if r and r[0].isdigit():
            m.setdefault(r[0], (r[5] if len(r) > 5 else ''))
    out['モデルID'] = m
    # ③ 武器ID（带机体名）
    m = {}
    for r in read_rows(os.path.join(SET, 'weapon_visual_customize.csv')):
        if r and r[0].isdigit():
            note = (r[7] if len(r) > 7 else '') or (r[3] if len(r) > 3 else '')
            m.setdefault(r[0], note)
    for r in read_rows(os.path.join(SET, 'msma_mesh_customize.csv')):
        if len(r) > 1 and r[1].isdigit():
            m.setdefault(r[1], (r[5] if len(r) > 5 else ''))
    out['武器ID'] = m
    return out


def variants(s):
    """一个 ID 的所有候选变换（切片 / 整数运算）"""
    v = {'原样': s, '前6': s[:6], '前5': s[:5], '前7': s[:7], '前8': s[:8],
         '去尾1': s[:-1], '去尾2': s[:-2], '去头1': s[1:], '去头1前6': s[1:7], '去头2': s[2:]}
    if s.isdigit():
        n = int(s)
        v['//10'] = str(n // 10)
        v['//100'] = str(n // 100)
        v['//1000'] = str(n // 1000)
        v['(n-1)//10'] = str((n - 1) // 10)
    return v


def main():
    name, page = wiki_index()
    ws = set(name) | set(page)
    print('wiki 机体序号：%d 个（有页面 %d，有名 %d）' % (len(ws), len(page), len(name)))
    lens = {}
    for x in ws:
        lens[len(x)] = lens.get(len(x), 0) + 1
    print('   位数分布：', dict(sorted(lens.items())))
    print('   样例：', sorted(ws)[:8])
    print()

    for label, m in local_sets().items():
        ids = list(m)
        print('=' * 66)
        print('%s：%d 个（样例如 %s）' % (label, len(ids), ids[:3]))
        score = {}
        for s in ids:
            for k, v in variants(s).items():
                if v in ws:
                    score[k] = score.get(k, 0) + 1
        if not score:
            print('   ⚠️ 所有候选变换 **0 命中**')
        else:
            for k, n in sorted(score.items(), key=lambda x: -x[1]):
                print('   ✅ 变换 %-10s 命中 %d / %d' % (k, n, len(ids)))
            best = max(score, key=score.get)
            print('   ⇒ 最佳变换：%s' % best)
            cnt = 0
            for s in ids:
                v = variants(s).get(best)
                if v in ws:
                    if cnt < 12:
                        nm = name.get(v) or page.get(v) or ''
                        print('        %s → %s  ⇒ %s  ｜本地名：%s' % (s, v, nm, m[s][:34]))
                    cnt += 1
        print()

    # 顺带看看：練度ID 与 モデルID 的关系
    lk = list(local_sets()['練度ID'])
    mid = list(local_sets()['モデルID'])
    print('== 練度ID(7位) 与 モデルID(9位) 是否同源？ ==')
    print('   練度ID 前4位分布：', sorted({x[:4] for x in lk})[:14])
    print('   モデルID 前4位分布：', sorted({x[:4] for x in mid})[:14])
    return 0


if __name__ == '__main__':
    sys.exit(main())
