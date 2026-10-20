# -*- coding: utf-8 -*-
"""在 IDA 侧执行：把「登录链文档引用过的全部函数」导出成伪代码 + 核心汇编。

用法（二选一）：
  1) IDA 菜单 File > Script file... 选中本文件；
  2) 或把本文件内容整段粘贴进 IDA 的 Python 控制台 / 经 ida-pro-mcp 的 py_eval 执行。

前置：
  reverse-login-chain/formats/_func_refs.json
  = 从节点/格式/主题文档里扫出的全部 sub_XXXXXX 地址（JSON 数组，元素为十进制或十六进制整数）。
  生成方式见 asm/README.md §一。

输出（写入 reverse-login-chain/asm/）：
  登录链-伪代码-NN.md    每批 40 个函数（VA/大小/调用者 + Hex-Rays 伪代码）
  登录链-汇编核心-NN.md  每批 25 个函数（= nodes/*.md 引用过的函数）的完整汇编
  _index.json            机读索引
"""
import io
import json
import os
import re
import glob

import idc
import idautils

try:
    import ida_hexrays
except Exception:                                   # 没有 Hex-Rays 时退化为只导汇编
    ida_hexrays = None

ROOT = r'f:/9ymsgo/9you'
OUT = ROOT + r'/reverse-login-chain/asm'
os.makedirs(OUT, exist_ok=True)

refs = json.load(io.open(ROOT + r'/reverse-login-chain/formats/_func_refs.json', encoding='utf-8'))
funcs = sorted(set(f for f in (idc.get_func_attr(a, idc.FUNCATTR_START) for a in refs) if f))

# 核心集合 = nodes/*.md 里引用过的函数（这些额外导出汇编）
core = set()
for p in glob.glob(ROOT + r'/reverse-login-chain/nodes/*.md'):
    try:
        t = io.open(p, encoding='utf-8', errors='replace').read()
    except Exception:
        continue
    for m in re.finditer(r'sub_([0-9A-Fa-f]{6})', t):
        f = idc.get_func_attr(int(m.group(1), 16), idc.FUNCATTR_START)
        if f:
            core.add(f)
core = sorted(core)


def pseudocode(f):
    if ida_hexrays is None:
        return None
    try:
        cf = ida_hexrays.decompile(f)
        return str(cf) if cf else None
    except Exception:
        return None


def callers(f):
    out = []
    for r in idautils.CodeRefsTo(f, 0):
        n = idc.get_func_name(r)
        if n:
            out.append(n)
    return sorted(set(out))


CH = 40                                             # 每批函数数（伪代码）
idx = []
for ci in range(0, len(funcs), CH):
    chunk = funcs[ci:ci + CH]
    L = ['# 登录链伪代码导出 · 第 %d 批（共 %d 批，每批 %d 个函数）' % (
        ci // CH + 1, (len(funcs) + CH - 1) // CH, CH), '',
        '> 来源：IDA Hex-Rays（IDB `unpacked/GundamOnline_CHINA_v15.exe.i64`，VA 基址 0x400000）。',
        '> 函数集合 = 本项目节点/格式/主题文档里出现过的全部 `sub_XXXXXX`。', '']
    for f in chunk:
        name = idc.get_func_name(f)
        size = idc.get_func_attr(f, idc.FUNCATTR_END) - f
        cs = callers(f)
        L.append('## `%s`  (VA 0x%X ｜ %d B ｜ 调用者 %d)' % (name, f, size, len(cs)))
        L.append('')
        if cs:
            L.append('- 调用者：%s' % (', '.join('`%s`' % c for c in cs[:12]) + (' …' if len(cs) > 12 else '')))
        code = pseudocode(f)
        if code:
            L += ['```c', code, '```']
        else:
            L.append('> ⚠️ Hex-Rays 反编译不可用（或非函数），汇编见 `登录链-汇编核心.md` 对应小节。')
        L.append('')
        idx.append({'fn': name, 'va': hex(f), 'size': size, 'callers': len(cs),
                    'file': '登录链-伪代码-%02d.md' % (ci // CH + 1), 'pseudo': bool(code)})
    io.open(os.path.join(OUT, '登录链-伪代码-%02d.md' % (ci // CH + 1)), 'w', encoding='utf-8').write('\n'.join(L))

CH2 = 25                                            # 每批函数数（汇编）
for ci in range(0, len(core), CH2):
    chunk = core[ci:ci + CH2]
    L = ['# 登录链汇编导出（核心）· 第 %d 批' % (ci // CH2 + 1), '',
         '> 集合 = `reverse-login-chain/nodes/*.md` 中引用过的函数。', '']
    for f in chunk:
        L += ['## `%s`  (VA 0x%X)' % (idc.get_func_name(f), f), '', '```asm']
        ea, end, n = f, idc.get_func_attr(f, idc.FUNCATTR_END), 0
        while ea < end and ea != idc.BADADDR and n < 4000:
            L.append('%08X  %s' % (ea, idc.generate_disasm_line(ea, 0)))
            ea = idc.next_head(ea)
            n += 1
        L += ['```', '']
    io.open(os.path.join(OUT, '登录链-汇编核心-%02d.md' % (ci // CH2 + 1)), 'w', encoding='utf-8').write('\n'.join(L))

io.open(os.path.join(OUT, '_index.json'), 'w', encoding='utf-8').write(
    json.dumps({'functions': idx, 'core': [hex(f) for f in core]}, ensure_ascii=False, indent=0))
print('funcs %d / core %d / pseudo files %d / asm files %d' % (
    len(funcs), len(core), (len(funcs) + CH - 1) // CH, (len(core) + CH2 - 1) // CH2))
