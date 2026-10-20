# 分析笔记 —— CS-0xF24B-auth-authenticate

> 状态：`DONE`（2026-09-20，批次-22）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push <容量>; call <reg>`（@ `0x00B04EF3`）。
- 字段名取自**提交（`sub_B02FF0`）之后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)` @ `0x00B05121`。
- 容量等式：`2 + 513 + 513 + 128 + 128 = 1284 ≤ 容量 0x50A = 1290（富余 6）`。
- 类型判定：一律取**写线指令宽度**（内联 `mov [reg],src` 看操作数宽度；`sub_B02D80/B02DA0/B061C0/B06190/B061E0/B02B40`），**不采用伪代码类型**；顶层 1 字节字段按写线操作数宽度记 `u8`。
- 配对：S→C `SC-0xA5DA-auth-authenticate_r`。

## 未决 / 存疑 / 备注

- 字段名取自提交后打印块（`login_id=`/`login_pw=`/`disk_uuid=`/`mac_addr=`），**日志名序 == 线序**。
- 串槽预算口径：`sub_B02B40(src,cursor,maxlen)` 消费 = 串长 + 1 ≤ maxlen，容量按槽预算计。

## 与其他命令的关联

- SC-0xA5DA-auth-authenticate_r
