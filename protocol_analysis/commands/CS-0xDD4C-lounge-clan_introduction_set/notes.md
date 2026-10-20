# 分析笔记 —— CS-0xDD4C-lounge-clan_introduction_set

> 状态：`DONE`（2026-09-20，批次-22）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push <容量>; call <reg>`（@ `0x00BA1246`）。
- 字段名取自**提交（`sub_B02FF0`）之后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)` @ `0x00BA1399`。
- 容量等式：`2 + 547(intro_info) + 1(clan_kind) = 550 ≤ 容量 0x22A = 554（富余 4）`。
- 类型判定：一律取**写线指令宽度**（内联 `mov [reg],src` 看操作数宽度；`sub_B02D80/B02DA0/B061C0/B06190/B061E0/B02B40`），**不采用伪代码类型**；顶层 1 字节字段按写线操作数宽度记 `u8`。
- 配对：S→C `SC-0xA5FE-lounge-clan_introduction_set_r`。

## 未决 / 存疑 / 备注

- `intro_info` 线长由**写入器函数体逐字段累加**确证（`sub_B41EC0` @`0xB41EC0`..`0xB41F54`）：`u8(active_time_bits)` + `u8(play_style)` + `u8[28]×4(feature_word=112)` + `u8[433](notice_body)` = **547**；配套打印器 `sub_B4F080`（@`0xB4F080`）成员名与偏移逐一对位（`active_time_bits=`@+0、`play_style=`@+1、`feature_word={`@+2/+0x1E/+0x3A/+0x56、`notice_body=`@+0x72），与写入器偏移完全一致。
- `intro_info` 的内部成员语义名（active_time_bits/play_style/feature_word/notice_body）取自打印器 `sub_B4F080`；其中 `feature_word` 为 4×28 的定长字节块（打印器按 4 段打印、写入器按 4×`cmp esi,1Ch` 循环写出）。
- **槽预算（2026-09-25 补，服务端落地时钉的判据）**：`feature_word` 每槽 28B，但**内容上限 27**
  —— 客户端自己的写入器是 `sub_CC65C6(dst, 28, src, 27)` @`0x92D766`（第 28 字节留给 NUL），
  UI 侧 4 个文本框各 28B 槽、按 27 字符截断；`notice_body` 的 433B 同理。
  依据（为什么不靠"约定俗成"）：客户端的读串原语 `sub_B02BA0` 是"**读到 NUL 为止**"，
  一个填满槽宽、没有 NUL 的槽会把它送进**下一个字段**（甚至越过 547B 块尾）。
  而我们的 `codec.TextSlot` 写侧截断、读侧吃满，**往返自洽**、编解码层报不出这个错
  ⇒ 「每槽 ≤27 字符 / 公告 ≤433B」只能由**服务端写侧**把住（超了回 `-10002`）。

## 与其他命令的关联

- SC-0xA5FE-lounge-clan_introduction_set_r
