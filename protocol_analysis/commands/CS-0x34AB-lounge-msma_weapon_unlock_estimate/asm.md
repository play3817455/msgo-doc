# 汇编证据 —— CS-0x34AB-lounge-msma_weapon_unlock_estimate

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B97B30 @ `0x00b97b30`（`0x00b97b30`..`0x00b97db6`）
- 命令名字符串：`)<-_proto_lounge_client::send_msma_weapon_unlock_estimate(` @ `0xeebad4`
- 声明容量：`0x16`（分配器指纹 @ `0xB97B76`）

## 2. 组包块切片（游标初始化 → 提交）

```asm
00B97B84  call sub_ABB2F0
00B97B89  lea ecx, [ebp+16h]
00B97B8C  lea eax, [ebp+2]
00B97B8F  cmp eax, ecx
00B97B91  mov [esp+48h+var_4], 0
00B97B99  mov [esp+48h+var_30], ebp
00B97B9D  mov dword ptr [esp+48h+var_2C], ecx
00B97BA1  ja loc_B97DA1
00B97BA7  lea edx, [eax+8]
00B97BAA  cmp edx, ecx
00B97BAC  mov word ptr [ebp+0], 34ABh
00B97BB2  ja loc_B97DA1
00B97BB8  mov esi, [esp+48h+arg_0]
00B97BBC  mov [eax], esi
00B97BBE  mov esi, [esp+48h+arg_4]
00B97BC2  mov [eax+4], esi
00B97BC5  lea eax, [edx+4]
00B97BC8  cmp eax, ecx
00B97BCA  ja loc_B97DA1
00B97BD0  mov ecx, [esp+48h+arg_8]
00B97BD4  mov [edx], ecx
00B97BD6  lea edx, [esp+48h+var_30]
00B97BDA  mov [esp+48h+var_30], eax
00B97BDE  push edx
00B97BDF  lea eax, [esp+4Ch+arg_C]
00B97BE3  push eax
00B97BE4  call sub_B02D80
00B97BE9  add esp, 8
00B97BEC  test al, al
00B97BEE  jz loc_B97DA1
00B97BF4  lea ecx, [esp+48h+var_30]
00B97BF8  push ecx
00B97BF9  lea edx, [esp+4Ch+arg_10]
00B97BFD  push edx
00B97BFE  call sub_B02D80
00B97C03  add esp, 8
00B97C06  test al, al
00B97C08  jz loc_B97DA1
00B97C0E  mov esi, [edi+7E1Ch]
00B97C14  test esi, esi
00B97C16  mov ebx, [esp+48h+var_30]
00B97C1A  jz loc_B97D42
00B97C20  lea eax, [esp+48h+var_28]
00B97C24  push eax
00B97C25  call sub_CA0CE0
00B97C2A  add esp, 4
00B97C2D  mov ecx, [edi+8]
00B97C30  push offset aProtoLoungeCli_471; ")<-_proto_lounge_client::send_msma_weap"...
00B97C35  push ecx
00B97C36  push offset aId; " (id:"
00B97C3B  push eax
00B97C3C  push esi
00B97C3D  mov byte ptr [esp+5Ch+var_4], 1
00B97C42  call sub_B03020
00B97C47  add esp, 8
00B97C4A  push eax
00B97C4B  call sub_41D990
00B97C50  add esp, 8
00B97C53  mov ecx, eax
00B97C55  call sub_ADC810
00B97C5A  push eax
00B97C5B  call sub_41D990
00B97C60  add esp, 8
00B97C63  lea ecx, [esp+48h+var_28]
00B97C67  mov byte ptr [esp+48h+var_4], 0
```

## 3. 发送去向切片（提交之后的实际发送）

```asm
00B97D3B  mov ecx, esi
00B97D3D  call sub_40DDF0
00B97D42  mov edx, [edi]
00B97D44  mov eax, [edx+58h]
00B97D47  sub ebx, ebp
00B97D49  push ebx
00B97D4A  push ebp
00B97D4B  mov ecx, edi
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB97BAC` | u16（2 字节） |
| `uniqid_ms` | `0xB97BBC` | u64（8 字节） |
| `item_id` | `0xB97BD4` | u32（4 字节） |
| `use_gp` | `0xB97BE4` | u32（4 字节） |
| `use_bc` | `0xB97BFE` | u32（4 字节） |
