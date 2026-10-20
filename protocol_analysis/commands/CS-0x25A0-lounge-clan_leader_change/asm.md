# 汇编证据 —— CS-0x25A0-lounge-clan_leader_change

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_BA0AD0 @ `0x00ba0ad0`（`0x00ba0ad0`..`0x00ba0d25`）
- 命令名字符串：`)<-_proto_lounge_client::send_clan_leader_change(` @ `0xeec96c`
- 声明容量：`0x26`（分配器指纹 @ `0xBA0B16`）

## 2. 组包块切片（游标初始化 → 提交）

```asm
00BA0B24  call sub_ABB2F0
00BA0B29  lea ecx, [ebp+26h]
00BA0B2C  lea eax, [ebp+2]
00BA0B2F  cmp eax, ecx
00BA0B31  mov [esp+48h+var_4], 0
00BA0B39  mov [esp+48h+var_30], ebp
00BA0B3D  mov dword ptr [esp+48h+var_2C], ecx
00BA0B41  ja loc_BA0D10
00BA0B47  lea edx, [eax+4]
00BA0B4A  cmp edx, ecx
00BA0B4C  mov word ptr [ebp+0], 25A0h
00BA0B52  ja loc_BA0D10
00BA0B58  mov ecx, [esp+48h+arg_0]
00BA0B5C  mov [esp+48h+var_30], edx
00BA0B60  push 19h
00BA0B62  lea edx, [esp+4Ch+var_30]
00BA0B66  mov [eax], ecx
00BA0B68  mov eax, dword ptr [esp+4Ch+arg_4]
00BA0B6C  push edx
00BA0B6D  push eax
00BA0B6E  call sub_B02B40
00BA0B73  add esp, 0Ch
00BA0B76  test al, al
00BA0B78  jz loc_BA0D10
00BA0B7E  lea ecx, [esp+48h+var_30]
00BA0B82  push ecx
00BA0B83  lea edx, [esp+4Ch+arg_8]
00BA0B87  push edx
00BA0B88  call sub_B061C0
00BA0B8D  add esp, 8
00BA0B90  test al, al
00BA0B92  jz loc_BA0D10
00BA0B98  mov esi, [edi+80B8h]
00BA0B9E  test esi, esi
00BA0BA0  mov ebx, [esp+48h+var_30]
00BA0BA4  jz loc_BA0CB1
00BA0BAA  lea eax, [esp+48h+var_28]
00BA0BAE  push eax
00BA0BAF  call sub_CA0CE0
00BA0BB4  add esp, 4
00BA0BB7  mov ecx, [edi+8]
00BA0BBA  push offset aProtoLoungeCli_492; ")<-_proto_lounge_client::send_clan_lead"...
00BA0BBF  push ecx
00BA0BC0  push offset aId; " (id:"
00BA0BC5  push eax
00BA0BC6  push esi
00BA0BC7  mov byte ptr [esp+5Ch+var_4], 1
00BA0BCC  call sub_B03020
00BA0BD1  add esp, 8
00BA0BD4  push eax
00BA0BD5  call sub_41D990
00BA0BDA  add esp, 8
00BA0BDD  mov ecx, eax
00BA0BDF  call sub_ADC810
00BA0BE4  push eax
00BA0BE5  call sub_41D990
00BA0BEA  add esp, 8
00BA0BED  lea ecx, [esp+48h+var_28]
00BA0BF1  mov byte ptr [esp+48h+var_4], 0
```

## 3. 发送去向切片（提交之后的实际发送）

```asm
00BA0CAA  mov ecx, esi
00BA0CAC  call sub_40DDF0
00BA0CB1  mov eax, [edi]
00BA0CB3  mov edx, [eax+58h]
00BA0CB6  sub ebx, ebp
00BA0CB8  push ebx
00BA0CB9  push ebp
00BA0CBA  mov ecx, edi
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xBA0B4C` | u16（2 字节） |
| `pilot_id_new` | `0xBA0B66` | u32（4 字节） |
| `pilot_name_new` | `0xBA0B6E` | str（变长） |
| `clan_kind` | `0xBA0B88` | u8（1 字节） |
