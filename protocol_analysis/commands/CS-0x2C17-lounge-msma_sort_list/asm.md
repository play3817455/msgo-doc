# 汇编证据 —— CS-0x2C17-lounge-msma_sort_list

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B95660 @ `0x00b95660`（`0x00b95660`..`0x00b95846`）
- 命令名字符串：`)<-_proto_lounge_client::send_msma_sort_list(` @ `0xeeb760`
- 声明容量：`0xA`（分配器指纹 @ `0xB956A6`）

## 2. 组包块切片（游标初始化 → 提交）

```asm
00B956B4  call sub_ABB2F0
00B956B9  lea ecx, [ebp+0Ah]
00B956BC  lea eax, [ebp+2]
00B956BF  cmp eax, ecx
00B956C1  mov [esp+40h+var_4], 0
00B956C9  ja loc_B95831
00B956CF  lea edx, [eax+4]
00B956D2  cmp edx, ecx
00B956D4  mov word ptr [ebp+0], 2C17h
00B956DA  ja loc_B95831
00B956E0  mov esi, [esp+40h+arg_0]
00B956E4  lea ebx, [edx+4]
00B956E7  cmp ebx, ecx
00B956E9  mov [eax], esi
00B956EB  ja loc_B95831
00B956F1  mov ecx, [esp+40h+arg_4]
00B956F5  mov [edx], ecx
00B956F7  mov esi, [edi+7D98h]
00B956FD  test esi, esi
00B956FF  jz loc_B957D2
00B95705  lea edx, [esp+40h+var_28]
00B95709  push edx
00B9570A  call sub_CA0CE0
00B9570F  add esp, 4
00B95712  mov ecx, [edi+8]
00B95715  push offset aProtoLoungeCli_569; ")<-_proto_lounge_client::send_msma_sort"...
00B9571A  push ecx
00B9571B  push offset aId; " (id:"
00B95720  push eax
00B95721  push esi
00B95722  mov byte ptr [esp+54h+var_4], 1
00B95727  call sub_B03020
00B9572C  add esp, 8
00B9572F  push eax
00B95730  call sub_41D990
00B95735  add esp, 8
00B95738  mov ecx, eax
00B9573A  call sub_ADC810
00B9573F  push eax
00B95740  call sub_41D990
00B95745  add esp, 8
00B95748  lea ecx, [esp+40h+var_28]
00B9574C  mov byte ptr [esp+40h+var_4], 0
```

## 3. 发送去向切片（提交之后的实际发送）

```asm
00B957CB  mov ecx, esi
00B957CD  call sub_40DDF0
00B957D2  mov edx, [edi]
00B957D4  mov eax, [edx+58h]
00B957D7  sub ebx, ebp
00B957D9  push ebx
00B957DA  push ebp
00B957DB  mov ecx, edi
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB956D4` | u16（2 字节） |
| `msma_sort_type` | `0xB956E9` | u32（4 字节） |
| `msma_sort_order` | `0xB956F5` | u32（4 字节） |
