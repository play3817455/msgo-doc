# 汇编证据 —— CS-0x26F2-lounge-you9_cps_SCAN_response

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_BA54D0 @ `0x00ba54d0`（`0x00ba54d0`..`0x00ba57c9`）
- 命令名字符串：`)<-_proto_lounge_client::send_you9_cps_SCAN_response(` @ `0xeed130`
- 声明容量：`0x2336`（分配器指纹 @ `0xBA5516`）

## 2. 组包块切片（游标初始化 → 提交）

```asm
00BA552B  call sub_ABB2F0
00BA5530  lea ecx, [edi+2336h]
00BA5536  lea eax, [edi+2]
00BA5539  cmp eax, ecx
00BA553B  mov [esp+4Ch+var_4], 0
00BA5543  mov [esp+4Ch+var_30], edi
00BA5547  mov [esp+4Ch+var_2C], ecx
00BA554B  ja loc_BA57B4
00BA5551  lea edx, [eax+4]
00BA5554  cmp edx, ecx
00BA5556  mov word ptr [edi], 26F2h
00BA555B  ja loc_BA57B4
00BA5561  mov ebp, [esp+4Ch+arg_8]
00BA5565  cmp ebp, 2000h
00BA556B  mov ecx, [esp+4Ch+arg_0]
00BA556F  mov [eax], ecx
00BA5571  mov [esp+4Ch+var_30], edx
00BA5575  ja loc_BA57B4
00BA557B  lea edx, [esp+4Ch+var_30]
00BA557F  push edx
00BA5580  lea eax, [esp+50h+arg_8]
00BA5584  push eax
00BA5585  call sub_B02D80
00BA558A  add esp, 8
00BA558D  test al, al
00BA558F  jz loc_BA57B4
00BA5595  xor eax, eax
00BA5597  test ebp, ebp
00BA5599  jbe short loc_BA55CC
00BA559B  mov ecx, [esp+4Ch+var_30]
00BA559F  mov edi, [esp+4Ch+var_2C]
00BA55A3  lea esi, [ecx+1]
00BA55A6  cmp esi, edi
00BA55A8  ja loc_BA57B0
00BA55AE  mov edx, [esp+4Ch+arg_4]
00BA55B2  mov dl, [eax+edx]
00BA55B5  mov [ecx], dl
00BA55B7  add eax, 1
00BA55BA  add ecx, 1
00BA55BD  add esi, 1
00BA55C0  cmp eax, ebp
00BA55C2  jb short loc_BA55A6
00BA55C4  mov edi, [esp+4Ch+var_34]
00BA55C8  mov [esp+4Ch+var_30], ecx
00BA55CC  mov ecx, [esp+4Ch+arg_C]
00BA55D0  push 32Bh
00BA55D5  lea eax, [esp+50h+var_30]
00BA55D9  push eax
00BA55DA  push ecx
00BA55DB  call sub_B02B40
00BA55E0  add esp, 0Ch
00BA55E3  test al, al
00BA55E5  jz loc_BA57B4
00BA55EB  mov esi, [ebx+8228h]
00BA55F1  test esi, esi
00BA55F3  jz loc_BA574D
00BA55F9  lea edx, [esp+4Ch+var_28]
00BA55FD  push edx
00BA55FE  call sub_CA0CE0
00BA5603  add esp, 4
00BA5606  mov ecx, [ebx+8]
00BA5609  push offset aProtoLoungeCli_351; ")<-_proto_lounge_client::send_you9_cps_"...
00BA560E  push ecx
00BA560F  push offset aId; " (id:"
00BA5614  push eax
00BA5615  push esi
00BA5616  mov byte ptr [esp+60h+var_4], 1
00BA561B  call sub_B03020
00BA5620  add esp, 8
00BA5623  push eax
00BA5624  call sub_41D990
00BA5629  add esp, 8
00BA562C  mov ecx, eax
00BA562E  call sub_ADC810
00BA5633  push eax
00BA5634  call sub_41D990
00BA5639  add esp, 8
00BA563C  lea ecx, [esp+4Ch+var_28]
00BA5640  mov byte ptr [esp+4Ch+var_4], 0
```

## 3. 发送去向切片（提交之后的实际发送）

```asm
00BA5749  mov edi, [esp+4Ch+var_34]
00BA574D  mov esi, [esp+4Ch+var_30]
00BA5751  mov edx, [ebx]
00BA5753  mov eax, [edx+58h]
00BA5756  sub esi, edi
00BA5758  push esi
00BA5759  push edi
00BA575A  mov ecx, ebx
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xBA5556` | u16（2 字节） |
| `cps_result` | `0xBA556F` | u32（4 字节） |
| `buffer_size` | `0xBA5585` | u32（4 字节） |
| `buffer` | `0xBA55B5` | array<u8,8192>（1 字节） |
| `virus_path` | `0xBA55DB` | str（变长） |
