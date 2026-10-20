# -*- coding: utf-8 -*-
"""_dump_range.py —— 临时：把 shop_lineup_r(0x99A0) case 的**完整汇编**打出来
（`dump_case_calls.py` 只打 call/cmp/mov-imm ✗ ⇒ 看不到"数组接在哪个偏移" ✓）

范围取 case 自身那一截：B6E1B0..B6E2E0（含 500 次循环与容器写入 ✓）
"""
import io
import sys

import idc
import ida_lines  # noqa: F401
import idaapi

if hasattr(sys.stdout, 'buffer'):  # ★IDA MCP 里 stdout 是 StringIO ⇒ 没有 buffer ✓
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

START = 0xB6E240
END = 0xB6E2A0


def plain(ea):
    s = idc.generate_disasm_line(ea, 0)
    return ida_lines.tag_remove(s) if s else ''


def main():
    ea = START
    n = 0
    while ea != idc.BADADDR and ea < END and n < MAX_INSN:
        print('%06X  %s' % (ea, plain(ea)))
        n += 1
        nx = idc.next_head(ea, END)
        # ★★★2026-09-17 血泪：`next_head` 在"非指令地址"上会**返回同一个 ea**
        #   ⇒ 原来的 `while ea < END` 会**死循环**，把 IDA 卡死（MCP 全体超时 ✗✗）
        #   ⇒ 必须"**没前进就退出**" + 次数上限（双保险 ✓）
        if nx == ea or nx == idc.BADADDR:
            print('  ⚠️ 停在 %06X（next_head 未前进 ⇒ 不是指令 ✓ 防死循环）' % ea)
            break
        ea = nx
    print('（共 %d 条指令）' % n)
    return 0


if __name__ == '__main__':
    sys.exit(main())
