# -*- coding: utf-8 -*-
"""
gen_msma_weapon_set.py —— 生成 `msma/msma_weapon_set.csv`（表ID 1，下载序 1）的**内容**。

产出：`server/datafiles/msma_msma_weapon_set.csv`（服务器实际下发的扁平文件名）

★ 本脚本只做"有内容"这一步（见 `03-还原进度.md` 三阶段：列已注释 → 有内容 → 数值已校准）。

数据来源（全部为仓库内可核对的真实资料，不凭空发明）：
  1) 机体名册        `unpackdat/settings/favms_ok_list.csv`（`練度ID,機体名`，700 行）
  2) 格斗武器池      `unpackdat/settings/weapon_wrestle.csv`
                     （`アイテムID,アイテム名,格闘攻撃ID,最大攻撃回数,追尾最大角度,クール時間,各種エフェクト`）
                     ⇒ 类别确证 = 近接格闘 ⇒ 枚举 `WRESTLE`
  3) 机体数值（备用）`unpackdat/codex/data/units.json`（699 台：armor/speed/boost/payload/type/cost…）

列语义（由 `sub_587160` 反编译实测，见 01-列注释/01-1-MSMA_WEAPONSET.md）：
  col0  = 武器组ID（主键；本表按"練度ID"落，见文件内 `#假设` 说明）
  col2  = ★武器ID → 指向 ITEM 表（`dword_11E3F08` = item/item.csv）★
  col4  = 槽位类别，字面量 `MAIN` / `EX`（`sub_586450`）
  col5  = 武器类别，28 值枚举 `sub_585FD0`（本批 = `WRESTLE`）
  col6  = 启用开关（bool）；消费方 `sub_581690` 只收集该位为真的行
  col7 及 8..29 各列 = 语义未定 ⇒ 一律留空（= 0，不触发 9999 联动）
  col28 = ★地区开关：`CHINA`/空 ⇒ 保留；`JAPAN` ⇒ 整行静默丢弃

用法：
  python gen_msma_weapon_set.py            # 生成
  python gen_msma_weapon_set.py --check     # 只做方言自检，不写文件
"""
import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SETTINGS = os.path.join(ROOT, 'unpackdat', 'settings')
OUT = os.path.join(ROOT, 'server', 'datafiles', 'lounge', 'msma', 'msma_weapon_set.csv')

REGION = 'CHINA'          # col28：CHINA / 空 ⇒ 保留
COLS = 29                 # 列号 0..28
SLOTS = ['MAIN', 'EX', 'EX']   # 每台机体 3 行：1×主武器 + 2×EX（消费方最多收集 3 把）
WEAPON_CLASS = 'WRESTLE'  # 本批武器池 = 近接格闘（`sub_585FD0` 第 7 项）


def load_ms_list():
    """机体名册：練度ID → 機体名（favms_ok_list.csv，700 台）

    注意：源文件有 2 行**缺分隔逗号**（实测：第 578 行 `1148032ギラ・ドーガ(フロ・フロンタル機)`、
    第 618 行 `1166011.ギャプラン`）⇒ 用"前导数字 = ID，其余 = 名"兜底，保证 700 台不漏。
    """
    path = os.path.join(SETTINGS, 'favms_ok_list.csv')
    out = []
    seen = set()
    for line in open(path, encoding='utf-8', errors='replace').read().splitlines():
        line = line.lstrip('\ufeff')
        if not line.strip() or line.lstrip()[0] == '#':
            continue
        parts = line.split(',')
        if len(parts) >= 2 and parts[0].strip().isdigit():
            pair = (parts[0].strip(), parts[1].strip())
        else:
            head = ''
            for ch in line:
                if ch.isdigit():
                    head += ch
                else:
                    break
            if not head or head == line:
                continue
            pair = (head, line[len(head):].lstrip('.．・ '))
        # ★名册有 4 条**完全重复行**（1507011 / 1143031 / 1145022 / 1243022）⇒ 700 行 → 696 个唯一 ID
        #   本表键即 col0（map 键）⇒ 必须按唯一键输出（重复键会互相覆盖/丢行）
        if pair[0] in seen:
            continue
        seen.add(pair[0])
        out.append(pair)
    return out


def load_wrestle_pool():
    """格斗武器池：アイテムID → (アイテム名, 格闘攻撃ID)（weapon_wrestle.csv）"""
    path = os.path.join(SETTINGS, 'weapon_wrestle.csv')
    out = []
    for line in open(path, encoding='utf-8', errors='replace').read().splitlines():
        line = line.lstrip('\ufeff')
        if not line.strip() or line.lstrip()[0] == '#':
            continue
        parts = line.split(',')
        if len(parts) < 3 or not parts[0].strip().isdigit():
            continue
        out.append((parts[0].strip(), parts[1].strip(), parts[2].strip()))
    return out


def load_codex():
    """codex 机体数值：name → dict（备用；本批只用于注释里标注 type/cost）"""
    path = os.path.join(ROOT, 'unpackdat', 'codex', 'data', 'units.json')
    try:
        units = json.load(open(path, encoding='utf-8'))['units']
    except Exception:
        return {}
    return {u['name']: u for u in units}


def build_rows(ms_list, pool):
    """每台机体 3 行（MAIN + EX + EX）；武器按机体序号确定性轮转取池内真实武器。"""
    rows = []
    for i, (ms_id, ms_name) in enumerate(ms_list):
        for k, slot in enumerate(SLOTS):
            wid, wname, atk = pool[(i * len(SLOTS) + k) % len(pool)]
            rows.append((ms_id, wid, slot, wname))
    return rows


