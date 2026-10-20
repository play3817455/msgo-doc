# 汇编证据 —— CS-0x34A9-auth-proto_version_check

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B04C70 @ `0x00b04c70`（`0x00b04c70`..`0x00b04ea6`）
- 命令名字符串：`)<-_proto_auth_client::send_proto_version_check(` @ `0xedafac`
- 声明容量：`0xE`（分配器指纹 @ `0xB04CB3`）

## 2. 组包块切片（游标初始化 → 提交）

```asm
00B04CC1  call sub_ABB2F0
00B04CC6  lea ecx, [ebp+0Eh]
00B04CC9  lea eax, [ebp+2]
00B04CCC  cmp eax, ecx
00B04CCE  mov [esp+48h+var_4], 0
00B04CD6  mov [esp+48h+var_30], ebp
00B04CDA  mov dword ptr [esp+48h+var_2C], ecx
00B04CDE  ja loc_B04E91
00B04CE4  lea edx, [eax+4]
00B04CE7  cmp edx, ecx
00B04CE9  mov word ptr [ebp+0], 34A9h
00B04CEF  ja loc_B04E91
00B04CF5  mov esi, [esp+48h+arg_0]
00B04CF9  mov [eax], esi
00B04CFB  mov eax, edx
00B04CFD  lea edx, [eax+4]
00B04D00  cmp edx, ecx
00B04D02  ja loc_B04E91
00B04D08  mov ecx, [esp+48h+arg_4]
00B04D0C  mov [esp+48h+var_30], edx
00B04D10  lea edx, [esp+48h+var_30]
00B04D14  mov [eax], ecx
00B04D16  push edx
00B04D17  lea eax, [esp+4Ch+arg_8]
00B04D1B  push eax
00B04D1C  call sub_B02D80
00B04D21  add esp, 8
00B04D24  test al, al
00B04D26  jz loc_B04E91
00B04D2C  mov esi, [edi+388h]
00B04D32  test esi, esi
00B04D34  mov ebx, [esp+48h+var_30]
00B04D38  jz loc_B04E33
00B04D3E  lea ecx, [esp+48h+var_28]
00B04D42  push ecx
00B04D43  call sub_CA0CE0
00B04D48  add esp, 4
00B04D4B  mov edx, [edi+8]
00B04D4E  push offset aProtoAuthClien_14; ")<-_proto_auth_client::send_proto_versi"...
00B04D53  push edx
00B04D54  push offset aId; " (id:"
00B04D59  push eax
00B04D5A  push esi
00B04D5B  mov byte ptr [esp+5Ch+var_4], 1
00B04D60  call sub_B03020
00B04D65  add esp, 8
00B04D68  push eax
00B04D69  call sub_41D990
00B04D6E  add esp, 8
00B04D71  mov ecx, eax
00B04D73  call sub_ADC810
00B04D78  push eax
00B04D79  call sub_41D990
00B04D7E  add esp, 8
00B04D81  lea ecx, [esp+48h+var_28]
00B04D85  mov byte ptr [esp+48h+var_4], 0
```

## 3. 发送去向切片（提交之后的实际发送）

```asm
00B04E2C  mov ecx, esi
00B04E2E  call sub_40DDF0
00B04E33  mov edx, [edi]
00B04E35  mov eax, [edx+58h]
00B04E38  mov esi, ebx
00B04E3A  sub esi, ebp
00B04E3C  push esi
00B04E3D  push ebp
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB04CE9` | u16（2 字节） |
| `version` | `0xB04CF9` | u32（4 字节） |
| `crc` | `0xB04D14` | u32（4 字节） |
| `gentime` | `0xB04D1C` | u32（4 字节） |
