# 汇编证据 —— CS-0xA8FE-battle-weapon_fire_prepare__destruct_r

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B39990 @ `0xB39990`（`0xB39990`..`0xB3A1EC`）
- 命令名字符串：`)<-_proto_battle_client::send_weapon_fire_prepare__destruct_r(` @ `0xEE0F68`
- opcode 写入：`0xB39A1A`
- 声明容量：`0x010E`（分配器容量 `push` @ `0xB399DA`）
- 发送去向：`vt[0x58]` @ `0xB3A17A`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00b399da  push    10Eh
  00b39a1a  mov     word ptr [esi], 0A8FEh   ; 字段 0 `opcode` => 2
  00b39a29  mov     [eax], esi   ; 字段 1 `frame_count` => 4
  00b39a44  mov     [eax], ecx   ; 字段 2 `weapon_itemid` => 4
  00b39a4c  call    sub_B02D80   ; 字段 3 `fire_id` => 4
  00b39a73  call    sub_B02D80   ; 字段 4 `ent_ids_count` => 4
  00b39a96  call    sub_B02DA0   ; 字段 5 `ent_ids` => 2N (N≤16)
  00b39ac7  call    sub_B02D80   ; 字段 6 `hit_pos_x_count` => 4
  00b39ae7  call    sub_B02DA0   ; 字段 7 `hit_pos_x` => 2N (N≤16)
  00b39b18  call    sub_B02D80   ; 字段 8 `hit_pos_y_count` => 4
  00b39b38  call    sub_B02DA0   ; 字段 9 `hit_pos_y` => 2N (N≤16)
  00b39b6c  call    sub_B02D80   ; 字段 10 `hit_pos_z_count` => 4
  00b39b8c  call    sub_B02DA0   ; 字段 11 `hit_pos_z` => 2N (N≤16)
  00b39bc3  call    sub_B02D80   ; 字段 12 `hit_dirs_count` => 4
  00b39be6  call    sub_B02DA0   ; 字段 13 `hit_dirs` => 2N (N≤16)
  00b39c1d  call    sub_B02D80   ; 字段 14 `hit_distance_count` => 4
  00b39c46  call    sub_B02DA0   ; 字段 15 `hit_distance` => 2N (N≤16)
  00b39c7d  call    sub_B02D80   ; 字段 16 `body_regions_count` => 4
  00b39cb3  mov     [ecx], di   ; 字段 17 `body_regions` => 2N (N≤16)
  00b39cda  mov     [ecx], ax   ; 字段 18 `AI_ent_id` => 2
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00EDC830  push offset a<name>; "frame_count="
  00EDC024  push offset a<name>; "weapon_itemid="
  00EDC560  push offset a<name>; "fire_id="
  00EDC554  push offset a<name>; "ent_ids={"
  00EDC548  push offset a<name>; "hit_pos_x={"
  00EDC53C  push offset a<name>; "hit_pos_y={"
  00EDC530  push offset a<name>; "hit_pos_z={"
  00EDC524  push offset a<name>; "hit_dirs={"
  00EDC514  push offset a<name>; "hit_distance={"
  00EDC4F4  push offset a<name>; "body_regions={"
  00EDC870  push offset a<name>; "AI_ent_id="
```

## 4. 发送去向切片

```asm
  00b3a17a  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB39A1A` | u16 / 2 |
| `frame_count` | `0xB39A29` | u32 / 4 |
| `weapon_itemid` | `0xB39A44` | u32 / 4 |
| `fire_id` | `0xB39A4C` | u32 / 4 |
| `ent_ids_count` | `0xB39A73` | u32 / 4 |
| `ent_ids` | `0xB39A96` | u16[N] / 2N (N≤16) |
| `hit_pos_x_count` | `0xB39AC7` | u32 / 4 |
| `hit_pos_x` | `0xB39AE7` | u16[N] / 2N (N≤16) |
| `hit_pos_y_count` | `0xB39B18` | u32 / 4 |
| `hit_pos_y` | `0xB39B38` | u16[N] / 2N (N≤16) |
| `hit_pos_z_count` | `0xB39B6C` | u32 / 4 |
| `hit_pos_z` | `0xB39B8C` | u16[N] / 2N (N≤16) |
| `hit_dirs_count` | `0xB39BC3` | u32 / 4 |
| `hit_dirs` | `0xB39BE6` | u16[N] / 2N (N≤16) |
| `hit_distance_count` | `0xB39C1D` | u32 / 4 |
| `hit_distance` | `0xB39C46` | u16[N] / 2N (N≤16) |
| `body_regions_count` | `0xB39C7D` | u32 / 4 |
| `body_regions` | `0xB39CB3` | u16[N] / 2N (N≤16) |
| `AI_ent_id` | `0xB39CDA` | u16 / 2 |
