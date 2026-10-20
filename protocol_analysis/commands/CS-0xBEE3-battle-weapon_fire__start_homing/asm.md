# 汇编证据 —— CS-0xBEE3-battle-weapon_fire__start_homing

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0xB38370`（`0xB38370`..`0xB38670`）
- 命令名字符串：`)<-_proto_battle_client::send_weapon_fire__start_homing(` @ `0xEE0E04`
- opcode 写入：`0xB383EC`
- 声明容量：`0x1A`（分配器容量 `push` @ `0xB383B6`）
- 提交（`sub_B02FF0`）：`0xB384DB`
- 发送去向：`vt[0x58]` @ `0xB385FE`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  0xB383B6  push    0x1A            ; 声明容量（不是线长）
  0xB383EC  mov     word ptr [buf], BEE3h   ; 字段 0 `opcode` => 2
  00b383fc  mov     [eax], esi                         ; 字段 1 `frame_count` => u32 (arg_0)
  00b38417  mov     [eax], ecx                         ; 字段 2 `grenade_id` => u32 (arg_4)
  00b3841f  call    sub_B02DA0                         ; 字段 3 `pos_x` => u16 (arg_8)
  00b38439  call    sub_B02DA0                         ; 字段 4 `pos_y` => u16 (arg_C)
  00b38453  call    sub_B02DA0                         ; 字段 5 `pos_z` => u16 (arg_10)
  00b3846d  call    sub_B02DA0                         ; 字段 6 `target_ent_id` => u16 (arg_14)
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  push offset a<Name>; "frame_count="
  push offset a<Name>; "grenade_id="
  push offset a<Name>; "pos_x="
  push offset a<Name>; "pos_y="
  push offset a<Name>; "pos_z="
  push offset a<Name>; "target_ent_id="
```

## 4. 发送去向切片

```asm
  0xB385FE  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB383EC` | u16 / 2 |
| `frame_count` | `0xB383FC` | u32 / 4 |
| `grenade_id` | `0xB38417` | u32 / 4 |
| `pos_x` | `0xB3841F` | u16 / 2 |
| `pos_y` | `0xB38439` | u16 / 2 |
| `pos_z` | `0xB38453` | u16 / 2 |
| `target_ent_id` | `0xB3846D` | u16 / 2 |
