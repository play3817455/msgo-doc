# -*- coding: utf-8 -*-
"""
parse_cache.py —— **离线**全量解析 bwiki 高达WIKI 的 1036 个机体页缓存（`wiki/cache/`），产出两张表：

  `wiki_ms_weapons.csv`  每行一把武器（含威力/射程/集弹/连射/装填/锁定/红锁距离…）
  `wiki_ms_stats.csv`    每行一台机体的**面板数值**（装甲/最高速度/推进容量/推进器冷却/机载量/紧急返回性能/倒地值…）

★站上有**两种格式**，都要吃：
  ① **模板格式**（新页）：`{{高达OL基础性能}}` + `{{高达OL武器模板}}`
  ② **wikitable 格式**（老页，占多数）：`{| class="wikitable"` 手写表；武器表用 `!名称 !重量 … !威力 …` 表头，
     每行一格一行；**红锁距离写在名称格的 `<sup>红锁距离：180</sup>` 里**；机体数值则是 `装甲 | 值 | 值2` 的键值网格。

用法：python parse_cache.py            # 只解析（无网络请求）
"""
import io
import os
import re
import sys

# ★只在**直接运行**时改 stdout 编码：本模块会被 `_probe_*.py` / 未来的生成器 import，
#   而 `io.TextIOWrapper` 被回收时会**关掉底层 buffer** ⇒ import 就再也 print 不出来了。
if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, 'cache')
OUT_W = os.path.join(HERE, 'wiki_ms_weapons.csv')
OUT_S = os.path.join(HERE, 'wiki_ms_stats.csv')

# 武器表可能的列（按 wiki 表头原名）
WCOL = ['重量', '弹数', '射击模式', '倒地值', '威力', '集弹性能', '连射速度', '射程距离',
        '装填性能', '装填时间', '锁定', '红锁距离', '诱导距离', '效果范围', '锁定范围', '持续时间']
# 模板格式的字段名 → 列名
TMPL_MAP = [('重量', '重量'), ('弹数', '弹数'), ('射击模式', '射击模式'), ('倒地值', '倒地值'),
            ('威力', '威力'), ('集弹性能', '集弹性能'), ('连射速度', '连射速度'),
            ('射程距离', '射程距离'), ('装填性能', '装填性能'), ('装填时间', '装填时间'),
            ('锁定', '锁定'), ('红锁距离', '红锁距离'), ('诱导距离', '诱导距离'),
            ('效果范围', '效果范围'), ('锁定范围', '锁定范围')]
# 机体数值：模板字段 + 表格里的键名（含同义写法）
MS_KEYS = ['序号', '名称', '势力', '类型', '机体类型', 'COST', 'TIME', '手持', '装甲', '盾牌',
           '盾牌拆卸', '护盾耐久值', '最高速度', '推进容量', '推进器冷却', '推进器冷却力',
           '载重量', '机载量', '紧急归投数量', '紧急返回性能', '机体倒地值', '地形适应',
           '插槽数', 'MCOST', 'M-COST', '搬运能力']
# ★老格式页面的键名同义（→ 规范键 MS_KEYS）
MS_SYN = {
    '推进器容量': '推进容量', '推进器容量力': '推进容量',
    '紧急归投性能': '紧急返回性能', '紧急归投数量': '紧急归投数量',
    '适应地形': '地形适应', '地形适应性': '地形适应',
    '盾牌耐久值': '护盾耐久值', '盾牌耐久': '护盾耐久值',
    '推进器冷却': '推进器冷却', '机体倒地值': '机体倒地值',
}
NOT_LABEL = set()


def tmpl_field(block, key):
    m = re.search(r'(?:\||^)\s*' + re.escape(key) + r'\s*=\s*([^|}\n]*)', block)
    return m.group(1).strip() if m else ''


def _is_media(v):
    """图片/文件格（不是数据列）。"""
    return v.startswith('[[File:') or v.startswith('[[file:') or v.startswith('[[文件')


_NUMISH = re.compile(r'^[\d\s,\./%()（）]+$')

