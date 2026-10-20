# 汇编证据 —— CS-0x6142-lounge-pilot_delete

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B8A630 @ `0xb8a630`（`0xb8a630`..`0xb8a8a8`）
- 命令名字符串：`)<-_proto_lounge_client::send_pilot_delete(` @ `0xeea3a0`
- opcode 写入：`0xb8a6a9`
- 声明容量：`0x12`

## 2. 组包块切片（游标初始化 → 提交）

```asm
  0xb8a677  mov     ebp, eax
  0xb8a679  mov     eax, [edi+0Ch]
  0xb8a67c  push    eax
  0xb8a67d  lea     ecx, [esp+4Ch+var_34]
  0xb8a681  call    sub_ABB2F0
  0xb8a686  lea     ecx, [ebp+12h]
  0xb8a689  lea     eax, [ebp+2]
  0xb8a68c  cmp     eax, ecx
  0xb8a68e  mov     [esp+48h+var_4], 0
  0xb8a696  mov     [esp+48h+var_30], ebp
  0xb8a69a  mov     dword ptr [esp+48h+var_2C], ecx
  0xb8a69e  ja      loc_B8A893
  0xb8a6a4  lea     edx, [eax+4]
  0xb8a6a7  cmp     edx, ecx
  0xb8a6a9  mov     word ptr [ebp+0], 6142h
  0xb8a6af  ja      loc_B8A893
  0xb8a6b5  mov     esi, [esp+48h+arg_0]
  0xb8a6b9  mov     [eax], esi
  0xb8a6bb  mov     eax, edx
  0xb8a6bd  lea     edx, [eax+4]
  0xb8a6c0  cmp     edx, ecx
  0xb8a6c2  ja      loc_B8A893
  0xb8a6c8  mov     ecx, [esp+48h+arg_4]
  0xb8a6cc  mov     [esp+48h+var_30], edx
  0xb8a6d0  lea     edx, [esp+48h+var_30]
  0xb8a6d4  mov     [eax], ecx
  0xb8a6d6  push    edx
  0xb8a6d7  lea     eax, [esp+4Ch+arg_8]
  0xb8a6db  push    eax
  0xb8a6dc  call    sub_B02D80
  0xb8a6e1  add     esp, 8
  0xb8a6e4  test    al, al
  0xb8a6e6  jz      loc_B8A893
  0xb8a6ec  lea     ecx, [esp+48h+var_30]
  0xb8a6f0  push    ecx
  0xb8a6f1  lea     edx, [esp+4Ch+arg_C]
  0xb8a6f5  push    edx
  0xb8a6f6  call    sub_B061C0
  0xb8a6fb  add     esp, 8
  0xb8a6fe  test    al, al
  0xb8a700  jz      loc_B8A893
  0xb8a706  mov     esi, [edi+79FCh]
  0xb8a70c  test    esi, esi
  0xb8a70e  mov     ebx, [esp+48h+var_30]
  0xb8a712  jz      loc_B8A837
  0xb8a718  lea     eax, [esp+48h+var_28]
  0xb8a71c  push    eax
  0xb8a71d  call    sub_CA0CE0
  0xb8a722  add     esp, 4
  0xb8a725  mov     ecx, [edi+8]
  0xb8a728  push    offset aProtoLoungeCli_375; ")<-_proto_lounge_client::send_pilot_del"...
  0xb8a72d  push    ecx
  0xb8a72e  push    offset aId; " (id:"
  0xb8a733  push    eax
  0xb8a734  push    esi
  0xb8a735  mov     byte ptr [esp+5Ch+var_4], 1
  0xb8a73a  call    sub_B03020
  0xb8a73f  add     esp, 8
  0xb8a742  push    eax
  0xb8a743  call    sub_41D990
  0xb8a748  add     esp, 8
  0xb8a74b  mov     ecx, eax
  0xb8a74d  call    sub_ADC810
  0xb8a752  push    eax
  0xb8a753  call    sub_41D990
  0xb8a758  add     esp, 8
  0xb8a75b  lea     ecx, [esp+48h+var_28]
  0xb8a75f  mov     byte ptr [esp+48h+var_4], 0
  0xb8a764  call    sub_B02FF0   <<<COMMIT
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb8a773  push    offset aTroops; "troops="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb8a79b  push    offset aSlot; "slot="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb8a7c3  push    offset aPilotId; "pilot_id="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb8a7e6  push    offset aDelKind; "del_kind="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb8a7fd  push    offset aByte; "]byte"
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
```

## 4. 发送去向切片

```asm
  0xb8a839  mov     eax, [edx+58h]
  0xb8a83c  sub     ebx, ebp
  0xb8a83e  push    ebx
  0xb8a83f  push    ebp
  0xb8a840  mov     ecx, edi
  0xb8a842  call    eax
  0xb8a844  test    al, al
  0xb8a846  jz      short loc_B8A893
  0xb8a848  mov     eax, [edi+79A8h]
  0xb8a84e  test    eax, eax
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。
> 本批 50 条**全部命中同一去向槽 `vt[0x58]`**（与批次-16/17 一致）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB8A6A9` | u16 |
| `troops` | `0xB8A6B9` | u32 |
| `slot` | `0xB8A6D4` | u32 |
| `pilot_id` | `0xB8A6DC` | u32 |
| `del_kind` | `0xB8A6F6` | u8 |
