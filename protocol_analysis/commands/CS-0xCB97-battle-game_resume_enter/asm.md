# 汇编证据 —— CS-0xCB97-battle-game_resume_enter

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0xB33810`（`0xB33810`..`0xB33A59`）
- 命令名字符串：`)<-_proto_battle_client::send_game_resume_enter(` @ `0xEE08E8`
- opcode 写入：`0xB3388C`
- 声明容量：`0x4E`（分配器容量 `push` @ `0xB33856`）
- 提交（`sub_B02FF0`）：`0xB3392D`
- 发送去向：`vt[0x58]` @ `0xB339EA`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  0xB33856  push    0x4E            ; 声明容量（不是线长）
  0xB3388C  mov     word ptr [buf], CB97h   ; 字段 0 `opcode` => 2
  00b3389c  mov     [ecx], esi                         ; 字段 1 `is_initial` => u32 (arg_0)
  00b338b7  mov     [edx], al                          ; 字段 2 `script_thread` => u8 (arg_4)
  00b338bf  call    sub_B02B40                         ; 字段 3 `src` => bytes (arg_8)
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  push offset a<Name>; "is_initial="
  push offset a<Name>; "script_thread="
  push offset a<Name>; "src="
```

## 4. 发送去向切片

```asm
  0xB339EA  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB3388C` | u16 / 2 |
| `is_initial` | `0xB3389C` | u32 / 4 |
| `script_thread` | `0xB338B7` | u8 / 1 |
| `src` | `0xB338BF` | bytes / 可变 |
