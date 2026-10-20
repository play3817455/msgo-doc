# 汇编证据 —— CS-0x457B-lounge-item_use_uniqid_in_lobby

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B9A120 @ `0xb9a120`（`0xb9a120`..`0xb9a314`）
- 命令名字符串：`)<-_proto_lounge_client::send_item_use_uniqid_in_lobby(` @ `0xeebec0`
- opcode 写入：`0xb9a194`
- 声明容量：`0xE`

## 2. 组包块切片（游标初始化 → 提交）

```asm
  0xb9a16a  mov     ebp, eax
  0xb9a16c  mov     eax, [edi+0Ch]
  0xb9a16f  push    eax
  0xb9a170  lea     ecx, [esp+44h+var_2C]
  0xb9a174  call    sub_ABB2F0
  0xb9a179  lea     ecx, [ebp+0Eh]
  0xb9a17c  lea     eax, [ebp+2]
  0xb9a17f  cmp     eax, ecx
  0xb9a181  mov     [esp+40h+var_4], 0
  0xb9a189  ja      loc_B9A2FF
  0xb9a18f  lea     edx, [eax+8]
  0xb9a192  cmp     edx, ecx
  0xb9a194  mov     word ptr [ebp+0], 457Bh
  0xb9a19a  ja      loc_B9A2FF
  0xb9a1a0  mov     esi, [esp+40h+arg_0]
  0xb9a1a4  mov     [eax], esi
  0xb9a1a6  mov     esi, [esp+40h+arg_4]
  0xb9a1aa  lea     ebx, [edx+2]
  0xb9a1ad  cmp     ebx, ecx
  0xb9a1af  mov     [eax+4], esi
  0xb9a1b2  ja      loc_B9A2FF
  0xb9a1b8  mov     cx, word ptr [esp+40h+arg_8]
  0xb9a1bd  mov     [edx], cx
  0xb9a1c0  mov     esi, [edi+7ECCh]
  0xb9a1c6  test    esi, esi
  0xb9a1c8  jz      loc_B9A2A0
  0xb9a1ce  lea     edx, [esp+40h+var_28]
  0xb9a1d2  push    edx
  0xb9a1d3  call    sub_CA0CE0
  0xb9a1d8  add     esp, 4
  0xb9a1db  mov     ecx, [edi+8]
  0xb9a1de  push    offset aProtoLoungeCli_575; ")<-_proto_lounge_client::send_item_use_"...
  0xb9a1e3  push    ecx
  0xb9a1e4  push    offset aId; " (id:"
  0xb9a1e9  push    eax
  0xb9a1ea  push    esi
  0xb9a1eb  mov     byte ptr [esp+54h+var_4], 1
  0xb9a1f0  call    sub_B03020
  0xb9a1f5  add     esp, 8
  0xb9a1f8  push    eax
  0xb9a1f9  call    sub_41D990
  0xb9a1fe  add     esp, 8
  0xb9a201  mov     ecx, eax
  0xb9a203  call    sub_ADC810
  0xb9a208  push    eax
  0xb9a209  call    sub_41D990
  0xb9a20e  add     esp, 8
  0xb9a211  lea     ecx, [esp+40h+var_28]
  0xb9a215  mov     byte ptr [esp+40h+var_4], 0
  0xb9a21a  call    sub_B02FF0   <<<COMMIT
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb9a22e  push    offset aUniqid; "uniqid="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb9a251  push    offset aNum; "num="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb9a266  push    offset aByte; "]byte"
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
```

## 4. 发送去向切片

```asm
  0xb9a2a2  mov     edx, [eax+58h]
  0xb9a2a5  sub     ebx, ebp
  0xb9a2a7  push    ebx
  0xb9a2a8  push    ebp
  0xb9a2a9  mov     ecx, edi
  0xb9a2ab  call    edx
  0xb9a2ad  test    al, al
  0xb9a2af  jz      short loc_B9A2FF
  0xb9a2b1  mov     eax, [edi+79A8h]
  0xb9a2b7  test    eax, eax
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。
> 本批 50 条**全部命中同一去向槽 `vt[0x58]`**（与批次-16/17 一致）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB9A194` | u16 |
| `uniqid` | `0xB9A1A4` | u64 |
| `num` | `0xB9A1BD` | u16 |
