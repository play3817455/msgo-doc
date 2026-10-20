# 分析笔记 —— CS-0xF86A-lounge-datafile_download

> 状态：`DONE`（2026-09-20，批次-23）。

## 结论要点与取证

- 分配器指纹：`mov ecx,[obj+0Ch]` → `mov eax,[ecx]` → `mov edx,[eax+78h]` → `push <容量>; call edx`；写线游标由 `sub_ABB2F0` 初始化 `{cur,end}`，**游标自 `buf+2` 起**（opcode 占 `buf+0..1`）。
- 字段名取证 = **提交（`sub_B02FF0`）之后**的 trace 打印块（`push offset a<Name>; … call sub_41D990`），**日志名序 == 线序**。打印器宽度：`sub_B03580`=u32 / `sub_B032A0`=u16 / `sub_B08500`=u64 / `sub_B0C1F0`=单字节（`movsx`，仅打印符号扩展，不改线宽）。
- 发送去向统一为 `vt[0x58](buf, 负载长度)`：`mov edx,[edi]; mov eax,[edx+58h]; sub <len>,<buf>; push <len>; push <buf>; mov ecx,<obj>; call eax`。
- 容量等式：`2 + 256 + 4 = 262 == 容量 0x106 = 262`（**上限场景精确相等**：串取满 255 字符 + NUL）
- 类型判定：一律取**写线指令宽度**（内联 `mov [reg],src` 看操作数宽度；`sub_B02D80/B02DA0/B061C0/B06190/B061E0/B02B40`），**不采用伪代码类型**；顶层 1 字节字段按写线操作数宽度记 `u8`；结构体/元素 1 字节成员按打印器 `movsx` 记 `i8`。
- 配对：S→C `SC-0x5290-lounge-datafile_download_r`。
- 与 S→C `SC-0x5290-lounge-datafile_download_r` 配对（该应答容量 `0x8000112` = `0x8000000 + 274`，含大数据段）。

## 未决 / 存疑 / 备注

- ★ 容量等式 **上限场景精确相等**：`2 + 256(串槽) + 4 = 262 == 0x106` ⇒ 同时确证「串槽预算 256」与线长上限。
- `sub_B02B40(src,cursor,maxlen)` 语义（承批次-20 固化）：`len = sub_C85E30(src,maxlen)`，`cmp len,maxlen; jnb 失败` ⇒ **消费 = len+1 ≤ maxlen**，`maxlen` 计入容量、与串实长无关。
- 串之后字段偏移为变长 ⇒ 偏移列记 `var`（不编造偏移）。
- 附加通知：`[obj+79A8h]` 回调（模块 id `0x8`）。

## 与其他命令的关联

- SC-0x5290-lounge-datafile_download_r

## 服务端实现（2026-09-30，§㊺ 杂项收尾族）

- 实现：`serverv/internal/lounge/misc.go` 的 `onDatafileDownload`；注册点
  `registerMiscHandlers`（← `internal/lounge/server.go` 的 `registerHandlers`）。
- 处置：**有 `_r`** 但本服回不出文件内容 ⇒ 拒答 `SC-0x5290`，`result = -10002`
  （`errcode.Wire(ErrCodeInvalidNumber)`）；**回显请求里的 `filepath`/`hashval`**
  （应答体自带这两格，客户端在途请求靠它们对号），`bin_count=0` + 空块。
- 理由：它要的是**原始文件字节**，而本服的 cfg 导入（`internal/cfg`）只把 `cfg.*` 表
  **行化**，没有任何"按路径取原始文件"的存储面（见 docs/01 §㊺③④）。
- 验收：`internal/lounge/misc_test.go` 的 `TestMiscDeniedHandlersReply/datafile_download`
  （恰好一帧、`result = -10002`、回显 `filepath`/`hashval`、`bin_count=0` 且 `bin` 空）、
  `TestMiscDatafileReplyWireShape`（空块线长 `4+2+4+4+2+4 = 20`；`bin_count=1` 而 `bin`
  为空 ⇒ 生成码**编码就失败**）、`TestMiscHandlersTolerateBadBody`。
- 配对：S→C `SC-0x5290-lounge-datafile_download_r`。
- 留账：`SC-0x5290` 的 `bin` **非空块**线上口径（是否分片/如何分片）无真机证据；
  将来要真的供文件，得先定"服务端从哪儿取原始文件"。
