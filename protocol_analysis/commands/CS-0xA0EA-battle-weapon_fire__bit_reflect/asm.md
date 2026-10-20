# 汇编证据 —— CS-0xA0EA-battle-weapon_fire__bit_reflect

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B3B350 @ `0xB3B350`（`0xB3B350`..`0xB3B79C`）
- 命令名字符串：`)<-_proto_battle_client::send_weapon_fire__bit_reflect(` @ `0xEE10BC`
- opcode 写入：`0xB3B3CC`
- 声明容量：`0x002E`（分配器容量 `push` @ `0xB3B396`）
- 发送去向：`vt[0x58]` @ `0xB3B72A`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00b3b396  push    2Eh ; '.'
  00b3b3cc  mov     word ptr [ebp+0], 0A0EAh   ; 字段 0 `opcode` => 2
  00b3b3dc  mov     [eax], esi   ; 字段 1 `frame_count` => 4
  00b3b3f7  mov     [eax], ecx   ; 字段 2 `itemid` => 4
  00b3b3ff  call    sub_B02DA0   ; 字段 3 `launch_x` => 2
  00b3b419  call    sub_B02DA0   ; 字段 4 `launch_y` => 2
  00b3b433  call    sub_B02DA0   ; 字段 5 `launch_z` => 2
  00b3b44d  call    sub_B02DA0   ; 字段 6 `target_x` => 2
  00b3b467  call    sub_B02DA0   ; 字段 7 `target_y` => 2
  00b3b481  call    sub_B02DA0   ; 字段 8 `target_z` => 2
  00b3b49b  call    sub_B061C0   ; 字段 9 `charge_lv` => 1
  00b3b4b5  call    sub_B02DA0   ; 字段 10 `AI_ent_id` => 2
  00b3b4cf  call    sub_B02DA0   ; 字段 11 `reflect_ent_id` => 2
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00EDC830  push offset a<name>; "frame_count="
  00EDBD4C  push offset a<name>; "itemid="
  00EDC464  push offset a<name>; "launch_x="
  00EDC458  push offset a<name>; "launch_y="
  00EDC44C  push offset a<name>; "launch_z="
  00EDB960  push offset a<name>; "target_x="
  00EDB954  push offset a<name>; "target_y="
  00EDB948  push offset a<name>; "target_z="
  00EDC780  push offset a<name>; "charge_lv="
  00EDC870  push offset a<name>; "AI_ent_id="
  00EDC32C  push offset a<name>; "reflect_ent_id="
```

## 4. 发送去向切片

```asm
  00b3b72a  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB3B3CC` | u16 / 2 |
| `frame_count` | `0xB3B3DC` | u32 / 4 |
| `itemid` | `0xB3B3F7` | u32 / 4 |
| `launch_x` | `0xB3B3FF` | u16 / 2 |
| `launch_y` | `0xB3B419` | u16 / 2 |
| `launch_z` | `0xB3B433` | u16 / 2 |
| `target_x` | `0xB3B44D` | u16 / 2 |
| `target_y` | `0xB3B467` | u16 / 2 |
| `target_z` | `0xB3B481` | u16 / 2 |
| `charge_lv` | `0xB3B49B` | u8 / 1 |
| `AI_ent_id` | `0xB3B4B5` | u16 / 2 |
| `reflect_ent_id` | `0xB3B4CF` | u16 / 2 |
