# -*- coding: utf-8 -*-
"""fill_from_master.py —— 从 names/机体总表.csv 统一把「模型打包值」写进 #4 col1 与 #5 col71（低32）+col72（高32）。

★唯一权威来源 = 机体总表.csv（由 match_model_names.py → build_mech_master.py 生成）。
先清空该列再填（本列只有我们写，避免残留），CRLF + 备份 + 方言自检。
★2026-09-15 更正：#5 模型坐标在 **col71**（旧误写 col69，见 chara/README §1.4 反汇编定案）。
用法：python datatables/fill_from_master.py [--apply]
"""
import io
import os
import re
import shutil
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
MASTER = os.path.join(HERE, 'names', '机体总表.csv')
DF = os.path.join(ROOT, 'server', 'datafiles', 'lounge', 'msma')
T4 = os.path.join(DF, 'msma_settings.csv')     # #4 CHARA_PARAM 模型在 col1
T5 = os.path.join(DF, 'msma_model.csv')        # #5 CHARA_MODEL 模型在 col71（低32）+col72（高32）


def read(p):
    b = open(p, 'rb').read()
    for enc in ('utf-8-sig', 'cp932', 'utf-8', 'latin1'):
        try:
            return b.decode(enc)
        except Exception:
            pass
    return b.decode('latin1')


def main():
    apply = '--apply' in sys.argv
    # 读主表（按表头取列，稳健）
    raw = read(MASTER).replace('\r\n', '\n').split('\n')
    hdr = [x.lstrip('#').strip() for x in raw if x.startswith('#')][0].split(',')
    ix = {h: i for i, h in enumerate(hdr)}
    ci_id, ci_v = ix['練度ID'], ix['模型打包值']
    model = {}
    for l in raw:
        if not l.strip() or l.startswith('#'):
            continue
        f = [x.strip() for x in l.rstrip(',').split(',')]
        if len(f) > ci_v and re.fullmatch(r'\d{7}', f[ci_id]) and re.fullmatch(r'\d{9}', f[ci_v]):
            model[f[ci_id]] = f[ci_v]
    print('主表有模型打包值：%d 台' % len(model))

    # 校验：坐标都能解出真实目录
    CH = os.path.join(ROOT, 'unpackdat', 'chara')
    bad = 0
    for rid, v in model.items():
        n = int(v)
        if not os.path.isdir(os.path.join(CH, '%02d' % (n // 10**8), '%02d' % ((n // 10**6) % 100),
                                         '%04d' % ((n // 100) % 10000))):
            bad += 1
    print('★目录存在性：%d / %d 有效（无效 %d 将被跳过）' % (len(model) - bad, len(model), bad))

    # (表路径, 模型坐标列, 表名, 需额外清空的旧错列, 是否统一列宽)
    # ★统一列宽：所有数据行补到同一列数（col+1），无值的行也垫满空逗号，
    #   避免"有值 72 列 / 无值 1 列"混排（越界读 0 虽正确，但列数不齐难看且易藏 bug）。
    for path, col, name, stale, pad_all in (
            (T4, 1, '#4 msma_settings', (), False),
            (T5, 71, '#5 msma_model', (69,), True)):
        raw = read(path).replace('\r\n', '\n').split('\n')
        head = [l for l in raw if l.startswith('#')]
        body = [l.rstrip(',').split(',') for l in raw if l.strip() and not l.startswith('#')]
        hit = 0
        for f in body:
            rid = f[0].strip()
            for sc in stale:
                if len(f) > sc:
                    f[sc] = ''                     # ★清掉旧错列 col69
            if pad_all:
                while len(f) <= col:               # ★统一补到 col+1 列（含空）
                    f.append('')
            elif len(f) > col:
                f[col] = ''
            if rid in model:
                while len(f) <= col:
                    f.append('')
                f[col] = model[rid]
                hit += 1
        print('%s：命中填充 %d 行（表 %d 行）' % (name, hit, len(body)))
        if apply:
            if not os.path.exists(path + '.bak'):
                shutil.copy2(path, path + '.bak')
            open(path, 'wb').write(('\r\n'.join(head + [','.join(x) + ',' for x in body]) + '\r\n').encode('utf-8'))
            b = open(path, 'rb').read()
            ok = (not b.startswith(b'\xef\xbb\xbf')) and (b.replace(b'\r\n', b'').find(b'\n') < 0)
            chk = [l for l in b.decode('utf-8', 'replace').replace('\r\n', '\n').split('\n')
                   if l.strip() and not l.startswith('#')]
            n = sum(1 for l in chk if len(l.rstrip(',').split(',')) > col and l.rstrip(',').split(',')[col].strip())
            print('   已写 + 方言%s ｜ 复核非空 col%d=%d' % ('OK' if ok else 'FAIL', col, n))
    if not apply:
        print('（未写；加 --apply 生效）')
    return 0


if __name__ == '__main__':
    sys.exit(main())
