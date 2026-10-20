# -*- coding: utf-8 -*-
"""list_unmatched_codes.py —— 列出"有内部代号但还没进 CODE2KEY"的资源目录，供批量扩字典。

★不 import pair_codes（它会重包 stdout 导致 buffer 冲突）⇒ 用 ast 从源码里读 CODE2KEY。
用法：python datatables/list_unmatched_codes.py [A前缀，默认 01]
"""
import ast
import io
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))


def load_code2key():
    src = open(os.path.join(HERE, 'pair_codes.py'), encoding='utf-8').read()
    for node in ast.parse(src).body:
        if isinstance(node, ast.Assign) and any(
                getattr(t, 'id', '') == 'CODE2KEY' for t in node.targets):
            return ast.literal_eval(node.value)
    return {}


def main():
    want_a = sys.argv[1] if len(sys.argv) > 1 else '01'
    KEY = load_code2key()
    rows = [l.split(',') for l in open(os.path.join(HERE, 'names', 'chara模型代号.csv'),
                                       encoding='utf-8').read().splitlines()
            if l.strip() and not l.startswith('#')]
    todo, done = {}, 0
    for f in rows:
        if len(f) < 5 or not f[3].strip():
            continue
        a, b, c, codes, val = f[0], f[1], f[2], f[3].strip(), f[4].strip()
        if a != want_a:
            continue
        if any(cd in KEY for cd in codes.split('/')):
            done += 1
            continue
        todo.setdefault(b, []).append('%s=%s#%s' % (c, codes, val))
    total = done + sum(len(v) for v in todo.values())
    print('CODE2KEY 现有 %d 条 ｜ chara/%s/*：有代号 %d 个目录（字典已覆盖 %d，★待扩 %d）'
          % (len(KEY), want_a, total, done, total - done))
    for b in sorted(todo):
        print('\n── chara/%s/%s（%d 个待扩）' % (want_a, b, len(todo[b])))
        line = todo[b]
        for i in range(0, len(line), 4):
            print('   ' + '  '.join(line[i:i + 4]))
    return 0


if __name__ == '__main__':
    sys.exit(main())
