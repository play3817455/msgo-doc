# 汇编证据 —— CS-0x34A9-battle-proto_version_check

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B318D0 @ `0x00b318d0`（`0x00b318d0`..`0x00b31b06`）
- 命令名字符串：`)<-_proto_battle_client::send_proto_version_check(` @ `0xee0540`
- 声明容量：`0xE`（分配器指纹 @ `0xB31913`）

## 2. 组包块切片（游标初始化 → 提交）

```asm
00B31921  call sub_ABB2F0
00B31926  lea ecx, [ebp+0Eh]
00B31929  lea eax, [ebp+2]
00B3192C  cmp eax, ecx
00B3192E  mov [esp+48h+var_4], 0
00B31936  mov [esp+48h+var_30], ebp
00B3193A  mov dword ptr [esp+48h+var_2C], ecx
00B3193E  ja loc_B31AF1
00B31944  lea edx, [eax+4]
00B31947  cmp edx, ecx
00B31949  mov word ptr [ebp+0], 34A9h
00B3194F  ja loc_B31AF1
00B31955  mov esi, [esp+48h+arg_0]
00B31959  mov [eax], esi
00B3195B  mov eax, edx
00B3195D  lea edx, [eax+4]
00B31960  cmp edx, ecx
00B31962  ja loc_B31AF1
00B31968  mov ecx, [esp+48h+arg_4]
00B3196C  mov [esp+48h+var_30], edx
00B31970  lea edx, [esp+48h+var_30]
00B31974  mov [eax], ecx
00B31976  push edx
00B31977  lea eax, [esp+4Ch+arg_8]
00B3197B  push eax
00B3197C  call sub_B02D80
00B31981  add esp, 8
00B31984  test al, al
00B31986  jz loc_B31AF1
00B3198C  mov esi, [edi+3BF8h]
00B31992  test esi, esi
00B31994  mov ebx, [esp+48h+var_30]
00B31998  jz loc_B31A93
00B3199E  lea ecx, [esp+48h+var_28]
00B319A2  push ecx
00B319A3  call sub_CA0CE0
00B319A8  add esp, 4
00B319AB  mov edx, [edi+8]
00B319AE  push offset aProtoBattleCli_295; ")<-_proto_battle_client::send_proto_ver"...
00B319B3  push edx
00B319B4  push offset aId; " (id:"
00B319B9  push eax
00B319BA  push esi
00B319BB  mov byte ptr [esp+5Ch+var_4], 1
00B319C0  call sub_B03020
00B319C5  add esp, 8
00B319C8  push eax
00B319C9  call sub_41D990
00B319CE  add esp, 8
00B319D1  mov ecx, eax
00B319D3  call sub_ADC810
00B319D8  push eax
00B319D9  call sub_41D990
00B319DE  add esp, 8
00B319E1  lea ecx, [esp+48h+var_28]
00B319E5  mov byte ptr [esp+48h+var_4], 0
```

## 3. 发送去向切片（提交之后的实际发送）

```asm
00B31A8C  mov ecx, esi
00B31A8E  call sub_40DDF0
00B31A93  mov edx, [edi]
00B31A95  mov eax, [edx+58h]
00B31A98  mov esi, ebx
00B31A9A  sub esi, ebp
00B31A9C  push esi
00B31A9D  push ebp
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB31949` | u16（2 字节） |
| `version` | `0xB31959` | u32（4 字节） |
| `crc` | `0xB31974` | u32（4 字节） |
| `gentime` | `0xB3197C` | u32（4 字节） |
