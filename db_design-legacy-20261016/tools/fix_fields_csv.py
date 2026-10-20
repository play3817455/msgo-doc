# -*- coding: utf-8 -*-
"""fix_fields_csv.py —— 把 protocol_analysis/commands/*/fields.csv 的畸形行修成规范 10 列。

为什么
======
`fields.csv` 是人手写的，csv 分列时有三类畸形（历史坑 ⑲/㉓）：

  A 线类型格未加引号（`array<item,A1>`）→ 被逗号切成两格；
  B `bytes,NUL串` 两格（本意是类型说明 `bytes(NUL 串)`，README 写的是 `bytes（NUL 串）`）；
  C 文本格（含义/用途/取值/证据VA）内含 ASCII 逗号（日志模板、`cmp edi,7`）；
  D 9 列的「（长度闭合）」行——约定省了「取值或枚举」格；
  E 9 列的 `struct X` 行——约定省了「字段名」格（结构名已写在线类型里）。

后果：两套读者各自启发式拼回，**口径不一**：`codecgen/main.py` 把 `NUL串` 当占位符、
真名从含义取；`import_commands.py` 反过来把字段名与含义并成一格，于是 B 类行的**真名被吞**
（`SC-0x1113` 的 `src` 变成 `f_0`）。同一份数据两个解释器 = 迟早对不上。

做法
====
**只修切分，不动内容**：把被切开的碎片并回同一格、把缺的格补上，再用规范引号写回。
文件编码/BOM/行尾沿用原文件。这样两套读者都不再需要启发式。

判定「哪一格被切开」优先用 README 同序号行的**锚定列**（线类型/字段名/取值或枚举/证据VA）
当对照（这几列与 CSV 只差反引号/空白），对候选切分打分取最高；README 缺失时退回结构评分。
所有结论写报告供复核。

用法
====
    python db_design/tools/fix_fields_csv.py --check      # 只报告，不写盘
    python db_design/tools/fix_fields_csv.py --write      # 就地修复
    python db_design/tools/fix_fields_csv.py --report out.txt
"""
from __future__ import annotations

import csv
import io
import itertools
import pathlib
import re
import sys
from collections import Counter

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import import_commands as IC  # noqa: E402

ROOT = pathlib.Path('protocol_analysis/commands')

HEADER = ["序号", "偏移", "长度", "线类型", "字段名", "含义", "用途", "取值或枚举", "证据VA", "置信度"]

CONFIDENCE_OK = {'确证', '推测', '类型确证/语义推测', '类型确证', '语义推测', '待复核', '?'}
CLOSURE_NAME = {'（长度闭合）', '(长度闭合)'}

VA_RE = re.compile(r'0x[0-9A-Fa-f]{3,}|(?<![A-Za-z0-9_])[0-9A-F]{6,8}(?![A-Za-z0-9_])')
IDENT_RE = re.compile(r'^[A-Za-z_]\w*(\.[A-Za-z_]\w*|\[\])*$')
ENUM_LITERAL_RE = re.compile(r'^(?:-|—|\d+|0x[0-9A-Fa-f]+|\d+\.\.\d+|0/\d+)$')
ENUM_HINT_RE = re.compile(r'(固定|上限|≤|<=|strlen|条数|元素线长|已知枚举|见 .*枚举)')
NUL_QUAL_RE = re.compile(r'^NUL\s*串$')
PURPOSE_BROAD_KW = ('交', '经', '上限', '驱动', '循环', '日志', '打印器', '来源', '去向', '数组', '元素',
                    '结构', '指针', '游标', '容量', '预留', '槽', '克隆', '回显', '提交', '发送', '分发',
                    '读取', '写入', 'vt[', '→', '校验', '规则')


def norm(s: str) -> str:
    s = (s or '').replace('\\', '')
    s = re.sub(r'[`*\s]', '', s)
    s = s.replace('（', '(').replace('）', ')').replace('，', ',')
    for d in '—–−':
        s = s.replace(d, '-')
    return s