# 表头「像武器表」的判据：**必须含 `威力`**（机体数值网格里没有这一栏）+ 至少 3 个已知列名。
# 用于兜住「表头用 `|` 写而不是 `!`」的老页面（实测 35 页 126 张表，否则整表被当键值网格丢掉）。
_HDR_HINT = ('名称', '重量', '弹数', '威力', '射程距离', '装填时间')


def _looks_like_hdr(cells):
    names = [canon_hdr(v) for v, _rs, _cs in cells]
    return '威力' in names and sum(1 for n in names if n in _HDR_HINT) >= 3


def _join_cont(prev, add):
    """数据格换行续写：并进上一格。

    ★两档值的续行**要加分隔符**：页面偶尔漏写左括号，写成一格 `10,500` + 下一行 `11,550)`
    （实测 `高达OL伊夫里特夜战型` 低温刀DⅢ灭绝式），直接接起来就成 `1050011550`
    —— 下游 `first_tier` 读成一千多万 ✗。规矩：前格是**纯数值**且续行**以数字开头** ⇒ 当第二档，
    用 `(` 分隔（`cell()` 会补右括号 ⇒ `10500(11550)` ✓ 与 `800(880)` 写法一致）。
    """
    if prev and _NUMISH.match(prev) and re.match(r'^\s*\d', add):
        return prev + '(' + add
    return (prev + ' ' + add).strip()


def tables(text):
    """产出该页所有 wikitable：(headers, rows)。

    `rows` = list[list[str]]，**按列号落位**（不是「有几个格就顺序排」），续行并入上一格。

    ★★三条版面规矩（2026-10-05 修，此前三条都踩坑）★★
    1. **跨行格**（`| rowspan="2" | 430`）只写在区间第一行 ⇒ 后续行那一格是空的。
       若按「本行格数」从前往后 zip 表头，后续行的值会**整体左移** —— 实测
       `高达OL帕拉斯·雅典娜(重击装备)(国)` 第 2 把武器 `蓄力式腕部2连光束枪` 的
       威力/集弹/射程 会读成 630/640/760（真值 2,600/880/630），`装填时间/锁定` 整格落空。
    2. **跨列格**（`| colspan="3" | 名称`、`| colspan="2" | [[File:…]]`）占多列 ⇒ 要按列号对齐，
       否则表头与数据差一格。同理一行里的多格写法 `! a !! b !! c` / `| a || b` 要拆开。
    3. **老式表格的数据行也用 `!` 开头**（实测 `高达OL陆战型吉姆` 的 100mm机枪 表）⇒
       不能「见到 `!` 就当表头」。规矩：**第一个含 `!` 格的行块是表头行块，其后所有行块都是数据**。
       无 `!` 的表格 = 机体数值的键值网格（`parse_ms` 吃 `headers == []`），保持原样。
    4. **表头块里的续行是页面笔误**（实测 `高达OL兹萨`：`!装填时间` 下面孤零零一行 `時間`）⇒
       表头格的续行**必须丢掉**，否则列名变成 `装填时间 時間`、该列整列落空。
       数据格的续行相反要**并进上一格**（实测 `550` / `(605)` 两行 = 一格 `550 (605)`）。
    5. **图片格不是列**（`| colspan="10" |[[File:…]]`）⇒ 算表头时丢掉，否则一张图变 10 个表头，
       列号整体右移、武器名整表落空（实测 `高达OL杰刚(ECOAS式样·康洛伊机)(国)` 光束步枪表）。
    6. **表头也可能一格都没写 `!`**（`|名称 |重量 … |威力 …`，实测 35 页 126 张表）⇒
       找不到 `!` 块时，退而认「**含 `威力` 且至少 3 个已知列名**」的那个行块为表头
       （机体数值网格里没有 `威力` 栏，不会误认）。
    """
    for m in re.finditer(r'\{\|\s*class="wikitable"(.*?)\n\s*\|\}', text, re.S):
        blocks = []          # [(cells, 是否出现过 ! 格)]；cells = [(值, rowspan, colspan)]
        cur, cur_th = [], False
        for ln in m.group(1).split('\n'):
            s = ln.strip()
            if not s or s.startswith('{|') or s.startswith('|}'):
                continue
            if s.startswith('|-'):
                blocks.append((cur, cur_th))
                cur, cur_th = [], False
                continue
            if s.startswith('!'):
                for piece in s[1:].split('!!'):
                    cur.append(_split_cell(piece))
                cur_th = True
                continue
            if s.startswith('|'):
                for piece in s[1:].split('||'):
                    cur.append(_split_cell(piece))
                continue
            if cur and not cur_th:       # 数据格的续行 → 并入上一格（表头块的续行丢掉，见 docstring 4）
                v, rs, cs = cur[-1]
                cur[-1] = (_join_cont(v, s), rs, cs)
        blocks.append((cur, cur_th))
        hdr_i = next((i for i, (_, th) in enumerate(blocks) if th), None)
        if hdr_i is None:                # 表头没写 `!` 的老页面：按「像武器表表头」认（见 docstring 6）
            hdr_i = next((i for i, (cells, _th) in enumerate(blocks)
                          if _looks_like_hdr(cells)), None)
        if hdr_i is None:
            yield [], _blocks_to_rows(blocks)
            continue
        headers = []
        for v, _rs, cs in blocks[hdr_i][0]:
            if _is_media(v):             # 图片格不是列（见 docstring 5）
                continue
            headers.extend([canon_hdr(v)] * cs)   # 跨列格按列展开（span 内同名）
        yield headers, _blocks_to_rows(blocks[hdr_i + 1:])


