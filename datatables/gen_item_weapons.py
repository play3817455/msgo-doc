# -*- coding: utf-8 -*-
"""gen_item_weapons.py —— 往 #65 `item/item.csv`（ITEM 物品总表）补武器行。

为什么必须补：`#1 MSMA_WEAPONSET` 的 col2 = 武器ID，消费方 `sub_581690` 会拿它去
**ITEM 表**（`dword_11E3F08`）查物品；**查不到就静默跳过**（不报错）⇒ 武器不会出现在机体上。
⇒ 所以最小闭环 = ① ITEM 里有该武器ID ② `#1` col2 指向它 ③ `#1` col6=1

列语义（`sub_593B70`，见 01-列注释/78-65-ITEM.md）：
    col0 = 物品ID（主键）｜ col2 = 名称 ｜ col3 = 说明 ｜ col4 = 类型（写名称，如 WEAPON）
来源（可回溯）：`unpackdat/settings/weapon_wrestle.csv`（`アイテムID,アイテム名(自動),…` 8 把近接格闘武器）

方言铁律：UTF-8 无 BOM、CRLF、数据行保留尾逗号、# 开头整行跳过。
"""
import io
import os
import shutil
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, 'unpackdat', 'settings', 'weapon_wrestle.csv')
OUT = os.path.join(ROOT, 'server', 'datafiles', 'lounge', 'item', 'item.csv')


def main():
    # ① 源：近接格闘武器表（アイテムID, アイテム名）
    weapons = []
    for l in open(SRC, 'rb').read().decode('utf-8', 'replace').replace('\r\n', '\n').split('\n'):
        s = l.strip()
        if not s or s.startswith('#'):
            continue
        f = s.split(',')
        if len(f) >= 2 and f[0].strip().isdigit() and f[1].strip():
            weapons.append((f[0].strip(), f[1].strip()))
    print('源 weapon_wrestle.csv：%d 把武器' % len(weapons))

    # ② 现有表：保留注释与已有行
    raw = open(OUT, 'rb').read().decode('utf-8', 'replace')
    lines = raw.replace('\r\n', '\n').split('\n')
    head = [l for l in lines if l.strip().startswith('#')]
    body = [l for l in lines if l.strip() and not l.strip().startswith('#')]
    have = set()
    for l in body:
        k = l.rstrip(',').split(',')[0].strip()
        if k:
            have.add(k)
    print('现有 ITEM：注释 %d 行 / 数据 %d 行（键 %d 个）' % (len(head), len(body), len(have)))

    # ③ 追加缺失的武器行：<ID>,,<名称>,,WEAPON,
    added = []
    for wid, wname in weapons:
        if wid in have:
            continue
        body.append('%s,,%s,,WEAPON,' % (wid, wname))
        have.add(wid)
        added.append((wid, wname))
    print('新增 %d 行：' % len(added))
    for wid, wname in added:
        print('   %-10s %s' % (wid, wname))

    if not os.path.exists(OUT + '.bak'):
        shutil.copy2(OUT, OUT + '.bak')
    open(OUT, 'wb').write(('\r\n'.join(head + body) + '\r\n').encode('utf-8'))

    # ④ 方言自检
    b = open(OUT, 'rb').read()
    ok_bom = not b.startswith(b'\xef\xbb\xbf')
    ok_crlf = b.replace(b'\r\n', b'').find(b'\n') < 0
    data_tail = all(l.endswith(b',') for l in b.split(b'\r\n') if l and not l.startswith(b'#'))
    print('★方言自检：无BOM=%s 全CRLF=%s 数据行尾逗号=%s' % (ok_bom, ok_crlf, data_tail))
    print('★已写 %s（数据 %d 行）' % (os.path.relpath(OUT, ROOT), len(body)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
