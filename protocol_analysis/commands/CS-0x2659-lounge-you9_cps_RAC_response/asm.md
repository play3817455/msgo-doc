# 汇编证据 —— CS-0x2659-lounge-you9_cps_RAC_response

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_BA52E0 @ `0x00ba52e0`（`0x00ba52e0`..`0x00ba54c6`）
- 命令名字符串：`)<-_proto_lounge_client::send_you9_cps_RAC_response(` @ `0xeed0f8`
- 声明容量：`0xA`（分配器指纹 @ `0xBA5326`）

## 2. 组包块切片（游标初始化 → 提交）

```asm
00BA5334  call sub_ABB2F0
00BA5339  lea ecx, [ebp+0Ah]
00BA533C  lea eax, [ebp+2]
00BA533F  cmp eax, ecx
00BA5341  mov [esp+40h+var_4], 0
00BA5349  ja loc_BA54B1
00BA534F  lea edx, [eax+4]
00BA5352  cmp edx, ecx
00BA5354  mov word ptr [ebp+0], 2659h
00BA535A  ja loc_BA54B1
00BA5360  mov esi, [esp+40h+arg_0]
00BA5364  lea ebx, [edx+4]
00BA5367  cmp ebx, ecx
00BA5369  mov [eax], esi
00BA536B  ja loc_BA54B1
00BA5371  mov ecx, [esp+40h+arg_4]
00BA5375  mov [edx], ecx
00BA5377  mov esi, [edi+8220h]
00BA537D  test esi, esi
00BA537F  jz loc_BA5452
00BA5385  lea edx, [esp+40h+var_28]
00BA5389  push edx
00BA538A  call sub_CA0CE0
00BA538F  add esp, 4
00BA5392  mov ecx, [edi+8]
00BA5395  push offset aProtoLoungeCli_595; ")<-_proto_lounge_client::send_you9_cps_"...
00BA539A  push ecx
00BA539B  push offset aId; " (id:"
00BA53A0  push eax
00BA53A1  push esi
00BA53A2  mov byte ptr [esp+54h+var_4], 1
00BA53A7  call sub_B03020
00BA53AC  add esp, 8
00BA53AF  push eax
00BA53B0  call sub_41D990
00BA53B5  add esp, 8
00BA53B8  mov ecx, eax
00BA53BA  call sub_ADC810
00BA53BF  push eax
00BA53C0  call sub_41D990
00BA53C5  add esp, 8
00BA53C8  lea ecx, [esp+40h+var_28]
00BA53CC  mov byte ptr [esp+40h+var_4], 0
```

## 3. 发送去向切片（提交之后的实际发送）

```asm
00BA544B  mov ecx, esi
00BA544D  call sub_40DDF0
00BA5452  mov edx, [edi]
00BA5454  mov eax, [edx+58h]
00BA5457  sub ebx, ebp
00BA5459  push ebx
00BA545A  push ebp
00BA545B  mov ecx, edi
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xBA5354` | u16（2 字节） |
| `factor` | `0xBA5369` | u32（4 字节） |
| `cps_result` | `0xBA5375` | u32（4 字节） |
