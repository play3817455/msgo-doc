# 汇编证据 —— CS-0x5F28-lounge-speedhack_check_response

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_BA4D50 @ `0xba4d50`（`0xba4d50`..`0xba4f3a`）
- 命令名字符串：`)<-_proto_lounge_client::send_speedhack_check_response(` @ `0xeed04c`
- opcode 写入：`0xba4dc4`
- 声明容量：`0xA`

## 2. 组包块切片（游标初始化 → 提交）

```asm
  0xba4d9a  mov     ebp, eax
  0xba4d9c  mov     eax, [edi+0Ch]
  0xba4d9f  push    eax
  0xba4da0  lea     ecx, [esp+44h+var_2C]
  0xba4da4  call    sub_ABB2F0
  0xba4da9  lea     ecx, [ebp+0Ah]
  0xba4dac  lea     eax, [ebp+2]
  0xba4daf  cmp     eax, ecx
  0xba4db1  mov     [esp+40h+var_4], 0
  0xba4db9  ja      loc_BA4F25
  0xba4dbf  lea     edx, [eax+2]
  0xba4dc2  cmp     edx, ecx
  0xba4dc4  mov     word ptr [ebp+0], 5F28h
  0xba4dca  ja      loc_BA4F25
  0xba4dd0  mov     si, word ptr [esp+40h+arg_0]
  0xba4dd5  lea     ebx, [edx+2]
  0xba4dd8  cmp     ebx, ecx
  0xba4dda  mov     [eax], si
  0xba4ddd  ja      loc_BA4F25
  0xba4de3  mov     cx, word ptr [esp+40h+arg_4]
  0xba4de8  mov     [edx], cx
  0xba4deb  mov     esi, [edi+8208h]
  0xba4df1  test    esi, esi
  0xba4df3  jz      loc_BA4EC6
  0xba4df9  lea     edx, [esp+40h+var_28]
  0xba4dfd  push    edx
  0xba4dfe  call    sub_CA0CE0
  0xba4e03  add     esp, 4
  0xba4e06  mov     ecx, [edi+8]
  0xba4e09  push    offset aProtoLoungeCli_598; ")<-_proto_lounge_client::send_speedhack"...
  0xba4e0e  push    ecx
  0xba4e0f  push    offset aId; " (id:"
  0xba4e14  push    eax
  0xba4e15  push    esi
  0xba4e16  mov     byte ptr [esp+54h+var_4], 1
  0xba4e1b  call    sub_B03020
  0xba4e20  add     esp, 8
  0xba4e23  push    eax
  0xba4e24  call    sub_41D990
  0xba4e29  add     esp, 8
  0xba4e2c  mov     ecx, eax
  0xba4e2e  call    sub_ADC810
  0xba4e33  push    eax
  0xba4e34  call    sub_41D990
  0xba4e39  add     esp, 8
  0xba4e3c  lea     ecx, [esp+40h+var_28]
  0xba4e40  mov     byte ptr [esp+40h+var_4], 0
  0xba4e45  call    sub_B02FF0   <<<COMMIT
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xba4e54  push    offset aDebuggerFound; "debugger_found="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xba4e77  push    offset aProcRefCount; "proc_ref_count="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xba4e8c  push    offset aByte; "]byte"
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
```

## 4. 发送去向切片

```asm
  0xba4ec8  mov     eax, [edx+58h]
  0xba4ecb  sub     ebx, ebp
  0xba4ecd  push    ebx
  0xba4ece  push    ebp
  0xba4ecf  mov     ecx, edi
  0xba4ed1  call    eax
  0xba4ed3  test    al, al
  0xba4ed5  jz      short loc_BA4F25
  0xba4ed7  mov     eax, [edi+79A8h]
  0xba4edd  test    eax, eax
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。
> 本批 50 条**全部命中同一去向槽 `vt[0x58]`**（与批次-16/17 一致）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xBA4DC4` | u16 |
| `debugger_found` | `0xBA4DDA` | u16 |
| `proc_ref_count` | `0xBA4DE8` | u16 |
