# -*- coding: utf-8 -*-
"""C4：sidecar 新旧对比（重跑 `gen_weapon_set_wiki.py` 前后的「ID ↔ 武器名」是否漂移）。

**这是落库前的头号安全检查**：sidecar 的 ID 是 `2+練度ID[1:5]+sub4`，武器名按 wiki 页面
**出现序**配前 N 个（`min(len(ids), len(weapons))`）。新解析器多解析出 2,571 行 ⇒ 若页面内
**插入**了新行，前 N 个就可能换人 ⇒ 全部武器的「名字 / 数值」会**整体搬家**到别的 ID。

判据：
  · id 集合变化；
  · 同名 id 上「武器名」是否变（变 = 可疑，要看新名是**补漏**还是**错位**）；
  · 值列变化（正常，解析器修的就是这个）。
"""
import collections
import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import weapon_client_raw as RAW  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
NEW = os.path.join(HERE, 'names', '武器分配明细.csv')
OLD = os.path.join(HERE, '_probe_sidecar_old.csv')


def rd(p):
    return [r for r in csv.reader(open(p, encoding='utf-8-sig', errors='replace')
                                  .read().replace('\r\n', '\n').split('\n'))
            if r and any(x.strip() for x in r) and not r[0].strip().startswith('#')]


def nk(k):
    k = k.strip()
    return k.zfill(8) if k.isdigit() and len(k) <= 8 else k


old = {nk(r[1]): r for r in rd(OLD) if len(r) > 1 and r[1].strip().isdigit()}
new = {nk(r[1]): r for r in rd(NEW) if len(r) > 1 and r[1].strip().isdigit()}
print('旧 sidecar 行 %d（唯一ID %d）／新 sidecar 行 %d（唯一ID %d）'
      % (len(rd(OLD)), len(old), len(rd(NEW)), len(new)))

only_o = sorted(set(old) - set(new))
only_n = sorted(set(new) - set(old))
print('只在旧：%d %s' % (len(only_o), [(k, old[k][5], old[k][3]) for k in only_o[:10]]))
print('只在新：%d %s' % (len(only_n), [(k, new[k][5], new[k][3]) for k in only_n[:10]]))

COLS = {6: '重量', 7: '弹数', 8: '模式', 10: '威力', 11: '集弹', 12: '连射', 13: '射程',
        14: '装填性能', 15: '装填时间', 16: '锁定', 17: '红锁'}
nm_diff, val_diff, unparsed_diff = [], [], []
for k in sorted(set(old) & set(new)):
    a, b = old[k], new[k]
    if a[5].strip() != b[5].strip():
        nm_diff.append((k, a[5], b[5], a[3], b[3]))
    va = [(i, a[i] if len(a) > i else '') for i in COLS]
    vb = [(i, b[i] if len(b) > i else '') for i in COLS]
    if [(i, RAW.first_tier(v)) for i, v in va] != [(i, RAW.first_tier(v)) for i, v in vb]:
        val_diff.append((k, a[5], [(COLS[i], x, y) for (i, x), (_, y) in zip(va, vb) if x != y]))
    if any((a[i] if len(a) > i else '') and not RAW.first_tier(a[i]) for i in COLS) != \
       any((b[i] if len(b) > i else '') and not RAW.first_tier(b[i]) for i in COLS):
        unparsed_diff.append(k)

print()
print('★ ID↔武器名 漂移：%d 个 id' % len(nm_diff))
for k, x, y, cx, cy in nm_diff[:30]:
    print('   %-11s 旧「%s」[%s] → 新「%s」[%s]' % (k, x, cx, y, cy))
print('值列（威力/集弹/连射/射程/装填/锁定/红锁）有变：%d 个 id' % len(val_diff))
cc = collections.Counter(c for _, _, ds in val_diff for c, _, _ in ds)
print('   按列统计:', dict(cc.most_common()))
for k, nm, ds in val_diff[:12]:
    print('   %-11s %-14s %s' % (k, nm[:14], ds))
print('非数字值出现/消失的 id：%d %s' % (len(unparsed_diff), unparsed_diff[:8]))

# 关键列填充率对比（新旧都算）
print()
print('=== 关键列填充率（旧 → 新）===')
for i, nm in ((10, '威力'), (11, '集弹'), (12, '连射'), (13, '射程'), (14, '装填性能'),
              (15, '装填时间'), (16, '锁定'), (17, '红锁')):
    c_old = sum(1 for r in old.values() if i < len(r) and RAW.first_tier(r[i]))
    c_new = sum(1 for r in new.values() if i < len(r) and RAW.first_tier(r[i]))
    c_both = sum(1 for k in set(old) & set(new)
                 if i < len(new[k]) and RAW.first_tier(new[k][i])
                 and not (i < len(old[k]) and RAW.first_tier(old[k][i])))
    print('   col%-3d %-8s %4d → %4d   （同名 id 上新增 %d）' % (i, nm, c_old, c_new, c_both))

# ── ★决定性检查：解析器给的**行序**是否忠于页面文字序 ────────────────────────
# sidecar 的「第 i 把 ↔ 第 i 个 sub4」是**按序配**的（无别证），所以解析器行序必须
# 与页面里武器名的**出现序**一致。判据：每个页面的武器名，在 wikitext 里**从头向后**
# 扫到的位置必须单调不减（同页复用名按上一位置往后找）。
print()
print('=== 行序保真（每页武器名在 wikitext 中的位置单调不减）===')
sys.path.insert(0, os.path.join(HERE, 'wiki'))
import parse_cache as PC  # noqa: E402  （import 期不改 stdout，见其 `__main__` 守卫）

CACHE = os.path.join(HERE, 'wiki', 'cache')
bad_pages, n_pages, n_rows_, miss = [], 0, 0, 0
for fn in sorted(os.listdir(CACHE)):
    if not fn.endswith('.txt'):
        continue
    title = fn[:-4]
    text = open(os.path.join(CACHE, fn), encoding='utf-8').read()
    try:
        ms = PC.parse_ms(title, text)
        rows = list(PC.parse_weapons(title, text, ms))
    except Exception as e:
        print('   ! %s 解析异常 %s' % (title, e))
        continue
    if not rows:
        continue
    n_pages += 1
    pos = 0
    viol = []
    for r in rows:
        nm = (r.get('武器名') or '').strip()
        if not nm:
            continue
        n_rows_ += 1
        j = text.find(nm, pos)
        if j < 0:
            miss += 1
            j = text.find(nm)
            if j >= 0 and j < pos:
                viol.append((nm, pos, j))
            continue
        pos = j
    if viol:
        bad_pages.append((title, viol[:3]))
print('扫描 %d 页 / %d 行；名字在文中找不到（或两次出现）%d；**顺序违规**页 %d'
      % (n_pages, n_rows_, miss, len(bad_pages)))
for title, v in bad_pages[:15]:
    print('   %s %s' % (title[:34], v))

# ── 旁证：MAIN 槽的类别分布（近战当主武器 = 可疑；新解析若更忠于页面，这一类应更少）──
print()
print('=== MAIN 槽类别分布（旧 → 新）===')
for tag, d in (('旧', old), ('新', new)):
    # 同一練度ID 多行 ⇒ MAIN 行是 slot(col2)=MAIN 的那一行
    main = collections.Counter(r[3].strip() for r in d.values()
                               if len(r) > 4 and r[2].strip() == 'MAIN')
    print('   %s MAIN %d 把：%s' % (tag, sum(main.values()), dict(main.most_common())))
