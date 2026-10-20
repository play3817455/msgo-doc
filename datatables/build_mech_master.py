# -*- coding: utf-8 -*-
"""
build_mech_master.py —— 以《机动战士敢达OL机体名称中日对照表.json》为准，建「机体总表」。

数据源（全部本地已有）：
  ① `unpackdat/codex/机动战士敢达OL机体名称中日对照表.json`  ← **主键来源**
     704 条：`id`(練度ID 7位) / `jp` / `cn` / `group` / `wiki_conf` / `wiki_name` / `wiki_url`
  ② `unpackdat/codex/data/units.json`（699 台机体数值：armor/shield/speed/boost/boost_cd/
     payload/return_val/down/slots/cost/time/type/terrain/faction，键=wiki 页面名）
  ③ `datatables/wiki/wiki_ms_stats.csv`（618 台 · 日文面板：装甲/盾牌/护盾耐久值/最高速度/
     推进容量/推进器冷却(力)/载重量/机载量/紧急返回性能/机体倒地值/地形适应/插槽数/COST/TIME）
  ④ `datatables/wiki/wiki_ms_weapons.csv`（6404 条武器行，键=wiki 页面名）
  ⑤ `datatables/names/模型号映射-初版.csv`（練度ID → 模型打包值，实测/真值/代号表已确认部分）

产物：`datatables/names/机体总表.csv`（每台机体一行：名字三语 + wiki 页 + 两套面板数值 + 模型 + 武器数）
用法：python datatables/build_mech_master.py
"""
import io
import json
import os
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CODEX = os.path.join(ROOT, 'unpackdat', 'codex')
OUT = os.path.join(HERE, 'names', '机体总表.csv')


def norm(s):
    """页面名归一：高达/敢达统一、去空格下划线、全角括号→半角、小写。"""
    s = str(s or '')
    s = s.replace('高达', '敢达').replace('高達', '敢达')
    s = re.sub(r'[\s_　]+', '', s)
    s = s.replace('（', '(').replace('）', ')').lower()
    return s


def rows_of(path, enc='utf-8'):
    if not os.path.exists(path):
        return []
    t = open(path, encoding=enc, errors='replace').read()
    return [l.rstrip('\r') for l in t.splitlines() if l.strip() and not l.lstrip().startswith('#')]


