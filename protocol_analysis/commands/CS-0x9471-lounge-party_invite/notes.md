# 分析笔记 —— CS-0x9471-lounge-party_invite

> 状态：`DONE`（2026-09-20，批次-19）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0x6; call <reg>`（容量 `push` @ `0xb91d76`）。
- 字段名取自**提交后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)`。
- 容量等式：`2 + 4 = 6 == 容量 0x6 = 6`（精确相等）
- 类型判定：一律取**写线指令宽度**（内联 `mov [reg],src` 看目标/源操作数宽度；`sub_B02D80/B02DA0/B061C0/B06190/B061E0/B02B40`），
  **不采用伪代码类型**。

## 与其他命令的关联

- 与 `CS-0x6E16-lounge-party_invite_refuse`（本批，拒绝邀请）互为逆操作。
- 与 S→C `SC-0x300A-lounge-party_invite_r` / `SC-0x5C61-lounge-party_invite_to`（已 DONE）关联。

## 服务端实现（本服，2026-09-29 落地）

实现：`serverv/internal/lounge/party.go` 的 `onPartyInvite` + `inviteOutcome`；
验收：`serverv/internal/lounge/party_invite_test.go` 的 `TestPartyInviteDB` / `TestPartyInviteNoStore`。

- **邀请者的队从哪来**：请求体只有被邀请人（`pilot_id`）⇒ 按会话反查
  `game.party_member`（`store.PartyOfPilot`），与 `0x5F80`/`0x9226` 同款（报文里没有 party_id）。
- **`SC-0x5C61 party_invite_to` 的收件人 = 被邀请者自己**（原先的"两种读法"歧义在此收口）：
  同族 `SC-0x816F-lounge-btlroom_invite_to` 也是"`pilot_id`/`pilot_name` = 收件人自己的号与名"
  （客户端按它认领邀请框）⇒ `0x5C61` 三格照此口径（`party_id` + `channel_id` 是**队**的，
  `pilot_id`/`pilot_name` 是**被邀请人**的）。
- **`channel_id` 取 `game.party.channel_id`**（队建在哪个频道），不是被邀请者自己的频道
  —— 与 `SC-0x5F18`/`SC-0x305D` 的"channel_id 与 party_id 并列"同口径。
- **结果码**（`SC-0x300A.result`，都在「パーティマッチング関連」段的**可发**条目里）：
  `0` 已送达 / `-11803` 我不在任何队里 / `-11804` 找不到邀请对象（`pilot_id` 为 0、
  是我自己、不在线、推送失败）/ `-10053` store 或会话缺字段、读写库失败。
- **不拦"被邀请者已在别的队里"**：该段里语义最近的 `-11800 既にパーティ参加している`
  是被注释掉的"只显示码"（`IsListed=false`、`Text` 空）⇒ 不借用，照发邀请只记日志。
- `SC-0x300A.reason` 恒 0（细分码枚举未取证，见下"未决"）。

## 未决 / 存疑

- 无未决项（线格式侧）。

## 服务端侧残留（不阻塞落地）

- `SC-0x300A.reason` 的取值枚举未取证 ⇒ 本服恒发 0，不猜值。
- 邀请**不落库**（库无邀请表）⇒ 没有"过期/撤回/去重"概念；被邀请者已在队中时也无法先拦。
  三笔残留（含拒邀只能回队长）记在 `party.go` 文件尾「留账」段 0.(a)(b)(c)。