def vas(s: str) -> set[str]:
    return {v.lower().removeprefix('0x') for v in VA_RE.findall(s or '')}


def recall(a: str, b: str) -> float:
    """a 的字符集合有多大比例出现在 b 里（b 通常更长）。"""
    sa, sb = set(norm(a)), set(norm(b))
    if not sa:
        return 0.0
    return len(sa & sb) / len(sa)


def balance(s: str, o: str, c: str) -> int:
    return (s or '').count(o) - (s or '').count(c)


# CSV 里括号多为**全角**（`（）｛｝［］【】`），只数半角会让「括号配平」这条判据整体失效
# ——`SC-0x07E9:8` 的错切分正是这样漏过。统一折算后再数。
_FW = {'（': '(', '）': ')', '｛': '{', '｝': '}', '［': '[', '］': ']', '【': '[', '】': ']',
       '＜': '<', '＞': '>', '〈': '<', '〉': '>'}


def pbalance(s: str) -> int:
    """**圆括号**净开数（全角折半角）。

    只算圆括号：文本格里出现 `{`/`}`（日志模板 `hav_voice={`）、`<`/`>`（比较式 `B<=52`）
    都是**正常**的，算进去反而会把切分正确的行判成不配平。
    """
    t = ''.join(_FW.get(ch, ch) for ch in (s or ''))
    return balance(t, '(', ')')


def wire_unbalanced(s: str) -> bool:
    t = ''.join(_FW.get(ch, ch) for ch in (s or ''))
    return balance(t, '<', '>') > 0 or balance(t, '{', '}') > 0


def readme_rows(cmd_dir: pathlib.Path) -> dict[str, list[str]]:
    p = cmd_dir / 'README.md'
    if not p.is_file():
        return {}
    out: dict[str, list[str]] = {}
    for line in p.read_text(encoding='utf-8', errors='replace').splitlines():
        s = line.strip()
        if not s.startswith('|'):
            continue
        cells = [c.strip() for c in s.strip('|').split('|')]
        if len(cells) < 10 or cells[0] == '序号' or set(cells[0]) <= set('-: '):
            continue
        out.setdefault(norm(cells[0]) or '-', cells)
    return out


# ---------------------------------------------------------------- 候选打分

def score_parts(groups: list[str], readme: list[str] | None) -> dict[str, float]:
    """各判据的得分明细（和为总分）。留明细是为了复核时能看出**哪条判据**在起作用。"""
    fname, meaning, purpose, enum, evid = groups
    p: dict[str, float] = {}

    if IDENT_RE.match(fname):
        p['fname_ident'] = 6
    elif fname.strip() in CLOSURE_NAME:
        p['fname_closure'] = 5
    elif re.search(r'[\u3400-\u9FFF]', fname):
        p['fname_cjk'] = -6
    if not fname.strip():
        p['fname_empty'] = -8

    if ENUM_LITERAL_RE.match(enum.strip()):
        p['enum_literal'] = 4
    elif ENUM_HINT_RE.search(enum):
        p['enum_hint'] = 3
    else:
        p['enum_shape'] = -2
    if len(enum) > 44:
        p['enum_long'] = -4
    if 'vt[' in enum or '日志' in enum:
        p['enum_purpose_ish'] = -6

    if IC.PURPOSE_START.match(purpose):
        p['purpose_start'] = 5
    elif any(k in purpose for k in PURPOSE_BROAD_KW):
        p['purpose_kw'] = 2
    else:
        p['purpose_shape'] = -4
    if not purpose.strip():
        p['purpose_empty'] = -5

    ve = vas(evid)
    if ve:
        p['evid_has_va'] = 4
    if '；' in evid or '。' in evid:
        p['evid_prose'] = -5

    for name, cell in (('meaning', meaning), ('purpose', purpose), ('enum', enum)):
        if pbalance(cell) != 0:
            p['bal_paren_' + name] = -1
        if cell.count('`') % 2:
            p['bal_tick_' + name] = -1

    if readme:
        rf, rm, rp, re_, rv = readme[4], readme[5], readme[6], readme[7], readme[8]
        if norm(fname) == norm(rf):
            p['rm_fname_eq'] = 8
        elif norm(fname) and norm(fname) in norm(rf):
            p['rm_fname_in'] = 4
        if norm(enum) == norm(re_):
            p['rm_enum_eq'] = 5
        elif norm(enum) and norm(enum) in norm(re_):
            p['rm_enum_in'] = 3
        vr = vas(rv)
        if ve and vr:
            if ve <= vr:
                p['rm_evid_sub'] = 4
            elif len(ve & vr) / len(ve) >= 0.6:
                p['rm_evid_ov'] = 2
        p['rm_purpose_recall'] = round(4 * recall(purpose, rp), 3)
        p['rm_meaning_recall'] = round(3 * recall(meaning, rm), 3)
    return p


