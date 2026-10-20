# 汇编证据 —— CS-0x2830-lounge-channel_list_select

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B89A30 @ `0x00b89a30`（`0x00b89a30`..`0x00b89bd6`）
- 命令名字符串：`)<-_proto_lounge_client::send_channel_list_select(` @ `0xeea270`
- 声明容量：`0x6`（分配器指纹 @ `0xB89A73`）

## 2. 组包块切片（游标初始化 → 提交）

```asm
00B89A81  call sub_ABB2F0
00B89A86  lea ecx, [edi+6]
00B89A89  lea eax, [edi+2]
00B89A8C  cmp eax, ecx
00B89A8E  mov [esp+40h+var_4], 0
00B89A96  ja loc_B89BC1
00B89A9C  lea ebx, [eax+4]
00B89A9F  cmp ebx, ecx
00B89AA1  mov word ptr [edi], 2830h
00B89AA6  ja loc_B89BC1
00B89AAC  mov ecx, [esp+40h+arg_0]
00B89AB0  mov [eax], ecx
00B89AB2  mov ebp, [esi+79C8h]
00B89AB8  test ebp, ebp
00B89ABA  jz loc_B89B65
00B89AC0  lea edx, [esp+40h+var_28]
00B89AC4  push edx
00B89AC5  call sub_CA0CE0
00B89ACA  add esp, 4
00B89ACD  mov ecx, [esi+8]
00B89AD0  push offset aProtoLoungeCli_358; ")<-_proto_lounge_client::send_channel_l"...
00B89AD5  push ecx
00B89AD6  push offset aId; " (id:"
00B89ADB  push eax
00B89ADC  push ebp
00B89ADD  mov byte ptr [esp+54h+var_4], 1
00B89AE2  call sub_B03020
00B89AE7  add esp, 8
00B89AEA  push eax
00B89AEB  call sub_41D990
00B89AF0  add esp, 8
00B89AF3  mov ecx, eax
00B89AF5  call sub_ADC810
00B89AFA  push eax
00B89AFB  call sub_41D990
00B89B00  add esp, 8
00B89B03  lea ecx, [esp+40h+var_28]
00B89B07  mov byte ptr [esp+40h+var_4], 0
```

## 3. 发送去向切片（提交之后的实际发送）

```asm
00B89B5E  mov ecx, ebp
00B89B60  call sub_40DDF0
00B89B65  mov edx, [esi]
00B89B67  mov eax, [edx+58h]
00B89B6A  sub ebx, edi
00B89B6C  push ebx
00B89B6D  push edi
00B89B6E  mov ecx, esi
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB89AA1` | u16（2 字节） |
| `channel_id` | `0xB89AB0` | u32（4 字节） |
