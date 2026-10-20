# 汇编证据 —— CS-0xDAE0-battle-commander_list_get

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0xB3DCB0`（`0xB3DCB0`..`0xB3DE9A`）
- 命令名字符串：`)<-_proto_battle_client::send_commander_list_get(` @ `0xEE13AC`
- opcode 写入：`0xB3DD24`
- 声明容量：`0xA`（分配器容量 `push` @ `0xB3DCF6`）
- 提交（`sub_B02FF0`）：`0xB3DDA1`
- 发送去向：`vt[0x58]` @ `0xB3DE28`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  0xB3DCF6  push    0xA            ; 声明容量（不是线长）
  0xB3DD24  mov     word ptr [buf], DAE0h   ; 字段 0 `opcode` => 2
  00b3dd39  mov     [eax], dl                          ; 字段 1 `team` => u8 (arg_0)
  00b3dd45  mov     [edi], al                          ; 字段 2 `troops` => u8 (arg_4)
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  push offset a<Name>; "team="
  push offset a<Name>; "troops="
```

## 4. 发送去向切片

```asm
  0xB3DE28  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB3DD24` | u16 / 2 |
| `team` | `0xB3DD39` | u8 / 1 |
| `troops` | `0xB3DD45` | u8 / 1 |
