# 汇编证据 —— CS-0xD2C3-battle-weapon_fire__grenade

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0xB372D0`（`0xB372D0`..`0xB379E5`）
- 命令名字符串：`)<-_proto_battle_client::send_weapon_fire__grenade(` @ `0xEE0D54`
- opcode 写入：`0xB37351`
- 声明容量：`0x5A`（分配器容量 `push` @ `0xB3731B`）
- 提交（`sub_B02FF0`）：`0xB375C5`
- 发送去向：`vt[0x58]` @ `0xB37964`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  0xB3731B  push    0x5A            ; 声明容量（不是线长）
  0xB37351  mov     word ptr [buf], D2C3h   ; 字段 0 `opcode` => 2
  00b3735f  mov     [ecx], esi                         ; 字段 1 `frame_count` => u32 (arg_0)
  00b37378  mov     [edx], ax                          ; 字段 2 `launch_x` => u16 (arg_4)
  00b37380  call    sub_B02DA0                         ; 字段 3 `launch_y` => u16 (arg_8)
  00b37399  call    sub_B02DA0                         ; 字段 4 `launch_z` => u16 (arg_C)
  00b373b2  call    sub_B02DA0                         ; 字段 5 `target1_x` => u16 (arg_10)
  00b373cb  call    sub_B02DA0                         ; 字段 6 `target1_y` => u16 (arg_14)
  00b373e4  call    sub_B02DA0                         ; 字段 7 `target1_z` => u16 (arg_18)
  00b373fd  call    sub_B02DA0                         ; 字段 8 `target2_x` => u16 (arg_1C)
  00b37416  call    sub_B02DA0                         ; 字段 9 `target2_y` => u16 (arg_20)
  00b3742f  call    sub_B02DA0                         ; 字段 10 `target2_z` => u16 (arg_24)
  00b37448  call    sub_B02DA0                         ; 字段 11 `target_ent_id` => u16 (arg_28)
  00b37461  call    sub_B02DA0                         ; 字段 12 `msec` => u16 (arg_2C)
  00b3747a  call    sub_B061C0                         ; 字段 13 `shot0_impact1` => u8 (arg_30)
  00b37493  call    sub_B061C0                         ; 字段 14 `fx_opt` => u8 (arg_34)
  00b374ac  call    sub_B02D80                         ; 字段 15 `impact_grenade_id` => u32 (arg_38)
  00b374c5  call    sub_B02D80                         ; 字段 16 `parent_grenade_id` => u32 (arg_3C)
  00b374de  call    sub_B061C0                         ; 字段 17 `charge_lv` => u8 (arg_40)
  00b374f7  call    sub_B02D80                         ; 字段 18 `ent_id` => u32 (arg_44)
  00b37510  call    sub_B02DA0                         ; 字段 19 `AI_ent_id` => u16 (arg_48)
  00b37529  call    sub_B061C0                         ; 字段 20 `impact_wall` => u8 (arg_4C)
  00b37542  call    sub_B061C0                         ; 字段 21 `salvo_slot` => u8 (arg_50)
  00b3755b  call    sub_B061C0                         ; 字段 22 `action` => u8 (arg_54)
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  push offset a<Name>; "frame_count="
  push offset a<Name>; "launch_x="
  push offset a<Name>; "launch_y="
  push offset a<Name>; "launch_z="
  push offset a<Name>; "target1_x="
  push offset a<Name>; "target1_y="
  push offset a<Name>; "target1_z="
  push offset a<Name>; "target2_x="
  push offset a<Name>; "target2_y="
  push offset a<Name>; "target2_z="
  push offset a<Name>; "target_ent_id="
  push offset a<Name>; "msec="
  push offset a<Name>; "shot0_impact1="
  push offset a<Name>; "fx_opt="
  push offset a<Name>; "impact_grenade_id="
  push offset a<Name>; "parent_grenade_id="
  push offset a<Name>; "charge_lv="
  push offset a<Name>; "ent_id="
  push offset a<Name>; "AI_ent_id="
  push offset a<Name>; "impact_wall="
  push offset a<Name>; "salvo_slot="
  push offset a<Name>; "action="
```

## 4. 发送去向切片

```asm
  0xB37964  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB37351` | u16 / 2 |
| `frame_count` | `0xB3735F` | u32 / 4 |
| `launch_x` | `0xB37378` | u16 / 2 |
| `launch_y` | `0xB37380` | u16 / 2 |
| `launch_z` | `0xB37399` | u16 / 2 |
| `target1_x` | `0xB373B2` | u16 / 2 |
| `target1_y` | `0xB373CB` | u16 / 2 |
| `target1_z` | `0xB373E4` | u16 / 2 |
| `target2_x` | `0xB373FD` | u16 / 2 |
| `target2_y` | `0xB37416` | u16 / 2 |
| `target2_z` | `0xB3742F` | u16 / 2 |
| `target_ent_id` | `0xB37448` | u16 / 2 |
| `msec` | `0xB37461` | u16 / 2 |
| `shot0_impact1` | `0xB3747A` | u8 / 1 |
| `fx_opt` | `0xB37493` | u8 / 1 |
| `impact_grenade_id` | `0xB374AC` | u32 / 4 |
| `parent_grenade_id` | `0xB374C5` | u32 / 4 |
| `charge_lv` | `0xB374DE` | u8 / 1 |
| `ent_id` | `0xB374F7` | u32 / 4 |
| `AI_ent_id` | `0xB37510` | u16 / 2 |
| `impact_wall` | `0xB37529` | u8 / 1 |
| `salvo_slot` | `0xB37542` | u8 / 1 |
| `action` | `0xB3755B` | u8 / 1 |
