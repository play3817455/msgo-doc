# 汇编证据 —— CS-0xF3B3-lounge-msma_over_custom_level_up

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0x00BA7CE0`（`0x00BA7CE0`..`0x00BA7ED2`），函数 `sub_BA7CE0`
- 命令名字符串：`)<-_proto_lounge_client::send_msma_over_custom_level_up(` @ `0x00EED594`
- opcode 写入：`0x00BA7D54`
- 声明容量：`0xE`（分配器容量 `push` @ `0x00BA7D26`）
- 提交（`sub_B02FF0`）：`0x00BA7DD8`
- 发送去向：`vt[0x58]` @ `0x00BA7E60`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00BA7D2F  push    eax
  00BA7D30  lea     ecx, [esp+44h+var_2C]
  00BA7D34  call    sub_ABB2F0   ; <<< 初始化 {cur,end}（游标自 buf+2 起）
  00BA7D39  lea     ecx, [ebp+0Eh]
  00BA7D3C  lea     eax, [ebp+2]
  00BA7D3F  cmp     eax, ecx
  00BA7D41  mov     [esp+40h+var_4], 0
  00BA7D49  ja      loc_BA7EBD
  00BA7D4F  lea     edx, [eax+8]
  00BA7D52  cmp     edx, ecx
  00BA7D54  mov     word ptr [ebp+0], 0F3B3h   ; <<< 内联写线（u16）
  00BA7D5A  ja      loc_BA7EBD
  00BA7D60  mov     esi, [esp+40h+arg_0]
  00BA7D64  mov     [eax], esi   ; <<< 内联写线（u32）
  00BA7D66  mov     esi, [esp+40h+arg_4]
  00BA7D6A  lea     ebx, [edx+4]
  00BA7D6D  cmp     ebx, ecx
  00BA7D6F  mov     [eax+4], esi   ; <<< 内联写线（u32）
  00BA7D72  ja      loc_BA7EBD
  00BA7D78  mov     ecx, [esp+40h+arg_8]
  00BA7D7C  mov     [edx], ecx   ; <<< 内联写线（u32）
  00BA7D7E  mov     esi, [edi+831Ch]
  00BA7D84  test    esi, esi
  00BA7D86  jz      loc_BA7E5E
  00BA7D8C  lea     edx, [esp+40h+var_28]
  00BA7D90  push    edx
  00BA7D91  call    sub_CA0CE0
  00BA7D96  add     esp, 4
  00BA7D99  mov     ecx, [edi+8]
  00BA7D9C  push    offset aProtoLoungeCli_463
  00BA7DA1  push    ecx
  00BA7DA2  push    offset aId
  00BA7DA7  push    eax
  00BA7DA8  push    esi
  00BA7DA9  mov     byte ptr [esp+54h+var_4], 1
  00BA7DAE  call    sub_B03020
  00BA7DB3  add     esp, 8
  00BA7DB6  push    eax
  00BA7DB7  call    sub_41D990
  00BA7DBC  add     esp, 8
  00BA7DBF  mov     ecx, eax
  00BA7DC1  call    sub_ADC810
  00BA7DC6  push    eax
  00BA7DC7  call    sub_41D990
  00BA7DCC  add     esp, 8
  00BA7DCF  lea     ecx, [esp+40h+var_28]
  00BA7DD3  mov     byte ptr [esp+40h+var_4], 0
  00BA7DD8  call    sub_B02FF0   ; <<< 提交（C→S 闭合点）
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00BA7DD8  call    sub_B02FF0
  00BA7DDD  mov     edx, [esp+40h+arg_4]
  00BA7DE1  mov     eax, [esp+40h+arg_0]
  00BA7DE5  push    offset word_F641DC
  00BA7DEA  push    edx
  00BA7DEB  push    eax
  00BA7DEC  push    offset aUniqMsid
  00BA7DF1  push    esi
  00BA7DF2  call    sub_41D990
  00BA7DF7  add     esp, 8
  00BA7DFA  mov     ecx, eax
  00BA7DFC  call    sub_B08500
  00BA7E01  push    eax
  00BA7E02  call    sub_41D990
  00BA7E07  mov     ecx, [esp+48h+arg_8]
  00BA7E0B  add     esp, 8
  00BA7E0E  push    ecx
  00BA7E0F  push    offset aLevel
  00BA7E14  push    esi
  00BA7E15  call    sub_41D990
  00BA7E1A  add     esp, 8
  00BA7E1D  mov     ecx, eax
  00BA7E1F  call    sub_B03580
  00BA7E24  push    offset aByte
  00BA7E29  mov     edx, ebx
  00BA7E2B  sub     edx, ebp
  00BA7E2D  push    edx
  00BA7E2E  push    offset asc_EDAD58
  00BA7E33  push    esi
  00BA7E34  call    sub_41D990
  00BA7E39  add     esp, 8
  00BA7E3C  mov     ecx, eax
  00BA7E3E  call    sub_B03580
  00BA7E43  push    eax
  00BA7E44  call    sub_41D990
  00BA7E49  add     esp, 8
  00BA7E4C  mov     esi, eax
  00BA7E4E  push    0Ah
  00BA7E50  mov     ecx, esi
  00BA7E52  call    sub_B036E0
  00BA7E57  mov     ecx, esi
  00BA7E59  call    sub_40DDF0
  00BA7E5E  mov     eax, [edi]
  00BA7E60  mov     edx, [eax+58h]
```

## 4. 发送去向切片

```asm
  00BA7E5E  mov     eax, [edi]
  00BA7E60  mov     edx, [eax+58h]
  00BA7E63  sub     ebx, ebp
  00BA7E65  push    ebx
  00BA7E66  push    ebp
  00BA7E67  mov     ecx, edi
  00BA7E69  call    edx
  00BA7E6B  test    al, al
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `00BA7D54` | u16 / 2 |
| `uniq_msid` | `0xBA7D64`;`0xBA7D6F` | u64 / 8 |
| `level` | `0xBA7D7C` | u32 / 4 |
