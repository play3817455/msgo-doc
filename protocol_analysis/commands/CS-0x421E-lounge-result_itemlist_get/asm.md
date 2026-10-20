# 汇编证据 —— CS-0x421E-lounge-result_itemlist_get

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B9EE30 @ `0x00b9ee30`（`0x00b9ee30`..`0x00b9efb6`）
- 命令名字符串：`)<-_proto_lounge_client::send_result_itemlist_get(` @ `0xeec658`
- 声明容量：`0x2`（分配器指纹 @ `0xB9EE76`）

## 2. 组包块切片（游标初始化 → 提交）

```asm
00B9EE84  call sub_ABB2F0
00B9EE89  mov word ptr [edi], 421Eh
00B9EE8E  mov ebp, [esi+802Ch]
00B9EE94  test ebp, ebp
00B9EE96  mov [esp+40h+var_4], 0
00B9EE9E  lea ebx, [edi+2]
00B9EEA1  jz loc_B9EF32
00B9EEA7  lea ecx, [esp+40h+var_28]
00B9EEAB  push ecx
00B9EEAC  call sub_CA0CE0
00B9EEB1  add esp, 4
00B9EEB4  mov edx, [esi+8]
00B9EEB7  push offset aProtoLoungeCli_554; ")<-_proto_lounge_client::send_result_it"...
00B9EEBC  push edx
00B9EEBD  push offset aId; " (id:"
00B9EEC2  push eax
00B9EEC3  push ebp
00B9EEC4  mov byte ptr [esp+54h+var_4], 1
00B9EEC9  call sub_B03020
00B9EECE  add esp, 8
00B9EED1  push eax
00B9EED2  call sub_41D990
00B9EED7  add esp, 8
00B9EEDA  mov ecx, eax
00B9EEDC  call sub_ADC810
00B9EEE1  push eax
00B9EEE2  call sub_41D990
00B9EEE7  add esp, 8
00B9EEEA  lea ecx, [esp+40h+var_28]
00B9EEEE  mov byte ptr [esp+40h+var_4], 0
```

## 3. 发送去向切片（提交之后的实际发送）

```asm
00B9EF2B  mov ecx, ebp
00B9EF2D  call sub_40DDF0
00B9EF32  mov edx, [esi]
00B9EF34  mov eax, [edx+58h]
00B9EF37  sub ebx, edi
00B9EF39  push ebx
00B9EF3A  push edi
00B9EF3B  mov ecx, esi
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB9EE89` | u16（2 字节） |
