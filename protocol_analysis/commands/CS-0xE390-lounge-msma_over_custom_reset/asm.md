# 汇编证据 —— CS-0xE390-lounge-msma_over_custom_reset

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0x00BA82F0`（`0x00BA82F0`..`0x00BA84A9`），函数 `sub_BA82F0`
- 命令名字符串：`)<-_proto_lounge_client::send_msma_over_custom_reset(` @ `0x00EED64C`
- opcode 写入：`0x00BA8364`
- 声明容量：`0xA`（分配器容量 `push` @ `0x00BA8336`）
- 提交（`sub_B02FF0`）：`0x00BA83D7`
- 发送去向：`vt[0x58]` @ `0x00BA8437`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00BA833F  push    eax
  00BA8340  lea     ecx, [esp+44h+var_2C]
  00BA8344  call    sub_ABB2F0   ; <<< 初始化 {cur,end}（游标自 buf+2 起）
  00BA8349  lea     ecx, [ebp+0Ah]
  00BA834C  lea     eax, [ebp+2]
  00BA834F  cmp     eax, ecx
  00BA8351  mov     [esp+40h+var_4], 0
  00BA8359  ja      loc_BA8494
  00BA835F  lea     ebx, [eax+8]
  00BA8362  cmp     ebx, ecx
  00BA8364  mov     word ptr [ebp+0], 0E390h   ; <<< 内联写线（u16）
  00BA836A  ja      loc_BA8494
  00BA8370  mov     ecx, [esp+40h+arg_0]
  00BA8374  mov     edx, [esp+40h+arg_4]
  00BA8378  mov     [eax], ecx   ; <<< 内联写线（u32）
  00BA837A  mov     [eax+4], edx   ; <<< 内联写线（u32）
  00BA837D  mov     edi, [esi+833Ch]
  00BA8383  test    edi, edi
  00BA8385  jz      loc_BA8435
  00BA838B  lea     eax, [esp+40h+var_28]
  00BA838F  push    eax
  00BA8390  call    sub_CA0CE0
  00BA8395  add     esp, 4
  00BA8398  mov     ecx, [esi+8]
  00BA839B  push    offset aProtoLoungeCli_465
  00BA83A0  push    ecx
  00BA83A1  push    offset aId
  00BA83A6  push    eax
  00BA83A7  push    edi
  00BA83A8  mov     byte ptr [esp+54h+var_4], 1
  00BA83AD  call    sub_B03020
  00BA83B2  add     esp, 8
  00BA83B5  push    eax
  00BA83B6  call    sub_41D990
  00BA83BB  add     esp, 8
  00BA83BE  mov     ecx, eax
  00BA83C0  call    sub_ADC810
  00BA83C5  push    eax
  00BA83C6  call    sub_41D990
  00BA83CB  add     esp, 8
  00BA83CE  lea     ecx, [esp+40h+var_28]
  00BA83D2  mov     byte ptr [esp+40h+var_4], 0
  00BA83D7  call    sub_B02FF0   ; <<< 提交（C→S 闭合点）
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00BA83D7  call    sub_B02FF0
  00BA83DC  mov     edx, [esp+40h+arg_4]
  00BA83E0  mov     eax, [esp+40h+arg_0]
  00BA83E4  push    edx
  00BA83E5  push    eax
  00BA83E6  push    offset aUniqMsid
  00BA83EB  push    edi
  00BA83EC  call    sub_41D990
  00BA83F1  add     esp, 8
  00BA83F4  mov     ecx, eax
  00BA83F6  call    sub_B08500
  00BA83FB  push    offset aByte
  00BA8400  mov     ecx, ebx
  00BA8402  sub     ecx, ebp
  00BA8404  push    ecx
  00BA8405  push    offset asc_EDAD58
  00BA840A  push    edi
  00BA840B  call    sub_41D990
  00BA8410  add     esp, 8
  00BA8413  mov     ecx, eax
  00BA8415  call    sub_B03580
  00BA841A  push    eax
  00BA841B  call    sub_41D990
  00BA8420  add     esp, 8
  00BA8423  mov     edi, eax
  00BA8425  push    0Ah
  00BA8427  mov     ecx, edi
  00BA8429  call    sub_B036E0
  00BA842E  mov     ecx, edi
  00BA8430  call    sub_40DDF0
  00BA8435  mov     edx, [esi]
  00BA8437  mov     eax, [edx+58h]
```

## 4. 发送去向切片

```asm
  00BA8435  mov     edx, [esi]
  00BA8437  mov     eax, [edx+58h]
  00BA843A  sub     ebx, ebp
  00BA843C  push    ebx
  00BA843D  push    ebp
  00BA843E  mov     ecx, esi
  00BA8440  call    eax
  00BA8442  test    al, al
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `00BA8364` | u16 / 2 |
| `uniq_msid` | `0xBA8378`;`0xBA837A` | u64 / 8 |
