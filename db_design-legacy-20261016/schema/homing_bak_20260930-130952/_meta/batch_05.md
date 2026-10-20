# 归位复核批次 · evidence

> 有定位但无地址级 VA：补 VA 或接受按 evidence_ref 追溯

待判 **7** 项。裁决写回 `schema/homing/_overrides.json`，然后 `python tools/review_homing.py --check`。

| 对象 | 无 VA 成员数 |
|---|---|
| `favms` | 18 |
| `favms_add` | 18 |
| `bonus_event` | 16 |
| `clan_search_hit` | 15 |
| `result_wave` | 10 |
| `examination_item` | 2 |
| `rental_module` | 2 |

口径：这批不阻塞归位（有 `evidence_ref` 可追溯），要严格满足「指回 VA」就得回 IDA 补地址（走 verify 批次）。
