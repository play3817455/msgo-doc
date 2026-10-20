# 汇编证据 —— CS-0xA76E-lounge-msma_msset_store

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B988D0 @ `0xB988D0`（`0xB988D0`..`0xB98A99`）
- 命令名字符串：`)<-_proto_lounge_client::send_msma_msset_store(` @ `0xEEBC18`
- opcode 写入：`0xB98951`
- 声明容量：`0x0062`（分配器容量 `push` @ `0xB98916`）
- 发送去向：`vt[0x58]` @ `0xB98A25`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00b98916  push    62h ; 'b'
  00b98951  mov     word ptr [edi], 0A76Eh   ; 字段 0 `opcode` => 2
  00b41b27  mov     edx, [edi]   ; 字段 1 `ms_set.uniq_id` => 8
  00b41b2b  mov     edx, [edi+4]   ; 字段 1 `ms_set.uniq_id` => 8
  00b41b42  mov     dx, [edi+8]   ; 字段 2 `ms_set.deck_type` => 2
  00b41b5a  mov     dx, [edi+0Ah]   ; 字段 3 `ms_set.deck_slot` => 2
  00b41b71  mov     dl, [ecx+edi+0Ch]   ; 字段 4 `ms_set.setname` => 43
  00b41b92  mov     ebx, [ecx]   ; 字段 5 `ms_set.msma_uniq_ids` => 32
  00b41b96  mov     ebx, [ecx+4]   ; 字段 5 `ms_set.msma_uniq_ids` => 32
  00b41bba  mov     di, [edx]   ; 字段 6 `ms_set.equip_set_slots` => 8
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00EE3C70  push offset a<name>; "ms_set="
```

## 4. 发送去向切片

```asm
  00b98a25  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB98951` | u16 / 2 |
| `ms_set.uniq_id` | `0xB41B27, 0xB41B2B` | u64 / 8 |
| `ms_set.deck_type` | `0xB41B42` | u16 / 2 |
| `ms_set.deck_slot` | `0xB41B5A` | u16 / 2 |
| `ms_set.setname` | `0xB41B71` | u8[43] / 43 |
| `ms_set.msma_uniq_ids` | `0xB41B92, 0xB41B96` | u64[4] / 32 |
| `ms_set.equip_set_slots` | `0xB41BBA` | u16[4] / 8 |
