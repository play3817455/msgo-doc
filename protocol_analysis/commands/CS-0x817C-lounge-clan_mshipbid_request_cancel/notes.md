# 分析笔记 —— CS-0x817C-lounge-clan_mshipbid_request_cancel

> 状态：`DONE`（2026-09-20，批次-19）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0x6; call <reg>`（容量 `push` @ `0xb9ff46`）。
- 字段名取自**提交后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)`。
- 容量等式：`2 + 1 = 3 ≤ 容量 0x6 = 6`（富余 3）
- 类型判定：一律取**写线指令宽度**（内联 `mov [reg],src` 看目标/源操作数宽度；`sub_B02D80/B02DA0/B061C0/B06190/B061E0/B02B40`），
  **不采用伪代码类型**。

## 与其他命令的关联

- 与 S→C `SC-0xB92F-lounge-clan_mshipbid_request_cancel_r` 构成请求/应答对。
- 与 `CS-0x2A35-lounge-clan_mshipbid_response`、`CS-0xE69C-lounge-clan_mshipbid_request_r`（均已 DONE）同族。
- **报文形状本身就是证据（S1.12 落地口径，2026-09-25）**：撤回**不带 `clan_id`**（只带 `clan_kind`）
  ⇒ 撤回的是"**我那条**"申请，目标氏族由会话解析（与 `clan_mshipbid_request` 带 `clan_id`
  恰好互补）。配合 `-13020` 的文案「部隊所属中or**入隊申請中**は入隊申請できない」可定：
  **一人一条**在队申请；行在 = 待处理（同意入族后删行、拒绝/撤回也删行），
  详见 `CS-0x2A35` 的 notes。服务端实现见 `serverv/internal/lounge/clan_mshipbid.go`。

## 未决 / 存疑

- 线上宽度 **1 字节**；`clan_kind` 取值域 {0,1}（0=部隊 1=大会チーム）；容量富余 3。
