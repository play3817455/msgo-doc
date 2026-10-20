# 汇编证据 —— CS-0x379B-battle-cutin_up

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B34F10 @ `0x00b34f10`（`0x00b34f10`..`0x00b351cd`）
- 命令名字符串：`)<-_proto_battle_client::send_cutin_up(` @ `0xee0b0c`
- 声明容量：`0x16`（分配器指纹 @ `0xB34F56`）

## 2. 组包块切片（游标初始化 → 提交）

```asm
00B34F64  call sub_ABB2F0
00B34F69  lea eax, [ebp+16h]
00B34F6C  lea ecx, [ebp+2]
00B34F6F  cmp ecx, eax
00B34F71  mov [esp+48h+var_4], 0
00B34F79  mov [esp+48h+var_30], ebp
00B34F7D  mov dword ptr [esp+48h+var_2C], eax
00B34F81  ja loc_B351B8
00B34F87  lea edx, [ecx+4]
00B34F8A  cmp edx, eax
00B34F8C  mov word ptr [ebp+0], 379Bh
00B34F92  ja loc_B351B8
00B34F98  mov esi, [esp+48h+arg_0]
00B34F9C  mov [ecx], esi
00B34F9E  lea ecx, [edx+2]
00B34FA1  cmp ecx, eax
00B34FA3  ja loc_B351B8
00B34FA9  mov ax, word ptr [esp+48h+arg_4]
00B34FAE  mov [esp+48h+var_30], ecx
00B34FB2  lea ecx, [esp+48h+var_30]
00B34FB6  mov [edx], ax
00B34FB9  push ecx
00B34FBA  lea edx, [esp+4Ch+arg_8]
00B34FBE  push edx
00B34FBF  call sub_B02D80
00B34FC4  add esp, 8
00B34FC7  test al, al
00B34FC9  jz loc_B351B8
00B34FCF  lea eax, [esp+48h+var_30]
00B34FD3  push eax
00B34FD4  lea ecx, [esp+4Ch+arg_C]
00B34FD8  push ecx
00B34FD9  call sub_B02D80
00B34FDE  add esp, 8
00B34FE1  test al, al
00B34FE3  jz loc_B351B8
00B34FE9  lea edx, [esp+48h+var_30]
00B34FED  push edx
00B34FEE  lea eax, [esp+4Ch+arg_10]
00B34FF2  push eax
00B34FF3  call sub_B061C0
00B34FF8  add esp, 8
00B34FFB  test al, al
00B34FFD  jz loc_B351B8
00B35003  mov esi, [edi+3D94h]
00B35009  test esi, esi
00B3500B  mov ebx, [esp+48h+var_30]
00B3500F  jz loc_B3515C
00B35015  lea ecx, [esp+48h+var_28]
00B35019  push ecx
00B3501A  call sub_CA0CE0
00B3501F  add esp, 4
00B35022  mov edx, [edi+8]
00B35025  push offset aProtoBattleCli_222; ")<-_proto_battle_client::send_cutin_up("...
00B3502A  push edx
00B3502B  push offset aId; " (id:"
00B35030  push eax
00B35031  push esi
00B35032  mov byte ptr [esp+5Ch+var_4], 1
00B35037  call sub_B03020
00B3503C  add esp, 8
00B3503F  push eax
00B35040  call sub_41D990
00B35045  add esp, 8
00B35048  mov ecx, eax
00B3504A  call sub_ADC810
00B3504F  push eax
00B35050  call sub_41D990
00B35055  add esp, 8
00B35058  lea ecx, [esp+48h+var_28]
00B3505C  mov byte ptr [esp+48h+var_4], 0
```

## 3. 发送去向切片（提交之后的实际发送）

```asm
00B35155  mov ecx, esi
00B35157  call sub_40DDF0
00B3515C  mov eax, [edi]
00B3515E  mov edx, [eax+58h]
00B35161  sub ebx, ebp
00B35163  push ebx
00B35164  push ebp
00B35165  mov ecx, edi
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB34F8C` | u16（2 字节） |
| `cutin_category_id` | `0xB34F9C` | u32（4 字节） |
| `AI_ent_id` | `0xB34FB6` | u16（2 字节） |
| `to_world_id` | `0xB34FBF` | u32（4 字节） |
| `to_pilot_id` | `0xB34FD9` | u32（4 字节） |
| `to_range` | `0xB34FF3` | u8（1 字节） |
