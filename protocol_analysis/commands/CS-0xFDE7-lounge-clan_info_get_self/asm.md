# 汇编证据 —— CS-0xFDE7-lounge-clan_info_get_self

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0x00B9F150`（`0x00B9F150`..`0x00B9F2FE`），函数 `sub_B9F150`
- 命令名字符串：`)<-_proto_lounge_client::send_clan_info_get_self( ` @ `0x00EEC6C4`
- opcode 写入：`0x00B9F1C4`
- 声明容量：`0x6`（分配器容量 `push` @ `0x00B9F196`）
- 提交（`sub_B02FF0`）：`0x00B9F22F`
- 发送去向：`vt[0x58]` @ `0x00B9F28C`

## 2. 组包块切片

```asm
  00B9F193  mov     edx, [eax+78h]
  00B9F196  push    6                        ; <<< 容量 6
  00B9F198  call    edx
  00B9F1A4  call    sub_ABB2F0               ; <<< 初始化 {cur,end}
  00B9F1C4  mov     word ptr [edi], 0FDE7h   ; <<< opcode
  00B9F1CF  mov     cl, [esp+40h+arg_0]
  00B9F1D3  mov     [eax], cl                ; <<< u8 (arg_0)
  00B9F22F  call    sub_B02FF0               ; <<< 提交
```

## 3. 提交后的 trace 打印块

```asm
  00B9F239  push    offset aClanKind           ; "clan_kind=" → sub_B0C1F0(1B, movsx)
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | ``00B9F1C4`` | u16 / 2 |
| `clan_kind` | ``0xB9F1D3`` | u8 / 1 |
