# -*- coding: utf-8 -*-
"""gen_msma_base_jp.py —— 【已停用 2026-09-28】

  ★★ 本脚本已被 `datatables/gen_msma_machine.py` 取代 ★★
     它同样写 msma_settings.csv + msma_battle_detail.csv，但数值只有「日服 panel」一层；
     现行口径是三层（codex(updated) → 日服 → codex(stale)），见 gen_msma_machine.py 文件头。
     直接跑本脚本会把 codex 主源的数值**覆盖回纯日服** ⇒ 默认已停用（要跑需设 MSMA_ALLOW_LEGACY=1）。

  以下为停用前的原始说明，保留备查：
  —— 用【日服 wiki 面板】给「机体基础参数」播种（两份产物同一份数值）。

产物（就地覆盖，先备份 .bak_wiki）：
  A. server/datafiles/lounge/msma/msma_settings.csv      ← CHARA_PARAM（表ID 4 / 读取 sub_582390）
     只填 6 个数值列（列号 = csv_index，位置对齐 cfg 表的物理列序）：
       col52 boost_gauge_base      ブースト容量
       col83 emergency_return_base 緊急帰投性能
       col85 payload_capacity_base 積載量
       col86 boost_charge_base     ブーストチャージ
       col89 max_speed_base        最高速度
       col90 armor_base            アーマー
  B. server/datafiles/lounge/msma/msma_battle_detail.csv ← MSMA_BATTLE_DETAIL（表ID 34 / 读取 sub_A47BC0）
     7 个属性（行 = `属性名,練度ID十进制串,值`，口径同 gen_msma_battle_detail.py）：
       RESPAWN_TIME(u32)      ← TIME（= **再出撃時間**，击破后的重生等待**秒数**；见 ATTRS 上方注释）
       MAX_HP(u32)            ← アーマー
       MOVE(float)            ← 最高速度
       BOOST_GAUGEMAX(u32)    ← ブースト容量
       BOOST_GAUGEHEAL(float) ← ブーストチャージ
       COST(u32)
       WARP_TIME(u32)         ← 緊急帰投性能
     ★RESPAWN_TIME 是 2026-09-28 补的（此前按"语义未定"不填）；面板 TIME 两档取第一档。

来源（每条可追溯）：
  ① 数值   = 日服 wiki：`gow_wiki/data/units.json` 每台机体的 `panel`（**第一档 = 基础值**，
             第二档 = 强化到顶的面板值）。units.json 由 `gow_wiki/build_units.py` 从
             `gow_wiki/cache/wikitext` 解析（機体比較表 + 机体页），是仓库里唯一的日服数值源。
  ② 練度ID ↔ モデルID = `datatables/names/ms_wiki_pairs.json`（用户给的 ms_wiki_pairs.json 原件、
             只读快照），兜底 `datatables/names/练度ID-モデルID-全集.csv`。
  ③ 名册（練度ID 全集 + 机名）= 现有 msma_settings.csv（来自客户端 favms_ok_list.csv，696 台）。
             ★名册顺序一律不动（它同时是客户端图鉴的 696 台），本脚本**只加列值、不加/不删/不排序行**，
             唯二例外是 units.json 里有面板、但名册没有的 4 台（追加在末尾，见 --check 输出）。

★ 为什么取「机体页 panel」而不是「機体比較表 的 装甲 列」：
  两处对装甲这一栏 119/510 台不一致（ジム：panel 3425 / 比較表 2510；ジム寒冷地仕様：3620 / 3185）。
  依据三条：① panel 就是玩家在游戏里看到的面板数（「面板」二字的所指）；② 中文 wiki（codex）
  在装甲一栏与 panel 同值的有 252 台、与 比較表 同值的更少；③ 比较表是人工维护的汇总表、
  机体页更新更勤。⇒ 本批取 panel。逐台差异用 `--check` 可打印。

★ 不填的列（无证据 ⇒ 不猜，与仓库惯例一致）：
  - col4 rank / col7 combat_role / col8 faction / col9,10,11 terrain_proper_*：
    日服 wiki 的 `機体タイプ`（強襲/重撃/支援/砲撃/狙撃）与客户端枚举
    （`sub_5804F0`：ASSAULT_A=1/ASSAULT_B=2/SNIPE=3/CANNON=4/SUPPORT=5）的**对应未取证**；
    地形三列（+136/+140/+144）连「是不是 0/1 标志」都没定。⇒ 全留空。
  - `緊急帰投性能` 的第二档不是固定倍率（实测比值 1.06~2.84，见 docs/01 §⑩），
    所以**只写第一档**，第二档不落库（那是「强化到顶」的面板值，属 ②实例层）。
  - `TIME`（RESPAWN_TIME）的第二档同理**只写第一档**：第二档是"强化到顶"的面板值，
    属 ②实例层，而且没有任何"缩短再出击时间"的强化项取证 ⇒ 不接。
    第一档的下游对应**已定案**：`respawn_wait_sec`/`respawn_wait_max`/`0xFEBB.countdown_msec`
    三处是同一个数（= 再出撃時間；见 serverv/internal/battle/warp.go 的文件头 ★）。

用法：
  python datatables/gen_msma_base_jp.py           # 生成（备份 + 自检）
  python datatables/gen_msma_base_jp.py --check   # 只自检 + 打印覆盖/差异统计（不写文件）
"""
import io
import json
import os
import re
import shutil
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PAIRS = os.path.join(HERE, 'names', 'ms_wiki_pairs.json')
MID_FULL = os.path.join(HERE, 'names', '练度ID-モデルID-全集.csv')
JPUNITS = os.path.join(ROOT, 'gow_wiki', 'data', 'units.json')
MSDIR = os.path.join(ROOT, 'server', 'datafiles', 'lounge', 'msma')
OUT_SETTINGS = os.path.join(MSDIR, 'msma_settings.csv')
OUT_DETAIL = os.path.join(MSDIR, 'msma_battle_detail.csv')

