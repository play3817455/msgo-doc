# -*- coding: utf-8 -*-
"""由 IDA 侧导出的 `enums.json` + `tables_spec.json` 生成《枚举表.md》。

`enums.json` 结构（IDA py_eval 生成）：
  { "<转换函数>": { "fn":…, "usedby":[{"seq","id","file","col"}…],
                    "shape": "table" | "cmp-chain",
                    "table": [[名, 值], …],        # shape=table
                    "lits":  [字符串, …],           # shape=cmp-chain
                    "consts":[数值, …] } }
用法： python gen_enum_spec.py
"""
import io
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def load(name):
    with io.open(os.path.join(HERE, name), encoding='utf-8') as f:
        return json.load(f)


def main():
    enums = load('enums.json')
    spec = load('tables_spec.json')
    byid = {s['tableId']: s for s in spec}
    # ★ 枚举列 ↔ 转换函数：优先用 IDA 侧按【全局代码顺序】重算过的 _enum_conv.json（列号已是解析值）
    enumcols = {}
    for s in spec:
        enumcols[s['tableId']] = [c for c in (s.get('cols') or []) if c.get('type') == 'enum']
    conv = None
    try:
        conv = load('_enum_conv.json')
    except Exception:
        conv = None
    use = {}
    used_override = {}
    if conv:
        for fn, lst in conv.items():
            used_override[fn] = lst
            for u in lst:
                use[(u['id'], u['col'])] = fn
    else:
        for fn, r in enums.items():
            cnt = {}
            for u in r.get('usedby') or []:
                tid = u['id']
                k = cnt.get(tid, 0)
                cnt[tid] = k + 1
                lst = enumcols.get(tid) or []
                col = lst[k]['col'] if k < len(lst) else u['col']
                use[(tid, col)] = fn
    tab = {r['fn']: r for r in enums.values() if r['shape'] == 'table'}
    chain = {r['fn']: r for r in enums.values() if r['shape'] != 'table'}

    def used_text(fn):
        lst = used_override.get(fn)
        if lst is not None:
            return ['%s（列 %s）' % (u['file'], u['col']) for u in lst]
        out = []
        for u in (enums[fn].get('usedby') or []):
            out.append('%s（列 %s）' % (u['file'] or ('id%d' % u['id']), u['col']))
        return out

    L = ['# 服务端数据表 · 枚举值表（字符串→数值，静态逆向自动导出）', '',
         '> 来源：客户端的"字符串→枚举"转换函数 + 其静态常量表（`{const char* 名; int 值}` 记录数组，值=0 结束）。',
         '> 生成：`python gen_enum_spec.py`（输入 `enums.json` / `tables_spec.json`）。', '',
         '- **表型**枚举（静态表可直接读出名↔值）：**%d 个，共 %d 条**' % (len(tab), sum(r['n'] for r in tab.values())),
         '- **比较链型**枚举（用字符串前缀/全等比较返回常量，值需按代码逐条确认）：**%d 个**' % len(chain), '',
         '★ 造表时：枚举列请写**名称字符串**（不是数字）；写错/未知名 ⇒ 转换函数返回 0 ⇒ 该列等于 0。', '',
         '---', '', '## 一、表型枚举（可直接照抄）', '']
    for fn in sorted(tab, key=lambda k: -tab[k]['n']):
        r = tab[fn]
        L.append('### `%s`（%d 条）' % (fn, r['n']))
        L.append('')
        u = used_text(fn)
        if u:
            L.append('- 被使用：' + '；'.join(u[:12]))
            L.append('')
        L.append('| 值 | 名称 | 值 | 名称 | 值 | 名称 |')
        L.append('|---|---|---|---|---|---|')
        rows = r['table']
        for i in range(0, len(rows), 3):
            cells = []
            for k in range(3):
                if i + k < len(rows):
                    cells += [str(rows[i + k][1]), '`%s`' % rows[i + k][0]]
                else:
                    cells += ['', '']
            L.append('| ' + ' | '.join(cells) + ' |')
        L.append('')
    L += ['---', '', '## 二、比较链型枚举（名称已导出，值需人工确认）', '']
    for fn in sorted(chain):
        r = chain[fn]
        L.append('### `%s`' % fn)
        L.append('')
        u = used_text(fn)
        if u:
            L.append('- 被使用：' + '；'.join(u[:12]))
        if r.get('lits'):
            L.append('- 合法字符串（写这些之一）：%s' % '、'.join('`%s`' % x for x in r['lits']))
        if r.get('consts'):
            L.append('- 代码里出现的常量：%s' % ', '.join(str(x) for x in r['consts']))
        L.append('- ⚠️ 该转换函数用 `sub_40CE20` 做**前缀/全等比较**后返回常量（或查另一张表）⇒ 名↔值需按代码逐条确认。')
        L.append('')
    L += ['---', '', '## 三、表/列 → 枚举 对照', '', '| 下载序 | 表ID | 文件 | 列号 | 枚举函数 |',
          '|---|---|---|---|---|']
    for s in spec:
        for c in s.get('cols') or []:
            if c.get('type') == 'enum':
                fn = use.get((s['tableId'], c['col']), '?')
                L.append('| %d | %d | `%s` | %s | `%s` |' % (
                    s['downloadIndex'], s['tableId'], s['fileName'] or s['defName'], c['col'], fn))
    L.append('')
    with io.open(os.path.join(HERE, '枚举表.md'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(L))
    print('OK: table-enums %d (%d entries), cmp-chain %d, enum cols %d' % (
        len(tab), sum(r['n'] for r in tab.values()), len(chain),
        sum(1 for s in spec for c in (s.get('cols') or []) if c.get('type') == 'enum')))


if __name__ == '__main__':
    main()
