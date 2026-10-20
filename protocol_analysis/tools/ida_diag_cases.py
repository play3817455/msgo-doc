# -*- coding: utf-8 -*-
"""
ida_diag_cases.py —— S→C 分发器「case 块 ↔ opcode ↔ 名字」三方对照诊断。

用途：回答“解出的 case 数 ≠ 名字数”时，差额究竟是什么：
  * alias  : 多个 opcode 映射到同一个 case 块（同一实现服务多条命令）
  * noname : 有 case 块但块内没有任何命令名字符串（无名 case）
  * orphan_names : 有名字但不在任何 case 块区间内（归属存疑）

运行：IDA MCP 的 py_exec_file
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EXTRACTOR = os.path.join(HERE, 'ida_extract_commands.py')

# 以“库”的方式载入提取器：去掉末尾的 main() 调用，避免重跑整轮提取
_src = open(EXTRACTOR, encoding='utf-8').read()
_src = _src.replace('\nmain()\n', '\n')
ns = {}
exec(compile(_src, EXTRACTOR, 'exec'), ns)

import idaapi  # noqa: E402
import idautils  # noqa: E402
import idc  # noqa: E402

resolve_case_map = ns['resolve_case_map']
collect_names = ns['collect_names']
attach_funcs = ns['attach_funcs']
func_of = ns['func_of']
func_end = ns['func_end']

DISPATCHERS = [(0xB03D30, 'auth'), (0xB0CC20, 'battle'), (0xB51930, 'lounge')]


def main():
    names = collect_names()
    by_func = attach_funcs(names)

    for f, proto in DISPATCHERS:
        items = by_func.get(f, [])
        fend = func_end(f)
        cmap, nodes, tables, drops = resolve_case_map(f, fend)
        # 反向：块 -> [opcode]
        blocks = {}
        for op, blk in cmap.items():
            blocks.setdefault(blk, []).append(op)
        starts = sorted(blocks)

        # 每个名字的 xref（限本函数内）
        nlist = []
        for it in items:
            for x in idautils.XrefsTo(it['str_ea']):
                if func_of(x.frm) == f:
                    nlist.append((x.frm, it['name'], it['str_ea']))
                    break
        nlist.sort()

        print('=' * 78)
        print('%-7s fn=%s  cases=%d  names=%d  tables=%d'
              % (proto, hex(f), len(cmap), len(items), len(tables)))
        print('  case 块数=%d' % len(starts))
        if drops:
            print('  [dropped] 被判为伪 case 并剔除：%s'
                  % [(hex(d['opcode']), d['ptr']) for d in drops])

        def owner_of(addr):
            own = None
            for s in starts:
                if s <= addr:
                    own = s
                else:
                    break
            return own

        alias = [(b, sorted(ops)) for b, ops in blocks.items() if len(ops) > 1]
        print('  [alias] 多 opcode 共用一个 case 块：%d 处' % len(alias))
        for b, ops in sorted(alias):
            print('      block %s <- opcodes %s' % (hex(b), [hex(o) for o in ops]))

        # 无名块
        named_blocks = {}
        orphan_names = []
        for xr, nm, sea in nlist:
            own = owner_of(xr)
            if own is None:
                orphan_names.append((hex(xr), nm))
                continue
            named_blocks.setdefault(own, []).append(nm)
        noname = [b for b in starts if b not in named_blocks]
        print('  [noname] 块内无命令名字符串：%d 处' % len(noname))
        for b in noname:
            nxt = fend
            for s in starts:
                if s > b:
                    nxt = s
                    break
            ops = sorted(blocks[b])
            print('      block %s..%s  opcodes=%s  size=%d'
                  % (hex(b), hex(nxt), [hex(o) for o in ops], nxt - b))
        print('  [orphan_names] 名字不属于任何 case 块：%d 处 %s'
              % (len(orphan_names), orphan_names[:6]))
        multi = [(hex(b), v) for b, v in sorted(named_blocks.items()) if len(v) > 1]
        print('  [multi-name] 一个块内有多个名字：%d 处 %s' % (len(multi), multi[:6]))

        # 每个块的 opcode 归属（仅打印无名的块所属 opcode）
        print('  case 数 - 块数 = %d - %d = %d ; 名字数 - 已归属名字数 = %d'
              % (len(cmap), len(starts), len(cmap) - len(starts),
                 len(nlist) - sum(len(v) for v in named_blocks.values())))
        print('')


main()