SET_COLS = 92          # CHARA_PARAM 的 csv_index 0..91（cfg 表物理列 = 92）
NAME_COL = 5
ID_COL = 0
MID_COL = 1

# (csv_index, units.json panel 键, 说明)
NUM_COLS = [
    (52, 'ブースト容量', 'boost_gauge_base'),
    (83, '緊急帰投性能', 'emergency_return_base'),
    (85, '積載量', 'payload_capacity_base'),
    (86, 'ブーストチャージ', 'boost_charge_base'),
    (89, '最高速度', 'max_speed_base'),
    (90, 'アーマー', 'armor_base'),
]

# (col0 属性名, units.json panel 键, 值类型)
#
# ★第一项 RESPAWN_TIME（子表 1）= 面板的 `TIME` = **再出撃時間**（击破后到能再出击的等待**秒数**）。
#   2026-09-28 补：这条的语义已定，不是"未定 ⇒ 不猜"了 —— 依据是
#     ① 词表 `off_D7A298` 的名字就叫 RESPAWN_TIME（`sub_57BB70` 分派到子表 1）；
#     ② `gow_wiki/战斗模型推导报告.md` §6.2.7⑨ 已写 `RESPAWN_TIME | 1 | — | 复活时间`，
#        并把 `SC-0x1EA5 entity_msma_reborn` 标成「复活（RESPAWN_TIME）」；
#     ③ 协议侧 `SC-0x9105` 的 `repair_wait_sec`（日志串 `repair_wait_sec=`）与
#        `SC-0x8DE4` 的 `respawn_wait_sec` / `respawn_wait_max` 就是这一格；
#     ④ 第三方资料直接称它为**再出撃時間**（"ザクⅠ：再出撃時間が短く"、
#        "バトルアシストモジュール：1スロットあたり+5コスト相当の再出撃時間"）。
#   ★**单位 = 秒**（定案 2026-09-28）：面板 `TIME` 就是秒，**不除以 10**，原样落库。
#   ⇒ 服务端的"重生等待"就从这里取（`store.LoadMsmaBaseParams` → `battle.MachineBase.RespawnWaitSec`）。
#   ⚠ 只写第一档；第二档（强化到顶）不落库（同下面的 `緊急帰投性能` 口径）。
ATTRS = [
    ('RESPAWN_TIME', 'TIME', 'int'),
    ('MAX_HP', 'アーマー', 'int'),
    ('MOVE', '最高速度', 'float'),
    ('BOOST_GAUGEMAX', 'ブースト容量', 'int'),
    ('BOOST_GAUGEHEAL', 'ブーストチャージ', 'float'),
    ('COST', 'COST', 'int'),
    ('WARP_TIME', '緊急帰投性能', 'int'),
]

NUM_RE = re.compile(r'-?\d+')


