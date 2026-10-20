# 汇编证据 —— CS-0x4CCB-lounge-msma_is_favorite_update

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B95460 @ `0xb95460`（`0xb95460`..`0xb95652`）
- 命令名字符串：`)<-_proto_lounge_client::send_msma_is_favorite_update(` @ `0xeeb728`
- opcode 写入：`0xb954d4`
- 声明容量：`0xE`

## 2. 组包块切片（游标初始化 → 提交）

```asm
  0xb954aa  mov     ebp, eax
  0xb954ac  mov     eax, [edi+0Ch]
  0xb954af  push    eax
  0xb954b0  lea     ecx, [esp+44h+var_2C]
  0xb954b4  call    sub_ABB2F0
  0xb954b9  lea     ecx, [ebp+0Eh]
  0xb954bc  lea     eax, [ebp+2]
  0xb954bf  cmp     eax, ecx
  0xb954c1  mov     [esp+40h+var_4], 0
  0xb954c9  ja      loc_B9563D
  0xb954cf  lea     edx, [eax+8]
  0xb954d2  cmp     edx, ecx
  0xb954d4  mov     word ptr [ebp+0], 4CCBh
  0xb954da  ja      loc_B9563D
  0xb954e0  mov     esi, [esp+40h+arg_0]
  0xb954e4  mov     [eax], esi
  0xb954e6  mov     esi, [esp+40h+arg_4]
  0xb954ea  lea     ebx, [edx+4]
  0xb954ed  cmp     ebx, ecx
  0xb954ef  mov     [eax+4], esi
  0xb954f2  ja      loc_B9563D
  0xb954f8  mov     ecx, [esp+40h+arg_8]
  0xb954fc  mov     [edx], ecx
  0xb954fe  mov     esi, [edi+7D94h]
  0xb95504  test    esi, esi
  0xb95506  jz      loc_B955DE
  0xb9550c  lea     edx, [esp+40h+var_28]
  0xb95510  push    edx
  0xb95511  call    sub_CA0CE0
  0xb95516  add     esp, 4
  0xb95519  mov     ecx, [edi+8]
  0xb9551c  push    offset aProtoLoungeCli_473; ")<-_proto_lounge_client::send_msma_is_f"...
  0xb95521  push    ecx
  0xb95522  push    offset aId; " (id:"
  0xb95527  push    eax
  0xb95528  push    esi
  0xb95529  mov     byte ptr [esp+54h+var_4], 1
  0xb9552e  call    sub_B03020
  0xb95533  add     esp, 8
  0xb95536  push    eax
  0xb95537  call    sub_41D990
  0xb9553c  add     esp, 8
  0xb9553f  mov     ecx, eax
  0xb95541  call    sub_ADC810
  0xb95546  push    eax
  0xb95547  call    sub_41D990
  0xb9554c  add     esp, 8
  0xb9554f  lea     ecx, [esp+40h+var_28]
  0xb95553  mov     byte ptr [esp+40h+var_4], 0
  0xb95558  call    sub_B02FF0   <<<COMMIT
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb9556c  push    offset aUniqid; "uniqid="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb9558f  push    offset aIsFavorite; "is_favorite="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb955a4  push    offset aByte; "]byte"
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
```

## 4. 发送去向切片

```asm
  0xb955e0  mov     edx, [eax+58h]
  0xb955e3  sub     ebx, ebp
  0xb955e5  push    ebx
  0xb955e6  push    ebp
  0xb955e7  mov     ecx, edi
  0xb955e9  call    edx
  0xb955eb  test    al, al
  0xb955ed  jz      short loc_B9563D
  0xb955ef  mov     eax, [edi+79A8h]
  0xb955f5  test    eax, eax
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。
> 本批 50 条**全部命中同一去向槽 `vt[0x58]`**（与批次-16/17 一致）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB954D4` | u16 |
| `uniqid` | `0xB954E4` | u64 |
| `is_favorite` | `0xB954FC` | u32 |
