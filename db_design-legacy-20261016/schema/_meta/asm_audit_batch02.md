# ASM 复核 · 批次 #2（10 表）

> 日期：2026-09-20  
> 工具：`ida_extract_wire_vas.py 2` → `apply_asm_vas.py --vas ida_wire_vas_batch2.json` → `_patch_asm_batch2.py` → `audit_asm_batch.py 2`

## 范围

| # | 表 | 读/写器 | 线长 | 成员 | IDA 解析 total |
|---|---|---|---|---|---|
| 1 | tbl_lpcard | sub_B43100 | 113 | 20 | 65 |
| 2 | tbl_ms | sub_B06D80 | 244 | 43 | 212 |
| 3 | tbl_snapshot | sub_B075A0 | 39 | 21 | 39 |
| 4 | tbl_funnelss | sub_B081C0 | 10 | 3 | 6 |
| 5 | tbl_unlockw | sub_B439D0 | 30 | 6 | 12 |
| 6 | tbl_adop_list | sub_B43D90 | 13 | 3 | 13 |
| 7 | tbl_recruits | sub_B45400 | 80 | 9 | 20 |
| 8 | tbl_leaders | sub_B454D0 | 52 | 7 | 34 |
| 9 | tbl_bracket | sub_B47060 | 166 | 2 | 166 |
| 10 | tbl_AI | sub_B07230 | 165 | 29 | 97 |

## 结论

| 检查项 | 结果 |
|---|---|
| evidence_va 逐字段（IDA 读器取证） | **10/10 · 0 缺口** |
| 成员 offset 链 = length（严格 wire 链） | **6/10 通过** |
| wire_sources 与成员 offset/length 一致 | **10/10 通过** |

### evidence_va 覆盖率

| composite | 有 VA | 缺 VA | 备注 |
|---|---|---|---|
| lpcard | 20/20 | 0 | 尾段 sub_B06230/sub_B02DD0 @ 0xB43213..AE |
| ms | 43/43 | 0 | 尾段 227–243 @ 0xB07157..213；adop 大 loop @ 0xB07134 |
| snapshot | 21/21 | 0 | 全匹配 sub_B075A0 |
| funnelss | 3/3 | 0 | |
| unlockw | 6/6 | 0 | spticket 尾 2B @ 0xB43A48/5B |
| adop_list | 3/3 | 0 | |
| recruits | 9/9 | 0 | comment 0x3D loop + 尾 @ 0xB45487..BE |
| leaders | 7/7 | 0 | 规范 reader VA；printer 保留 `B656FA\|B4D9D0` |
| bracket | 2/2 | 0 | nodes 循环 sub_B46FC0 @ 0xB4707E |
| AI | 29/29 | 0 | 三组 0xA loop + 14×u16 链 @ 0xB0724C..520 |

另：**bracket_node**（子结构 7 成员）已补 @ sub_B46FC0 0xB46FDA..045。

## 严格 offset 链未过（已知：槽内对齐 vs 线上紧凑）

以下 4 表 composite 成员 offset 按 **memory_claim/槽布局** 标注，与 **wire 紧凑链** 不完全重合；wire_sources 与成员 self-consistent，evidence_va 已按读器 asm 逐字段绑定：

| 表 | 现象 |
|---|---|
| tbl_recruits | member_count 槽 10 vs 线 9；尾段 75/78 vs 线 76/80 |
| tbl_leaders | avatar/pstat 槽 36/60 vs 线 33/54 |
| tbl_bracket | nodes 槽 offset 2（is_abort 后 1B 填充）vs 线 1 |
| tbl_AI | param_id/move_spd 槽填充；总长 168 vs 线 165 |

## IDA 取证要点

- **lpcard**：name/clan_name 定长 loop；avatar sub_B068B0；clan_id sub_B02DD0
- **ms**：witem/sitem 三组 loop；eq_modules 0xA×u16 + 0xA×u32；adop_items_eq 四组×4 u32 @ 0xB07134
- **AI**：name 0x21 loop；stat/hate 三组 0xA；坐标 14×u16 链式 sub_B02DF0
- **bracket**：15× sub_B46FC0（11B 线 / 14B 槽步进）

## 缺口补全（2026-09-20）

工具：`tools/_patch_asm_batch2.py`（63 字段，含 AI 读器 VA 修正与 leaders 规范化）
