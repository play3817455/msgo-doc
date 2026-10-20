# 汇编证据 —— CS-0x2DA4-battle-access_to

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B35B70 @ `0x00b35b70`（`0x00b35b70`..`0x00b35d57`）
- 命令名字符串：`)<-_proto_battle_client::send_access_to(` @ `0xee0b94`
- 声明容量：`0xA`（分配器指纹 @ `0xB35BB6`）

## 2. 组包块切片（游标初始化 → 提交）

```asm
00B35BC4  call sub_ABB2F0
00B35BC9  lea ecx, [ebp+0Ah]
00B35BCC  lea eax, [ebp+2]
00B35BCF  cmp eax, ecx
00B35BD1  mov [esp+40h+var_4], 0
00B35BD9  ja loc_B35D42
00B35BDF  lea edx, [eax+2]
00B35BE2  cmp edx, ecx
00B35BE4  mov word ptr [ebp+0], 2DA4h
00B35BEA  ja loc_B35D42
00B35BF0  mov si, word ptr [esp+40h+arg_0]
00B35BF5  lea ebx, [edx+2]
00B35BF8  cmp ebx, ecx
00B35BFA  mov [eax], si
00B35BFD  ja loc_B35D42
00B35C03  mov cx, word ptr [esp+40h+arg_4]
00B35C08  mov [edx], cx
00B35C0B  mov esi, [edi+3DACh]
00B35C11  test esi, esi
00B35C13  jz loc_B35CE6
00B35C19  lea edx, [esp+40h+var_28]
00B35C1D  push edx
00B35C1E  call sub_CA0CE0
00B35C23  add esp, 4
00B35C26  mov ecx, [edi+8]
00B35C29  push offset aProtoBattleCli_259; ")<-_proto_battle_client::send_access_to"...
00B35C2E  push ecx
00B35C2F  push offset aId; " (id:"
00B35C34  push eax
00B35C35  push esi
00B35C36  mov byte ptr [esp+54h+var_4], 1
00B35C3B  call sub_B03020
00B35C40  add esp, 8
00B35C43  push eax
00B35C44  call sub_41D990
00B35C49  add esp, 8
00B35C4C  mov ecx, eax
00B35C4E  call sub_ADC810
00B35C53  push eax
00B35C54  call sub_41D990
00B35C59  add esp, 8
00B35C5C  lea ecx, [esp+40h+var_28]
00B35C60  mov byte ptr [esp+40h+var_4], 0
```

## 3. 发送去向切片（提交之后的实际发送）

```asm
00B35CDF  mov ecx, esi
00B35CE1  call sub_40DDF0
00B35CE6  mov edx, [edi]
00B35CE8  mov eax, [edx+58h]
00B35CEB  sub ebx, ebp
00B35CED  push ebx
00B35CEE  push ebp
00B35CEF  mov ecx, edi
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB35BE4` | u16（2 字节） |
| `access_ent_id` | `0xB35BFA` | u16（2 字节） |
| `AI_ent_id` | `0xB35C08` | u16（2 字节） |
