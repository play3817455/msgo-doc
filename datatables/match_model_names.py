# -*- coding: utf-8 -*-
"""
match_model_names.py —— 把「練度ID（日文机体名）」配到「chara 模型目录（内部英文代号）」。

为什么需要它：`#5 CHARA_MODEL` 的第 69 列要填**打包值**（= 目录坐标），
而目录里没有日文名，只有**模型文件内部的英文代号**（`MSM_0101_0202_01_GMT` ⇒ GMT）。
日文名 ↔ 英文代号之间没有数字关系，只能靠"名字→罗马字→与代号相似度"来配。

输入：
  `names/chara模型代号.csv`（目录 / 代号 / 打包值，由 scan_model_abbr.py 生成）
  `unpackdat/settings/favms_ok_list.csv`（練度ID / 日文机体名，698 条权威名册）
  + 本文件里的 `CONFIRMED`（已由客户端实测证实的一对一）与 `OVERRIDE`（人工确认）
输出：
  `names/模型号映射-初版.csv`（練度ID, 日文名, 打包值, 目录, 代号, 匹配方式, 相似度）
用法：python datatables/match_model_names.py
"""
import io
import os
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ABBR = os.path.join(HERE, 'names', 'chara模型代号.csv')
FAVMS = os.path.join(ROOT, 'unpackdat', 'settings', 'favms_ok_list.csv')
OUT = os.path.join(HERE, 'names', '模型号映射-初版.csv')

