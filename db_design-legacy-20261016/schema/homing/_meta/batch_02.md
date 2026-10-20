# 归位复核批次 · fold

> 同形线布局未折叠：判定是否同一业务对象

待判 **5** 项。裁决写回 `schema/homing/_overrides.json`，然后 `python tools/review_homing.py --check`。

| 同形组 |
|---|
| `bmgpack`, `item_list` |
| `favms`, `favms_add` |
| `funnel_snapshot_entry`, `funnelss` |
| `navi_entry`, `unlocked_navi` |
| `pcard`, `pilots_list` |

裁决写法：`"fold": [{"composites": ["a","b"], "as": "a"}]`
