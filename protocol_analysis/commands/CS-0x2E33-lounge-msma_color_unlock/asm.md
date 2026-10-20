# 汇编证据 —— CS-0x2E33-lounge-msma_color_unlock

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B98050 @ `0x00b98050`（`0x00b98050`..`0x00b98294`）
- 命令名字符串：`)<-_proto_lounge_client::send_msma_color_unlock(` @ `0xeebb4c`
- 声明容量：`0x12`（分配器指纹 @ `0xB98096`）

## 2. 组包块切片（游标初始化 → 提交）

```asm
00B980A4  call sub_ABB2F0
00B980A9  lea ecx, [ebp+12h]
00B980AC  lea eax, [ebp+2]
00B980AF  cmp eax, ecx
00B980B1  mov [esp+48h+var_4], 0
00B980B9  mov [esp+48h+var_30], ebp
00B980BD  mov dword ptr [esp+48h+var_2C], ecx
00B980C1  ja loc_B9827F
00B980C7  lea edx, [eax+8]
00B980CA  cmp edx, ecx
00B980CC  mov word ptr [ebp+0], 2E33h
00B980D2  ja loc_B9827F
00B980D8  mov esi, [esp+48h+arg_0]
00B980DC  mov [eax], esi
00B980DE  mov esi, [esp+48h+arg_4]
00B980E2  mov [eax+4], esi
00B980E5  lea eax, [edx+4]
00B980E8  cmp eax, ecx
00B980EA  ja loc_B9827F
00B980F0  mov ecx, [esp+48h+arg_8]
00B980F4  mov [edx], ecx
00B980F6  lea edx, [esp+48h+var_30]
00B980FA  mov [esp+48h+var_30], eax
00B980FE  push edx
00B980FF  lea eax, [esp+4Ch+arg_C]
00B98103  push eax
00B98104  call sub_B02D80
00B98109  add esp, 8
00B9810C  test al, al
00B9810E  jz loc_B9827F
00B98114  mov esi, [edi+7E2Ch]
00B9811A  test esi, esi
00B9811C  mov ebx, [esp+48h+var_30]
00B98120  jz loc_B98220
00B98126  lea ecx, [esp+48h+var_28]
00B9812A  push ecx
00B9812B  call sub_CA0CE0
00B98130  add esp, 4
00B98133  mov edx, [edi+8]
00B98136  push offset aProtoLoungeCli_461; ")<-_proto_lounge_client::send_msma_colo"...
00B9813B  push edx
00B9813C  push offset aId; " (id:"
00B98141  push eax
00B98142  push esi
00B98143  mov byte ptr [esp+5Ch+var_4], 1
00B98148  call sub_B03020
00B9814D  add esp, 8
00B98150  push eax
00B98151  call sub_41D990
00B98156  add esp, 8
00B98159  mov ecx, eax
00B9815B  call sub_ADC810
00B98160  push eax
00B98161  call sub_41D990
00B98166  add esp, 8
00B98169  lea ecx, [esp+48h+var_28]
00B9816D  mov byte ptr [esp+48h+var_4], 0
```

## 3. 发送去向切片（提交之后的实际发送）

```asm
00B98219  mov ecx, esi
00B9821B  call sub_40DDF0
00B98220  mov edx, [edi]
00B98222  mov eax, [edx+58h]
00B98225  sub ebx, ebp
00B98227  push ebx
00B98228  push ebp
00B98229  mov ecx, edi
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB980CC` | u16（2 字节） |
| `uniqid_ms` | `0xB980DC` | u64（8 字节） |
| `color_id` | `0xB980F4` | u32（4 字节） |
| `use_gp` | `0xB98104` | u32（4 字节） |
