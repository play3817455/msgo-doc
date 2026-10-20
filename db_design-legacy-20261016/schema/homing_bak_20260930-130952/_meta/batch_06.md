# 归位复核批次 · legacy

> 与旧库 UNIQUE 对账不一致：确认新键是改进（旧库压行）还是回归（会丢行）

待判 **11** 项。裁决写回 `schema/homing/_overrides.json`，然后 `python tools/review_homing.py --check`。

| 对象 | 旧表 | 新 PK | 旧 UNIQUE | 依据 |
|---|---|---|---|---|
| `bracket_info` | bracket_info | world_id+pilot_id+bracket_id | world_id+pilot_id | self_named |
| `challenge_info` | challenge_info | world_id+pilot_id+id | world_id+pilot_id | uniqid |
| `clan_eff` | clan_eff | world_id+pilot_id+clan_id | world_id+pilot_id | self_named |
| `item_list` | item_list | world_id+pilot_id | world_id+pilot_id+slot | scope_only |
| `leaders` | leaders | world_id+pilot_id | world_id+pilot_id+slot | scope_only |
| `lpcard` | lpcard | world_id+pilot_id | world_id+pilot_id+slot | scope_only |
| `party_member_stat` | party_member_stat | world_id+pilot_id | world_id+pilot_id+slot | scope_only |
| `ranking` | ranking | world_id+pilot_id | world_id+pilot_id+slot | scope_only |
| `recruits` | recruits | world_id+pilot_id | world_id+pilot_id+slot | scope_only |
| `replay_info` | replay_info | world_id+pilot_id+id | world_id+pilot_id | uniqid |
| `roominfo` | roominfo | world_id+pilot_id+room_id | world_id+pilot_id | self_named |

判法：
* **新键比旧键细**（新多一列）→ 多半是新模型更准，旧库把多行压成了一行；确认后可放行，并在 `note` 里记「旧库压行」。
* **新键比旧键粗**（旧多 `+slot`）→ **危险**：新模型会把多行 upsert 成一行。要判定旧 `slot` 的业务含义（是数组下标，还是「卡片所属机师」这类被丢掉的维度），再决定补成员、还是走 `pk` 订正。
* 裁决写法：`"pk": {"<对象>": ["<成员>", ...]}`。