def render(rows, ms_list, pool, codex):
    n_ms = len(ms_list)
    hit = sum(1 for _, nm in ms_list if nm in codex)
    head = [
        '#ID,,,,,,,,,,,,,,,,,,,,,,,,,,地区,',
        '# ===== msma/msma_weapon_set.csv （表ID 1 / 下载序 1 / CMSMAWeaponSetTable / 读取函数 sub_587160）=====',
        '# 列语义（静态实测，详见 datatables/01-列注释/01-1-MSMA_WEAPONSET.md）：',
        '#   col0  = 武器组ID（主键）',
        '#   col2  = ★武器ID → 指向 ITEM 表（item/item.csv）★',
        '#   col4  = 槽位类别（枚举 sub_586450：MAIN / EX）',
        '#   col5  = 武器类别（枚举 sub_585FD0 共 28 值；本批 = WRESTLE 近接格闘）',
        '#   col6  = 启用开关；消费方 sub_581690 只收集该位为真的行（最多 3 把/组）',
        '#   col7、col8..col27 = 语义未定 ⇒ 一律留空（读作 0；不触发 col26=9999 的联动规则）',
        '#   col28 = 地区开关：CHINA / 空 ⇒ 保留；JAPAN ⇒ 整行静默丢弃',
        '# 取值来源（全部可回溯到仓库内真实资料）：',
        '#   col0 = 練度ID     ← unpackdat/settings/favms_ok_list.csv（700 台，与 msma_msma_model.csv 同源同序）',
        '#   col2 = 武器アイテムID ← unpackdat/settings/weapon_wrestle.csv（8 把近接格闘武器，真实 ID）',
        '#   col5 = WRESTLE   ← 同上（该表表头即「近接格闘武器」）',
        '# ⚠️ 假设 1（col0 的编号空间）：本表键取"練度ID"，与 msma_model.csv / msma_settings.csv 保持一致。',
        '#      静态依据只到"消费方用机体侧某字段作键"，未能证实该字段就是模型ID ⇒ 列为待证假设。',
        '#      另一候选 = モデルID（9/13 位，见 msma_mesh_customize.csv 的真实配对）⇒ 若后续证实需换，重跑本脚本即可。',
        '# ⚠️ 假设 2（武器↔机体 的对应关系）：无法从现有资料得到"哪台机体挂哪把武器" ⇒ 采用确定性轮转填充；',
        '#      池内每个武器 ID 均为真实值，仅"分配关系"是占位。',
        '# ⚠️ 待补（T2）：射击/盾/特殊/EX 类武器池 —— 需先定案 `item/weapon_settings.csv`(#37) 的类别列后回填。',
        '#   已确证的真实武器参考：unpackdat/settings/weapon_visual_customize.csv（45 个武器ID）、',
        '#                          unpackdat/settings/msma_mesh_customize.csv（モデルID→武器ID 真实配对）',
        '# 依赖：本表 col2 指向 ITEM（#78）与 WEAPON_SETTING（#37）；两张表未填前，武器不会出现在机体上（客户端的静默跳过，不是错误）。',
        '# 生成：python datatables/gen_msma_weapon_set.py（机体 %d 台 × %d 槽 = %d 行）' % (n_ms, len(SLOTS), len(rows)),
        '# codex 可对上数值的机体：%d/%d 台' % (hit, n_ms),
    ]
    lines = list(head)
    for ms_id, wid, slot, wname in rows:
        f = [''] * COLS
        f[0] = ms_id
        f[2] = wid
        f[4] = slot
        f[5] = WEAPON_CLASS
        f[6] = '1'
        f[28] = REGION
        lines.append(','.join(f) + ',')
    return '\r\n'.join(lines) + '\r\n'


def self_check(text):
    b = text.encode('utf-8')
    ok = True
    if b.startswith(b'\xef\xbb\xbf'):
        print('!! 带 BOM'); ok = False
    if b.count(b'\n') != b.count(b'\r\n'):
        print('!! 存在非 CRLF 换行'); ok = False
    body = [x for x in text.split('\r\n') if x and not x.startswith('#')]
    bad = [x for x in body if not x.endswith(',')]
    if bad:
        print('!! %d 行缺尾逗号，例: %r' % (len(bad), bad[0][:60])); ok = False
    if not body:
        print('!! 无数据行'); ok = False
    print('自检：BOM 无 ✓ / CRLF ✓ / UTF-8 ✓ / 尾逗号 ✓' if ok else '自检：失败 ✗')
    print('数据行 %d，注释行 %d' % (len(body), text.count('\r\n#') + 1))
    return ok


def main():
    ms_list = load_ms_list()
    pool = load_wrestle_pool()
    codex = load_codex()
    print('机体名册 %d 台；格斗武器池 %d 把；codex 数值 %d 台' % (len(ms_list), len(pool), len(codex)))
    for wid, wname, atk in pool:
        print('   武器 %s  %s（格闘攻撃ID=%s）' % (wid, wname, atk))
    rows = build_rows(ms_list, pool)
    text = render(rows, ms_list, pool, codex)
    if '--check' in sys.argv:
        if os.path.exists(OUT):
            # ★必须 newline='' 读，否则 Python 通用换行会把 CRLF 折成 LF ⇒ 自检误判
            self_check(open(OUT, encoding='utf-8', newline='').read())
        else:
            print('目标文件不存在')
        return 0
    with open(OUT, 'wb') as f:
        f.write(text.encode('utf-8'))
    print('已写 %s' % OUT)
    self_check(text)
    print('前 3 行数据：')
    for l in [x for x in text.split('\r\n') if x and not x.startswith('#')][:3]:
        print('   ' + l)
    return 0


if __name__ == '__main__':
    sys.exit(main())
