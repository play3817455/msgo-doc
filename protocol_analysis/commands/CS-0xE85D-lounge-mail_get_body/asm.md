# 汇编证据 —— CS-0xE85D-lounge-mail_get_body

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0x00B9C110`（`0x00B9C110`..`0x00B9C316`），函数 `sub_B9C110`
- 命令名字符串：`)<-_proto_lounge_client::send_mail_get_body(` @ `0x00EEC224`
- opcode 写入：`0x00B9C18C`
- 声明容量：`0xE`（分配器容量 `push` @ `0x00B9C156`）
- 提交（`sub_B02FF0`）：`0x00B9C21A`
- 发送去向：`vt[0x58]` @ `0x00B9C2A2`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00B9C15F  push    eax
  00B9C160  lea     ecx, [esp+4Ch+var_34]
  00B9C164  call    sub_ABB2F0   ; <<< 初始化 {cur,end}（游标自 buf+2 起）
  00B9C169  lea     ecx, [ebp+0Eh]
  00B9C16C  lea     eax, [ebp+2]
  00B9C16F  cmp     eax, ecx
  00B9C171  mov     [esp+48h+var_4], 0
  00B9C179  mov     [esp+48h+var_30], ebp
  00B9C17D  mov     dword ptr [esp+48h+var_2C], ecx
  00B9C181  ja      loc_B9C301
  00B9C187  lea     edx, [eax+4]
  00B9C18A  cmp     edx, ecx
  00B9C18C  mov     word ptr [ebp+0], 0E85Dh   ; <<< 内联写线（u16）
  00B9C192  ja      loc_B9C301
  00B9C198  mov     ecx, [esp+48h+arg_0]
  00B9C19C  mov     [esp+48h+var_30], edx
  00B9C1A0  lea     edx, [esp+48h+var_30]
  00B9C1A4  mov     [eax], ecx   ; <<< 内联写线（u32）
  00B9C1A6  push    edx
  00B9C1A7  lea     eax, [esp+4Ch+arg_4]
  00B9C1AB  push    eax
  00B9C1AC  call    sub_B06190   ; <<< 写线原语 u64
  00B9C1B1  add     esp, 8
  00B9C1B4  test    al, al
  00B9C1B6  jz      loc_B9C301
  00B9C1BC  mov     edi, [esi+7F60h]
  00B9C1C2  test    edi, edi
  00B9C1C4  mov     ebx, [esp+48h+var_30]
  00B9C1C8  jz      loc_B9C2A0
  00B9C1CE  lea     ecx, [esp+48h+var_28]
  00B9C1D2  push    ecx
  00B9C1D3  call    sub_CA0CE0
  00B9C1D8  add     esp, 4
  00B9C1DB  mov     edx, [esi+8]
  00B9C1DE  push    offset aProtoLoungeCli_549
  00B9C1E3  push    edx
  00B9C1E4  push    offset aId
  00B9C1E9  push    eax
  00B9C1EA  push    edi
  00B9C1EB  mov     byte ptr [esp+5Ch+var_4], 1
  00B9C1F0  call    sub_B03020
  00B9C1F5  add     esp, 8
  00B9C1F8  push    eax
  00B9C1F9  call    sub_41D990
  00B9C1FE  add     esp, 8
  00B9C201  mov     ecx, eax
  00B9C203  call    sub_ADC810
  00B9C208  push    eax
  00B9C209  call    sub_41D990
  00B9C20E  add     esp, 8
  00B9C211  lea     ecx, [esp+48h+var_28]
  00B9C215  mov     byte ptr [esp+48h+var_4], 0
  00B9C21A  call    sub_B02FF0   ; <<< 提交（C→S 闭合点）
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00B9C21A  call    sub_B02FF0
  00B9C21F  mov     eax, [esp+48h+arg_0]
  00B9C223  push    offset word_F641DC
  00B9C228  push    eax
  00B9C229  push    offset aBoxType
  00B9C22E  push    edi
  00B9C22F  call    sub_41D990
  00B9C234  add     esp, 8
  00B9C237  mov     ecx, eax
  00B9C239  call    sub_B03580
  00B9C23E  push    eax
  00B9C23F  call    sub_41D990
  00B9C244  mov     ecx, [esp+50h+arg_8]
  00B9C248  mov     edx, [esp+50h+arg_4]
  00B9C24C  add     esp, 8
  00B9C24F  push    ecx
  00B9C250  push    edx
  00B9C251  push    offset aMailid
  00B9C256  push    edi
  00B9C257  call    sub_41D990
  00B9C25C  add     esp, 8
  00B9C25F  mov     ecx, eax
  00B9C261  call    sub_B08500
  00B9C266  push    offset aByte
  00B9C26B  mov     eax, ebx
  00B9C26D  sub     eax, ebp
  00B9C26F  push    eax
  00B9C270  push    offset asc_EDAD58
  00B9C275  push    edi
  00B9C276  call    sub_41D990
  00B9C27B  add     esp, 8
  00B9C27E  mov     ecx, eax
  00B9C280  call    sub_B03580
  00B9C285  push    eax
  00B9C286  call    sub_41D990
  00B9C28B  add     esp, 8
  00B9C28E  mov     edi, eax
  00B9C290  push    0Ah
  00B9C292  mov     ecx, edi
  00B9C294  call    sub_B036E0
  00B9C299  mov     ecx, edi
  00B9C29B  call    sub_40DDF0
  00B9C2A0  mov     edx, [esi]
  00B9C2A2  mov     eax, [edx+58h]
```

## 4. 发送去向切片

```asm
  00B9C2A0  mov     edx, [esi]
  00B9C2A2  mov     eax, [edx+58h]
  00B9C2A5  mov     edi, ebx
  00B9C2A7  sub     edi, ebp
  00B9C2A9  push    edi
  00B9C2AA  push    ebp
  00B9C2AB  mov     ecx, esi
  00B9C2AD  call    eax
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `00B9C18C` | u16 / 2 |
| `box_type` | `0xB9C1A4` | u32 / 4 |
| `mailid` | `0xB9C1AC` | u64 / 8 |
