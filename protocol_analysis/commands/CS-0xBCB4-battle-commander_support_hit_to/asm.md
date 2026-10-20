# 汇编证据 —— CS-0xBCB4-battle-commander_support_hit_to

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0xB3E890`（`0xB3E890`..`0xB3ECBE`）
- 命令名字符串：`)<-_proto_battle_client::send_commander_support_hit_to(` @ `0xEE1500`
- opcode 写入：`0xB3E91A`
- 声明容量：`0x41A`（分配器容量 `push` @ `0xB3E8DA`）
- 提交（`sub_B02FF0`）：`0xB3EA88`
- 发送去向：`vt[0x58]` @ `0xB3EC4C`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  0xB3E8DA  push    0x41A            ; 声明容量（不是线长）
  0xB3E91A  mov     word ptr [buf], BCB4h   ; 字段 0 `opcode` => 2
  00b3e92a  mov     [ecx], si                          ; 字段 1 `ent_id` => u16 (arg_0)
  00b3e944  mov     [edx], al                          ; 字段 2 `hit_team` => u8 (arg_4)
  00b3e94c  call    sub_B061C0                         ; 字段 3 `hit_troops` => u8 (arg_8)
  00b3e966  call    sub_B02D80                         ; 字段 4 `support_type` => u32 (arg_C)
  00b3e990  call    sub_B02D80                         ; 字段 5 `ent_ids_num` => u32 (arg_14)
  00b3e9b6  call    sub_B02DA0                         ; 字段 6 `ent_ids` => u16[N] (arg_10)
  00b3e9ea  call    sub_B02D80                         ; 字段 7 `hit_dirs_num` => u32 (arg_1C)
  00b3ea12  call    sub_B02DA0                         ; 字段 8 `hit_dirs` => u16[N] (arg_18)
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  push offset a<Name>; "ent_id="
  push offset a<Name>; "hit_team="
  push offset a<Name>; "hit_troops="
  push offset a<Name>; "support_type="
  push offset a<Name>; "ent_ids_num="
  push offset a<Name>; "ent_ids="
  push offset a<Name>; "hit_dirs_num="
  push offset a<Name>; "hit_dirs="
```

## 4. 发送去向切片

```asm
  0xB3EC4C  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB3E91A` | u16 / 2 |
| `ent_id` | `0xB3E92A` | u16 / 2 |
| `hit_team` | `0xB3E944` | u8 / 1 |
| `hit_troops` | `0xB3E94C` | u8 / 1 |
| `support_type` | `0xB3E966` | u32 / 4 |
| `ent_ids_num` | `0xB3E990` | u32 / 4；写循环前与 `0x100` 比较（上界闸） |
| `ent_ids` | `0xB3E9B6` | u16[N] / 2N（N≤256，循环上界取自 `ent_ids_num`） |
| `hit_dirs_num` | `0xB3E9EA` | u32 / 4；写循环前与 `0x100` 比较（上界闸） |
| `hit_dirs` | `0xB3EA12` | u16[N] / 2N（N≤256，循环上界取自 `hit_dirs_num`） |
