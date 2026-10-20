# 汇编证据 —— CS-0xF24B-lounge-authenticate

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0x00B896A0`（`0x00B896A0`..`0x00B898AD`），函数 `sub_B896A0`
- 命令名字符串：`)<-_proto_lounge_client::send_authenticate(` @ `0x00EEA20C`
- opcode 写入：`0x00B89719`
- 声明容量：`0x32`（分配器容量 `push` @ `0x00B896E3`）
- 提交（`sub_B02FF0`）：`0x00B897A9`
- 发送去向：`vt[0x58]` @ `0x00B8983C`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00B896EC  push    eax
  00B896ED  lea     ecx, [esp+4Ch+var_34]
  00B896F1  call    sub_ABB2F0   ; <<< 初始化 {cur,end}（游标自 buf+2 起）
  00B896F6  lea     ecx, [ebp+32h]
  00B896F9  lea     eax, [ebp+2]
  00B896FC  cmp     eax, ecx
  00B896FE  mov     [esp+48h+var_4], 0
  00B89706  mov     [esp+48h+var_30], ebp
  00B8970A  mov     dword ptr [esp+48h+var_2C], ecx
  00B8970E  ja      loc_B89898
  00B89714  lea     edx, [eax+4]
  00B89717  cmp     edx, ecx
  00B89719  mov     word ptr [ebp+0], 0F24Bh   ; <<< 内联写线（u16）
  00B8971F  ja      loc_B89898
  00B89725  mov     ecx, [esp+48h+arg_0]
  00B89729  mov     [esp+48h+var_30], edx
  00B8972D  push    29h
  00B8972F  lea     edx, [esp+4Ch+var_30]
  00B89733  mov     [eax], ecx   ; <<< 内联写线（u32）
  00B89735  mov     eax, [esp+4Ch+arg_4]
  00B89739  push    edx
  00B8973A  push    eax
  00B8973B  call    sub_B02B40   ; <<< 写线原语 str
  00B89740  add     esp, 0Ch
  00B89743  test    al, al
  00B89745  jz      loc_B89898
  00B8974B  mov     edi, [esi+79B8h]
  00B89751  test    edi, edi
  00B89753  mov     ebx, [esp+48h+var_30]
  00B89757  jz      loc_B8983A
  00B8975D  lea     ecx, [esp+48h+var_28]
  00B89761  push    ecx
  00B89762  call    sub_CA0CE0
  00B89767  add     esp, 4
  00B8976A  mov     edx, [esi+8]
  00B8976D  push    offset aProtoLoungeCli_399
  00B89772  push    edx
  00B89773  push    offset aId
  00B89778  push    eax
  00B89779  push    edi
  00B8977A  mov     byte ptr [esp+5Ch+var_4], 1
  00B8977F  call    sub_B03020
  00B89784  add     esp, 8
  00B89787  push    eax
  00B89788  call    sub_41D990
  00B8978D  add     esp, 8
  00B89790  mov     ecx, eax
  00B89792  call    sub_ADC810
  00B89797  push    eax
  00B89798  call    sub_41D990
  00B8979D  add     esp, 8
  00B897A0  lea     ecx, [esp+48h+var_28]
  00B897A4  mov     byte ptr [esp+48h+var_4], 0
  00B897A9  call    sub_B02FF0   ; <<< 提交（C→S 闭合点）
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00B897A9  call    sub_B02FF0
  00B897AE  mov     eax, [esp+48h+arg_0]
  00B897B2  push    offset word_F641DC
  00B897B7  push    eax
  00B897B8  push    offset aUserid
  00B897BD  push    edi
  00B897BE  call    sub_41D990
  00B897C3  add     esp, 8
  00B897C6  mov     ecx, eax
  00B897C8  call    sub_B03580
  00B897CD  push    eax
  00B897CE  call    sub_41D990
  00B897D3  mov     ecx, [esp+50h+arg_4]
  00B897D7  add     esp, 8
  00B897DA  push    offset asc_EDAD54
  00B897DF  push    ecx
  00B897E0  push    offset aOtp
  00B897E5  push    edi
  00B897E6  call    sub_41D990
  00B897EB  add     esp, 8
  00B897EE  push    eax
  00B897EF  call    sub_41D990
  00B897F4  add     esp, 8
  00B897F7  push    eax
  00B897F8  call    sub_41D990
  00B897FD  add     esp, 8
  00B89800  push    offset aByte
  00B89805  mov     edx, ebx
  00B89807  sub     edx, ebp
  00B89809  push    edx
  00B8980A  push    offset asc_EDAD58
  00B8980F  push    edi
  00B89810  call    sub_41D990
  00B89815  add     esp, 8
  00B89818  mov     ecx, eax
  00B8981A  call    sub_B03580
  00B8981F  push    eax
  00B89820  call    sub_41D990
  00B89825  add     esp, 8
  00B89828  mov     edi, eax
  00B8982A  push    0Ah
  00B8982C  mov     ecx, edi
  00B8982E  call    sub_B036E0
  00B89833  mov     ecx, edi
  00B89835  call    sub_40DDF0
  00B8983A  mov     eax, [esi]
  00B8983C  mov     edx, [eax+58h]
```

## 4. 发送去向切片

```asm
  00B8983A  mov     eax, [esi]
  00B8983C  mov     edx, [eax+58h]
  00B8983F  mov     edi, ebx
  00B89841  sub     edi, ebp
  00B89843  push    edi
  00B89844  push    ebp
  00B89845  mov     ecx, esi
  00B89847  call    edx
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `00B89719` | u16 / 2 |
| `userid` | `0xB89725`;`0xB89733` | u32 / 4 |
| `otp` | `0xB8972D`;`0xB8973B` | str / var |
