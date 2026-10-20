# -*- coding: utf-8 -*-
"""build_model_bridge.py —— 汇总**所有带机体名的客户端表**，自动 join 出"練度ID → モデルID"。

名字源（都是客户端自带、可回溯）：
  settings/msma_ui_customize.csv          col0=モデルID，末列=備考(机体名)
  settings/msma_visual_customize.csv      同上
  settings/msma_mesh_customize.csv        col0=モデルID，cap=机体名（附武器）
  settings/msma_mesh_hide_setup.csv       col0=モデルID，cap=机体名
  settings/weapon_visual_customize.csv    col0=武器モデルID，cap="XXの武器" ⇒ 抠出机体名
  names/模型号映射-人工.csv                （pair_codes 的产物，已过自检）

名册（練度ID ↔ 名字）：settings/favms_ok_list.csv + names/机体名对照表.csv

用法：python datatables/build_model_bridge.py [--apply]
      --apply 会把结果写进 server/datafiles/lounge/msma/msma_settings.csv 的 **col1**
"""
import difflib
import io
import os
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
S = os.path.join(ROOT, 'unpackdat', 'settings')
OUT_CSV = os.path.join(HERE, 'names', '模型号映射-合并.csv')
TARGET = os.path.join(ROOT, 'server', 'datafiles', 'lounge', 'msma', 'msma_settings.csv')


def read(p):
    b = open(p, 'rb').read()
    for enc in ('utf-8-sig', 'cp932', 'utf-8', 'latin1'):
        try:
            return b.decode(enc)
        except Exception:
            pass
    return b.decode('latin1')


def rows(p):
    out = []
    for l in read(p).replace('\r\n', '\n').split('\n'):
        if l.strip() and not l.lstrip().startswith('#'):
            out.append([f.strip() for f in l.rstrip(',').split(',')])
    return out


def norm(s):
    out = []
    for ch in s:
        o = ord(ch)
        out.append(chr(o - 0xFEE0) if 0xFF01 <= o <= 0xFF5E else ch)
    t = ''.join(out).replace('（', '(').replace('）', ')')
    t = t.replace('　', '').replace('ガンダム', 'gundam').replace('敢达', 'gundam')
    for x in (' ', '・', '･', '.', '·', '-', '−'):
        t = t.replace(x, '')
    return t.lower()


