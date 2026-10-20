# 汇编证据 —— CS-0x9EE0-lounge-clan_search

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_BA1600 @ `0xBA1600`（`0xBA1600`..`0xBA1863`）
- 命令名字符串：`)<-_proto_lounge_client::send_clan_search(` @ `0xEECA78`
- opcode 写入：`0xBA1683`
- 声明容量：`0x002A`（分配器容量 `push` @ `0xBA1646`）
- 发送去向：`vt[0x58]` @ `0xBA17EF`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00ba1646  push    2Ah ; '*'
  00ba1683  mov     word ptr [ebp+0], 9EE0h   ; 字段 0 `opcode` => 2
  00ba168d  call    sub_B02B40   ; 字段 1 `clan_name` => var(≤31)
  00ba16ba  mov     [ecx], dl   ; 字段 2 `clan_kind` => 1
  00ba16c2  call    sub_B061C0   ; 字段 3 `search_kind` => 1
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00EDCA98  push offset a<name>; "clan_name=""
  00EE3398  push offset a<name>; "clan_kind="
  00EE3C94  push offset a<name>; "search_kind="
```

## 4. 发送去向切片

```asm
  00ba17ef  mov     edx, [eax+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xBA1683` | u16 / 2 |
| `clan_name` | `0xBA168D` | str / var(≤31) |
| `clan_kind` | `0xBA16BA` | u8 / 1 |
| `search_kind` | `0xBA16C2` | u8 / 1 |
