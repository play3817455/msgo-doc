# 汇编证据 —— CS-0x36AC-battle-weapon_fire__for_myself

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B3A1F0 @ `0x00b3a1f0`（`0x00b3a1f0`..`0x00b3a576`）
- 命令名字符串：`)<-_proto_battle_client::send_weapon_fire__for_myself(` @ `0xee0fa8`
- 声明容量：`0x22`（分配器指纹 @ `0xB3A236`）

## 2. 组包块切片（游标初始化 → 提交）

```asm
00B3A244  call sub_ABB2F0
00B3A249  lea eax, [ebp+22h]
00B3A24C  lea ecx, [ebp+2]
00B3A24F  cmp ecx, eax
00B3A251  mov [esp+48h+var_4], 0
00B3A259  mov [esp+48h+var_30], ebp
00B3A25D  mov dword ptr [esp+48h+var_2C], eax
00B3A261  ja loc_B3A561
00B3A267  lea edx, [ecx+4]
00B3A26A  cmp edx, eax
00B3A26C  mov word ptr [ebp+0], 36ACh
00B3A272  ja loc_B3A561
00B3A278  mov esi, [esp+48h+arg_0]
00B3A27C  mov [ecx], esi
00B3A27E  lea ecx, [edx+2]
00B3A281  cmp ecx, eax
00B3A283  ja loc_B3A561
00B3A289  mov ax, word ptr [esp+48h+arg_4]
00B3A28E  mov [esp+48h+var_30], ecx
00B3A292  lea ecx, [esp+48h+var_30]
00B3A296  mov [edx], ax
00B3A299  push ecx
00B3A29A  lea edx, [esp+4Ch+arg_8]
00B3A29E  push edx
00B3A29F  call sub_B02DA0
00B3A2A4  add esp, 8
00B3A2A7  test al, al
00B3A2A9  jz loc_B3A561
00B3A2AF  lea eax, [esp+48h+var_30]
00B3A2B3  push eax
00B3A2B4  lea ecx, [esp+4Ch+arg_C]
00B3A2B8  push ecx
00B3A2B9  call sub_B02DA0
00B3A2BE  add esp, 8
00B3A2C1  test al, al
00B3A2C3  jz loc_B3A561
00B3A2C9  lea edx, [esp+48h+var_30]
00B3A2CD  push edx
00B3A2CE  lea eax, [esp+4Ch+arg_10]
00B3A2D2  push eax
00B3A2D3  call sub_B02DA0
00B3A2D8  add esp, 8
00B3A2DB  test al, al
00B3A2DD  jz loc_B3A561
00B3A2E3  lea ecx, [esp+48h+var_30]
00B3A2E7  push ecx
00B3A2E8  lea edx, [esp+4Ch+arg_14]
00B3A2EC  push edx
00B3A2ED  call sub_B02DA0
00B3A2F2  add esp, 8
00B3A2F5  test al, al
00B3A2F7  jz loc_B3A561
00B3A2FD  lea eax, [esp+48h+var_30]
00B3A301  push eax
00B3A302  lea ecx, [esp+4Ch+arg_18]
00B3A306  push ecx
00B3A307  call sub_B061C0
00B3A30C  add esp, 8
00B3A30F  test al, al
00B3A311  jz loc_B3A561
00B3A317  lea edx, [esp+48h+var_30]
00B3A31B  push edx
00B3A31C  lea eax, [esp+4Ch+arg_1C]
00B3A320  push eax
00B3A321  call sub_B02DA0
00B3A326  add esp, 8
00B3A329  test al, al
00B3A32B  jz loc_B3A561
00B3A331  mov esi, [edi+3E34h]
00B3A337  test esi, esi
00B3A339  mov ebx, [esp+48h+var_30]
00B3A33D  jz loc_B3A502
00B3A343  lea ecx, [esp+48h+var_28]
00B3A347  push ecx
00B3A348  call sub_CA0CE0
00B3A34D  add esp, 4
00B3A350  mov edx, [edi+8]
00B3A353  push offset aProtoBattleCli_248; ")<-_proto_battle_client::send_weapon_fi"...
00B3A358  push edx
00B3A359  push offset aId; " (id:"
00B3A35E  push eax
00B3A35F  push esi
00B3A360  mov byte ptr [esp+5Ch+var_4], 1
00B3A365  call sub_B03020
00B3A36A  add esp, 8
00B3A36D  push eax
00B3A36E  call sub_41D990
00B3A373  add esp, 8
00B3A376  mov ecx, eax
00B3A378  call sub_ADC810
00B3A37D  push eax
00B3A37E  call sub_41D990
00B3A383  add esp, 8
00B3A386  lea ecx, [esp+48h+var_28]
00B3A38A  mov byte ptr [esp+48h+var_4], 0
```

## 3. 发送去向切片（提交之后的实际发送）

```asm
00B3A4FB  mov ecx, esi
00B3A4FD  call sub_40DDF0
00B3A502  mov eax, [edi]
00B3A504  mov edx, [eax+58h]
00B3A507  sub ebx, ebp
00B3A509  push ebx
00B3A50A  push ebp
00B3A50B  mov ecx, edi
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB3A26C` | u16（2 字节） |
| `frame_count` | `0xB3A27C` | u32（4 字节） |
| `target_x` | `0xB3A296` | u16（2 字节） |
| `target_y` | `0xB3A29F` | u16（2 字节） |
| `target_z` | `0xB3A2B9` | u16（2 字节） |
| `rcnt_bullet_mgz` | `0xB3A2D3` | u16（2 字节） |
| `rcnt_bullet_all` | `0xB3A2ED` | u16（2 字节） |
| `begin1_end0` | `0xB3A307` | u8（1 字节） |
| `AI_ent_id` | `0xB3A321` | u16（2 字节） |
