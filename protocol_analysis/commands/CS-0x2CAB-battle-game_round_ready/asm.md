# 汇编证据 —— CS-0x2CAB-battle-game_round_ready

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B33680 @ `0x00b33680`（`0x00b33680`..`0x00b33803`）
- 命令名字符串：`)<-_proto_battle_client::send_game_round_ready(` @ `0xee08b4`
- 声明容量：`0x2`（分配器指纹 @ `0xB336C6`）

## 2. 组包块切片（游标初始化 → 提交）

```asm
00B336D4  call sub_ABB2F0
00B336D9  mov word ptr [edi], 2CABh
00B336DE  mov ebp, [esi+3CD4h]
00B336E4  test ebp, ebp
00B336E6  mov [esp+40h+var_4], 0
00B336EE  lea ebx, [edi+2]
00B336F1  jz loc_B33782
00B336F7  lea ecx, [esp+40h+var_28]
00B336FB  push ecx
00B336FC  call sub_CA0CE0
00B33701  add esp, 4
00B33704  mov edx, [esi+8]
00B33707  push offset aProtoBattleCli_219; ")<-_proto_battle_client::send_game_roun"...
00B3370C  push edx
00B3370D  push offset aId; " (id:"
00B33712  push eax
00B33713  push ebp
00B33714  mov byte ptr [esp+54h+var_4], 1
00B33719  call sub_B03020
00B3371E  add esp, 8
00B33721  push eax
00B33722  call sub_41D990
00B33727  add esp, 8
00B3372A  mov ecx, eax
00B3372C  call sub_ADC810
00B33731  push eax
00B33732  call sub_41D990
00B33737  add esp, 8
00B3373A  lea ecx, [esp+40h+var_28]
00B3373E  mov byte ptr [esp+40h+var_4], 0
```

## 3. 发送去向切片（提交之后的实际发送）

```asm
00B3377B  mov ecx, ebp
00B3377D  call sub_40DDF0
00B33782  mov edx, [esi]
00B33784  mov eax, [edx+58h]
00B33787  sub ebx, edi
00B33789  push ebx
00B3378A  push edi
00B3378B  mov ecx, esi
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB336D9` | u16（2 字节） |
