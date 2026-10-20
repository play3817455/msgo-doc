# 汇编证据 —— CS-0x49D1-lounge-clan_invite_pilotlist_get

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_BA2680 @ `0xba2680`（`0xba2680`..`0xba2883`）
- 命令名字符串：`)<-_proto_lounge_client::send_clan_invite_pilotlist_get(` @ `0xeecc3c`
- opcode 写入：`0xba26fc`
- 声明容量：`0x12`

## 2. 组包块切片（游标初始化 → 提交）

```asm
  0xba26ca  mov     ebp, eax
  0xba26cc  mov     eax, [esi+0Ch]
  0xba26cf  push    eax
  0xba26d0  lea     ecx, [esp+4Ch+var_34]
  0xba26d4  call    sub_ABB2F0
  0xba26d9  lea     ecx, [ebp+12h]
  0xba26dc  lea     eax, [ebp+2]
  0xba26df  cmp     eax, ecx
  0xba26e1  mov     [esp+48h+var_4], 0
  0xba26e9  mov     [esp+48h+var_30], ebp
  0xba26ed  mov     dword ptr [esp+48h+var_2C], ecx
  0xba26f1  ja      loc_BA286E
  0xba26f7  lea     edx, [eax+4]
  0xba26fa  cmp     edx, ecx
  0xba26fc  mov     word ptr [ebp+0], 49D1h
  0xba2702  ja      loc_BA286E
  0xba2708  mov     ecx, [esp+48h+arg_0]
  0xba270c  mov     [esp+48h+var_30], edx
  0xba2710  lea     edx, [esp+48h+var_30]
  0xba2714  mov     [eax], ecx
  0xba2716  mov     eax, [esp+48h+arg_4]
  0xba271a  push    edx
  0xba271b  push    eax
  0xba271c  call    sub_B41E00
  0xba2721  add     esp, 8
  0xba2724  test    al, al
  0xba2726  jz      loc_BA286E
  0xba272c  mov     edi, [esi+8124h]
  0xba2732  test    edi, edi
  0xba2734  mov     ebx, [esp+48h+var_30]
  0xba2738  jz      loc_BA280D
  0xba273e  lea     ecx, [esp+48h+var_28]
  0xba2742  push    ecx
  0xba2743  call    sub_CA0CE0
  0xba2748  add     esp, 4
  0xba274b  mov     edx, [esi+8]
  0xba274e  push    offset aProtoLoungeCli_488; ")<-_proto_lounge_client::send_clan_invi"...
  0xba2753  push    edx
  0xba2754  push    offset aId; " (id:"
  0xba2759  push    eax
  0xba275a  push    edi
  0xba275b  mov     byte ptr [esp+5Ch+var_4], 1
  0xba2760  call    sub_B03020
  0xba2765  add     esp, 8
  0xba2768  push    eax
  0xba2769  call    sub_41D990
  0xba276e  add     esp, 8
  0xba2771  mov     ecx, eax
  0xba2773  call    sub_ADC810
  0xba2778  push    eax
  0xba2779  call    sub_41D990
  0xba277e  add     esp, 8
  0xba2781  lea     ecx, [esp+48h+var_28]
  0xba2785  mov     byte ptr [esp+48h+var_4], 0
  0xba278a  call    sub_B02FF0   <<<COMMIT
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xba2799  push    offset aPage_0; "page="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xba27bc  push    offset aSortInfo; "sort_info="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xba27d3  push    offset aByte; "]byte"
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
```

## 4. 发送去向切片

```asm
  0xba280f  mov     edx, [eax+58h]
  0xba2812  mov     edi, ebx
  0xba2814  sub     edi, ebp
  0xba2816  push    edi
  0xba2817  push    ebp
  0xba2818  mov     ecx, esi
  0xba281a  call    edx
  0xba281c  test    al, al
  0xba281e  jz      short loc_BA286E
  0xba2820  mov     eax, [esi+79A8h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。
> 本批 50 条**全部命中同一去向槽 `vt[0x58]`**（与批次-16/17 一致）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xBA26FC` | u16 |
| `page` | `0xBA2714` | u32 |
| `sort_info` | `0xBA271C` | struct |
