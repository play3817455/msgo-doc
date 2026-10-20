# 分析笔记 —— CS-0xCC9F-lounge-clan_mshipbid_request

> 状态：`DONE`（2026-09-20，批次-21）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0xA; call <reg>`（@ `0xB9FD56`）。
- 字段名取自**提交（`sub_B02FF0`）之后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)` @ `0xB9FE86`。
- 容量等式：`2+4+1 = 7 ≤ 容量 0xA = 10`（富余 3）。
- 类型判定：一律取**写线指令宽度**（内联 `mov [reg],src` 看操作数宽度；`sub_B02D80/B02DA0/B061C0/B06190/B061E0/B02B40`），**不采用伪代码类型**；顶层 1 字节字段按写线操作数宽度记 `u8`。

## 未决 / 存疑 / 备注

- 容量 `0xA` = 10 ≥ `2+4+1` = 7（富余 3）。

## 与其他命令的关联

- **申请链（S1.12 落地口径，2026-09-25）**：`clan_id` 就是**被申请的氏族**（写线 @`0xB9FD99`，
  入参 `arg_0`）—— 这条不是"读侧猜的"，配对响应 `SC-0xE69C` 回的 `mclan_id`/`mclan_name`
  （母舰战队 id/名）就是它的回显；两个包装 `sub_63BC00`(`clan_kind`=0) / `sub_696E00`(`clan_kind`=1)
  各自传一种族类型。落库行主 = `(world_id, mclan_id, mshipbid_card_pilot_id)`，
  行的生命期见 `CS-0x2A35` 的 notes（**行在 = 待处理**：申请建行、同意入族后删行、
  拒绝/撤回也删行）。一人一条（`-13020` 的文案「…or入隊申請中…」）；列表上限 20 出自
  客户端读取器的硬上限（`cmp …,0x14; ja` @`0xB80236`，超了整包丢）。
  服务端实现见 `serverv/internal/lounge/clan_mshipbid.go` / `serverv/internal/store/clan_mshipbid.go`。
