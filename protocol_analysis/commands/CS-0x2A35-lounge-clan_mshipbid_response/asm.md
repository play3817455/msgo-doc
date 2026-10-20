# 汇编证据 —— CS-0x2A35-lounge-clan_mshipbid_response

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_BA0260 @ `0x00ba0260`（`0x00ba0260`..`0x00ba049c`）
- 命令名字符串：`)<-_proto_lounge_client::send_clan_mshipbid_response(` @ `0xeec89c`
- 声明容量：`0xE`（分配器指纹 @ `0xBA02A6`）

## 2. 组包块切片（游标初始化 → 提交）

```asm
00BA02B4  call sub_ABB2F0
00BA02B9  lea ecx, [ebp+0Eh]
00BA02BC  lea eax, [ebp+2]
00BA02BF  cmp eax, ecx
00BA02C1  mov [esp+48h+var_4], 0
00BA02C9  mov [esp+48h+var_30], ebp
00BA02CD  mov dword ptr [esp+48h+var_2C], ecx
00BA02D1  ja loc_BA0487
00BA02D7  lea edx, [eax+4]
00BA02DA  cmp edx, ecx
00BA02DC  mov word ptr [ebp+0], 2A35h
00BA02E2  ja loc_BA0487
00BA02E8  mov esi, [esp+48h+arg_0]
00BA02EC  mov [eax], esi
00BA02EE  mov eax, edx
00BA02F0  lea edx, [eax+4]
00BA02F3  cmp edx, ecx
00BA02F5  ja loc_BA0487
00BA02FB  mov ecx, dword ptr [esp+48h+arg_4]
00BA02FF  mov [esp+48h+var_30], edx
00BA0303  lea edx, [esp+48h+var_30]
00BA0307  mov [eax], ecx
00BA0309  push edx
00BA030A  lea eax, [esp+4Ch+arg_8]
00BA030E  push eax
00BA030F  call sub_B061C0
00BA0314  add esp, 8
00BA0317  test al, al
00BA0319  jz loc_BA0487
00BA031F  mov esi, [edi+8098h]
00BA0325  test esi, esi
00BA0327  mov ebx, [esp+48h+var_30]
00BA032B  jz loc_BA0428
00BA0331  lea ecx, [esp+48h+var_28]
00BA0335  push ecx
00BA0336  call sub_CA0CE0
00BA033B  add esp, 4
00BA033E  mov edx, [edi+8]
00BA0341  push offset aProtoLoungeCli_491; ")<-_proto_lounge_client::send_clan_mshi"...
00BA0346  push edx
00BA0347  push offset aId; " (id:"
00BA034C  push eax
00BA034D  push esi
00BA034E  mov byte ptr [esp+5Ch+var_4], 1
00BA0353  call sub_B03020
00BA0358  add esp, 8
00BA035B  push eax
00BA035C  call sub_41D990
00BA0361  add esp, 8
00BA0364  mov ecx, eax
00BA0366  call sub_ADC810
00BA036B  push eax
00BA036C  call sub_41D990
00BA0371  add esp, 8
00BA0374  lea ecx, [esp+48h+var_28]
00BA0378  mov byte ptr [esp+48h+var_4], 0
```

## 3. 发送去向切片（提交之后的实际发送）

```asm
00BA0421  mov ecx, esi
00BA0423  call sub_40DDF0
00BA0428  mov edx, [edi]
00BA042A  mov eax, [edx+58h]
00BA042D  sub ebx, ebp
00BA042F  push ebx
00BA0430  push ebp
00BA0431  mov ecx, edi
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xBA02DC` | u16（2 字节） |
| `pilot_id_applicant` | `0xBA02EC` | u32（4 字节） |
| `is_ok` | `0xBA0307` | u32（4 字节） |
| `clan_kind` | `0xBA030F` | u8（1 字节） |
