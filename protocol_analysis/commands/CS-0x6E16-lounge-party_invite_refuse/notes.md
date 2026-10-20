# 分析笔记 —— CS-0x6E16-lounge-party_invite_refuse

> 状态：`DONE`（2026-09-20，批次-19）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0x12; call <reg>`（容量 `push` @ `0xb91f26`）。
- 字段名取自**提交后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)`。
- 容量等式：`2(opcode) + 4×4 = 18 == 容量 0x12 = 18`（精确相等）
- 类型判定：一律取**写线指令宽度**（内联 `mov [reg],src` 看目标/源操作数宽度；`sub_B02D80/B02DA0/B061C0/B06190/B061E0/B02B40`），
  **不采用伪代码类型**。

## 与其他命令的关联

- 与 S→C `SC-0x300A-lounge-party_invite_r` 构成请求/应答对（对方收邀请 → 本方拒绝对）。
- 与 `CS-0x9471-lounge-party_invite` 反向（邀请/拒绝邀请）。

## 服务端实现（本服，2026-09-29 落地）

实现：`serverv/internal/lounge/party.go` 的 `onPartyInviteRefuse`；
验收：`serverv/internal/lounge/party_invite_test.go` 的 `TestPartyInviteRefuseDB`。

- **本命令没有配对应答**（单向通知）⇒ 效果是"让邀请者知道"：转发
  `SC-0x300A party_invite_r`（`result=0`、`pilot_id`=**拒绝者**、`reason`=原样透传）。
  读侧证据（`sub_653530`）：`result >= 0 && reason != 0` 才弹"对方拒绝了"的框，
  框里的名字取自 `pilot_id` ⇒ 这一格必须是拒绝者自己的号。
- **防改包**：请求里的 `pilot_id` 只能是**我自己**（写侧 `sub_B91EE0` 送的就是拒绝者自己的号），
  不是我的号则只记日志、不转发；`pilot_id = 0` 按"就是我"处理。
- **收件人 = 队长**（`game.party_member` 里 `is_leader<>0` 那一行）：报文只有 `party_id`，
  **没有"邀请人是谁"这一格**，邀请又不落库 ⇒ 精确回给邀请者做不到。取与同族
  `onBtlroomInviteRefuse`（拒绝回给房主）相同的口径。**残留**：非队长发起的邀请，
  拒绝框会落到队长屏幕上（记在 `party.go` 文件尾「留账」0.(c)）。
- `channel_id` 只当参考不当键（与 `CS-0x16AE` 同款：队的归属以 `(world_id, party_id)` 库行为准）。

## 未决 / 存疑

- `reason` 取值域 {1,19}（1=手动婉拒 `sub_6557F0`；19=自动婉拒/取込中 `sub_AF8680`）。⇒ 本服**原样透传**，
  不映射、不钳位（`reason = 0` 时客户端不弹框，如实照做）。
- 容量 0x12 与 Σ 线长精确相等，无富余。