# ── 已由客户端实测证实（练度ID → 打包值）──────────────────────────────
CONFIRMED = {
    '1301011': 101020201,   # ジム・トレーナー（联邦初始）  ✓ 用户实测
    '1301012': 121010201,   # ザク・ワーカー（吉翁初始）    ✓ 用户实测
    '1124081': 101285001,   # フリーダム                    ✓ 用户实测(目录目视=フリーダム)
}
# ── 人工确认的口径（练度ID → 打包值），逐步补充 ────────────────────────
OVERRIDE = {
    '1124011': 101280101,   # エールストライク（文档 35 组真值）
    '1124281': 101285201,   # ストライクフリーダム
    '1132032': 184300101,   # ガンダムエクシア
    '1220101': 101281601,   # バスター(地球連合機)
    '1173021': 101280501,   # ストライクガンダムI.W.S.P.
}
# ── 代号 → 日文名关键词（人工，按需扩充；命中即高置信）──────────────────
CODE_NAME = {
    '00GND': '00ガンダム セブンソード／G',
    '00GND7GI': '00ガンダム セブンソード／G',
    '100SK': '百式',
    '100SKC': '百式改',
    '81LA': 'ジーライン(ライトアーマー)',
    '81ST': 'ジム・ストライカー',
    'AEUECT': 'AEUイナクト',
    'AGM': 'アクア・ジム',
    'AGMUC': 'アクア・ジム',
    'AGY': 'アッガイ',
    'AGYTB': 'アッガイ火力型(TB)',
    'AKTKO': 'アカツキ(シラヌイ)',
    'AKTKS': 'アカツキ(オオワシ)',
    'ALSTG': 'エールストライクガンダム',
    'ALVAARON': 'アルヴァアロン',
    'ALX': 'ガンダムNT-1',
    'AMKS': 'アマクサ',
    'BD1': 'ブルーディスティニー1号機',
    'BD2': 'ブルーディスティニー2号機',
    'BD2E': 'ブルーディスティニー2号機',
    'BD2N': 'ブルーディスティニー2号機',
    'BD3': 'ブルーディスティニー3号機',
    'BIMPLSG': 'ブラストインパルスガンダム',
    'BLITZ': 'ブリッツガンダム',
    'BRG': 'ベルガ・ギロス',
    'BSHN': 'バンシィ・ノルン',
    'BSHNGF': 'バンシィ・ノルン',
    'BUSTERO': 'バスターガンダム(地球連合機)',
    'BUSTERR': 'バスターガンダム(ザフト機)',
    'BW': 'リバウ',
    'BWMPT': 'バウ(量産型)',
    'BYARC': 'バイアラン',
    'CBGNDX0': 'クロスボーン・ガンダムX-0',
    'CBGNDX1': 'クロスボーン・ガンダムX-1',
    'CBGNDX1FC': 'CBガンダムX1フルクロス',
    'CBGNDX2': 'クロスボーン・ガンダムX-2',
    'CMTG': 'カラミティガンダム',
    'DBWC': 'ドーベン・ウルフ',
    'DBWJ': 'ドーベン・ウルフ',
    'DIJEH': 'ディジェ',
    'DLTG': 'デルタガンダム',
    'DMC': 'ドム・キャノン(単砲装備)',
    'DMC2': 'ドムキャノン（複砲装備）',
    'DMTP': 'ドム・トローペン',
    'DNZ': 'デナン・ゾン',
    'DOM': 'ドム',
    'DSTNYGDM': 'デスティニーガンダム',
    'DTP': 'ドム・トローペン',
    'DWC': 'ドワッジ改',
    'DZK': 'ドム',
    'DZKR': 'ドズル専用ザク',
    'EWJGD': 'EWACジェガン',
    'EZ8': 'ガンダムEz8',
    'EZ8WR': 'ガンダムEz8',
    'F90': 'ガンダムF90',
    'FA0GDM': 'フルアーマー0ガンダム',
    'FA100SKC': 'フルアーマー百式改',
    'FAG': 'フルアーマーガンダム',
    'FAG7': 'フルアーマーガンダム7号機',
    'FAUNCG': 'FAユニコーンガンダム',
    'FAZZ': 'フルアーマーZZ',
    'FBDGND': 'フォビドゥンガンダム',
    'FIMPLSG': 'フォースインパルスガンダム',
    'FLSA': 'ファルシア',
    'FRDGND': 'フリーダムガンダム',
    'FRDGNDGCP': 'フリーダムガンダム Ver.GCP',
    'GAFRAN': 'ガフラン',
    'GAGE1N': 'AGE-1 ノーマル',
    'GAGE1S': 'AGE-1 ソーディア',
    'GAGE2DB': 'AGE-2 ダブルバレット',
    'GAGE2DBLD': 'ガンダムAGE-2 ダブルブレイド',
    'GASTRYBF': 'アストレイブルーフレーム',
    'GASTRYBFSLLG': 'ブルーフレームSLローエンー',
    'GASTRYRD': 'アストレイレッドフレーム',
    'GBL': 'ガブスレイ',
    'GC2': 'ガンキャノンⅡ',
    'GCLA': 'ジム・コマンド・ライトアーマー',
    'GCN': 'G・キャノン',
    'GD1': 'ガンダム試作１号機',
    'GDFF': 'グフ・フライトタイプ',
    'GDNMSFS': 'ガンダムデュナメス',
    'GDNMSTPD': 'ガンダムデュナメストルペード',
    'GDS': 'デザート・ジム',
    'GEL': 'ゲルググ',
    'GEXIA': 'ガンダムエクシア',
    'GEXIAR2': 'ガンダムエクシア',
    'GFC': 'グフカスタム',
    'GGC': 'ジム・ガードカスタム',
    'GIC': 'ジム・インターセプトカスタム',
    'GICFB': 'ジム・インターセプトカスタム',
    'GINN': 'ジン',
    'GLA': 'ジム・ライトアーマー',
    'GLC': 'ゲルググキャノン',
    'GLJ': 'ゲルググJ',
    'GLJS': 'ゲルググJ',
    'GM': 'ジム',
    'GM2': 'ジムⅡ',
    'GM2SS': 'ジムⅡ・セミストライカー',
    'GM3': 'ジムⅢ',
    'GMC': 'ジム・コマンド',
    'GMCS': 'ジム・コマンド(宇宙戦仕様)',
    'GMCWD': 'ジム(WD隊仕様)',
    'GME': '初期型ジム',
    'GMH': '陸戦型ガンダム(ジムヘッド)',
    'GMK': 'ジム改(地上戦仕様)',
    'GMK2': 'ジムⅡ',
    'GMK2T': 'ジムⅡ',
    'GMLT': 'ジム・ライトアーマー',
    'GMNS': 'ジム・スナイパー',
    'GMNS2': 'ジム・スナイパーⅡ',
    'GMQL': 'ジム・クゥエル',
    'GMS': 'ジム・スナイパー',
    'GMSG': 'ゲルググM',
    'GMSK': 'ジム・スナイパー',
    'GMST': 'ジム・ストライカー',
    'GMSTN': 'ジム・スナイパーⅡ',
    'GMT': 'ジム・トレーナー',
    'GMTC': 'ジム・トレーナー',
    'GND': 'ガンダム',
    'GND4': 'ガンダム4号機',
    'GND5': 'ガンダム5号機',
    'GNDF91': 'ガンダムF91',
    'GNDF91H': 'ガンダムF91(ハリソン機)',
    'GNDFSD': 'ガンダムFSD[GOR]',
    'GNDG40O': 'ガンダムG40',
    'GNDMK3': 'ガンダムMk-Ⅲ',
    'GNDTRNE': 'ガンダムスローネアイン',
    'GNG': '陸戦型ガンダム',
    'GNG6': 'ガンダム6号機',
    'GOG': 'ゴッグ',
    'GP01': 'ガンダム試作１号機',
    'GP01AQA': 'ガンダム試作１号機',
    'GP02': 'ガンダム試作２号機',
    'GP03': 'ガンダム試作3号機',
    'GP04': 'ガンダム試作4号機',
    'GP04S': 'ガンダム試作4号機',
    'GSC': 'ジム・スナイパーカスタム',
    'GSCS': 'ジム・スナイパーカスタム',
    'GSL': 'ジム・スナイパー',
    'GSLF': 'ジム・スナイパー',
    'GSP2': 'ジム・スナイパーⅡ',
    'GSP2LW': 'ジム・スナイパーⅡ',
    'GUF': 'グフ',
    'GWD': 'ジム(WD隊仕様)',
    'GYN': 'ギャン',
    'GYNKG': 'ギャン・クリーガー',
    'GZJ': 'グフ',
    'GZJD': 'グフ',
    'GZJF': 'グフ',
    'GZS': 'グフ',
    'HAMBB': 'ハンブラビ',
    'HMJG': 'ジェガン(高機動仕様)',
    'HNGDM': 'Hi-νガンダム',
    'HNGHWS': 'Hi-νガンダム(HWS装備型)',
    'HVG': 'ヘビーガンダム',
    'HVGN': 'ヘビーガン',
    'HYG': 'ハイゴッグ',
    'HZAK': 'ハイザック',
    'HZAKC': 'ハイザック・カスタム',
    'IFC': 'イフリート改',
    'IFN': 'イフリート・ナハト',
    'IFR': 'イフリート',
    'IFRMS': 'イフリート',
    'IFRS': 'イフリート',
    'JAG': 'ジュアッグ',
    'JAGMSV': 'ジュアッグ',
    'JGA2': 'ジェガンA2型(GR配備機)',
    'JGBN': 'ジェガン(バーナム所属機)',
    'JGN': 'ジェガン',
    'JGND1': 'ジェガン',
    'JST': 'ジェスタ',
    'JSTC': 'ジェスタ・キャノン',
    'JSTTU': 'ジェスタ',
    'JTSGND': 'ジャスティスガンダム',
    'KMPH': 'ケンプファー',
    'KSTRIYA': 'クシャトリヤ',
    'KYRIOS': 'ガンダムキュリオス',
    'LNSTG': 'ライトニングストライク',
    'METS': 'メタス',
    'MGDM': '量産型νガンダム',
    'MKGF': 'マ・クベ専用グフ',
    'MSR': 'メッサーラ',
    'NGDM': 'νガンダム',
    'NGDMHWS': 'νガンダム(HWS装備)',
    'NT1FA': 'ガンダムNT-1(チョバム・アーマー装備)',
    'NTGDM': 'ナラティブガンダム Ｂ装備',
    'NTGDMCP': 'ナラティブガンダム Ｃ装備',
    'OGDM': '0ガンダム',
    'PALC': 'パラス・アテネ',
    'PDG': 'パワード・ジム',
    'PDWG': 'ペズン・ドワッジ',
    'PFSTG': 'パーフェクトストライク',
    'PNXE': 'フェネクス',
    'PNXZ': 'フェネクス',
    'PRVDNCGND': 'プロヴィデンスガンダム',
    'PSYZAK': '中国用サイコ・ザク',
    'PX': 'ガンダム・ピクシー',
    'PXF': 'ピクシー(フレッド機)',
    'QUBE': 'キュベレイ',
    'QUBE2P': 'キュベレイMk-Ⅱ',
    'QUBEP2': 'キュベレイMk-Ⅱ',
    'RD': 'リック・ディアス',
    'RD2': 'リック・ドムⅡ',
    'RDB': 'リック・ディアス',
    'RDM': 'リック・ドム',
    'RGZ': 'リ・ガズィ',
    'ROZU': 'ローゼン・ズール',
    'RSGM': 'ジム・ライトアーマー',
    'RXA': 'ジーライン(アサルトアーマー)',
    'RXS': 'ジーライン(スタンダードアーマー)',
    'RYOQUBE': '量産型キュベレイ',
    'RYOU100SKC': '量産型百式改',
    'RZL': 'リゼル',
    'SD': 'シュツルム・ディアス',
    'SIMPLSG': 'ソードインパルスガンダム',
    'SJGCCA': '中国用スタークジェガン',
    'SKG': 'ストライクルージュ',
    'SRDM': 'シュツルム・ディアス',
    'STC': 'ストライクノワール',
    'STFRGND': 'ストライクフリーダムガンダム',
    'STGIWSP': 'ストライクガンダムI.W.S.P.',
    'STGIWSPJ': 'ストライクガンダムI.W.S.P.',
    'STJG': 'スターク・ジェガン',
    'STNG': 'ストライクノワール',
    'STRKRG': 'ストライクルージュ',
    'SWCMT': 'ソードカラミティガンダム',
    'SZK': 'シャア専用ザクⅡS型',
    'THE': 'ジ・Ｏ',
    'TRTZ': 'ティエレンタオツー',
    'UNCG': 'FAユニコーンガンダム',
    'VG': 'ヴィクトリーガンダム',
    'VG2': 'V2ガンダム',
    'VG2J': 'V2ガンダム',
    'ZCN': 'ザクキャノン',
    'ZCNG': 'ザクキャノン(グレーデン機)',
    'ZFS': 'ザクⅡF型',
    'ZGE': 'ズゴックE',
    'ZGK': 'ズゴック',
    'ZHC': 'ザク・ハーフキャノン',
    'ZIONG': 'ジオング',
    'ZK1': 'ザクⅠ',
    'ZK1G': 'ザクⅠ(ゲラート機)',
    'ZK2': 'ザクⅡ改',
    'ZK2FB': 'ザクⅡF型',
    'ZK2FD': 'ザクⅡF型',
    'ZK2S': 'ザクIIS型',
    'ZK3': 'ザクⅢ',
    'ZK3C': 'ザクⅢ改',
    'ZKF2': 'ザクⅡF2型',
    'ZKFP': 'ザクⅡF型',
    'ZKFS': 'ザクⅡFS',
    'ZKM': 'ザク・マリンタイプ',
    'ZKMN': 'ザク・マリンタイプ',
    'ZKS': 'ザクⅠ・スナイパータイプ',
    'ZKSS': 'ザクⅠ・スナイパータイプ',
    'ZKT': 'ザクタンク',
    'ZKW': 'ザク・ワーカー',
    'ZML': 'ザク・マインレイヤー',
    'ZNY': 'ザニー',
    'ZOK': 'ゾック',
    'ZRAT': 'ゾロアット',
    'ZSSA': 'ズサ',
    'ZUD': 'ヅダ',
    'ZUD2U': 'ヅダ予備機',
    'ZZG': 'ZZガンダム',
}

