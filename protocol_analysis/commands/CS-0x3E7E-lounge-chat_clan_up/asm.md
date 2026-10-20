# 汇编证据 —— CS-0x3E7E-lounge-chat_clan_up

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B8D1F0 @ `0x00b8d1f0`（`0x00b8d1f0`..`0x00b8d3cf`）
- 命令名字符串：`)<-_proto_lounge_client::send_chat_clan_up(` @ `0xeea8c0`
- 声明容量：`0xBA`（分配器指纹 @ `0xB8D236`）

## 2. 组包块切片（游标初始化 → 提交）

```asm
00B8D247  call sub_ABB2F0
00B8D24C  lea ecx, [edi+0BAh]
00B8D252  lea eax, [edi+2]
00B8D255  cmp eax, ecx
00B8D257  mov [esp+48h+var_4], 0
00B8D25F  mov [esp+48h+var_30], edi
00B8D263  mov dword ptr [esp+48h+var_2C], ecx
00B8D267  ja loc_B8D3BA
00B8D26D  mov edx, [esp+48h+arg_0]
00B8D271  push 0B5h
00B8D276  lea ecx, [esp+4Ch+var_30]
00B8D27A  push ecx
00B8D27B  push edx
00B8D27C  mov word ptr [edi], 3E7Eh
00B8D281  mov [esp+54h+var_30], eax
00B8D285  call sub_B02B40
00B8D28A  add esp, 0Ch
00B8D28D  test al, al
00B8D28F  jz loc_B8D3BA
00B8D295  mov ebp, [esi+7AECh]
00B8D29B  test ebp, ebp
00B8D29D  mov ebx, [esp+48h+var_30]
00B8D2A1  jz loc_B8D35C
00B8D2A7  lea eax, [esp+48h+var_28]
00B8D2AB  push eax
00B8D2AC  call sub_CA0CE0
00B8D2B1  add esp, 4
00B8D2B4  mov ecx, [esi+8]
00B8D2B7  push offset aProtoLoungeCli_413; ")<-_proto_lounge_client::send_chat_clan"...
00B8D2BC  push ecx
00B8D2BD  push offset aId; " (id:"
00B8D2C2  push eax
00B8D2C3  push ebp
00B8D2C4  mov byte ptr [esp+5Ch+var_4], 1
00B8D2C9  call sub_B03020
00B8D2CE  add esp, 8
00B8D2D1  push eax
00B8D2D2  call sub_41D990
00B8D2D7  add esp, 8
00B8D2DA  mov ecx, eax
00B8D2DC  call sub_ADC810
00B8D2E1  push eax
00B8D2E2  call sub_41D990
00B8D2E7  add esp, 8
00B8D2EA  lea ecx, [esp+48h+var_28]
00B8D2EE  mov byte ptr [esp+48h+var_4], 0
```

## 3. 发送去向切片（提交之后的实际发送）

```asm
00B8D355  mov ecx, ebp
00B8D357  call sub_40DDF0
00B8D35C  mov edx, [esi]
00B8D35E  mov eax, [edx+58h]
00B8D361  mov ebp, ebx
00B8D363  sub ebp, edi
00B8D365  push ebp
00B8D366  push edi
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB8D27C` | u16（2 字节） |
| `msg` | `0xB8D285` | str（变长） |
