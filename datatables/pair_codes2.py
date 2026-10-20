# -*- coding: utf-8 -*-
"""pair_codes2.py —— 第二轮代号配对：**只用我有把握的代号**扩字典（不再用骨架匹配瞎猜）。

规则：
  1. 遍历 `chara模型代号.csv`（按 C 升序），代码匹配字典 → 名册（关键词：先全等于、再最短名）
  2. 目录已配 / 该台已配 ⇒ 跳过（每台一个目录）
  3. 产出 names/模型号映射-补充.csv；未命中的关键词单独报出
用法：python datatables/pair_codes2.py [--apply]
"""
import io
import os
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
S = os.path.join(ROOT, 'unpackdat', 'settings')
OUT = os.path.join(HERE, 'names', '模型号映射-补充.csv')

# ★代号 → 日文名关键词（多个候选按顺序试；只写有把握的）
KEY = {
    # ── chara/01/01（联邦/SEED/00 主群）
    'GND': ['ガンダム'], 'GND4': ['ガンダム4号機'], 'GND5': ['ガンダム5号機'],
    'GNDG40O': ['ガンダムG40'],
    'FAG7': ['フルアーマーガンダム7号機'], 'FAG': ['フルアーマーガンダム'],
    'GLA': ['ジム・ライトアーマー'], 'GMT': ['ジム・トレーナー'],
    'GMC': ['ジム・コマンド'], 'GMCS': ['ジム・コマンド(宇宙戦仕様)'],
    'GMQL': ['ジム・クゥエル'], 'GSCS': ['ジム・スナイパーカスタム'],
    'GGC': ['ジム・ガードカスタム'], 'GMNS2': ['ジム・スナイパーⅡ'],
    'GSP2': ['ジム・スナイパーⅡ'], 'GSP2LW': ['ジム・スナイパーⅡ'],
    'GIC': ['ジム・インターセプトカスタム'], 'GICFB': ['ジム・インターセプトカスタム'],
    'GSL': ['ジム・スナイパー'], 'GSLF': ['ジム・スナイパー'], 'GMNS': ['ジム・スナイパー'],
    'GME': ['初期型ジム'],
    # ★"81xx" = RX-81（ジーライン）系，不是 RGM-79 ジム系（2026-09-14 更正）
    '81LA': ['ジーライン(ライトアーマー)'], 'RXA': ['ジーライン(アサルトアーマー)'],
    'RXS': ['ジーライン(スタンダードアーマー)'], '81ST': ['ジム・ストライカー'],
    'EZ8': ['ガンダムEz8'], 'ALX': ['ガンダムNT-1'],
    'NT1FA': ['ガンダムNT-1(チョバム・アーマー装備)'],
    'BD2': ['ブルーディスティニー2号機'], 'BD2N': ['ブルーディスティニー2号機'],
    'BD2E': ['ブルーディスティニー2号機'],
    'PDG': ['パワード・ジム'],
    'HVG': ['ヘビーガンダム'],
    '100SK': ['百式'], 'FA100SKC': ['フルアーマー百式改'], 'RYOU100SKC': ['量産型百式改'],
    'JGN': ['ジェガン'], 'STJG': ['スターク・ジェガン'],
    'STGIWSP': ['ストライクI.W.S.P'],
    'GASTRYBF': ['アストレイブルーフレーム'], 'GASTRYRD': ['アストレイレッドフレーム'],
    'GAGE1N': ['AGE-1 ノーマル'], 'GAGE1S': ['AGE-1 ソーディア'],
    # ── chara/01/01 追加（2026-09-14 第二轮：按"代号=英文缩写"扩）
    'GMLT': ['ジム後期生産型'],            # GM Late Type
    'GMCWD': ['ジム(WD隊仕様)'],          # GM Command WD
    'GCLA': ['ジム・コマンド・ライトアーマー'],  # GM Cmd Light Armor
    'AGMUC': ['アクア・ジム'],            # Aqua GM 强化型
    'GNG6': ['ガンダム6号機'],
    'PX': ['ガンダム・ピクシー'],          # Pixy
    'PXF': ['ピクシー(フレッド機)'],        # Pixy Fred
    'GNDFSD': ['ガンダムFSD'],
    '100SKC': ['百式改'],
    'EWJGD': ['EWACジェガン'],
    'HMJG': ['ジェガン(高機動仕様)'],
    'JGBN': ['ジェガン(バーナム所属機)'],
    'JGA2': ['ジェガンA2型'],
    'JST': ['ジェスタ'], 'JSTTU': ['ジェスタ'], 'JSTC': ['ジェスタ・キャノン'],
    'GM2SS': ['ジムⅡ・セミストライカー'],
    'SJGCCA': ['中国用スタークジェガン'],
    'LNSTG': ['ライトニングストライク'],
    'STNG': ['ストライクノワール'],
    'BUSTERO': ['バスターガンダム'],
    'GASTRYBFSLLG': ['ブルーフレームSLローエンー'],
    'GAGE2DB': ['AGE-2 ダブルバレット'], 'GAGE2DBLD': ['AGE-2 ダブルブレイド'],
    'AEUECT': ['AEUイナクト'], 'TRTZ': ['ティエレンタオツー'],
    'GAFRAN': ['ガフラン'], 'FLSA': ['ファルシア'],
    'GINN': ['ジン'], 'DNZ': ['デナン・ゾン'], 'BRG': ['ベルガ・ギロス'],
    'AMKS': ['アマクサ'],
    'KSTRIYA': ['クシャトリヤ'], 'ROZU': ['ローゼン・ズール'],
    # ── chara/01/21（吉翁·扎古系）
    'ZK1': ['ザクⅠ'], 'ZK2': ['ザクⅡ'], 'ZCN': ['ザク・キャノン'],
    'ZKF2': ['ザクⅡF2型'], 'ZHC': ['ザク・ハーフキャノン'],
    'HZAK': ['ハイザック'], 'HZAKC': ['ハイザック・カスタム'],
    'GDFF': ['グフ・フライトタイプ'], 'ZKMN': ['ザク・マリンタイプ'],
    'ZKW': ['ザク・ワーカー'], 'GUF': ['グフ'],
    'SZK': ['ザクIIS型'], 'ZK2S': ['ザクIIS型'],
    'ZKFS': ['ザクⅡFS'], 'ZKM': ['ザク・マリンタイプ'],
    'ZCNG': ['ザクキャノン(グレーデン機)'],
    'ZUD': ['ヅダ'], 'ZUD2U': ['ヅダ予備機'],
    'ZML': ['ザク・マインレイヤー'], 'ZK1G': ['ザクⅠ(ゲラート機)'],
    'ZK3': ['ザクⅢ'], 'ZK3C': ['ザクⅢ改'],
    # ── chara/01/22（グフ/イフリート）
    'MKGF': ['マ・クベ専用グフ'], 'GFC': ['グフカスタム'],
    'IFR': ['イフリート'], 'IFC': ['イフリート改'], 'IFN': ['イフリート・ナハト'],
    # ── chara/01/23（ドム系）
    'RDM': ['リック・ドム'], 'DMTP': ['ドム・トローペン'],
    'DMC': ['ドム・キャノン(単砲装備)'], 'DMC2': ['ドムキャノン（複砲装備）'],
    'PDWG': ['ペズン・ドワッジ'], 'RD2': ['リック・ドムⅡ'],
    # ── chara/01/24（ゲルググ/ディアス/ディジェ）
    'GEL': ['ゲルググ'], 'GLC': ['ゲルググキャノン'],
    'GLJ': ['ゲルググJ'], 'GLJS': ['ゲルググJ'],
    'GMSG': ['ゲルググM'],
    'RD': ['リック・ディアス'], 'RDB': ['リック・ディアス'], 'SD': ['シュツルム・ディアス'],
    'DIJEH': ['ディジェ'],
    # ── chara/01/25〜01/36（水陸両用・ギャン系）
    'KMPH': ['ケンプファー'],
    'GOG': ['ゴッグ'], 'ZGK': ['ズゴック'], 'ZGE': ['ズゴックE'],
    'AGY': ['アッガイ'], 'HYG': ['ハイゴッグ'], 'ZOK': ['ゾック'],
    'JAG': ['ジュアッグ'], 'JAGMSV': ['ジュアッグ'],
    'GYN': ['ギャン'], 'GYNKG': ['ギャン・クリーガー'],
    # ── chara/01/44〜01/71（Ζ/ZZ/ν/F91/V/クロスボーン）
    'QUBE': ['キュベレイ'], 'QUBE2P': ['キュベレイMk-Ⅱ'], 'QUBEP2': ['キュベレイMk-Ⅱ'],
    'RYOQUBE': ['量産型キュベレイ'],
    'ZSSA': ['ズサ'], 'BW': ['バウ'], 'BWMPT': ['バウ(量産型)'],
    'DBWC': ['ドーベン・ウルフ'], 'DBWJ': ['ドーベン・ウルフ'],
    'NGDM': ['νガンダム'], 'NGDMHWS': ['νガンダム(HWS装備)'],
    'MGDM': ['量産型νガンダム'],
    'NTGDM': ['ナラティブガンダム Ｂ装備'], 'NTGDMCP': ['ナラティブガンダム Ｃ装備'],
    'RGZ': ['リ・ガズィ'], 'DLTG': ['デルタガンダム'],
    'ZIONG': ['ジオング'],
    'UNCG': ['ユニコーンガンダム'], 'FAUNCG': ['FAユニコーンガンダム'],
    'BSHN': ['バンシィ・ノルン'], 'BSHNGF': ['バンシィ・ノルン'],
    'PNXE': ['フェネクス'],
    'CBGNDX1': ['クロスボーン・ガンダムX-1'], 'CBGNDX2': ['クロスボーン・ガンダムX-2'],
    'CBGNDX1FC': ['CBガンダムX1フルクロス'], 'CBGNDX0': ['クロスボーン・ガンダムX-0'],
    'GNDF91': ['ガンダムF91'], 'GNDF91H': ['ガンダムF91(ハリソン機)'], 'F90': ['ガンダムF90'],
    'VG': ['ヴィクトリーガンダム'], 'VG2J': ['V2ガンダム'],
    'HVGN': ['ヘビーガン'], 'GCN': ['G・キャノン'], 'ZRAT': ['ゾロアット'],
    'HNGDM': ['Hi-νガンダム'], 'HNGHWS': ['Hi-νガンダム(HWS装備型)'],
    'AGYTB': ['アッガイ火力型'],
    'GDNMSFS': ['ガンダムデュナメス'], 'GDNMSTPD': ['ガンダムデュナメストルペード'],
    '00GND7GI': ['00ガンダム セブンソード'],
}


