# 汇编证据 —— CS-0x34BE-battle-preset_voice_up_commander

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B34D20 @ `0x00b34d20`（`0x00b34d20`..`0x00b34f05`）
- 命令名字符串：`)<-_proto_battle_client::send_preset_voice_up_commander(` @ `0xee0ad0`
- 声明容量：`0xA`（分配器指纹 @ `0xB34D66`）

## 2. 组包块切片（游标初始化 → 提交）

```asm
00B34D74  call sub_ABB2F0
00B34D79  lea eax, [ebp+0Ah]
00B34D7C  lea ecx, [ebp+2]
00B34D7F  cmp ecx, eax
00B34D81  mov [esp+40h+var_4], 0
00B34D89  ja loc_B34EF0
00B34D8F  lea edx, [ecx+4]
00B34D92  cmp edx, eax
00B34D94  mov word ptr [ebp+0], 34BEh
00B34D9A  ja loc_B34EF0
00B34DA0  mov esi, [esp+40h+arg_0]
00B34DA4  lea ebx, [edx+2]
00B34DA7  cmp ebx, eax
00B34DA9  mov [ecx], esi
00B34DAB  ja loc_B34EF0
00B34DB1  mov cx, word ptr [esp+40h+arg_4]
00B34DB6  mov [edx], cx
00B34DB9  mov esi, [edi+3D90h]
00B34DBF  test esi, esi
00B34DC1  jz loc_B34E94
00B34DC7  lea edx, [esp+40h+var_28]
00B34DCB  push edx
00B34DCC  call sub_CA0CE0
00B34DD1  add esp, 4
00B34DD4  mov ecx, [edi+8]
00B34DD7  push offset aProtoBattleCli_285; ")<-_proto_battle_client::send_preset_vo"...
00B34DDC  push ecx
00B34DDD  push offset aId; " (id:"
00B34DE2  push eax
00B34DE3  push esi
00B34DE4  mov byte ptr [esp+54h+var_4], 1
00B34DE9  call sub_B03020
00B34DEE  add esp, 8
00B34DF1  push eax
00B34DF2  call sub_41D990
00B34DF7  add esp, 8
00B34DFA  mov ecx, eax
00B34DFC  call sub_ADC810
00B34E01  push eax
00B34E02  call sub_41D990
00B34E07  add esp, 8
00B34E0A  lea ecx, [esp+40h+var_28]
00B34E0E  mov byte ptr [esp+40h+var_4], 0
```

## 3. 发送去向切片（提交之后的实际发送）

```asm
00B34E8D  mov ecx, esi
00B34E8F  call sub_40DDF0
00B34E94  mov edx, [edi]
00B34E96  mov eax, [edx+58h]
00B34E99  sub ebx, ebp
00B34E9B  push ebx
00B34E9C  push ebp
00B34E9D  mov ecx, edi
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB34D94` | u16（2 字节） |
| `voice_id` | `0xB34DA9` | u32（4 字节） |
| `AI_ent_id` | `0xB34DB6` | u16（2 字节） |
