# 汇编证据 —— CS-0x34C8-battle-roomlobby_ban_vote_cancel

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B327E0 @ `0x00b327e0`（`0x00b327e0`..`0x00b32987`）
- 命令名字符串：`)<-_proto_battle_client::send_roomlobby_ban_vote_cancel(` @ `0xee06f8`
- 声明容量：`0x6`（分配器指纹 @ `0xB32823`）

## 2. 组包块切片（游标初始化 → 提交）

```asm
00B32831  call sub_ABB2F0
00B32836  lea ecx, [ebp+6]
00B32839  lea eax, [ebp+2]
00B3283C  cmp eax, ecx
00B3283E  mov [esp+40h+var_4], 0
00B32846  ja loc_B32972
00B3284C  lea ebx, [eax+4]
00B3284F  cmp ebx, ecx
00B32851  mov word ptr [ebp+0], 34C8h
00B32857  ja loc_B32972
00B3285D  mov ecx, [esp+40h+arg_0]
00B32861  mov [eax], ecx
00B32863  mov edi, [esi+3C60h]
00B32869  test edi, edi
00B3286B  jz loc_B32916
00B32871  lea edx, [esp+40h+var_28]
00B32875  push edx
00B32876  call sub_CA0CE0
00B3287B  add esp, 4
00B3287E  mov ecx, [esi+8]
00B32881  push offset aProtoBattleCli_228; ")<-_proto_battle_client::send_roomlobby"...
00B32886  push ecx
00B32887  push offset aId; " (id:"
00B3288C  push eax
00B3288D  push edi
00B3288E  mov byte ptr [esp+54h+var_4], 1
00B32893  call sub_B03020
00B32898  add esp, 8
00B3289B  push eax
00B3289C  call sub_41D990
00B328A1  add esp, 8
00B328A4  mov ecx, eax
00B328A6  call sub_ADC810
00B328AB  push eax
00B328AC  call sub_41D990
00B328B1  add esp, 8
00B328B4  lea ecx, [esp+40h+var_28]
00B328B8  mov byte ptr [esp+40h+var_4], 0
```

## 3. 发送去向切片（提交之后的实际发送）

```asm
00B3290F  mov ecx, edi
00B32911  call sub_40DDF0
00B32916  mov edx, [esi]
00B32918  mov eax, [edx+58h]
00B3291B  sub ebx, ebp
00B3291D  push ebx
00B3291E  push ebp
00B3291F  mov ecx, esi
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB32851` | u16（2 字节） |
| `msma_id` | `0xB32861` | u32（4 字节） |
