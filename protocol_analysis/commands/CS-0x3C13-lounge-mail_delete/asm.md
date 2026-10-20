# 汇编证据 —— CS-0x3C13-lounge-mail_delete

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B9BC80 @ `0x00b9bc80`（`0x00b9bc80`..`0x00b9bf14`）
- 命令名字符串：`)<-_proto_lounge_client::send_mail_delete(` @ `0xeec1c8`
- 声明容量：`0x19A`（分配器指纹 @ `0xB9BCC8`）

## 2. 组包块切片（游标初始化 → 提交）

```asm
00B9BCDD  call sub_ABB2F0
00B9BCE2  lea ecx, [edi+19Ah]
00B9BCE8  lea eax, [edi+2]
00B9BCEB  cmp eax, ecx
00B9BCED  mov [esp+4Ch+var_4], esi
00B9BCF1  mov [esp+4Ch+var_30], edi
00B9BCF5  mov dword ptr [esp+4Ch+var_2C], ecx
00B9BCF9  ja loc_B9BEFF
00B9BCFF  lea edx, [eax+4]
00B9BD02  cmp edx, ecx
00B9BD04  mov word ptr [edi], 3C13h
00B9BD09  ja loc_B9BEFF
00B9BD0F  mov ebp, [esp+4Ch+arg_8]
00B9BD13  cmp ebp, 32h ; '2'
00B9BD16  mov ecx, [esp+4Ch+arg_0]
00B9BD1A  mov [eax], ecx
00B9BD1C  mov [esp+4Ch+var_30], edx
00B9BD20  ja loc_B9BEFF
00B9BD26  lea edx, [esp+4Ch+var_30]
00B9BD2A  push edx
00B9BD2B  lea eax, [esp+50h+arg_8]
00B9BD2F  push eax
00B9BD30  call sub_B02D80
00B9BD35  add esp, 8
00B9BD38  test al, al
00B9BD3A  jz loc_B9BEFF
00B9BD40  cmp ebp, esi
00B9BD42  jbe short loc_B9BD72
00B9BD44  mov ecx, [esp+4Ch+arg_4]
00B9BD48  mov [esp+4Ch+arg_8], ecx
00B9BD4C  mov eax, [esp+4Ch+arg_8]
00B9BD50  lea edx, [esp+4Ch+var_30]
00B9BD54  push edx
00B9BD55  push eax
00B9BD56  call sub_B06190
00B9BD5B  add esp, 8
00B9BD5E  test al, al
00B9BD60  jz loc_B9BEFF
00B9BD66  add [esp+4Ch+arg_8], 8
00B9BD6B  add esi, 1
00B9BD6E  cmp esi, ebp
00B9BD70  jb short loc_B9BD4C
00B9BD72  mov esi, [ebx+7F50h]
00B9BD78  test esi, esi
00B9BD7A  jz loc_B9BE9C
00B9BD80  lea ecx, [esp+4Ch+var_28]
00B9BD84  push ecx
00B9BD85  call sub_CA0CE0
00B9BD8A  add esp, 4
00B9BD8D  mov edx, [ebx+8]
00B9BD90  push offset aProtoLoungeCli_377; ")<-_proto_lounge_client::send_mail_dele"...
00B9BD95  push edx
00B9BD96  push offset aId; " (id:"
00B9BD9B  push eax
00B9BD9C  push esi
00B9BD9D  mov byte ptr [esp+60h+var_4], 1
00B9BDA2  call sub_B03020
00B9BDA7  add esp, 8
00B9BDAA  push eax
00B9BDAB  call sub_41D990
00B9BDB0  add esp, 8
00B9BDB3  mov ecx, eax
00B9BDB5  call sub_ADC810
00B9BDBA  push eax
00B9BDBB  call sub_41D990
00B9BDC0  add esp, 8
00B9BDC3  lea ecx, [esp+4Ch+var_28]
00B9BDC7  mov byte ptr [esp+4Ch+var_4], 0
```

## 3. 发送去向切片（提交之后的实际发送）

```asm
00B9BE98  mov edi, [esp+4Ch+var_34]
00B9BE9C  mov esi, [esp+4Ch+var_30]
00B9BEA0  mov edx, [ebx]
00B9BEA2  mov eax, [edx+58h]
00B9BEA5  sub esi, edi
00B9BEA7  push esi
00B9BEA8  push edi
00B9BEA9  mov ecx, ebx
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB9BD04` | u16（2 字节） |
| `box_type` | `0xB9BD1A` | u32（4 字节） |
| `mail_num` | `0xB9BD30` | u32（4 字节） |
| `mailids` | `0xB9BD56` | array<u64,50>（8 字节） |
