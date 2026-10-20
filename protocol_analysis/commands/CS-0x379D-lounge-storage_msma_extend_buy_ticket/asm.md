# 汇编证据 —— CS-0x379D-lounge-storage_msma_extend_buy_ticket

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_BA4110 @ `0x00ba4110`（`0x00ba4110`..`0x00ba4458`）
- 命令名字符串：`)<-_proto_lounge_client::send_storage_msma_extend_buy_ticket(` @ `0xeecf00`
- 声明容量：`0x1E`（分配器指纹 @ `0xBA4156`）

## 2. 组包块切片（游标初始化 → 提交）

```asm
00BA4164  call sub_ABB2F0
00BA4169  lea eax, [ebp+1Eh]
00BA416C  lea ecx, [ebp+2]
00BA416F  cmp ecx, eax
00BA4171  mov [esp+48h+var_4], 0
00BA4179  mov [esp+48h+var_30], ebp
00BA417D  mov dword ptr [esp+48h+var_2C], eax
00BA4181  ja loc_BA4443
00BA4187  lea edx, [ecx+4]
00BA418A  cmp edx, eax
00BA418C  mov word ptr [ebp+0], 379Dh
00BA4192  ja loc_BA4443
00BA4198  mov esi, dword ptr [esp+48h+arg_0]
00BA419C  mov [ecx], esi
00BA419E  lea ecx, [edx+1]
00BA41A1  cmp ecx, eax
00BA41A3  ja loc_BA4443
00BA41A9  mov al, byte ptr [esp+48h+arg_4]
00BA41AD  mov [esp+48h+var_30], ecx
00BA41B1  lea ecx, [esp+48h+var_30]
00BA41B5  mov [edx], al
00BA41B7  push ecx
00BA41B8  lea edx, [esp+4Ch+arg_8]
00BA41BC  push edx
00BA41BD  call sub_B02D80
00BA41C2  add esp, 8
00BA41C5  test al, al
00BA41C7  jz loc_BA4443
00BA41CD  lea eax, [esp+48h+var_30]
00BA41D1  push eax
00BA41D2  lea ecx, [esp+4Ch+arg_C]
00BA41D6  push ecx
00BA41D7  call sub_B061C0
00BA41DC  add esp, 8
00BA41DF  test al, al
00BA41E1  jz loc_BA4443
00BA41E7  lea edx, [esp+48h+var_30]
00BA41EB  push edx
00BA41EC  lea eax, [esp+4Ch+arg_10]
00BA41F0  push eax
00BA41F1  call sub_B061C0
00BA41F6  add esp, 8
00BA41F9  test al, al
00BA41FB  jz loc_BA4443
00BA4201  lea ecx, [esp+48h+var_30]
00BA4205  push ecx
00BA4206  lea edx, [esp+4Ch+arg_14]
00BA420A  push edx
00BA420B  call sub_B02D80
00BA4210  add esp, 8
00BA4213  test al, al
00BA4215  jz loc_BA4443
00BA421B  lea eax, [esp+48h+var_30]
00BA421F  push eax
00BA4220  lea ecx, [esp+4Ch+arg_18]
00BA4224  push ecx
00BA4225  call sub_B02D80
00BA422A  add esp, 8
00BA422D  test al, al
00BA422F  jz loc_BA4443
00BA4235  mov esi, [edi+8190h]
00BA423B  test esi, esi
00BA423D  mov ebx, [esp+48h+var_30]
00BA4241  jz loc_BA43E2
00BA4247  lea edx, [esp+48h+var_28]
00BA424B  push edx
00BA424C  call sub_CA0CE0
00BA4251  add esp, 4
00BA4254  mov ecx, [edi+8]
00BA4257  push offset aProtoLoungeCli_580; ")<-_proto_lounge_client::send_storage_m"...
00BA425C  push ecx
00BA425D  push offset aId; " (id:"
00BA4262  push eax
00BA4263  push esi
00BA4264  mov byte ptr [esp+5Ch+var_4], 1
00BA4269  call sub_B03020
00BA426E  add esp, 8
00BA4271  push eax
00BA4272  call sub_41D990
00BA4277  add esp, 8
00BA427A  mov ecx, eax
00BA427C  call sub_ADC810
00BA4281  push eax
00BA4282  call sub_41D990
00BA4287  add esp, 8
00BA428A  lea ecx, [esp+48h+var_28]
00BA428E  mov byte ptr [esp+48h+var_4], 0
```

## 3. 发送去向切片（提交之后的实际发送）

```asm
00BA43DB  mov ecx, esi
00BA43DD  call sub_40DDF0
00BA43E2  mov edx, [edi]
00BA43E4  mov eax, [edx+58h]
00BA43E7  mov esi, ebx
00BA43E9  sub esi, ebp
00BA43EB  push esi
00BA43EC  push ebp
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xBA418C` | u16（2 字节） |
| `shopitemid` | `0xBA419C` | u32（4 字节） |
| `id_type` | `0xBA41B5` | u8（1 字节） |
| `num` | `0xBA41BD` | u32（4 字节） |
| `tab_type` | `0xBA41D7` | u8（1 字节） |
| `is_cp` | `0xBA41F1` | u8（1 字节） |
| `total_price` | `0xBA420B` | u32（4 字节） |
| `extend_num` | `0xBA4225` | u32（4 字节） |
