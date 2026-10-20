# 汇编证据 —— CS-0xC3BD-battle-weapon_fire__snipe_beam

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0xB39090`（`0xB39090`..`0xB39416`）
- 命令名字符串：`)<-_proto_battle_client::send_weapon_fire__snipe_beam(` @ `0xEE0EFC`
- opcode 写入：`0xB3910C`
- 声明容量：`0x22`（分配器容量 `push` @ `0xB390D6`）
- 提交（`sub_B02FF0`）：`0xB3922F`
- 发送去向：`vt[0x58]` @ `0xB393A4`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  0xB390D6  push    0x22            ; 声明容量（不是线长）
  0xB3910C  mov     word ptr [buf], C3BDh   ; 字段 0 `opcode` => 2
  00b3911c  mov     [ecx], esi                         ; 字段 1 `frame_count` => u32 (arg_0)
  00b39136  mov     [edx], ax                          ; 字段 2 `target_x` => u16 (arg_4)
  00b3913f  call    sub_B02DA0                         ; 字段 3 `target_y` => u16 (arg_8)
  00b39159  call    sub_B02DA0                         ; 字段 4 `target_z` => u16 (arg_C)
  00b39173  call    sub_B02DA0                         ; 字段 5 `rcnt_bullet_mgz` => u16 (arg_10)
  00b3918d  call    sub_B02DA0                         ; 字段 6 `rcnt_bullet_all` => u16 (arg_14)
  00b391a7  call    sub_B061C0                         ; 字段 7 `begin1_end0` => u8 (arg_18)
  00b391c1  call    sub_B02DA0                         ; 字段 8 `AI_ent_id` => u16 (arg_1C)
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  push offset a<Name>; "frame_count="
  push offset a<Name>; "target_x="
  push offset a<Name>; "target_y="
  push offset a<Name>; "target_z="
  push offset a<Name>; "rcnt_bullet_mgz="
  push offset a<Name>; "rcnt_bullet_all="
  push offset a<Name>; "begin1_end0="
  push offset a<Name>; "AI_ent_id="
```

## 4. 发送去向切片

```asm
  0xB393A4  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB3910C` | u16 / 2 |
| `frame_count` | `0xB3911C` | u32 / 4 |
| `target_x` | `0xB39136` | u16 / 2 |
| `target_y` | `0xB3913F` | u16 / 2 |
| `target_z` | `0xB39159` | u16 / 2 |
| `rcnt_bullet_mgz` | `0xB39173` | u16 / 2 |
| `rcnt_bullet_all` | `0xB3918D` | u16 / 2 |
| `begin1_end0` | `0xB391A7` | u8 / 1 |
| `AI_ent_id` | `0xB391C1` | u16 / 2 |
