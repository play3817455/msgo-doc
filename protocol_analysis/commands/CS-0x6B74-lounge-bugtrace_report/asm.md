# 汇编证据 —— CS-0x6B74-lounge-bugtrace_report

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_BA5BE0 @ `0xba5be0`（`0xba5be0`..`0xba5ece`）
- 命令名字符串：`)<-_proto_lounge_client::send_bugtrace_report(` @ `0xeed1a8`
- opcode 写入：`0xba5c62`
- 声明容量：`0x1816`

## 2. 组包块切片（游标初始化 → 提交）

```asm
  0xba5c2d  mov     ebp, eax
  0xba5c2f  mov     eax, [edi+0Ch]
  0xba5c32  push    eax
  0xba5c33  lea     ecx, [esp+4Ch+var_34]
  0xba5c37  call    sub_ABB2F0
  0xba5c3c  lea     ecx, [ebp+1816h]
  0xba5c42  lea     eax, [ebp+2]
  0xba5c45  cmp     eax, ecx
  0xba5c47  mov     [esp+48h+var_4], 0
  0xba5c4f  mov     [esp+48h+var_30], ebp
  0xba5c53  mov     dword ptr [esp+48h+var_2C], ecx
  0xba5c57  ja      loc_BA5EB9
  0xba5c5d  lea     edx, [eax+4]
  0xba5c60  cmp     edx, ecx
  0xba5c62  mov     word ptr [ebp+0], 6B74h
  0xba5c68  ja      loc_BA5EB9
  0xba5c6e  mov     esi, [esp+48h+arg_0]
  0xba5c72  mov     [eax], esi
  0xba5c74  mov     eax, edx
  0xba5c76  lea     edx, [eax+4]
  0xba5c79  cmp     edx, ecx
  0xba5c7b  ja      loc_BA5EB9
  0xba5c81  mov     ecx, [esp+48h+arg_4]
  0xba5c85  mov     [esp+48h+var_30], edx
  0xba5c89  push    0C01h
  0xba5c8e  lea     edx, [esp+4Ch+var_30]
  0xba5c92  mov     [eax], ecx
  0xba5c94  mov     eax, [esp+4Ch+arg_8]
  0xba5c98  push    edx
  0xba5c99  push    eax
  0xba5c9a  call    sub_B02B40   <<< pushN=3073(0xC01)
  0xba5c9f  add     esp, 0Ch
  0xba5ca2  test    al, al
  0xba5ca4  jz      loc_BA5EB9
  0xba5caa  lea     ecx, [esp+48h+var_30]
  0xba5cae  push    ecx
  0xba5caf  lea     edx, [esp+4Ch+arg_C]
  0xba5cb3  push    edx
  0xba5cb4  call    sub_B02D80
  0xba5cb9  add     esp, 8
  0xba5cbc  test    al, al
  0xba5cbe  jz      loc_BA5EB9
  0xba5cc4  mov     ecx, [esp+48h+arg_10]
  0xba5cc8  push    0C01h
  0xba5ccd  lea     eax, [esp+4Ch+var_30]
  0xba5cd1  push    eax
  0xba5cd2  push    ecx
  0xba5cd3  call    sub_B02B40   <<< pushN=3073(0xC01)
  0xba5cd8  add     esp, 0Ch
  0xba5cdb  test    al, al
  0xba5cdd  jz      loc_BA5EB9
  0xba5ce3  mov     esi, [edi+8230h]
  0xba5ce9  test    esi, esi
  0xba5ceb  mov     ebx, [esp+48h+var_30]
  0xba5cef  jz      loc_BA5E5A
  0xba5cf5  lea     edx, [esp+48h+var_28]
  0xba5cf9  push    edx
  0xba5cfa  call    sub_CA0CE0
  0xba5cff  add     esp, 4
  0xba5d02  mov     ecx, [edi+8]
  0xba5d05  push    offset aProtoLoungeCli_388; ")<-_proto_lounge_client::send_bugtrace_"...
  0xba5d0a  push    ecx
  0xba5d0b  push    offset aId; " (id:"
  0xba5d10  push    eax
  0xba5d11  push    esi
  0xba5d12  mov     byte ptr [esp+5Ch+var_4], 1
  0xba5d17  call    sub_B03020
  0xba5d1c  add     esp, 8
  0xba5d1f  push    eax
  0xba5d20  call    sub_41D990
  0xba5d25  add     esp, 8
  0xba5d28  mov     ecx, eax
  0xba5d2a  call    sub_ADC810
  0xba5d2f  push    eax
  0xba5d30  call    sub_41D990
  0xba5d35  add     esp, 8
  0xba5d38  lea     ecx, [esp+48h+var_28]
  0xba5d3c  mov     byte ptr [esp+48h+var_4], 0
  0xba5d41  call    sub_B02FF0   <<<COMMIT
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xba5d50  push    offset aOccuredTime; "occured_time="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xba5d78  push    offset aPc; "pc="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xba5da5  push    offset aStack_0; "stack=\""
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xba5dd8  push    offset aExcode; "excode="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xba5e00  push    offset aExinfo; "exinfo=\""
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xba5e20  push    offset aByte; "]byte"
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
```

## 4. 发送去向切片

```asm
  0xba5e5c  mov     eax, [edx+58h]
  0xba5e5f  sub     ebx, ebp
  0xba5e61  push    ebx
  0xba5e62  push    ebp
  0xba5e63  mov     ecx, edi
  0xba5e65  call    eax
  0xba5e67  test    al, al
  0xba5e69  jz      short loc_BA5EB9
  0xba5e6b  mov     eax, [edi+79A8h]
  0xba5e71  test    eax, eax
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。
> 本批 50 条**全部命中同一去向槽 `vt[0x58]`**（与批次-16/17 一致）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xBA5C62` | u16 |
| `occured_time` | `0xBA5C72` | u32 |
| `pc` | `0xBA5C92` | u32 |
| `stack` | `0xBA5C9A` | bytes |
| `excode` | `0xBA5CB4` | u32 |
| `exinfo` | `0xBA5CD3` | bytes |