def main():
    tab = json.load(open(os.path.join(CODEX, '机动战士敢达OL机体名称中日对照表.json'), encoding='utf-8'))
    entries = tab['entries']
    units = json.load(open(os.path.join(CODEX, 'data', 'units.json'), encoding='utf-8'))['units']

    # codex：多键索引（★关键：codex 的页名形如 `敢达ol<名>机体数据`，要剥掉 "机体数据" 后缀与 ol 前缀）
    def bare(s):
        s = re.sub(r'机体数据$', '', norm(s))
        return re.sub(r'^(敢达ol|高达ol|ol)', '', s)

    cx = {}
    for u in units:
        for k in ('id', 'page', 'article', 'name'):
            if u.get(k):
                cx.setdefault(norm(u[k]), u)
                cx.setdefault(bare(u[k]), u)

    # wiki 面板
    st = []
    for l in rows_of(os.path.join(HERE, 'wiki', 'wiki_ms_stats.csv'), 'utf-8-sig'):
        f = l.rstrip(',').split(',')
        st.append(f)
    sth = [x.lstrip('#') for x in rows_of(os.path.join(HERE, 'wiki', 'wiki_ms_stats.csv'), 'utf-8-sig')[0].split(',')] if st else []
    # 上面的 rows_of 已过滤 '#' 行 ⇒ 表头单独取
    raw = open(os.path.join(HERE, 'wiki', 'wiki_ms_stats.csv'), encoding='utf-8-sig').read().splitlines()
    hdr = [x for x in raw if x.startswith('#页面')]
    hdr = hdr[0].lstrip('#').rstrip(',').split(',') if hdr else []
    ws = {}
    for l in raw:
        if not l.strip() or l.startswith('#'):
            continue
        f = l.rstrip(',').split(',')
        if f:
            ws.setdefault(norm(f[0]), f)

    # wiki 武器
    wraw = open(os.path.join(HERE, 'wiki', 'wiki_ms_weapons.csv'), encoding='utf-8-sig').read().splitlines()
    whdr = [x for x in wraw if x.startswith('#页面')]
    whdr = whdr[0].lstrip('#').rstrip(',').split(',') if whdr else []
    wp = {}
    for l in wraw:
        if not l.strip() or l.startswith('#'):
            continue
        f = l.rstrip(',').split(',')
        if f:
            wp.setdefault(norm(f[0]), []).append(f)

    # 模型号映射
    mm = {}
    for l in rows_of(os.path.join(HERE, 'names', '模型号映射-初版.csv')):
        f = l.split(',')
        if len(f) > 5 and f[2]:
            mm[f[0]] = (f[2], f[3], f[5])

    print('对照表 %d ｜ codex %d ｜ wiki面板 %d ｜ wiki武器页 %d ｜ 已知模型号 %d'
          % (len(entries), len(cx), len(ws), len(wp), len(mm)))

    def pick(f, name):
        try:
            i = hdr.index(name)
        except ValueError:
            return ''
        return f[i] if i < len(f) else ''

    out = []
    n_cx = n_ws = n_wp = n_mm = 0
    for e in entries:
        wk = norm(e.get('wiki_name'))
        u = (cx.get(wk) or cx.get(bare(e.get('wiki_name'))) or cx.get(norm(e.get('jp')))
             or cx.get(bare(e.get('jp'))) or {})
        s = ws.get(wk) or ws.get(bare(e.get('wiki_name'))) or []
        w = wp.get(wk) or []
        v, rel, how = mm.get(e['id'], ('', '', ''))
        if u:
            n_cx += 1
        if s:
            n_ws += 1
        if w:
            n_wp += 1
        if v:
            n_mm += 1
        S = lambda x: str(x if x is not None else '')
        out.append([
            S(e.get('id')), S(e.get('jp')), S(e.get('cn')), S(e.get('group')),
            S(e.get('wiki_conf')), S(e.get('wiki_name')),
            # codex 数值
            str(u.get('cost', '')), str(u.get('time', '')), str(u.get('armor', '')), str(u.get('shield', '')),
            str(u.get('speed', '')), str(u.get('boost', '')), str(u.get('boost_cd', '')), str(u.get('payload', '')),
            str(u.get('return_val', '')), str(u.get('down', '')), str(u.get('slots', '')), str(u.get('type', '')),
            str(u.get('faction', '')), str(u.get('terrain', '')),
            # wiki 面板
            pick(s, 'COST'), pick(s, '装甲'), pick(s, '盾牌'), pick(s, '护盾耐久值'), pick(s, '最高速度'),
            pick(s, '推进容量'), pick(s, '推进器冷却'), pick(s, '推載重量'.replace('推', '')) or pick(s, '载重量'),
            pick(s, '机载量'), pick(s, '紧急返回性能'), pick(s, '机体倒地值'), pick(s, '地形适应'), pick(s, '插槽数'),
            # 模型 + 武器
            v, rel, how, str(len(w)),
        ])

    H = ['練度ID', '日文名', '中文名', '分段', 'wiki置信', 'wiki页面',
         'cx_cost', 'cx_time', 'cx_armor', 'cx_shield', 'cx_speed', 'cx_boost', 'cx_boost_cd', 'cx_payload',
         'cx_return', 'cx_down', 'cx_slots', 'cx_type', 'cx_faction', 'cx_terrain',
         'wk_COST', 'wk_装甲', 'wk_盾牌', 'wk_盾耐久', 'wk_最高速度', 'wk_推进容量', 'wk_推进器冷却', 'wk_载重量',
         'wk_机载量', 'wk_紧急返回', 'wk_倒地值', 'wk_地形', 'wk_插槽数',
         '模型打包值', '模型目录', '模型来源', 'wiki武器数']
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    L = ['#' + ','.join(H) + ',',
         '# 主键 = 練度ID（= msma_model.csv / msma_settings.csv 的行键）；wiki 页面 = 中日对照表给出的真实页名,',
         '# cx_* = unpackdat/codex/data/units.json；wk_* = datatables/wiki/wiki_ms_stats.csv（日文面板，与游戏面板口径一致）,',
         '# 模型打包值 = 第 69 列要填的数（A*1e8+B*1e6+C*100+NN）；模型来源：实测确认/UI表真值/人工口径/代号表命中,',]
    L += [','.join(x) + ',' for x in out]
    open(OUT, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    print('已写 %s' % OUT)
    print('覆盖：codex %d ｜ wiki面板 %d ｜ wiki武器 %d ｜ 已定模型号 %d（共 %d）'
          % (n_cx, n_ws, n_wp, n_mm, len(entries)))
    print('\n=== 抽样（前 6 台）===')
    for x in out[:6]:
        print('  %-9s %-14s %-14s 装甲=%-5s/%s 速度=%-5s/%s 模型=%s' %
              (x[0], x[1][:12], x[2][:12], x[8], x[22], x[10], x[24], x[33] or '-'))
    return 0


if __name__ == '__main__':
    sys.exit(main())
