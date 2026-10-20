# 汇编证据 —— CS-0x5A5D-battle-eqparts_exec_toggle

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B3C750 @ `0xb3c750`（`0xb3c750`..`0xb3c98a`）
- 命令名字符串：`)<-_proto_battle_client::send_eqparts_exec_toggle(` @ `0xee1194`
- opcode 写入：`0xb3c7cc`
- 声明容量：`0xE`

## 2. 组包块切片（游标初始化 → 提交）

```asm
  0xb3c79a  mov     ebp, eax
  0xb3c79c  mov     eax, [edi+0Ch]
  0xb3c79f  push    eax
  0xb3c7a0  lea     ecx, [esp+4Ch+var_34]
  0xb3c7a4  call    sub_ABB2F0
  0xb3c7a9  lea     eax, [ebp+0Eh]
  0xb3c7ac  lea     ecx, [ebp+2]
  0xb3c7af  cmp     ecx, eax
  0xb3c7b1  mov     [esp+48h+var_4], 0
  0xb3c7b9  mov     [esp+48h+var_30], ebp
  0xb3c7bd  mov     dword ptr [esp+48h+var_2C], eax
  0xb3c7c1  ja      loc_B3C975
  0xb3c7c7  lea     edx, [ecx+4]
  0xb3c7ca  cmp     edx, eax
  0xb3c7cc  mov     word ptr [ebp+0], 5A5Dh
  0xb3c7d2  ja      loc_B3C975
  0xb3c7d8  mov     esi, [esp+48h+arg_0]
  0xb3c7dc  mov     [ecx], esi
  0xb3c7de  lea     ecx, [edx+2]
  0xb3c7e1  cmp     ecx, eax
  0xb3c7e3  ja      loc_B3C975
  0xb3c7e9  mov     ax, word ptr [esp+48h+arg_4]
  0xb3c7ee  mov     [esp+48h+var_30], ecx
  0xb3c7f2  lea     ecx, [esp+48h+var_30]
  0xb3c7f6  mov     [edx], ax
  0xb3c7f9  push    ecx
  0xb3c7fa  lea     edx, [esp+4Ch+arg_8]
  0xb3c7fe  push    edx
  0xb3c7ff  call    sub_B02DA0
  0xb3c804  add     esp, 8
  0xb3c807  test    al, al
  0xb3c809  jz      loc_B3C975
  0xb3c80f  mov     esi, [edi+3E9Ch]
  0xb3c815  test    esi, esi
  0xb3c817  mov     ebx, [esp+48h+var_30]
  0xb3c81b  jz      loc_B3C916
  0xb3c821  lea     eax, [esp+48h+var_28]
  0xb3c825  push    eax
  0xb3c826  call    sub_CA0CE0
  0xb3c82b  add     esp, 4
  0xb3c82e  mov     ecx, [edi+8]
  0xb3c831  push    offset aProtoBattleCli_255; ")<-_proto_battle_client::send_eqparts_e"...
  0xb3c836  push    ecx
  0xb3c837  push    offset aId; " (id:"
  0xb3c83c  push    eax
  0xb3c83d  push    esi
  0xb3c83e  mov     byte ptr [esp+5Ch+var_4], 1
  0xb3c843  call    sub_B03020
  0xb3c848  add     esp, 8
  0xb3c84b  push    eax
  0xb3c84c  call    sub_41D990
  0xb3c851  add     esp, 8
  0xb3c854  mov     ecx, eax
  0xb3c856  call    sub_ADC810
  0xb3c85b  push    eax
  0xb3c85c  call    sub_41D990
  0xb3c861  add     esp, 8
  0xb3c864  lea     ecx, [esp+48h+var_28]
  0xb3c868  mov     byte ptr [esp+48h+var_4], 0
  0xb3c86d  call    sub_B02FF0   <<<COMMIT
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb3c87c  push    offset aFrameCount; "frame_count="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb3c8a4  push    offset aAiEntId; "AI_ent_id="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb3c8c7  push    offset aGroupId; "group_id="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb3c8dc  push    offset aByte; "]byte"
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
```

## 4. 发送去向切片

```asm
  0xb3c918  mov     edx, [eax+58h]
  0xb3c91b  sub     ebx, ebp
  0xb3c91d  push    ebx
  0xb3c91e  push    ebp
  0xb3c91f  mov     ecx, edi
  0xb3c921  call    edx
  0xb3c923  test    al, al
  0xb3c925  jz      short loc_B3C975
  0xb3c927  mov     eax, [edi+3BF0h]
  0xb3c92d  test    eax, eax
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。
> 本批 50 条**全部命中同一去向槽 `vt[0x58]`**（与批次-16/17 一致）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB3C7CC` | u16 |
| `frame_count` | `0xB3C7DC` | u32 |
| `AI_ent_id` | `0xB3C7F6` | u16 |
| `group_id` | `0xB3C7FF` | u16 |
