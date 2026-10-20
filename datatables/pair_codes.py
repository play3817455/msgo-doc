# -*- coding: utf-8 -*-
"""
pair_codes.py —— 把「chara 目录的内部英文代号」配到「名册（練度ID/日文名）」，生成模型号映射。

背景：
  · 模型目录 = `chara/<A>/<B>/<C>/`，内部代号写在模型文件里（`MSM_0101_0202_01_GMT` ⇒ GMT）
    —— 见 `scan_model_abbr.py` / `names/chara模型代号.csv`
  · 名册 = `unpackdat/settings/favms_ok_list.csv`（練度ID ↔ 日文名），
    与《中日对照表》`id` 同键 ⇒ 名字可用 `names/机体总表.csv` 的 jp/cn 列
  · 打包值 = `A*1e8 + B*1e6 + C*100 + NN`（客户端 sub_473390 实测口径）⇒ 填 `#5` 第 69 列

做法：本文件维护 `CODE2KEY`（代号 → 日文名关键词，人工确认），
      按其把目录配到名册条目（关键词唯一命中才算）。
用法：
  python datatables/pair_codes.py            # 只出映射表
  python datatables/pair_codes.py --apply    # 同时写进 server/datafiles/lounge/msma/msma_model.csv（第 69 列）
"""
import io
import os
import shutil
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ABBR = os.path.join(HERE, 'names', 'chara模型代号.csv')
MASTER = os.path.join(HERE, 'names', '机体总表.csv')
OUT = os.path.join(HERE, 'names', '模型号映射-人工.csv')
MODEL = os.path.join(ROOT, 'server', 'datafiles', 'lounge', 'msma', 'msma_model.csv')
COL = 71          # 0 基：#5 CHARA_MODEL 模型号在 col71（低32）+col72（高32）；旧 69 已作废（见 chara/README §1.4）

# ★ 代号 → 日文名关键词（人工确认；关键词在名册里必须唯一命中，否则报歧义）
CODE2KEY = {
    # ── 联邦早期（chara/01/01 段）
    'GMT': 'ジム・トレーナー', 'GMTC': 'ジム・トレーナー',
    'GLA': 'ジム・ライトアーマー',
    'GSC': 'ジム・スナイパーカスタム',
    'GDS': 'デザート・ジム',
    'ZNY': 'ザニー',
    'GND4': 'ガンダム4号機', 'GND5': 'ガンダム5号機',
    'AGM': 'アクア・ジム',
    'EZ8': 'ガンダムEz8', 'EZ8WR': 'ガンダムEz8',
    'GNG': '陸戦型ガンダム',
    'GMH': 'ジムヘッド',
    'GMK': 'ジム改',
    'GMC': 'ジム・コマンド',
    'GM2': 'ジムⅡ', 'GM3': 'ジムⅢ',
    'GP01': 'ガンダム試作１号機', 'GP01AQA': 'ガンダム試作１号機',
    'GP02': 'ガンダム試作2号機', 'GP03': 'ガンダム試作3号機',
    'GP04': 'ガンダム試作4号機',
    'BD1': 'ブルーディスティニー1号機', 'BD2': 'ブルーディスティニー2号機',
    'BD3': 'ブルーディスティニー3号機',
    'JGN': 'ジェガン', 'JGND1': 'ジェガン',
    # ── SEED 系（chara/01/01 后段）
    'ALSTG': 'エールストライク', 'SWSTG': 'ソードストライク', 'LCSTG': 'ランチャーストライク',
    'STGIWSP': 'ストライクガンダムI.W.S.P', 'STGIWSPJ': 'ストライクガンダムI.W.S.P',
    'STRIWSPJ': 'ストライクルージュI.W.S.P',
    'STRKRG': 'ストライクルージュ',
    'BUSTERO': 'バスターガンダム(地球連合機)', 'BUSTERR': 'バスターガンダム(ザフト機)',
    'BLITZ': 'ブリッツガンダム', 'DUELGAS': 'デュエルガンダム',
    'CMTG': 'カラミティガンダム', 'FBDGND': 'フォビドゥンガンダム',
    'SWCMT': 'ソードカラミティガンダム',
    'AKTKO': 'アカツキ(シラヌイ)', 'AKTKS': 'アカツキ',
    'PFSTG': 'パーフェクトストライク',
    'FRDGND': 'フリーダムガンダム', 'FRDGNDGCP': 'フリーダムガンダム Ver.GCP',
    'JTSGND': 'ジャスティスガンダム',
    'STFRGND': 'ストライクフリーダムガンダム',
    'IFJTSGND': 'インフィニットジャスティスガンダム',
    'PRVDNCGND': 'プロヴィデンスガンダム',
    'FIMPLSG': 'フォースインパルスガンダム', 'SIMPLSG': 'ソードインパルスガンダム',
    'BIMPLSG': 'ブラストインパルスガンダム',
    'DSTNYGDM': 'デスティニーガンダム',
    # ── 00 系 / 后期
    'OGDM': '0ガンダム', 'FA0GDM': 'フルアーマー0ガンダム', 'ALVAARON': 'アルヴァアロン',
    'GEXES': 'G-エクセス',
    # ── 吉翁段（chara/01/21、01/22）
    'ZKW': 'ザク・ワーカー', 'ZK1': 'ザクⅠ', 'ZK2': 'ザクⅡ',
    'GUF': 'グフ', 'IFR': 'イフリート', 'IFRMS': 'イフリート', 'IFRS': 'イフリート',
    'HZAK': 'ハイザック', 'PSYZAK': 'サイコザク',
    'DZK': 'ドム',
    # ── 其他已确认
    'GNDTRNE': 'ガンダムスローネアイン',
}