def _blocks_to_rows(blocks):
    """行块 → list[list[str]]，按列号落位并**把跨行格续给后续行**。"""
    rows, carry = [], {}
    for cells, _th in blocks:
        carried, nxt = {}, {}
        for c, (v, n) in carry.items():
            carried[c] = v
            if n > 1:
                nxt[c] = [v, n - 1]
        carry = nxt
        cur = dict(carried)
        taken = set(cur)
        for val, rs, cs in cells:
            pos = 0
            while pos in taken:          # 跳过跨行格占住的列
                pos += 1
            keep = '' if _is_media(val) else val
            cur[pos] = keep
            for i in range(cs):
                taken.add(pos + i)
                if rs > 1:
                    carry[pos + i] = [val if (i == 0 and keep) else '', rs - 1]
        rows.append([cur.get(i, '') for i in range(max(cur) + 1)] if cur else [])
    return rows


_ATTRS = re.compile(r'^\s*((?:[A-Za-z][A-Za-z0-9-]*\s*=\s*"[^"]*"\s*)+)\|(.*)$', re.S)
_SPAN = re.compile(r'([A-Za-z][A-Za-z0-9-]*)\s*=\s*"([^"]*)"')


def _split_cell(raw):
    """`rowspan="2" width="2%" colspan="5" | 值` → (值, rowspan, colspan)。

    返回**值**（属性已剥掉）+ 跨行/跨列数（缺省 1）。
    """
    rs = cs = 1
    m = _ATTRS.match(raw)
    if m:
        for k, v in _SPAN.findall(m.group(1)):
            n = int(re.sub(r'\D', '', v) or 1)
            if k.lower() == 'rowspan':
                rs = max(1, n)
            elif k.lower() == 'colspan':
                cs = max(1, n)
        raw = m.group(2)
    return raw.strip(), rs, cs


