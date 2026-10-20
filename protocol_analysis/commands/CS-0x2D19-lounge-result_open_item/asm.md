# 汇编证据 —— CS-0x2D19-lounge-result_open_item

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B9EAF0 @ `0x00b9eaf0`（`0x00b9eaf0`..`0x00b9ec9d`）
- 命令名字符串：`)<-_proto_lounge_client::send_result_open_item(` @ `0xeec5ec`
- 声明容量：`0x6`（分配器指纹 @ `0xB9EB36`）

## 2. 组包块切片（游标初始化 → 提交）

```asm
00B9EB44  call sub_ABB2F0
00B9EB49  lea ecx, [ebp+6]
00B9EB4C  lea eax, [ebp+2]
00B9EB4F  cmp eax, ecx
00B9EB51  mov [esp+40h+var_4], 0
00B9EB59  ja loc_B9EC88
00B9EB5F  lea ebx, [eax+4]
00B9EB62  cmp ebx, ecx
00B9EB64  mov word ptr [ebp+0], 2D19h
00B9EB6A  ja loc_B9EC88
00B9EB70  mov ecx, [esp+40h+arg_0]
00B9EB74  mov [eax], ecx
00B9EB76  mov edi, [esi+801Ch]
00B9EB7C  test edi, edi
00B9EB7E  jz loc_B9EC29
00B9EB84  lea edx, [esp+40h+var_28]
00B9EB88  push edx
00B9EB89  call sub_CA0CE0
00B9EB8E  add esp, 4
00B9EB91  mov ecx, [esi+8]
00B9EB94  push offset aProtoLoungeCli_553; ")<-_proto_lounge_client::send_result_op"...
00B9EB99  push ecx
00B9EB9A  push offset aId; " (id:"
00B9EB9F  push eax
00B9EBA0  push edi
00B9EBA1  mov byte ptr [esp+54h+var_4], 1
00B9EBA6  call sub_B03020
00B9EBAB  add esp, 8
00B9EBAE  push eax
00B9EBAF  call sub_41D990
00B9EBB4  add esp, 8
00B9EBB7  mov ecx, eax
00B9EBB9  call sub_ADC810
00B9EBBE  push eax
00B9EBBF  call sub_41D990
00B9EBC4  add esp, 8
00B9EBC7  lea ecx, [esp+40h+var_28]
00B9EBCB  mov byte ptr [esp+40h+var_4], 0
```

## 3. 发送去向切片（提交之后的实际发送）

```asm
00B9EC22  mov ecx, edi
00B9EC24  call sub_40DDF0
00B9EC29  mov edx, [esi]
00B9EC2B  mov eax, [edx+58h]
00B9EC2E  sub ebx, ebp
00B9EC30  push ebx
00B9EC31  push ebp
00B9EC32  mov ecx, esi
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB9EB64` | u16（2 字节） |
| `acc_index` | `0xB9EB74` | u32（4 字节） |
