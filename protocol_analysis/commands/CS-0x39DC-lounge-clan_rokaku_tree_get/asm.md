# 汇编证据 —— CS-0x39DC-lounge-clan_rokaku_tree_get

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_BA2890 @ `0x00ba2890`（`0x00ba2890`..`0x00ba2a76`）
- 命令名字符串：`)<-_proto_lounge_client::send_clan_rokaku_tree_get(` @ `0xeecc78`
- 声明容量：`0xA`（分配器指纹 @ `0xBA28D6`）

## 2. 组包块切片（游标初始化 → 提交）

```asm
00BA28E4  call sub_ABB2F0
00BA28E9  lea ecx, [ebp+0Ah]
00BA28EC  lea eax, [ebp+2]
00BA28EF  cmp eax, ecx
00BA28F1  mov [esp+40h+var_4], 0
00BA28F9  ja loc_BA2A61
00BA28FF  lea edx, [eax+4]
00BA2902  cmp edx, ecx
00BA2904  mov word ptr [ebp+0], 39DCh
00BA290A  ja loc_BA2A61
00BA2910  mov esi, [esp+40h+arg_0]
00BA2914  lea ebx, [edx+4]
00BA2917  cmp ebx, ecx
00BA2919  mov [eax], esi
00BA291B  ja loc_BA2A61
00BA2921  mov ecx, [esp+40h+arg_4]
00BA2925  mov [edx], ecx
00BA2927  mov esi, [edi+812Ch]
00BA292D  test esi, esi
00BA292F  jz loc_BA2A02
00BA2935  lea edx, [esp+40h+var_28]
00BA2939  push edx
00BA293A  call sub_CA0CE0
00BA293F  add esp, 4
00BA2942  mov ecx, [edi+8]
00BA2945  push offset aProtoLoungeCli_577; ")<-_proto_lounge_client::send_clan_roka"...
00BA294A  push ecx
00BA294B  push offset aId; " (id:"
00BA2950  push eax
00BA2951  push esi
00BA2952  mov byte ptr [esp+54h+var_4], 1
00BA2957  call sub_B03020
00BA295C  add esp, 8
00BA295F  push eax
00BA2960  call sub_41D990
00BA2965  add esp, 8
00BA2968  mov ecx, eax
00BA296A  call sub_ADC810
00BA296F  push eax
00BA2970  call sub_41D990
00BA2975  add esp, 8
00BA2978  lea ecx, [esp+40h+var_28]
00BA297C  mov byte ptr [esp+40h+var_4], 0
```

## 3. 发送去向切片（提交之后的实际发送）

```asm
00BA29FB  mov ecx, esi
00BA29FD  call sub_40DDF0
00BA2A02  mov edx, [edi]
00BA2A04  mov eax, [edx+58h]
00BA2A07  sub ebx, ebp
00BA2A09  push ebx
00BA2A0A  push ebp
00BA2A0B  mov ecx, edi
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xBA2904` | u16（2 字节） |
| `clan_id` | `0xBA2919` | u32（4 字节） |
| `page` | `0xBA2925` | u32（4 字节） |
