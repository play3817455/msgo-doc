# 汇编证据 —— CS-0x3C26-lounge-item_buyback_delete_term_get

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B9A730 @ `0x00b9a730`（`0x00b9a730`..`0x00b9a8b6`）
- 命令名字符串：`)<-_proto_lounge_client::send_item_buyback_delete_term_get(` @ `0xeebf68`
- 声明容量：`0x2`（分配器指纹 @ `0xB9A776`）

## 2. 组包块切片（游标初始化 → 提交）

```asm
00B9A784  call sub_ABB2F0
00B9A789  mov word ptr [edi], 3C26h
00B9A78E  mov ebp, [esi+7EE4h]
00B9A794  test ebp, ebp
00B9A796  mov [esp+40h+var_4], 0
00B9A79E  lea ebx, [edi+2]
00B9A7A1  jz loc_B9A832
00B9A7A7  lea ecx, [esp+40h+var_28]
00B9A7AB  push ecx
00B9A7AC  call sub_CA0CE0
00B9A7B1  add esp, 4
00B9A7B4  mov edx, [esi+8]
00B9A7B7  push offset aProtoLoungeCli_526; ")<-_proto_lounge_client::send_item_buyb"...
00B9A7BC  push edx
00B9A7BD  push offset aId; " (id:"
00B9A7C2  push eax
00B9A7C3  push ebp
00B9A7C4  mov byte ptr [esp+54h+var_4], 1
00B9A7C9  call sub_B03020
00B9A7CE  add esp, 8
00B9A7D1  push eax
00B9A7D2  call sub_41D990
00B9A7D7  add esp, 8
00B9A7DA  mov ecx, eax
00B9A7DC  call sub_ADC810
00B9A7E1  push eax
00B9A7E2  call sub_41D990
00B9A7E7  add esp, 8
00B9A7EA  lea ecx, [esp+40h+var_28]
00B9A7EE  mov byte ptr [esp+40h+var_4], 0
```

## 3. 发送去向切片（提交之后的实际发送）

```asm
00B9A82B  mov ecx, ebp
00B9A82D  call sub_40DDF0
00B9A832  mov edx, [esi]
00B9A834  mov eax, [edx+58h]
00B9A837  sub ebx, edi
00B9A839  push ebx
00B9A83A  push edi
00B9A83B  mov ecx, esi
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB9A789` | u16（2 字节） |
