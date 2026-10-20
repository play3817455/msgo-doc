# -*- coding: utf-8 -*-
"""
fetch_wiki_weapons.py —— 从「高达WIKI（bwiki）」抓取**每个机体的武器性能数据**，作为 #36 `item/weapon_battle_detail.csv`
（WEAPON_BATTLE_DETAIL）与 #37 `item/weapon_settings.csv`（WEAPON_SETTING）的**数值来源**。

为什么用它：本地资产（`unpackdat/`）与 `codex` 都**没有武器数值**（侦查见 `01-列注释/37-37-WEAPON_SETTING.md`），
而 wiki 单机体页的「武器-性能」表正好是 #36 要的那些字段（见下方字段映射）。

字段映射（wiki → #36 的 11 个属性，依据见 `datatables/11-资料站武器字段映射.md`）：
    威力       → POWER          （int）
    射程距离   → RANGE          （float）
    集弹性能   → STABILITY      （"集弹"=弹道散布）
    连射速度   → RAPIDDELAY
    （装填时间/装填性能）→ RELOAD / COOLTIME（两者关系待定案）
    锁定       → LOCKON_CAM
    红锁距离   → HIGH_LOCKON    （★名字级吻合 HIGH_LOCKON_RANGE）
    诱导距离   → （待定）
    倒地值 / 重量 / 弹数 / 射击模式 → #37 的对应列（待定案）

用法：
    python fetch_wiki_weapons.py --dump "高达OL强袭自由敢达"     # 看原始 wikitext（定解析用）
    python fetch_wiki_weapons.py --page "高达OL强袭自由敢达"     # 单页解析
    python fetch_wiki_weapons.py --limit 10                    # 前 10 个机体页
    python fetch_wiki_weapons.py --all                         # 全量（AppPrefix=高达OL 的所有页）
输出：`wiki_ms_weapons.csv`（UTF-8 BOM，给 Excel 友好；解析结果一机体多行）
"""
import io
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

API = 'https://wiki.biligame.com/gundam/api.php'
RAW = 'https://wiki.biligame.com/gundam/index.php'
BASE = 'https://wiki.biligame.com/gundam/'
# ★bilibili WAF 会对脚本 UA/高频请求返回 567 ⇒ 用浏览器 UA + 退避 + 限速
UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36')
HDR = {'User-Agent': UA, 'Accept': 'application/json,text/html,*/*',
       'Accept-Language': 'zh-CN,zh;q=0.9', 'Referer': BASE}
SLEEP = 1.2          # 每次请求间隔（秒）—— 被限流时调大
PREFIX = '高达OL'
HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, 'cache')
OUT = os.path.join(HERE, 'wiki_ms_weapons.csv')


def cache_path(title):
    return os.path.join(CACHE, re.sub(r'[\\/:*?"<>|]', '_', title) + '.txt')

# wiki 武器模板里要抽的字段（原名 → 输出列名）
WEAPON_FIELDS = [
    ('重量', '重量'), ('弹数', '弹数'), ('射击模式', '射击模式'), ('倒地值', '倒地值'),
    ('威力', '威力'), ('集弹性能', '集弹性能'), ('连射速度', '连射速度'),
    ('射程距离', '射程距离'), ('装填性能', '装填性能'), ('装填时间', '装填时间'),
    ('锁定', '锁定'), ('红锁距离', '红锁距离'), ('诱导距离', '诱导距离'),
    ('效果范围', '效果范围'), ('锁定范围', '锁定范围'),
]
# 机体基础性能字段
MS_FIELDS = ['名称', '序号', '势力', '类型', 'COST', 'TIME', '装甲', '盾牌', '最高速度',
             '推进容量', '推进器冷却', '载重量', '紧急归投数量', '机体倒地值', '地形适应']


