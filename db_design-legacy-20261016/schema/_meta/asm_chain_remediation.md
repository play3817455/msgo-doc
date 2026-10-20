# ASM 严格链未过 · Remediation 计划

> 日期：2026-09-20  
> 现状：73 表 evidence_va **0 缺口**；wire 链 **73/73 pass** · memory 链 **54/54 pass**（24 表无槽差跳过）✓

## 根因分类

| 类型 | 表数 | 现象 | 修法 |
|---|---|---|---|
| **A · 槽 vs 线** | ~14 | `member.offset` = 读器写槽 `a1+N`，`length` = 线长 | `offset`→线序；旧值迁到 `memory_offset` |
| **B · 多命令线** | ~5 | 1365 线紧凑 vs A5DA 等同读器不同线偏移 | `offset`=读器线序；每命令 `wire_sources` 保留各自 offset |
| **C · 内存独占** | 2 | dc_point `bef_next`/`aft_next` 不在 41B 线上 | `memory_only: true`，不参与 wire 链 |
| **D · 槽步进阵列** | 2 | xwar row 槽 +0x80 vs 线 124 | row 成员双线 offset + 可选 `_pad` 显式化 |
| **E · 别名** | 4 | member→leaders 等 | 修源 composite 即过 |

## 字段约定（新增）

```json
{
  "name": "avatar",
  "offset": 33,
  "memory_offset": 36,
  "length": 18,
  "memory_only": false
}
```

- `offset`：**wire 链**偏移（审计对比 `composite.length`）
- `memory_offset`：可选；读/写器 `a1+N` 槽位
- `memory_only`：true 时跳过 wire 链（仅校验 `memory_offset` 与 evidence）

## 工具

| 脚本 | 作用 |
|---|---|
| `_scan_asm_fails.py` | 列出全队列 fail |
| `audit_asm_batch.py` | 已升级：wire 链 + memory 链分项 |
| `_remediate_wire_layout.py` | 批量迁移 / 手工 YAML 补丁 |
| `ida_extract_memory_slots.py` | IDA 读器 decompile → `a1+N` / `a1[N]` 槽位 JSON |
| `audit_memory_chain.py` | memory_offset 字段 vs IDA 槽位 + 显式槽链 |
| `_scan_memory_fails.py` | 列出 memory 审计 fail |

## 执行顺序

1. 基础设施（audit v2）✓  
2. 试点：leaders、dc_point、config  
3. batch #2 四表 → #4 config 系 → #5 → #3 ranking 系 → xwar  
4. 别名表随源表自动 pass  
5. 全批重跑 `audit_asm_batch.py 1..8`，目标 chain_ok = 73/73 ✓（2026-09-20）

## 本轮收尾（8→0 fail）

| 表 | 修法 |
|---|---|
| recruits | 尾段线序 pstat@72 → party_type@76（非槽 73/77） |
| AI | param@34 move@39 stat@41；mem≥44 时 wire=mem−3 |
| party_member_stat / ranking | avatar wire@13/77；ws 全量同步 |
| xwar_ext_rule | row 线序 6/130/254/378 + `tail_pad` 502×12 → 514 |
| avatar | E536 sub_B068B0 ws 改为 struct-relative |
| extrarule_xwar_info / toppilots | 别名随源表 pass |
