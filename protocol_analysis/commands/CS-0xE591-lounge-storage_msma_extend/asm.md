# 汇编证据 —— CS-0xE591-lounge-storage_msma_extend

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0x00BA3E90`（`0x00BA3E90`..`0x00BA410C`），函数 `sub_BA3E90`
- 命令名字符串：`)<-_proto_lounge_client::send_storage_msma_extend(` @ `0x00EECECC`
- opcode 写入：`0x00BA3F0C`
- 声明容量：`0x12`（分配器容量 `push` @ `0x00BA3ED6`）
- 提交（`sub_B02FF0`）：`0x00BA3FC7`
- 发送去向：`vt[0x58]` @ `0x00BA409A`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00BA3EDF  push    eax
  00BA3EE0  lea     ecx, [esp+4Ch+var_34]
  00BA3EE4  call    sub_ABB2F0   ; <<< 初始化 {cur,end}（游标自 buf+2 起）
  00BA3EE9  lea     ecx, [ebp+12h]
  00BA3EEC  lea     eax, [ebp+2]
  00BA3EEF  cmp     eax, ecx
  00BA3EF1  mov     [esp+48h+var_4], 0
  00BA3EF9  mov     [esp+48h+var_30], ebp
  00BA3EFD  mov     dword ptr [esp+48h+var_2C], ecx
  00BA3F01  ja      loc_BA40F7
  00BA3F07  lea     edx, [eax+4]
  00BA3F0A  cmp     edx, ecx
  00BA3F0C  mov     word ptr [ebp+0], 0E591h   ; <<< 内联写线（u16）
  00BA3F12  ja      loc_BA40F7
  00BA3F18  mov     esi, [esp+48h+arg_0]
  00BA3F1C  mov     [eax], esi   ; <<< 内联写线（u32）
  00BA3F1E  mov     eax, edx
  00BA3F20  lea     edx, [eax+4]
  00BA3F23  cmp     edx, ecx
  00BA3F25  ja      loc_BA40F7
  00BA3F2B  mov     ecx, [esp+48h+arg_4]
  00BA3F2F  mov     [esp+48h+var_30], edx
  00BA3F33  lea     edx, [esp+48h+var_30]
  00BA3F37  mov     [eax], ecx   ; <<< 内联写线（u32）
  00BA3F39  push    edx
  00BA3F3A  lea     eax, [esp+4Ch+arg_8]
  00BA3F3E  push    eax
  00BA3F3F  call    sub_B02D80   ; <<< 写线原语 u32
  00BA3F44  add     esp, 8
  00BA3F47  test    al, al
  00BA3F49  jz      loc_BA40F7
  00BA3F4F  lea     ecx, [esp+48h+var_30]
  00BA3F53  push    ecx
  00BA3F54  lea     edx, [esp+4Ch+arg_C]
  00BA3F58  push    edx
  00BA3F59  call    sub_B02D80   ; <<< 写线原语 u32
  00BA3F5E  add     esp, 8
  00BA3F61  test    al, al
  00BA3F63  jz      loc_BA40F7
  00BA3F69  mov     esi, [edi+8188h]
  00BA3F6F  test    esi, esi
  00BA3F71  mov     ebx, [esp+48h+var_30]
  00BA3F75  jz      loc_BA4098
  00BA3F7B  lea     eax, [esp+48h+var_28]
  00BA3F7F  push    eax
  00BA3F80  call    sub_CA0CE0
  00BA3F85  add     esp, 4
  00BA3F88  mov     ecx, [edi+8]
  00BA3F8B  push    offset aProtoLoungeCli_579
  00BA3F90  push    ecx
  00BA3F91  push    offset aId
  00BA3F96  push    eax
  00BA3F97  push    esi
  00BA3F98  mov     byte ptr [esp+5Ch+var_4], 1
  00BA3F9D  call    sub_B03020
  00BA3FA2  add     esp, 8
  00BA3FA5  push    eax
  00BA3FA6  call    sub_41D990
  00BA3FAB  add     esp, 8
  00BA3FAE  mov     ecx, eax
  00BA3FB0  call    sub_ADC810
  00BA3FB5  push    eax
  00BA3FB6  call    sub_41D990
  00BA3FBB  add     esp, 8
  00BA3FBE  lea     ecx, [esp+48h+var_28]
  00BA3FC2  mov     byte ptr [esp+48h+var_4], 0
  00BA3FC7  call    sub_B02FF0   ; <<< 提交（C→S 闭合点）
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00BA3FC7  call    sub_B02FF0
  00BA3FCC  mov     edx, [esp+48h+arg_0]
  00BA3FD0  push    offset word_F641DC
  00BA3FD5  push    edx
  00BA3FD6  push    offset aCount
  00BA3FDB  push    esi
  00BA3FDC  call    sub_41D990
  00BA3FE1  add     esp, 8
  00BA3FE4  mov     ecx, eax
  00BA3FE6  call    sub_B03580
  00BA3FEB  push    eax
  00BA3FEC  call    sub_41D990
  00BA3FF1  mov     eax, [esp+50h+arg_4]
  00BA3FF5  add     esp, 8
  00BA3FF8  push    offset word_F641DC
  00BA3FFD  push    eax
  00BA3FFE  push    offset aTotalPrice
  00BA4003  push    esi
  00BA4004  call    sub_41D990
  00BA4009  add     esp, 8
  00BA400C  mov     ecx, eax
  00BA400E  call    sub_B03580
  00BA4013  push    eax
  00BA4014  call    sub_41D990
  00BA4019  mov     ecx, [esp+50h+arg_8]
  00BA401D  add     esp, 8
  00BA4020  push    offset word_F641DC
  00BA4025  push    ecx
  00BA4026  push    offset aUseBc
  00BA402B  push    esi
  00BA402C  call    sub_41D990
  00BA4031  add     esp, 8
  00BA4034  mov     ecx, eax
  00BA4036  call    sub_B03580
  00BA403B  push    eax
  00BA403C  call    sub_41D990
  00BA4041  mov     edx, [esp+50h+arg_C]
  00BA4045  add     esp, 8
  00BA4048  push    edx
  00BA4049  push    offset aTokenId
  00BA404E  push    esi
  00BA404F  call    sub_41D990
  00BA4054  add     esp, 8
  00BA4057  mov     ecx, eax
  00BA4059  call    sub_B03580
  00BA405E  push    offset aByte
  00BA4063  mov     eax, ebx
  00BA4065  sub     eax, ebp
  00BA4067  push    eax
  00BA4068  push    offset asc_EDAD58
  00BA406D  push    esi
  00BA406E  call    sub_41D990
  00BA4073  add     esp, 8
  00BA4076  mov     ecx, eax
  00BA4078  call    sub_B03580
  00BA407D  push    eax
  00BA407E  call    sub_41D990
  00BA4083  add     esp, 8
  00BA4086  mov     esi, eax
  00BA4088  push    0Ah
  00BA408A  mov     ecx, esi
  00BA408C  call    sub_B036E0
  00BA4091  mov     ecx, esi
  00BA4093  call    sub_40DDF0
  00BA4098  mov     edx, [edi]
  00BA409A  mov     eax, [edx+58h]
```

## 4. 发送去向切片

```asm
  00BA4098  mov     edx, [edi]
  00BA409A  mov     eax, [edx+58h]
  00BA409D  sub     ebx, ebp
  00BA409F  push    ebx
  00BA40A0  push    ebp
  00BA40A1  mov     ecx, edi
  00BA40A3  call    eax
  00BA40A5  test    al, al
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `00BA3F0C` | u16 / 2 |
| `count` | `0xBA3F18`;`0xBA3F1C` | u32 / 4 |
| `total_price` | `0xBA3F2B`;`0xBA3F37` | u32 / 4 |
| `use_bc` | `0xBA3F3F` | u32 / 4 |
| `token_id` | `0xBA3F59` | u32 / 4 |
