# 汇编证据 —— CS-0xE410-lounge-msma_equipset_del

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0x00B994C0`（`0x00B994C0`..`0x00B996B4`），函数 `sub_B994C0`
- 命令名字符串：`)<-_proto_lounge_client::send_msma_equipset_del(` @ `0x00EEBD54`
- opcode 写入：`0x00B99534`
- 声明容量：`0xE`（分配器容量 `push` @ `0x00B99506`）
- 提交（`sub_B02FF0`）：`0x00B995BA`
- 发送去向：`vt[0x58]` @ `0x00B99642`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00B9950F  push    eax
  00B99510  lea     ecx, [esp+44h+var_2C]
  00B99514  call    sub_ABB2F0   ; <<< 初始化 {cur,end}（游标自 buf+2 起）
  00B99519  lea     ecx, [ebp+0Eh]
  00B9951C  lea     eax, [ebp+2]
  00B9951F  cmp     eax, ecx
  00B99521  mov     [esp+40h+var_4], 0
  00B99529  ja      loc_B9969F
  00B9952F  lea     edx, [eax+8]
  00B99532  cmp     edx, ecx
  00B99534  mov     word ptr [ebp+0], 0E410h   ; <<< 内联写线（u16）
  00B9953A  ja      loc_B9969F
  00B99540  mov     esi, [esp+40h+arg_0]
  00B99544  mov     [eax], esi   ; <<< 内联写线（u32）
  00B99546  mov     esi, [esp+40h+arg_4]
  00B9954A  lea     ebx, [edx+2]
  00B9954D  cmp     ebx, ecx
  00B9954F  mov     [eax+4], esi   ; <<< 内联写线（u32）
  00B99552  ja      loc_B9969F
  00B99558  mov     cx, word ptr [esp+40h+arg_8]
  00B9955D  mov     [edx], cx   ; <<< 内联写线（u16）
  00B99560  mov     esi, [edi+7E84h]
  00B99566  test    esi, esi
  00B99568  jz      loc_B99640
  00B9956E  lea     edx, [esp+40h+var_28]
  00B99572  push    edx
  00B99573  call    sub_CA0CE0
  00B99578  add     esp, 4
  00B9957B  mov     ecx, [edi+8]
  00B9957E  push    offset aProtoLoungeCli_440
  00B99583  push    ecx
  00B99584  push    offset aId
  00B99589  push    eax
  00B9958A  push    esi
  00B9958B  mov     byte ptr [esp+54h+var_4], 1
  00B99590  call    sub_B03020
  00B99595  add     esp, 8
  00B99598  push    eax
  00B99599  call    sub_41D990
  00B9959E  add     esp, 8
  00B995A1  mov     ecx, eax
  00B995A3  call    sub_ADC810
  00B995A8  push    eax
  00B995A9  call    sub_41D990
  00B995AE  add     esp, 8
  00B995B1  lea     ecx, [esp+40h+var_28]
  00B995B5  mov     byte ptr [esp+40h+var_4], 0
  00B995BA  call    sub_B02FF0   ; <<< 提交（C→S 闭合点）
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00B995BA  call    sub_B02FF0
  00B995BF  mov     edx, [esp+40h+arg_4]
  00B995C3  mov     eax, [esp+40h+arg_0]
  00B995C7  push    offset word_F641DC
  00B995CC  push    edx
  00B995CD  push    eax
  00B995CE  push    offset aUniqidMs
  00B995D3  push    esi
  00B995D4  call    sub_41D990
  00B995D9  add     esp, 8
  00B995DC  mov     ecx, eax
  00B995DE  call    sub_B08500
  00B995E3  push    eax
  00B995E4  call    sub_41D990
  00B995E9  mov     ecx, [esp+48h+arg_8]
  00B995ED  add     esp, 8
  00B995F0  push    ecx
  00B995F1  push    offset aSlot
  00B995F6  push    esi
  00B995F7  call    sub_41D990
  00B995FC  add     esp, 8
  00B995FF  mov     ecx, eax
  00B99601  call    sub_B032A0
  00B99606  push    offset aByte
  00B9960B  mov     edx, ebx
  00B9960D  sub     edx, ebp
  00B9960F  push    edx
  00B99610  push    offset asc_EDAD58
  00B99615  push    esi
  00B99616  call    sub_41D990
  00B9961B  add     esp, 8
  00B9961E  mov     ecx, eax
  00B99620  call    sub_B03580
  00B99625  push    eax
  00B99626  call    sub_41D990
  00B9962B  add     esp, 8
  00B9962E  mov     esi, eax
  00B99630  push    0Ah
  00B99632  mov     ecx, esi
  00B99634  call    sub_B036E0
  00B99639  mov     ecx, esi
  00B9963B  call    sub_40DDF0
  00B99640  mov     eax, [edi]
  00B99642  mov     edx, [eax+58h]
```

## 4. 发送去向切片

```asm
  00B99640  mov     eax, [edi]
  00B99642  mov     edx, [eax+58h]
  00B99645  sub     ebx, ebp
  00B99647  push    ebx
  00B99648  push    ebp
  00B99649  mov     ecx, edi
  00B9964B  call    edx
  00B9964D  test    al, al
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `00B99534` | u16 / 2 |
| `uniqid_ms` | `0xB99544`;`0xB9954F` | u64 / 8 |
| `slot` | `0xB9955D` | u16 / 2 |