# ── 表头同义写法 → 规范列名 ────────────────────────────────────────────────
# 来源：把 cache 里所有武器表的表头原字面全量收集后逐个人工核对（见 `_probe_c4_headers.py`）。
# 只收**同一栏的异体写法**（简繁/日文/中文另写/HTML 标签），不把语义不同的栏并进来：
#   · `恢复力`（修理系的治疗量）**不并** 进 `威力` —— 与 `威力` 不同栏，宁缺勿造；
#   · `威力MAX`/`蓄力威力`/`型号`/`类型`/`连射距离`/`射击速度`/`效果时间`/`性能锁定` 同理不并。
HDR_SYN = {
    '弾数': '弹数', '載弹量': '弹数', '载弹量': '弹数', '载弹数': '弹数', '弹量': '弹数',
    '集弾性能': '集弹性能',
    '連射速度': '连射速度',
    '射程距離': '射程距离', '射击距离': '射程距离', '射程': '射程距离',
    '装填時間': '装填时间', 'リロード時間': '装填时间', 'リロード': '装填时间',
    '効果範囲': '效果范围', '効果范围': '效果范围',
    '锁定性能': '锁定', '锁定性能=': '锁定',
    '射击方式': '射击模式',
}


def canon_hdr(h):
    """表头格 → 规范列名（去 HTML 标签/`'''` 粗体 → 同义归一）。"""
    s = re.sub(r'<[^>]*>', '', str(h)).strip()
    s = s.strip("'").strip()
    return HDR_SYN.get(s, s)


_MEDIA = re.compile(r'\[\[(?:文件|File):[^\]]*\]\]')
_DIST = re.compile(r'(红锁距离|诱导距离)[:：]?\s*([\d,]+)')


def parse_weapons(title, text, ms):
    """两种格式一起收，返回 list[dict]"""
    rows = []
    # ① 模板格式
    for wm in re.finditer(r'\{\{\s*高达OL武器模板(.*?)\}\}', text, re.S):
        b = wm.group(1)
        nm = re.match(r'\s*\|\s*([^=|\n}]+)', b)
        r = {'数据格式': '模板', '武器名': (tmpl_field(b, '武器名称') or (nm.group(1).strip() if nm else '')).strip()}
        for wk, col in TMPL_MAP:
            r[col] = tmpl_field(b, wk)
        if r['武器名'] or any(r.get(c) for _, c in TMPL_MAP):
            rows.append(r)
    # ② wikitable 格式（表头里必须有「威力」）
    for headers, trows in tables(text):
        if not headers or '威力' not in headers:
            continue
        hdr = ['武器名' if canon_hdr(h) == '名称' else canon_hdr(h) for h in headers]
        # ★表头之外的**前置列**（武器图片格）：数据行比表头宽，按「右对齐」还原列号。
        #   实测：帕拉斯页 数据 12 列 / 表头 11 列 ⇒ 前置 1 列（图片）；
        #        修理喷枪页 表头 9 列（`colspan="3" | 名称`）/ 数据 9 列（图片 colspan=2）⇒ 前置 0 列。
        off = max(0, max([len(c) for c in trows] or [0]) - len(hdr))
        for cells in trows:
            d = {}
            for c, v in enumerate(cells):
                i = c - off
                if 0 <= i < len(hdr):
                    nm = hdr[i]
                    if nm not in d or (not d[nm] and v):   # 跨列同名格：取非空者
                        d[nm] = v
            name = d.pop('武器名', '').strip()
            # ★名字里常混着**装饰**：`<sup>红锁距离：180</sup>`、`[[文件:诱导箭头G1.png|…]]诱导距离：200`。
            #   红锁/诱导距离抽成**自己的列**（WCOL 里有），名字里要擦干净 —— 名字是要拿去和客户端
            #   武器名对上的，留着文件标记就永远对不上（实测 `高达OL沙扎比` 光束战斧 6 把、`高达OL敢达(Ver.3.0)`）。
            for k, v in _DIST.findall(name + ' ' + ' '.join(cells)):
                col = '红锁距离' if k == '红锁距离' else '诱导距离'
                if not d.get(col):
                    d[col] = v
            name = _MEDIA.sub('', name)
            name = _DIST.sub('', name)
            name = re.sub(r'<br\s*/?>', ' ', name, flags=re.I)   # 名字里的 `<br />` 是换行标记，别当分隔符
            name = re.sub(r'<sup>.*?</sup>', '', name)
            name = re.sub(r'<[^>]*>', '', name)
            name = re.sub(r'[（(]\s*[)）]', '', name)     # 残留的空括号
            name = re.sub(r'\s+', ' ', name).strip()
            if not name:
                continue
            d['武器名'] = name
            d['数据格式'] = '表格'
            rows.append(d)
    for r in rows:
        r['页面'] = title
        r['机体序号'] = ms.get('序号', '')
    return rows