def _get(url, as_json=False):
    req = urllib.request.Request(url, headers=HDR)
    last = None
    for i, wait in enumerate([3, 8, 20, 45]):
        try:
            with urllib.request.urlopen(req, timeout=45) as r:
                b = r.read().decode('utf-8', 'replace')
                return json.loads(b) if as_json else b
        except Exception as e:
            last = e
            print('   ! 重试 %d（%s），等 %ds' % (i + 1, e, wait))
            time.sleep(wait)
    raise last


def api(params):
    p = dict(params)
    p['format'] = 'json'
    p['formatversion'] = '2'
    return _get(API + '?' + urllib.parse.urlencode(p), as_json=True)


def raw_wikitext(title):
    """备用端点：index.php?action=raw（API 被 WAF 拦时用）"""
    return _get(RAW + '?' + urllib.parse.urlencode({'title': title, 'action': 'raw'}))


def all_pages():
    """全量机体页清单（带磁盘缓存，避免每次都打 allpages）"""
    os.makedirs(CACHE, exist_ok=True)
    fp = os.path.join(CACHE, '_allpages.json')
    if os.path.exists(fp):
        return json.load(open(fp, encoding='utf-8'))
    out, cont = [], None
    while True:
        p = {'action': 'query', 'list': 'allpages', 'apprefix': PREFIX, 'aplimit': '500'}
        if cont:
            p['apcontinue'] = cont
        d = api(p)
        out += [x['title'] for x in d['query']['allpages']]
        cont = d.get('continue', {}).get('apcontinue')
        time.sleep(SLEEP)
        if not cont:
            break
    json.dump(out, open(fp, 'w', encoding='utf-8'), ensure_ascii=False)
    return out


def get_wikitext(titles):
    """逐个标题取 wikitext（★批量 titles=a|b|c 会被 bilibili WAF 拦成 567），带本地缓存与限速"""
    os.makedirs(CACHE, exist_ok=True)
    res, miss = {}, 0
    for n, t in enumerate(titles):
        fp = cache_path(t)
        if os.path.exists(fp):
            res[t] = open(fp, encoding='utf-8').read()
            continue
        txt = None
        try:                                   # ① 首选 API
            d = api({'action': 'query', 'prop': 'revisions', 'rvprop': 'content',
                     'rvslots': 'main', 'titles': t})
            for pg in d.get('query', {}).get('pages', []):
                revs = pg.get('revisions') or []
                if revs:
                    txt = revs[0]['slots']['main']['content']
        except Exception as e:
            print('   ! API 失败 %s（%s）→ 试 raw 端点' % (t, e))
        if txt is None:
            try:                               # ② 备用 raw 端点
                txt = raw_wikitext(t)
            except Exception as e:
                print('   !! 放弃 %s（%s）' % (t, e))
                continue
        if txt and txt.strip():
            res[t] = txt
            open(fp, 'wb').write(txt.encode('utf-8'))
            miss += 1
        time.sleep(SLEEP)
        if (n + 1) % 25 == 0:
            print('   ... %d/%d' % (n + 1, len(titles)))
    print('   本次新抓 %d 页（其余走缓存）' % miss)
    return res


def field(block, key):
    """从模板块里取 `|key=值` 或 `key=值`"""
    m = re.search(r'(?:\||^)\s*' + re.escape(key) + r'\s*=\s*([^|}\n]*)', block)
    return m.group(1).strip() if m else ''


