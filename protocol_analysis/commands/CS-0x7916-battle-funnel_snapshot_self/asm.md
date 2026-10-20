# 汇编证据 —— CS-0x7916-battle-funnel_snapshot_self

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B3AB30 @ `0xb3ab30`（`0xb3ab30`..`0xb3ad27`）
- 命令名字符串：`)<-_proto_battle_client::send_funnel_snapshot_self(` @ `0xee1048`
- opcode 写入：`0xb3abd4`
- 声明容量：`0xE`（分配器容量 `push` @ `0xb3ab99`）

## 2. 组包块切片（游标初始化 → 逐字段写线 → 提交）

```asm
  0xb3ab9d  mov     edi, eax
  0xb3ab9f  mov     eax, [esi+0Ch]
  0xb3aba2  push    eax
  0xb3aba3  lea     ecx, [esp+5Ch+var_44]
  0xb3aba7  call    sub_ABB2F0
  0xb3abac  lea     ecx, [edi+0Eh]
  0xb3abaf  lea     eax, [edi+2]
  0xb3abb2  cmp     eax, ecx
  0xb3abb4  mov     [esp+58h+var_4], 0
  0xb3abbc  mov     [esp+58h+var_40], edi
  0xb3abc0  mov     dword ptr [esp+58h+var_3C], ecx
  0xb3abc4  ja      loc_B3AD12
  0xb3abca  lea     ecx, [esp+58h+var_40]
  0xb3abce  push    ecx
  0xb3abcf  lea     edx, [esp+5Ch+var_1C]
  0xb3abd3  push    edx
  0xb3abd4  mov     word ptr [edi], 7916h
  0xb3abd9  mov     [esp+60h+var_40], eax
  0xb3abdd  call    sub_B06850
  0xb3abe2  add     esp, 8
  0xb3abe5  test    al, al
  0xb3abe7  jz      loc_B3AD12
  0xb3abed  mov     ebp, [esi+3E4Ch]
  0xb3abf3  test    ebp, ebp
  0xb3abf5  mov     ebx, [esp+58h+var_40]
  0xb3abf9  jz      loc_B3ACA6
  0xb3abff  lea     eax, [esp+58h+var_38]
  0xb3ac03  push    eax
  0xb3ac04  call    sub_CA0CE0
  0xb3ac09  add     esp, 4
  0xb3ac0c  mov     ecx, [esi+8]
  0xb3ac0f  push    offset aProtoBattleCli_209; ")<-_proto_battle_client::send_funnel_sn"...
  0xb3ac14  push    ecx
  0xb3ac15  push    offset aId; " (id:"
  0xb3ac1a  push    eax
  0xb3ac1b  push    ebp
  0xb3ac1c  mov     byte ptr [esp+6Ch+var_4], 1
  0xb3ac21  call    sub_B03020
  0xb3ac26  add     esp, 8
  0xb3ac29  push    eax
  0xb3ac2a  call    sub_41D990
  0xb3ac2f  add     esp, 8
  0xb3ac32  mov     ecx, eax
  0xb3ac34  call    sub_ADC810
  0xb3ac39  push    eax
  0xb3ac3a  call    sub_41D990
  0xb3ac3f  add     esp, 8
  0xb3ac42  lea     ecx, [esp+58h+var_38]
  0xb3ac46  mov     byte ptr [esp+58h+var_4], 0
  0xb3ac4b  call    sub_B02FF0
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。
> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B02B40`=写 NUL 串（其**紧邻之前的 `push N`** = 串槽预算）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb3ac55  push    offset aSnapshot; "snapshot="
  0xb3ac6c  push    offset aByte; "]byte"
  0xb3ac76  push    offset asc_EDAD58; " ) ["
```

## 4. 发送去向切片

```asm
  0xb3ab58  lea     eax, [esp+58h+var_C]
  0xb3ab62  mov     eax, [esp+58h+arg_0]
  0xb3ab66  mov     edx, [esp+58h+arg_8]
  0xb3ab73  mov     ecx, [esp+58h+arg_4]
  0xb3ab77  mov     [esp+58h+var_1C], eax
  0xb3ab7b  mov     [esp+58h+var_18], ecx
  0xb3ab7f  mov     [esp+58h+var_14], edx
  0xb3abb4  mov     [esp+58h+var_4], 0
  0xb3abbc  mov     [esp+58h+var_40], edi
  0xb3abc0  mov     dword ptr [esp+58h+var_3C], ecx
  0xb3abca  lea     ecx, [esp+58h+var_40]
  0xb3abf5  mov     ebx, [esp+58h+var_40]
  0xb3abff  lea     eax, [esp+58h+var_38]
  0xb3ac42  lea     ecx, [esp+58h+var_38]
  0xb3ac46  mov     byte ptr [esp+58h+var_4], 0
  0xb3ac50  lea     edx, [esp+58h+var_1C]
  0xb3aca8  mov     eax, [edx+58h]
  0xb3acd7  lea     ecx, [esp+58h+var_44]
  0xb3acdb  mov     [esp+58h+var_4], 0FFFFFFFFh
  0xb3acf1  mov     ecx, dword ptr [esp+58h+var_C]
  0xb3ad12  lea     ecx, [esp+58h+var_44]
  0xb3ad16  mov     [esp+58h+var_4], 0FFFFFFFFh
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xb3abd4` | u16 |
| `snapshot.ent_id` | `0xB41C63` | u32 |
| `snapshot.wslot_idx` | `0xB41C74` | i8 |
| `snapshot.move_info` | `0xB41C89` | u8[5] |