def parse_ms(title, text):
    ms = {}
    m = re.search(r'\{\{\s*高达OL基础性能(.*?)\}\}', text, re.S)
    if m:
        for k in MS_KEYS:
            v = tmpl_field(m.group(1), k)
            if v:
                ms.setdefault(k, v)
    # 表格格式的键值网格（无表头的表）
    for headers, trows in tables(text):
        if headers:
            continue
        cells = [c for r in trows for c in r if c and not c.startswith('[[文件')]
        i = 0
        while i < len(cells):
            if cells[i] in MS_KEYS:
                key = cells[i]
                vals = []
                j = i + 1
                while j < len(cells) and cells[j] not in MS_KEYS and len(vals) < 2:
                    if re.match(r'^[\d,\.\-/]+$', cells[j]) or cells[j] in ('可', '不可', '有', '无'):
                        vals.append(cells[j])
                    j += 1
                if vals:
                    ms.setdefault(key, vals[0])
                    if len(vals) > 1:
                        ms.setdefault(key + '_2', vals[1])
                i = j
            else:
                i += 1
    # ★老格式：`! 装甲` 表头键 + 值（带表头的 wikitable）
    for k, v in parse_ms_old(text).items():
        ms.setdefault(k, v)
    return ms


def parse_ms_old(text):
    """老页面：`! 键` 表头（行首 !）后跟值；键名经 MS_SYN 归一到规范名。"""
    ms, key = {}, None
    for ln in text.split('\n'):
        s = ln.strip()
        if not s:
            continue
        if s.startswith('{|') or s.startswith('|}') or s.startswith('|-') or s.startswith('=='):
            key = None
            continue
        m = re.match(r'^[!|]\s*(.+?)\s*$', s)
        if m:
            canon = MS_SYN.get(m.group(1), m.group(1))
            if canon in MS_KEYS:
                key = canon
                continue
        if key is None:
            continue
        v = s[1:].strip() if s.startswith('|') else s
        v = re.sub(r'<[^>]*>', '', v).strip()
        if not v or v == '|':
            continue
        if re.match(r'^[\d,\.\-/]+$', v):
            if key not in ms:
                ms[key] = v
            elif key + '_2' not in ms:
                ms[key + '_2'] = v
        else:
            if key not in ms:
                ms[key] = v
    return ms


TEXT_COLS = {'页面', '数据格式', '武器名', '名称', '势力', '类型', '机体类型', '地形适应', '手持',
             '盾牌拆卸', '搬运能力', '机体倒地值'}
_BR = re.compile(r'<br\s*/?>', re.I)


def cell(v, col):
    """写 CSV 前清洗：去 HTML 标签；数字列去千分位逗号；文本列逗号换全角（保护 CSV 结构）。

    ★★标签剥离时**必须保住两档值的边界**★★：页面写 `840<br/><span style="color:red">872</span>`
    （无印值 / 强化值两档），若把标签直接删掉就成了 `840872` —— 下游 `first_tier` 取第一档会读成
    `840872`（✗ 数值直接翻千倍）。规矩：`<br/>` 当**分隔符**换成 `(` 并补右括号 ⇒ `840(872)`，
    与 `weapon_client_raw.first_tier` 文档里的 `800(880)` 写法一致。

    ★补右括号只看**半角** `(`/`)`（全角 `（`/`）` 别掺进来）：页面名 `钢加农(喷射导弹发射器式样）`
    半角左括号配全角右括号，若按半角配平会凭空多出一个 `)`，把「页面」列写坏（实测踩过）。
    """
    s = _BR.sub('(', str(v))
    s = re.sub(r'<[^>]*>', '', s)
    s = re.sub(r'\s+', ' ', s).strip()
    s = re.sub(r'\(\s*\(', '(', s)
    if s.count('(') > s.count(')') + s.count('）'):
        s += ')' * (s.count('(') - s.count(')') - s.count('）'))
    if col in TEXT_COLS:
        return s.replace(',', '，')
    return s.replace(',', '').replace('，', '').replace(' ', '')


