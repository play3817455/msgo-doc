# 汇编证据 —— CS-0x3FFF-lounge-msma_sp_parts_change

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B984F0 @ `0x00b984f0`（`0x00b984f0`..`0x00b98734`）
- 命令名字符串：`)<-_proto_lounge_client::send_msma_sp_parts_change(` @ `0xeebbb0`
- 声明容量：`0x12`（分配器指纹 @ `0xB98536`）

## 2. 组包块切片（游标初始化 → 提交）

```asm
00B98544  call sub_ABB2F0
00B98549  lea ecx, [ebp+12h]
00B9854C  lea eax, [ebp+2]
00B9854F  cmp eax, ecx
00B98551  mov [esp+48h+var_4], 0
00B98559  mov [esp+48h+var_30], ebp
00B9855D  mov dword ptr [esp+48h+var_2C], ecx
00B98561  ja loc_B9871F
00B98567  lea edx, [eax+8]
00B9856A  cmp edx, ecx
00B9856C  mov word ptr [ebp+0], 3FFFh
00B98572  ja loc_B9871F
00B98578  mov esi, [esp+48h+arg_0]
00B9857C  mov [eax], esi
00B9857E  mov esi, [esp+48h+arg_4]
00B98582  mov [eax+4], esi
00B98585  lea eax, [edx+4]
00B98588  cmp eax, ecx
00B9858A  ja loc_B9871F
00B98590  mov ecx, [esp+48h+arg_8]
00B98594  mov [edx], ecx
00B98596  lea edx, [esp+48h+var_30]
00B9859A  mov [esp+48h+var_30], eax
00B9859E  push edx
00B9859F  lea eax, [esp+4Ch+arg_C]
00B985A3  push eax
00B985A4  call sub_B02D80
00B985A9  add esp, 8
00B985AC  test al, al
00B985AE  jz loc_B9871F
00B985B4  mov esi, [edi+7E44h]
00B985BA  test esi, esi
00B985BC  mov ebx, [esp+48h+var_30]
00B985C0  jz loc_B986C0
00B985C6  lea ecx, [esp+48h+var_28]
00B985CA  push ecx
00B985CB  call sub_CA0CE0
00B985D0  add esp, 4
00B985D3  mov edx, [edi+8]
00B985D6  push offset aProtoLoungeCli_458; ")<-_proto_lounge_client::send_msma_sp_p"...
00B985DB  push edx
00B985DC  push offset aId; " (id:"
00B985E1  push eax
00B985E2  push esi
00B985E3  mov byte ptr [esp+5Ch+var_4], 1
00B985E8  call sub_B03020
00B985ED  add esp, 8
00B985F0  push eax
00B985F1  call sub_41D990
00B985F6  add esp, 8
00B985F9  mov ecx, eax
00B985FB  call sub_ADC810
00B98600  push eax
00B98601  call sub_41D990
00B98606  add esp, 8
00B98609  lea ecx, [esp+48h+var_28]
00B9860D  mov byte ptr [esp+48h+var_4], 0
```

## 3. 发送去向切片（提交之后的实际发送）

```asm
00B986B9  mov ecx, esi
00B986BB  call sub_40DDF0
00B986C0  mov edx, [edi]
00B986C2  mov eax, [edx+58h]
00B986C5  sub ebx, ebp
00B986C7  push ebx
00B986C8  push ebp
00B986C9  mov ecx, edi
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB9856C` | u16（2 字节） |
| `uniqid_ms` | `0xB9857C` | u64（8 字节） |
| `bef_sp_parts_id` | `0xB98594` | u32（4 字节） |
| `aft_sp_parts_id` | `0xB985A4` | u32（4 字节） |
