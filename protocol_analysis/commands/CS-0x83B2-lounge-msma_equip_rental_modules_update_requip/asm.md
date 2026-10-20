# 汇编证据 —— CS-0x83B2-lounge-msma_equip_rental_modules_update_requip

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B947B0 @ `0xb947b0`（`0xb947b0`..`0xb94a10`）
- 命令名字符串：`)<-_proto_lounge_client::send_msma_equip_rental_modules_update_requip(` @ `0xeeb5d8`
- opcode 写入：`0xb94832`
- 声明容量：`0x12C6`（分配器容量 `push` @ `0xb947fa`）

## 2. 组包块切片（游标初始化 → 逐字段写线 → 提交）

```asm
  0xb94801  mov     esi, eax
  0xb94803  mov     eax, [ebp+0Ch]
  0xb94806  push    eax
  0xb94807  lea     ecx, [esp+4Ch+var_34]
  0xb9480b  mov     [esp+4Ch+var_30], esi
  0xb9480f  call    sub_ABB2F0
  0xb94814  lea     edx, [esi+12C6h]
  0xb9481a  lea     eax, [esi+2]
  0xb9481d  cmp     eax, edx
  0xb9481f  mov     [esp+48h+var_4], 0
  0xb94827  ja      loc_B949FB
  0xb9482d  lea     ebx, [eax+4]
  0xb94830  cmp     ebx, edx
  0xb94832  mov     word ptr [esi], 83B2h
  0xb94837  ja      loc_B949FB
  0xb9483d  mov     esi, [esp+48h+arg_4]
  0xb94841  test    esi, esi
  0xb94843  mov     ecx, [esp+48h+arg_0]
  0xb94847  mov     [eax], ecx
  0xb94849  jz      loc_B949FB
  0xb9484f  xor     eax, eax
  0xb94851  lea     ecx, [ebx+8]
  0xb94854  cmp     ecx, edx
  0xb94856  ja      loc_B949FB
  0xb9485c  mov     edi, [esi+eax*8]
  0xb9485f  mov     [ebx], edi
  0xb94861  mov     edi, [esi+eax*8+4]
  0xb94865  mov     [ebx+4], edi
  0xb94868  add     eax, 1
  0xb9486b  add     ebx, 8
  0xb9486e  add     ecx, 8
  0xb94871  cmp     eax, 258h
  0xb94876  jb      short loc_B94854
  0xb94878  mov     edi, [ebp+7D5Ch]
  0xb9487e  test    edi, edi
  0xb94880  jz      loc_B94997
  0xb94886  lea     edx, [esp+48h+var_28]
  0xb9488a  push    edx
  0xb9488b  call    sub_CA0CE0
  0xb94890  add     esp, 4
  0xb94893  mov     ecx, [ebp+8]
  0xb94896  push    offset aProtoLoungeCli_467; ")<-_proto_lounge_client::send_msma_equi"...
  0xb9489b  push    ecx
  0xb9489c  push    offset aId; " (id:"
  0xb948a1  push    eax
  0xb948a2  push    edi
  0xb948a3  mov     byte ptr [esp+5Ch+var_4], 1
  0xb948a8  call    sub_B03020
  0xb948ad  add     esp, 8
  0xb948b0  push    eax
  0xb948b1  call    sub_41D990
  0xb948b6  add     esp, 8
  0xb948b9  mov     ecx, eax
  0xb948bb  call    sub_ADC810
  0xb948c0  push    eax
  0xb948c1  call    sub_41D990
  0xb948c6  add     esp, 8
  0xb948c9  lea     ecx, [esp+48h+var_28]
  0xb948cd  mov     byte ptr [esp+48h+var_4], 0
  0xb948d2  call    sub_B02FF0
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。
> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B02B40`=写 NUL 串（其**紧邻之前的 `push N`** = 串槽预算）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb948e1  push    offset aModuleId; "module_id="
  0xb948fc  push    offset aMsidList; "msid_list={"
  0xb9495d  push    offset aByte; "]byte"
  0xb94963  push    offset asc_EDAD58; " ) ["
```

## 4. 发送去向切片

```asm
  0xb94871  cmp     eax, 258h
  0xb94941  cmp     ebp, 258h
  0xb9499e  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xb94832` | u16 |
| `module_id` | `0xB94847` | u32 |
| `msid_list` | `0xB9485F, 0xB94865 (loop @0xB94854..0xB94876)` | u64[600] |
