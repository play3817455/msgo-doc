# 汇编证据 —— CS-0xE1DB-lounge-clan_kick_member

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0x00BA1410`（`0x00BA1410`..`0x00BA15F8`），函数 `sub_BA1410`
- 命令名字符串：`)<-_proto_lounge_client::send_clan_kick_member(` @ `0x00EECA44`
- opcode 写入：`0x00BA1484`
- 声明容量：`0xA`（分配器容量 `push` @ `0x00BA1456`）
- 提交（`sub_B02FF0`）：`0x00BA1501`
- 发送去向：`vt[0x58]` @ `0x00BA1586`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00BA145F  push    eax
  00BA1460  lea     ecx, [esp+44h+var_2C]
  00BA1464  call    sub_ABB2F0   ; <<< 初始化 {cur,end}（游标自 buf+2 起）
  00BA1469  lea     eax, [ebp+0Ah]
  00BA146C  lea     ecx, [ebp+2]
  00BA146F  cmp     ecx, eax
  00BA1471  mov     [esp+40h+var_4], 0
  00BA1479  ja      loc_BA15E3
  00BA147F  lea     edx, [ecx+4]
  00BA1482  cmp     edx, eax
  00BA1484  mov     word ptr [ebp+0], 0E1DBh   ; <<< 内联写线（u16）
  00BA148A  ja      loc_BA15E3
  00BA1490  mov     edi, dword ptr [esp+40h+arg_0]
  00BA1494  lea     ebx, [edx+1]
  00BA1497  cmp     ebx, eax
  00BA1499  mov     [ecx], edi   ; <<< 内联写线（u32）
  00BA149B  ja      loc_BA15E3
  00BA14A1  mov     cl, [esp+40h+arg_4]
  00BA14A5  mov     [edx], cl   ; <<< 内联写线（u8）
  00BA14A7  mov     edi, [esi+80D8h]
  00BA14AD  test    edi, edi
  00BA14AF  jz      loc_BA1584
  00BA14B5  lea     edx, [esp+40h+var_28]
  00BA14B9  push    edx
  00BA14BA  call    sub_CA0CE0
  00BA14BF  add     esp, 4
  00BA14C2  mov     ecx, [esi+8]
  00BA14C5  push    offset aProtoLoungeCli_484
  00BA14CA  push    ecx
  00BA14CB  push    offset aId
  00BA14D0  push    eax
  00BA14D1  push    edi
  00BA14D2  mov     byte ptr [esp+54h+var_4], 1
  00BA14D7  call    sub_B03020
  00BA14DC  add     esp, 8
  00BA14DF  push    eax
  00BA14E0  call    sub_41D990
  00BA14E5  add     esp, 8
  00BA14E8  mov     ecx, eax
  00BA14EA  call    sub_ADC810
  00BA14EF  push    eax
  00BA14F0  call    sub_41D990
  00BA14F5  add     esp, 8
  00BA14F8  lea     ecx, [esp+40h+var_28]
  00BA14FC  mov     byte ptr [esp+40h+var_4], 0
  00BA1501  call    sub_B02FF0   ; <<< 提交（C→S 闭合点）
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00BA1501  call    sub_B02FF0
  00BA1506  mov     edx, dword ptr [esp+40h+arg_0]
  00BA150A  push    offset word_F641DC
  00BA150F  push    edx
  00BA1510  push    offset aPilotIdKick
  00BA1515  push    edi
  00BA1516  call    sub_41D990
  00BA151B  add     esp, 8
  00BA151E  mov     ecx, eax
  00BA1520  call    sub_B03580
  00BA1525  push    eax
  00BA1526  call    sub_41D990
  00BA152B  add     esp, 8
  00BA152E  lea     eax, [esp+40h+arg_4]
  00BA1532  push    eax
  00BA1533  push    offset aClanKind
  00BA1538  push    edi
  00BA1539  call    sub_41D990
  00BA153E  add     esp, 8
  00BA1541  push    eax
  00BA1542  call    sub_B0C1F0
  00BA1547  add     esp, 8
  00BA154A  push    offset aByte
  00BA154F  mov     ecx, ebx
  00BA1551  sub     ecx, ebp
  00BA1553  push    ecx
  00BA1554  push    offset asc_EDAD58
  00BA1559  push    edi
  00BA155A  call    sub_41D990
  00BA155F  add     esp, 8
  00BA1562  mov     ecx, eax
  00BA1564  call    sub_B03580
  00BA1569  push    eax
  00BA156A  call    sub_41D990
  00BA156F  add     esp, 8
  00BA1572  mov     edi, eax
  00BA1574  push    0Ah
  00BA1576  mov     ecx, edi
  00BA1578  call    sub_B036E0
  00BA157D  mov     ecx, edi
  00BA157F  call    sub_40DDF0
  00BA1584  mov     edx, [esi]
  00BA1586  mov     eax, [edx+58h]
```

## 4. 发送去向切片

```asm
  00BA1584  mov     edx, [esi]
  00BA1586  mov     eax, [edx+58h]
  00BA1589  sub     ebx, ebp
  00BA158B  push    ebx
  00BA158C  push    ebp
  00BA158D  mov     ecx, esi
  00BA158F  call    eax
  00BA1591  test    al, al
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `00BA1484` | u16 / 2 |
| `pilot_id_kick` | `0xBA1499` | u32 / 4 |
| `clan_kind` | `0xBA14A5` | u8 / 1 |
