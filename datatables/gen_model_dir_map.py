# -*- coding: utf-8 -*-
"""
gen_model_dir_map.py —— 导出「モデルID → chara 模型资源」对照表（供解包器逐个预览核对）。

规则（2026-09-14 破解并验证，39/47 命中且语义全对）：
    モデルID(9位) = `1` + B(2位, 作品系列) + C(4位, 机体) + NN(2位, 形态编号)
    资源目录      = `unpackdat/chara/01/<B>/<C>/`          （01 = MS 种族；另有 02=MA/03=BS/05/06/07）
    模型文件      = `model/MSM_01<B>_<C>_<NN>.dxg`
                    纹理 `tex/MST_01<B>_<C>_<NN>C*.dds` ／ 属性 `attr/MSZ_01<B>_<C>_<NN>.vra`
    例：`101280501`(ストライクI.W.S.P) ⇒ chara/01/01/2805/model/MSM_0101_2805_01.dxg
        `184300101`(ガンダムエクシア)   ⇒ chara/01/84/3001/model/MSM_0184_3001_01.dxg

对照源：客户端本地表 `settings/msma_visual_customize.csv` / `msma_mesh_customize.csv`
（它们的第 0 列就是 モデルID，末列注释里有日文机体名）。

产物：`datatables/names/模型ID-资源目录对照.csv`
用法：python datatables/gen_model_dir_map.py
"""
import io
import os
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CHARA = os.path.join(ROOT, 'unpackdat', 'chara')
SETT = os.path.join(ROOT, 'unpackdat', 'settings')
OUT = os.path.join(HERE, 'names', '模型ID-资源目录对照.csv')


def rows(path):
    if not os.path.exists(path):
        return []
    t = open(path, encoding='utf-8', errors='replace').read()
    return [l.rstrip('\r').rstrip(',') for l in t.splitlines()
            if l.strip() and not l.lstrip().startswith('#')]


def local_pairs():
    """返回 [(モデルID, 名字, 来源表)]"""
    out, seen = [], set()
    for f in ('msma_visual_customize.csv', 'msma_mesh_customize.csv'):
        for r in rows(os.path.join(SETT, f)):
            c = r.split(',')
            if not c or not c[0].strip().isdigit():
                continue
            m = re.search(r'#\s*([^,#]+?)\s*$', r)
            name = m.group(1).strip() if m else ''
            key = (c[0].strip(), name)
            if key in seen:
                continue
            seen.add(key)
            out.append((c[0].strip(), name, f))
    return out


def resolve(mid):
    """按 R1 找资源目录与模型文件（NN 优先取 ID 尾部两位）。"""
    if len(mid) != 9 or not mid.isdigit():
        return None
    B, C, NN = mid[1:3], mid[3:7], mid[7:9]
    for a in sorted(os.listdir(CHARA)) if os.path.isdir(CHARA) else []:
        d = os.path.join(CHARA, a, B, C)
        if not os.path.isdir(d):
            continue
        md = os.path.join(d, 'model')
        files = sorted(os.listdir(md)) if os.path.isdir(md) else []
        pick = [x for x in files if x.lower().endswith('_%s.dxg' % NN)]
        return dict(race=a, B=B, C=C, NN=NN,
                    rel='chara/%s/%s/%s' % (a, B, C),
                    dxg=(pick or files or [''])[0],
                    ndxg=len(files))
    return None


