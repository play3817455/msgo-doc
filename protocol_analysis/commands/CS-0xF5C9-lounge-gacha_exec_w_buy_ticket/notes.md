# 分析笔记 —— CS-0xF5C9-lounge-gacha_exec_w_buy_ticket

> 状态：`DONE`（2026-09-20，批次-22）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push <容量>; call <reg>`（@ `0x00B9E286`）。
- 字段名取自**提交（`sub_B02FF0`）之后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)` @ `0x00B9E558`。
- 容量等式：`2 + 4 + 1 + 4 + 1 + 1 + 4 + 4 + 1 = 22 == 容量 0x22 = 22（精确相等）`。
- 类型判定：一律取**写线指令宽度**（内联 `mov [reg],src` 看操作数宽度；`sub_B02D80/B02DA0/B061C0/B06190/B061E0/B02B40`），**不采用伪代码类型**；顶层 1 字节字段按写线操作数宽度记 `u8`。
- 配对：S→C `SC-0xF66B-lounge-gacha_exec_w_buy_ticket_r`。

## 未决 / 存疑 / 备注

- 字段名取自提交后打印块（`shopitemid=`/`id_type=`/`num=`/`tab_type=`/`is_cp=`/`total_price=`/`gacha_id=`/`is_bundle=`），**日志名序 == 线序**（8 名 ↔ 8 字段）。
- `id_type` / `tab_type` 的**取值集**仍无字面量枚举表（继续标 `?`）；本轮只把**来源**定位到「商品/扭蛋券记录」的字节成员：`id_type = [rec+4]`、`tab_type = [rec+6]`（`0xF5C9` 的 `sub_43EB70` 调用点 @`0x86A057`/`0x86A131` 把 `[rec+4]`/`[rec+6]` 原样送装配器；`0xADB6` 的 `sub_659770` 调用点同理）⇒ 该域由**商品表数据**决定，客户端没有字面量集合可采集。

## 与其他命令的关联

- SC-0xF66B-lounge-gacha_exec_w_buy_ticket_r
