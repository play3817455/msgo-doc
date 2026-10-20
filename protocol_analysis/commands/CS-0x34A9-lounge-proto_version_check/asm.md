# 汇编证据 —— CS-0x34A9-lounge-proto_version_check

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B89460 @ `0x00b89460`（`0x00b89460`..`0x00b89696`）
- 命令名字符串：`)<-_proto_lounge_client::send_proto_version_check(` @ `0xeea1d8`
- 声明容量：`0xE`（分配器指纹 @ `0xB894A3`）

## 2. 组包块切片（游标初始化 → 提交）

```asm
00B894B1  call sub_ABB2F0
00B894B6  lea ecx, [ebp+0Eh]
00B894B9  lea eax, [ebp+2]
00B894BC  cmp eax, ecx
00B894BE  mov [esp+48h+var_4], 0
00B894C6  mov [esp+48h+var_30], ebp
00B894CA  mov dword ptr [esp+48h+var_2C], ecx
00B894CE  ja loc_B89681
00B894D4  lea edx, [eax+4]
00B894D7  cmp edx, ecx
00B894D9  mov word ptr [ebp+0], 34A9h
00B894DF  ja loc_B89681
00B894E5  mov esi, [esp+48h+arg_0]
00B894E9  mov [eax], esi
00B894EB  mov eax, edx
00B894ED  lea edx, [eax+4]
00B894F0  cmp edx, ecx
00B894F2  ja loc_B89681
00B894F8  mov ecx, [esp+48h+arg_4]
00B894FC  mov [esp+48h+var_30], edx
00B89500  lea edx, [esp+48h+var_30]
00B89504  mov [eax], ecx
00B89506  push edx
00B89507  lea eax, [esp+4Ch+arg_8]
00B8950B  push eax
00B8950C  call sub_B02D80
00B89511  add esp, 8
00B89514  test al, al
00B89516  jz loc_B89681
00B8951C  mov esi, [edi+79B0h]
00B89522  test esi, esi
00B89524  mov ebx, [esp+48h+var_30]
00B89528  jz loc_B89623
00B8952E  lea ecx, [esp+48h+var_28]
00B89532  push ecx
00B89533  call sub_CA0CE0
00B89538  add esp, 4
00B8953B  mov edx, [edi+8]
00B8953E  push offset aProtoLoungeCli_597; ")<-_proto_lounge_client::send_proto_ver"...
00B89543  push edx
00B89544  push offset aId; " (id:"
00B89549  push eax
00B8954A  push esi
00B8954B  mov byte ptr [esp+5Ch+var_4], 1
00B89550  call sub_B03020
00B89555  add esp, 8
00B89558  push eax
00B89559  call sub_41D990
00B8955E  add esp, 8
00B89561  mov ecx, eax
00B89563  call sub_ADC810
00B89568  push eax
00B89569  call sub_41D990
00B8956E  add esp, 8
00B89571  lea ecx, [esp+48h+var_28]
00B89575  mov byte ptr [esp+48h+var_4], 0
```

## 3. 发送去向切片（提交之后的实际发送）

```asm
00B8961C  mov ecx, esi
00B8961E  call sub_40DDF0
00B89623  mov edx, [edi]
00B89625  mov eax, [edx+58h]
00B89628  mov esi, ebx
00B8962A  sub esi, ebp
00B8962C  push esi
00B8962D  push ebp
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB894D9` | u16（2 字节） |
| `version` | `0xB894E9` | u32（4 字节） |
| `crc` | `0xB89504` | u32（4 字节） |
| `gentime` | `0xB8950C` | u32（4 字节） |
