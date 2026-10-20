# 汇编证据 —— CS-0x6C48-battle-commander_candidacy_inbattle

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B3E050 @ `0xb3e050`（`0xb3e050`..`0xb3e1d6`）
- 命令名字符串：`)<-_proto_battle_client::send_commander_candidacy_inbattle(` @ `0xee1414`
- opcode 写入：`0xb3e0a9`
- 声明容量：`0x2`

## 2. 组包块切片（游标初始化 → 提交）

```asm
  0xb3e09a  mov     edi, eax
  0xb3e09c  mov     eax, [esi+0Ch]
  0xb3e09f  push    eax
  0xb3e0a0  lea     ecx, [esp+44h+var_2C]
  0xb3e0a4  call    sub_ABB2F0
  0xb3e0a9  mov     word ptr [edi], 6C48h
  0xb3e0ae  mov     ebp, [esi+3F54h]
  0xb3e0b4  test    ebp, ebp
  0xb3e0b6  mov     [esp+40h+var_4], 0
  0xb3e0be  lea     ebx, [edi+2]
  0xb3e0c1  jz      loc_B3E152
  0xb3e0c7  lea     ecx, [esp+40h+var_28]
  0xb3e0cb  push    ecx
  0xb3e0cc  call    sub_CA0CE0
  0xb3e0d1  add     esp, 4
  0xb3e0d4  mov     edx, [esi+8]
  0xb3e0d7  push    offset aProtoBattleCli_277; ")<-_proto_battle_client::send_commander"...
  0xb3e0dc  push    edx
  0xb3e0dd  push    offset aId; " (id:"
  0xb3e0e2  push    eax
  0xb3e0e3  push    ebp
  0xb3e0e4  mov     byte ptr [esp+54h+var_4], 1
  0xb3e0e9  call    sub_B03020
  0xb3e0ee  add     esp, 8
  0xb3e0f1  push    eax
  0xb3e0f2  call    sub_41D990
  0xb3e0f7  add     esp, 8
  0xb3e0fa  mov     ecx, eax
  0xb3e0fc  call    sub_ADC810
  0xb3e101  push    eax
  0xb3e102  call    sub_41D990
  0xb3e107  add     esp, 8
  0xb3e10a  lea     ecx, [esp+40h+var_28]
  0xb3e10e  mov     byte ptr [esp+40h+var_4], 0
  0xb3e113  call    sub_B02FF0   <<<COMMIT
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb3e118  push    offset aByte; "]byte"
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
```

## 4. 发送去向切片

```asm
  0xb3e154  mov     eax, [edx+58h]
  0xb3e157  sub     ebx, edi
  0xb3e159  push    ebx
  0xb3e15a  push    edi
  0xb3e15b  mov     ecx, esi
  0xb3e15d  call    eax
  0xb3e15f  test    al, al
  0xb3e161  jnz     short loc_B3E18A
  0xb3e163  lea     ecx, [esp+40h+var_2C]
  0xb3e167  mov     [esp+40h+var_4], 0FFFFFFFFh
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。
> 本批 50 条**全部命中同一去向槽 `vt[0x58]`**（与批次-16/17 一致）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB3E0A9` | u16 |
