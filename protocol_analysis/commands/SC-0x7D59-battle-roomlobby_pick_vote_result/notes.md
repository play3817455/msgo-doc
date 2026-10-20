# 未决问题 / 反例 / 关联 —— SC-0x7D59-battle-roomlobby_pick_vote_result

## 1. 本命令要点

- 报文体线长：48；容量 `0x30`。
- 容量 `0x30`=48 = `4 + 5×4 + 5×4 + 4`，与线长**精确相等**（两个定长数组无线上计数，循环上界为字面量 5）。
- ★**机器草案只抽到 1 个字段**（`0x7D59` 草案 `u32` @0，总长 4）——草案在 `sub_B41740` 阵列预留处停扫，漏掉两个 5 元数组与尾字段；按容量等式人工续扫补齐为 **4 字段**。
- 与同批/同族 `SC-0x30A9-battle-roomlobby_ban_vote_result`（容量同为 `0x30`）结构一致，互为旁证。

## 2. 待补 / 存疑（已标 `?`）

| # | 项 | 现状 | 待补证据 |
|---|---|---|---|
| 1 | `vote_count` / `pick_msma_id` 的席位语义 | ~~仅由日志串 `vote_count={` / `pick_msma_id={` 与 5 元固定长度确定~~ ⇒ ✅ **已定案（2026-09-28）**：`vote_count[i]` 是**原始票数**（第 i 格 = 候选 `pick_msma_id[i]` 得几票），百分比由客户端现算；见 §4 | 已补：消费端 `sub_44EA60` 反汇编（`10000 * vote_count / member_count`，夹在 `[0,10000]`） |

## 3. 关联

- 同批样本见 `_meta\自动化进度.md`「批次记录」的 批次-10 行。
- 方法论：`00-规范-组包格式分析SOP.md` §4/§5/§6/§7；容量口径 `_meta\环境与工具约定.md` §7.5。
- 跨批口径：`_meta\长期记忆.md`（零负载判据 / 槽步进 vs 元素线长 / 分配器指纹 / 守卫与收尾）。

## 4. 下游消费（2026-09-28 复核，定案「票况表」读法）

去向槽 `vt[0xC4]` 的实现链（逐级 `callees` 核实）：

```text
sub_BA8FC0 (vt_thunk) → sub_AFAE10 → sub_44EA60(this, state, vote_count, pick_msma_id, member_count)
```

`sub_44EA60` 反汇编要点（`0x44EA80..0x44EAC2` 的 5 次循环）：

```c
v7 = this + 28755; v8 = 5;
do {
  result = 10000 * *a3 / a5;      // a3 = vote_count[5]，a5 = member_count
  if (result < 0) result = 0;
  else if (result > 10000) result = 10000;
  *(v7 - 5) = *a4;                // a4 = pick_msma_id[5]
  *v7 = result;                   // 折成万分比
  ++a4; ++a3; ++v7;
} while (--v8);
```

⇒ ① `vote_count` 是**分子**（原始票数，不是百分比）；② 客户端拿 `member_count`（= 分母）**现算**
百分比并夹在 `[0,10000]`；③ 两个数组是**平行**的（第 i 格 = 候选 `pick_msma_id[i]` 得
`vote_count[i]` 票）⇒ "逐席位"读法被否掉，**票况表**成立。
另一条同形旁证：`0x30A9` ⇒ `sub_BA8FA0 → sub_AFADF0 → sub_44E960`（结构同形）。