def num(s):
    """取单元格里的**第一个**数字。

    ★必须按空白先切词，不能先把空格删掉：wiki 里有若干单元格在**同一格里**写了两个数
    （第二档/注记），例如 `アーマー = "4,150 8,300"`（基础 4150 / 强化到顶 8300）、
    `最高速度 = "1,185 1,540"`。先删空格会拼成 `41508300` —— 那是 4000 万点装甲，
    机体永远打不死（B7 的层三统计就是靠这条口径发现并修掉的）。
    `"1,219 (1,279)"` 这类括注不受影响：切词后首词仍是 `1,219` ⇒ 1219。
    """
    tok = (s or '').replace(',', '').split()
    if not tok:
        return None
    m = NUM_RE.search(tok[0])
    return int(m.group(0)) if m else None


def base_of(panel, key):
    """panel 的第一档 = 基础值（第二档是强化到顶，不落库）。"""
    v = (panel or {}).get(key) or []
    return num(v[0]) if v else None


def rows_of(path):
    out = []
    for line in io.open(path, encoding='utf-8', errors='replace').read().splitlines():
        if not line.strip() or line.lstrip().startswith('#'):
            continue
        out.append(line)
    return out


def load_roster():
    """现有 msma_settings.csv 的名册（顺序原样保留）：[(練度ID, モデルID, 机名)]。"""
    out = []
    for line in rows_of(OUT_SETTINGS):
        p = line.split(',')
        lid = p[ID_COL].strip()
        if not lid.isdigit():
            continue
        mid = p[MID_COL].strip() if len(p) > MID_COL else ''
        name = p[NAME_COL].strip() if len(p) > NAME_COL else ''
        out.append((lid, mid, name))
    return out


def load_mid_full():
    m = {}
    p = MID_FULL
    if not os.path.exists(p):
        return m
    for line in io.open(p, encoding='utf-8-sig', errors='replace').read().splitlines():
        if not line.strip() or line.startswith('#'):
            continue
        c = line.split(',')
        if len(c) >= 2 and c[0].strip().isdigit() and c[1].strip().isdigit():
            m.setdefault(c[0].strip(), c[1].strip())
    return m


def load_pairs():
    """ms_wiki_pairs.json → {練度ID: モデルID}（+ 反查：モデルID → wiki 名，仅供报告）。"""
    d = json.load(io.open(PAIRS, encoding='utf-8'))
    lid2mid, mid2name = {}, {}
    for p in d.get('pairs') or []:
        lid = (p.get('lid') or '').strip()
        mid = (p.get('mid') or '').strip()
        if lid.isdigit() and mid.isdigit():
            lid2mid.setdefault(lid, mid)
        if mid and p.get('wiki'):
            mid2name.setdefault(mid, p['wiki'])
    return lid2mid, mid2name


def load_jp_panels():
    """日服 wiki → {練度ID: (机名, panel)}。

    同一个 練度ID 可能落在多条 wiki 条目上（如「アクア・ジム」与「アクア・ジム（トリントン）」）：
    取**名字不含「（」的那条**（本名优先），其次按键数多的，最后按名字排序 —— 保证确定性。
    """
    units = json.load(io.open(JPUNITS, encoding='utf-8'))
    g = {}
    for u in units:
        lid = (u.get('dev_id') or '').strip()
        if not lid.isdigit():
            continue
        g.setdefault(lid, []).append(u)

    def rank(u):
        nm = u.get('name') or ''
        return ('（' in nm or '(' in nm, -len(u.get('panel') or {}), nm)

    return {lid: (sorted(v, key=rank)[0].get('name') or '', sorted(v, key=rank)[0].get('panel') or {})
            for lid, v in g.items()}


def fmt(v, kind):
    if kind == 'float':
        return '%.6f' % float(v)
    return str(int(v))


