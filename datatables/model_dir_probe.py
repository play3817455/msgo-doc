# -*- coding: utf-8 -*-
"""
model_dir_probe.py —— 破解「モデルID ↔ chara 资源目录」的对应关系。

背景（2026-09-14）：
  * `unpackdat/chara/<A:02d>/<B:02|03d>/<C:04|05d>/` 是机体模型目录，
    文件名形如 `MSM_<A><B>_<C>_<NN>.dxg` / `MST_..._NNc.dds` / `MSZ_..._NN.vra`
    （前缀：MS=機体 / MA / BS / BA / PL / VE 六类，与 chara 顶层 6 个目录对应）。
  * exe 里的路径格式串（0xD6B4D8 起）：
      `chara/%02d/%02d/%04d/attr/MSZ_%02d%02d_%04d_%02d.vra`
      `chara/%02d/%03d/%05d/attr/MSZ_%02d%03d_%05d_%02d.vra`   （大编号形态）
  * 服务端表 / 客户端本地表里的「モデルID」是 9 位（少数 13 位）数字串
    （例：`184300101`=ガンダムエクシア、`101280501`=ストライクI.W.S.P）。
  * `favms_ok_list.csv` 的键是 **7 位「練度ID」** —— 与 モデルID **不是同一套**（本脚本顺带验证）。

做法：
  ① 枚举真实存在的 chara (A,B,C) 目录；
  ② 正向：把每个已知 モデルID 按所有可能位数切分，看是否能命中真实目录；
  ③ 反向：把每个真实目录的数字拼成各种候选串，看是否出现在已知 モデルID 集合里。
用法：python datatables/model_dir_probe.py
"""
import io
import os
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
UNPACK = os.path.join(ROOT, 'unpackdat')
CHARA = os.path.join(UNPACK, 'chara')
SETT = os.path.join(UNPACK, 'settings')


def read_rows(path):
    if not os.path.exists(path):
        return []
    try:
        t = open(path, encoding='utf-8', errors='replace').read()
    except Exception:
        return []
    return [l.rstrip('\r').rstrip(',') for l in t.splitlines() if l.strip() and not l.lstrip().startswith('#')]


def model_ids_from_local():
    """本地表里的 モデルID ↔ 名前（从注释列/# 尾巴里取名字）。"""
    out = []
    for f in ('msma_mesh_customize.csv', 'msma_visual_customize.csv'):
        for r in read_rows(os.path.join(SETT, f)):
            c = r.split(',')
            if not c or not c[0].strip().isdigit():
                continue
            name = ''
            m = re.search(r'#\s*([^,#]+)\s*$', r)
            if m:
                name = m.group(1).strip()
            out.append((c[0].strip(), name, f))
    return out


def favms_ids():
    out = []
    for r in read_rows(os.path.join(SETT, 'favms_ok_list.csv')):
        c = r.split(',')
        if len(c) >= 2 and c[0].strip().isdigit():
            out.append((c[0].strip(), c[1].strip()))
    return out


def chara_dirs():
    dirs = []
    if not os.path.isdir(CHARA):
        return dirs
    for a in sorted(os.listdir(CHARA)):
        pa = os.path.join(CHARA, a)
        if not os.path.isdir(pa):
            continue
        for b in sorted(os.listdir(pa)):
            pb = os.path.join(pa, b)
            if not os.path.isdir(pb):
                continue
            for c in sorted(os.listdir(pb)):
                pc = os.path.join(pb, c)
                if os.path.isdir(pc) and a.isdigit() and b.isdigit() and c.isdigit():
                    dirs.append((a, b, c))
    return dirs


def main():
    dirs = chara_dirs()
    ids = model_ids_from_local()
    fav = favms_ids()
    print('chara 模型目录：%d 个' % len(dirs))
    print('本地表 モデルID：%d 个（msma_visual/mesh_customize）' % len(ids))
    print('favms 練度ID：%d 个' % len(fav))
    if not dirs or not ids:
        return 1

    dirset = set(dirs)
    # ── ① 反向：真实目录 → 候选串 → 看是否等于某个 モデルID ─────────────
    idset = {i for i, _, _ in ids}
    favset = {i for i, _ in fav}
    print('\n=== 反向：真实目录数字拼接，是否命中已知 ID ===')
    hit = 0
    for (a, b, c) in dirs:
        cands = {
            a + b + c, b + c, a + c, c, a + b + c + '01', b + c + '01',
            a + b + '0' + c, str(int(a)) + str(int(b)) + str(int(c)),
        }
        m = cands & idset
        if m:
            hit += 1
            nm = [n for i, n, _ in ids if i in m]
            print('   %s/%s/%s  ⇒ モデルID %s  %s' % (a, b, c, sorted(m), nm[:2]))
    if not hit:
        print('   （0 命中 —— 说明 モデルID 与目录号不是直接拼接关系）')

    # ── ② ★规则 R1：モデルID(9位) = `1` + B(02) + C(04) + NN(02) ────────
    #    例：101280501 ⇒ B=01, C=2805, NN=01 ⇒ chara/<A>/01/2805/
    print('\n=== 正向 R1：モデルID(9位) = 1 + B(2) + C(4) + NN(2) ===')
    A_all = sorted({a for a, _, _ in dirs})
    ok = miss = 0
    for (i, n, f) in ids:
        if len(i) != 9:
            miss += 1
            continue
        B, C, NN = i[1:3], i[3:7], i[7:9]
        got = [a for a in A_all if (a, B, C) in dirset]
        if got:
            ok += 1
            print('   %-12s %-24s ⇒ %s   (NN=%s)' % (
                i, n[:22], ['chara/%s/%s/%s' % (a, B, C) for a in got], NN))
        else:
            miss += 1
            if miss <= 6:
                print('   %-12s %-24s ⇒ ✗（试过 B=%s C=%s）' % (i, n[:22], B, C))
    print('   R1 命中 %d / 未命中 %d（共 %d）' % (ok, miss, len(ids)))

    # ── ②b 正向兜底：所有位数切分 ───────────────────────────────────────
    print('\n=== 反向兜底：モデルID 各种 A/B/C 切分 → 命中真实目录 ===')
    hit2 = 0
    for (i, n, f) in ids:
        got = []
        L = len(i)
        for wa in (1, 2):
            for wb in (2, 3):
                wc = L - wa - wb
                if wc not in (4, 5):
                    continue
                A, B, C = i[:wa], i[wa:wa + wb], i[wa + wb:]
                for AA in (A, '0' + A if len(A) == 1 else A, str(int(A))):
                    if (AA, B, C) in dirset:
                        got.append(AA + '/' + B + '/' + C)
        if got:
            hit2 += 1
            print('   %-14s %-22s ⇒ %s' % (i, n[:20], got))
    if not hit2:
        print('   （0 命中）')

    # ── ③ 练度ID（7位）是否出现在任何目录号里 ───────────────────────────
    print('\n=== favms 7 位練度ID vs 目录号（看是否有 7 位前缀关系）===')
    j = 0
    for (i, n) in fav:
        for (a, b, c) in dirs:
            s = a + b + c
            if i[:4] == s[:4] or i[1:5] == s or i[:3] == b:
                j += 1
                if j <= 8:
                    print('   favms %-9s %-18s ~ %s/%s/%s' % (i, n[:16], a, b, c))
    print('   命中 %d 条' % j)
    return 0


if __name__ == '__main__':
    sys.exit(main())
