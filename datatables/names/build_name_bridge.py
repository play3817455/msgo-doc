# -*- coding: utf-8 -*-
"""
build_name_bridge.py（v2 · 权威表驱动）—— 建「机体名 ↔ ID ↔ 数值」总对照表。

★ v1 的做法（片假名→中文自造字典 + 命中率打分）已被**用户提供的权威表**取代：
   `unpackdat/codex/机动战士敢达OL机体名称中日对照表.json`（**704 台**：`id`=練度ID / `jp` / `cn`（万代官方简中）/ `group` / `note`）
  ⇒ 練度ID ↔ 日文名 ↔ 官方中文名 **已是确定关系**，只剩"官方中文名 → codex/wiki 页面"这一步，而且大多是**直接同名**。

三份数据：
  ① 权威表            `unpackdat/codex/机动战士敢达OL机体名称中日对照表.json`（704：id/jp/cn/group/note）
  ② codex 数值        `unpackdat/codex/data/units.json`（699：**order = wiki 序号** + armor/shield/speed/boost/boost_cd/payload/return_val/down/type/cost/time/carry/slots/mcost/terrain）
  ③ wiki 数值（自抓）  `datatables/wiki/wiki_ms_stats.csv`（618：页面/序号/装甲/最高速度/推进容量/推进器冷却/载重量/紧急返回性能/机体倒地值…）

匹配策略（权威 cn → codex name）：
  P1 归一化后**完全相等**
  P2 「中国用X」↔「X(国)」等价（用户提示：表里的「中国用」对应 wiki 的「（国）」）
  P3 相似度（difflib）贪心一对一（阈值 0.62），同分优先同名长度接近者
  P4 `手动对照.tsv`（`練度ID<TAB>codex名`）人工覆盖，**最高优先级**
数值侧：codex ↔ wiki 用 **`order` == wiki 序号** 直接对齐（不靠名字）⇒ 顺便做**双源一致性校验**。

输出：
  · `机体名对照表.csv`（前 15 列与 v1 兼容，后面追加权威/两源字段）
  · `机体名对照表.md`（覆盖率与分档报告 + 未匹配清单 + 双源不一致清单）
用法：python build_name_bridge.py [--diag]
"""
import difflib
import io
import json
import os
import re
import sys
import unicodedata

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
AUTH = os.path.join(ROOT, 'unpackdat', 'codex', '机动战士敢达OL机体名称中日对照表.json')
CODEX = os.path.join(ROOT, 'unpackdat', 'codex', 'data', 'units.json')
WIKI = os.path.join(ROOT, 'datatables', 'wiki', 'wiki_ms_stats.csv')
MANUAL = os.path.join(HERE, '手动对照.tsv')
SYN = os.path.join(HERE, '同义词.tsv')
OUT_CSV = os.path.join(HERE, '机体名对照表.csv')
OUT_MD = os.path.join(HERE, '机体名对照表.md')

# wiki_ms_stats.csv 里要用的列（按名字取，避免列序变化）
WIKI_COLS = ['页面', '序号', '装甲', '最高速度', '推进容量', '推进器冷却', '推进器冷却力',
             '载重量', '机载量', '紧急返回性能', '紧急归投数量', '机体倒地值', '护盾耐久值', '插槽数']
# 两源一致性校验对（codex 字段 → wiki 列名候选）
XCHECK = [('armor', ['装甲']), ('speed', ['最高速度']), ('boost', ['推进容量']),
          ('boost_cd', ['推进器冷却', '推进器冷却力']), ('payload', ['载重量', '机载量']),
          ('return_val', ['紧急返回性能', '紧急归投数量'])]


def norm(s):
    """归一化：全角→半角、高达→敢达、罗马数字、去空白与括号与间隔符"""
    s = unicodedata.normalize('NFKC', str(s or ''))
    s = s.replace('高达', '敢达').replace('鋼彈', '敢达')
    s = s.replace('・', '·').replace('•', '·')
    s = re.sub(r'[\(\)\[\]【】]', '', s)
    s = s.replace('·', '').replace('-', '').replace('－', '').replace('_', '')
    s = re.sub(r'[\s\u3000]+', '', s)
    return s.lower()


