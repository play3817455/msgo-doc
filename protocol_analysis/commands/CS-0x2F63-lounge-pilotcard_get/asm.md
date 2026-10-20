# 汇编证据 —— CS-0x2F63-lounge-pilotcard_get

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B8E0A0 @ `0x00b8e0a0`（`0x00b8e0a0`..`0x00b8e283`）
- 命令名字符串：`)<-_proto_lounge_client::send_pilotcard_get(` @ `0xeeaa60`
- 声明容量：`0xA`（分配器指纹 @ `0xB8E0E6`）

## 2. 组包块切片（游标初始化 → 提交）

```asm
00B8E0F4  call sub_ABB2F0
00B8E0F9  lea ecx, [ebp+0Ah]
00B8E0FC  lea eax, [ebp+2]
00B8E0FF  cmp eax, ecx
00B8E101  mov [esp+40h+var_4], 0
00B8E109  ja loc_B8E26E
00B8E10F  lea edx, [eax+4]
00B8E112  cmp edx, ecx
00B8E114  mov word ptr [ebp+0], 2F63h
00B8E11A  ja loc_B8E26E
00B8E120  mov esi, [esp+40h+arg_0]
00B8E124  lea ebx, [edx+4]
00B8E127  cmp ebx, ecx
00B8E129  mov [eax], esi
00B8E12B  ja loc_B8E26E
00B8E131  mov ecx, [esp+40h+arg_4]
00B8E135  mov [edx], ecx
00B8E137  mov esi, [edi+7B44h]
00B8E13D  test esi, esi
00B8E13F  jz loc_B8E212
00B8E145  lea edx, [esp+40h+var_28]
00B8E149  push edx
00B8E14A  call sub_CA0CE0
00B8E14F  add esp, 4
00B8E152  mov ecx, [edi+8]
00B8E155  push offset aProtoLoungeCli_361; ")<-_proto_lounge_client::send_pilotcard"...
00B8E15A  push ecx
00B8E15B  push offset aId; " (id:"
00B8E160  push eax
00B8E161  push esi
00B8E162  mov byte ptr [esp+54h+var_4], 1
00B8E167  call sub_B03020
00B8E16C  add esp, 8
00B8E16F  push eax
00B8E170  call sub_41D990
00B8E175  add esp, 8
00B8E178  mov ecx, eax
00B8E17A  call sub_ADC810
00B8E17F  push eax
00B8E180  call sub_41D990
00B8E185  add esp, 8
00B8E188  lea ecx, [esp+40h+var_28]
00B8E18C  mov byte ptr [esp+40h+var_4], 0
```

## 3. 发送去向切片（提交之后的实际发送）

```asm
00B8E20B  mov ecx, esi
00B8E20D  call sub_40DDF0
00B8E212  mov edx, [edi]
00B8E214  mov eax, [edx+58h]
00B8E217  sub ebx, ebp
00B8E219  push ebx
00B8E21A  push ebp
00B8E21B  mov ecx, edi
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB8E114` | u16（2 字节） |
| `pilot_id` | `0xB8E129` | u32（4 字节） |
| `world_id` | `0xB8E135` | u32（4 字节） |
