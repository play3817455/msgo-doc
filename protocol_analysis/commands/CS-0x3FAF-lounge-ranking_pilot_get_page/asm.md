# 汇编证据 —— CS-0x3FAF-lounge-ranking_pilot_get_page

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_BA3820 @ `0x00ba3820`（`0x00ba3820`..`0x00ba3a23`）
- 命令名字符串：`)<-_proto_lounge_client::send_ranking_pilot_get_page(` @ `0xeece28`
- 声明容量：`0x12`（分配器指纹 @ `0xBA3866`）

## 2. 组包块切片（游标初始化 → 提交）

```asm
00BA3874  call sub_ABB2F0
00BA3879  lea ecx, [ebp+12h]
00BA387C  lea eax, [ebp+2]
00BA387F  cmp eax, ecx
00BA3881  mov [esp+48h+var_4], 0
00BA3889  mov [esp+48h+var_30], ebp
00BA388D  mov dword ptr [esp+48h+var_2C], ecx
00BA3891  ja loc_BA3A0E
00BA3897  mov edx, [esp+48h+arg_0]
00BA389B  lea ecx, [esp+48h+var_30]
00BA389F  push ecx
00BA38A0  push edx
00BA38A1  mov word ptr [ebp+0], 3FAFh
00BA38A7  mov [esp+50h+var_30], eax
00BA38AB  call sub_B42060
00BA38B0  add esp, 8
00BA38B3  test al, al
00BA38B5  jz loc_BA3A0E
00BA38BB  mov eax, [esp+48h+var_30]
00BA38BF  lea ebx, [eax+4]
00BA38C2  cmp ebx, dword ptr [esp+48h+var_2C]
00BA38C6  ja loc_BA3A0E
00BA38CC  mov ecx, [esp+48h+arg_4]
00BA38D0  mov [eax], ecx
00BA38D2  mov edi, [esi+8174h]
00BA38D8  test edi, edi
00BA38DA  jz loc_BA39AF
00BA38E0  lea edx, [esp+48h+var_28]
00BA38E4  push edx
00BA38E5  call sub_CA0CE0
00BA38EA  add esp, 4
00BA38ED  mov ecx, [esi+8]
00BA38F0  push offset aProtoLoungeCli_422; ")<-_proto_lounge_client::send_ranking_p"...
00BA38F5  push ecx
00BA38F6  push offset aId; " (id:"
00BA38FB  push eax
00BA38FC  push edi
00BA38FD  mov byte ptr [esp+5Ch+var_4], 1
00BA3902  call sub_B03020
00BA3907  add esp, 8
00BA390A  push eax
00BA390B  call sub_41D990
00BA3910  add esp, 8
00BA3913  mov ecx, eax
00BA3915  call sub_ADC810
00BA391A  push eax
00BA391B  call sub_41D990
00BA3920  add esp, 8
00BA3923  lea ecx, [esp+48h+var_28]
00BA3927  mov byte ptr [esp+48h+var_4], 0
```

## 3. 发送去向切片（提交之后的实际发送）

```asm
00BA39A8  mov ecx, edi
00BA39AA  call sub_40DDF0
00BA39AF  mov edx, [esi]
00BA39B1  mov eax, [edx+58h]
00BA39B4  sub ebx, ebp
00BA39B6  push ebx
00BA39B7  push ebp
00BA39B8  mov ecx, esi
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xBA38A1` | u16（2 字节） |
| `order` | `0xBA38AB` | struct（10 字节） |
| `page` | `0xBA38D0` | u32（4 字节） |

## 5. 复合写入器（结构体字段逐项证据）

- `sub_B42060`（`0x00B42060..0x00B420D3`）：字段构成 `5×u16`，共 **10** 字节。
- 逐字段写线序列见取证记录（`ex1b` 中该函数全文）。
