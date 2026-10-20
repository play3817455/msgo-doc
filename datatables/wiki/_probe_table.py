# -*- coding: utf-8 -*-
"""Debug one cached page: dump each wikitable's headers + first rows via parse_cache.tables()."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding='utf-8')
import parse_cache as P

CACHE = P.CACHE

def main():
    page = sys.argv[1]
    text = open(os.path.join(CACHE, page + '.txt'), encoding='utf-8').read()
    for ti, (headers, rows) in enumerate(P.tables(text)):
        if headers and '威力' not in [P.canon_hdr(h) for h in headers]:
            continue
        print('=' * 70)
        print('table#%d headers(%d)=' % (ti, len(headers)), headers)
        for ri, r in enumerate(rows[:6]):
            print('  row%d len=%d' % (ri, len(r)), r)
    print('#' * 70)
    ms = P.parse_ms(page, text)
    for r in P.parse_weapons(page, text, ms):
        print('  W %-26s 威力=%-8s 集弹=%-6s 射程=%-6s 装填=%-6s 锁定=%-6s' % (
            r['武器名'], r.get('威力'), r.get('集弹性能'), r.get('射程距离'),
            r.get('装填时间'), r.get('锁定')))

if __name__ == '__main__':
    main()
