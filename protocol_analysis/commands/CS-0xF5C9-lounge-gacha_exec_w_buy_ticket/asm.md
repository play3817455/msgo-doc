# 汇编证据 —— CS-0xF5C9-lounge-gacha_exec_w_buy_ticket

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0x00B9E240`（`0x00B9E240`..`0x00B9E5CC`），函数 `sub_B9E240`
- 命令名字符串：`)<-_proto_lounge_client::send_gacha_exec_w_buy_ticket(` @ `0x00EEC524`
- opcode 写入：`0x00B9E2BC`
- 声明容量：`0x22`（分配器容量 `push` @ `0x00B9E286`）
- 提交（`sub_B02FF0`）：`0x00B9E3DD`
- 发送去向：`vt[0x58]` @ `0x00B9E558`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00B9E28F  push    eax
  00B9E290  lea     ecx, [esp+4Ch+var_34]
  00B9E294  call    sub_ABB2F0   ; <<< 初始化 {cur,end}（游标自 buf+2 起）
  00B9E299  lea     eax, [ebp+22h]
  00B9E29C  lea     ecx, [ebp+2]
  00B9E29F  cmp     ecx, eax
  00B9E2A1  mov     [esp+48h+var_4], 0
  00B9E2A9  mov     [esp+48h+var_30], ebp
  00B9E2AD  mov     dword ptr [esp+48h+var_2C], eax
  00B9E2B1  ja      loc_B9E5B7
  00B9E2B7  lea     edx, [ecx+4]
  00B9E2BA  cmp     edx, eax
  00B9E2BC  mov     word ptr [ebp+0], 0F5C9h   ; <<< 内联写线（u16）
  00B9E2C2  ja      loc_B9E5B7
  00B9E2C8  mov     esi, dword ptr [esp+48h+arg_0]
  00B9E2CC  mov     [ecx], esi   ; <<< 内联写线（u32）
  00B9E2CE  lea     ecx, [edx+1]
  00B9E2D1  cmp     ecx, eax
  00B9E2D3  ja      loc_B9E5B7
  00B9E2D9  mov     al, byte ptr [esp+48h+arg_4]
  00B9E2DD  mov     [esp+48h+var_30], ecx
  00B9E2E1  lea     ecx, [esp+48h+var_30]
  00B9E2E5  mov     [edx], al   ; <<< 内联写线（u8）
  00B9E2E7  push    ecx
  00B9E2E8  lea     edx, [esp+4Ch+arg_8]
  00B9E2EC  push    edx
  00B9E2ED  call    sub_B02D80   ; <<< 写线原语 u32
  00B9E2F2  add     esp, 8
  00B9E2F5  test    al, al
  00B9E2F7  jz      loc_B9E5B7
  00B9E2FD  lea     eax, [esp+48h+var_30]
  00B9E301  push    eax
  00B9E302  lea     ecx, [esp+4Ch+arg_C]
  00B9E306  push    ecx
  00B9E307  call    sub_B061C0   ; <<< 写线原语 u8
  00B9E30C  add     esp, 8
  00B9E30F  test    al, al
  00B9E311  jz      loc_B9E5B7
  00B9E317  lea     edx, [esp+48h+var_30]
  00B9E31B  push    edx
  00B9E31C  lea     eax, [esp+4Ch+arg_10]
  00B9E320  push    eax
  00B9E321  call    sub_B061C0   ; <<< 写线原语 u8
  00B9E326  add     esp, 8
  00B9E329  test    al, al
  00B9E32B  jz      loc_B9E5B7
  00B9E331  lea     ecx, [esp+48h+var_30]
  00B9E335  push    ecx
  00B9E336  lea     edx, [esp+4Ch+arg_14]
  00B9E33A  push    edx
  00B9E33B  call    sub_B02D80   ; <<< 写线原语 u32
  00B9E340  add     esp, 8
  00B9E343  test    al, al
  00B9E345  jz      loc_B9E5B7
  00B9E34B  lea     eax, [esp+48h+var_30]
  00B9E34F  push    eax
  00B9E350  lea     ecx, [esp+4Ch+arg_18]
  00B9E354  push    ecx
  00B9E355  call    sub_B02D80   ; <<< 写线原语 u32
  00B9E35A  add     esp, 8
  00B9E35D  test    al, al
  00B9E35F  jz      loc_B9E5B7
  00B9E365  lea     edx, [esp+48h+var_30]
  00B9E369  push    edx
  00B9E36A  lea     eax, [esp+4Ch+arg_1C]
  00B9E36E  push    eax
  00B9E36F  call    sub_B061C0   ; <<< 写线原语 u8
  00B9E374  add     esp, 8
  00B9E377  test    al, al
  00B9E379  jz      loc_B9E5B7
  00B9E37F  mov     esi, [edi+7FF8h]
  00B9E385  test    esi, esi
  00B9E387  mov     ebx, [esp+48h+var_30]
  00B9E38B  jz      loc_B9E556
  00B9E391  lea     ecx, [esp+48h+var_28]
  00B9E395  push    ecx
  00B9E396  call    sub_CA0CE0
  00B9E39B  add     esp, 4
  00B9E39E  mov     edx, [edi+8]
  00B9E3A1  push    offset aProtoLoungeCli_403
  00B9E3A6  push    edx
  00B9E3A7  push    offset aId
  00B9E3AC  push    eax
  00B9E3AD  push    esi
  00B9E3AE  mov     byte ptr [esp+5Ch+var_4], 1
  00B9E3B3  call    sub_B03020
  00B9E3B8  add     esp, 8
  00B9E3BB  push    eax
  00B9E3BC  call    sub_41D990
  00B9E3C1  add     esp, 8
  ...（窗口余量略）
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00B9E3DD  call    sub_B02FF0
  00B9E3E2  mov     eax, dword ptr [esp+48h+arg_0]
  00B9E3E6  push    offset word_F641DC
  00B9E3EB  push    eax
  00B9E3EC  push    offset aShopitemid
  00B9E3F1  push    esi
  00B9E3F2  call    sub_41D990
  00B9E3F7  add     esp, 8
  00B9E3FA  mov     ecx, eax
  00B9E3FC  call    sub_B03580
  00B9E401  push    eax
  00B9E402  call    sub_41D990
  00B9E407  add     esp, 8
  00B9E40A  push    offset word_F641DC
  00B9E40F  lea     ecx, [esp+4Ch+arg_4]
  00B9E413  push    ecx
  00B9E414  push    offset aIdType
  00B9E419  push    esi
  00B9E41A  call    sub_41D990
  00B9E41F  add     esp, 8
  00B9E422  push    eax
  00B9E423  call    sub_B0C1F0
  00B9E428  add     esp, 8
  00B9E42B  push    eax
  00B9E42C  call    sub_41D990
  00B9E431  mov     edx, dword ptr [esp+50h+arg_8]
  00B9E435  add     esp, 8
  00B9E438  push    offset word_F641DC
  00B9E43D  push    edx
  00B9E43E  push    offset aNum
  00B9E443  push    esi
  00B9E444  call    sub_41D990
  00B9E449  add     esp, 8
  00B9E44C  mov     ecx, eax
  00B9E44E  call    sub_B03580
  00B9E453  push    eax
  00B9E454  call    sub_41D990
  00B9E459  add     esp, 8
  00B9E45C  push    offset word_F641DC
  00B9E461  lea     eax, [esp+4Ch+arg_C]
  00B9E465  push    eax
  00B9E466  push    offset aTabType
  00B9E46B  push    esi
  00B9E46C  call    sub_41D990
  00B9E471  add     esp, 8
  00B9E474  push    eax
  00B9E475  call    sub_ADCBF0
  00B9E47A  add     esp, 8
  00B9E47D  push    eax
  00B9E47E  call    sub_41D990
  00B9E483  add     esp, 8
  00B9E486  push    offset word_F641DC
  00B9E48B  lea     ecx, [esp+4Ch+arg_10]
  00B9E48F  push    ecx
  00B9E490  push    offset aIsCp
  00B9E495  push    esi
  00B9E496  call    sub_41D990
  00B9E49B  add     esp, 8
  00B9E49E  push    eax
  00B9E49F  call    sub_B0C1F0
  00B9E4A4  add     esp, 8
  00B9E4A7  push    eax
  00B9E4A8  call    sub_41D990
  00B9E4AD  mov     edx, [esp+50h+arg_14]
  00B9E4B1  add     esp, 8
  00B9E4B4  push    offset word_F641DC
  00B9E4B9  push    edx
  00B9E4BA  push    offset aTotalPrice
  00B9E4BF  push    esi
  00B9E4C0  call    sub_41D990
  00B9E4C5  add     esp, 8
  00B9E4C8  mov     ecx, eax
  00B9E4CA  call    sub_B03580
  00B9E4CF  push    eax
  00B9E4D0  call    sub_41D990
  00B9E4D5  mov     eax, dword ptr [esp+50h+arg_18]
  00B9E4D9  add     esp, 8
  00B9E4DC  push    offset word_F641DC
  00B9E4E1  push    eax
  00B9E4E2  push    offset aGachaId
  00B9E4E7  push    esi
  00B9E4E8  call    sub_41D990
  00B9E4ED  add     esp, 8
  00B9E4F0  mov     ecx, eax
  00B9E4F2  call    sub_B03580
  00B9E4F7  push    eax
  00B9E4F8  call    sub_41D990
  00B9E4FD  add     esp, 8
  00B9E500  lea     ecx, [esp+48h+arg_1C]
  00B9E504  push    ecx
  00B9E505  push    offset aIsBundle
  00B9E50A  push    esi
  00B9E50B  call    sub_41D990
  00B9E510  add     esp, 8
  00B9E513  push    eax
  00B9E514  call    sub_B0C1F0
  00B9E519  add     esp, 8
  00B9E51C  push    offset aByte
  00B9E521  mov     edx, ebx
  00B9E523  sub     edx, ebp
  00B9E525  push    edx
  00B9E526  push    offset asc_EDAD58
  00B9E52B  push    esi
  00B9E52C  call    sub_41D990
  00B9E531  add     esp, 8
  00B9E534  mov     ecx, eax
  00B9E536  call    sub_B03580
  00B9E53B  push    eax
  00B9E53C  call    sub_41D990
  00B9E541  add     esp, 8
  00B9E544  mov     esi, eax
  00B9E546  push    0Ah
  00B9E548  mov     ecx, esi
  00B9E54A  call    sub_B036E0
  00B9E54F  mov     ecx, esi
  00B9E551  call    sub_40DDF0
  00B9E556  mov     eax, [edi]
  00B9E558  mov     edx, [eax+58h]
```

## 4. 发送去向切片

```asm
  00B9E556  mov     eax, [edi]
  00B9E558  mov     edx, [eax+58h]
  00B9E55B  mov     esi, ebx
  00B9E55D  sub     esi, ebp
  00B9E55F  push    esi
  00B9E560  push    ebp
  00B9E561  mov     ecx, edi
  00B9E563  call    edx
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `00B9E2BC` | u16 / 2 |
| `shopitemid` | `0xB9E2C8`;`0xB9E2CC` | u32 / 4 |
| `id_type` | `0xB9E2D9`;`0xB9E2E5` | u8 / 1 |
| `num` | `0xB9E2ED` | u32 / 4 |
| `tab_type` | `0xB9E307` | u8 / 1 |
| `is_cp` | `0xB9E321` | u8 / 1 |
| `total_price` | `0xB9E33B` | u32 / 4 |
| `gacha_id` | `0xB9E355` | u32 / 4 |
| `is_bundle` | `0xB9E36F` | u8 / 1 |
