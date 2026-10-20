# 汇编证据 —— CS-0x2EFF-lounge-xwar_booking_regist

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B913E0 @ `0x00b913e0`（`0x00b913e0`..`0x00b91722`）
- 命令名字符串：`)<-_proto_lounge_client::send_xwar_booking_regist(` @ `0xeeb050`
- 声明容量：`0x1E`（分配器指纹 @ `0xB91426`）

## 2. 组包块切片（游标初始化 → 提交）

```asm
00B91434  call sub_ABB2F0
00B91439  lea ecx, [ebp+1Eh]
00B9143C  lea eax, [ebp+2]
00B9143F  cmp eax, ecx
00B91441  mov [esp+48h+var_4], 0
00B91449  mov [esp+48h+var_30], ebp
00B9144D  mov dword ptr [esp+48h+var_2C], ecx
00B91451  ja loc_B9170D
00B91457  lea edx, [eax+4]
00B9145A  cmp edx, ecx
00B9145C  mov word ptr [ebp+0], 2EFFh
00B91462  ja loc_B9170D
00B91468  mov esi, [esp+48h+arg_0]
00B9146C  mov [eax], esi
00B9146E  mov eax, edx
00B91470  lea edx, [eax+4]
00B91473  cmp edx, ecx
00B91475  ja loc_B9170D
00B9147B  mov ecx, [esp+48h+arg_4]
00B9147F  mov [esp+48h+var_30], edx
00B91483  lea edx, [esp+48h+var_30]
00B91487  mov [eax], ecx
00B91489  push edx
00B9148A  lea eax, [esp+4Ch+arg_8]
00B9148E  push eax
00B9148F  call sub_B02D80
00B91494  add esp, 8
00B91497  test al, al
00B91499  jz loc_B9170D
00B9149F  lea ecx, [esp+48h+var_30]
00B914A3  push ecx
00B914A4  lea edx, [esp+4Ch+arg_C]
00B914A8  push edx
00B914A9  call sub_B02D80
00B914AE  add esp, 8
00B914B1  test al, al
00B914B3  jz loc_B9170D
00B914B9  lea eax, [esp+48h+var_30]
00B914BD  push eax
00B914BE  lea ecx, [esp+4Ch+arg_10]
00B914C2  push ecx
00B914C3  call sub_B02D80
00B914C8  add esp, 8
00B914CB  test al, al
00B914CD  jz loc_B9170D
00B914D3  lea edx, [esp+48h+var_30]
00B914D7  push edx
00B914D8  lea eax, [esp+4Ch+arg_14]
00B914DC  push eax
00B914DD  call sub_B02D80
00B914E2  add esp, 8
00B914E5  test al, al
00B914E7  jz loc_B9170D
00B914ED  lea ecx, [esp+48h+var_30]
00B914F1  push ecx
00B914F2  lea edx, [esp+4Ch+arg_18]
00B914F6  push edx
00B914F7  call sub_B02D80
00B914FC  add esp, 8
00B914FF  test al, al
00B91501  jz loc_B9170D
00B91507  mov esi, [edi+7C4Ch]
00B9150D  test esi, esi
00B9150F  mov ebx, [esp+48h+var_30]
00B91513  jz loc_B916AE
00B91519  lea eax, [esp+48h+var_28]
00B9151D  push eax
00B9151E  call sub_CA0CE0
00B91523  add esp, 4
00B91526  mov ecx, [edi+8]
00B91529  push offset aProtoLoungeCli_380; ")<-_proto_lounge_client::send_xwar_book"...
00B9152E  push ecx
00B9152F  push offset aId; " (id:"
00B91534  push eax
00B91535  push esi
00B91536  mov byte ptr [esp+5Ch+var_4], 1
00B9153B  call sub_B03020
00B91540  add esp, 8
00B91543  push eax
00B91544  call sub_41D990
00B91549  add esp, 8
00B9154C  mov ecx, eax
00B9154E  call sub_ADC810
00B91553  push eax
00B91554  call sub_41D990
00B91559  add esp, 8
00B9155C  lea ecx, [esp+48h+var_28]
00B91560  mov byte ptr [esp+48h+var_4], 0
```

## 3. 发送去向切片（提交之后的实际发送）

```asm
00B916A7  mov ecx, esi
00B916A9  call sub_40DDF0
00B916AE  mov edx, [edi]
00B916B0  mov eax, [edx+58h]
00B916B3  sub ebx, ebp
00B916B5  push ebx
00B916B6  push ebp
00B916B7  mov ecx, edi
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB9145C` | u16（2 字节） |
| `matching_type` | `0xB9146C` | u32（4 字节） |
| `matching_request_flag` | `0xB91487` | u32（4 字节） |
| `matching_battlerule_flag` | `0xB9148F` | u32（4 字节） |
| `matching_extrule_flag` | `0xB914A9` | u32（4 字节） |
| `mission_select_type` | `0xB914C3` | u32（4 字节） |
| `mission_select_value` | `0xB914DD` | u32（4 字节） |
| `client_bogo_version` | `0xB914F7` | u32（4 字节） |
