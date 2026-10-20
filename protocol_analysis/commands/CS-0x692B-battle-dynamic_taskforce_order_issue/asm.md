# 汇编证据 —— CS-0x692B-battle-dynamic_taskforce_order_issue

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B3F3F0 @ `0xb3f3f0`（`0xb3f3f0`..`0xb3f77e`）
- 命令名字符串：`)<-_proto_battle_client::send_dynamic_taskforce_order_issue(` @ `0xee1644`
- opcode 写入：`0xb3f46f`
- 声明容量：`0x5E`

## 2. 组包块切片（游标初始化 → 提交）

```asm
  0xb3f43e  mov     esi, eax
  0xb3f440  mov     eax, [edi+0Ch]
  0xb3f443  push    eax
  0xb3f444  lea     ecx, [esp+54h+var_3C]
  0xb3f448  mov     [esp+54h+var_38], esi
  0xb3f44c  call    sub_ABB2F0
  0xb3f451  lea     eax, [esi+5Eh]
  0xb3f454  lea     ecx, [esi+2]
  0xb3f457  cmp     ecx, eax
  0xb3f459  mov     [esp+50h+var_4], 0
  0xb3f461  mov     [esp+50h+var_30], esi
  0xb3f465  mov     dword ptr [esp+50h+var_2C], eax
  0xb3f469  ja      loc_B3F769
  0xb3f46f  mov     word ptr [esi], 692Bh
  0xb3f474  lea     esi, [ecx+1]
  0xb3f477  cmp     esi, eax
  0xb3f479  ja      loc_B3F769
  0xb3f47f  mov     dl, byte ptr [esp+50h+arg_0]
  0xb3f483  mov     [ecx], dl
  0xb3f485  lea     ecx, [esi+4]
  0xb3f488  cmp     ecx, eax
  0xb3f48a  ja      loc_B3F769
  0xb3f490  mov     ebp, [esp+50h+arg_C]
  0xb3f494  cmp     ebp, 33h ; '3'
  0xb3f497  mov     eax, [esp+50h+arg_4]
  0xb3f49b  mov     [esi], eax
  0xb3f49d  mov     [esp+50h+var_30], ecx
  0xb3f4a1  ja      loc_B3F769
  0xb3f4a7  lea     ecx, [esp+50h+var_30]
  0xb3f4ab  push    ecx
  0xb3f4ac  lea     edx, [esp+54h+arg_C]
  0xb3f4b0  push    edx
  0xb3f4b1  call    sub_B02D80
  0xb3f4b6  add     esp, 8
  0xb3f4b9  test    al, al
  0xb3f4bb  jz      loc_B3F769
  0xb3f4c1  xor     esi, esi
  0xb3f4c3  test    ebp, ebp
  0xb3f4c5  jbe     short loc_B3F4EB
  0xb3f4c7  mov     ecx, [esp+50h+arg_8]
  0xb3f4cb  lea     eax, [esp+50h+var_30]
  0xb3f4cf  push    eax
  0xb3f4d0  lea     edx, [esi+ecx]
  0xb3f4d3  push    edx
  0xb3f4d4  call    sub_B061C0
  0xb3f4d9  add     esp, 8
  0xb3f4dc  test    al, al
  0xb3f4de  jz      loc_B3F769
  0xb3f4e4  add     esi, 1
  0xb3f4e7  cmp     esi, ebp
  0xb3f4e9  jb      short loc_B3F4C7
  0xb3f4eb  mov     ebx, [esp+50h+arg_14]
  0xb3f4ef  cmp     ebx, 0Ch
  0xb3f4f2  ja      loc_B3F769
  0xb3f4f8  lea     eax, [esp+50h+var_30]
  0xb3f4fc  push    eax
  0xb3f4fd  lea     ecx, [esp+54h+arg_14]
  0xb3f501  push    ecx
  0xb3f502  call    sub_B02D80
  0xb3f507  add     esp, 8
  0xb3f50a  test    al, al
  0xb3f50c  jz      loc_B3F769
  0xb3f512  xor     esi, esi
  0xb3f514  test    ebx, ebx
  0xb3f516  jbe     short loc_B3F546
  0xb3f518  mov     edx, [esp+50h+arg_10]
  0xb3f51c  mov     [esp+50h+arg_C], edx
  0xb3f520  mov     ecx, [esp+50h+arg_C]
  0xb3f524  lea     eax, [esp+50h+var_30]
  0xb3f528  push    eax
  0xb3f529  push    ecx
  0xb3f52a  call    sub_B02DA0
  0xb3f52f  add     esp, 8
  0xb3f532  test    al, al
  0xb3f534  jz      loc_B3F769
  0xb3f53a  add     [esp+50h+arg_C], 2
  0xb3f53f  add     esi, 1
  0xb3f542  cmp     esi, ebx
  0xb3f544  jb      short loc_B3F520
  0xb3f546  mov     esi, [edi+3FD8h]
  0xb3f54c  test    esi, esi
  0xb3f54e  jz      loc_B3F702
  0xb3f554  lea     edx, [esp+50h+var_28]
  0xb3f558  push    edx
  0xb3f559  call    sub_CA0CE0
  0xb3f55e  add     esp, 4
  0xb3f561  mov     ecx, [edi+8]
  0xb3f564  push    offset aProtoBattleCli_279; ")<-_proto_battle_client::send_dynamic_t"...
  0xb3f569  push    ecx
  0xb3f56a  push    offset aId; " (id:"
  0xb3f56f  push    eax
  0xb3f570  push    esi
  0xb3f571  mov     byte ptr [esp+64h+var_4], 1
  0xb3f576  call    sub_B03020
  0xb3f57b  add     esp, 8
  0xb3f57e  push    eax
  0xb3f57f  call    sub_41D990
  0xb3f584  add     esp, 8
  0xb3f587  mov     ecx, eax
  0xb3f589  call    sub_ADC810
  0xb3f58e  push    eax
  0xb3f58f  call    sub_41D990
  0xb3f594  add     esp, 8
  0xb3f597  lea     ecx, [esp+50h+var_28]
  0xb3f59b  mov     byte ptr [esp+50h+var_4], 0
  0xb3f5a0  call    sub_B02FF0   <<<COMMIT
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb3f5af  push    offset aOrderKind; "order_kind="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb3f5d9  push    offset aOrderParam; "order_param="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb3f5f4  push    offset aSelectMembers; "select_members={"
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb3f65e  push    offset aSelectNpcs; "select_npcs={"
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb3f6c8  push    offset aByte; "]byte"
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
```

## 4. 发送去向切片

```asm
  0xb3f5cc  mov     eax, [esp+58h+arg_4]
  0xb3f5d0  add     esp, 8
  0xb3f5d3  push    offset word_F641DC
  0xb3f5d8  push    eax
  0xb3f5d9  push    offset aOrderParam; "order_param="
  0xb3f5de  push    esi
  0xb3f5df  call    sub_41D990
  0xb3f5e4  add     esp, 8
  0xb3f5e7  mov     ecx, eax
  0xb3f5e9  call    sub_B03580
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。
> 本批 50 条**全部命中同一去向槽 `vt[0x58]`**（与批次-16/17 一致）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB3F46F` | u16 |
| `order_kind` | `0xB3F483` | u8 |
| `order_param` | `0xB3F49B` | u32 |
| `select_members_num` | `0xB3F4B1` | u32 |
| `select_members` | `0xB3F4D4` | array<u8,N> |
| `select_npcs_num` | `0xB3F502` | u32 |
| `select_npcs` | `0xB3F52A` | array<u16,N> |
