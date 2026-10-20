# 汇编证据 —— CS-0x3ED4-lounge-mail_get_present_body

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B9C320 @ `0x00b9c320`（`0x00b9c320`..`0x00b9c526`）
- 命令名字符串：`)<-_proto_lounge_client::send_mail_get_present_body(` @ `0xeec254`
- 声明容量：`0xE`（分配器指纹 @ `0xB9C366`）

## 2. 组包块切片（游标初始化 → 提交）

```asm
00B9C374  call sub_ABB2F0
00B9C379  lea ecx, [ebp+0Eh]
00B9C37C  lea eax, [ebp+2]
00B9C37F  cmp eax, ecx
00B9C381  mov [esp+48h+var_4], 0
00B9C389  mov [esp+48h+var_30], ebp
00B9C38D  mov dword ptr [esp+48h+var_2C], ecx
00B9C391  ja loc_B9C511
00B9C397  lea edx, [eax+4]
00B9C39A  cmp edx, ecx
00B9C39C  mov word ptr [ebp+0], 3ED4h
00B9C3A2  ja loc_B9C511
00B9C3A8  mov ecx, [esp+48h+arg_0]
00B9C3AC  mov [esp+48h+var_30], edx
00B9C3B0  lea edx, [esp+48h+var_30]
00B9C3B4  mov [eax], ecx
00B9C3B6  push edx
00B9C3B7  lea eax, [esp+4Ch+arg_4]
00B9C3BB  push eax
00B9C3BC  call sub_B06190
00B9C3C1  add esp, 8
00B9C3C4  test al, al
00B9C3C6  jz loc_B9C511
00B9C3CC  mov edi, [esi+7F68h]
00B9C3D2  test edi, edi
00B9C3D4  mov ebx, [esp+48h+var_30]
00B9C3D8  jz loc_B9C4B0
00B9C3DE  lea ecx, [esp+48h+var_28]
00B9C3E2  push ecx
00B9C3E3  call sub_CA0CE0
00B9C3E8  add esp, 4
00B9C3EB  mov edx, [esi+8]
00B9C3EE  push offset aProtoLoungeCli_548; ")<-_proto_lounge_client::send_mail_get_"...
00B9C3F3  push edx
00B9C3F4  push offset aId; " (id:"
00B9C3F9  push eax
00B9C3FA  push edi
00B9C3FB  mov byte ptr [esp+5Ch+var_4], 1
00B9C400  call sub_B03020
00B9C405  add esp, 8
00B9C408  push eax
00B9C409  call sub_41D990
00B9C40E  add esp, 8
00B9C411  mov ecx, eax
00B9C413  call sub_ADC810
00B9C418  push eax
00B9C419  call sub_41D990
00B9C41E  add esp, 8
00B9C421  lea ecx, [esp+48h+var_28]
00B9C425  mov byte ptr [esp+48h+var_4], 0
```

## 3. 发送去向切片（提交之后的实际发送）

```asm
00B9C4A9  mov ecx, edi
00B9C4AB  call sub_40DDF0
00B9C4B0  mov edx, [esi]
00B9C4B2  mov eax, [edx+58h]
00B9C4B5  mov edi, ebx
00B9C4B7  sub edi, ebp
00B9C4B9  push edi
00B9C4BA  push ebp
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB9C39C` | u16（2 字节） |
| `box_type` | `0xB9C3B4` | u32（4 字节） |
| `mailid` | `0xB9C3BC` | u64（8 字节） |