def norm2(s):
    """在 norm 基础上再抹掉「中国用 / (国)」标记 ⇒ 用于 P2 等价"""
    t = norm(s).replace('中国用', '')
    t = t.replace('国服版', '').replace('(国)', '')
    return t


def sim(a, b):
    return difflib.SequenceMatcher(None, a, b).ratio()


def load_syn():
    """`同义词.tsv`：A<TAB>B —— 抹平"同一台机体两种叫法"（如 教练型↔训练机）"""
    out = []
    if os.path.exists(SYN):
        for l in open(SYN, encoding='utf-8'):
            if l.startswith('#') or '\t' not in l:
                continue
            p = l.rstrip('\n').split('\t')
            if len(p) >= 2 and p[0].strip() and p[1].strip():
                out.append((p[0].strip(), p[1].strip()))
    return out


def syn_variants(s, pairs):
    """对一个名字生成"替换同义词后"的变体（双向）"""
    out = []
    for a, b in pairs:
        if a in s:
            out.append(s.replace(a, b))
        if b in s:
            out.append(s.replace(b, a))
    return out


def aliases(a):
    """★从 `note` 里抠别名：表里写着「旧译「铁奥」」「亦有译名「波尔」」「俗称「逆A敢达」」⇒ 全是可用的匹配键"""
    return [m.group(1) for m in re.finditer(r'「([^」]{2,})」', a.get('note', ''))]


def load_manual():
    m = {}
    if os.path.exists(MANUAL):
        for l in open(MANUAL, encoding='utf-8'):
            if not l.strip() or l.startswith('#'):
                continue
            p = l.rstrip('\n').split('\t')
            if len(p) >= 2 and p[0].strip() and p[1].strip():
                m[p[0].strip()] = p[1].strip()
    return m


def load_wiki():
    """→ {序号: {列: 值}} + 列名索引"""
    if not os.path.exists(WIKI):
        return {}, {}
    lines = [l for l in open(WIKI, encoding='utf-8-sig').read().splitlines() if l and not l.startswith('#')]
    hdr = None
    for l in open(WIKI, encoding='utf-8-sig'):
        if l.startswith('#页面'):
            hdr = l.lstrip('#').rstrip('\n').rstrip(',').split(',')
            break
    idx = {c: i for i, c in enumerate(hdr or [])}
    out = {}
    for l in lines:
        f = l.rstrip(',').split(',')
        if len(f) <= idx.get('序号', 2):
            continue
        no = f[idx['序号']]
        if no.isdigit():
            out.setdefault(no, {}).update({c: f[i] for c, i in idx.items() if i < len(f)})
    return out, idx


def diag():
    """诊断：wiki 页面正文里能否直接找到**权威日文名**（能找到 ⇒ 可用"日文名"做硬匹配，替代模糊猜名）"""
    import glob
    auth = json.load(open(AUTH, encoding='utf-8'))['entries']
    J = {}
    for a in auth:
        j = norm(a.get('jp', ''))
        if len(j) >= 4:
            J.setdefault(j, a['id'])
    fs = glob.glob(os.path.join(ROOT, 'datatables', 'wiki', 'cache', '*.txt'))
    print('权威日文名 %d 个（长度≥4）｜缓存页 %d' % (len(J), len(fs)))
    cn_by_id = {a['id']: a.get('cn', '') for a in auth}
    ok = amb = 0
    samples = []
    for f in fs:
        page = os.path.basename(f)[:-4]
        t = norm(open(f, encoding='utf-8').read())
        cand = [rid for j, rid in J.items() if j in t]
        if not cand:
            continue
        # ★用官方中文名与页面名的相似度排序，取最高
        pn = norm2(page)
        ranked = sorted(cand, key=lambda r: -sim(pn, norm2(cn_by_id.get(r, ''))))
        if len(cand) > 1:
            amb += 1
        ok += 1
        samples.append((page, ranked[:3], [round(sim(pn, norm2(cn_by_id.get(r, ''))), 2) for r in ranked[:3]]))
    print('正文命中日文名候选的页：%d（其中多候选 %d）' % (ok, amb))
    print('   排序后样例（页 → 候选练度ID ｜ 与页面名的相似度）：')
    for page, r, s in samples[:10]:
        print('   %-30s → %s ｜ %s' % (page, r, s))
    print()
    print('手动对照.tsv 前 3 行：')
    if os.path.exists(MANUAL):
        for i, l in enumerate(open(MANUAL, encoding='utf-8')):
            if i < 3:
                print('   %r' % l[:80])
    else:
        print('   （不存在）')
    return 0


