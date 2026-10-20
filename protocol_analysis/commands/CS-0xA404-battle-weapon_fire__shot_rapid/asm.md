# 汇编证据 —— CS-0xA404-battle-weapon_fire__shot_rapid

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B368B0 @ `0xB368B0`（`0xB368B0`..`0xB36C77`）
- 命令名字符串：`)<-_proto_battle_client::send_weapon_fire__shot_rapid(` @ `0xEE0C9C`
- opcode 写入：`0xB3692C`
- 声明容量：`0x0026`（分配器容量 `push` @ `0xB368F6`）
- 发送去向：`vt[0x58]` @ `0xB36C08`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00b368f6  push    26h ; '&'
  00b3692c  mov     word ptr [ebp+0], 0A404h   ; 字段 0 `opcode` => 2
  00b3693c  mov     [ecx], esi   ; 字段 1 `frame_count` => 4
  00b36956  mov     [edx], ax   ; 字段 2 `target_x` => 2
  00b3695f  call    sub_B02DA0   ; 字段 3 `target_y` => 2
  00b36979  call    sub_B02DA0   ; 字段 4 `target_z` => 2
  00b36993  call    sub_B02DA0   ; 字段 5 `rcnt_bullet_mgz` => 2
  00b369ad  call    sub_B02DA0   ; 字段 6 `rcnt_bullet_all` => 2
  00b369c7  call    sub_B061C0   ; 字段 7 `begin1_end0` => 1
  00b369e1  call    sub_B02DA0   ; 字段 8 `AI_ent_id` => 2
  00b369fb  call    sub_B061C0   ; 字段 9 `salvo_slot` => 1
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00EDC830  push offset a<name>; "frame_count="
  00EDB960  push offset a<name>; "target_x="
  00EDB954  push offset a<name>; "target_y="
  00EDB948  push offset a<name>; "target_z="
  00EDC6EC  push offset a<name>; "rcnt_bullet_mgz="
  00EDC6D8  push offset a<name>; "rcnt_bullet_all="
  00EDC6C8  push offset a<name>; "begin1_end0="
  00EDC870  push offset a<name>; "AI_ent_id="
  00EDC470  push offset a<name>; "salvo_slot="
```

## 4. 发送去向切片

```asm
  00b36c08  mov     edx, [eax+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB3692C` | u16 / 2 |
| `frame_count` | `0xB3693C` | u32 / 4 |
| `target_x` | `0xB36956` | u16 / 2 |
| `target_y` | `0xB3695F` | u16 / 2 |
| `target_z` | `0xB36979` | u16 / 2 |
| `rcnt_bullet_mgz` | `0xB36993` | u16 / 2 |
| `rcnt_bullet_all` | `0xB369AD` | u16 / 2 |
| `begin1_end0` | `0xB369C7` | u8 / 1 |
| `AI_ent_id` | `0xB369E1` | u16 / 2 |
| `salvo_slot` | `0xB369FB` | u8 / 1 |
