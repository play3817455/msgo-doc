# 汇编证据 —— CS-0x271F-battle-battleship_crash_impact

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B3FCD0 @ `0x00b3fcd0`（`0x00b3fcd0`..`0x00b3feba`）
- 命令名字符串：`)<-_proto_battle_client::send_battleship_crash_impact(` @ `0xee1734`
- 声明容量：`0xA`（分配器指纹 @ `0xB3FD16`）

## 2. 组包块切片（游标初始化 → 提交）

```asm
00B3FD24  call sub_ABB2F0
00B3FD29  lea ecx, [ebp+0Ah]
00B3FD2C  lea eax, [ebp+2]
00B3FD2F  cmp eax, ecx
00B3FD31  mov [esp+40h+var_4], 0
00B3FD39  ja loc_B3FEA5
00B3FD3F  lea edx, [eax+2]
00B3FD42  cmp edx, ecx
00B3FD44  mov word ptr [ebp+0], 271Fh
00B3FD4A  ja loc_B3FEA5
00B3FD50  mov si, word ptr [esp+40h+arg_0]
00B3FD55  lea ebx, [edx+2]
00B3FD58  cmp ebx, ecx
00B3FD5A  mov [eax], si
00B3FD5D  ja loc_B3FEA5
00B3FD63  mov cx, word ptr [esp+40h+arg_4]
00B3FD68  mov [edx], cx
00B3FD6B  mov esi, [edi+3FF8h]
00B3FD71  test esi, esi
00B3FD73  jz loc_B3FE46
00B3FD79  lea edx, [esp+40h+var_28]
00B3FD7D  push edx
00B3FD7E  call sub_CA0CE0
00B3FD83  add esp, 4
00B3FD86  mov ecx, [edi+8]
00B3FD89  push offset aProtoBattleCli_237; ")<-_proto_battle_client::send_battleshi"...
00B3FD8E  push ecx
00B3FD8F  push offset aId; " (id:"
00B3FD94  push eax
00B3FD95  push esi
00B3FD96  mov byte ptr [esp+54h+var_4], 1
00B3FD9B  call sub_B03020
00B3FDA0  add esp, 8
00B3FDA3  push eax
00B3FDA4  call sub_41D990
00B3FDA9  add esp, 8
00B3FDAC  mov ecx, eax
00B3FDAE  call sub_ADC810
00B3FDB3  push eax
00B3FDB4  call sub_41D990
00B3FDB9  add esp, 8
00B3FDBC  lea ecx, [esp+40h+var_28]
00B3FDC0  mov byte ptr [esp+40h+var_4], 0
```

## 3. 发送去向切片（提交之后的实际发送）

```asm
00B3FE3F  mov ecx, esi
00B3FE41  call sub_40DDF0
00B3FE46  mov edx, [edi]
00B3FE48  mov eax, [edx+58h]
00B3FE4B  sub ebx, ebp
00B3FE4D  push ebx
00B3FE4E  push ebp
00B3FE4F  mov ecx, edi
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB3FD44` | u16（2 字节） |
| `from_ent_id` | `0xB3FD5A` | u16（2 字节） |
| `to_ent_id` | `0xB3FD68` | u16（2 字节） |