def main():
    apply = '--apply' in sys.argv

    # ── 名册：練度ID ↔ 名字集合
    roster = {}
    for f in rows(os.path.join(S, 'favms_ok_list.csv')):
        if len(f) >= 2 and re.fullmatch(r'\d{7}', f[0]):
            roster.setdefault(f[0], set()).add(f[1])
    for f in rows(os.path.join(HERE, 'names', '机体名对照表.csv')):
        if len(f) > 2 and re.fullmatch(r'\d{7}', f[0]):
            for v in (f[1], f[2], f[15] if len(f) > 15 else ''):
                if v.strip():
                    roster.setdefault(f[0], set()).add(v.strip())
    rnorm = {}
    for rid, names in roster.items():
        for n in names:
            rnorm.setdefault(norm(n), rid)
    print('名册：%d 个練度ID，%d 个可匹配名' % (len(roster), len(rnorm)))

    # ── 模型名源
    pairs = {}          # モデルID → 机体名（原始）
    CH = os.path.join(ROOT, 'unpackdat', 'chara')

    def dir_ok(v):
        """★存在性过滤：该模型坐标能否解出真实的 chara 目录（否则客户端加载不出模型）"""
        try:
            n = int(v)
        except Exception:
            return False
        if not re.fullmatch(r'\d{9}', v):
            return False
        d = os.path.join(CH, '%02d' % (n // 10**8), '%02d' % ((n // 10**6) % 100),
                         '%04d' % ((n // 100) % 10000))
        return os.path.isdir(d)

    def add(mid, name):
        name = re.sub(r'の武器$|の武装$', '', name).strip()
        if re.fullmatch(r'\d{9}', mid) and name and dir_ok(mid):
            pairs.setdefault(mid, name)

    for fn in ('msma_ui_customize.csv', 'msma_visual_customize.csv',
               'msma_mesh_customize.csv', 'msma_mesh_hide_setup.csv',
               'weapon_visual_customize.csv'):
        p = os.path.join(S, fn)
        if not os.path.exists(p):
            continue
        n0 = len(pairs)
        for f in rows(p):
            if not f:
                continue
            mid = f[0]
            # 名字：优先最后一个非空、且不是纯数字的字段
            cand = [x for x in f[1:] if x and not re.fullmatch(r'[\d\-\s]+', x)]
            if not re.fullmatch(r'\d{9}', mid):
                # 有的表 ID 不在 col0，扫一遍找第一个 9 位
                m9 = [x for x in f if re.fullmatch(r'\d{9}', x)]
                if not m9:
                    continue
                mid = m9[0]
            if cand:
                add(mid, cand[-1])
        print('  %-34s +%d 条（累计 %d）' % (fn, len(pairs) - n0, len(pairs)))

    # pair_codes 的人工/自检映射（最高可信）
    manual = {}
    for f in rows(os.path.join(HERE, 'names', '模型号映射-人工.csv')):
        if len(f) > 2 and re.fullmatch(r'\d+', f[0]) and re.fullmatch(r'\d{9}', f[2]):
            manual[f[0]] = f[2]
    print('  模型号映射-人工.csv              %d 条（练度ID→モデルID）' % len(manual))

    # ── 匹配：モデルID 的名字 → 練度ID
    auto, fuzzy = {}, []
    for mid, name in sorted(pairs.items()):
        n = norm(name)
        rid = rnorm.get(n)
        if rid:
            auto.setdefault(rid, mid)
            continue
        best = difflib.get_close_matches(n, list(rnorm), n=1, cutoff=0.72)
        if best:
            fuzzy.append((rid := rnorm[best[0]], mid, name, roster[rid] and sorted(roster[rid])[0]))
    print('★按名字精确命中 %d 台；模糊命中(≥0.72) %d 台；未命中 %d 条'
          % (len(auto), len(fuzzy), len(pairs) - len(auto) - len(fuzzy)))

    merged = dict(auto)
    for rid, mid, name, rn in fuzzy:
        merged.setdefault(rid, mid)
    merged.update(manual)          # 人工/自检结果最优先
    print('★合并后 **%d / %d** 台練度ID 有モデルID' % (len(merged), len(roster)))

    # ── 写映射表
    lst = ['#練度ID,モデルID,机体名,来源,']
    for rid in sorted(merged):
        src = '人工' if rid in manual else ('精确' if rid in auto else '模糊')
        nm = sorted(roster.get(rid, ['']))[0]
        lst.append('%s,%s,%s,%s,' % (rid, merged[rid], nm.replace(',', '，'), src))
    open(OUT_CSV, 'wb').write(('\r\n'.join(lst) + '\r\n').encode('utf-8'))
    print('写入 %s（%d 行）' % (os.path.relpath(OUT_CSV, ROOT), len(lst) - 1))

    if not apply:
        print('（未写 #4；加 --apply 生效）')
        return 0
    # ── 写进 #4 的 col1
    raw = read(TARGET).replace('\r\n', '\n').split('\n')
    head = [l for l in raw if l.strip().startswith('#')]
    body = [l.rstrip(',').split(',') for l in raw if l.strip() and not l.lstrip().startswith('#')]
    hit = 0
    for f in body:
        rid = f[0].strip()
        if rid in merged:
            while len(f) <= 1:
                f.append('')
            f[1] = merged[rid]
            hit += 1
    open(TARGET, 'wb').write(('\r\n'.join(head + [','.join(x) + ',' for x in body]) + '\r\n').encode('utf-8'))
    b = open(TARGET, 'rb').read()
    ok = (not b.startswith(b'\xef\xbb\xbf')) and (b.replace(b'\r\n', b'').find(b'\n') < 0)
    print('★ 写入 #4 col1：%d 行 ｜ 方言%s' % (hit, 'OK' if ok else 'FAIL'))
    return 0


if __name__ == '__main__':
    sys.exit(main())