def build():
    roster = load_roster()
    lid2mid, _ = load_pairs()
    mid_full = load_mid_full()
    panels = load_jp_panels()

    roster_ids = {lid for lid, _m, _n in roster}
    extra = sorted(lid for lid in panels if lid not in roster_ids)

    rows, panels_seq, filled = [], [], 0
    mid_src = {'pairs': 0, '全集': 0, '原值': 0, '无': 0}
    for lid, mid_old, name_old in roster:
        fields = [''] * SET_COLS
        fields[ID_COL] = lid
        mid = lid2mid.get(lid)
        if mid:
            mid_src['pairs'] += 1
        else:
            mid = mid_full.get(lid)
            if mid:
                mid_src['全集'] += 1
            else:
                mid = mid_old
                mid_src['原值' if mid else '无'] += 1
        fields[MID_COL] = mid
        name = name_old or (panels.get(lid) or ('', {}))[0]
        fields[NAME_COL] = name.replace(',', '・')

        panel = (panels.get(lid) or ('', {}))[1]
        for idx, key, _col in NUM_COLS:
            v = base_of(panel, key)
            if v is not None:
                fields[idx] = str(v)
        if any(fields[i] for i, _k, _c in NUM_COLS):
            filled += 1
        rows.append(fields)
        panels_seq.append(panel)

    for lid in extra:
        nm, panel = panels[lid]
        fields = [''] * SET_COLS
        fields[ID_COL] = lid
        fields[MID_COL] = lid2mid.get(lid, '')
        fields[NAME_COL] = (nm or '').replace(',', '・')
        for idx, key, _col in NUM_COLS:
            v = base_of(panel, key)
            if v is not None:
                fields[idx] = str(v)
        filled += 1
        rows.append(fields)
        panels_seq.append(panel)

    return rows, panels_seq, filled, roster, extra, mid_src


def project_verified_r001_roles(rows):
    # Verified v15 role/label readers and original wiki main tables; only two units.
    import json
    from pathlib import Path
    tools_dir = Path(__file__).resolve().parents[1] / 'serverv' / 'tools'
    if str(tools_dir) not in sys.path:
        sys.path.insert(0, str(tools_dir))
    from project_chara_roles import resolve_roles, project_rows
    project_root = tools_dir.parents[1]
    units = json.loads((project_root / 'gow_wiki/data/units.json').read_text(encoding='utf-8'))
    crosswalk = json.loads((tools_dir / 'chara_role_crosswalk_v15.json').read_text(encoding='utf-8'))
    bindings = resolve_roles(units, project_root / 'gow_wiki/cache/wikitext', crosswalk)
    return project_rows(rows, bindings)


def render_settings(rows, filled, extra):
    rows = project_verified_r001_roles(rows)
    head = [
        '#模型ID（=練度ID）,,,,,名称,',
        '# ===== msma/msma_settings.csv （CHARA_PARAM / 表ID 4 / 下载序 4 / CCharaParamTable / 读取函数 sub_582390）=====',
        '# 本表 = ★机体参数主表★。行键 col0 = 練度ID（7 位）；col1 = モデルID（9 位，客户端 sub_A86810 用它拼 chara/ 路径）',
        '# ★★2026-09-27：**日服基础数值已播种**（本批）。填的全是「机体页面板第一档 = 基础值」：',
        '#   col52 ブースト容量(col52→+248) / col83 緊急帰投性能(col83→+252) / col85 積載量(col85→+356)',
        '#   col86 ブーストチャージ(col86→+256) / col89 最高速度(col89→+244) / col90 アーマー(col90→+148)',
        '# 数值源：gow_wiki/data/units.json 的 panel（日服 wiki，见 gow_wiki/build_units.py）；',
        '#   ID 源：datatables/names/ms_wiki_pairs.json（練度ID↔モデルID）+ 练度ID-モデルID-全集.csv 兜底；',
        '#   名册：仍来自客户端 favms_ok_list.csv（696 台，顺序不动）；本轮末尾追加日服面板有值、名册缺的 %d 台。' % len(extra),
        '# 仍有值 = %d 台（其余名册行只填 ID/名，数值留空 = 未知，见 docs/01 §⑩「读不到 ≠ 0」）。' % filled,
        '# R001两台col7由project_verified_r001_roles保护；其余旧列解释仍需按当前权威来源重审。',
        '#   —— 日服 wiki 的 機体タイプ（強襲/重撃/支援/砲撃/狙撃）与客户端枚举 sub_5804F0',
        '#   （ASSAULT_A=1/ASSAULT_B=2/SNIPE=3/CANNON=4/SUPPORT=5）的对应未取证；地形三列连是否 0/1 标志都没定。',
        '# ★面板第二档（强化到顶）不写进本表：那是②实例层的东西；緊急帰投性能 第二档还不是固定倍率。',
        '# 生成：python datatables/gen_msma_base_jp.py',
    ]
    lines = list(head)
    for f in rows:
        lines.append(','.join(f) + ',')
    return '\r\n'.join(lines) + '\r\n'


