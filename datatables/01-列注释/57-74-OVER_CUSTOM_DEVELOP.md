# OVER_CUSTOM_DEVELOP ｜ `develop/mechanic_overcustom.csv`

- **用途**：超改开发配方
- 表ID `74` ｜ 下载序 `57` ｜ 类名 `CMechanicOverCustomTable` ｜ disposition `DOWNLOAD`
- 逐列读取函数 `sub_57A650` ｜ **列数 7**

| 读序 | CSV# | 订案名 | 类型 | 内存 | 语义（ASM 确证） |
|---|---|---|---|---|---|
| 1 | `0` | `recipe_id` | u32 | +0 | 超改开发配方 ID（主键） |
| 2 | `1` | `msma_id` | u32 | +4 | 目标机体 ID |
| 3 | `2` | `stage` | u32 | +8 | 超改阶段 |
| 4 | `3` | `material_id` | u32 | +12 | 消耗素材物品 ID（→ ITEM） |
| 5 | `4` | `material_qty` | u32 | +16 | 素材消耗数量 |
| 6 | `5` | `gp_cost` | u32 | +20 | GP 开发费用 |
| 7 | `6` | `success_rate` | u32 | +24 | 开发成功率或权重（u32 col6） |

**填写规则**：
- 编码 **UTF-8 无 BOM**、换行 **CRLF**、数据行**保留尾逗号**；`#` 开头整行跳过。
- 枚举列写**名称字符串**（见 `reverse-login-chain/formats/枚举表.md`）。
- **越界列 = 0**：只需写到最大列号，后面可省略。

---

## 复核节（2026-10-05，n3 批次）

**列映射：逐 push 常量复核 `sub_57A650` ⇒ 与上表 7 行逐项一致 ✓**
（push `0..6` → `+0,+4,+8,+0Ch,+10h,+14h,+18h`，全 `sub_BBB370` atoi）⇒ 无列错位、无枚举列。

**内容现状（占位）**：种子 64 行只有字段 0（`recipe_id = 1..64`），字段 `1..6` **全空** ⇒
`msma_id`（字段 1 → `+4`）恒 0、`material_id` 恒 0、`material_qty`/`gp_cost`/`success_rate` 恒 0
⇒ 超改开发配方**没有绑定任何机体/素材**。

★ 真值无来源，不猜（`16-` §11.6 红线）；与 `#72 OVER_CUSTOM` 同病（两表 `msma_id` 都空）。
