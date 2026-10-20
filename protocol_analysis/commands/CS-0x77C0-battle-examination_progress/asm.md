# 汇编证据 —— CS-0x77C0-battle-examination_progress

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B40070 @ `0xb40070`（`0xb40070`..`0xb401f6`）
- 命令名字符串：`)<-_proto_battle_client::send_examination_progress(` @ `0xee17a4`
- opcode 写入：`0xb400c9`
- 声明容量：`0x2`（分配器容量 `push` @ `0xb400b6`）

## 2. 组包块切片（游标初始化 → 逐字段写线 → 提交）

```asm
  0xb400ba  mov     edi, eax
  0xb400bc  mov     eax, [esi+0Ch]
  0xb400bf  push    eax
  0xb400c0  lea     ecx, [esp+44h+var_2C]
  0xb400c4  call    sub_ABB2F0
  0xb400c9  mov     word ptr [edi], 77C0h
  0xb400ce  mov     ebp, [esi+4030h]
  0xb400d4  test    ebp, ebp
  0xb400d6  mov     [esp+40h+var_4], 0
  0xb400de  lea     ebx, [edi+2]
  0xb400e1  jz      loc_B40172
  0xb400e7  lea     ecx, [esp+40h+var_28]
  0xb400eb  push    ecx
  0xb400ec  call    sub_CA0CE0
  0xb400f1  add     esp, 4
  0xb400f4  mov     edx, [esi+8]
  0xb400f7  push    offset aProtoBattleCli_283; ")<-_proto_battle_client::send_examinati"...
  0xb400fc  push    edx
  0xb400fd  push    offset aId; " (id:"
  0xb40102  push    eax
  0xb40103  push    ebp
  0xb40104  mov     byte ptr [esp+54h+var_4], 1
  0xb40109  call    sub_B03020
  0xb4010e  add     esp, 8
  0xb40111  push    eax
  0xb40112  call    sub_41D990
  0xb40117  add     esp, 8
  0xb4011a  mov     ecx, eax
  0xb4011c  call    sub_ADC810
  0xb40121  push    eax
  0xb40122  call    sub_41D990
  0xb40127  add     esp, 8
  0xb4012a  lea     ecx, [esp+40h+var_28]
  0xb4012e  mov     byte ptr [esp+40h+var_4], 0
  0xb40133  call    sub_B02FF0
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。
> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B02B40`=写 NUL 串（其**紧邻之前的 `push N`** = 串槽预算）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb40138  push    offset aByte; "]byte"
  0xb40142  push    offset asc_EDAD58; " ) ["
```

## 4. 发送去向切片

```asm
  0xb40174  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xb400c9` | u16 |
