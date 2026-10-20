# 汇编证据 —— CS-0x416D-lounge-item_sort_list

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B99F70 @ `0x00b99f70`（`0x00b99f70`..`0x00b9a11f`）
- 命令名字符串：`)<-_proto_lounge_client::send_item_sort_list(` @ `0xeebe90`
- 声明容量：`0x6`（分配器指纹 @ `0xB99FB6`）

## 2. 组包块切片（游标初始化 → 提交）

```asm
00B99FC4  call sub_ABB2F0
00B99FC9  lea ecx, [ebp+6]
00B99FCC  lea eax, [ebp+2]
00B99FCF  cmp eax, ecx
00B99FD1  mov [esp+40h+var_4], 0
00B99FD9  ja loc_B9A10A
00B99FDF  lea ebx, [eax+2]
00B99FE2  cmp ebx, ecx
00B99FE4  mov word ptr [ebp+0], 416Dh
00B99FEA  ja loc_B9A10A
00B99FF0  mov cx, word ptr [esp+40h+arg_0]
00B99FF5  mov [eax], cx
00B99FF8  mov edi, [esi+7EC4h]
00B99FFE  test edi, edi
00B9A000  jz loc_B9A0AB
00B9A006  lea edx, [esp+40h+var_28]
00B9A00A  push edx
00B9A00B  call sub_CA0CE0
00B9A010  add esp, 4
00B9A013  mov ecx, [esi+8]
00B9A016  push offset aProtoLoungeCli_574; ")<-_proto_lounge_client::send_item_sort"...
00B9A01B  push ecx
00B9A01C  push offset aId; " (id:"
00B9A021  push eax
00B9A022  push edi
00B9A023  mov byte ptr [esp+54h+var_4], 1
00B9A028  call sub_B03020
00B9A02D  add esp, 8
00B9A030  push eax
00B9A031  call sub_41D990
00B9A036  add esp, 8
00B9A039  mov ecx, eax
00B9A03B  call sub_ADC810
00B9A040  push eax
00B9A041  call sub_41D990
00B9A046  add esp, 8
00B9A049  lea ecx, [esp+40h+var_28]
00B9A04D  mov byte ptr [esp+40h+var_4], 0
```

## 3. 发送去向切片（提交之后的实际发送）

```asm
00B9A0A4  mov ecx, edi
00B9A0A6  call sub_40DDF0
00B9A0AB  mov edx, [esi]
00B9A0AD  mov eax, [edx+58h]
00B9A0B0  sub ebx, ebp
00B9A0B2  push ebx
00B9A0B3  push ebp
00B9A0B4  mov ecx, esi
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB99FE4` | u16（2 字节） |
| `inv_place` | `0xB99FF5` | u16（2 字节） |
