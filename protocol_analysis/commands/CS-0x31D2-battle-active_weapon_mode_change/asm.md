# 汇编证据 —— CS-0x31D2-battle-active_weapon_mode_change

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B362F0 @ `0x00b362f0`（`0x00b362f0`..`0x00b364d7`）
- 命令名字符串：`)<-_proto_battle_client::send_active_weapon_mode_change(` @ `0xee0c24`
- 声明容量：`0xA`（分配器指纹 @ `0xB36336`）

## 2. 组包块切片（游标初始化 → 提交）

```asm
00B36344  call sub_ABB2F0
00B36349  lea ecx, [ebp+0Ah]
00B3634C  lea eax, [ebp+2]
00B3634F  cmp eax, ecx
00B36351  mov [esp+40h+var_4], 0
00B36359  ja loc_B364C2
00B3635F  lea edx, [eax+2]
00B36362  cmp edx, ecx
00B36364  mov word ptr [ebp+0], 31D2h
00B3636A  ja loc_B364C2
00B36370  mov si, word ptr [esp+40h+arg_0]
00B36375  lea ebx, [edx+2]
00B36378  cmp ebx, ecx
00B3637A  mov [eax], si
00B3637D  ja loc_B364C2
00B36383  mov cx, word ptr [esp+40h+arg_4]
00B36388  mov [edx], cx
00B3638B  mov esi, [edi+3DC0h]
00B36391  test esi, esi
00B36393  jz loc_B36466
00B36399  lea edx, [esp+40h+var_28]
00B3639D  push edx
00B3639E  call sub_CA0CE0
00B363A3  add esp, 4
00B363A6  mov ecx, [edi+8]
00B363A9  push offset aProtoBattleCli_236; ")<-_proto_battle_client::send_active_we"...
00B363AE  push ecx
00B363AF  push offset aId; " (id:"
00B363B4  push eax
00B363B5  push esi
00B363B6  mov byte ptr [esp+54h+var_4], 1
00B363BB  call sub_B03020
00B363C0  add esp, 8
00B363C3  push eax
00B363C4  call sub_41D990
00B363C9  add esp, 8
00B363CC  mov ecx, eax
00B363CE  call sub_ADC810
00B363D3  push eax
00B363D4  call sub_41D990
00B363D9  add esp, 8
00B363DC  lea ecx, [esp+40h+var_28]
00B363E0  mov byte ptr [esp+40h+var_4], 0
```

## 3. 发送去向切片（提交之后的实际发送）

```asm
00B3645F  mov ecx, esi
00B36461  call sub_40DDF0
00B36466  mov edx, [edi]
00B36468  mov eax, [edx+58h]
00B3646B  sub ebx, ebp
00B3646D  push ebx
00B3646E  push ebp
00B3646F  mov ecx, edi
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB36364` | u16（2 字节） |
| `mode` | `0xB3637A` | u16（2 字节） |
| `AI_ent_id` | `0xB36388` | u16（2 字节） |
