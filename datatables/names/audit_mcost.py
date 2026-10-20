# -*- coding: utf-8 -*-
"""M-cost 例外核对记录生成器 → `datatables/names/mcost_audit.csv`。

背景
====
服务端的 M-cost（`game.ms_rokaku.mission_cost`）按 `CostToMissionCost` 的**档位表**产出，
档位表的来源是 wiki 抓取的 `wiki_ms_cost.json`（699 页，352 页 COST/MCOST 都有值）。
352 页里有 9 页的 MCOST 与档位表不符，本脚本把**这 9 页**的核对结论落成一张表：

    python datatables/names/audit_mcost.py

判据（2026-10-01 逐页复核）
==========================
- 取 wiki API 原始 wikitext（`action=parse&prop=wikitext`）：9 页**每页只有 1 个
  「高达OL基础性能」模板**，且模板 `序号` 与抓取记录一致 ⇒ 页面上的 COST/MCOST 确属该机体
  （排除「同页多机体、取到隔壁模板」的提取误差）；
- 外部互证（见 `机体名对照表.md` M-cost 小节）：英文资料站写明 M-cost 是「按 COST 查表」的
  派生值；日文 wiki（超攻略）**同一页面**上 infobox 与同 COST 对比表互相矛盾（夏柯 20 vs 30）；
  日服玩家实测面板 260⇒40 / 300⇒30 / 320⇒30 / 340⇒20 与档位表逐条吻合。
  ⇒ 结论：保留档位表，这 9 页按「页面 infobox 的失效值」处理（旧版 M-cost / 沿用日服值）。

`PAGE_FACTS` / `NOTES` 是**人工核对结果**（不是从 CSV 推出来的），改动它们等于改结论 —— 请连同
`机体名对照表.md` 的小节一起改。
"""
import io, os, csv, json

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
COST_JSON = os.path.join(ROOT, 'datatables', 'names', 'wiki_ms_cost.json')
BRIDGE = os.path.join(ROOT, 'datatables', 'names', '机体名对照表.csv')
OUT = os.path.join(ROOT, 'datatables', 'names', 'mcost_audit.csv')

TIERS = [(400, 10), (340, 20), (280, 30), (200, 40), (1, 50)]


def tier(cost):
    for mn, mc in TIERS:
        if cost >= mn:
            return mc
    return 0


# wiki 页面 -> 复核到的页面事实（模板数 / 序号 / COST / MCOST / TIME）
PAGE_FACTS = {
    '高达OL完美独角兽敢达(国)': (1, 110991, 400, 20, 690),
    '高达OL报丧女妖(重击装备)(国)': (1, 120998, 400, 20, 690),
    '高达OLZⅡ(国)': (1, 112986, 360, 10, 490),
    '高达OL敢达Mk-Ⅲ 8号机(重击装备)(国)': (1, 122988, 360, 10, 490),
    '高达OL蓝色命运2号机': (1, 213988, 340, 40, 400),
    '高达OLZ PLUS A1型(试验机配色型)(国)': (1, 113971, 340, 30, 400),
    '高达OL格雷兹骑士(卡尔塔机)': (1, 115966, 300, 40, 250),
    '高达OL夏柯': (1, 216987, 280, 20, 190),
    '高达OLV敢达': (1, 116984, 280, 20, 190),
}

# wiki 页面 -> 逐机备注（结论）
NOTES = {
    '高达OL完美独角兽敢达(国)': '国服机体；页面 MCOST 疑为旧版/日服档位值（400C 的日服前身多为 380C⇒20）',
    '高达OL报丧女妖(重击装备)(国)': '国服首发的 400C 机体；JP 侧同型为 380C⇒20，页面 MCOST 疑为沿用旧值',
    '高达OLZⅡ(国)': '国服版 COST 与日服不同（日服 400C⇒10），页面 MCOST 疑为沿用日服值',
    '高达OL敢达Mk-Ⅲ 8号机(重击装备)(国)': '国服首发 400C 机体降为 360C，页面 MCOST 疑为沿用日服值（10）',
    '高达OL蓝色命运2号机': '非 (国) 机体；页面 MCOST 与档位不符，无外部来源可证（保留档位值）',
    '高达OLZ PLUS A1型(试验机配色型)(国)': '国服版；日服同型为 320C⇒30，页面 MCOST 疑为沿用日服值',
    '高达OL格雷兹骑士(卡尔塔机)': '页面 MCOST 与档位不符；JP 侧同机也是 300C（stoicfps），无外部来源可证（保留档位值）',
    '高达OL夏柯': '★反证：JP 同一页面 infobox 写 20、同页 COST280 对比表写 30 ⇒ infobox 的 MCOST 不可信',
    '高达OLV敢达': '★反证：同上（胜利敢达，与夏柯同族同数值）；且桥表把它误配给了 練度ID 1173011（∀敢达）',
}


def main():
    units = json.load(io.open(COST_JSON, encoding='utf-8'))['units']
    rows = list(csv.reader(io.open(BRIDGE, encoding='utf-8-sig', errors='replace')))
    hdr = [h.lstrip('#') for h in rows[0]]
    idx = {h: i for i, h in enumerate(hdr)}

    by_page = {}
    for r in rows[1:]:
        if not r:
            continue
        p = r[idx['wiki页面']].strip()
        if p:
            by_page.setdefault(p, r)

    out = [['wiki页面', '机体（wiki名）', 'wiki序号', 'COST', 'wiki MCOST', '档位表取值',
            '差', '桥表練度ID', '桥表匹配方式', '桥表分数', '页面复核（模板数/序号）', '备注']]
    n = 0
    for name, info in units.items():
        m = info.get('mcost')
        if m in (None, '', 'None'):
            continue
        cost = int(info.get('cost') or 0)
        mc = int(str(m).strip())
        if mc == tier(cost):
            continue
        n += 1
        page = info.get('page') or ''
        facts = PAGE_FACTS.get(page)
        br = by_page.get(page)
        out.append([
            page, name,
            (facts[1] if facts else ''),
            cost, mc, tier(cost), mc - tier(cost),
            (br[idx['練度ID']] if br else '（桥表未匹配）'),
            (br[idx['匹配方式']] if br else ''),
            (br[idx['分数']] if br else ''),
            ('%d 个模板 / 序号 %s' % (facts[0], facts[1])) if facts else '未逐页复核',
            NOTES.get(page, ''),
        ])
    out[1:] = sorted(out[1:], key=lambda r: -int(r[3]))
    io.open(OUT, 'w', encoding='utf-8-sig', newline='\r\n').write(
        ''.join(','.join('"%s"' % str(c).replace('"', '""') for c in row) + '\r\n' for row in out))
    print('wrote', OUT, n, 'rows')


if __name__ == '__main__':
    main()
