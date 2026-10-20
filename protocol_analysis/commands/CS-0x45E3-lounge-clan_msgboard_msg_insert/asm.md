# 汇编证据 —— CS-0x45E3-lounge-clan_msgboard_msg_insert

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_BA1FD0 @ `0xba1fd0`（`0xba1fd0`..`0xba2275`）
- 命令名字符串：`)<-_proto_lounge_client::send_clan_msgboard_msg_insert(` @ `0xeecb88`
- opcode 写入：`0xba2052`
- 声明容量：`0xD6`

## 2. 组包块切片（游标初始化 → 提交）

```asm
  0xba201d  mov     ebp, eax
  0xba201f  mov     eax, [edi+0Ch]
  0xba2022  push    eax
  0xba2023  lea     ecx, [esp+4Ch+var_34]
  0xba2027  call    sub_ABB2F0
  0xba202c  lea     ecx, [ebp+0D6h]
  0xba2032  lea     eax, [ebp+2]
  0xba2035  cmp     eax, ecx
  0xba2037  mov     [esp+48h+var_4], 0
  0xba203f  mov     [esp+48h+var_30], ebp
  0xba2043  mov     dword ptr [esp+48h+var_2C], ecx
  0xba2047  ja      loc_BA2260
  0xba204d  lea     edx, [eax+8]
  0xba2050  cmp     edx, ecx
  0xba2052  mov     word ptr [ebp+0], 45E3h
  0xba2058  ja      loc_BA2260
  0xba205e  mov     esi, [esp+48h+arg_0]
  0xba2062  mov     [eax], esi
  0xba2064  mov     esi, [esp+48h+arg_4]
  0xba2068  mov     [eax+4], esi
  0xba206b  lea     eax, [edx+2]
  0xba206e  cmp     eax, ecx
  0xba2070  ja      loc_BA2260
  0xba2076  mov     cx, word ptr [esp+48h+arg_8]
  0xba207b  mov     [edx], cx
  0xba207e  push    0C1h
  0xba2083  lea     edx, [esp+4Ch+var_30]
  0xba2087  mov     [esp+4Ch+var_30], eax
  0xba208b  mov     eax, dword ptr [esp+4Ch+arg_C]
  0xba208f  push    edx
  0xba2090  push    eax
  0xba2091  call    sub_B02B40   <<< pushN=193(0xC1)
  0xba2096  add     esp, 0Ch
  0xba2099  test    al, al
  0xba209b  jz      loc_BA2260
  0xba20a1  lea     ecx, [esp+48h+var_30]
  0xba20a5  push    ecx
  0xba20a6  lea     edx, [esp+4Ch+arg_10]
  0xba20aa  push    edx
  0xba20ab  call    sub_B061C0
  0xba20b0  add     esp, 8
  0xba20b3  test    al, al
  0xba20b5  jz      loc_BA2260
  0xba20bb  mov     esi, [edi+810Ch]
  0xba20c1  test    esi, esi
  0xba20c3  mov     ebx, [esp+48h+var_30]
  0xba20c7  jz      loc_BA2201
  0xba20cd  lea     eax, [esp+48h+var_28]
  0xba20d1  push    eax
  0xba20d2  call    sub_CA0CE0
  0xba20d7  add     esp, 4
  0xba20da  mov     ecx, [edi+8]
  0xba20dd  push    offset aProtoLoungeCli_500; ")<-_proto_lounge_client::send_clan_msgb"...
  0xba20e2  push    ecx
  0xba20e3  push    offset aId; " (id:"
  0xba20e8  push    eax
  0xba20e9  push    esi
  0xba20ea  mov     byte ptr [esp+5Ch+var_4], 1
  0xba20ef  call    sub_B03020
  0xba20f4  add     esp, 8
  0xba20f7  push    eax
  0xba20f8  call    sub_41D990
  0xba20fd  add     esp, 8
  0xba2100  mov     ecx, eax
  0xba2102  call    sub_ADC810
  0xba2107  push    eax
  0xba2108  call    sub_41D990
  0xba210d  add     esp, 8
  0xba2110  lea     ecx, [esp+48h+var_28]
  0xba2114  mov     byte ptr [esp+48h+var_4], 0
  0xba2119  call    sub_B02FF0   <<<COMMIT
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xba212d  push    offset aParentMsgid; "parent_msgid="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xba2155  push    offset aKind; "kind="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xba2182  push    offset aBody_0; "body=\""
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xba21b0  push    offset aClanKind; "clan_kind="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xba21c9  push    offset aByte; "]byte"
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
```

## 4. 发送去向切片

```asm
  0xba2203  mov     eax, [edx+58h]
  0xba2206  sub     ebx, ebp
  0xba2208  push    ebx
  0xba2209  push    ebp
  0xba220a  mov     ecx, edi
  0xba220c  call    eax
  0xba220e  test    al, al
  0xba2210  jz      short loc_BA2260
  0xba2212  mov     eax, [edi+79A8h]
  0xba2218  test    eax, eax
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。
> 本批 50 条**全部命中同一去向槽 `vt[0x58]`**（与批次-16/17 一致）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xBA2052` | u16 |
| `parent_msgid` | `0xBA2062` | u64 |
| `kind` | `0xBA207B` | u16 |
| `body` | `0xBA2091` | bytes |
| `clan_kind` | `0xBA20AB` | u8 |
