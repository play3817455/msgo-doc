# 汇编证据 —— CS-0x3E0B-lounge-channel_list_get

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B898B0 @ `0x00b898b0`（`0x00b898b0`..`0x00b89a30`）
- 命令名字符串：`)<-_proto_lounge_client::send_channel_list_get(` @ `0xeea23c`
- 声明容量：`0x2`（分配器指纹 @ `0xB898F3`）

## 2. 组包块切片（游标初始化 → 提交）

```asm
00B89901  call sub_ABB2F0
00B89906  mov word ptr [edi], 3E0Bh
00B8990B  mov ebp, [esi+79C0h]
00B89911  test ebp, ebp
00B89913  mov [esp+40h+var_4], 0
00B8991B  lea ebx, [edi+2]
00B8991E  jz loc_B899AF
00B89924  lea ecx, [esp+40h+var_28]
00B89928  push ecx
00B89929  call sub_CA0CE0
00B8992E  add esp, 4
00B89931  mov edx, [esi+8]
00B89934  push offset aProtoLoungeCli_357; ")<-_proto_lounge_client::send_channel_l"...
00B89939  push edx
00B8993A  push offset aId; " (id:"
00B8993F  push eax
00B89940  push ebp
00B89941  mov byte ptr [esp+54h+var_4], 1
00B89946  call sub_B03020
00B8994B  add esp, 8
00B8994E  push eax
00B8994F  call sub_41D990
00B89954  add esp, 8
00B89957  mov ecx, eax
00B89959  call sub_ADC810
00B8995E  push eax
00B8995F  call sub_41D990
00B89964  add esp, 8
00B89967  lea ecx, [esp+40h+var_28]
00B8996B  mov byte ptr [esp+40h+var_4], 0
```

## 3. 发送去向切片（提交之后的实际发送）

```asm
00B899A8  mov ecx, ebp
00B899AA  call sub_40DDF0
00B899AF  mov edx, [esi]
00B899B1  mov eax, [edx+58h]
00B899B4  sub ebx, edi
00B899B6  push ebx
00B899B7  push edi
00B899B8  mov ecx, esi
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB89906` | u16（2 字节） |
