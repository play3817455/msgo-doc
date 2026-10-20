# 汇编证据 —— CS-0x33CC-lounge-msma_missionunit_store

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B99850 @ `0x00b99850`（`0x00b99850`..`0x00b99a19`）
- 命令名字符串：`)<-_proto_lounge_client::send_msma_missionunit_store(` @ `0xeebdc4`
- 声明容量：`0xE`（分配器指纹 @ `0xB99896`）

## 2. 组包块切片（游标初始化 → 提交）

```asm
00B998A4  call sub_ABB2F0
00B998A9  lea ecx, [edi+0Eh]
00B998AC  lea eax, [edi+2]
00B998AF  cmp eax, ecx
00B998B1  mov [esp+48h+var_4], 0
00B998B9  mov [esp+48h+var_30], edi
00B998BD  mov dword ptr [esp+48h+var_2C], ecx
00B998C1  ja loc_B99A04
00B998C7  mov edx, [esp+48h+arg_0]
00B998CB  lea ecx, [esp+48h+var_30]
00B998CF  push ecx
00B998D0  push edx
00B998D1  mov word ptr [edi], 33CCh
00B998D6  mov [esp+50h+var_30], eax
00B998DA  call sub_B41BF0
00B998DF  add esp, 8
00B998E2  test al, al
00B998E4  jz loc_B99A04
00B998EA  mov ebp, [esi+7E94h]
00B998F0  test ebp, ebp
00B998F2  mov ebx, [esp+48h+var_30]
00B998F6  jz loc_B999A3
00B998FC  lea eax, [esp+48h+var_28]
00B99900  push eax
00B99901  call sub_CA0CE0
00B99906  add esp, 4
00B99909  mov ecx, [esi+8]
00B9990C  push offset aProtoLoungeCli_578; ")<-_proto_lounge_client::send_msma_miss"...
00B99911  push ecx
00B99912  push offset aId; " (id:"
00B99917  push eax
00B99918  push ebp
00B99919  mov byte ptr [esp+5Ch+var_4], 1
00B9991E  call sub_B03020
00B99923  add esp, 8
00B99926  push eax
00B99927  call sub_41D990
00B9992C  add esp, 8
00B9992F  mov ecx, eax
00B99931  call sub_ADC810
00B99936  push eax
00B99937  call sub_41D990
00B9993C  add esp, 8
00B9993F  lea ecx, [esp+48h+var_28]
00B99943  mov byte ptr [esp+48h+var_4], 0
```

## 3. 发送去向切片（提交之后的实际发送）

```asm
00B9999C  mov ecx, ebp
00B9999E  call sub_40DDF0
00B999A3  mov edx, [esi]
00B999A5  mov eax, [edx+58h]
00B999A8  mov ebp, ebx
00B999AA  sub ebp, edi
00B999AC  push ebp
00B999AD  push edi
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB998D1` | u16（2 字节） |
| `missionunit_set` | `0xB998DA` | struct（12 字节） |

## 5. 复合写入器（结构体字段逐项证据）

- `sub_B41BF0`（`0x00B41BF0..0x00B41C53`）：字段构成 `u16+u16+2×u32`，共 **12** 字节。
- 逐字段写线序列见取证记录（`ex1b` 中该函数全文）。
