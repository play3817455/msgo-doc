# 汇编证据 —— CS-0xBFA9-battle-weapon_fire__deploy_arms

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0xB38670`（`0xB38670`..`0xB38AC0`）
- 命令名字符串：`)<-_proto_battle_client::send_weapon_fire__deploy_arms(` @ `0xEE0E40`
- opcode 写入：`0xB386EC`
- 声明容量：`0x2E`（分配器容量 `push` @ `0xB386B6`）
- 提交（`sub_B02FF0`）：`0xB3885D`
- 发送去向：`vt[0x58]` @ `0xB38A4E`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  0xB386B6  push    0x2E            ; 声明容量（不是线长）
  0xB386EC  mov     word ptr [buf], BFA9h   ; 字段 0 `opcode` => 2
  00b386fc  mov     [ecx], esi                         ; 字段 1 `frame_count` => u32 (arg_0)
  00b38716  mov     [edx], ax                          ; 字段 2 `target_x` => u16 (arg_4)
  00b3871f  call    sub_B02DA0                         ; 字段 3 `target_y` => u16 (arg_8)
  00b38739  call    sub_B02DA0                         ; 字段 4 `target_z` => u16 (arg_C)
  00b38753  call    sub_B02DA0                         ; 字段 5 `target_ent_id` => u16 (arg_10)
  00b3876d  call    sub_B061C0                         ; 字段 6 `state` => u8 (arg_14)
  00b38787  call    sub_B061C0                         ; 字段 7 `fx_opt` => u8 (arg_18)
  00b387a1  call    sub_B02D80                         ; 字段 8 `impact_arms_id` => u32 (arg_1C)
  00b387bb  call    sub_B02DA0                         ; 字段 9 `AI_ent_id` => u16 (arg_20)
  00b387d5  call    sub_B02D80                         ; 字段 10 `is_gmk` => u32 (arg_24)
  00b387ef  call    sub_B061C0                         ; 字段 11 `index` => u8 (arg_28)
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  push offset a<Name>; "frame_count="
  push offset a<Name>; "target_x="
  push offset a<Name>; "target_y="
  push offset a<Name>; "target_z="
  push offset a<Name>; "target_ent_id="
  push offset a<Name>; "state="
  push offset a<Name>; "fx_opt="
  push offset a<Name>; "impact_arms_id="
  push offset a<Name>; "AI_ent_id="
  push offset a<Name>; "is_gmk="
  push offset a<Name>; "index="
```

## 4. 发送去向切片

```asm
  0xB38A4E  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB386EC` | u16 / 2 |
| `frame_count` | `0xB386FC` | u32 / 4 |
| `target_x` | `0xB38716` | u16 / 2 |
| `target_y` | `0xB3871F` | u16 / 2 |
| `target_z` | `0xB38739` | u16 / 2 |
| `target_ent_id` | `0xB38753` | u16 / 2 |
| `state` | `0xB3876D` | u8 / 1 |
| `fx_opt` | `0xB38787` | u8 / 1 |
| `impact_arms_id` | `0xB387A1` | u32 / 4 |
| `AI_ent_id` | `0xB387BB` | u16 / 2 |
| `is_gmk` | `0xB387D5` | u32 / 4 |
| `index` | `0xB387EF` | u8 / 1 |
