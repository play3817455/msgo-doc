# 汇编证据 —— CS-0x7E45-battle-roomlobby_pick_vote

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B32990 @ `0xb32990`（`0xb32990`..`0xb32b37`）
- 命令名字符串：`)<-_proto_battle_client::send_roomlobby_pick_vote(` @ `0xee0734`
- opcode 写入：`0xb32a01`
- 声明容量：`0x6`（分配器容量 `push` @ `0xb329d3`）

## 2. 组包块切片（游标初始化 → 逐字段写线 → 提交）

```asm
  0xb329d7  mov     ebp, eax
  0xb329d9  mov     eax, [esi+0Ch]
  0xb329dc  push    eax
  0xb329dd  lea     ecx, [esp+44h+var_2C]
  0xb329e1  call    sub_ABB2F0
  0xb329e6  lea     ecx, [ebp+6]
  0xb329e9  lea     eax, [ebp+2]
  0xb329ec  cmp     eax, ecx
  0xb329ee  mov     [esp+40h+var_4], 0
  0xb329f6  ja      loc_B32B22
  0xb329fc  lea     ebx, [eax+4]
  0xb329ff  cmp     ebx, ecx
  0xb32a01  mov     word ptr [ebp+0], 7E45h
  0xb32a07  ja      loc_B32B22
  0xb32a0d  mov     ecx, [esp+40h+arg_0]
  0xb32a11  mov     [eax], ecx
  0xb32a13  mov     edi, [esi+3C68h]
  0xb32a19  test    edi, edi
  0xb32a1b  jz      loc_B32AC6
  0xb32a21  lea     edx, [esp+40h+var_28]
  0xb32a25  push    edx
  0xb32a26  call    sub_CA0CE0
  0xb32a2b  add     esp, 4
  0xb32a2e  mov     ecx, [esi+8]
  0xb32a31  push    offset aProtoBattleCli_229; ")<-_proto_battle_client::send_roomlobby"...
  0xb32a36  push    ecx
  0xb32a37  push    offset aId; " (id:"
  0xb32a3c  push    eax
  0xb32a3d  push    edi
  0xb32a3e  mov     byte ptr [esp+54h+var_4], 1
  0xb32a43  call    sub_B03020
  0xb32a48  add     esp, 8
  0xb32a4b  push    eax
  0xb32a4c  call    sub_41D990
  0xb32a51  add     esp, 8
  0xb32a54  mov     ecx, eax
  0xb32a56  call    sub_ADC810
  0xb32a5b  push    eax
  0xb32a5c  call    sub_41D990
  0xb32a61  add     esp, 8
  0xb32a64  lea     ecx, [esp+40h+var_28]
  0xb32a68  mov     byte ptr [esp+40h+var_4], 0
  0xb32a6d  call    sub_B02FF0
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。
> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B02B40`=写 NUL 串（其**紧邻之前的 `push N`** = 串槽预算）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb32a77  push    offset aMsmaId; "msma_id="
  0xb32a8c  push    offset aByte; "]byte"
  0xb32a96  push    offset asc_EDAD58; " ) ["
```

## 4. 发送去向切片

```asm
  0xb32ac8  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xb32a01` | u16 |
| `msma_id` | `0xB32A11` | u32 |