def render_detail(rows, panels_seq):
    head = [
        '#属性名,键,值,',
        '# ===== msma/msma_battle_detail.csv （MSMA_BATTLE_DETAIL / 表ID 34 / 下载序 34 / CMSMABattleDetailTables / 读取 sub_A47BC0）=====',
        '# 本表 = ★机体战斗明细的"属性→值"长表★：一个容器装 13 张子表，col0 的属性名决定进哪张子表。',
        '#   结构实测：sub_A47BC0 读 col0 → sub_57BD40 查词表 off_D7A298 → sub_57BB70 按编号 1..10 分派到子表；',
        '#             子表再读 col1（★字符串键★）与 col2（值；每个子表自带取列函数 sub_BBB370=整型 / sub_BBB470=浮点）。',
        '# ★col0 词表（名 → 子表编号）：',
        '#   RESPAWN_TIME=1  WARP_TIME=2  COST=3  MAX_HP=4  ENERGY=5',
        '#   MOVE=6  BOOST_GAUGEMAX=7  BOOST_GAUGEHEAL=8  BOOST_SPEED=9  JUMP=10',
        '#   （SHOT/LOCKON/RELOAD 三张子表不在本词表 ⇒ 由别的表喂）',
        '# ★★2026-09-27：本批改成**日服口径**（旧内容 = 中文 wiki/codex 口径，已备份 .bak_wiki）。',
        '#   ★★2026-09-28：补 1 个属性 RESPAWN_TIME（此前按"语义未定"不填）；单位 = 秒（定案，不除以 10）。',
        '#   填 7 个属性（除 RESPAWN_TIME 外的 6 个 = msma_settings.csv 的 6 个 *_base，两处永远一致）：',
        '#   RESPAWN_TIME(u32)←TIME(= **再出撃時間**：击破后到能再出击的等待**秒数**（不除以 10）；',
        '#     对应下行 SC-0x9105.repair_wait_sec / SC-0x8DE4.respawn_wait_sec / 0xFEBB.countdown_msec；',
        '#     见 ATTRS 上方注释的 4 条依据)',
        '#   MAX_HP(u32)←アーマー   MOVE(float)←最高速度        BOOST_GAUGEMAX(u32)←ブースト容量',
        '#   BOOST_GAUGEHEAL(float)←ブーストチャージ            COST(u32)←COST   WARP_TIME(u32)←緊急帰投性能',
        '#   数值源：gow_wiki/data/units.json 的 panel 第一档（日服 wiki 机体页）。',
        '#   不填：ENERGY / BOOST_SPEED / JUMP（语义或列数未定 ⇒ 不猜；旧文件里那 3 项是',
        '#   中文 wiki 口径的残值，本批按"日服为准"撤下，需要时从 .bak_wiki 取回）。',
        '# 键 col1 = 練度ID 的十进制字符串（口径不变；已证"键是字符串"）。',
        '# 生成：python datatables/gen_msma_base_jp.py',
    ]
    lines = list(head)
    n = 0
    for f, panel in zip(rows, panels_seq):
        lid = f[ID_COL]
        for attr, key, kind in ATTRS:
            v = base_of(panel, key)
            if v is None:
                continue
            lines.append('%s,%s,%s,' % (attr, lid, fmt(v, kind)))
            n += 1
    return '\r\n'.join(lines) + '\r\n', n


def check_file(text, tag, want_cols, digit_first=True):
    b = text.encode('utf-8')
    ok = True
    if b.startswith(b'\xef\xbb\xbf'):
        print('!![%s] 带 BOM' % tag); ok = False
    if b.count(b'\n') != b.count(b'\r\n'):
        print('!![%s] 存在非 CRLF 换行' % tag); ok = False
    body = [x for x in text.split('\r\n') if x and not x.startswith('#')]
    if not body:
        print('!![%s] 无数据行' % tag); ok = False
    if [x for x in body if not x.endswith(',')]:
        print('!![%s] 数据行缺尾逗号' % tag); ok = False
    if want_cols:
        bad = [x for x in body if len(x.split(',')) - 1 != want_cols]
        if bad:
            print('!![%s] 列数 != %d 的行有 %d 条，例：%s' % (tag, want_cols, len(bad), bad[0][:120]))
            ok = False
    if digit_first and [x for x in body if not x.split(',')[0].strip().isdigit()]:
        print('!![%s] 首列不是数字' % tag); ok = False
    print('[%s] 自检 %s  UTF-8 无 BOM ✓ / CRLF ✓ / 尾逗号 ✓ / 列数=%s / 数据行=%d'
          % (tag, '✓' if ok else '✗', want_cols or '任意', len(body)))
    return ok