def main():
    auth = json.load(open(AUTH, encoding='utf-8'))['entries']
    units = json.load(open(CODEX, encoding='utf-8'))['units']
    manual = load_manual()
    syn = load_syn()
    wiki, widx = load_wiki()
    print('权威表 %d 台 ｜ codex %d 台 ｜ wiki 数值 %d 序号 ｜ 人工覆盖 %d 条'
          % (len(auth), len(units), len(wiki), len(manual)))

    cn2unit = {}
    for u in units:
        cn2unit.setdefault(norm(u['name']), u)
    cn2unit2 = {}
    for u in units:
        cn2unit2.setdefault(norm2(u['name']), u)

    rows, used = [], set()
    cnt = {'manual': 0, 'exact': 0, 'alias': 0, 'syn': 0, 'guo': 0, 'fuzzy': 0, 'none': 0}
    for a in auth:
        rid, jp, cn = a['id'], a.get('jp', ''), a.get('cn', '')
        u, how, score = None, '', 0.0
        if rid in manual:                                  # P4 人工
            want = norm(manual[rid])
            u = cn2unit.get(want) or cn2unit2.get(want)
            how = '手动' if u else '手动(未命中)'
        extra = aliases(a) + syn_variants(cn, syn) + syn_variants(jp, syn)
        cands = [cn, jp] + extra
        if u is None:                                      # P1 精确（含 note 别名 / 同义词替换变体）
            for c in cands:
                u = cn2unit.get(norm(c))
                if u:
                    how = '精确' if c == cn else ('同义词' if c in extra else '别名')
                    break
        if u is None:                                      # P2 中国用 ↔ (国) 等价
            for c in cands:
                u = cn2unit2.get(norm2(c))
                if u:
                    how = '国字等价'
                    break
        ranked = None
        if u is None:                                      # P3 相似度（跨 cn+别名 取最优；只对未用过的）
            ts = [norm2(c) for c in cands if c]
            scored = []
            for un in units:
                if un['name'] not in used:
                    scored.append((max(sim(t, norm2(un['name'])) for t in ts), un))
            scored.sort(key=lambda x: -x[0])
            ranked = scored[:3]
            if scored and scored[0][0] >= 0.62:
                second = scored[1][0] if len(scored) > 1 else 0.0
                # ★领先度要求：第一必须明显优于第二，否则宁可留空（避免"吉姆A配到吉姆B"式错配）
                if scored[0][0] >= 0.80 or scored[0][0] - second >= 0.05:
                    u, how, score = scored[0][1], '相似', round(scored[0][0], 3)
        status = how
        rec_note = ''
        if u is None or how == '相似':
            if ranked is None:
                ts = [norm2(c) for c in cands if c]
                scored = sorted(((max(sim(t, norm2(un['name'])) for t in ts), un) for un in units),
                                key=lambda x: -x[0])[:3]
                ranked = scored
            rec_note = ' / '.join('%s(%.2f)' % (un['name'], s) for s, un in ranked)
        if u is None:
            cnt['none'] += 1
        else:
            used.add(u['name'])
            score = score or (1.0 if how in ('手动', '精确', '别名', '同义词', '国字等价') else 0.0)
            cnt[{'精确': 'exact', '别名': 'alias', '同义词': 'syn', '国字等价': 'guo', '相似': 'fuzzy'}.get(how, 'manual')] += 1
        u = u or {}
        w = wiki.get(str(u.get('order', '')), {})
        rec = {
            '練度ID': rid, '日文名': jp, 'codex中文名': u.get('name', ''), '方式': 'auto' if how else 'unmatched',
            '分数': '%.3f' % score, '档位': {'手动': '人工', '精确': '精确', '别名': '别名', '同义词': '同义词', '国字等价': '国', '相似': '近似'}.get(how, '未匹配'),
            'type': u.get('type', ''), 'cost': u.get('cost', ''), 'armor': u.get('armor', ''),
            'speed': u.get('speed', ''), 'boost': u.get('boost', ''), 'payload': u.get('payload', ''),
            'shield': u.get('shield', ''), 'down': u.get('down', ''), 'terrain': u.get('terrain', ''),
            # ↓ v2 新增
            '官方中文名': cn, '段': a.get('group', ''), '备注': a.get('note', ''),
            '匹配方式': status, 'codex页面': u.get('id', ''), 'wiki序号': u.get('order', ''),
            'faction': u.get('faction', ''), 'time': u.get('time', ''), 'carry': u.get('carry', ''),
            'boost_cd': u.get('boost_cd', ''), 'return_val': u.get('return_val', ''),
            'slots': u.get('slots', ''), 'mcost': u.get('mcost', ''),
            'wiki页面': w.get('页面', ''), 'wiki装甲': w.get('装甲', ''), 'wiki最高速度': w.get('最高速度', ''),
            'wiki推进容量': w.get('推进容量', ''), 'wiki推进器冷却': w.get('推进器冷却', '') or w.get('推进器冷却力', ''),
            'wiki载重量': w.get('载重量', '') or w.get('机载量', ''), 'wiki紧急返回': w.get('紧急返回性能', '') or w.get('紧急归投数量', ''),
            'wiki倒地值': w.get('机体倒地值', ''), 'wiki插槽数': w.get('插槽数', ''),
        }
        # 双源一致性（只在两边都是纯数字时比）
        diffs = []
        for k, cols in XCHECK:
            cv = str(rec.get(k) or '').strip()
            for c in cols:
                wv = str(w.get(c) or '').strip()
                if cv.isdigit() and wv.replace(',', '').isdigit() and wv:
                    if abs(int(cv) - int(wv.replace(',', ''))) > max(1, int(cv) * 0.02):
                        diffs.append('%s(codex %s vs wiki %s)' % (k, cv, wv))
                    break
        rec['两源差异'] = '; '.join(diffs)
        rec['候选'] = rec_note
        rows.append(rec)

    cols = ['練度ID', '日文名', 'codex中文名', '方式', '分数', '档位', 'type', 'cost', 'armor', 'speed',
            'boost', 'payload', 'shield', 'down', 'terrain',
            '官方中文名', '段', '备注', '匹配方式', 'codex页面', 'wiki序号', 'faction', 'time', 'carry',
            'boost_cd', 'return_val', 'slots', 'mcost', 'wiki页面', 'wiki装甲', 'wiki最高速度', 'wiki推进容量',
            'wiki推进器冷却', 'wiki载重量', 'wiki紧急返回', 'wiki倒地值', 'wiki插槽数', '两源差异', '候选']
    with open(OUT_CSV, 'wb') as f:
        txt = ['#' + ','.join(cols) + ',']
        for r in rows:
            txt.append(','.join(str(r.get(c, '')).replace(',', '，') for c in cols) + ',')
        f.write(('\r\n'.join(txt) + '\r\n').encode('utf-8'))

    # ── 重新生成 `手动对照.tsv`：保留已填的人工行 + 给未匹配/近似项附候选清单（第 3 列，仅供参照）
    keep = []
    if os.path.exists(MANUAL):
        for l in open(MANUAL, encoding='utf-8').read().splitlines():
            if l.startswith('#') or '\t' not in l:
                continue
            p = l.split('\t')
            if len(p) >= 2 and p[0].strip() and p[1].strip():
                keep.append('%s\t%s' % (p[0].strip(), p[1].strip()))
    todo = [r for r in rows if r['方式'] != 'auto' or r['档位'] == '近似']
    tsv = ['# 人工对照（覆盖自动匹配）：練度ID<TAB>codex 中文名<TAB>#注释',
           '# 第 2 列填"正确的 codex 中文名"即生效（填了就覆盖自动结果）；第 3 列是自动给的候选，仅供参照、勿照抄',
           '# 现有自动匹配：%d / %d；下表待确认 %d 条'
           % (len([r for r in rows if r['方式'] == 'auto']), len(rows), len(todo))]
    tsv += keep
    tsv += ['%s\t\t# 官方：%s ｜ jp：%s ｜ 候选：%s' % (r['練度ID'], r['官方中文名'], r['日文名'], r['候选'] or '（无）')
            for r in todo]
    open(MANUAL, 'w', encoding='utf-8').write('\n'.join(tsv) + '\n')
    print('已刷新 %s（保留人工行 %d 条，待确认 %d 条）' % (MANUAL, len(keep), len(todo)))

    got = [r for r in rows if r['方式'] == 'auto']
    diff = [r for r in rows if r['两源差异']]
    md = ['# 机体名 ↔ ID ↔ 数值 总对照表（v2 · 权威表驱动）', '',
          '- 权威来源：`unpackdat/codex/机动战士敢达OL机体名称中日对照表.json`（704 台：練度ID/jp/cn/group/note）',
          '- 数值来源：codex `units.json`（699，`order` = wiki 序号）+ 自抓 `wiki/wiki_ms_stats.csv`（618）',
          '- 匹配：手动覆盖 > 精确 > 「中国用↔(国)」等价 > 相似度(≥0.62) 贪心；数值侧用 **`order`==wiki 序号** 直接对齐', '',
          '## 覆盖率', '',
          '| 结果 | 数量 |', '|---|---|',
          '| ✅ 已对上 | **%d / %d（%.1f%%）** |' % (len(got), len(rows), 100.0 * len(got) / max(1, len(rows))),
          '| ├ 人工覆盖 | %d |' % cnt['manual'], '| ├ 精确同名 | %d |' % cnt['exact'],
          '| ├ note 别名 | %d |' % cnt['alias'], '| ├ 同义词替换 | %d |' % cnt['syn'],
          '| ├ 中国用↔(国) | %d |' % cnt['guo'],
          '| └ 相似度 | %d |' % cnt['fuzzy'],
          '| ❌ 未匹配 | %d |' % cnt['none'], '',
          '## 双源数值差异（codex vs wiki，>2%% 才算）', '',
          '共 **%d** 台存在差异 ⇒ 建议以 **wiki（页面人工维护）为准**，codex 作备用。' % len(diff), '']
    if diff:
        md += ['| 練度ID | 官方中文名 | 差异 |', '|---|---|---|']
        for r in diff[:60]:
            md.append('| %s | %s | %s |' % (r['練度ID'], r['官方中文名'], r['两源差异']))
    bad = [r for r in rows if r['方式'] != 'auto']
    md += ['', '## 未匹配清单（%d 台，待人工补 `手动对照.tsv`）' % len(bad), '']
    if bad:
        md += ['| 練度ID | 官方中文名 | 日文名 | 段 |', '|---|---|---|---|']
        for r in bad[:120]:
            md.append('| %s | %s | %s | %s |' % (r['練度ID'], r['官方中文名'], r['日文名'], r['段']))
    open(OUT_MD, 'w', encoding='utf-8').write('\n'.join(md) + '\n')

    print('✅ 已对上 %d / %d（%.1f%%）：人工 %d / 精确 %d / 国字 %d / 相似 %d ｜ 未匹配 %d'
          % (len(got), len(rows), 100.0 * len(got) / max(1, len(rows)), cnt['manual'], cnt['exact'], cnt['guo'], cnt['fuzzy'], cnt['none']))
    print('双源数值差异 %d 台' % len(diff))
    print('写入 %s / %s' % (OUT_CSV, OUT_MD))
    return 0


if __name__ == '__main__':
    sys.exit(diag() if '--diag' in sys.argv else main())
