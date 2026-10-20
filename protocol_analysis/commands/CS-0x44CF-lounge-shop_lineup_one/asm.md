# 汇编证据 —— CS-0x44CF-lounge-shop_lineup_one

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B9CB80 @ `0xb9cb80`（`0xb9cb80`..`0xb9cd68`）
- 命令名字符串：`)<-_proto_lounge_client::send_shop_lineup_one(` @ `0xeec320`
- opcode 写入：`0xb9cbf4`
- 声明容量：`0xA`

## 2. 组包块切片（游标初始化 → 提交）

```asm
  0xb9cbca  mov     ebp, eax
  0xb9cbcc  mov     eax, [esi+0Ch]
  0xb9cbcf  push    eax
  0xb9cbd0  lea     ecx, [esp+44h+var_2C]
  0xb9cbd4  call    sub_ABB2F0
  0xb9cbd9  lea     eax, [ebp+0Ah]
  0xb9cbdc  lea     ecx, [ebp+2]
  0xb9cbdf  cmp     ecx, eax
  0xb9cbe1  mov     [esp+40h+var_4], 0
  0xb9cbe9  ja      loc_B9CD53
  0xb9cbef  lea     edi, [ecx+1]
  0xb9cbf2  cmp     edi, eax
  0xb9cbf4  mov     word ptr [ebp+0], 44CFh
  0xb9cbfa  ja      loc_B9CD53
  0xb9cc00  mov     dl, byte ptr [esp+40h+arg_0]
  0xb9cc04  lea     ebx, [edi+4]
  0xb9cc07  cmp     ebx, eax
  0xb9cc09  mov     [ecx], dl
  0xb9cc0b  ja      loc_B9CD53
  0xb9cc11  mov     eax, [esp+40h+arg_4]
  0xb9cc15  mov     [edi], eax
  0xb9cc17  mov     edi, [esi+7F90h]
  0xb9cc1d  test    edi, edi
  0xb9cc1f  jz      loc_B9CCF4
  0xb9cc25  lea     ecx, [esp+40h+var_28]
  0xb9cc29  push    ecx
  0xb9cc2a  call    sub_CA0CE0
  0xb9cc2f  add     esp, 4
  0xb9cc32  mov     edx, [esi+8]
  0xb9cc35  push    offset aProtoLoungeCli_371; ")<-_proto_lounge_client::send_shop_line"...
  0xb9cc3a  push    edx
  0xb9cc3b  push    offset aId; " (id:"
  0xb9cc40  push    eax
  0xb9cc41  push    edi
  0xb9cc42  mov     byte ptr [esp+54h+var_4], 1
  0xb9cc47  call    sub_B03020
  0xb9cc4c  add     esp, 8
  0xb9cc4f  push    eax
  0xb9cc50  call    sub_41D990
  0xb9cc55  add     esp, 8
  0xb9cc58  mov     ecx, eax
  0xb9cc5a  call    sub_ADC810
  0xb9cc5f  push    eax
  0xb9cc60  call    sub_41D990
  0xb9cc65  add     esp, 8
  0xb9cc68  lea     ecx, [esp+40h+var_28]
  0xb9cc6c  mov     byte ptr [esp+40h+var_4], 0
  0xb9cc71  call    sub_B02FF0   <<<COMMIT
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb9cc80  push    offset aTabType; "tab_type="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb9cca5  push    offset aShopitemId; "shopitem_id="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb9ccba  push    offset aByte; "]byte"
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
```

## 4. 发送去向切片

```asm
  0xb9ccf6  mov     edx, [eax+58h]
  0xb9ccf9  sub     ebx, ebp
  0xb9ccfb  push    ebx
  0xb9ccfc  push    ebp
  0xb9ccfd  mov     ecx, esi
  0xb9ccff  call    edx
  0xb9cd01  test    al, al
  0xb9cd03  jz      short loc_B9CD53
  0xb9cd05  mov     eax, [esi+79A8h]
  0xb9cd0b  test    eax, eax
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。
> 本批 50 条**全部命中同一去向槽 `vt[0x58]`**（与批次-16/17 一致）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB9CBF4` | u16 |
| `tab_type` | `0xB9CC09` | u8 |
| `shopitem_id` | `0xB9CC15` | u32 |