def norm(s):
    out = []
    for ch in s:
        o = ord(ch)
        out.append(chr(o - 0xFEE0) if 0xFF01 <= o <= 0xFF5E else ch)
    t = ''.join(out).replace('（', '(').replace('）', ')')
    for x in (' ', '　', '・', '･', '.', '·', '-', '−'):
        t = t.replace(x, '')
    return t.lower()


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


def wiki_wcounts():
    """練度ID → wiki 武器数（机体总表 第 36 列），用于交叉校验"""
    m = {}
    p = os.path.join(HERE, 'names', '机体总表.csv')
    if not os.path.exists(p):
        return m
    for f in rows(p):
        if len(f) > 36 and re.fullmatch(r'\d{7}', f[0]):
            try:
                m[f[0]] = int(f[36])
            except ValueError:
                pass
    return m


def main():
    apply = '--apply' in sys.argv
    roster, rnorm = [], {}
    for f in rows(os.path.join(S, 'favms_ok_list.csv')):
        m = re.match(r'^(\d{7})', ''.join(f))
        if not m:
            continue
        rid = m.group(1)
        if rid in [r[0] for r in roster]:
            continue
        roster.append((rid, f[1] if len(f) > 1 else ''))
        if len(roster) > 900:
            break
    for rid, nm in roster:
        rnorm.setdefault(norm(nm), (rid, nm))

    # 已配（人工 + 合并）
    used_dir, used_unit, master = set(), set(), []
    for fn in ('模型号映射-人工.csv', '模型号映射-合并.csv'):
        for f in rows(os.path.join(HERE, 'names', fn)):
            if len(f) > 1 and re.fullmatch(r'\d{7}', f[0]) and re.fullmatch(r'\d{9}', f[1] or ''):
                v = int(f[1])
                master.append((f[0], f[1]))
                used_unit.add(f[0])
                used_dir.add((v // 10**8, (v // 10**6) % 100, (v // 100) % 10000))

    wc = wiki_wcounts()
    add, nohit, conflict = [], [], []
    for f in rows(os.path.join(HERE, 'names', 'chara模型代号.csv')):
        if len(f) < 5:
            continue
        a, b, c, val = int(f[0]), int(f[1]), int(f[2]), f[4]
        # ★注意：不跳过"已用目录" —— 同一模型可被多台（本体 / 重撃装備 / 強襲装備）共用
        for code in f[3].split('/'):
            for kw in KEY.get(code, []):
                hit = rnorm.get(norm(kw))
                if not hit:
                    # 允许"前缀"匹配（取最短名）；★必须是前缀，避免"ユニコーン"命中"FAユニコーン"
                    cand = [v for k, v in rnorm.items() if k.startswith(norm(kw))]
                    hit = sorted(cand, key=lambda x: (len(x[1]), x[1]))[0] if cand else None
                if not hit:
                    nohit.append((code, kw))
                    continue
                rid, nm = hit
                if rid in used_unit:
                    conflict.append((code, rid, nm))
                    break
                add.append((rid, val, nm, code, 'chara/%02d/%02d/%04d' % (a, b, c)))
                used_unit.add(rid)
                break

    print('★新增配对 %d 台（总 %d / %d）' % (len(add), len(used_unit), len(roster)))
    for x in add:
        print('   %s %-26s %-10s %-10s wiki武=%s'
              % (x[0], x[2][:26], x[3], x[4][-9:], wc.get(x[0], '-') if wc else '-'))
    if nohit:
        print('关键词在名册找不到（%d）：%s' % (len(nohit), sorted(set(nohit))[:14]))
    if conflict:
        print('该台已配、跳过（%d）：%s' % (len(conflict), conflict[:8]))

    lst = ['#練度ID,モデルID,机体名,代号,资源目录,来源,']
    for rid, val, nm, code, d in add:
        lst.append('%s,%s,%s,%s,%s,补充,' % (rid, val, nm.replace(',', '，'), code, d))
    open(OUT, 'wb').write(('\r\n'.join(lst) + '\r\n').encode('utf-8'))
    print('写入 %s（%d 行）' % (os.path.relpath(OUT, ROOT), len(lst) - 1))
    return 0


if __name__ == '__main__':
    sys.exit(main())
