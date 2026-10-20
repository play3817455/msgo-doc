# 汇编证据 —— CS-0xF969-lounge-msma_deckslot_change

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0x00B93160`（`0x00B93160`..`0x00B933A6`），函数 `sub_B93160`
- 命令名字符串：`)<-_proto_lounge_client::send_msma_deckslot_change( ` @ `0x00EEB350`
- opcode 写入：`0x00B931DC`
- 声明容量：`0x12`（分配器容量 `push` @ `0x00B931A6`）
- 提交（`sub_B02FF0`）：`0x00B93284`
- 发送去向：`vt[0x58]` @ `0x00B93334`

## 2. 组包块切片

```asm
  00B931A3  mov     edx, [eax+78h]
  00B931A6  push    12h                      ; <<< 容量 0x12 = 18
  00B931A8  call    edx
  00B931B4  call    sub_ABB2F0               ; <<< 初始化 {cur,end}
  00B931DC  mov     word ptr [ebp+0], 0F969h ; <<< opcode
  00B931EC  mov     [eax], esi               ; <<< u64 低 32 位（arg_0）
  00B931F2  mov     [eax+4], esi             ; <<< u64 高 32 位（arg_4）
  00B93205  mov     [edx], cx                ; <<< u16 (arg_8)
  00B93216  call    sub_B02DA0               ; <<< u16 (arg_C)
  00B93284  call    sub_B02FF0               ; <<< 提交
```

## 3. 提交后的 trace 打印块

```asm
  00B93298  push    offset aUniqid             ; "uniqid="  → sub_B08500(u64)
  00B932C0  push    offset aDecktype           ; "decktype=" → sub_B032A0(u16)
  00B932E3  push    offset aDeckslot           ; "deckslot=" → sub_B032A0(u16)
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | ``00B931DC`` | u16 / 2 |
| `uniqid` | ``0xB931EC`,`0xB931F2`` | u64 / 8 |
| `decktype` | ``0xB93205`` | u16 / 2 |
| `deckslot` | ``0xB93216`` | u16 / 2 |