def write_and_backup(path, text):
    if os.path.exists(path):
        bak = path + '.bak_wiki'
        if not os.path.exists(bak):
            shutil.copy(path, bak)
            print('  备份 → %s' % os.path.basename(bak))
        else:
            print('  备份已存在（保留首次）→ %s' % os.path.basename(bak))
    with io.open(path, 'wb') as f:
        f.write(text.encode('utf-8'))
    print('  写入 %s' % path)


def report_name_conflicts(panels, roster_names):
    """对账：pairs 里给出的 練度ID 与日服 wiki 同名条目是否对得上（用机名交叉验证）。"""
    d = json.load(io.open(PAIRS, encoding='utf-8'))
    checked = agree = 0
    bad = []
    for p in d.get('pairs') or []:
        lid = (p.get('lid') or '').strip()
        if not lid.isdigit() or lid not in panels:
            continue
        jp = panels[lid][0]
        cands = set()
        for k in p.get('known') or []:
            if (k.get('lid') or '').strip() == lid and k.get('jp'):
                cands.add(k['jp'].strip())
        for z in p.get('zh') or []:
            if (z.get('lid') or '').strip() == lid and z.get('jp'):
                cands.add(z['jp'].strip())
        if not cands:
            continue
        checked += 1
        if jp in cands or roster_names.get(lid) in cands:
            agree += 1
        elif len(bad) < 8:
            bad.append((lid, jp, sorted(cands)))
    print('名对账（pairs 的 lid ↔ 日服 wiki 机名）：可比 %d 条，一致 %d，不一致 %d'
          % (checked, agree, checked - agree))
    for lid, jp, cands in bad:
        print('   ⚠ %s 日服wiki=%s  pairs候选=%s' % (lid, jp, cands))


def report(rows, filled, roster, extra, mid_src, settings_text, detail_text, detail_rows):
    print('名册 %d 台 + 追加 %d 台 = %d 行；有日服数值 %d 台'
          % (len(roster), len(extra), len(rows), filled))
    print('col1 モデルID 来源：pairs=%d / 全集csv=%d / 原值=%d / 无=%d'
          % (mid_src['pairs'], mid_src['全集'], mid_src['原值'], mid_src['无']))
    if extra:
        print('追加行（日服面板有值、名册缺）：%s' % ', '.join(extra))
    print('battle_detail：%d 属性 × 有值机体 = %d 行' % (len(ATTRS), detail_rows))
    print('  msma_settings.csv %d B ｜ msma_battle_detail.csv %d B'
          % (len(settings_text.encode('utf-8')), len(detail_text.encode('utf-8'))))


def main():
    if os.environ.get('MSMA_ALLOW_LEGACY') != '1':
        print('!! gen_msma_base_jp.py 已停用（2026-09-28）：数值口径已并入 datatables/gen_msma_machine.py')
        print('   本脚本只有「日服 panel」一层，跑起来会把 codex 主源的数值覆盖回去 ⇒ 默认不执行。')
        print('   ★现行生成器：python datatables/gen_msma_machine.py')
        print('   （确需重跑旧口径：设环境变量 MSMA_ALLOW_LEGACY=1）')
        return 2
    check_only = '--check' in sys.argv
    rows, panels_seq, filled, roster, extra, mid_src = build()
    settings_text = render_settings(rows, filled, extra)
    detail_text, detail_rows = render_detail(rows, panels_seq)
    report(rows, filled, roster, extra, mid_src, settings_text, detail_text, detail_rows)
    if not check_only:
        print('\n[1] msma_settings.csv')
        write_and_backup(OUT_SETTINGS, settings_text)
        print('\n[2] msma_battle_detail.csv')
        write_and_backup(OUT_DETAIL, detail_text)
    ok = check_file(settings_text, 'settings', SET_COLS)
    ok = check_file(detail_text, 'detail', 3, digit_first=False) and ok
    if check_only:
        roster_names = {lid: nm for lid, _m, nm in roster}
        report_name_conflicts(load_jp_panels(), roster_names)
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
