# 汇编证据 —— CS-0x43F2-lounge-pilot_avatar_edit

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B8B8E0 @ `0x00b8b8e0`（`0x00b8b8e0`..`0x00b8bae4`）
- 命令名字符串：`)<-_proto_lounge_client::send_pilot_avatar_edit(` @ `0xeea5b0`
- 声明容量：`0x1A`（分配器指纹 @ `0xB8B926`）

## 2. 组包块切片（游标初始化 → 提交）

```asm
00B8B934  call sub_ABB2F0
00B8B939  lea ecx, [ebp+1Ah]
00B8B93C  lea eax, [ebp+2]
00B8B93F  cmp eax, ecx
00B8B941  mov [esp+48h+var_4], 0
00B8B949  mov [esp+48h+var_30], ebp
00B8B94D  mov dword ptr [esp+48h+var_2C], ecx
00B8B951  ja loc_B8BACF
00B8B957  mov edx, dword ptr [esp+48h+arg_0]
00B8B95B  lea ecx, [esp+48h+var_30]
00B8B95F  push ecx
00B8B960  push edx
00B8B961  mov word ptr [ebp+0], 43F2h
00B8B967  mov [esp+50h+var_30], eax
00B8B96B  call sub_B06290
00B8B970  add esp, 8
00B8B973  test al, al
00B8B975  jz loc_B8BACF
00B8B97B  mov eax, [esp+48h+var_30]
00B8B97F  lea ebx, [eax+1]
00B8B982  cmp ebx, dword ptr [esp+48h+var_2C]
00B8B986  ja loc_B8BACF
00B8B98C  mov cl, [esp+48h+arg_4]
00B8B990  mov [eax], cl
00B8B992  mov edi, [esi+7A60h]
00B8B998  test edi, edi
00B8B99A  jz loc_B8BA71
00B8B9A0  lea edx, [esp+48h+var_28]
00B8B9A4  push edx
00B8B9A5  call sub_CA0CE0
00B8B9AA  add esp, 4
00B8B9AD  mov ecx, [esi+8]
00B8B9B0  push offset aProtoLoungeCli_583; ")<-_proto_lounge_client::send_pilot_ava"...
00B8B9B5  push ecx
00B8B9B6  push offset aId; " (id:"
00B8B9BB  push eax
00B8B9BC  push edi
00B8B9BD  mov byte ptr [esp+5Ch+var_4], 1
00B8B9C2  call sub_B03020
00B8B9C7  add esp, 8
00B8B9CA  push eax
00B8B9CB  call sub_41D990
00B8B9D0  add esp, 8
00B8B9D3  mov ecx, eax
00B8B9D5  call sub_ADC810
00B8B9DA  push eax
00B8B9DB  call sub_41D990
00B8B9E0  add esp, 8
00B8B9E3  lea ecx, [esp+48h+var_28]
00B8B9E7  mov byte ptr [esp+48h+var_4], 0
```

## 3. 发送去向切片（提交之后的实际发送）

```asm
00B8BA6A  mov ecx, edi
00B8BA6C  call sub_40DDF0
00B8BA71  mov edx, [esi]
00B8BA73  mov eax, [edx+58h]
00B8BA76  mov edi, ebx
00B8BA78  sub edi, ebp
00B8BA7A  push edi
00B8BA7B  push ebp
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB8B961` | u16（2 字节） |
| `avatar` | `0xB8B96B` | struct（18 字节） |
| `is_reset` | `0xB8B990` | u8（1 字节） |

## 5. 复合写入器（结构体字段逐项证据）

- `sub_B06290`（`0x00B06290..0x00B0635C`）：字段构成 `4+1+1+1+2+4+1+1+1+2`，共 **18** 字节。
- 逐字段写线序列见取证记录（`ex1b` 中该函数全文）。
