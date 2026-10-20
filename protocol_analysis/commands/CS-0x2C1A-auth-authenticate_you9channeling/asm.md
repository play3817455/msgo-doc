# 汇编证据 —— CS-0x2C1A-auth-authenticate_you9channeling

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B055D0 @ `0x00b055d0`（`0x00b055d0`..`0x00b058aa`）
- 命令名字符串：`)<-_proto_auth_client::send_authenticate_you9channeling(` @ `0xedb084`
- 声明容量：`0x146`（分配器指纹 @ `0xB05613`）

## 2. 组包块切片（游标初始化 → 提交）

```asm
00B05624  call sub_ABB2F0
00B05629  lea ecx, [ebp+146h]
00B0562F  lea eax, [ebp+2]
00B05632  cmp eax, ecx
00B05634  mov [esp+48h+var_4], 0
00B0563C  mov [esp+48h+var_30], ebp
00B05640  mov dword ptr [esp+48h+var_2C], ecx
00B05644  ja loc_B05895
00B0564A  mov edx, [esp+48h+arg_0]
00B0564E  push 20h ; ' '
00B05650  lea ecx, [esp+4Ch+var_30]
00B05654  push ecx
00B05655  push edx
00B05656  mov word ptr [ebp+0], 2C1Ah
00B0565C  mov [esp+54h+var_30], eax
00B05660  call sub_B02B40
00B05665  add esp, 0Ch
00B05668  test al, al
00B0566A  jz loc_B05895
00B05670  mov ecx, [esp+48h+arg_4]
00B05674  push 21h ; '!'
00B05676  lea eax, [esp+4Ch+var_30]
00B0567A  push eax
00B0567B  push ecx
00B0567C  call sub_B02B40
00B05681  add esp, 0Ch
00B05684  test al, al
00B05686  jz loc_B05895
00B0568C  mov eax, [esp+48h+arg_8]
00B05690  push 80h
00B05695  lea edx, [esp+4Ch+var_30]
00B05699  push edx
00B0569A  push eax
00B0569B  call sub_B02B40
00B056A0  add esp, 0Ch
00B056A3  test al, al
00B056A5  jz loc_B05895
00B056AB  mov edx, [esp+48h+arg_C]
00B056AF  push 80h
00B056B4  lea ecx, [esp+4Ch+var_30]
00B056B8  push ecx
00B056B9  push edx
00B056BA  call sub_B02B40
00B056BF  add esp, 0Ch
00B056C2  test al, al
00B056C4  jz loc_B05895
00B056CA  mov esi, [edi+3A8h]
00B056D0  test esi, esi
00B056D2  mov ebx, [esp+48h+var_30]
00B056D6  jz loc_B05839
00B056DC  lea eax, [esp+48h+var_28]
00B056E0  push eax
00B056E1  call sub_CA0CE0
00B056E6  add esp, 4
00B056E9  mov ecx, [edi+8]
00B056EC  push offset aProtoAuthClien_2; ")<-_proto_auth_client::send_authenticat"...
00B056F1  push ecx
00B056F2  push offset aId; " (id:"
00B056F7  push eax
00B056F8  push esi
00B056F9  mov byte ptr [esp+5Ch+var_4], 1
00B056FE  call sub_B03020
00B05703  add esp, 8
00B05706  push eax
00B05707  call sub_41D990
00B0570C  add esp, 8
00B0570F  mov ecx, eax
00B05711  call sub_ADC810
00B05716  push eax
00B05717  call sub_41D990
00B0571C  add esp, 8
00B0571F  lea ecx, [esp+48h+var_28]
00B05723  mov byte ptr [esp+48h+var_4], 0
```

## 3. 发送去向切片（提交之后的实际发送）

```asm
00B05832  mov ecx, esi
00B05834  call sub_40DDF0
00B05839  mov edx, [edi]
00B0583B  mov eax, [edx+58h]
00B0583E  sub ebx, ebp
00B05840  push ebx
00B05841  push ebp
00B05842  mov ecx, edi
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB05656` | u16（2 字节） |
| `ticket` | `0xB05660` | str（变长） |
| `channel` | `0xB0567C` | str（变长） |
| `disk_uuid` | `0xB0569B` | str（变长） |
| `mac_addr` | `0xB056BA` | str（变长） |