# ── 假名 → 罗马字（够用即可）──────────────────────────────────────────
KANA = {
    'ア': 'A', 'イ': 'I', 'ウ': 'U', 'エ': 'E', 'オ': 'O', 'カ': 'KA', 'キ': 'KI', 'ク': 'KU', 'ケ': 'KE',
    'コ': 'KO', 'サ': 'SA', 'シ': 'SHI', 'ス': 'SU', 'セ': 'SE', 'ソ': 'SO', 'タ': 'TA', 'チ': 'CHI',
    'ツ': 'TSU', 'テ': 'TE', 'ト': 'TO', 'ナ': 'NA', 'ニ': 'NI', 'ヌ': 'NU', 'ネ': 'NE', 'ノ': 'NO',
    'ハ': 'HA', 'ヒ': 'HI', 'フ': 'FU', 'ヘ': 'HE', 'ホ': 'HO', 'マ': 'MA', 'ミ': 'MI', 'ム': 'MU',
    'メ': 'ME', 'モ': 'MO', 'ヤ': 'YA', 'ユ': 'YU', 'ヨ': 'YO', 'ラ': 'RA', 'リ': 'RI', 'ル': 'RU',
    'レ': 'RE', 'ロ': 'RO', 'ワ': 'WA', 'ヲ': 'WO', 'ン': 'N', 'ガ': 'GA', 'ギ': 'GI', 'グ': 'GU',
    'ゲ': 'GE', 'ゴ': 'GO', 'ザ': 'ZA', 'ジ': 'JI', 'ズ': 'ZU', 'ゼ': 'ZE', 'ゾ': 'ZO', 'ダ': 'DA',
    'ヂ': 'JI', 'ヅ': 'ZU', 'デ': 'DE', 'ド': 'DO', 'バ': 'BA', 'ビ': 'BI', 'ブ': 'BU', 'ベ': 'BE',
    'ボ': 'BO', 'パ': 'PA', 'ピ': 'PI', 'プ': 'PU', 'ペ': 'PE', 'ポ': 'PO', 'ァ': 'A', 'ィ': 'I',
    'ゥ': 'U', 'ェ': 'E', 'ォ': 'O', 'ッ': '', 'ー': '', '・': '', '（': '(', '）': ')',
    '０': '0', '１': '1', '２': '2', '３': '3', '４': '4', '５': '5', '６': '6', '７': '7', '８': '8', '９': '9',
    'Ｉ': 'I', 'Ｖ': 'V', 'Ｘ': 'X', 'Ｚ': 'Z', 'Ａ': 'A', 'Ｂ': 'B', 'Ｃ': 'C', 'Ｄ': 'D', 'Ｅ': 'E',
    'Ｆ': 'F', 'Ｇ': 'G', 'Ｈ': 'H', 'Ｊ': 'J', 'Ｋ': 'K', 'Ｌ': 'L', 'Ｍ': 'M', 'Ｎ': 'N', 'Ｏ': 'O',
    'Ｐ': 'P', 'Ｑ': 'Q', 'Ｒ': 'R', 'Ｓ': 'S', 'Ｔ': 'T', 'Ｕ': 'U', 'Ｗ': 'W', 'Ｙ': 'Y',
}


