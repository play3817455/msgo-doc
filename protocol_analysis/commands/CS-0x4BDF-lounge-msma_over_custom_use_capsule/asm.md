# 汇编证据 —— CS-0x4BDF-lounge-msma_over_custom_use_capsule

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_BA80F0 @ `0xba80f0`（`0xba80f0`..`0xba82e2`）
- 命令名字符串：`)<-_proto_lounge_client::send_msma_over_custom_use_capsule(` @ `0xeed60c`
- opcode 写入：`0xba8164`
- 声明容量：`0xE`

## 2. 组包块切片（游标初始化 → 提交）

```asm
  0xba813a  mov     ebp, eax
  0xba813c  mov     eax, [edi+0Ch]
  0xba813f  push    eax
  0xba8140  lea     ecx, [esp+44h+var_2C]
  0xba8144  call    sub_ABB2F0
  0xba8149  lea     ecx, [ebp+0Eh]
  0xba814c  lea     eax, [ebp+2]
  0xba814f  cmp     eax, ecx
  0xba8151  mov     [esp+40h+var_4], 0
  0xba8159  ja      loc_BA82CD
  0xba815f  lea     edx, [eax+8]
  0xba8162  cmp     edx, ecx
  0xba8164  mov     word ptr [ebp+0], 4BDFh
  0xba816a  ja      loc_BA82CD
  0xba8170  mov     esi, [esp+40h+arg_0]
  0xba8174  mov     [eax], esi
  0xba8176  mov     esi, [esp+40h+arg_4]
  0xba817a  lea     ebx, [edx+4]
  0xba817d  cmp     ebx, ecx
  0xba817f  mov     [eax+4], esi
  0xba8182  ja      loc_BA82CD
  0xba8188  mov     ecx, [esp+40h+arg_8]
  0xba818c  mov     [edx], ecx
  0xba818e  mov     esi, [edi+8334h]
  0xba8194  test    esi, esi
  0xba8196  jz      loc_BA826E
  0xba819c  lea     edx, [esp+40h+var_28]
  0xba81a0  push    edx
  0xba81a1  call    sub_CA0CE0
  0xba81a6  add     esp, 4
  0xba81a9  mov     ecx, [edi+8]
  0xba81ac  push    offset aProtoLoungeCli_466; ")<-_proto_lounge_client::send_msma_over"...
  0xba81b1  push    ecx
  0xba81b2  push    offset aId; " (id:"
  0xba81b7  push    eax
  0xba81b8  push    esi
  0xba81b9  mov     byte ptr [esp+54h+var_4], 1
  0xba81be  call    sub_B03020
  0xba81c3  add     esp, 8
  0xba81c6  push    eax
  0xba81c7  call    sub_41D990
  0xba81cc  add     esp, 8
  0xba81cf  mov     ecx, eax
  0xba81d1  call    sub_ADC810
  0xba81d6  push    eax
  0xba81d7  call    sub_41D990
  0xba81dc  add     esp, 8
  0xba81df  lea     ecx, [esp+40h+var_28]
  0xba81e3  mov     byte ptr [esp+40h+var_4], 0
  0xba81e8  call    sub_B02FF0   <<<COMMIT
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xba81fc  push    offset aUniqMsid; "uniq_msid="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xba821f  push    offset aItemId; "item_id="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xba8234  push    offset aByte; "]byte"
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
```

## 4. 发送去向切片

```asm
  0xba8270  mov     edx, [eax+58h]
  0xba8273  sub     ebx, ebp
  0xba8275  push    ebx
  0xba8276  push    ebp
  0xba8277  mov     ecx, edi
  0xba8279  call    edx
  0xba827b  test    al, al
  0xba827d  jz      short loc_BA82CD
  0xba827f  mov     eax, [edi+79A8h]
  0xba8285  test    eax, eax
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。
> 本批 50 条**全部命中同一去向槽 `vt[0x58]`**（与批次-16/17 一致）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xBA8164` | u16 |
| `uniq_msid` | `0xBA8174` | u64 |
| `item_id` | `0xBA818C` | u32 |
