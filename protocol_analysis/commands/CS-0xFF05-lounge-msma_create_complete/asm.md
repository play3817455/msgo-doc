# 汇编证据 —— CS-0xFF05-lounge-msma_create_complete

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0x00B95EC0`（`0x00B95EC0`..`0x00B960FA`），函数 `sub_B95EC0`
- 命令名字符串：`)<-_proto_lounge_client::send_msma_create_complete( ` @ `0x00EEB828`
- opcode 写入：`0x00B95F3C`
- 声明容量：`0xE`（分配器容量 `push` @ `0x00B95F06`）
- 提交（`sub_B02FF0`）：`0x00B95FDD`
- 发送去向：`vt[0x58]` @ `0x00B96088`

## 2. 组包块切片

```asm
  00B95F03  mov     edx, [eax+78h]
  00B95F06  push    0Eh                      ; <<< 容量 0xE = 14
  00B95F08  call    edx
  00B95F14  call    sub_ABB2F0               ; <<< 初始化 {cur,end}
  00B95F3C  mov     word ptr [ebp+0], 0FF05h ; <<< opcode
  00B95F4C  mov     [eax], esi               ; <<< u32 (arg_0)
  00B95F67  mov     [eax], ecx               ; <<< u32 (arg_4)
  00B95F6F  call    sub_B02DA0               ; <<< u16 (arg_8)
  00B95FDD  call    sub_B02FF0               ; <<< 提交
```

## 3. 提交后的 trace 打印块

```asm
  00B95FEC  push    offset aMsPlanId           ; "ms_plan_id=" → sub_B03580(u32)
  00B96014  push    offset aTicketId           ; "ticket_id="  → sub_B03580(u32)
  00B96037  push    offset aUsenum             ; "usenum="     → sub_B032A0(u16)
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | ``00B95F3C`` | u16 / 2 |
| `ms_plan_id` | ``0xB95F4C`` | u32 / 4 |
| `ticket_id` | ``0xB95F67`` | u32 / 4 |
| `usenum` | ``0xB95F6F`` | u16 / 2 |
