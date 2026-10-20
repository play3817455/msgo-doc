# 分析笔记 —— CS-0xA8FE-battle-weapon_fire_prepare__destruct_r

> 状态：`DONE`（2026-09-20，批次-20）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0x010E; call <reg>`（容量 `push` @ `0xB399DA`）。
- 字段名取自**提交（`sub_B02FF0`）之后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)` @ `0xB3A17A`。
- 附加通知：`[obj+79A8h]` 回调模块 id `0x08D` @ `0xB3A195`（发送成功后的统计/日志钩子）。
- 容量等式：上限场景 `2 + 3×4 + 7×(4 + 16×2) + 2 = 268 ≤ 容量 0x10E = 270`（富余 2）
- 结构体/数组展开：7 组变长数组均为 `u32 count` + `count × u16`（每组计数上限 16，`cmp ebp,10h; ja 出错`）；数组名取自打印器日志串。
- 类型判定：一律取**写线指令宽度**（内联 `mov [reg],src` 看目标/源操作数宽度；`sub_B02D80/B02DA0/B061C0/B06190/B061E0/B02B40`），
  **不采用伪代码类型**。**顶层 1 字节字段按写线操作数宽度记 `u8`**（打印器 `sub_B0C1F0` 的 `movsx` 只表示打印时符号扩展，不改线宽）。

## 与其他命令的关联

- 配对命令：S→C `SC-0xEAEA-battle-weapon_fire_prepare__destruct`（已 DONE）

## 未决 / 存疑

- 7 组数组的「计数」字段在日志中没有单独打标签（命名按 `<数组名>_count` 推定，类型/长度/上限均已确证）。

---

## 追加：调用方取证 ⇒ 本命令是「命中上报短格式」，不是 destruct（2026-09-27）

**原结论**：本命令 = 上发「自爆（destruct）发射准备」，语义依据是函数内 trace 串
`")<-_proto_battle_client::send_weapon_fire_prepare__destruct_r( "` @`0xEE0F68`。

**推翻依据（生产者/调用方唯一性）**：

| 事实 | 证据 |
|---|---|
| `sub_B39990` 的调用者**只有 1 处** | `xrefs(0xB39990)` = `0xB024D1`（在 `sub_B02460` 内） |
| `sub_B02460` 的调用者**只有 1 处** | `xrefs(0xB02460)` = `0x517E74`（在 `sub_517D50` 内） |
| `sub_517D50` 正是 `CS-0x770D weapon_hit_to` 的上报器，且两条分支读**同一块**命中暂存区 | `0x517DCA` 调 `sub_5173F0(…, sub_517AF0)`；`0x517D8A` `sub_CC6510(&dword_11EB810, 0, 284)` 清零 |
| 短格式分支传入的实参就是命中数组 | `0x517E30~0x517E79`：`&word_11EB818`(ent_ids) / `&word_11EB8CC`(pos_x) / `&word_11EB8EC`(pos_y) / `&word_11EB90C`(pos_z) / `&word_11EB838`(dirs) / `&word_11EB858`(distance) / `&word_11EB898`(body_regions)，计数均为 `dword_11EB8BC` |
| 分支判据 | `sub_474B90` @`0x474B90`：`v1 = this[54]; return v1 && *(v1+120) == 23;` ⇒ 为真走完整 `CS-0x770D`，否则走本命令。**判据不上线** |

**由此可补全 §3 帧格式表里未定来源的三项**：

- `arg_0`（`frame_count`，序号 1）= `*(dword_11E3EA8 + 0x1C240)`，由 `sub_B02460` 在 `0xB024C9` 额外压入
  （本函数实收 **18** 个栈参：`arg_44` 存在这条证据即隐含这一点，与 `sub_B02460` 的
  「17 个转发参数 + 1 个前置值」完全配平）。
- `arg_4`（`weapon_itemid`，序号 2）= `dword_11EB814`（`mov ecx, dword_11EB814` @`0x517E49` → `push ecx` @`0x517E73`）。
- `arg_8`（`fire_id`，序号 3）= `dword_11EB810`（`mov eax, dword_11EB810` @`0x517E68` → `push eax` @`0x517E72`）。
- `arg_44`（`AI_ent_id`，序号 18）= `movzx edx, word ptr dword_11EB8C0` @`0x517E35`（因此是 u16，与 §3 一致）。

**新结论**：本命令 = **命中上报的短格式**（与 `CS-0x770D` 同源，由 `sub_517D50` 按客户端状态二选一发出），
`send_weapon_fire_prepare__destruct_r` 只是该函数 trace 块里引用到的邻近名字，**不能作为语义依据**。
⇒ 本文件夹命令名与 `INDEX-命令总表.md` 第 216 行（`weapon_fire_prepare__destruct_r`）**需订正为 `weapon_hit_to` 短格式**；
改名属「命令发现」范畴，按 SOP §3.1 须由 `tools/ida_extract_commands.py` 重跑并同步 INDEX，
**本笔记不手改 INDEX**（避免破坏 `tools/verify_index.py` 一致性）。

**线格式本身不变**：§3 帧格式表的 19 项字段（类型/偏移/长度/证据）**全部仍然成立**，仅语义标签从
「自爆准备」改为「命中上报（短）：帧 + 武器 + 火线 id + 命中实体/点/方向/距离/部位 + 施放实体」。
另外注意：`charge_lv` / `instate_from_ent_id` / `create_frame_count` / `is_down_range` /
`is_wrestle_first_high_lockon` / `body_distance[]` / `phash` **在这条短格式里根本不存在**
（完整格式 `CS-0x770D` 才有），两套不可混用偏移解析。

---

## 追加：`sub_517D50` 的**全部**上游（三条路）—— 本命令何时会被发出（2026-09-30）

前面的追加只钉死了「本命令的唯一生产者在 `sub_517D50` 的短格式分支」。本节把 `sub_517D50` 的**调用者**
也查全（`xrefs(0x517D50)`），短格式因此有了完备的触发条件：

| # | 上游 | 场景 | 备注 |
|---|---|---|---|
| 1 | `sub_4E0D50 @ 0x4E0FDF` | **本机侧的范围/爆风解算**（`EXP_RANGE` 的消费点，见《战斗模型推导报告》§6.1.4①） | `sub_4E0D50` 只被虚表数据 `0xD71E30` 引用 ⇒ 是某个控制器的虚函数 |
| 2 | `sub_AFDCD0 @ 0xAFDD9E` | **`SC-0xEAEA weapon_fire_prepare__destruct` 的消费端**（服务端委派：爆点在该实体上） | 收件集 = 该实体的**属主单播** |
| 3 | `sub_518940 @ 0x518AAA` | **`SC-0x747B weapon_fire__chain_mine` → `sub_AFD7C0`**（连锁机雷：爆点在 `to_ent` 上） | 收件集 = **全房广播**；但该路**只发完整格式** |

⇒ 结论：**只有第 1、2 两条路可能走到短格式 `CS-0xA8FE`**；第 3 条路（连锁机雷）在
`sub_518940` 里直接调 `sub_B028D0`（完整 `CS-0x770D`），没有 `sub_474B90` 那个分支判据。
本结论不改变本命令的线格式（§3 的 19 项逐项仍成立），只把「服务端何时该期待短格式」变成了可判定的事。

