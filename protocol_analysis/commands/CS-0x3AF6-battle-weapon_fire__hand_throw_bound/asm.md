# 汇编证据 —— CS-0x3AF6-battle-weapon_fire__hand_throw_bound

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B37F60 @ `0x00b37f60`（`0x00b37f60`..`0x00b38365`）
- 命令名字符串：`)<-_proto_battle_client::send_weapon_fire__hand_throw_bound(` @ `0xee0dc4`
- 声明容量：`0x2A`（分配器指纹 @ `0xB37FA6`）

## 2. 组包块切片（游标初始化 → 提交）

```asm
00B37FB4  call sub_ABB2F0
00B37FB9  lea ecx, [ebp+2Ah]
00B37FBC  lea eax, [ebp+2]
00B37FBF  cmp eax, ecx
00B37FC1  mov [esp+48h+var_4], 0
00B37FC9  mov [esp+48h+var_30], ebp
00B37FCD  mov dword ptr [esp+48h+var_2C], ecx
00B37FD1  ja loc_B38350
00B37FD7  lea edx, [eax+4]
00B37FDA  cmp edx, ecx
00B37FDC  mov word ptr [ebp+0], 3AF6h
00B37FE2  ja loc_B38350
00B37FE8  mov esi, [esp+48h+arg_0]
00B37FEC  mov [eax], esi
00B37FEE  mov eax, edx
00B37FF0  lea edx, [eax+4]
00B37FF3  cmp edx, ecx
00B37FF5  ja loc_B38350
00B37FFB  mov ecx, [esp+48h+arg_4]
00B37FFF  mov [esp+48h+var_30], edx
00B38003  lea edx, [esp+48h+var_30]
00B38007  mov [eax], ecx
00B38009  push edx
00B3800A  lea eax, [esp+4Ch+arg_8]
00B3800E  push eax
00B3800F  call sub_B02DA0
00B38014  add esp, 8
00B38017  test al, al
00B38019  jz loc_B38350
00B3801F  lea ecx, [esp+48h+var_30]
00B38023  push ecx
00B38024  lea edx, [esp+4Ch+arg_C]
00B38028  push edx
00B38029  call sub_B02DA0
00B3802E  add esp, 8
00B38031  test al, al
00B38033  jz loc_B38350
00B38039  lea eax, [esp+48h+var_30]
00B3803D  push eax
00B3803E  lea ecx, [esp+4Ch+arg_10]
00B38042  push ecx
00B38043  call sub_B02DA0
00B38048  add esp, 8
00B3804B  test al, al
00B3804D  jz loc_B38350
00B38053  lea edx, [esp+48h+var_30]
00B38057  push edx
00B38058  lea eax, [esp+4Ch+arg_14]
00B3805C  push eax
00B3805D  call sub_B02DA0
00B38062  add esp, 8
00B38065  test al, al
00B38067  jz loc_B38350
00B3806D  lea ecx, [esp+48h+var_30]
00B38071  push ecx
00B38072  lea edx, [esp+4Ch+arg_18]
00B38076  push edx
00B38077  call sub_B02DA0
00B3807C  add esp, 8
00B3807F  test al, al
00B38081  jz loc_B38350
00B38087  lea eax, [esp+48h+var_30]
00B3808B  push eax
00B3808C  lea ecx, [esp+4Ch+arg_1C]
00B38090  push ecx
00B38091  call sub_B02DA0
00B38096  add esp, 8
00B38099  test al, al
00B3809B  jz loc_B38350
00B380A1  lea edx, [esp+48h+var_30]
00B380A5  push edx
00B380A6  lea eax, [esp+4Ch+arg_20]
00B380AA  push eax
00B380AB  call sub_B02DA0
00B380B0  add esp, 8
00B380B3  test al, al
00B380B5  jz loc_B38350
00B380BB  lea ecx, [esp+48h+var_30]
00B380BF  push ecx
00B380C0  lea edx, [esp+4Ch+arg_24]
00B380C4  push edx
00B380C5  call sub_B02DA0
00B380CA  add esp, 8
00B380CD  test al, al
00B380CF  jz loc_B38350
00B380D5  mov esi, [edi+3DF4h]
00B380DB  test esi, esi
00B380DD  mov ebx, [esp+48h+var_30]
00B380E1  jz loc_B382F4
00B380E7  lea eax, [esp+48h+var_28]
00B380EB  push eax
00B380EC  call sub_CA0CE0
00B380F1  add esp, 4
00B380F4  mov ecx, [edi+8]
00B380F7  push offset aProtoBattleCli_266; ")<-_proto_battle_client::send_weapon_fi"...
00B380FC  push ecx
00B380FD  push offset aId; " (id:"
00B38102  push eax
00B38103  push esi
00B38104  mov byte ptr [esp+5Ch+var_4], 1
00B38109  call sub_B03020
00B3810E  add esp, 8
00B38111  push eax
00B38112  call sub_41D990
00B38117  add esp, 8
00B3811A  mov ecx, eax
00B3811C  call sub_ADC810
00B38121  push eax
00B38122  call sub_41D990
00B38127  add esp, 8
00B3812A  lea ecx, [esp+48h+var_28]
00B3812E  mov byte ptr [esp+48h+var_4], 0
```

## 3. 发送去向切片（提交之后的实际发送）

```asm
00B382ED  mov ecx, esi
00B382EF  call sub_40DDF0
00B382F4  mov edx, [edi]
00B382F6  mov eax, [edx+58h]
00B382F9  sub ebx, ebp
00B382FB  push ebx
00B382FC  push ebp
00B382FD  mov ecx, edi
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB37FDC` | u16（2 字节） |
| `frame_count` | `0xB37FEC` | u32（4 字节） |
| `grenade_id` | `0xB38007` | u32（4 字节） |
| `hit_x` | `0xB3800F` | u16（2 字节） |
| `hit_y` | `0xB38029` | u16（2 字节） |
| `hit_z` | `0xB38043` | u16（2 字节） |
| `vec_x` | `0xB3805D` | u16（2 字节） |
| `vec_y` | `0xB38077` | u16（2 字节） |
| `vec_z` | `0xB38091` | u16（2 字节） |
| `vec_power` | `0xB380AB` | u16（2 字节） |
| `AI_ent_id` | `0xB380C5` | u16（2 字节） |
