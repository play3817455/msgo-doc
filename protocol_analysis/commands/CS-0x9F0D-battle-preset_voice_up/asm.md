# 汇编证据 —— CS-0x9F0D-battle-preset_voice_up

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B34930 @ `0xB34930`（`0xB34930`..`0xB34D16`）
- 命令名字符串：`)<-_proto_battle_client::send_preset_voice_up(` @ `0xEE0AA0`
- opcode 写入：`0xB349B2`
- 声明容量：`0x00DA`（分配器容量 `push` @ `0xB34976`）
- 发送去向：`vt[0x58]` @ `0xB34CA7`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00b34976  push    0DAh
  00b349b2  mov     word ptr [ebp+0], 9F0Dh   ; 字段 0 `opcode` => 2
  00b349c2  mov     [ecx], esi   ; 字段 1 `voice_id` => 4
  00b349dc  mov     [edx], ax   ; 字段 2 `AI_ent_id` => 2
  00b349e5  call    sub_B02D80   ; 字段 3 `to_world_id` => 4
  00b349ff  call    sub_B02D80   ; 字段 4 `to_pilot_id` => 4
  00b34a19  call    sub_B061C0   ; 字段 5 `is_party` => 1
  00b34a33  call    sub_B061C0   ; 字段 6 `is_use_textmsg` => 1
  00b34a52  call    sub_B02B40   ; 字段 7 `textmsg` => var(≤181)
  00b34a6c  call    sub_B061C0   ; 字段 8 `is_cutin` => 1
  00b34a86  call    sub_B061C0   ; 字段 9 `is_voice` => 1
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00EDC740  push offset a<name>; "voice_id="
  00EDC870  push offset a<name>; "AI_ent_id="
  00EDC71C  push offset a<name>; "to_world_id="
  00EDC70C  push offset a<name>; "to_pilot_id="
  00EDC380  push offset a<name>; "is_party="
  00EDC370  push offset a<name>; "is_use_textmsg="
  00EDC364  push offset a<name>; "textmsg=""
  00EDC358  push offset a<name>; "is_cutin="
  00EDC34C  push offset a<name>; "is_voice="
```

## 4. 发送去向切片

```asm
  00b34ca7  mov     edx, [eax+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB349B2` | u16 / 2 |
| `voice_id` | `0xB349C2` | u32 / 4 |
| `AI_ent_id` | `0xB349DC` | u16 / 2 |
| `to_world_id` | `0xB349E5` | u32 / 4 |
| `to_pilot_id` | `0xB349FF` | u32 / 4 |
| `is_party` | `0xB34A19` | u8 / 1 |
| `is_use_textmsg` | `0xB34A33` | u8 / 1 |
| `textmsg` | `0xB34A52` | str / var(≤181) |
| `is_cutin` | `0xB34A6C` | u8 / 1 |
| `is_voice` | `0xB34A86` | u8 / 1 |