def enumerate_all():
    """枚举全部 chara 模型目录 → 反推 モデルID（口径见文件头，已由 sub_49D030/sub_473390 证实）。

    モデルID = A(1位)*1e8 + B(2位)*1e6 + C(4位)*100 + NN(2位)
    """
    out = []
    if not os.path.isdir(CHARA):
        return out
    for a in sorted(os.listdir(CHARA)):
        pa = os.path.join(CHARA, a)
        if not os.path.isdir(pa) or not a.isdigit():
            continue
        for b in sorted(os.listdir(pa)):
            pb = os.path.join(pa, b)
            if not os.path.isdir(pb) or not b.isdigit():
                continue
            for c in sorted(os.listdir(pb)):
                pc = os.path.join(pb, c)
                md = os.path.join(pc, 'model')
                if not (os.path.isdir(pc) and c.isdigit() and os.path.isdir(md)):
                    continue
                files = sorted(os.listdir(md))
                nns = []
                for f in files:
                    m = re.search(r'_(\d{2})\.dxg$', f, re.I)
                    if m and m.group(1) not in nns:
                        nns.append(m.group(1))
                for nn in nns:
                    mid = (int(a) * 10 ** 8 + int(b) * 10 ** 6 + int(c) * 100 + int(nn))
                    out.append(dict(mid=str(mid), A=a, B=b, C=c, NN=nn,
                                    rel='chara/%s/%s/%s' % (a, b, c),
                                    dxg='MSM_%s%s_%s_%s.dxg' % (a, b, c, nn),
                                    nvar=len(nns), nmesh=len(files)))
    return out


def main():
    allm = enumerate_all()
    fp2 = os.path.join(HERE, 'names', 'chara目录-ID清单.csv')
    os.makedirs(os.path.dirname(fp2), exist_ok=True)
    L2 = ['#モデルID,A,B,C,NN,资源目录,模型文件,同目录形态数,同目录网格数,',
          '# モデルID = A(类型1位)*1e8 + B(系列2位)*1e6 + C(机体4位)*100 + NN(形态2位),',
          '# 依据：客户端 sub_49D030（拼 chara 路径）+ sub_473390（十进制拆位）,',
          '# A：0/1=MS(MSZ) 2=MA(MAZ) 3=BS(BSZ) 4=VE(VEZ) 5=PL(PLZ) 6/7=BA(BAZ),']
    L2 += ['%s,%s,%s,%s,%s,%s,%s,%d,%d,' % (r['mid'], r['A'], r['B'], r['C'], r['NN'],
                                            r['rel'], r['dxg'], r['nvar'], r['nmesh'])
           for r in allm]
    open(fp2, 'w', encoding='utf-8').write('\n'.join(L2) + '\n')
    print('已写 %s（%d 条模型ID / %d 个目录）'
          % (fp2, len(allm), len({r['rel'] for r in allm})))
    print('  A 分布：', {a: len([r for r in allm if r['A'] == a]) for a in sorted({r['A'] for r in allm})})
    print('  样例：', [(r['mid'], r['rel']) for r in allm[:3]], '...',
          [(r['mid'], r['rel']) for r in allm[-3:]])

    pairs = local_pairs()
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    lines = ['#モデルID,机体名,资源目录,模型文件,同目录模型数,来源表,',
             '# 规则：モデルID(9位)=1+B(2)+C(4)+NN(2)；资源=chara/01/<B>/<C>/model/MSM_01<B>_<C>_<NN>.dxg,',
             '# 解包器里打开「资源目录/模型文件」即可看到该机体；对不上就说明该行 ID↔机体 映射有问题,',
             '# （★本表用 9 位モデルID；favms_ok_list.csv 的 7 位「練度ID」是另一套编号，不能直接当资源号）,',]
    ok = bad = 0
    samples = []
    for mid, name, src in pairs:
        r = resolve(mid)
        if r:
            ok += 1
            lines.append('%s,%s,%s,%s,%d,%s,' % (mid, name, r['rel'], r['dxg'], r['ndxg'], src))
            if len(samples) < 14 and name:
                samples.append((mid, name, r['rel'], r['dxg']))
        else:
            bad += 1
            lines.append('%s,%s,???,???,0,%s,' % (mid, name, src))
    open(OUT, 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
    print('已写 %s' % OUT)
    print('解析成功 %d / 失败 %d（共 %d）' % (ok, bad, len(pairs)))
    print('\n=== 可直接拿去解包器核对的样本（资源目录 + 模型文件）===')
    for mid, name, rel, dxg in samples:
        print('  %-11s %-26s %s/model/%s' % (mid, name[:24], rel, dxg))
    return 0


if __name__ == '__main__':
    sys.exit(main())