def romaji(s):
    out = [KANA.get(ch, ch) for ch in s]
    return re.sub(r'[^A-Z0-9]', '', ''.join(out).upper())


def lcs_ratio(a, b):
    """最长公共子序列占比（0..1，取相对较短串）。"""
    if not a or not b:
        return 0.0
    m, n = len(a), len(b)
    prev = [0] * (n + 1)
    best = 0
    for i in range(1, m + 1):
        cur = [0] * (n + 1)
        for j in range(1, n + 1):
            cur[j] = prev[j - 1] + 1 if a[i - 1] == b[j - 1] else max(prev[j], cur[j - 1])
        best = max(best, cur[n])
        prev = cur
    return best / min(m, n)


def ui_pairs():
    """★真值表：本地 4 个 customize 表里就有「9位モデルID ↔ 日文机体名」——
    9 位 ID 按公式解出即为目录坐标（已由用户实测确认：101285001→chara/01/01/2850=フリーダム ✓）。
    返回 {机体名: 打包值}（9 位的才收；13 位是"大编号"分支，口径未定，先跳过）。"""
    out = {}
    for fn in ('msma_ui_customize.csv', 'msma_visual_customize.csv',
               'msma_mesh_customize.csv', 'msma_mesh_hide_setup.csv'):
        p = os.path.join(ROOT, 'unpackdat', 'settings', fn)
        if not os.path.exists(p):
            continue
        for l in open(p, encoding='utf-8', errors='replace').read().splitlines():
            if not l.strip() or l.lstrip().startswith('#'):
                continue
            f = [x.strip() for x in l.rstrip(',').split(',')]
            if not f or not f[0].isdigit() or len(f[0]) != 9:
                continue
            nm = ''
            for x in reversed(f):                    # 名字一般在最后一格（可带前导 #）
                x = x.lstrip('#').strip()
                if x and not x.isdigit() and not x.isupper() and x not in ('#',):
                    nm = x
                    break
            if nm:
                out.setdefault(nm, int(f[0]))
    return out


