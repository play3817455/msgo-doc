# -*- coding: utf-8 -*-
"""
build_index.py —— 由 _meta/commands_raw.json 生成 INDEX 与命令文件夹骨架。

用法：
    python protocol_analysis\\tools\\build_index.py            # 只补齐缺失的文件
    python protocol_analysis\\tools\\build_index.py --force    # 强制重写全部骨架文件

约定：
  * INDEX-命令总表.md 每次都重写（它是生成物）。
  * 命令文件夹内的 README.md / fields.csv / asm.md / notes.md
    默认**只在缺失时创建**，避免冲掉已有人工分析成果。
  * INDEX 的状态列从各命令 README.md 的 `> 状态：\\`XXX\\`` 行解析，缺失视为 TODO。
"""

import argparse
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
META = os.path.join(ROOT, '_meta')
RAW = os.path.join(META, 'commands_raw.json')
CMDS = os.path.join(ROOT, 'commands')
INDEX = os.path.join(ROOT, 'INDEX-命令总表.md')
TPL = os.path.join(ROOT, '_template-命令文件夹')

STATUS_RE = re.compile(r'状态：`([A-Z]+)`')
DIR_FULL = {'SC': '服务端 → 客户端（recv）', 'CS': '客户端 → 服务端（send）'}


def proto_short(c):
    return (c.get('proto') or '?').replace('_client', '')


def folder_name(c):
    op = c.get('opcode_hex') or '0x----'
    return '%s-%s-%s-%s' % (c['direction'], op, proto_short(c), c['name'])


def load_raw():
    with open(RAW, encoding='utf-8') as fp:
        return json.load(fp)


def read_status(folder):
    p = os.path.join(CMDS, folder, 'README.md')
    if not os.path.exists(p):
        return 'TODO'
    with open(p, encoding='utf-8') as fp:
        head = fp.read(4000)
    m = STATUS_RE.search(head)
    return m.group(1) if m else 'TODO'


def code_loc(c):
    if c['direction'] == 'SC':
        fn = c.get('handler_name') or '?'
        loc = '%s @ `%s`' % (fn, c.get('handler_fn'))
        if c.get('case_start'):
            loc += '　块 `%s`..`%s`' % (c['case_start'], c.get('case_end'))
        if c.get('dispatch'):
            loc = '**%s**（默认分支：%s @ `%s`）' % (loc, c.get('caller_fn'), c.get('caller_site'))
        return loc
    fn = c.get('send_fn_name') or '?'
    return '%s @ `%s`（`%s`..`%s`）' % (fn, c.get('send_fn'),
                                        c.get('fn_start'), c.get('fn_end'))


def evidence_line(c):
    if c['direction'] == 'SC':
        return '`%s`' % c.get('namestr_xref', '?')
    return '`%s`' % c.get('opcode_insn', '?')



def len_cell(c):
    if c['direction'] == 'CS' and c.get('declared_total_len') is not None:
        return '容量 `%s`' % c['declared_total_len_hex']
    return '-'