def main():
    def cache_file(t):
        return os.path.join(CACHE, re.sub(r'[\\/:*?"<>|]', '_', t) + '.txt')

    fs = [f for f in os.listdir(CACHE) if f.endswith('.txt')]
    fs.sort()
    wrows, srows = [], []
    for f in fs:
        title = f[:-4]
        text = open(os.path.join(CACHE, f), encoding='utf-8').read()
        seen = set()
        while text.lstrip().startswith(('#重定向', '#redirect', '#REDIRECT')):   # ★跟随重定向
            m = re.search(r'\[\[\s*([^\]|]+)', text)
            if not m:
                break
            tgt = m.group(1).strip()
            if tgt in seen or not os.path.exists(cache_file(tgt)):
                break
            seen.add(tgt)
            text = open(cache_file(tgt), encoding='utf-8').read()
        ms = parse_ms(title, text)
        if ms or '武器-性能' in text:
            ms['页面'] = title
            ms['数据格式'] = '模板' if '高达OL基础性能' in text else '表格'
            srows.append(ms)
        for r in parse_weapons(title, text, ms):
            wrows.append(r)
    # 写武器表
    wcols = ['页面', '机体序号', '数据格式', '武器名'] + WCOL
    wl = ['#' + ','.join(wcols) + ',',
          '# 来源：bwiki 高达WIKI 机体页（{{高达OL武器模板}} + wikitable 两种格式）',
          '# 生成：datatables/wiki/fetch_wiki_weapons.py（抓取）+ parse_cache.py（离线解析）']
    for r in wrows:
        wl.append(','.join(cell(r.get(c, ''), c) for c in wcols) + ',')
    open(OUT_W, 'wb').write(('\r\n'.join(wl) + '\r\n').encode('utf-8-sig'))
    # 写机体数值表
    scols = ['页面', '数据格式'] + [k for k in MS_KEYS if k not in ('机体类型',)] + ['机体类型']
    scols = [c for c in scols] + [c for c in ms_keys_extra(srows)]
    scols = list(dict.fromkeys(scols))
    sl = ['#' + ','.join(scols) + ',',
          '# 来源：bwiki 高达WIKI 机体页（{{高达OL基础性能}} + wikitable 键值网格）',
          '# 用途：★#34 MSMA_BATTLE_DETAIL 的面板数值（装甲/最高速度/推进容量/推进器冷却/载重量/紧急返回性能）对照来源★']
    for r in srows:
        sl.append(','.join(cell(r.get(c, ''), c) for c in scols) + ',')
    open(OUT_S, 'wb').write(('\r\n'.join(sl) + '\r\n').encode('utf-8-sig'))
    print('武器表 %s：%d 行（模板 %d / 表格 %d）' % (
        OUT_W, len(wrows),
        len([r for r in wrows if r['数据格式'] == '模板']),
        len([r for r in wrows if r['数据格式'] == '表格'])))
    print('机体表 %s：%d 行（模板 %d / 表格 %d）' % (
        OUT_S, len(srows),
        len([r for r in srows if r.get('数据格式') == '模板']),
        len([r for r in srows if r.get('数据格式') == '表格'])))
    print('武器表列覆盖：')
    for c in WCOL:
        print('   %-8s %d' % (c, len([r for r in wrows if str(r.get(c, '')).strip()])))
    print('机体表列覆盖：')
    for c in scols:
        print('   %-12s %d' % (c, len([r for r in srows if str(r.get(c, '')).strip()])))
    return 0


def ms_keys_extra(rows):
    out = []
    for r in rows:
        for k in r:
            if k.endswith('_2') and k not in out:
                out.append(k)
    return sorted(out)


if __name__ == '__main__':
    sys.exit(main())