def score_split(groups: list[str], readme: list[str] | None) -> float:
    return sum(score_parts(groups, readme).values())



def split_region(rest: list[str], readme: list[str] | None) -> tuple[list[str], float, float]:
    """把 rest 切成 [字段名,含义,用途,取值,证据VA]；返回 (最优, 分数, 次优分数)。

    **硬约束**：`证据VA` 格必须含汇编地址（README 口径「每行必须有汇编证据 VA」）。
    没有这条约束时，评分会把「置信度」当证据、把证据当取值
    （`SC-0xF66B:5` 曾被切成 `取值=0xB87296 / 证据=确证`）。全被滤掉时退回不滤。
    """
    m = len(rest)
    if m < 5:
        return rest + [''] * (5 - m), -999.0, -999.0
    cands = []
    for cuts in itertools.combinations(range(1, m), 4):
        b = (0,) + cuts + (m,)
        groups = [','.join(rest[b[i]:b[i + 1]]) for i in range(5)]
        cands.append(groups)
    strict = [g for g in cands if vas(g[4])]
    pool = strict or cands
    scored = [(score_split(g, readme), g) for g in pool]
    scored.sort(key=lambda kv: -kv[0])
    best = scored[0]
    second = scored[1][0] if len(scored) > 1 else -999.0
    return best[1], best[0], second


# ---------------------------------------------------------------- 行修复

def fix_row(raw: list[str], readme: list[str] | None) -> tuple[list[str] | None, list[str]]:
    cells = [c.strip() for c in raw]
    fix: list[str] = []

    guard = 0
    while len(cells) > 4 and wire_unbalanced(cells[3]) and guard < 6:
        cells[3] = cells[3] + ',' + cells[4]
        del cells[4]
        guard += 1
    if guard:
        fix.append('wire_comma_merge_x%d' % guard)

    if len(cells) > 4 and NUL_QUAL_RE.match(cells[4]) and cells[3].strip() in ('bytes', 'str', 'string'):
        cells[3] = '%s(NUL 串)' % cells[3].strip()
        del cells[4]
        fix.append('nul_qual_merge')

    n = len(cells)
    if n == 10:
        return cells, fix
    if n < 10:
        if n == 9:
            if cells[4].strip() in CLOSURE_NAME:
                cells.insert(7, '-')
                fix.append('closure_missing_enum_filled')
                return cells, fix
            m = IC.STRUCT_WT_RE.match(cells[3])
            if m and re.search(r'[\u3400-\u9FFF]', cells[4] or ''):
                cells.insert(4, m.group('name'))
                fix.append('struct_missing_name_filled')
                return cells, fix
            cells.insert(7, '-')
            fix.append('short_row_enum_filled')
            return cells, fix
        return None, fix + ['unrepairable_%d_cols' % n]

    rest = cells[4:-1]
    groups, best, second = split_region(rest, readme)
    out = cells[:3] + [cells[3]] + groups + [cells[-1]]
    fix.append('text_comma_split(k=%d,score=%.1f,second=%.1f)' % (n - 10, best, second))
    if best - second < 2.0:
        fix.append('ambiguous_split')
    return out, fix


# ---------------------------------------------------------------- 主流程

