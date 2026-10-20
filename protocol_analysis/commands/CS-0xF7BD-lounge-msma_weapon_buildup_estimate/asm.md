# 汇编证据 —— CS-0xF7BD-lounge-msma_weapon_buildup_estimate

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0x00B97100`（`0x00B97100`..`0x00B973C8`），函数 `sub_B97100`
- 命令名字符串：`)<-_proto_lounge_client::send_msma_weapon_buildup_estimate( ` @ `0x00EEB9E4`
- opcode 写入：`0x00B9717C`
- 声明容量：`0x1A`（分配器容量 `push` @ `0x00B97146`）
- 提交（`sub_B02FF0`）：`0x00B97256`
- 发送去向：`vt[0x58]` @ `0x00B97356`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00B97143  mov     edx, [eax+78h]
  00B97146  push    1Ah                      ; <<< 容量 0x1A = 26
  00B97148  call    edx
  00B97154  call    sub_ABB2F0               ; <<< 初始化 {cur,end}（游标自 buf+2 起）
  00B9717C  mov     word ptr [ebp+0], 0F7BDh ; <<< opcode（u16）
  00B9718C  mov     [eax], esi               ; <<< u64 低 32 位（arg_0）
  00B97192  mov     [eax+4], esi             ; <<< u64 高 32 位（arg_4）
  00B971A4  mov     [edx], ecx               ; <<< u32 (arg_8)
  00B971B4  call    sub_B02D80               ; <<< u32 (arg_C)
  00B971CE  call    sub_B02DA0               ; <<< u16 (arg_10)
  00B971E8  call    sub_B02DA0               ; <<< u16 (arg_14)
  00B97256  call    sub_B02FF0               ; <<< 提交（C→S 闭合点）
```

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00B9726A  push    offset aUniqidMs          ; "uniqid_ms="  → sub_B08500(u64 打印器)
  00B97292  push    offset aItemId            ; "item_id="    → sub_B03580(u32)
  00B972BA  push    offset aTicketId          ; "ticket_id="  → sub_B03580(u32)
  00B972E2  push    offset aUsenum            ; "usenum="     → sub_B032A0(u16)
  00B97305  push    offset aParamTarget       ; "param_target=" → sub_B032A0(u16)
  00B9731F  mov     edx, ebx
  00B97321  sub     edx, ebp                 ; 负载长度 = 游标 − 缓冲首址
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | ``00B9717C`` | u16 / 2 |
| `uniqid_ms` | ``0xB9718C`,`0xB97192`` | u64 / 8 |
| `item_id` | ``0xB971A4`` | u32 / 4 |
| `ticket_id` | ``0xB971B4`` | u32 / 4 |
| `usenum` | ``0xB971CE`` | u16 / 2 |
| `param_target` | ``0xB971E8`` | u16 / 2 |
