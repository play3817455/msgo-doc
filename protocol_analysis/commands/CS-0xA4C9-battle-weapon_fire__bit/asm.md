# 汇编证据 —— CS-0xA4C9-battle-weapon_fire__bit

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B39420 @ `0xB39420`（`0xB39420`..`0xB3998D`）
- 命令名字符串：`)<-_proto_battle_client::send_weapon_fire__bit(` @ `0xEE0F34`
- opcode 写入：`0xB3949C`
- 声明容量：`0x003E`（分配器容量 `push` @ `0xB39466`）
- 发送去向：`vt[0x58]` @ `0xB3991B`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00b39466  push    3Eh ; '>'
  00b3949c  mov     word ptr [ebp+0], 0A4C9h   ; 字段 0 `opcode` => 2
  00b394ac  mov     [eax], esi   ; 字段 1 `frame_count` => 4
  00b394c7  mov     [eax], ecx   ; 字段 2 `shot_bit_id` => 4
  00b394cf  call    sub_B02DA0   ; 字段 3 `shot_ent_id` => 2
  00b394e9  call    sub_B061C0   ; 字段 4 `shot_alive` => 1
  00b39503  call    sub_B02DA0   ; 字段 5 `launch_x` => 2
  00b3951d  call    sub_B02DA0   ; 字段 6 `launch_y` => 2
  00b39537  call    sub_B02DA0   ; 字段 7 `launch_z` => 2
  00b39551  call    sub_B02DA0   ; 字段 8 `target_x` => 2
  00b3956b  call    sub_B02DA0   ; 字段 9 `target_y` => 2
  00b39585  call    sub_B02DA0   ; 字段 10 `target_z` => 2
  00b3959f  call    sub_B02DA0   ; 字段 11 `target_ent_id` => 2
  00b395b9  call    sub_B02DA0   ; 字段 12 `msec` => 2
  00b395d6  call    sub_B061C0   ; 字段 13 `release0_shot1` => 1
  00b395f3  call    sub_B061C0   ; 字段 14 `fx_opt` => 1
  00b39610  call    sub_B02DA0   ; 字段 15 `AI_ent_id` => 2
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00EDC830  push offset a<name>; "frame_count="
  00EDC31C  push offset a<name>; "shot_bit_id="
  00EDC30C  push offset a<name>; "shot_ent_id="
  00EDC300  push offset a<name>; "shot_alive="
  00EDC464  push offset a<name>; "launch_x="
  00EDC458  push offset a<name>; "launch_y="
  00EDC44C  push offset a<name>; "launch_z="
  00EDB960  push offset a<name>; "target_x="
  00EDB954  push offset a<name>; "target_y="
  00EDB948  push offset a<name>; "target_z="
  00EDC7F8  push offset a<name>; "target_ent_id="
  00EDC78C  push offset a<name>; "msec="
  00EDC2F0  push offset a<name>; "release0_shot1="
  00EDC434  push offset a<name>; "fx_opt="
  00EDC870  push offset a<name>; "AI_ent_id="
```

## 4. 发送去向切片

```asm
  00b3991b  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB3949C` | u16 / 2 |
| `frame_count` | `0xB394AC` | u32 / 4 |
| `shot_bit_id` | `0xB394C7` | u32 / 4 |
| `shot_ent_id` | `0xB394CF` | u16 / 2 |
| `shot_alive` | `0xB394E9` | u8 / 1 |
| `launch_x` | `0xB39503` | u16 / 2 |
| `launch_y` | `0xB3951D` | u16 / 2 |
| `launch_z` | `0xB39537` | u16 / 2 |
| `target_x` | `0xB39551` | u16 / 2 |
| `target_y` | `0xB3956B` | u16 / 2 |
| `target_z` | `0xB39585` | u16 / 2 |
| `target_ent_id` | `0xB3959F` | u16 / 2 |
| `msec` | `0xB395B9` | u16 / 2 |
| `release0_shot1` | `0xB395D6` | u8 / 1 |
| `fx_opt` | `0xB395F3` | u8 / 1 |
| `AI_ent_id` | `0xB39610` | u16 / 2 |
