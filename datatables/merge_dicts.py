# -*- coding: utf-8 -*-
"""merge_dicts.py —— 把三份「代号→机体名」字典合并成一份，写回 match_model_names.py 的 CODE_NAME。

来源（三份平行字典，本轮合并为一份）：
  · match_model_names.py  CODE_NAME   （代号→日文名，精确匹配口径）
  · pair_codes.py        CODE2KEY    （代号→日文名关键词，子串匹配口径）
  · pair_codes2.py       KEY         （代号→名册候选，列表）
合并口径：统一解析成 **favms_ok_list.csv 名册里的精确日文名**（match_model_names 用精确名做 byname）。
用法：python datatables/merge_dicts.py [--apply]  （--apply 才写回 match_model_names.py）
"""
import ast
import io
import os
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FAVMS = os.path.join(ROOT, 'unpackdat', 'settings', 'favms_ok_list.csv')
TARGET = os.path.join(HERE, 'match_model_names.py')


def norm(s):
    out = []
    for ch in s or '':
        o = ord(ch)
        out.append(chr(o - 0xFEE0) if 0xFF01 <= o <= 0xFF5E else ch)
    t = ''.join(out).replace('（', '(').replace('）', ')')
    for x in (' ', '　', '・', '･', '.', '·', '-', '−'):
        t = t.replace(x, '')
    return t.lower()


def load_dict(path, name):
    src = open(path, encoding='utf-8').read()
    tree = ast.parse(src)
    for n in tree.body:
        if isinstance(n, ast.Assign) and any(getattr(t, 'id', '') == name for t in n.targets):
            return ast.literal_eval(n.value)
    return {}


def flatten(d):
    """dict → {code: [候选名...]}（值可能是 str 或 list）"""
    out = {}
    for k, v in (d or {}).items():
        out[k] = v if isinstance(v, (list, tuple)) else [v]
    return out


def main():
    apply = '--apply' in sys.argv
    cn = flatten(load_dict(TARGET, 'CODE_NAME'))
    c2 = flatten(load_dict(os.path.join(HERE, 'pair_codes.py'), 'CODE2KEY'))
    k2 = flatten(load_dict(os.path.join(HERE, 'pair_codes2.py'), 'KEY'))
    mo = flatten(load_dict(os.path.join(HERE, '_more_codes.py'), 'MORE'))

    # 名册精确名（favms：練度ID,日文名）
    roster = []
    for l in open(FAVMS, encoding='utf-8', errors='replace').read().splitlines():
        f = [x.strip() for x in l.split(',')]
        if f and re.fullmatch(r'\d{7}', f[0]):
            roster.append(f[1] if len(f) > 1 else '')
    rnorm = {}
    for nm in roster:
        rnorm.setdefault(norm(nm), []).append(nm)

    merged = {}
    for code, cands in [*cn.items(), *c2.items(), *k2.items(), *mo.items()]:
        merged.setdefault(code, [])
        for c in cands:
            if c and c not in merged[code]:
                merged[code].append(c)

    # 解析到精确名
    resolved, unresolved, conflict = {}, [], {}
    for code, cands in merged.items():
        hit = None
        for c in cands:
            nc = norm(c)
            if nc in rnorm:
                hit = sorted(rnorm[nc], key=len)[0]
                break
            sub = [nm for nm in roster if nc in norm(nm)]
            if sub:
                hit = sorted(sub, key=len)[0]
                break
        if hit:
            if code in resolved and resolved[code] != hit:
                conflict[code] = (resolved[code], hit)
            resolved[code] = hit
        else:
            unresolved.append((code, cands))

    print('三份字典合并：原始 code 数 %d（CODE_NAME %d + CODE2KEY %d + KEY %d）'
          % (len(merged), len(cn), len(c2), len(k2)))
    print('解析到名册精确名：%d 个 code ｜ 未解析 %d ｜ 冲突(同名不同code) %d'
          % (len(resolved), len(unresolved), len(conflict)))
    if unresolved:
        print('  --- 未解析样例（名册里没有对应名，多半是非可玩机体）---')
        for c, v in unresolved[:18]:
            print('     %-14s %s' % (c, v))
    if conflict:
        print('  --- 冲突 ---')
        for c, v in conflict.items():
            print('     %-14s %s' % (c, v))

    if not apply:
        print('（未写回；加 --apply 生效）')
        return 0

    # 写回 match_model_names.py 的 CODE_NAME 块
    src = open(TARGET, encoding='utf-8').read()
    pat = re.compile(r'CODE_NAME = \{[^}]*?\n\}', re.S)
    items = '\n'.join("    '%s': '%s'," % (c, n) for c, n in sorted(resolved.items()))
    newblock = 'CODE_NAME = {\n%s\n}' % items
    src2, nsub = pat.subn(lambda m: newblock, src, count=1)
    if nsub != 1:
        print('✗ 未找到 CODE_NAME 块，写回失败')
        return 1
    open(TARGET, 'w', encoding='utf-8').write(src2)
    print('已写回 %s 的 CODE_NAME（%d 条）' % (os.path.basename(TARGET), len(resolved)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
