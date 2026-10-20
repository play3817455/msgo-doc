# -*- coding: utf-8 -*-
"""Dump raw cached wikitext lines around a marker for a given page."""
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cache')

def find_file(page):
    for n in os.listdir(CACHE):
        if n.endswith('.txt') and n[:-4] == page:
            return os.path.join(CACHE, n)
    return None

def main():
    page = sys.argv[1]
    markers = sys.argv[2:]
    p = find_file(page)
    if not p:
        print('NOT FOUND', page)
        return
    with open(p, encoding='utf-8') as f:
        lines = f.read().replace('\r\n', '\n').split('\n')
    print('# file', p, len(lines), 'lines')
    if not markers:
        for i, l in enumerate(lines, 1):
            print('%4d| %s' % (i, l))
        return
    hits = [i for i, l in enumerate(lines) if any(m in l for m in markers)]
    print('# marker hits:', hits)
    for h in hits:
        lo = max(0, h - 6); hi = min(len(lines), h + 10)
        print('-' * 60)
        for i in range(lo, hi):
            print('%4d| %s' % (i + 1, lines[i]))

if __name__ == '__main__':
    main()
