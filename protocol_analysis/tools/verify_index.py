# -*- coding: utf-8 -*-
"""
verify_index.py —— 校验 INDEX / 命令文件夹 / commands_raw.json 三者一致。

用法：python protocol_analysis\\tools\\verify_index.py

检查项：
  1. JSON 计数 与 INDEX 概览 一致；
  2. 每条命令的文件夹存在，且 4 件套齐全；
  3. 每个文件夹名可从 INDEX 找到（无孤儿文件夹）；
  4. 同方向内 opcode 不重复（重复即提示可能归属错误）；
  5. 未解出 opcode 的命令列出（不视为失败，但要可见）；
  6. 各命令 README.md 的状态取值合法。

退出码：0 = 全部通过；1 = 存在不一致。
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RAW = os.path.join(ROOT, '_meta', 'commands_raw.json')
CMDS = os.path.join(ROOT, 'commands')
INDEX = os.path.join(ROOT, 'INDEX-命令总表.md')
FILES = ('README.md', 'fields.csv', 'asm.md', 'notes.md')
OK_STATUS = {'TODO', 'DRAFT', 'WIP', 'DONE', 'BLOCKED'}
STATUS_RE = re.compile(r'状态：`([A-Z]+)`')


def proto_short(c):
    return (c.get('proto') or '?').replace('_client', '')


def folder_name(c):
    op = c.get('opcode_hex') or '0x----'
    return '%s-%s-%s-%s' % (c['direction'], op, proto_short(c), c['name'])


def main():
    problems = []
    if not os.path.exists(RAW):
        print('[FAIL] 缺少 %s' % RAW)
        return 1
    with open(RAW, encoding='utf-8') as fp:
        data = json.load(fp)
    cmds = data['commands']
    sc = [c for c in cmds if c['direction'] == 'SC']
    cs = [c for c in cmds if c['direction'] == 'CS']
    print('[i] JSON：S->C %d / C->S %d / 合计 %d' % (len(sc), len(cs), len(cmds)))

    # 1. INDEX 概览
    if not os.path.exists(INDEX):
        problems.append('缺少 INDEX-命令总表.md（先跑 build_index.py）')
    else:
        with open(INDEX, encoding='utf-8') as fp:
            idx = fp.read()
        m = re.search(r'\| 合计 \| (\d+) \|', idx)
        if not m:
            problems.append('INDEX 缺少「合计」行')
        elif int(m.group(1)) != len(cmds):
            problems.append('INDEX 合计 %s != JSON %d' % (m.group(1), len(cmds)))

    # 2. 文件夹与 4 件套
    missing_dir, missing_file = [], []
    for c in cmds:
        d = os.path.join(CMDS, folder_name(c))
        if not os.path.isdir(d):
            missing_dir.append(folder_name(c))
            continue
        for f in FILES:
            if not os.path.exists(os.path.join(d, f)):
                missing_file.append('%s/%s' % (folder_name(c), f))
    if missing_dir:
        problems.append('缺少文件夹 %d 个（示例：%s）' % (len(missing_dir), missing_dir[:3]))
    if missing_file:
        problems.append('缺少文件 %d 个（示例：%s）' % (len(missing_file), missing_file[:3]))

    # 3. 孤儿文件夹
    known = set(folder_name(c) for c in cmds)
    orphan = []
    if os.path.isdir(CMDS):
        for name in sorted(os.listdir(CMDS)):
            if os.path.isdir(os.path.join(CMDS, name)) and name not in known:
                orphan.append(name)
    if orphan:
        problems.append('多余文件夹 %d 个（示例：%s）' % (len(orphan), orphan[:3]))

    # 4. opcode 重复（同一协议类内重复才是真问题；跨协议类共享同名命令是正常的）
    for tag, rows in (('S->C', sc), ('C->S', cs)):
        seen = {}
        for c in rows:
            if not c['opcode_hex']:
                continue
            seen.setdefault((c['proto'], c['opcode_hex']), []).append(c['name'])
        dup = {k: v for k, v in seen.items() if len(v) > 1}
        if dup:
            problems.append('%s 同协议类内 opcode 重复 %d 组（示例：%s）' % (tag, len(dup), list(dup.items())[:3]))
        share = {}
        for c in rows:
            if not c['opcode_hex']:
                continue
            share.setdefault(c['opcode_hex'], set()).add(c['proto'])
        n_share = len([k for k, v in share.items() if len(v) > 1])
        if n_share:
            print('[i] %s 跨协议类共享 opcode：%d 个（属正常，如握手/CPF/系统消息）' % (tag, n_share))

    # 5. 未解出 opcode
    no_op = [c for c in cmds if not c['opcode_hex']]
    print('[i] 未解出 opcode：%d 条%s' % (len(no_op), ('（%s）' % [c['name'] for c in no_op][:5]) if no_op else ''))

    # 6. 状态合法性
    bad_status = []
    for c in cmds:
        p = os.path.join(CMDS, folder_name(c), 'README.md')
        if not os.path.exists(p):
            continue
        with open(p, encoding='utf-8') as fp:
            head = fp.read(4000)
        m = STATUS_RE.search(head)
        st = m.group(1) if m else 'TODO'
        if st not in OK_STATUS:
            bad_status.append('%s=%s' % (folder_name(c), st))
    if bad_status:
        problems.append('非法状态 %d 个（示例：%s）' % (len(bad_status), bad_status[:3]))

    print('')
    if problems:
        for p in problems:
            print('[FAIL] %s' % p)
        return 1
    print('[PASS] INDEX / 文件夹 / JSON 三者一致。')
    return 0


if __name__ == '__main__':
    sys.exit(main())
