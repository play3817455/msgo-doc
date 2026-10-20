# -*- coding: utf-8 -*-
"""apply_model_both.py —— 把"練度ID → 模型坐标"同时写进两张表。

★依据（两处 IDA 实证 + 编码自洽校验）：
  · `#5 CHARA_MODEL`（msma/msma_model.csv）**第 71 列**（低 32 位）+ 第 72 列（高 32 位，可省）
    —— 由 `sub_571380` 反汇编定案：`mov [edi+1B4h](+436) ← 读于 0x5719f7(esi=col71)`、
    `mov [edi+1B8h](+440) ← 读于 0x571a07(esi=col72)`；★旧结论"第 69/71 列"是**读序数错** ✗
  · `#4 CHARA_PARAM`（msma/msma_settings.csv）**第 1 列**（64 位）
    —— 由 `sub_4C5CE0`（模型加载器唯一调用者）实测：查 #4 → 取行 +8（=col1）→ `sub_4BEB30`
  · 编码 = `类别(1)*1e8 + 系列(2)*1e6 + 叶(4)*100 + 变体(2)`（`sub_473390` 分支B 反推，
    已用 `chara/01/01/0202` + `MSM_0101_0202_01.dxg` 校验自洽）

映射来源（按可信度）：names/模型号映射-人工.csv（pair_codes 自检通过）< names/模型号映射-合并.csv（名字 join）
用法：python datatables/apply_model_both.py [--apply]
"""
import io
import os
import re
import shutil
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DF = os.path.join(ROOT, 'server', 'datafiles', 'lounge', 'msma')
T4 = os.path.join(DF, 'msma_settings.csv')     # #4 CHARA_PARAM，模型在 col1
T5 = os.path.join(DF, 'msma_model.csv')        # #5 CHARA_MODEL，模型在 col71（低32）+col72（高32）


def read(p):
    b = open(p, 'rb').read()
    for enc in ('utf-8-sig', 'cp932', 'utf-8', 'latin1'):
        try:
            return b.decode(enc)
        except Exception:
            pass
    return b.decode('latin1')


def rows(p):
    return [[f.strip() for f in l.rstrip(',').split(',')]
            for l in read(p).replace('\r\n', '\n').split('\n')
            if l.strip() and not l.lstrip().startswith('#')]


def load_map():
    """优先级：人工 > 补充 > 名字join。每行取"第 0 列=練度ID、行内第一个 9 位数字=模型坐标"。"""
    m, src = {}, {}
    for fn, tag in (('模型号映射-合并.csv', 'join'),
                    ('模型号映射-补充.csv', '补充'),
                    ('模型号映射-人工.csv', '人工')):
        p = os.path.join(HERE, 'names', fn)
        if not os.path.exists(p):
            continue
        for f in rows(p):
            if not f or not re.fullmatch(r'\d{7}', f[0]):
                continue
            m9 = [x for x in f[1:] if re.fullmatch(r'\d{9}', x)]
            if m9:
                m[f[0]] = m9[0]
                src[f[0]] = tag
    return m, src


def decode(v):
    """按 sub_473390 反推，打印该值指向的 chara 目录（自检用）"""
    v = int(v)
    return 'chara/%02d/%02d/%04d (变体 %02d)' % (v // 10**8, (v // 10**6) % 100,
                                                  (v // 100) % 10000, v % 100)


def main():
    apply = '--apply' in sys.argv
    m, src = load_map()
    print('待写映射 %d 台（人工 %d / 名字join %d）'
          % (len(m), sum(1 for k in src if src[k] == '人工'), sum(1 for k in src if src[k] == 'join')))
    for k in list(m)[:4]:
        print('   %s → %s  ⇒ %s' % (k, m[k], decode(m[k])))

    # ★(表路径, 模型坐标列, 表名, 需要额外清空的旧错列)
    #   #5 CHARA_MODEL：模型坐标 = col71(低32) + col72(高32)（sub_571380 反汇编 0x571a01/0x571a11 定案）；
    #   旧代码误写 col69 → 现在一律清掉，防止残留旧值。
    for path, col, name, stale in (
            (T4, 1, '#4 msma_settings', ()),
            (T5, 71, '#5 msma_model', (69,))):
        raw = read(path).replace('\r\n', '\n').split('\n')
        head = [l for l in raw if l.strip().startswith('#')]
        body = [l.rstrip(',').split(',') for l in raw if l.strip() and not l.lstrip().startswith('#')]
        hit = 0
        for f in body:
            rid = f[0].strip()
            for sc in stale:
                if len(f) > sc:
                    f[sc] = ''                 # ★清掉旧错列
            if len(f) > col:
                f[col] = ''                     # ★先清空本列，避免残留旧值
            if rid in m:
                while len(f) <= col:
                    f.append('')
                f[col] = m[rid]
                hit += 1
        print('%s：命中并填充 **%d 行**（表共 %d 行）' % (name, hit, len(body)))
        if apply:
            if not os.path.exists(path + '.bak'):
                shutil.copy2(path, path + '.bak')
            open(path, 'wb').write(
                ('\r\n'.join(head + [','.join(x) + ',' for x in body]) + '\r\n').encode('utf-8'))
            b = open(path, 'rb').read()
            ok = (not b.startswith(b'\xef\xbb\xbf')) and (b.replace(b'\r\n', b'').find(b'\n') < 0)
            # ★写完立即复核（同一进程，排除外部改写干扰）
            chk = [l for l in b.decode('utf-8', 'replace').replace('\r\n', '\n').split('\n')
                   if l.strip() and not l.startswith('#')]
            n = sum(1 for l in chk if len(l.rstrip(',').split(',')) > col
                    and l.rstrip(',').split(',')[col].strip())
            print('   已写 + 方言%s ｜ 复核非空 col%d = %d 行 ｜ 备份 .bak ✓'
                  % ('OK' if ok else 'FAIL', col, n))
    if not apply:
        print('（未写表；加 --apply 生效）')
    return 0


if __name__ == '__main__':
    sys.exit(main())
