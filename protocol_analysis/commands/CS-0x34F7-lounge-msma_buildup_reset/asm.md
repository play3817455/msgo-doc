# 汇编证据 —— CS-0x34F7-lounge-msma_buildup_reset

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B96A70 @ `0x00b96a70`（`0x00b96a70`..`0x00b96c29`）
- 命令名字符串：`)<-_proto_lounge_client::send_msma_buildup_reset(` @ `0xeeb930`
- 声明容量：`0xA`（分配器指纹 @ `0xB96AB6`）

## 2. 组包块切片（游标初始化 → 提交）

```asm
00B96AC4  call sub_ABB2F0
00B96AC9  lea ecx, [ebp+0Ah]
00B96ACC  lea eax, [ebp+2]
00B96ACF  cmp eax, ecx
00B96AD1  mov [esp+40h+var_4], 0
00B96AD9  ja loc_B96C14
00B96ADF  lea ebx, [eax+8]
00B96AE2  cmp ebx, ecx
00B96AE4  mov word ptr [ebp+0], 34F7h
00B96AEA  ja loc_B96C14
00B96AF0  mov ecx, [esp+40h+arg_0]
00B96AF4  mov edx, [esp+40h+arg_4]
00B96AF8  mov [eax], ecx
00B96AFA  mov [eax+4], edx
00B96AFD  mov edi, [esi+7DE4h]
00B96B03  test edi, edi
00B96B05  jz loc_B96BB5
00B96B0B  lea eax, [esp+40h+var_28]
00B96B0F  push eax
00B96B10  call sub_CA0CE0
00B96B15  add esp, 4
00B96B18  mov ecx, [esi+8]
00B96B1B  push offset aProtoLoungeCli_454; ")<-_proto_lounge_client::send_msma_buil"...
00B96B20  push ecx
00B96B21  push offset aId; " (id:"
00B96B26  push eax
00B96B27  push edi
00B96B28  mov byte ptr [esp+54h+var_4], 1
00B96B2D  call sub_B03020
00B96B32  add esp, 8
00B96B35  push eax
00B96B36  call sub_41D990
00B96B3B  add esp, 8
00B96B3E  mov ecx, eax
00B96B40  call sub_ADC810
00B96B45  push eax
00B96B46  call sub_41D990
00B96B4B  add esp, 8
00B96B4E  lea ecx, [esp+40h+var_28]
00B96B52  mov byte ptr [esp+40h+var_4], 0
```

## 3. 发送去向切片（提交之后的实际发送）

```asm
00B96BAE  mov ecx, edi
00B96BB0  call sub_40DDF0
00B96BB5  mov edx, [esi]
00B96BB7  mov eax, [edx+58h]
00B96BBA  sub ebx, ebp
00B96BBC  push ebx
00B96BBD  push ebp
00B96BBE  mov ecx, esi
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB96AE4` | u16（2 字节） |
| `uniqid_ms` | `0xB96AF8` | u64（8 字节） |
