# ASM 复核 · 批次 #8（3 表 · 终批）

> 日期：2026-09-20  
> 工具：`ida_extract_wire_vas.py 8` → `apply_asm_vas.py --vas ida_wire_vas_batch8.json` → `_patch_asm_batch8.py` → `audit_asm_batch.py 8`

## 范围

| # | 表 | 读/写器 | 线长 | 成员 | IDA 解析 total |
|---|---|---|---|---|---|
| 1 | tbl_replay_info | sub_B47340 | 38 | 10 | 38 |
| 2 | tbl_season_rb_conf | sub_B471E0 | 52 | 10 | 52 |
| 3 | tbl_precord | sub_B440B0 | 242 | 61 | 242 |

## 结论

| 检查项 | 结果 |
|---|---|
| evidence_va 逐字段 | **3/3 · 0 缺口** |
| layout_same_as 别名 | **无** |
| 成员 offset 链 = length（严格 wire 链） | **3/3 通过** |
| wire_sources 与成员 offset 一致 | **3/3 通过** |

### evidence_va 覆盖率

| composite | 有 VA | 缺 VA | 备注 |
|---|---|---|---|
| replay_info | 10/10 | 0 | u64 id + helper 尾 5×sub_B02DD0 |
| season_rb_conf | 10/10 | 0 | 7×u32 + mission_id_dm loop + is_end/is_debug |
| precord | 61/61 | 0 | 52×u32 + u16 vsl_td_score_best + 8×u32 尾 |

## IDA 取证要点

- **replay_info**：u64 @ 0xB47362；troopsB sub_B06230；5×u32 尾 @ sub_B473B5..02
- **season_rb_conf**：7×add u32 头；mission_id_dm call_loop×4 @ 0xB47276
- **precord**：61 段顺序 sub_B02DD0 链；offset 208 sub_B02DF0(u16)；242B 线 = 槽线一致

## 缺口补全（2026-09-20）

工具：`tools/_patch_asm_batch8.py`（81 读路径 0x 前缀；IDA total 与线长三表全匹配）

## 全队列状态

批次 #1–#8 均已 `complete` 或 `complete_with_issues`；73 表 ASM 逐字段复核闭环。