def make_index(rows_sc, rows_cs):
    out = []
    out.append('# INDEX —— 命令总表\n')
    out.append('> 本文件由 `tools/build_index.py` 生成，**不要手工编辑**；新增/修订命令请改 `_meta/commands_raw.json` 后重跑。\n')
    out.append('> 每条命令对应 `commands/<方向>-<opcode>-<协议类>-<命令名>/` 文件夹，产物 4 件套见规范 §2。\n')
    out.append('> 同一命令名可能出现在多个协议类（同一 opcode，如握手/CPF/系统消息），故文件夹名含协议类短名。\n')
    out.append('')
    out.append('## 0. 概览\n')
    out.append('| 项 | 数量 |')
    out.append('|---|---|')
    out.append('| S→C 命令（`recv_*`） | %d |' % len(rows_sc))
    out.append('| C→S 命令（`send_*`） | %d |' % len(rows_cs))
    out.append('| 合计 | %d |' % (len(rows_sc) + len(rows_cs)))
    done = sum(1 for r in rows_sc + rows_cs if r['status'] == 'DONE')
    wip = sum(1 for r in rows_sc + rows_cs if r['status'] == 'WIP')
    draft = sum(1 for r in rows_sc + rows_cs if r['status'] == 'DRAFT')
    todo = len(rows_sc) + len(rows_cs) - done - wip - draft
    out.append('| 状态 DONE / WIP / DRAFT / TODO | %d / %d / %d / %d |' % (done, wip, draft, todo))
    out.append('')
    out.append('状态：`TODO` 未开始 / `DRAFT` 机器草案（`draft-wire.md` 已生成，待人工补「含义」、未过质量门）'
               ' / `WIP` 人工进行中 / `DONE` 过质量门（规范 §10）/ `BLOCKED` 阻塞。')
    out.append('')

    out.append('## 1. S→C 命令索引（服务端 → 客户端，共 %d 条）\n' % len(rows_sc))
    out.append('| # | opcode | 协议类 | 命令名 | 代码位置（处理块） | 线长 | 状态 | 文件夹 |')
    out.append('|---|---|---|---|---|---|---|---|')
    for i, r in enumerate(rows_sc, 1):
        out.append('| %d | `%s` | `%s` | `%s` | %s | %s | %s | [%s](commands/%s/) |'
                   % (i, r['opcode_hex'], r['proto'], r['name'], code_loc(r),
                      len_cell(r), r['status'], r['folder'], r['folder']))
    out.append('')

    out.append('## 2. C→S 命令索引（客户端 → 服务端，共 %d 条）\n' % len(rows_cs))
    out.append('| # | opcode | 协议类 | 命令名 | 代码位置（组包函数） | 声明容量 | 状态 | 文件夹 |')
    out.append('|---|---|---|---|---|---|---|---|')
    for i, r in enumerate(rows_cs, 1):
        out.append('| %d | `%s` | `%s` | `%s` | %s | %s | %s | [%s](commands/%s/) |'
                   % (i, r['opcode_hex'], r['proto'], r['name'], code_loc(r),
                      len_cell(r), r['status'], r['folder'], r['folder']))
    out.append('')

    out.append('## 3. 异常与遗留\n')
    out.append('| 项 | 说明 |')
    out.append('|---|---|')
    out.append('| 未解出 opcode 的 S→C | %d 条 |' % sum(1 for r in rows_sc if not r['opcode_hex']))
    n_orphan = sum(1 for r in rows_sc if r.get('dispatch'))
    out.append('| 不经分发器的 recv | %d 条（由分发器默认分支调用；opcode 取自处理函数内 `cmp <16位寄存器>, IMM`） |' % n_orphan)
    out.append('| 被剔除的伪 case | 见 `_meta/命令发现方法.md` §6.1 |')
    out.append('| 跳转表形态的 case | 见 `_meta/环境与工具约定.md` §4 |')
    out.append('')
    return '\n'.join(out)


def render(tpl_text, c):
    rep = {
        '{{DIR}}': c['direction'],
        '{{DIR_FULL}}': DIR_FULL[c['direction']],
        '{{OPCODE}}': c['opcode_hex'] or '?',
        '{{OPCODE_EVIDENCE}}': evidence_line(c),
        '{{PROTO}}': c['proto'],
        '{{NAME}}': c['name'],
        '{{NAMESTR}}': (c.get('expr') or '').strip(),
        '{{NAMESTR_EA}}': c.get('namestr_ea', '?'),
        '{{CODE_LOC}}': code_loc(c),
        '{{CASE_START}}': c.get('case_start', '-') or '-',
        '{{CASE_END}}': c.get('case_end', '-') or '-',
    }
    for k, v in rep.items():
        tpl_text = tpl_text.replace(k, v)
    return tpl_text


def scaffold(c, force=False):
    folder = os.path.join(CMDS, c['folder'])
    os.makedirs(folder, exist_ok=True)
    created = 0
    for fname in ('README.md', 'fields.csv', 'asm.md', 'notes.md'):
        dst = os.path.join(folder, fname)
        if os.path.exists(dst) and not force:
            continue
        tplp = os.path.join(TPL, fname)
        with open(tplp, encoding='utf-8') as fp:
            tpl_text = fp.read()
        with open(dst, 'w', encoding='utf-8', newline='') as fp:
            fp.write(render(tpl_text, c))
        created += 1
    return created


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--force', action='store_true', help='覆盖已存在的骨架文件')
    args = ap.parse_args()

    data = load_raw()
    cmds = data['commands']
    for c in cmds:
        c['folder'] = folder_name(c)
    sc = [c for c in cmds if c['direction'] == 'SC']
    cs = [c for c in cmds if c['direction'] == 'CS']
    sc.sort(key=lambda c: (c['opcode'] is None, c['opcode'] or 0, c['name']))
    cs.sort(key=lambda c: (c['opcode'] is None, c['opcode'] or 0, c['name']))

    n = 0
    for c in sc + cs:
        c['status'] = read_status(c['folder'])
        n += scaffold(c, args.force)

    with open(INDEX, 'w', encoding='utf-8', newline='') as fp:
        fp.write(make_index(sc, cs))

    print('[OK] 命令 %d 条（S->C %d / C->S %d）' % (len(cmds), len(sc), len(cs)))
    print('[OK] 新建骨架文件 %d 个（已有文件默认不动）' % n)
    print('[OK] INDEX -> %s' % INDEX)


if __name__ == '__main__':
    main()
