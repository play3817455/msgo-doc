# 汇编证据 —— CS-0xF277-lounge-chat_all_up

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0x00B8CE30`（`0x00B8CE30`..`0x00B8D00F`），函数 `sub_B8CE30`
- 命令名字符串：`)<-_proto_lounge_client::send_chat_all_up(` @ `0x00EEA864`
- opcode 写入：`0x00B8CEBC`
- 声明容量：`0xBA`（分配器容量 `push` @ `0x00B8CE76`）
- 提交（`sub_B02FF0`）：`0x00B8CF33`
- 发送去向：`vt[0x58]` @ `0x00B8CF9E`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00B8CE82  push    eax
  00B8CE83  lea     ecx, [esp+4Ch+var_34]
  00B8CE87  call    sub_ABB2F0   ; <<< 初始化 {cur,end}（游标自 buf+2 起）
  00B8CE8C  lea     ecx, [edi+0BAh]
  00B8CE92  lea     eax, [edi+2]
  00B8CE95  cmp     eax, ecx
  00B8CE97  mov     [esp+48h+var_4], 0
  00B8CE9F  mov     [esp+48h+var_30], edi
  00B8CEA3  mov     dword ptr [esp+48h+var_2C], ecx
  00B8CEA7  ja      loc_B8CFFA
  00B8CEAD  mov     edx, [esp+48h+arg_0]
  00B8CEB1  push    0B5h
  00B8CEB6  lea     ecx, [esp+4Ch+var_30]
  00B8CEBA  push    ecx
  00B8CEBB  push    edx
  00B8CEBC  mov     word ptr [edi], 0F277h   ; <<< 内联写线（u16）
  00B8CEC1  mov     [esp+54h+var_30], eax
  00B8CEC5  call    sub_B02B40   ; <<< 写线原语 str
  00B8CECA  add     esp, 0Ch
  00B8CECD  test    al, al
  00B8CECF  jz      loc_B8CFFA
  00B8CED5  mov     ebp, [esi+7AD4h]
  00B8CEDB  test    ebp, ebp
  00B8CEDD  mov     ebx, [esp+48h+var_30]
  00B8CEE1  jz      loc_B8CF9C
  00B8CEE7  lea     eax, [esp+48h+var_28]
  00B8CEEB  push    eax
  00B8CEEC  call    sub_CA0CE0
  00B8CEF1  add     esp, 4
  00B8CEF4  mov     ecx, [esi+8]
  00B8CEF7  push    offset aProtoLoungeCli_411
  00B8CEFC  push    ecx
  00B8CEFD  push    offset aId
  00B8CF02  push    eax
  00B8CF03  push    ebp
  00B8CF04  mov     byte ptr [esp+5Ch+var_4], 1
  00B8CF09  call    sub_B03020
  00B8CF0E  add     esp, 8
  00B8CF11  push    eax
  00B8CF12  call    sub_41D990
  00B8CF17  add     esp, 8
  00B8CF1A  mov     ecx, eax
  00B8CF1C  call    sub_ADC810
  00B8CF21  push    eax
  00B8CF22  call    sub_41D990
  00B8CF27  add     esp, 8
  00B8CF2A  lea     ecx, [esp+48h+var_28]
  00B8CF2E  mov     byte ptr [esp+48h+var_4], 0
  00B8CF33  call    sub_B02FF0   ; <<< 提交（C→S 闭合点）
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00B8CF33  call    sub_B02FF0
  00B8CF38  mov     edx, [esp+48h+arg_0]
  00B8CF3C  push    offset asc_EDAD54
  00B8CF41  push    edx
  00B8CF42  push    offset aMsg
  00B8CF47  push    ebp
  00B8CF48  call    sub_41D990
  00B8CF4D  add     esp, 8
  00B8CF50  push    eax
  00B8CF51  call    sub_41D990
  00B8CF56  add     esp, 8
  00B8CF59  push    eax
  00B8CF5A  call    sub_41D990
  00B8CF5F  add     esp, 8
  00B8CF62  push    offset aByte
  00B8CF67  mov     eax, ebx
  00B8CF69  sub     eax, edi
  00B8CF6B  push    eax
  00B8CF6C  push    offset asc_EDAD58
  00B8CF71  push    ebp
  00B8CF72  call    sub_41D990
  00B8CF77  add     esp, 8
  00B8CF7A  mov     ecx, eax
  00B8CF7C  call    sub_B03580
  00B8CF81  push    eax
  00B8CF82  call    sub_41D990
  00B8CF87  add     esp, 8
  00B8CF8A  mov     ebp, eax
  00B8CF8C  push    0Ah
  00B8CF8E  mov     ecx, ebp
  00B8CF90  call    sub_B036E0
  00B8CF95  mov     ecx, ebp
  00B8CF97  call    sub_40DDF0
  00B8CF9C  mov     edx, [esi]
  00B8CF9E  mov     eax, [edx+58h]
```

## 4. 发送去向切片

```asm
  00B8CF9C  mov     edx, [esi]
  00B8CF9E  mov     eax, [edx+58h]
  00B8CFA1  mov     ebp, ebx
  00B8CFA3  sub     ebp, edi
  00B8CFA5  push    ebp
  00B8CFA6  push    edi
  00B8CFA7  mov     ecx, esi
  00B8CFA9  call    eax
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `00B8CEBC` | u16 / 2 |
| `msg` | `0xB8CEB1`;`0xB8CEC5` | str / var |
