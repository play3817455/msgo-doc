# 汇编证据 —— CS-0x50D8-lounge-clan_shop_buy

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_BA3280 @ `0xba3280`（`0xba3280`..`0xba34ba`）
- 命令名字符串：`)<-_proto_lounge_client::send_clan_shop_buy(` @ `0xeecd90`
- opcode 写入：`0xba32fc`
- 声明容量：`0xE`

## 2. 组包块切片（游标初始化 → 提交）

```asm
  0xba32ca  mov     ebp, eax
  0xba32cc  mov     eax, [edi+0Ch]
  0xba32cf  push    eax
  0xba32d0  lea     ecx, [esp+4Ch+var_34]
  0xba32d4  call    sub_ABB2F0
  0xba32d9  lea     ecx, [ebp+0Eh]
  0xba32dc  lea     eax, [ebp+2]
  0xba32df  cmp     eax, ecx
  0xba32e1  mov     [esp+48h+var_4], 0
  0xba32e9  mov     [esp+48h+var_30], ebp
  0xba32ed  mov     dword ptr [esp+48h+var_2C], ecx
  0xba32f1  ja      loc_BA34A5
  0xba32f7  lea     edx, [eax+4]
  0xba32fa  cmp     edx, ecx
  0xba32fc  mov     word ptr [ebp+0], 50D8h
  0xba3302  ja      loc_BA34A5
  0xba3308  mov     esi, [esp+48h+arg_0]
  0xba330c  mov     [eax], esi
  0xba330e  mov     eax, edx
  0xba3310  lea     edx, [eax+4]
  0xba3313  cmp     edx, ecx
  0xba3315  ja      loc_BA34A5
  0xba331b  mov     ecx, [esp+48h+arg_4]
  0xba331f  mov     [esp+48h+var_30], edx
  0xba3323  lea     edx, [esp+48h+var_30]
  0xba3327  mov     [eax], ecx
  0xba3329  push    edx
  0xba332a  lea     eax, [esp+4Ch+arg_8]
  0xba332e  push    eax
  0xba332f  call    sub_B02D80
  0xba3334  add     esp, 8
  0xba3337  test    al, al
  0xba3339  jz      loc_BA34A5
  0xba333f  mov     esi, [edi+815Ch]
  0xba3345  test    esi, esi
  0xba3347  mov     ebx, [esp+48h+var_30]
  0xba334b  jz      loc_BA3446
  0xba3351  lea     ecx, [esp+48h+var_28]
  0xba3355  push    ecx
  0xba3356  call    sub_CA0CE0
  0xba335b  add     esp, 4
  0xba335e  mov     edx, [edi+8]
  0xba3361  push    offset aProtoLoungeCli_532; ")<-_proto_lounge_client::send_clan_shop"...
  0xba3366  push    edx
  0xba3367  push    offset aId; " (id:"
  0xba336c  push    eax
  0xba336d  push    esi
  0xba336e  mov     byte ptr [esp+5Ch+var_4], 1
  0xba3373  call    sub_B03020
  0xba3378  add     esp, 8
  0xba337b  push    eax
  0xba337c  call    sub_41D990
  0xba3381  add     esp, 8
  0xba3384  mov     ecx, eax
  0xba3386  call    sub_ADC810
  0xba338b  push    eax
  0xba338c  call    sub_41D990
  0xba3391  add     esp, 8
  0xba3394  lea     ecx, [esp+48h+var_28]
  0xba3398  mov     byte ptr [esp+48h+var_4], 0
  0xba339d  call    sub_B02FF0   <<<COMMIT
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xba33ac  push    offset aShopitemid; "shopitemid="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xba33d4  push    offset aNum; "num="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xba33f7  push    offset aTotalPrice; "total_price="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xba340c  push    offset aByte; "]byte"
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
```

## 4. 发送去向切片

```asm
  0xba3448  mov     eax, [edx+58h]
  0xba344b  sub     ebx, ebp
  0xba344d  push    ebx
  0xba344e  push    ebp
  0xba344f  mov     ecx, edi
  0xba3451  call    eax
  0xba3453  test    al, al
  0xba3455  jz      short loc_BA34A5
  0xba3457  mov     eax, [edi+79A8h]
  0xba345d  test    eax, eax
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。
> 本批 50 条**全部命中同一去向槽 `vt[0x58]`**（与批次-16/17 一致）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xBA32FC` | u16 |
| `shopitemid` | `0xBA330C` | u32 |
| `num` | `0xBA3327` | u32 |
| `total_price` | `0xBA332F` | u32 |
