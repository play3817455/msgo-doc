# 汇编证据 —— CS-0x60D6-lounge-msma_equip_bonus_modules_lot_update

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B94280 @ `0xb94280`（`0xb94280`..`0xb944a0`）
- 命令名字符串：`)<-_proto_lounge_client::send_msma_equip_bonus_modules_lot_update(` @ `0xeeb548`
- opcode 写入：`0xb942f4`
- 声明容量：`0xE`

## 2. 组包块切片（游标初始化 → 提交）

```asm
  0xb942ca  mov     ebx, eax
  0xb942cc  mov     eax, [ebp+0Ch]
  0xb942cf  push    eax
  0xb942d0  lea     ecx, [esp+44h+var_2C]
  0xb942d4  call    sub_ABB2F0
  0xb942d9  lea     ecx, [ebx+0Eh]
  0xb942dc  lea     eax, [ebx+2]
  0xb942df  cmp     eax, ecx
  0xb942e1  mov     [esp+40h+var_4], 0
  0xb942e9  ja      loc_B9448B
  0xb942ef  lea     edi, [eax+8]
  0xb942f2  cmp     edi, ecx
  0xb942f4  mov     word ptr [ebx], 60D6h
  0xb942f9  ja      loc_B9448B
  0xb942ff  mov     ecx, [esp+40h+arg_0]
  0xb94303  mov     edx, [esp+40h+arg_4]
  0xb94307  mov     [eax], ecx
  0xb94309  mov     [eax+4], edx
  0xb9430c  mov     edx, [esp+40h+arg_8]
  0xb94310  test    edx, edx
  0xb94312  jz      loc_B9448B
  0xb94318  xor     eax, eax
  0xb9431a  lea     ecx, [edi+4]
  0xb9431d  lea     ecx, [ecx+0]
  0xb94320  lea     esi, [ebx+0Eh]
  0xb94323  cmp     ecx, esi
  0xb94325  ja      loc_B9448B
  0xb9432b  mov     esi, [edx+eax*4]
  0xb9432e  mov     [edi], esi
  0xb94330  add     eax, 1
  0xb94333  add     edi, 4
  0xb94336  add     ecx, 4
  0xb94339  cmp     eax, 1
  0xb9433c  jb      short loc_B94320
  0xb9433e  mov     esi, [ebp+7D4Ch]
  0xb94344  test    esi, esi
  0xb94346  jz      loc_B9442B
  0xb9434c  lea     eax, [esp+40h+var_28]
  0xb94350  push    eax
  0xb94351  call    sub_CA0CE0
  0xb94356  add     esp, 4
  0xb94359  mov     ecx, [ebp+8]
  0xb9435c  push    offset aProtoLoungeCli_433; ")<-_proto_lounge_client::send_msma_equi"...
  0xb94361  push    ecx
  0xb94362  push    offset aId; " (id:"
  0xb94367  push    eax
  0xb94368  push    esi
  0xb94369  mov     byte ptr [esp+54h+var_4], 1
  0xb9436e  call    sub_B03020
  0xb94373  add     esp, 8
  0xb94376  push    eax
  0xb94377  call    sub_41D990
  0xb9437c  add     esp, 8
  0xb9437f  mov     ecx, eax
  0xb94381  call    sub_ADC810
  0xb94386  push    eax
  0xb94387  call    sub_41D990
  0xb9438c  add     esp, 8
  0xb9438f  lea     ecx, [esp+40h+var_28]
  0xb94393  mov     byte ptr [esp+40h+var_4], 0
  0xb94398  call    sub_B02FF0   <<<COMMIT
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb943ac  push    offset aUniqidMs; "uniqid_ms="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb943c7  push    offset aEqBonusModules; "eq_bonus_modules={"
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb943f1  push    offset aByte; "]byte"
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
```

## 4. 发送去向切片

```asm
  0xb9442e  mov     eax, [edx+58h]
  0xb94431  sub     edi, ebx
  0xb94433  push    edi
  0xb94434  push    ebx
  0xb94435  mov     ecx, ebp
  0xb94437  call    eax
  0xb94439  test    al, al
  0xb9443b  jz      short loc_B9448B
  0xb9443d  mov     eax, [ebp+79A8h]
  0xb94443  test    eax, eax
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。
> 本批 50 条**全部命中同一去向槽 `vt[0x58]`**（与批次-16/17 一致）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB942F4` | u16 |
| `uniqid_ms` | `0xB94307` | u64 |
| `eq_bonus_modules` | `0xB9432E` | array<u32,1> |
