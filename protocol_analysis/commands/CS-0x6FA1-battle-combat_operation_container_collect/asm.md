# 汇编证据 —— CS-0x6FA1-battle-combat_operation_container_collect

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B3F000 @ `0xb3f000`（`0xb3f000`..`0xb3f1ad`）
- 命令名字符串：`)<-_proto_battle_client::send_combat_operation_container_collect(` @ `0xee15c0`
- opcode 写入：`0xb3f074`
- 声明容量：`0x6`（分配器容量 `push` @ `0xb3f046`）

## 2. 组包块切片（游标初始化 → 逐字段写线 → 提交）

```asm
  0xb3f04a  mov     ebp, eax
  0xb3f04c  mov     eax, [esi+0Ch]
  0xb3f04f  push    eax
  0xb3f050  lea     ecx, [esp+44h+var_2C]
  0xb3f054  call    sub_ABB2F0
  0xb3f059  lea     ecx, [ebp+6]
  0xb3f05c  lea     eax, [ebp+2]
  0xb3f05f  cmp     eax, ecx
  0xb3f061  mov     [esp+40h+var_4], 0
  0xb3f069  ja      loc_B3F198
  0xb3f06f  lea     ebx, [eax+4]
  0xb3f072  cmp     ebx, ecx
  0xb3f074  mov     word ptr [ebp+0], 6FA1h
  0xb3f07a  ja      loc_B3F198
  0xb3f080  mov     ecx, [esp+40h+arg_0]
  0xb3f084  mov     [eax], ecx
  0xb3f086  mov     edi, [esi+3FC4h]
  0xb3f08c  test    edi, edi
  0xb3f08e  jz      loc_B3F139
  0xb3f094  lea     edx, [esp+40h+var_28]
  0xb3f098  push    edx
  0xb3f099  call    sub_CA0CE0
  0xb3f09e  add     esp, 4
  0xb3f0a1  mov     ecx, [esi+8]
  0xb3f0a4  push    offset aProtoBattleCli_286; ")<-_proto_battle_client::send_combat_op"...
  0xb3f0a9  push    ecx
  0xb3f0aa  push    offset aId; " (id:"
  0xb3f0af  push    eax
  0xb3f0b0  push    edi
  0xb3f0b1  mov     byte ptr [esp+54h+var_4], 1
  0xb3f0b6  call    sub_B03020
  0xb3f0bb  add     esp, 8
  0xb3f0be  push    eax
  0xb3f0bf  call    sub_41D990
  0xb3f0c4  add     esp, 8
  0xb3f0c7  mov     ecx, eax
  0xb3f0c9  call    sub_ADC810
  0xb3f0ce  push    eax
  0xb3f0cf  call    sub_41D990
  0xb3f0d4  add     esp, 8
  0xb3f0d7  lea     ecx, [esp+40h+var_28]
  0xb3f0db  mov     byte ptr [esp+40h+var_4], 0
  0xb3f0e0  call    sub_B02FF0
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。
> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B02B40`=写 NUL 串（其**紧邻之前的 `push N`** = 串槽预算）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb3f0ea  push    offset aDestination; "destination="
  0xb3f0ff  push    offset aByte; "]byte"
  0xb3f109  push    offset asc_EDAD58; " ) ["
```

## 4. 发送去向切片

```asm
  0xb3f13b  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xb3f074` | u16 |
| `destination` | `0xB3F084` | u32 |
