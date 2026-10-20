# 汇编证据 —— CS-0x2749-lounge-clan_search_sortfilter_get

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_BA1A20 @ `0x00ba1a20`（`0x00ba1a20`..`0x00ba1c25`）
- 命令名字符串：`)<-_proto_lounge_client::send_clan_search_sortfilter_get(` @ `0xeecad8`
- 声明容量：`0x1A`（分配器指纹 @ `0xBA1A66`）

## 2. 组包块切片（游标初始化 → 提交）

```asm
00BA1A74  call sub_ABB2F0
00BA1A79  lea ecx, [ebp+1Ah]
00BA1A7C  lea eax, [ebp+2]
00BA1A7F  cmp eax, ecx
00BA1A81  mov [esp+48h+var_4], 0
00BA1A89  mov [esp+48h+var_30], ebp
00BA1A8D  mov dword ptr [esp+48h+var_2C], ecx
00BA1A91  ja loc_BA1C10
00BA1A97  lea edx, [eax+1]
00BA1A9A  cmp edx, ecx
00BA1A9C  mov word ptr [ebp+0], 2749h
00BA1AA2  ja loc_BA1C10
00BA1AA8  mov cl, byte ptr [esp+48h+arg_0]
00BA1AAC  mov [esp+48h+var_30], edx
00BA1AB0  lea edx, [esp+48h+var_30]
00BA1AB4  mov [eax], cl
00BA1AB6  mov eax, [esp+48h+arg_4]
00BA1ABA  push edx
00BA1ABB  push eax
00BA1ABC  call sub_B41F60
00BA1AC1  add esp, 8
00BA1AC4  test al, al
00BA1AC6  jz loc_BA1C10
00BA1ACC  mov edi, [esi+80F4h]
00BA1AD2  test edi, edi
00BA1AD4  mov ebx, [esp+48h+var_30]
00BA1AD8  jz loc_BA1BAF
00BA1ADE  lea ecx, [esp+48h+var_28]
00BA1AE2  push ecx
00BA1AE3  call sub_CA0CE0
00BA1AE8  add esp, 4
00BA1AEB  mov edx, [esi+8]
00BA1AEE  push offset aProtoLoungeCli_486; ")<-_proto_lounge_client::send_clan_sear"...
00BA1AF3  push edx
00BA1AF4  push offset aId; " (id:"
00BA1AF9  push eax
00BA1AFA  push edi
00BA1AFB  mov byte ptr [esp+5Ch+var_4], 1
00BA1B00  call sub_B03020
00BA1B05  add esp, 8
00BA1B08  push eax
00BA1B09  call sub_41D990
00BA1B0E  add esp, 8
00BA1B11  mov ecx, eax
00BA1B13  call sub_ADC810
00BA1B18  push eax
00BA1B19  call sub_41D990
00BA1B1E  add esp, 8
00BA1B21  lea ecx, [esp+48h+var_28]
00BA1B25  mov byte ptr [esp+48h+var_4], 0
```

## 3. 发送去向切片（提交之后的实际发送）

```asm
00BA1BA8  mov ecx, edi
00BA1BAA  call sub_40DDF0
00BA1BAF  mov eax, [esi]
00BA1BB1  mov edx, [eax+58h]
00BA1BB4  mov edi, ebx
00BA1BB6  sub edi, ebp
00BA1BB8  push edi
00BA1BB9  push ebp
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xBA1A9C` | u16（2 字节） |
| `clan_kind` | `0xBA1AB4` | u8（1 字节） |
| `sort_info` | `0xBA1ABC` | struct（18 字节） |

## 5. 复合写入器（结构体字段逐项证据）

- `sub_B41F60`（`0x00B41F60..0x00B42054`）：字段构成 `2+1+1+1+1+1+1+2+2+1+4+1`，共 **18** 字节。
- 逐字段写线序列见取证记录（`ex1b` 中该函数全文）。
