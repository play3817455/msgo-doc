# 汇编证据 —— CS-0x2761-battle-roomlobby_game_ready

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B32180 @ `0x00b32180`（`0x00b32180`..`0x00b32327`）
- 命令名字符串：`)<-_proto_battle_client::send_roomlobby_game_ready(` @ `0xee0624`
- 声明容量：`0x6`（分配器指纹 @ `0xB321C3`）

## 2. 组包块切片（游标初始化 → 提交）

```asm
00B321D1  call sub_ABB2F0
00B321D6  lea ecx, [ebp+6]
00B321D9  lea eax, [ebp+2]
00B321DC  cmp eax, ecx
00B321DE  mov [esp+40h+var_4], 0
00B321E6  ja loc_B32312
00B321EC  lea ebx, [eax+4]
00B321EF  cmp ebx, ecx
00B321F1  mov word ptr [ebp+0], 2761h
00B321F7  ja loc_B32312
00B321FD  mov ecx, [esp+40h+arg_0]
00B32201  mov [eax], ecx
00B32203  mov edi, [esi+3C40h]
00B32209  test edi, edi
00B3220B  jz loc_B322B6
00B32211  lea edx, [esp+40h+var_28]
00B32215  push edx
00B32216  call sub_CA0CE0
00B3221B  add esp, 4
00B3221E  mov ecx, [esi+8]
00B32221  push offset aProtoBattleCli_213; ")<-_proto_battle_client::send_roomlobby"...
00B32226  push ecx
00B32227  push offset aId; " (id:"
00B3222C  push eax
00B3222D  push edi
00B3222E  mov byte ptr [esp+54h+var_4], 1
00B32233  call sub_B03020
00B32238  add esp, 8
00B3223B  push eax
00B3223C  call sub_41D990
00B32241  add esp, 8
00B32244  mov ecx, eax
00B32246  call sub_ADC810
00B3224B  push eax
00B3224C  call sub_41D990
00B32251  add esp, 8
00B32254  lea ecx, [esp+40h+var_28]
00B32258  mov byte ptr [esp+40h+var_4], 0
```

## 3. 发送去向切片（提交之后的实际发送）

```asm
00B322AF  mov ecx, edi
00B322B1  call sub_40DDF0
00B322B6  mov edx, [esi]
00B322B8  mov eax, [edx+58h]
00B322BB  sub ebx, ebp
00B322BD  push ebx
00B322BE  push ebp
00B322BF  mov ecx, esi
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB321F1` | u16（2 字节） |
| `stat` | `0xB32201` | u32（4 字节） |
