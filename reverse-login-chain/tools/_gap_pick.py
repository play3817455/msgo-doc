# -*- coding: utf-8 -*-
"""_gap_pick.py —— 临时：把"推送缺口"里指定几条的 **case 入口** 写进 `_case_addrs.txt` ✓

用法：`python reverse-login-chain/tools/_gap_pick.py pilot_level_update pilot_lvpt_update …`
（名字用清单里的 S→C 名 ✓；入口从 `formats/_lounge_recv_idmap.json` 取 ✓）
"""
import io
import json
import os
import sys

if hasattr(sys.stdout, 'buffer'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
IDMAP = os.path.join(ROOT, 'reverse-login-chain', 'formats', '_lounge_recv_idmap.json')
OUT = os.path.join(ROOT, 'reverse-login-chain', 'tools', '_case_addrs.txt')


def main():
    names = sys.argv[1:]
    if not names:
        print('用法：_gap_pick.py <推送名…>')
        return 1
    m = json.load(open(IDMAP, encoding='utf-8'))
    lines, miss = [], []
    for n in names:
        e = m.get(n)
        if not e:
            miss.append(n)
            continue
        lines.append('%s  # %s %s' % (e['entry'].upper(), e['id_hex'], n))
        print('   %-40s %-8s entry=%s' % (n, e['id_hex'], e['entry']))
    for n in miss:
        print('   %-40s ✗ 不在 recv idmap 里（可能不是客户端 case）' % n)
    open(OUT, 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
    print('已写 %s（%d 条 ✓）' % (OUT, len(lines)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