def main():
    dirs = []
    for l in open(ABBR, encoding='utf-8').read().splitlines():
        if not l or l.startswith('#'):
            continue
        f = l.split(',')
        if len(f) >= 5 and f[3]:
            dirs.append(dict(a=f[0], b=f[1], c=f[2], abbr=f[3], val=int(f[4]),
                             rel='chara/%s/%s/%s' % (f[0], f[1], f[2])))
    names = []
    for l in open(FAVMS, encoding='utf-8', errors='replace').read().splitlines():
        f = l.split(',')
        if len(f) >= 2 and f[0].strip().isdigit():
            names.append((f[0].strip(), f[1].strip()))
    uip = ui_pairs()
    print('带代号的目录 %d 个 ｜ 名册 %d 条 ｜ UI表真值 %d 条' % (len(dirs), len(names), len(uip)))

    byabbr = {}
    for d in dirs:
        for k in d['abbr'].split('/'):
            byabbr.setdefault(k, d)
    byname = {n: d for d in dirs for n in [CODE_NAME.get(k) for k in d['abbr'].split('/')] if n}

    rows = []
    for (rid, nm) in names:
        if rid in CONFIRMED:
            v = CONFIRMED[rid]
            rows.append((rid, nm, v, '', '', '实测确认', 1.0))
            continue
        if rid in OVERRIDE:
            v = OVERRIDE[rid]
            rows.append((rid, nm, v, '', '', '人工口径', 1.0))
            continue
        v = uip.get(nm)                              # ★UI 表真值（名册名与 UI 表名逐字相同才命中）
        if v:
            rows.append((rid, nm, v, 'chara/%02d/%02d/%04d' % (v // 10 ** 8, (v // 10 ** 6) % 100,
                                                              (v // 100) % 10000), '', 'UI表真值', 1.0))
            continue
        d = byname.get(nm)
        if d:
            rows.append((rid, nm, d['val'], d['rel'], d['abbr'], '代号表命中', 1.0))
            continue
        r = romaji(nm)
        best, bs = None, 0.0
        for dd in dirs:
            for k in dd['abbr'].split('/'):
                # ★必须按【长串】归一化 + 代号至少 4 位，否则 3 字母代号会因"是名字的子序列"而假 1.0
                sc = lcs_ratio(r, k) * min(len(r), len(k)) / float(max(len(r), len(k)))
                if len(k) >= 4 and sc > bs:
                    best, bs = dd, sc
        # ★默认关掉模糊层（实测不可靠：ジム・キャノン→GINN、パワード・ジム→DOM 全是错的）
        if best and os.environ.get('MODEL_FUZZY') == '1' and bs >= 0.5:
            rows.append((rid, nm, best['val'], best['rel'], best['abbr'], '模糊(勿用)', round(bs, 2)))
        else:
            rows.append((rid, nm, '', '', '', '未匹配', round(bs, 2)))

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    L = ['#練度ID,机体名,打包值(第69列),目录,内部代号,匹配方式,相似度,',
         '# 打包值 = A*1e8+B*1e6+C*100+NN ⇒ 目录 chara/0A/B/C（客户端 sub_473390/sub_49D030 实测口径）,',
         '# 用法：把"打包值"写进 msma_model.csv 该行第 69 列；未匹配/低置信的先别写,',]
    L += ['%s,%s,%s,%s,%s,%s,%s,' % r for r in rows]
    open(OUT, 'w', encoding='utf-8').write('\n'.join(L) + '\n')

    import collections
    cnt = collections.Counter(r[5] for r in rows)
    print('已写 %s' % OUT)
    print('  匹配情况：', dict(cnt))
    print('\n=== 自检（应为：フリーダム / ザク・ワーカー / ジム・トレーナー 各自命中已知目录）===')
    for rid in ('1124081', '1301012', '1301011'):
        for r in rows:
            if r[0] == rid:
                print('   %s %-14s %-11s %-22s %s' % (r[0], r[1], r[2], r[3], r[5]))
    print('\n=== 模糊匹配样例（供人工抽查）===')
    k = 0
    for r in rows:
        if r[5] == '模糊匹配' and k < 15:
            print('   %s %-22s → %-11s %-20s %s %s' % (r[0], r[1][:20], r[2], r[3], r[4][:16], r[6]))
            k += 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
