# 汇编证据 —— CS-0xFC4B-lounge-xwar_booking_info_get

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0x00B91230`（`0x00B91230`..`0x00B913DD`），函数 `sub_B91230`
- 命令名字符串：`)<-_proto_lounge_client::send_xwar_booking_info_get( ` @ `0x00EEB018`
- opcode 写入：`0x00B912A4`
- 声明容量：`0x6`（分配器容量 `push` @ `0x00B91276`）
- 提交（`sub_B02FF0`）：`0x00B91310`
- 发送去向：`vt[0x58]` @ `0x00B9136B`

## 2. 组包块切片

```asm
  00B91273  mov     edx, [eax+78h]
  00B91276  push    6                        ; <<< 容量 6
  00B91278  call    edx
  00B91284  call    sub_ABB2F0               ; <<< 初始化 {cur,end}
  00B912A4  mov     word ptr [ebp+0], 0FC4Bh ; <<< opcode
  00B912B4  mov     [eax], ecx               ; <<< u32 (arg_0)
  00B91310  call    sub_B02FF0               ; <<< 提交
```

## 3. 提交后的 trace 打印块

```asm
  00B9131A  push    offset aMatchingType       ; "matching_type=" → sub_B03580(u32)
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | ``00B912A4`` | u16 / 2 |
| `matching_type` | ``0xB912B4`` | u32 / 4 |
