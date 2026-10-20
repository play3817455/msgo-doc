# -*- coding: utf-8 -*-
"""fix_msma_weapon_set.py —— 规整 `msma/msma_weapon_set.csv` 的行键口径与方言。

背景（2026-09-28 反汇编定案，见 04-填充日志.md）：
    `CHARA_PARAM.col38 → 行 +0x174`，`sub_581690` 用该 +0x174 查 MSMA_WEAPONSET
    (`dword_11EBAB4`)，`sub_836D10` 用同一个 +0x174 查 MSMA_WEAPON_EQUIPCOMB
    (`dword_11EBAB8`)。两张表都是 `std::map<int32, ...>`（`sub_581200` 比较 node+16），
    这条链上**没有任何 練度ID ↔ モデルID 转换**。

    ⇒ **不变式：`msma_weapon_set.col0` 必须是 7 位練度ID**（与 `msma_settings.col0` 同空间）。

实测到的两处缺陷（本次修）：
    1. **1 组 8 行写了 9 位モデルID `101286001`**（= 天帝敢达 / 天意敢达，其練度ID = `1124102`）。
       该组与 `1124102` 组的 8 个武器ID **完全相同** ⇒ 是同一台机体的重复行，被 9 位列键"复制"了一份。
       9 位键永远不可能等于 col38（col38 只填 7 位練度ID）⇒ **整组死行**，直接删除。
    2. **整文件是 LF 换行**（CRLF=0 / LF=2280）⇒ 违反本仓方言自检（应 CRLF）。

做法：只做这三件事 —— ① 丢弃键不是 7 位数字的数据行；② 统一 CRLF；③ 去 BOM / 补尾逗号。
      不动任何列的值、不动行序、不动注释头。

用法：
    python datatables/fix_msma_weapon_set.py            # 只报告（dry-run）
    python datatables/fix_msma_weapon_set.py --apply    # 写入（先备份 .bak_keyfix）
"""
import io
import os
import re
import shutil
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PATH = os.path.join(ROOT, 'server', 'datafiles', 'lounge', 'msma', 'msma_weapon_set.csv')

KEY = re.compile(r'^\d{7}$')          # 練度ID = 7 位


def main():
    apply = '--apply' in sys.argv

    raw = open(PATH, 'rb').read()
    text = raw.decode('utf-8-sig').replace('\r\n', '\n')
    lines = text.split('\n')

    head = [l for l in lines if l.strip().startswith('#')]
    body = [l for l in lines if l.strip() and not l.strip().startswith('#')]

    keep, drop = [], []
    for l in body:
        cols = l.rstrip(',').split(',')
        c0 = cols[0].strip()
        (keep if KEY.match(c0) else drop).append(l)

    # 重复组体检：同一台机体是否出现多组（键不同、武器ID集合相同）
    print('原文件 : %d 字节 / 注释 %d 行 / 数据 %d 行' % (len(raw), len(head), len(body)))
    print('换行   : CRLF=%d / 裸 LF=%d %s'
          % (raw.count(b'\r\n'), raw.replace(b'\r\n', b'').count(b'\n'),
             '（★需修）' if raw.replace(b'\r\n', b'').count(b'\n') else '（OK）'))
    print('BOM    : %s' % ('有（★需修）' if raw[:3] == b'\xef\xbb\xbf' else '无（OK）'))
    print('保留   : %d 行' % len(keep))
    print('丢弃   : %d 行（键不是 7 位練度ID）' % len(drop))
    for l in drop[:10]:
        print('     - %s' % l[:110])

    seen = {}
    for l in keep:
        seen.setdefault(l.split(',')[0].strip(), []).append(l.split(',')[2].strip())
    print('组数   : %d ｜ 组内武器ID集合重复的组（可能同机多键）:'
          % len(seen))
    rev = {}
    for k, v in seen.items():
        rev.setdefault(tuple(sorted(v)), []).append(k)
    dup = {k: v for k, v in rev.items() if len(v) > 1}
    if not dup:
        print('     （无）')
    else:
        for k, v in list(dup.items())[:10]:
            print('     %s' % v)

    out = '\r\n'.join(head + keep) + '\r\n'
    b = out.encode('utf-8')
    ok = (not b.startswith(b'\xef\xbb\xbf')) and b.count(b'\n') == b.count(b'\r\n')
    bad = [x for x in keep if not x.endswith(',')]
    print()
    print('自检   : BOM 无=%s / CRLF=%s / 尾逗号缺 %d 行'
          % ('✓' if not b.startswith(b'\xef\xbb\xbf') else '✗',
             '✓' if b.count(b'\n') == b.count(b'\r\n') else '✗', len(bad)))
    ncols = set(len(x.split(',')) for x in keep)
    print('列数   : %s' % sorted(ncols))

    if not apply:
        print('\n（dry-run；加 --apply 写入）')
        return 0

    bak = PATH + '.bak_keyfix'
    if not os.path.exists(bak):
        shutil.copy2(PATH, bak)
        print('备份 → %s' % os.path.basename(bak))
    with open(PATH, 'wb') as f:
        f.write(b)
    print('写入 %s（%d 行数据）' % (PATH, len(keep)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
