# 汇编证据 —— CS-0x2EE7-lounge-friend_xworld_search

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B9AF90 @ `0x00b9af90`（`0x00b9af90`..`0x00b9b169`）
- 命令名字符串：`)<-_proto_lounge_client::send_friend_xworld_search(` @ `0xeec088`
- 声明容量：`0x1E`（分配器指纹 @ `0xB9AFD6`）

## 2. 组包块切片（游标初始化 → 提交）

```asm
00B9AFE4  call sub_ABB2F0
00B9AFE9  lea ecx, [edi+1Eh]
00B9AFEC  lea eax, [edi+2]
00B9AFEF  cmp eax, ecx
00B9AFF1  mov [esp+48h+var_4], 0
00B9AFF9  mov [esp+48h+var_30], edi
00B9AFFD  mov dword ptr [esp+48h+var_2C], ecx
00B9B001  ja loc_B9B154
00B9B007  mov edx, [esp+48h+arg_0]
00B9B00B  push 19h
00B9B00D  lea ecx, [esp+4Ch+var_30]
00B9B011  push ecx
00B9B012  push edx
00B9B013  mov word ptr [edi], 2EE7h
00B9B018  mov [esp+54h+var_30], eax
00B9B01C  call sub_B02B40
00B9B021  add esp, 0Ch
00B9B024  test al, al
00B9B026  jz loc_B9B154
00B9B02C  mov ebp, [esi+7F20h]
00B9B032  test ebp, ebp
00B9B034  mov ebx, [esp+48h+var_30]
00B9B038  jz loc_B9B0F3
00B9B03E  lea eax, [esp+48h+var_28]
00B9B042  push eax
00B9B043  call sub_CA0CE0
00B9B048  add esp, 4
00B9B04B  mov ecx, [esi+8]
00B9B04E  push offset aProtoLoungeCli_381; ")<-_proto_lounge_client::send_friend_xw"...
00B9B053  push ecx
00B9B054  push offset aId; " (id:"
00B9B059  push eax
00B9B05A  push ebp
00B9B05B  mov byte ptr [esp+5Ch+var_4], 1
00B9B060  call sub_B03020
00B9B065  add esp, 8
00B9B068  push eax
00B9B069  call sub_41D990
00B9B06E  add esp, 8
00B9B071  mov ecx, eax
00B9B073  call sub_ADC810
00B9B078  push eax
00B9B079  call sub_41D990
00B9B07E  add esp, 8
00B9B081  lea ecx, [esp+48h+var_28]
00B9B085  mov byte ptr [esp+48h+var_4], 0
```

## 3. 发送去向切片（提交之后的实际发送）

```asm
00B9B0EC  mov ecx, ebp
00B9B0EE  call sub_40DDF0
00B9B0F3  mov edx, [esi]
00B9B0F5  mov eax, [edx+58h]
00B9B0F8  mov ebp, ebx
00B9B0FA  sub ebp, edi
00B9B0FC  push ebp
00B9B0FD  push edi
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB9B013` | u16（2 字节） |
| `to_pilot_name` | `0xB9B01C` | str（变长） |
