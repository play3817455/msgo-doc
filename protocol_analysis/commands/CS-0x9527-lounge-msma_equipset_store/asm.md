# 汇编证据 —— CS-0x9527-lounge-msma_equipset_store

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B98E80 @ `0xb98e80`（`0xb98e80`..`0xb99093`）
- 命令名字符串：`)<-_proto_lounge_client::send_msma_equipset_store(` @ `0xeebcb0`
- opcode 写入：`0xb98f02`
- 声明容量：`0x86`（分配器容量 `push` @ `0xb98ec6`）

## 2. 组包块切片（游标初始化 → 逐字段写线 → 提交）

```asm
  0xb98ecd  mov     ebp, eax
  0xb98ecf  mov     eax, [edi+0Ch]
  0xb98ed2  push    eax
  0xb98ed3  lea     ecx, [esp+4Ch+var_34]
  0xb98ed7  call    sub_ABB2F0
  0xb98edc  lea     ecx, [ebp+86h]
  0xb98ee2  lea     eax, [ebp+2]
  0xb98ee5  cmp     eax, ecx
  0xb98ee7  mov     [esp+48h+var_4], 0
  0xb98eef  mov     [esp+48h+var_30], ebp
  0xb98ef3  mov     dword ptr [esp+48h+var_2C], ecx
  0xb98ef7  ja      loc_B9907E
  0xb98efd  lea     edx, [eax+8]
  0xb98f00  cmp     edx, ecx
  0xb98f02  mov     word ptr [ebp+0], 9527h
  0xb98f08  ja      loc_B9907E
  0xb98f0e  mov     ecx, [esp+48h+arg_0]
  0xb98f12  mov     [eax], ecx
  0xb98f14  mov     ecx, [esp+48h+arg_4]
  0xb98f18  mov     [esp+48h+var_30], edx
  0xb98f1c  lea     edx, [esp+48h+var_30]
  0xb98f20  mov     [eax+4], ecx
  0xb98f23  mov     eax, [esp+48h+arg_8]
  0xb98f27  push    edx
  0xb98f28  push    eax
  0xb98f29  call    sub_B41C60
  0xb98f2e  add     esp, 8
  0xb98f31  test    al, al
  0xb98f33  jz      loc_B9907E
  0xb98f39  mov     esi, [edi+7E6Ch]
  0xb98f3f  test    esi, esi
  0xb98f41  mov     ebx, [esp+48h+var_30]
  0xb98f45  jz      loc_B9901F
  0xb98f4b  lea     ecx, [esp+48h+var_28]
  0xb98f4f  push    ecx
  0xb98f50  call    sub_CA0CE0
  0xb98f55  add     esp, 4
  0xb98f58  mov     edx, [edi+8]
  0xb98f5b  push    offset aProtoLoungeCli_439; ")<-_proto_lounge_client::send_msma_equi"...
  0xb98f60  push    edx
  0xb98f61  push    offset aId; " (id:"
  0xb98f66  push    eax
  0xb98f67  push    esi
  0xb98f68  mov     byte ptr [esp+5Ch+var_4], 1
  0xb98f6d  call    sub_B03020
  0xb98f72  add     esp, 8
  0xb98f75  push    eax
  0xb98f76  call    sub_41D990
  0xb98f7b  add     esp, 8
  0xb98f7e  mov     ecx, eax
  0xb98f80  call    sub_ADC810
  0xb98f85  push    eax
  0xb98f86  call    sub_41D990
  0xb98f8b  add     esp, 8
  0xb98f8e  lea     ecx, [esp+48h+var_28]
  0xb98f92  mov     byte ptr [esp+48h+var_4], 0
  0xb98f97  call    sub_B02FF0
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。
> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B02B40`=写 NUL 串（其**紧邻之前的 `push N`** = 串槽预算）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb98fab  push    offset aUniqidMs; "uniqid_ms="
  0xb98fce  push    offset aEquipSet; "equip_set="
  0xb98fe5  push    offset aByte; "]byte"
  0xb98fef  push    offset asc_EDAD58; " ) ["
```

## 4. 发送去向切片

```asm
  0xb99021  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xb98f02` | u16 |
| `uniqid_ms` | `0xB98F12, 0xB98F20` | u64 |
| `equip_set.uniq_id` | `0xB41C73, 0xB41C7B` | u64 |
| `equip_set.slot` | `0xB41C92` | u16 |
| `equip_set.eq_weapon` | `0xB41CA3 (loop @0xB41CA3..0xB41CC3)` | u32[3] |
| `equip_set.eq_shield` | `0xB41CD1` | u32 |
| `equip_set.eq_special` | `0xB41CE7` | u32 |
| `equip_set.eq_modules` | `0xB41D00 (loop @0xB41D00..0xB41D1E)` | u32[10] |
| `equip_set.eq_bonus_modules` | `0xB41D25 (loop @0xB41D25..0xB41D3F)` | u32 |
| `equip_set.eq_rental_modules` | `0xB41D46 (loop @0xB41D46..0xB41D60)` | u32 |
| `equip_set.setname` | `0xB41D64 (loop @0xB41D64..0xB41D7D)` | u8[43] |
