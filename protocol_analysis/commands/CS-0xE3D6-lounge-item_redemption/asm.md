# 汇编证据 —— CS-0xE3D6-lounge-item_redemption

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0x00B9A4E0`（`0x00B9A4E0`..`0x00B9A726`），函数 `sub_B9A4E0`
- 命令名字符串：`)<-_proto_lounge_client::send_item_redemption(` @ `0x00EEBF38`
- opcode 写入：`0x00B9A55C`
- 声明容量：`0x12`（分配器容量 `push` @ `0x00B9A526`）
- 提交（`sub_B02FF0`）：`0x00B9A604`
- 发送去向：`vt[0x58]` @ `0x00B9A6B4`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00B9A52F  push    eax
  00B9A530  lea     ecx, [esp+4Ch+var_34]
  00B9A534  call    sub_ABB2F0   ; <<< 初始化 {cur,end}（游标自 buf+2 起）
  00B9A539  lea     ecx, [ebp+12h]
  00B9A53C  lea     eax, [ebp+2]
  00B9A53F  cmp     eax, ecx
  00B9A541  mov     [esp+48h+var_4], 0
  00B9A549  mov     [esp+48h+var_30], ebp
  00B9A54D  mov     dword ptr [esp+48h+var_2C], ecx
  00B9A551  ja      loc_B9A711
  00B9A557  lea     edx, [eax+8]
  00B9A55A  cmp     edx, ecx
  00B9A55C  mov     word ptr [ebp+0], 0E3D6h   ; <<< 内联写线（u16）
  00B9A562  ja      loc_B9A711
  00B9A568  mov     esi, [esp+48h+arg_0]
  00B9A56C  mov     [eax], esi   ; <<< 内联写线（u32）
  00B9A56E  mov     esi, [esp+48h+arg_4]
  00B9A572  mov     [eax+4], esi   ; <<< 内联写线（u32）
  00B9A575  lea     eax, [edx+2]
  00B9A578  cmp     eax, ecx
  00B9A57A  ja      loc_B9A711
  00B9A580  mov     cx, word ptr [esp+48h+arg_8]
  00B9A585  mov     [edx], cx   ; <<< 内联写线（u16）
  00B9A588  lea     edx, [esp+48h+var_30]
  00B9A58C  mov     [esp+48h+var_30], eax
  00B9A590  push    edx
  00B9A591  lea     eax, [esp+4Ch+arg_C]
  00B9A595  push    eax
  00B9A596  call    sub_B02D80   ; <<< 写线原语 u32
  00B9A59B  add     esp, 8
  00B9A59E  test    al, al
  00B9A5A0  jz      loc_B9A711
  00B9A5A6  mov     esi, [edi+7EDCh]
  00B9A5AC  test    esi, esi
  00B9A5AE  mov     ebx, [esp+48h+var_30]
  00B9A5B2  jz      loc_B9A6B2
  00B9A5B8  lea     ecx, [esp+48h+var_28]
  00B9A5BC  push    ecx
  00B9A5BD  call    sub_CA0CE0
  00B9A5C2  add     esp, 4
  00B9A5C5  mov     edx, [edi+8]
  00B9A5C8  push    offset aProtoLoungeCli_572
  00B9A5CD  push    edx
  00B9A5CE  push    offset aId
  00B9A5D3  push    eax
  00B9A5D4  push    esi
  00B9A5D5  mov     byte ptr [esp+5Ch+var_4], 1
  00B9A5DA  call    sub_B03020
  00B9A5DF  add     esp, 8
  00B9A5E2  push    eax
  00B9A5E3  call    sub_41D990
  00B9A5E8  add     esp, 8
  00B9A5EB  mov     ecx, eax
  00B9A5ED  call    sub_ADC810
  00B9A5F2  push    eax
  00B9A5F3  call    sub_41D990
  00B9A5F8  add     esp, 8
  00B9A5FB  lea     ecx, [esp+48h+var_28]
  00B9A5FF  mov     byte ptr [esp+48h+var_4], 0
  00B9A604  call    sub_B02FF0   ; <<< 提交（C→S 闭合点）
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00B9A604  call    sub_B02FF0
  00B9A609  mov     eax, [esp+48h+arg_4]
  00B9A60D  mov     ecx, [esp+48h+arg_0]
  00B9A611  push    offset word_F641DC
  00B9A616  push    eax
  00B9A617  push    ecx
  00B9A618  push    offset aUniqid
  00B9A61D  push    esi
  00B9A61E  call    sub_41D990
  00B9A623  add     esp, 8
  00B9A626  mov     ecx, eax
  00B9A628  call    sub_B08500
  00B9A62D  push    eax
  00B9A62E  call    sub_41D990
  00B9A633  mov     edx, [esp+50h+arg_8]
  00B9A637  add     esp, 8
  00B9A63A  push    offset word_F641DC
  00B9A63F  push    edx
  00B9A640  push    offset aNum
  00B9A645  push    esi
  00B9A646  call    sub_41D990
  00B9A64B  add     esp, 8
  00B9A64E  mov     ecx, eax
  00B9A650  call    sub_B032A0
  00B9A655  push    eax
  00B9A656  call    sub_41D990
  00B9A65B  mov     eax, [esp+50h+arg_C]
  00B9A65F  add     esp, 8
  00B9A662  push    eax
  00B9A663  push    offset aTotalPrice
  00B9A668  push    esi
  00B9A669  call    sub_41D990
  00B9A66E  add     esp, 8
  00B9A671  mov     ecx, eax
  00B9A673  call    sub_B03580
  00B9A678  push    offset aByte
  00B9A67D  mov     ecx, ebx
  00B9A67F  sub     ecx, ebp
  00B9A681  push    ecx
  00B9A682  push    offset asc_EDAD58
  00B9A687  push    esi
  00B9A688  call    sub_41D990
  00B9A68D  add     esp, 8
  00B9A690  mov     ecx, eax
  00B9A692  call    sub_B03580
  00B9A697  push    eax
  00B9A698  call    sub_41D990
  00B9A69D  add     esp, 8
  00B9A6A0  mov     esi, eax
  00B9A6A2  push    0Ah
  00B9A6A4  mov     ecx, esi
  00B9A6A6  call    sub_B036E0
  00B9A6AB  mov     ecx, esi
  00B9A6AD  call    sub_40DDF0
  00B9A6B2  mov     edx, [edi]
  00B9A6B4  mov     eax, [edx+58h]
```

## 4. 发送去向切片

```asm
  00B9A6B2  mov     edx, [edi]
  00B9A6B4  mov     eax, [edx+58h]
  00B9A6B7  sub     ebx, ebp
  00B9A6B9  push    ebx
  00B9A6BA  push    ebp
  00B9A6BB  mov     ecx, edi
  00B9A6BD  call    eax
  00B9A6BF  test    al, al
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `00B9A55C` | u16 / 2 |
| `uniqid` | `0xB9A56C`;`0xB9A572` | u64 / 8 |
| `num` | `0xB9A585` | u16 / 2 |
| `total_price` | `0xB9A596` | u32 / 4 |
