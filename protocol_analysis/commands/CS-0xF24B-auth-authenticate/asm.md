# 汇编证据 —— CS-0xF24B-auth-authenticate

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0x00B04EB0`（`0x00B04EB0`..`0x00B05190`），函数 `sub_B04EB0`
- 命令名字符串：`)<-_proto_auth_client::send_authenticate(` @ `0x00EDAFE0`
- opcode 写入：`0x00B04F39`
- 声明容量：`0x50A`（分配器容量 `push` @ `0x00B04EF3`）
- 提交（`sub_B02FF0`）：`0x00B0500E`
- 发送去向：`vt[0x58]` @ `0x00B05121`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00B04EFF  push    eax
  00B04F00  lea     ecx, [esp+4Ch+var_34]
  00B04F04  call    sub_ABB2F0   ; <<< 初始化 {cur,end}（游标自 buf+2 起）
  00B04F09  lea     ecx, [ebp+50Ah]
  00B04F0F  lea     eax, [ebp+2]
  00B04F12  cmp     eax, ecx
  00B04F14  mov     [esp+48h+var_4], 0
  00B04F1C  mov     [esp+48h+var_30], ebp
  00B04F20  mov     dword ptr [esp+48h+var_2C], ecx
  00B04F24  ja      loc_B0517B
  00B04F2A  mov     edx, [esp+48h+arg_0]
  00B04F2E  push    201h
  00B04F33  lea     ecx, [esp+4Ch+var_30]
  00B04F37  push    ecx
  00B04F38  push    edx
  00B04F39  mov     word ptr [ebp+0], 0F24Bh   ; <<< 内联写线（u16）
  00B04F3F  mov     [esp+54h+var_30], eax
  00B04F43  call    sub_B02B40   ; <<< 写线原语 str
  00B04F48  add     esp, 0Ch
  00B04F4B  test    al, al
  00B04F4D  jz      loc_B0517B
  00B04F53  mov     ecx, [esp+48h+arg_4]
  00B04F57  push    201h
  00B04F5C  lea     eax, [esp+4Ch+var_30]
  00B04F60  push    eax
  00B04F61  push    ecx
  00B04F62  call    sub_B02B40   ; <<< 写线原语 str
  00B04F67  add     esp, 0Ch
  00B04F6A  test    al, al
  00B04F6C  jz      loc_B0517B
  00B04F72  mov     eax, [esp+48h+arg_8]
  00B04F76  push    80h
  00B04F7B  lea     edx, [esp+4Ch+var_30]
  00B04F7F  push    edx
  00B04F80  push    eax
  00B04F81  call    sub_B02B40   ; <<< 写线原语 str
  00B04F86  add     esp, 0Ch
  00B04F89  test    al, al
  00B04F8B  jz      loc_B0517B
  00B04F91  mov     edx, [esp+48h+arg_C]
  00B04F95  push    80h
  00B04F9A  lea     ecx, [esp+4Ch+var_30]
  00B04F9E  push    ecx
  00B04F9F  push    edx
  00B04FA0  call    sub_B02B40   ; <<< 写线原语 str
  00B04FA5  add     esp, 0Ch
  00B04FA8  test    al, al
  00B04FAA  jz      loc_B0517B
  00B04FB0  mov     esi, [edi+390h]
  00B04FB6  test    esi, esi
  00B04FB8  mov     ebx, [esp+48h+var_30]
  00B04FBC  jz      loc_B0511F
  00B04FC2  lea     eax, [esp+48h+var_28]
  00B04FC6  push    eax
  00B04FC7  call    sub_CA0CE0
  00B04FCC  add     esp, 4
  00B04FCF  mov     ecx, [edi+8]
  00B04FD2  push    offset aProtoAuthClien_1
  00B04FD7  push    ecx
  00B04FD8  push    offset aId
  00B04FDD  push    eax
  00B04FDE  push    esi
  00B04FDF  mov     byte ptr [esp+5Ch+var_4], 1
  00B04FE4  call    sub_B03020
  00B04FE9  add     esp, 8
  00B04FEC  push    eax
  00B04FED  call    sub_41D990
  00B04FF2  add     esp, 8
  00B04FF5  mov     ecx, eax
  00B04FF7  call    sub_ADC810
  00B04FFC  push    eax
  00B04FFD  call    sub_41D990
  00B05002  add     esp, 8
  00B05005  lea     ecx, [esp+48h+var_28]
  00B05009  mov     byte ptr [esp+48h+var_4], 0
  00B0500E  call    sub_B02FF0   ; <<< 提交（C→S 闭合点）
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00B0500E  call    sub_B02FF0
  00B05013  mov     edx, [esp+48h+arg_0]
  00B05017  push    offset word_F641DC
  00B0501C  push    offset asc_EDAD54
  00B05021  push    edx
  00B05022  push    offset aLoginId
  00B05027  push    esi
  00B05028  call    sub_41D990
  00B0502D  add     esp, 8
  00B05030  push    eax
  00B05031  call    sub_41D990
  00B05036  add     esp, 8
  00B05039  push    eax
  00B0503A  call    sub_41D990
  00B0503F  add     esp, 8
  00B05042  push    eax
  00B05043  call    sub_41D990
  00B05048  mov     eax, [esp+50h+arg_4]
  00B0504C  add     esp, 8
  00B0504F  push    offset word_F641DC
  00B05054  push    offset asc_EDAD54
  00B05059  push    eax
  00B0505A  push    offset aLoginPw
  00B0505F  push    esi
  00B05060  call    sub_41D990
  00B05065  add     esp, 8
  00B05068  push    eax
  00B05069  call    sub_41D990
  00B0506E  add     esp, 8
  00B05071  push    eax
  00B05072  call    sub_41D990
  00B05077  add     esp, 8
  00B0507A  push    eax
  00B0507B  call    sub_41D990
  00B05080  mov     ecx, [esp+50h+arg_8]
  00B05084  add     esp, 8
  00B05087  push    offset word_F641DC
  00B0508C  push    offset asc_EDAD54
  00B05091  push    ecx
  00B05092  push    offset aDiskUuid
  00B05097  push    esi
  00B05098  call    sub_41D990
  00B0509D  add     esp, 8
  00B050A0  push    eax
  00B050A1  call    sub_41D990
  00B050A6  add     esp, 8
  00B050A9  push    eax
  00B050AA  call    sub_41D990
  00B050AF  add     esp, 8
  00B050B2  push    eax
  00B050B3  call    sub_41D990
  00B050B8  mov     edx, [esp+50h+arg_C]
  00B050BC  add     esp, 8
  00B050BF  push    offset asc_EDAD54
  00B050C4  push    edx
  00B050C5  push    offset aMacAddr
  00B050CA  push    esi
  00B050CB  call    sub_41D990
  00B050D0  add     esp, 8
  00B050D3  push    eax
  00B050D4  call    sub_41D990
  00B050D9  add     esp, 8
  00B050DC  push    eax
  00B050DD  call    sub_41D990
  00B050E2  add     esp, 8
  00B050E5  push    offset aByte
  00B050EA  mov     eax, ebx
  00B050EC  sub     eax, ebp
  00B050EE  push    eax
  00B050EF  push    offset asc_EDAD58
  00B050F4  push    esi
  00B050F5  call    sub_41D990
  00B050FA  add     esp, 8
  00B050FD  mov     ecx, eax
  00B050FF  call    sub_B03580
  00B05104  push    eax
  00B05105  call    sub_41D990
  00B0510A  add     esp, 8
  00B0510D  mov     esi, eax
  00B0510F  push    0Ah
  00B05111  mov     ecx, esi
  00B05113  call    sub_B036E0
  00B05118  mov     ecx, esi
  00B0511A  call    sub_40DDF0
  00B0511F  mov     edx, [edi]
  00B05121  mov     eax, [edx+58h]
```

## 4. 发送去向切片

```asm
  00B0511F  mov     edx, [edi]
  00B05121  mov     eax, [edx+58h]
  00B05124  sub     ebx, ebp
  00B05126  push    ebx
  00B05127  push    ebp
  00B05128  mov     ecx, edi
  00B0512A  call    eax
  00B0512C  test    al, al
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `00B04F39` | u16 / 2 |
| `login_id` | `0xB04F2E`;`0xB04F43` | str / var |
| `login_pw` | `0xB04F57`;`0xB04F62` | str / var |
| `disk_uuid` | `0xB04F76`;`0xB04F81` | str / var |
| `mac_addr` | `0xB04F95`;`0xB04FA0` | str / var |
