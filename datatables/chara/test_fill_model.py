# -*- coding: utf-8 -*-
"""
test_fill_model.py —— 给 `#5 CHARA_MODEL`（`server/datafiles/msma_msma_model.csv`）**试填模型号**，用于客户端实测。

背景（已定案，见 `datatables/chara/README.md`）：
  · 模型号写在 **CSV 第 71 列（0 基，低 32 位）**（第 72 列=高 32 位，9 位数够用，留空=0）；旧"第 69 列"已作废 ✗
  · 值 = `<类别:1><系列:2><leaf:6>` 形态的 9 位十进制，客户端 `sub_473390` 会拆成 `chara/%02d/%02d/%04d/...` 的路径
  · 推导：`chara/01/28/0101`（エールストライク）⇔ `128000101`（已验证）

本次试填（两台初始机 ↔ 资源树里同一个 leaf `1301` 的两个目录）：
  1301011 ジム・トレーナー → `101001301`（= 1|01|00|1301 → chara/01/01/1301）
  1301012 ザク・ワーカー   → `122001301`（= 1|22|00|1301 → chara/01/22/1301）
备用口径（若上面不生效）：UI 风格 `<1><L1><L2><leaf>`，即 1301011 → `101011301`

用法：
  python test_fill_model.py --show 1301011            # 看当前行（字段数 + 第69列）
  python test_fill_model.py --set 1301011=101001301 1301012=122001301
  python test_fill_model.py --restore                 # 还原备份
"""
import io
import os
import shutil
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
TARGET = os.path.join(ROOT, 'server', 'datafiles', 'lounge', 'msma', 'msma_model.csv')
BAK = TARGET + '.bak'
COL = 71          # 0 基：模型号所在列（低32）；旧 69 已作废（见 chara/README §1.4）


def load():
    if not os.path.exists(TARGET):
        print('!! 找不到', TARGET)
        sys.exit(1)
    lines = open(TARGET, encoding='utf-8').read().splitlines()
    return lines


def show(rid):
    for l in load():
        f = l.split(',')
        if f and f[0].strip() == rid:
            print('行字段数 %d ｜ 第0列=%s ｜ 第%d列=%r' % (len(f), f[0], COL, f[COL] if len(f) > COL else '(越界=0)'))
            return
    print('没找到该行：', rid)


def save(lines):
    if not os.path.exists(BAK):
        shutil.copy2(TARGET, BAK)
        print('已备份 →', os.path.basename(BAK))
    with open(TARGET, 'wb') as fh:
        fh.write(('\r\n'.join(lines) + '\r\n').encode('utf-8'))


def setvals(pairs):
    lines = load()
    done = []
    for l in lines:
        f = l.rstrip(',').split(',')
        if f and f[0].strip() in pairs:
            rid = f[0].strip()
            if len(f) <= COL:                       # 补足到第 COL 列
                f = f + [''] * (COL + 1 - len(f))
            f[COL] = pairs[rid]
            done.append((rid, pairs[rid]))
            lines[lines.index(l)] = ','.join(f) + ','
    save(lines)
    for rid, v in done:
        print('已写入：%s  第%d列 = %s' % (rid, COL, v))
    for rid in pairs:
        if rid not in [d[0] for d in done]:
            print('⚠️ 未找到行：', rid)
    print('文件：', TARGET)
    print('★ 客户端要取到新表：重启服务端（该表在登录后下发）')


def restore():
    if os.path.exists(BAK):
        shutil.copy2(BAK, TARGET)
        print('已还原自备份')
    else:
        print('没有备份文件')


def main():
    a = sys.argv[1:]
    if not a:
        print(__doc__)
        return 0
    if a[0] == '--show':
        show(a[1])
    elif a[0] == '--set':
        pairs = {}
        for kv in a[1:]:
            k, _, v = kv.partition('=')
            if k and v:
                pairs[k.strip()] = v.strip()
        setvals(pairs)
    elif a[0] == '--restore':
        restore()
    return 0


if __name__ == '__main__':
    sys.exit(main())
