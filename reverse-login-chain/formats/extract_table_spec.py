# -*- coding: utf-8 -*-
"""把 IDA 侧导出的 JSON 合成《服务端数据表·列规格》。

输入（均由 IDA Pro MCP 的 py_eval 生成，方法链见 topics/16 §一/§六）：
  _idmap.json          : download_list.csv 行序 → 表ID（客户端 sub_575FF0 的常量表 @0xD783E0）
  _tables_extract.json : 表ID → 类名/全局/ctor/派生vtable/逐列读取函数/列定义
  ../unpackdat/settings/download_list.csv : 行序 → (定义名, 文件名)

输出：
  数据表-80表列规格.md   （人读）
  tables_spec.json       （机读，供造表脚本消费）

用法： python extract_table_spec.py
"""
import io
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
DL = os.path.join(ROOT, 'unpackdat', 'settings', 'download_list.csv')

TYPE_ORDER = ['u32', 'i64', 'float', 'str', 'enum']

# ─────────────────────────────────────────────────────────────────────────────
# ★ 人工覆写（自动提取解不出/需要展开循环的表）
#   cols 元素 = (列号表达式, 类型)；类型 ∈ u32/i64/float/str/enum
#   证据见 .codebuddy/memory/topics/16 §六 与当天日志
# ─────────────────────────────────────────────────────────────────────────────
MANUAL = {
    # AUTOEXEC：不是 CSV（autoexec_sv.cfg，脚本方言），无列定义
    0: {'className': '(autoexec 脚本，无列定义)', 'reader': None, 'cols': []},
    # CLvupMsmaTable：col0=ID，col1..9 为循环读取（且内存里做累加）
    14: {'className': 'CLvupMsmaTable', 'reader': 'sub_579D60',
         'cols': [('0', 'u32')] + [(str(i), 'u32') for i in range(1, 10)]},
    # CCommanderSupportTable：只读 3/4/7/8/0x0B(u32) 与 0x0C(float)
    29: {'className': 'CCommanderSupportTable', 'reader': 'sub_574300',
         'cols': [('3', 'u32'), ('4', 'u32'), ('7', 'u32'), ('8', 'u32'),
                  ('0x0B', 'u32'), ('0x0C', 'float')]},
    # CBGMTable：col0/1/2/4/5/6=u32，col3=字符串
    39: {'className': 'CBGMTable', 'reader': 'sub_570560',
         'cols': [('0', 'u32'), ('1', 'u32'), ('2', 'u32'), ('3', 'str'),
                  ('4', 'u32'), ('5', 'u32'), ('6', 'u32')]},
    # CMSMAModuleTable：col0=ID，随后 v3=2 起、步长 2、共 10 个（2,4,...,20）
    53: {'className': 'CMSMAModuleTable', 'reader': 'sub_57EA90',
         'cols': [('0', 'u32')] + [(str(i), 'u32') for i in range(2, 22, 2)]},
    # CScoreConfigCategoryTable：行回调 sub_A55530 读 col0(str 主键)，
    #   本类 vt[0]=sub_58DDB0 读 col1（枚举，经 sub_5812E0）
    69: {'className': 'CScoreConfigCategoryTable', 'reader': 'sub_58DDB0',
         'cols': [('0', 'str'), ('1', 'enum')]},
    # CTrendDataWeaponTable：col0=ID，col1..10（循环 result+1，result=0..9）
    79: {'className': 'CTrendDataWeaponTable', 'reader': 'sub_5928E0',
         'cols': [('0', 'u32')] + [(str(i), 'u32') for i in range(1, 11)]},
    # CBuildupWeaponTable（reader sub_570880）：col0=ID；循环 10 次（v6=1..10）每轮读
    #   col v6（bool，且 ×10 存第二处）+ col (v6+10)  ⇒ 合计列 0，1..10，11..20
    40: {'className': 'CBuildupWeaponTable', 'reader': 'sub_570880',
         'cols': [('0', 'u32')]
                 + [(str(i), 'u32') for i in range(1, 11)]
                 + [(str(i), 'u32') for i in range(11, 21)]},
}


def read_download_list():
    rows = []
    with io.open(DL, encoding='utf-8-sig') as f:
        for i, line in enumerate(f):
            parts = line.rstrip('\r\n').split(',')
            if i == 0 or not parts or not parts[0].strip():
                continue
            rows.append((parts[0].strip(), parts[1].strip() if len(parts) > 1 else ''))
    return rows


def load(name):
    with io.open(os.path.join(HERE, name), encoding='utf-8') as f:
        return json.load(f)