def process(write: bool, report_path: pathlib.Path | None) -> int:
    buf: list[str] = []
    W = buf.append
    stat: Counter = Counter()
    rows_total = 0
    files_changed = 0
    low_conf: list[str] = []

    for cmd_dir in sorted(ROOT.iterdir()):
        csvp = cmd_dir / 'fields.csv'
        if not csvp.is_file():
            continue
        blob = csvp.read_bytes()
        bom = blob[:3] == b'\xef\xbb\xbf'
        crlf = b'\r\n' in blob
        text = blob.decode('utf-8-sig')
        rows = list(csv.reader(io.StringIO(text, newline='')))
        if not rows:
            continue
        readme = readme_rows(cmd_dir)
        out_rows = [rows[0]]
        changed = False
        for line_no, raw in enumerate(rows[1:], start=2):
            rows_total += 1
            if not any(c.strip() for c in raw):
                out_rows.append(raw)
                continue
            if len(raw) == 10 and all(not c.startswith(' ') and not c.endswith(' ') for c in raw):
                out_rows.append(raw)
                continue
            fixed, fix = fix_row(list(raw), readme.get(norm(raw[0]) or '-'))
            if fixed is None:
                stat['unrepairable'] += 1
                W('!! 修不出 %s:%d  %r' % (cmd_dir.name, line_no, raw))
                out_rows.append(raw)
                continue
            if len(raw) != 10:
                stat['malformed'] += 1
                for f in fix:
                    stat[f.split('(')[0]] += 1
                W('%s:%d  raw=%d -> %r' % (cmd_dir.name, line_no, len(raw), fix))
                W('    was = %r' % (raw,))
                W('    now = %r' % (fixed,))
                r = readme.get(norm(raw[0]) or '-')
                if r:
                    W('    readme = %r' % ([r[3], r[4], r[5], r[6], r[7], r[8]],))
                if 'ambiguous_split' in fix:
                    low_conf.append('%s:%d' % (cmd_dir.name, line_no))
                if fixed != raw:
                    changed = True
            out_rows.append(fixed)

        if changed:
            files_changed += 1
            if write:
                sio = io.StringIO()
                w = csv.writer(sio, lineterminator='\r\n' if crlf else '\n', quoting=csv.QUOTE_MINIMAL)
                w.writerows(out_rows)
                data = sio.getvalue().encode('utf-8')
                if bom:
                    data = b'\xef\xbb\xbf' + data
                csvp.write_bytes(data)

    W('')
    W('=' * 90)
    W('行总数 %d；畸形行 %d；修复后文件 %d；修不出 %d'
      % (rows_total, stat['malformed'], files_changed, stat['unrepairable']))
    W('修复动作分布：')
    for k, v in stat.most_common():
        W('   %-30s %d' % (k, v))
    W('切分可疑（最优/次优接近，需人工看一眼） %d 行：' % len(low_conf))
    for x in low_conf:
        W('   ' + x)

    if report_path is not None:
        report_path.write_text('\n'.join(buf) + '\n', encoding='utf-8')
    print('行总数 %d；畸形 %d；文件 %d；修不出 %d；切分可疑 %d'
          % (rows_total, stat['malformed'], files_changed, stat['unrepairable'], len(low_conf)))
    for k, v in stat.most_common(10):
        print('   %-30s %d' % (k, v))
    return 0


def main() -> int:
    write = '--write' in sys.argv
    # 默认报告分「干跑」和「实写」两份：写写实跑会改盘，报告要对得上盘上状态。
    # 早前两者共用一个默认路径，`--check` 一回就把 `--write` 留下的逐行明细
    # （`was=` / `now=` / README 锚）覆盖成空表，事后想复核「改前长什么样」就没料了。
    report = pathlib.Path('db_design/tools/_fixcsv_report.txt' if write
                          else 'db_design/tools/_fixcsv_check.txt')
    for i, a in enumerate(sys.argv):
        if a == '--report' and i + 1 < len(sys.argv):
            report = pathlib.Path(sys.argv[i + 1])
    return process(write, report)


if __name__ == '__main__':
    sys.exit(main())
