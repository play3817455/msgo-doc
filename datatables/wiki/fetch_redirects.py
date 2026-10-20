# -*- coding: utf-8 -*-
"""fetch_redirects.py —— 跟随 #重定向 补抓目标页，解决"高达OLX 只是重定向"造成的漏解析。

只抓 cache 里还没有的目标页；抓完请再跑 parse_cache.py。
用法：python datatables/wiki/fetch_redirects.py
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fetch_wiki_weapons as fw   # 复用 get_wikitext（API→raw 退避 + 限速 + 缓存）；它会接管 stdout 编码


def norm(s):
    s = str(s or '').replace('高达', '敢达').replace('高達', '敢达')
    s = re.sub(r'[\s_　]+', '', s)
    s = s.replace('（', '(').replace('）', ')').lower()
    return s


def main():
    tab = json.load(open(os.path.join(HERE, os.pardir, os.pardir, 'unpackdat', 'codex',
                                      '机动战士敢达OL机体名称中日对照表.json'), encoding='utf-8'))['entries']
    cache = {norm(f[:-4]): f for f in os.listdir(fw.CACHE) if f.endswith('.txt')}
    stats = {norm(l.rstrip(',').split(',')[0])
             for l in open(os.path.join(HERE, 'wiki_ms_stats.csv'), encoding='utf-8-sig', errors='replace').read().splitlines()
             if l.strip() and not l.startswith('#')}
    targets = set()
    for x in tab:
        n = norm(x.get('wiki_name'))
        if n not in cache or n in stats:
            continue
        t = open(os.path.join(fw.CACHE, cache[n]), encoding='utf-8').read()
        m = re.search(r'重定向\s*\[\[\s*([^\]|]+)', t)
        if m:
            targets.add(m.group(1).strip())
    targets = sorted(targets)
    missing = [t for t in targets if norm(t) not in cache]
    print('重定向目标 %d 个 ｜ 其中 cache 缺 %d 个，开始抓取' % (len(targets), len(missing)))
    if missing:
        fw.get_wikitext(missing)
    print('完成。请再跑 python datatables/wiki/parse_cache.py 重新解析。')
    return 0


if __name__ == '__main__':
    sys.exit(main())