def parse_page(title, text):
    """返回 (ms_info:dict, rows:list[dict])"""
    ms = {'页面': title}
    # 基础性能：取 {{高达OL基础性能 ... }} 块里的字段
    m = re.search(r'\{\{\s*高达OL基础性能(.*?)\}\}', text, re.S)
    blk = m.group(1) if m else text[:4000]
    for k in MS_FIELDS:
        v = field(blk, k)
        if v:
            ms[k] = v
    # 武器：每个 {{高达OL武器模板 ... }} 块
    rows = []
    for wm in re.finditer(r'\{\{\s*高达OL武器模板(.*?)\}\}', text, re.S):
        b = wm.group(1)
        r = {'页面': title, '机体序号': ms.get('序号', '')}
        # 名称：模板第一个无名参数（|名称 或 |无名）
        nm = re.match(r'\s*\|\s*([^=|\n}]+)', b)
        r['武器名'] = (field(b, '武器名称') or field(b, '名称') or (nm.group(1).strip() if nm else '')).strip()
        for wk, col in WEAPON_FIELDS:
            r[col] = field(b, wk)
        if r['武器名'] or any(r.get(c) for _, c in WEAPON_FIELDS):
            rows.append(r)
    return ms, rows


def dump(title):
    d = get_wikitext([title])
    if title not in d:
        print('!! 取不到页面：', title)
        return 1
    t = d[title]
    print('总长度', len(t))
    print('--- 页头 900 字（含基础性能块）---')
    print(t[:900])
    i = t.find('高达OL武器模板')
    print('首个武器模板位置', i)
    print('--- 从武器模板起 2000 字 ---')
    print(t[i:i + 2000] if i >= 0 else t[:2000])
    return 0


def main():
    a = sys.argv[1:]
    if not a:
        print(__doc__)
        return 0
    if a[0] == '--dump':
        return dump(a[1])
    if a[0] == '--api':      # 通用查询：--api "action=query;list=search;srsearch=武器ID;srlimit=20"（用 ; 分隔，避免 shell 转义）
        q = {}
        for kv in a[1].split(';'):
            k, _, v = kv.partition('=')
            if k:
                q[k] = v
        print(json.dumps(api(q), ensure_ascii=False, indent=1)[:6000])
        return 0
    allp = all_pages()
    print('wiki 上 `%s*` 页面共 %d 个' % (PREFIX, len(allp)))
    if a[0] == '--page':
        todo = [a[1]]
    elif a[0] == '--limit':
        todo = allp[:int(a[1])]
    elif a[0] == '--fill':                     # ★断点续抓：只抓还没缓存的页
        pending = [t for t in allp if not os.path.exists(cache_path(t))]
        n = int(a[1]) if len(a) > 1 else 120
        print('未抓 %d 页 ⇒ 本次最多抓 %d 页（剩 %d 页留待下次）'
              % (len(pending), n, max(0, len(pending) - n)))
        todo = pending[:n]
    else:                                       # --all
        todo = allp
    print('本次抓取 %d 页...' % len(todo))
    get_wikitext(todo)
    # ★每次都从"全部已缓存页"重建 CSV（避免只写本批、覆盖掉之前抓的）
    have = [t for t in allp if os.path.exists(cache_path(t))]
    print('缓存累计 %d 页 ⇒ 全量重建 CSV' % len(have))
    texts = get_wikitext(have)
    allrows, allms = [], []
    for t in have:
        if t not in texts:
            continue
        ms, rows = parse_page(t, texts[t])
        allms.append(ms)
        allrows += rows
        print('   %-34s 武器 %d 条' % (t, len(rows)))
    cols = ['页面', '机体序号'] + [c for _, c in WEAPON_FIELDS]
    lines = ['#' + ','.join(cols) + ',',
             '# 来源：bwiki 高达WIKI「%s*」机体页（{{高达OL武器模板}}），供 #36 WEAPON_BATTLE_DETAIL / #37 WEAPON_SETTING 取数用' % PREFIX,
             '# 生成：datatables/wiki/fetch_wiki_weapons.py']
    for r in allrows:
        lines.append(','.join(str(r.get(c, '')).replace(',', '，') for c in cols) + ',')
    with open(OUT, 'wb') as f:
        f.write(('\r\n'.join(lines) + '\r\n').encode('utf-8-sig'))
    print('写入 %s：机体 %d 页 / 武器 %d 条' % (OUT, len(allms), len(allrows)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
