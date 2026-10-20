# -*- coding: utf-8 -*-
"""fill_chara_model_col.py —— 把「模型标识(モデルID)」填进 #4 CHARA_PARAM 的 **col1**。

★依据（IDA 实证，2026-09-14）：
    `sub_4C5CE0`（模型加载器的唯一调用者）：
        v4 = dword_11E3F14;                 // #4 CHARA_PARAM
        sub_581200(&v11, v10);              // 用键查 #4
        v5 = v11 + 8;                       // ★ 行内偏移 +8 = col1（QWORD）
        sub_4BEB30(ptr, *v5, v5[1]);        // ★ 把 col1 的 64 位值传给模型加载器
    → `sub_4BEB30` 里 `sub_473390(a2,a3)` 拆成 {A,B,C,NN} → `sub_49D030` 拼 `chara/<A>/<B>/<C>/`
    ⇒ ★**#4 的 col1 = 模型标识（9 位或 13 位モデルID）**★

映射来源（可回溯）：
    names/模型号映射-人工.csv   （練度ID → モデルID，由目录内部代号 + 真值自检生成）
    names/模型号-客户端表.csv    （从客户端 msma_*_customize 表挖出的真值）
用法：python datatables/fill_chara_model_col.py [--apply]
"""
import io
import os
import shutil
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, 'server', 'datafiles', 'lounge', 'msma', 'msma_settings.csv')
COL = 1


def rows(p, keycols=1):
    out = []
    for l in open(p, encoding='utf-8', errors='replace').read().replace('\r\n', '\n').split('\n'):
        if l.strip() and not l.lstrip().startswith('#'):
            out.append(l.rstrip(',').split(','))
    return out


def main():
    apply = '--apply' in sys.argv
    mp = {}
    for f in rows(os.path.join(HERE, 'names', '模型号映射-人工.csv')):
        if len(f) > 2 and f[0].strip().isdigit() and f[2].strip().isdigit():
            mp[f[0].strip()] = f[2].strip()
    n1 = len(mp)
    for f in rows(os.path.join(HERE, 'names', '模型号-客户端表.csv')):
        if len(f) > 2 and f[0].strip().isdigit() and f[2].strip().isdigit():
            mp.setdefault(f[0].strip(), f[2].strip())
    print('映射：人工 %d 条 ⇒ 合并后 **%d 台**有モデルID' % (n1, len(mp)))

    raw = open(OUT, encoding='utf-8', errors='replace').read().replace('\r\n', '\n').split('\n')
    head = [l for l in raw if l.strip().startswith('#')]
    body = [l.rstrip(',').split(',') for l in raw if l.strip() and not l.lstrip().startswith('#')]
    hit, miss = 0, []
    for f in body:
        rid = f[0].strip()
        if rid in mp:
            if len(f) <= COL:
                f += [''] * (COL + 1 - len(f))
            f[COL] = mp[rid]
            hit += 1
        elif rid.isdigit():
            miss.append(rid)
    print('命中并填充 col%d：**%d 行**；本次未命中 %d 台（其余保持空）' % (COL, hit, len(miss)))
    for fid in ['1301011', '1301012', '1124081', '1107011']:
        r = next((x for x in body if x[0].strip() == fid), None)
        print('   样例 %s → col%d=%s' % (fid, COL, (r[COL] if r else '(缺行)')))
    if not apply:
        print('（未写表；加 --apply 生效）')
        return 0
    if not os.path.exists(OUT + '.bak'):
        shutil.copy2(OUT, OUT + '.bak')
    txt = head + [','.join(x) + ',' for x in body]
    open(OUT, 'wb').write(('\r\n'.join(txt) + '\r\n').encode('utf-8'))
    b = open(OUT, 'rb').read()
    ok = (not b.startswith(b'\xef\xbb\xbf')) and (b.replace(b'\r\n', b'').find(b'\n') < 0)
    print('★ 已写 %s（%d 行）方言%s ｜ 备份 .bak ✓'
          % (os.path.relpath(OUT, ROOT), len(body), 'OK' if ok else 'FAIL'))
    return 0


if __name__ == '__main__':
    sys.exit(main())
