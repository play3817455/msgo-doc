# 汇编证据 —— CS-0x522B-lounge-update_check_progress_quest_id

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_BA61F0 @ `0xba61f0`（`0xba61f0`..`0xba639d`）
- 命令名字符串：`)<-_proto_lounge_client::send_update_check_progress_quest_id(` @ `0xeed250`
- opcode 写入：`0xba6264`
- 声明容量：`0x6`

## 2. 组包块切片（游标初始化 → 提交）

```asm
  0xba623a  mov     ebp, eax
  0xba623c  mov     eax, [esi+0Ch]
  0xba623f  push    eax
  0xba6240  lea     ecx, [esp+44h+var_2C]
  0xba6244  call    sub_ABB2F0
  0xba6249  lea     ecx, [ebp+6]
  0xba624c  lea     eax, [ebp+2]
  0xba624f  cmp     eax, ecx
  0xba6251  mov     [esp+40h+var_4], 0
  0xba6259  ja      loc_BA6388
  0xba625f  lea     ebx, [eax+4]
  0xba6262  cmp     ebx, ecx
  0xba6264  mov     word ptr [ebp+0], 522Bh
  0xba626a  ja      loc_BA6388
  0xba6270  mov     ecx, [esp+40h+arg_0]
  0xba6274  mov     [eax], ecx
  0xba6276  mov     edi, [esi+8260h]
  0xba627c  test    edi, edi
  0xba627e  jz      loc_BA6329
  0xba6284  lea     edx, [esp+40h+var_28]
  0xba6288  push    edx
  0xba6289  call    sub_CA0CE0
  0xba628e  add     esp, 4
  0xba6291  mov     ecx, [esi+8]
  0xba6294  push    offset aProtoLoungeCli_581; ")<-_proto_lounge_client::send_update_ch"...
  0xba6299  push    ecx
  0xba629a  push    offset aId; " (id:"
  0xba629f  push    eax
  0xba62a0  push    edi
  0xba62a1  mov     byte ptr [esp+54h+var_4], 1
  0xba62a6  call    sub_B03020
  0xba62ab  add     esp, 8
  0xba62ae  push    eax
  0xba62af  call    sub_41D990
  0xba62b4  add     esp, 8
  0xba62b7  mov     ecx, eax
  0xba62b9  call    sub_ADC810
  0xba62be  push    eax
  0xba62bf  call    sub_41D990
  0xba62c4  add     esp, 8
  0xba62c7  lea     ecx, [esp+40h+var_28]
  0xba62cb  mov     byte ptr [esp+40h+var_4], 0
  0xba62d0  call    sub_B02FF0   <<<COMMIT
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xba62da  push    offset aQuestId; "quest_id="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xba62ef  push    offset aByte; "]byte"
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
```

## 4. 发送去向切片

```asm
  0xba632b  mov     eax, [edx+58h]
  0xba632e  sub     ebx, ebp
  0xba6330  push    ebx
  0xba6331  push    ebp
  0xba6332  mov     ecx, esi
  0xba6334  call    eax
  0xba6336  test    al, al
  0xba6338  jz      short loc_BA6388
  0xba633a  mov     eax, [esi+79A8h]
  0xba6340  test    eax, eax
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。
> 本批 50 条**全部命中同一去向槽 `vt[0x58]`**（与批次-16/17 一致）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xBA6264` | u16 |
| `quest_id` | `0xBA6274` | u32 |
