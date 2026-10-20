# 汇编证据 —— CS-0x2ADC-battle-weapon_fire__wrestle

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B36EC0 @ `0x00b36ec0`（`0x00b36ec0`..`0x00b372cb`）
- 命令名字符串：`)<-_proto_battle_client::send_weapon_fire__wrestle(` @ `0xee0d1c`
- 声明容量：`0x2A`（分配器指纹 @ `0xB36F06`）

## 2. 组包块切片（游标初始化 → 提交）

```asm
00B36F14  call sub_ABB2F0
00B36F19  lea eax, [ebp+2Ah]
00B36F1C  lea ecx, [ebp+2]
00B36F1F  cmp ecx, eax
00B36F21  mov [esp+48h+var_4], 0
00B36F29  mov [esp+48h+var_30], ebp
00B36F2D  mov dword ptr [esp+48h+var_2C], eax
00B36F31  ja loc_B372B6
00B36F37  lea edx, [ecx+4]
00B36F3A  cmp edx, eax
00B36F3C  mov word ptr [ebp+0], 2ADCh
00B36F42  ja loc_B372B6
00B36F48  mov esi, [esp+48h+arg_0]
00B36F4C  mov [ecx], esi
00B36F4E  lea ecx, [edx+2]
00B36F51  cmp ecx, eax
00B36F53  ja loc_B372B6
00B36F59  mov ax, word ptr [esp+48h+arg_4]
00B36F5E  mov [esp+48h+var_30], ecx
00B36F62  lea ecx, [esp+48h+var_30]
00B36F66  mov [edx], ax
00B36F69  push ecx
00B36F6A  lea edx, [esp+4Ch+arg_8]
00B36F6E  push edx
00B36F6F  call sub_B02DA0
00B36F74  add esp, 8
00B36F77  test al, al
00B36F79  jz loc_B372B6
00B36F7F  lea eax, [esp+48h+var_30]
00B36F83  push eax
00B36F84  lea ecx, [esp+4Ch+arg_C]
00B36F88  push ecx
00B36F89  call sub_B02DA0
00B36F8E  add esp, 8
00B36F91  test al, al
00B36F93  jz loc_B372B6
00B36F99  lea edx, [esp+48h+var_30]
00B36F9D  push edx
00B36F9E  lea eax, [esp+4Ch+arg_10]
00B36FA2  push eax
00B36FA3  call sub_B02D80
00B36FA8  add esp, 8
00B36FAB  test al, al
00B36FAD  jz loc_B372B6
00B36FB3  lea ecx, [esp+48h+var_30]
00B36FB7  push ecx
00B36FB8  lea edx, [esp+4Ch+arg_14]
00B36FBC  push edx
00B36FBD  call sub_B061C0
00B36FC2  add esp, 8
00B36FC5  test al, al
00B36FC7  jz loc_B372B6
00B36FCD  lea eax, [esp+48h+var_30]
00B36FD1  push eax
00B36FD2  lea ecx, [esp+4Ch+arg_18]
00B36FD6  push ecx
00B36FD7  call sub_B02DA0
00B36FDC  add esp, 8
00B36FDF  test al, al
00B36FE1  jz loc_B372B6
00B36FE7  lea edx, [esp+48h+var_30]
00B36FEB  push edx
00B36FEC  lea eax, [esp+4Ch+arg_1C]
00B36FF0  push eax
00B36FF1  call sub_B061C0
00B36FF6  add esp, 8
00B36FF9  test al, al
00B36FFB  jz loc_B372B6
00B37001  lea ecx, [esp+48h+var_30]
00B37005  push ecx
00B37006  lea edx, [esp+4Ch+arg_20]
00B3700A  push edx
00B3700B  call sub_B02DA0
00B37010  add esp, 8
00B37013  test al, al
00B37015  jz loc_B372B6
00B3701B  lea eax, [esp+48h+var_30]
00B3701F  push eax
00B37020  lea ecx, [esp+4Ch+arg_24]
00B37024  push ecx
00B37025  call sub_B061C0
00B3702A  add esp, 8
00B3702D  test al, al
00B3702F  jz loc_B372B6
00B37035  mov esi, [edi+3DD8h]
00B3703B  test esi, esi
00B3703D  mov ebx, [esp+48h+var_30]
00B37041  jz loc_B3725A
00B37047  lea edx, [esp+48h+var_28]
00B3704B  push edx
00B3704C  call sub_CA0CE0
00B37051  add esp, 4
00B37054  mov ecx, [edi+8]
00B37057  push offset aProtoBattleCli_250; ")<-_proto_battle_client::send_weapon_fi"...
00B3705C  push ecx
00B3705D  push offset aId; " (id:"
00B37062  push eax
00B37063  push esi
00B37064  mov byte ptr [esp+5Ch+var_4], 1
00B37069  call sub_B03020
00B3706E  add esp, 8
00B37071  push eax
00B37072  call sub_41D990
00B37077  add esp, 8
00B3707A  mov ecx, eax
00B3707C  call sub_ADC810
00B37081  push eax
00B37082  call sub_41D990
00B37087  add esp, 8
00B3708A  lea ecx, [esp+48h+var_28]
00B3708E  mov byte ptr [esp+48h+var_4], 0
```

## 3. 发送去向切片（提交之后的实际发送）

```asm
00B37253  mov ecx, esi
00B37255  call sub_40DDF0
00B3725A  mov edx, [edi]
00B3725C  mov eax, [edx+58h]
00B3725F  sub ebx, ebp
00B37261  push ebx
00B37262  push ebp
00B37263  mov ecx, edi
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB36F3C` | u16（2 字节） |
| `frame_count` | `0xB36F4C` | u32（4 字节） |
| `dir_h` | `0xB36F66` | u16（2 字节） |
| `dir_v` | `0xB36F6F` | u16（2 字节） |
| `msec` | `0xB36F89` | u16（2 字节） |
| `wrestle_id` | `0xB36FA3` | u32（4 字节） |
| `charge_lv` | `0xB36FBD` | u8（1 字节） |
| `AI_ent_id` | `0xB36FD7` | u16（2 字节） |
| `action` | `0xB36FF1` | u8（1 字节） |
| `chase_ent_id` | `0xB3700B` | u16（2 字节） |
| `is_dp_damage_cut` | `0xB37025` | u8（1 字节） |