def build():
    dl = read_download_list()
    idmap = load('_idmap.json')
    tabs = {int(t['id']): t for t in load('_tables_extract.json')}
    spec = []
    for r in idmap:
        idx, tid, deff = r['idx'], int(r['id']), r['def']
        fname = ''
        for n, fn in dl:
            if n == deff:
                fname = fn
                break
        t = tabs.get(tid, {})
        vt = (t.get('vtable') or {})
        cols = list(t.get('cols') or [])
        cls = (vt.get('name') or '').replace('??_7', '').replace('@@6B@', '')
        reader = t.get('reader')
        man = MANUAL.get(tid) or {}
        if 'cols' in man:
            cols = [{'fn': ('sub_402310' if c[1] == 'str' else 'sub_BBB4F0' if c[1] == 'enum'
                            else 'sub_BBB370'), 'type': c[1], 'col': c[0], 'resolved': True}
                    for c in man['cols']]
        if man.get('className'):
            cls = man['className']
        if man.get('reader') is not None:
            reader = man['reader']
        if man.get('dropBadCol'):
            cols = [c for c in cols if c.get('resolved')]
        bytype = {}
        for c in cols:
            bytype[c['type']] = bytype.get(c['type'], 0) + 1
        spec.append({
            'downloadIndex': idx, 'tableId': tid, 'defName': deff, 'fileName': fname,
            'className': cls, 'global': t.get('global'), 'ctor': t.get('ctor'),
            'vtable': hex(vt['addr']) if vt.get('addr') else None,
            'loaderSlot': t.get('slot'), 'reader': reader,
            'colCount': len(cols), 'types': bytype, 'cols': cols,
        })
    return spec


def write_spec(spec):
    with io.open(os.path.join(HERE, 'tables_spec.json'), 'w', encoding='utf-8') as f:
        f.write(json.dumps(spec, ensure_ascii=False, indent=1))


def write_md(spec):
    ok = [s for s in spec if s['colCount']]
    bad = [s for s in spec if not s['colCount']]
    L = ['# 服务端数据表 · 列规格（静态逆向自动导出）', '',
         '> 覆盖范围：`settings/download_list.csv` **全部 76 行**（75 个 .csv ＋ 1 个 `autoexec_sv.cfg`）',
         '> ＋ 客户端表ID 表里的其余 3 条本地表（`LVUP_MSMA` / `MSMA_MATERIAL` / `BGMPACKAGE`，不下发）。',
         '> 表ID 空间 = 80（含无效/保留），实际有装载器的是下面这 79 条。', '',
         '> 生成方式：`python extract_table_spec.py`（依赖 `_idmap.json` / `_tables_extract.json`）。',
         '> 方法链见 `.codebuddy/memory/topics/16-服务端数据表格式逆向.md §一`。',
         '> **列号一律 0-based**，与 CSV 里逗号分隔的位置一一对应；`类型` 的读法见文末"原语表"。',
         '> 逐表小节里的行是**代码的读取顺序**（≠ 列号顺序），**以"列号"列为准**。', '',
         '- 已解出列定义：**%d / %d** 张（`AUTOEXEC` 是脚本、无列定义）。' % (len(ok), len(spec)), '',
         '## 0. 总表（下载序 → 表ID → 文件 → 类名 → 逐列读取函数）', '',
         '| 下载序 | 表ID | 定义名 | 文件 | 类名 | 逐列读取 | 列数 | 类型分布 |',
         '|---|---|---|---|---|---|---|---|']
    for s in spec:
        td = ' '.join('%s×%d' % (k, s['types'][k]) for k in TYPE_ORDER if k in s['types'])
        L.append('| %d | %d | %s | `%s` | %s | %s | %s | %s |' % (
            s['downloadIndex'], s['tableId'], s['defName'], s['fileName'],
            ('`%s`' % s['className']) if s['className'] else '?',
            ('`%s`' % s['reader']) if s['reader'] else '—',
            s['colCount'] or '—', td or '—'))
    L += ['', '---', '', '## 1. 逐表列定义', '']
    for s in spec:
        L.append('### %d `%s`（表ID %d，%s）' % (s['downloadIndex'], s['fileName'] or s['defName'],
                                                 s['tableId'], s['defName']))
        L.append('')
        if not s['cols']:
            L.append('- 无需列定义（%s）' % (s['className'] or '?'))
            L.append('')
            continue
        L.append('- 类名 `%s` ｜ 全局 `%s` ｜ ctor `%s` ｜ 派生 vtable `%s` ｜ 逐列读取 `%s`' % (
            s['className'] or '?', s['global'], s['ctor'], s['vtable'], s['reader']))
        L.append('')
        L.append('| 读序 | 列号（CSV 位置，权威） | 读取原语 | 类型 |')
        L.append('|---|---|---|---|')
        for n, c in enumerate(s['cols']):
            L.append('| %d | `%s` | `%s` | %s |' % (n, c['col'], c['fn'], c['type']))
        L.append('')
    L += ['---', '', '## 2. 原语表（造表时的类型语义）', '',
          '| 读取函数 | 含义 | CSV 里应写 |', '|---|---|---|',
          '| `sub_BBB370` | 读 u32 整型 | 十进制数字 |',
          '| `sub_BBB470` | 读 float | 小数（如 `1.5`） |',
          '| `sub_BBB3F0` | 读 i64 | 十进制数字 |',
          '| `sub_456D90` | 读字符串 | 文本 |',
          '| `sub_BBB4F0` | 读字符串 → 枚举查表 | **枚举名**（见 `枚举表.md`） |', '',
          '> 其它铁律（编码 UTF-8 无 BOM / CRLF / 尾逗号 / `#` 行跳过 / 越界列=0）'
          '见 `topics/16 §三` 与 `formats/README §四`。', '']
    with io.open(os.path.join(HERE, '数据表-80表列规格.md'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(L))
    return len(ok), len(bad)


def main():
    spec = build()
    write_spec(spec)
    ok, bad = write_md(spec)
    print('OK: %d tables, %d with cols, %d without' % (len(spec), ok, bad))


if __name__ == '__main__':
    main()
