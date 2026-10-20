# 汇编证据 —— CS-0x27B7-lounge-mail_sell_present

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B9C780 @ `0x00b9c780`（`0x00b9c780`..`0x00b9c9c4`）
- 命令名字符串：`)<-_proto_lounge_client::send_mail_sell_present(` @ `0xeec2c0`
- 声明容量：`0x12`（分配器指纹 @ `0xB9C7C6`）

## 2. 组包块切片（游标初始化 → 提交）

```asm
00B9C7D4  call sub_ABB2F0
00B9C7D9  lea ecx, [ebp+12h]
00B9C7DC  lea eax, [ebp+2]
00B9C7DF  cmp eax, ecx
00B9C7E1  mov [esp+48h+var_4], 0
00B9C7E9  mov [esp+48h+var_30], ebp
00B9C7ED  mov dword ptr [esp+48h+var_2C], ecx
00B9C7F1  ja loc_B9C9AF
00B9C7F7  lea edx, [eax+8]
00B9C7FA  cmp edx, ecx
00B9C7FC  mov word ptr [ebp+0], 27B7h
00B9C802  ja loc_B9C9AF
00B9C808  mov esi, [esp+48h+arg_0]
00B9C80C  mov [eax], esi
00B9C80E  mov esi, [esp+48h+arg_4]
00B9C812  mov [eax+4], esi
00B9C815  lea eax, [edx+4]
00B9C818  cmp eax, ecx
00B9C81A  ja loc_B9C9AF
00B9C820  mov ecx, [esp+48h+arg_8]
00B9C824  mov [edx], ecx
00B9C826  lea edx, [esp+48h+var_30]
00B9C82A  mov [esp+48h+var_30], eax
00B9C82E  push edx
00B9C82F  lea eax, [esp+4Ch+arg_C]
00B9C833  push eax
00B9C834  call sub_B02D80
00B9C839  add esp, 8
00B9C83C  test al, al
00B9C83E  jz loc_B9C9AF
00B9C844  mov esi, [edi+7F78h]
00B9C84A  test esi, esi
00B9C84C  mov ebx, [esp+48h+var_30]
00B9C850  jz loc_B9C950
00B9C856  lea ecx, [esp+48h+var_28]
00B9C85A  push ecx
00B9C85B  call sub_CA0CE0
00B9C860  add esp, 4
00B9C863  mov edx, [edi+8]
00B9C866  push offset aProtoLoungeCli_504; ")<-_proto_lounge_client::send_mail_sell"...
00B9C86B  push edx
00B9C86C  push offset aId; " (id:"
00B9C871  push eax
00B9C872  push esi
00B9C873  mov byte ptr [esp+5Ch+var_4], 1
00B9C878  call sub_B03020
00B9C87D  add esp, 8
00B9C880  push eax
00B9C881  call sub_41D990
00B9C886  add esp, 8
00B9C889  mov ecx, eax
00B9C88B  call sub_ADC810
00B9C890  push eax
00B9C891  call sub_41D990
00B9C896  add esp, 8
00B9C899  lea ecx, [esp+48h+var_28]
00B9C89D  mov byte ptr [esp+48h+var_4], 0
```

## 3. 发送去向切片（提交之后的实际发送）

```asm
00B9C949  mov ecx, esi
00B9C94B  call sub_40DDF0
00B9C950  mov edx, [edi]
00B9C952  mov eax, [edx+58h]
00B9C955  sub ebx, ebp
00B9C957  push ebx
00B9C958  push ebp
00B9C959  mov ecx, edi
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB9C7FC` | u16（2 字节） |
| `mailid` | `0xB9C80C` | u64（8 字节） |
| `attach_type` | `0xB9C824` | u32（4 字节） |
| `attach_id` | `0xB9C834` | u32（4 字节） |
