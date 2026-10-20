# 汇编证据 —— CS-0xC90D-battle-weapon_fire__air_bomb

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0xB38AC0`（`0xB38AC0`..`0xB38E48`）
- 命令名字符串：`)<-_proto_battle_client::send_weapon_fire__air_bomb(` @ `0xEE0E7C`
- opcode 写入：`0xB38B3C`
- 声明容量：`0x22`（分配器容量 `push` @ `0xB38B06`）
- 提交（`sub_B02FF0`）：`0xB38C5F`
- 发送去向：`vt[0x58]` @ `0xB38DD6`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  0xB38B06  push    0x22            ; 声明容量（不是线长）
  0xB38B3C  mov     word ptr [buf], C90Dh   ; 字段 0 `opcode` => 2
  00b38b4c  mov     [ecx], esi                         ; 字段 1 `frame_count` => u32 (arg_0)
  00b38b66  mov     [edx], ax                          ; 字段 2 `target_x` => u16 (arg_4)
  00b38b6f  call    sub_B02DA0                         ; 字段 3 `target_y` => u16 (arg_8)
  00b38b89  call    sub_B02DA0                         ; 字段 4 `target_z` => u16 (arg_C)
  00b38ba3  call    sub_B061C0                         ; 字段 5 `shot0_drop1_impact2` => u8 (arg_10)
  00b38bbd  call    sub_B061C0                         ; 字段 6 `fx_opt` => u8 (arg_14)
  00b38bd7  call    sub_B02D80                         ; 字段 7 `airbomb_id` => u32 (arg_18)
  00b38bf1  call    sub_B02DA0                         ; 字段 8 `AI_ent_id` => u16 (arg_1C)
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  push offset a<Name>; "frame_count="
  push offset a<Name>; "target_x="
  push offset a<Name>; "target_y="
  push offset a<Name>; "target_z="
  push offset a<Name>; "shot0_drop1_impact2="
  push offset a<Name>; "fx_opt="
  push offset a<Name>; "airbomb_id="
  push offset a<Name>; "AI_ent_id="
```

## 4. 发送去向切片

```asm
  0xB38DD6  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB38B3C` | u16 / 2 |
| `frame_count` | `0xB38B4C` | u32 / 4 |
| `target_x` | `0xB38B66` | u16 / 2 |
| `target_y` | `0xB38B6F` | u16 / 2 |
| `target_z` | `0xB38B89` | u16 / 2 |
| `shot0_drop1_impact2` | `0xB38BA3` | u8 / 1 |
| `fx_opt` | `0xB38BBD` | u8 / 1 |
| `airbomb_id` | `0xB38BD7` | u32 / 4 |
| `AI_ent_id` | `0xB38BF1` | u16 / 2 |
