# 汇编证据 —— CS-0x7938-battle-roomlobby_pick_vote_cancel

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B32B40 @ `0xb32b40`（`0xb32b40`..`0xb32ce7`）
- 命令名字符串：`)<-_proto_battle_client::send_roomlobby_pick_vote_cancel(` @ `0xee0768`
- opcode 写入：`0xb32bb1`
- 声明容量：`0x6`（分配器容量 `push` @ `0xb32b83`）

## 2. 组包块切片（游标初始化 → 逐字段写线 → 提交）

```asm
  0xb32b87  mov     ebp, eax
  0xb32b89  mov     eax, [esi+0Ch]
  0xb32b8c  push    eax
  0xb32b8d  lea     ecx, [esp+44h+var_2C]
  0xb32b91  call    sub_ABB2F0
  0xb32b96  lea     ecx, [ebp+6]
  0xb32b99  lea     eax, [ebp+2]
  0xb32b9c  cmp     eax, ecx
  0xb32b9e  mov     [esp+40h+var_4], 0
  0xb32ba6  ja      loc_B32CD2
  0xb32bac  lea     ebx, [eax+4]
  0xb32baf  cmp     ebx, ecx
  0xb32bb1  mov     word ptr [ebp+0], 7938h
  0xb32bb7  ja      loc_B32CD2
  0xb32bbd  mov     ecx, [esp+40h+arg_0]
  0xb32bc1  mov     [eax], ecx
  0xb32bc3  mov     edi, [esi+3C70h]
  0xb32bc9  test    edi, edi
  0xb32bcb  jz      loc_B32C76
  0xb32bd1  lea     edx, [esp+40h+var_28]
  0xb32bd5  push    edx
  0xb32bd6  call    sub_CA0CE0
  0xb32bdb  add     esp, 4
  0xb32bde  mov     ecx, [esi+8]
  0xb32be1  push    offset aProtoBattleCli_230; ")<-_proto_battle_client::send_roomlobby"...
  0xb32be6  push    ecx
  0xb32be7  push    offset aId; " (id:"
  0xb32bec  push    eax
  0xb32bed  push    edi
  0xb32bee  mov     byte ptr [esp+54h+var_4], 1
  0xb32bf3  call    sub_B03020
  0xb32bf8  add     esp, 8
  0xb32bfb  push    eax
  0xb32bfc  call    sub_41D990
  0xb32c01  add     esp, 8
  0xb32c04  mov     ecx, eax
  0xb32c06  call    sub_ADC810
  0xb32c0b  push    eax
  0xb32c0c  call    sub_41D990
  0xb32c11  add     esp, 8
  0xb32c14  lea     ecx, [esp+40h+var_28]
  0xb32c18  mov     byte ptr [esp+40h+var_4], 0
  0xb32c1d  call    sub_B02FF0
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。
> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B02B40`=写 NUL 串（其**紧邻之前的 `push N`** = 串槽预算）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb32c27  push    offset aMsmaId; "msma_id="
  0xb32c3c  push    offset aByte; "]byte"
  0xb32c46  push    offset asc_EDAD58; " ) ["
```

## 4. 发送去向切片

```asm
  0xb32c78  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xb32bb1` | u16 |
| `msma_id` | `0xB32BC1` | u32 |
