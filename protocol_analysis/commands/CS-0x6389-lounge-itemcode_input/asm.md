# 汇编证据 —— CS-0x6389-lounge-itemcode_input

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B9E910 @ `0xb9e910`（`0xb9e910`..`0xb9eae9`）
- 命令名字符串：`)<-_proto_lounge_client::send_itemcode_input(` @ `0xeec5bc`
- opcode 写入：`0xb9e993`
- 声明容量：`0x26`

## 2. 组包块切片（游标初始化 → 提交）

```asm
  0xb9e95a  mov     edi, eax
  0xb9e95c  mov     eax, [esi+0Ch]
  0xb9e95f  push    eax
  0xb9e960  lea     ecx, [esp+4Ch+var_34]
  0xb9e964  call    sub_ABB2F0
  0xb9e969  lea     ecx, [edi+26h]
  0xb9e96c  lea     eax, [edi+2]
  0xb9e96f  cmp     eax, ecx
  0xb9e971  mov     [esp+48h+var_4], 0
  0xb9e979  mov     [esp+48h+var_30], edi
  0xb9e97d  mov     dword ptr [esp+48h+var_2C], ecx
  0xb9e981  ja      loc_B9EAD4
  0xb9e987  mov     edx, [esp+48h+arg_0]
  0xb9e98b  push    21h ; '!'
  0xb9e98d  lea     ecx, [esp+4Ch+var_30]
  0xb9e991  push    ecx
  0xb9e992  push    edx
  0xb9e993  mov     word ptr [edi], 6389h
  0xb9e998  mov     [esp+54h+var_30], eax
  0xb9e99c  call    sub_B02B40   <<< pushN=33(0x21)
  0xb9e9a1  add     esp, 0Ch
  0xb9e9a4  test    al, al
  0xb9e9a6  jz      loc_B9EAD4
  0xb9e9ac  mov     ebp, [esi+8010h]
  0xb9e9b2  test    ebp, ebp
  0xb9e9b4  mov     ebx, [esp+48h+var_30]
  0xb9e9b8  jz      loc_B9EA73
  0xb9e9be  lea     eax, [esp+48h+var_28]
  0xb9e9c2  push    eax
  0xb9e9c3  call    sub_CA0CE0
  0xb9e9c8  add     esp, 4
  0xb9e9cb  mov     ecx, [esi+8]
  0xb9e9ce  push    offset aProtoLoungeCli_573; ")<-_proto_lounge_client::send_itemcode_"...
  0xb9e9d3  push    ecx
  0xb9e9d4  push    offset aId; " (id:"
  0xb9e9d9  push    eax
  0xb9e9da  push    ebp
  0xb9e9db  mov     byte ptr [esp+5Ch+var_4], 1
  0xb9e9e0  call    sub_B03020
  0xb9e9e5  add     esp, 8
  0xb9e9e8  push    eax
  0xb9e9e9  call    sub_41D990
  0xb9e9ee  add     esp, 8
  0xb9e9f1  mov     ecx, eax
  0xb9e9f3  call    sub_ADC810
  0xb9e9f8  push    eax
  0xb9e9f9  call    sub_41D990
  0xb9e9fe  add     esp, 8
  0xb9ea01  lea     ecx, [esp+48h+var_28]
  0xb9ea05  mov     byte ptr [esp+48h+var_4], 0
  0xb9ea0a  call    sub_B02FF0   <<<COMMIT
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb9ea19  push    offset aCode; "code=\""
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb9ea39  push    offset aByte; "]byte"
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
```

## 4. 发送去向切片

```asm
  0xb9ea75  mov     eax, [edx+58h]
  0xb9ea78  mov     ebp, ebx
  0xb9ea7a  sub     ebp, edi
  0xb9ea7c  push    ebp
  0xb9ea7d  push    edi
  0xb9ea7e  mov     ecx, esi
  0xb9ea80  call    eax
  0xb9ea82  test    al, al
  0xb9ea84  jz      short loc_B9EAD4
  0xb9ea86  mov     eax, [esi+79A8h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。
> 本批 50 条**全部命中同一去向槽 `vt[0x58]`**（与批次-16/17 一致）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB9E993` | u16 |
| `code` | `0xB9E99C` | bytes |