def norm_name(s):
    """名字归一：全角字母数字→半角、去空格/中点/连字符、括号统一（名册与关键词两边都过一遍）。"""
    out = []
    for ch in s:
        o = ord(ch)
        if 0xFF01 <= o <= 0xFF5E:            # 全角 ASCII 段
            ch = chr(o - 0xFEE0)
        out.append(ch)
    t = ''.join(out).replace('（', '(').replace('）', ')')
    for x in (' ', '\u3000', '・', '･', '.', '·', '-'):
        t = t.replace(x, '')
    return t.lower()


def main():
    apply = '--apply' in sys.argv
    # 目录代号表
    dirs = []
    for l in open(ABBR, encoding='utf-8').read().splitlines():
        if not l or l.startswith('#'):
            continue
        f = l.split(',')
        if len(f) >= 5 and f[3]:
            for code in f[3].split('/'):
                dirs.append((f[0], f[1], f[2], code, int(f[4])))
    # 名册（从机体总表取 jp/cn）
    raw = open(MASTER, encoding='utf-8').read().splitlines()
    hdr = [x.lstrip('#').rstrip(',') for x in raw if x.startswith('#')][0].split(',')
    rows = [l.rstrip(',').split(',') for l in raw if l.strip() and not l.startswith('#')]
    ix = {h: i for i, h in enumerate(hdr)}
    named = [(r[ix['練度ID']], r[ix['日文名']], r[ix['中文名']]) for r in rows]
    nkey = {}                                        # 归一化名 → 名册条目（保持原名输出）
    for n in named:
        nkey.setdefault(norm_name(n[1]), n)

    out, amb, nomatch = [], [], []
    for (a, b, c, code, val) in dirs:
        keys = CODE2KEY.get(code)
        if not keys:
            continue
        keys = keys if isinstance(keys, (list, tuple)) else [keys]
        nkeys = [norm_name(k) for k in keys]
        hit, key = [], nkeys[0]
        for nk in nkeys:                             # 多个候选关键词，取第一个有命中的
            h = [n for n in named if nk in norm_name(n[1])]
            if h:
                hit, key = h, nk
                break
        if len(hit) > 1:
            # ★优先：归一化后与关键词**完全相等**的；否则取**最短**名（基础型；带括号的是加装备变体）
            exact = [n for n in hit if norm_name(n[1]) == key]
            hit = exact or sorted(hit, key=lambda n: (len(norm_name(n[1])), n[1]))[:1]
        if len(hit) == 1:
            out.append((hit[0][0], hit[0][1], str(val), 'chara/%s/%s/%s' % (a, b, c), code, hit[0][2]))
        else:
            nomatch.append((code, key))

    # ★同一代号出现在多个目录（重复槽位）⇒ 取 **C 最小**（基础型），其余报出来备查
    best, dup = {}, {}
    for r in out:
        c = r[4]
        dup.setdefault(c, []).append(r[3])
        if c not in best or int(r[2]) < int(best[c][2]):
            best[c] = r
    if dup:
        print('--- 同代号多目录（取 C 最小者）---')
        for c, ds in sorted(dup.items()):
            if len(ds) > 1:
                print('   %-12s %s → 取 %s' % (c, ds, best[c][3]))
    out = [best[c] for c in sorted(best, key=lambda c: int(best[c][2]))]
    print('目录(代号)命中 %d 条 → 唯一配对 **%d** 条；歧义 %d；名册无此名 %d'
          % (len([1 for d in dirs if d[3] in CODE2KEY]), len(out), len(amb), len(nomatch)))
    if nomatch:
        print('--- 名册里没有该名字 ---', [(c, k) for c, k in nomatch[:12]])

    # ★自检：这些代号的值已被用户实测/UI 真值确认，配出来必须一致
    KNOWN = {'GMT': 101020201, 'ZKW': 121010201, 'FRDGND': 101285001,
             'CMTG': 101284001, 'FBDGND': 101284101, 'BUSTERO': 101281601,
             'PFSTG': 101284901, 'OGDM': 101300101, 'FA0GDM': 101300201,
             'ALVAARON': 101300301, 'GNDTRNE': 190300101}
    got = {r[4]: int(r[2]) for r in out}
    bad = [(c, v, got.get(c)) for c, v in KNOWN.items() if got.get(c) != v]
    hitk = [c for c in KNOWN if c in got]
    print('★自检：已知 %d 个代号中配对成功 %d 个，冲突 %d 个' % (len(KNOWN), len(hitk), len(bad)))
    for c, want, g in bad:
        print('   ✗ %-12s 期望 %s 实得 %s' % (c, want, g))

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    L = ['#練度ID,日文名,模型打包值,资源目录,内部代号,中文名,来源,',
         '# 由 datatables/pair_codes.py 的 CODE2KEY（人工确认的 代号→日文名）自动配对生成,',
         '# 打包值 = A*1e8+B*1e6+C*100+NN ⇒ 写进 msma_model.csv 第 69 列（客户端 sub_473390 拆位）,',]
    L += [','.join(x) + ',' for x in out]
    open(OUT, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    print('已写 %s（%d 条）' % (OUT, len(out)))

    if not apply:
        print('（未写模型表；加 --apply 生效）')
        return 0
    lines = open(MODEL, encoding='utf-8', errors='replace').read().splitlines()
    if not os.path.exists(MODEL + '.bak'):
        shutil.copy2(MODEL, MODEL + '.bak')
    want = {r[0]: r[2] for r in out}
    n = 0
    for i, l in enumerate(lines):
        f = l.rstrip(',').split(',')
        if f and f[0].strip() in want:
            if len(f) <= COL:
                f = f + [''] * (COL + 1 - len(f))
            if f[COL] != want[f[0].strip()]:
                f[COL] = want[f[0].strip()]
                lines[i] = ','.join(f) + ','
                n += 1
    open(MODEL, 'w', encoding='utf-8').write('\r\n'.join(lines) + '\r\n')
    print('★ 已写模型表 %s：更新 %d 行（备份 %s）' % (MODEL, n, os.path.basename(MODEL) + '.bak'))
    return 0


if __name__ == '__main__':
    sys.exit(main())
