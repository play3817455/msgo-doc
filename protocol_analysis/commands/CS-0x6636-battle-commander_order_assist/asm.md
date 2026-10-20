# 汇编证据 —— CS-0x6636-battle-commander_order_assist

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B3E3D0 @ `0xb3e3d0`（`0xb3e3d0`..`0xb3e57e`）
- 命令名字符串：`)<-_proto_battle_client::send_commander_order_assist(` @ `0xee148c`
- opcode 写入：`0xb3e444`
- 声明容量：`0x6`

## 2. 组包块切片（游标初始化 → 提交）

```asm
  0xb3e41a  mov     edi, eax
  0xb3e41c  mov     eax, [esi+0Ch]
  0xb3e41f  push    eax
  0xb3e420  lea     ecx, [esp+44h+var_2C]
  0xb3e424  call    sub_ABB2F0
  0xb3e429  lea     ecx, [edi+6]
  0xb3e42c  lea     eax, [edi+2]
  0xb3e42f  cmp     eax, ecx
  0xb3e431  mov     [esp+40h+var_4], 0
  0xb3e439  ja      loc_B3E569
  0xb3e43f  lea     ebx, [eax+1]
  0xb3e442  cmp     ebx, ecx
  0xb3e444  mov     word ptr [edi], 6636h
  0xb3e449  ja      loc_B3E569
  0xb3e44f  mov     cl, [esp+40h+arg_0]
  0xb3e453  mov     [eax], cl
  0xb3e455  mov     ebp, [esi+3F64h]
  0xb3e45b  test    ebp, ebp
  0xb3e45d  jz      loc_B3E50A
  0xb3e463  lea     edx, [esp+40h+var_28]
  0xb3e467  push    edx
  0xb3e468  call    sub_CA0CE0
  0xb3e46d  add     esp, 4
  0xb3e470  mov     ecx, [esi+8]
  0xb3e473  push    offset aProtoBattleCli_275; ")<-_proto_battle_client::send_commander"...
  0xb3e478  push    ecx
  0xb3e479  push    offset aId; " (id:"
  0xb3e47e  push    eax
  0xb3e47f  push    ebp
  0xb3e480  mov     byte ptr [esp+54h+var_4], 1
  0xb3e485  call    sub_B03020
  0xb3e48a  add     esp, 8
  0xb3e48d  push    eax
  0xb3e48e  call    sub_41D990
  0xb3e493  add     esp, 8
  0xb3e496  mov     ecx, eax
  0xb3e498  call    sub_ADC810
  0xb3e49d  push    eax
  0xb3e49e  call    sub_41D990
  0xb3e4a3  add     esp, 8
  0xb3e4a6  lea     ecx, [esp+40h+var_28]
  0xb3e4aa  mov     byte ptr [esp+40h+var_4], 0
  0xb3e4af  call    sub_B02FF0   <<<COMMIT
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb3e4b9  push    offset aType_0; "type="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb3e4d0  push    offset aByte; "]byte"
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
```

## 4. 发送去向切片

```asm
  0xb3e50c  mov     eax, [edx+58h]
  0xb3e50f  sub     ebx, edi
  0xb3e511  push    ebx
  0xb3e512  push    edi
  0xb3e513  mov     ecx, esi
  0xb3e515  call    eax
  0xb3e517  test    al, al
  0xb3e519  jz      short loc_B3E569
  0xb3e51b  mov     eax, [esi+3BF0h]
  0xb3e521  test    eax, eax
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。
> 本批 50 条**全部命中同一去向槽 `vt[0x58]`**（与批次-16/17 一致）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB3E444` | u16 |
| `type` | `0xB3E453` | u8 |
