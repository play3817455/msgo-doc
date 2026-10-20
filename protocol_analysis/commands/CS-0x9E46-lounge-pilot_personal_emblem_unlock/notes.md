# 分析笔记 —— CS-0x9E46-lounge-pilot_personal_emblem_unlock

> 状态：`DONE`（2026-09-20，批次-20）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0x000A; call <reg>`（容量 `push` @ `0xB8BF16`）。
- 字段名取自**提交（`sub_B02FF0`）之后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)` @ `0xB8C044`。
- 附加通知：`[obj+79A8h]` 回调模块 id `0x033` @ `0xB8C05F`（发送成功后的统计/日志钩子）。
- 容量等式：`2 + 4 + 4 = 10 == 容量 0xA = 10`（精确相等）
- 类型判定：一律取**写线指令宽度**（内联 `mov [reg],src` 看目标/源操作数宽度；`sub_B02D80/B02DA0/B061C0/B06190/B061E0/B02B40`），
  **不采用伪代码类型**。**顶层 1 字节字段按写线操作数宽度记 `u8`**（打印器 `sub_B0C1F0` 的 `movsx` 只表示打印时符号扩展，不改线宽）。

## 与其他命令的关联

- 配对命令：S→C `SC-0xC779-lounge-pilot_personal_emblem_unlock_r`（已 DONE）

## 未决 / 存疑

- 无。

## 服务端实现（本服，2026-09-29 落地）

实现：`serverv/internal/lounge/pilot_unlock.go` 的 `onPilotPersonalEmblemUnlock`（落库
`store.UnlockPilotPersonalEmblem`）；
验收：`serverv/internal/lounge/pilot_unlock_test.go`（`TestPilotPersonalEmblemUnlockChargesOnceAndIsIdempotent` /
`TestPilotPersonalEmblemUnlockRejections` / `TestPilotPersonalEmblemUnlockZeroCostIsFree`）
+ `serverv/internal/store/pilot_unlock_db_test.go`。

- **落点 = `game.pilot_detail.hav_emblem`**（`BIGINT[]`，线上 `u64[8]`）。
- **`use_gp` 是客户端算好的金额（报价单），不是开关位**：本库没有徽章价目表（价目在客户端
  datafile 里）⇒ 与 `msma_color_unlock`（`0x2E33`）**完全同一口径**：照单扣，`use_gp = 0`
  则不碰钱包、也照常解锁。
- **已拥有 ⇒ 幂等、不二次收费**：应答里的 `use_gp` 回**真扣掉的数**（没扣就回 0）——
  回原请求值会让客户端按"扣过了"去改本地余额显示。
- **一个事务**：「锁行 → 判已拥有/超槽 → 扣 GP → 写 `hav_emblem`」；GP 不足整笔回滚。
- **`hav_emblem` 必须补零到恰好 8 项**才回发（`SC-0xC779` 的编码器 `!= 8` 即报错）；
  被拒时回**库里真值**（store 在读行时就带回）。
- 真扣了钱才推 `0x090C`（新余额）。
- **结果码**（`SC-0xC779.result`）：`0` / `-10002`（`emblem_id = 0`、越权）/ `-26002`（8 槽满）/
  `-26007`（GP 不足）/ `-10053`（无 `pilot_detail` 行或真库错误）。
