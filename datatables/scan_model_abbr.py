# -*- coding: utf-8 -*-
"""
scan_model_abbr.py —— 扫 chara 全树，**从模型文件里读出机体代号**（这是"机体身份证"）。

发现（2026-09-14，用户确认 `chara/01/01/2850` = フリーダム 之后）：
  模型/属性文件内部的网格名形如 `MSM_<A><B>_<C>_<NN>_<代号>_<xx>`
  例：`MSM_0101_2850_01_FRDGND_00`（FRDGND=FreedomGundam ✓ 与用户目视一致）、
      `MSM_0101_1301_01_BD1_00`（BD1=BlueDestiny-1）、`MSM_0122_1301_01_IFR_00`（IFR=Ifrit）
  ⇒ 于是**每个模型目录的机体身份可自动判定**（不必再靠猜/靠目视）。

产物：
  `datatables/names/chara模型代号.csv`  每目录一行：目录/A/B/C/代号/打包值/文件
  并在 stdout 打印"代号 → 目录"频次最高的若干条，便于人工对名。

用法：
  python datatables/scan_model_abbr.py                 # 全树扫描 + 导出
  python datatables/scan_model_abbr.py FRDGND GM ZAKU  # 只打印含这些代号的目录（找机体用）
"""
import io
import os
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CHARA = os.path.join(ROOT, 'unpackdat', 'chara')
OUT = os.path.join(HERE, 'names', 'chara模型代号.csv')

# 两种写法都要吃：
#   `.dxg` 里： MSM_0101_2850_01_FRDGND_00
#   `.vra` 里： (name string[1] "MSM_0101_2851_01_JTSGND")   ← 代号后面是引号/括号，没有 _NN
RE = re.compile(rb'MSM_(\d{4})_(\d{4})_(\d{2})_([A-Z0-9]{2,12})')
# 目录 model/*.dxg 里的实际形态编号（末两位），如 MSM_0101_0101_01.dxg
RE_NN = re.compile(rb'MSM_(\d{4})_(\d{4})_(\d{2})\.dxg')


def dirs():
    out = []
    for a in sorted(os.listdir(CHARA)):
        pa = os.path.join(CHARA, a)
        if not (os.path.isdir(pa) and a.isdigit()):
            continue
        for b in sorted(os.listdir(pa)):
            pb = os.path.join(pa, b)
            if not (os.path.isdir(pb) and b.isdigit()):
                continue
            for c in sorted(os.listdir(pb)):
                if os.path.isdir(os.path.join(pb, c)) and c.isdigit():
                    out.append((a, b, c))
    return out


def abbr_of(d):
    """从 attr/*.vra（小、快）取代号；没有则退到 model/*.dxg。返回 {代号: (nn, 出处)}。"""
    got = {}
    for sub in ('attr', 'model'):
        sd = os.path.join(d, sub)
        if not os.path.isdir(sd):
            continue
        for f in sorted(os.listdir(sd)):
            if not (f.lower().endswith('.vra') or f.lower().endswith('.dxg')):
                continue
            try:
                b = open(os.path.join(sd, f), 'rb').read(400000)
            except Exception:
                continue
            for m in RE.finditer(b):
                ab = m.group(4).decode()
                got.setdefault(ab, ('', '%s/%s' % (sub, f)))
        if got:
            break
    return got


def nn_of(d):
    """目录内 model/*.dxg 的形态号（末两位）；取最小的那个，缺省 01。"""
    md = os.path.join(d, 'model')
    nns = []
    if os.path.isdir(md):
        for f in sorted(os.listdir(md)):
            m = RE_NN.search(f.encode('latin1', 'replace'))
            if m:
                nns.append(int(m.group(3)))
    return min(nns) if nns else 1


def main():
    want = [x.upper() for x in sys.argv[1:]]
    rows = []
    for (a, b, c) in dirs():
        d = os.path.join(CHARA, a, b, c)
        got = abbr_of(d)
        abbr = '/'.join(sorted(got.keys()))
        nn = nn_of(d)
        val = int(a) * 10 ** 8 + int(b) * 10 ** 6 + int(c) * 100 + nn
        rows.append((a, b, c, abbr, val, (sorted(got.values())[0][1] if got else '')))

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    L = ['#A,B,C,内部代号,打包值(列69用),代号出处,',
         '# 打包值 = A*1e8+B*1e6+C*100+NN（NN 默认取目录内首个形态）,',
         '# 代号来自模型文件内的网格名 MSM_<A><B>_<C>_<NN>_<代号>_<xx>,',
         '# 用法：填 msma_model.csv 第 69 列 = 该目录的打包值（NN 按需要的形态改末两位）,',
         '# ★注意：行键（第 0 列）是練度ID，与这里的打包值是两套编号，需按机体名对应,',]
    L += ['%s,%s,%s,%s,%d,%s,' % r for r in rows]
    open(OUT, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    named = [r for r in rows if r[3]]
    print('已写 %s' % OUT)
    print('目录 %d 个，其中读出代号 %d 个（%.0f%%）' % (len(rows), len(named), 100.0 * len(named) / max(1, len(rows))))

    if want:
        print('\n=== 含这些代号的目录 ===')
        for (a, b, c, ab, val, src) in rows:
            if any(w in ab for w in want):
                print('  chara/%s/%s/%s  代号=%-14s 打包值=%d  (%s)' % (a, b, c, ab, val, src))
        return 0

    print('\n=== 代号样例（每行 = 目录 / 代号 / 打包值）===')
    for r in named[:20]:
        print('  chara/%s/%s/%s  %-16s %d' % (r[0], r[1], r[2], r[3], r[4]))
    import collections
    cnt = collections.Counter(r[3] for r in named)
    print('\n=== 出现最多的代号（前 15）===')
    for k, v in cnt.most_common(15):
        print('   %-16s %d' % (k, v))
    return 0


if __name__ == '__main__':
    sys.exit(main())
