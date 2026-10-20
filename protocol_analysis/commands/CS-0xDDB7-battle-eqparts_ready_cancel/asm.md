# 汇编证据 —— CS-0xDDB7-battle-eqparts_ready_cancel

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0x00B3C510`（`0x00B3C510`..`0x00B3C74A`），函数 `sub_B3C510`
- 命令名字符串：`)<-_proto_battle_client::send_eqparts_ready_cancel(` @ `0x00EE115C`
- opcode 写入：`0x00B3C58C`
- 声明容量：`0xE`（分配器容量 `push` @ `0x00B3C556`）
- 提交（`sub_B02FF0`）：`0x00B3C62D`
- 发送去向：`vt[0x58]` @ `0x00B3C6D8`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00B3C55F  push    eax
  00B3C560  lea     ecx, [esp+4Ch+var_34]
  00B3C564  call    sub_ABB2F0   ; <<< 初始化 {cur,end}（游标自 buf+2 起）
  00B3C569  lea     eax, [ebp+0Eh]
  00B3C56C  lea     ecx, [ebp+2]
  00B3C56F  cmp     ecx, eax
  00B3C571  mov     [esp+48h+var_4], 0
  00B3C579  mov     [esp+48h+var_30], ebp
  00B3C57D  mov     dword ptr [esp+48h+var_2C], eax
  00B3C581  ja      loc_B3C735
  00B3C587  lea     edx, [ecx+4]
  00B3C58A  cmp     edx, eax
  00B3C58C  mov     word ptr [ebp+0], 0DDB7h   ; <<< 内联写线（u16）
  00B3C592  ja      loc_B3C735
  00B3C598  mov     esi, [esp+48h+arg_0]
  00B3C59C  mov     [ecx], esi   ; <<< 内联写线（u32）
  00B3C59E  lea     ecx, [edx+2]
  00B3C5A1  cmp     ecx, eax
  00B3C5A3  ja      loc_B3C735
  00B3C5A9  mov     ax, word ptr [esp+48h+arg_4]
  00B3C5AE  mov     [esp+48h+var_30], ecx
  00B3C5B2  lea     ecx, [esp+48h+var_30]
  00B3C5B6  mov     [edx], ax   ; <<< 内联写线（u16）
  00B3C5B9  push    ecx
  00B3C5BA  lea     edx, [esp+4Ch+arg_8]
  00B3C5BE  push    edx
  00B3C5BF  call    sub_B02DA0   ; <<< 写线原语 u16
  00B3C5C4  add     esp, 8
  00B3C5C7  test    al, al
  00B3C5C9  jz      loc_B3C735
  00B3C5CF  mov     esi, [edi+3E94h]
  00B3C5D5  test    esi, esi
  00B3C5D7  mov     ebx, [esp+48h+var_30]
  00B3C5DB  jz      loc_B3C6D6
  00B3C5E1  lea     eax, [esp+48h+var_28]
  00B3C5E5  push    eax
  00B3C5E6  call    sub_CA0CE0
  00B3C5EB  add     esp, 4
  00B3C5EE  mov     ecx, [edi+8]
  00B3C5F1  push    offset aProtoBattleCli_263
  00B3C5F6  push    ecx
  00B3C5F7  push    offset aId
  00B3C5FC  push    eax
  00B3C5FD  push    esi
  00B3C5FE  mov     byte ptr [esp+5Ch+var_4], 1
  00B3C603  call    sub_B03020
  00B3C608  add     esp, 8
  00B3C60B  push    eax
  00B3C60C  call    sub_41D990
  00B3C611  add     esp, 8
  00B3C614  mov     ecx, eax
  00B3C616  call    sub_ADC810
  00B3C61B  push    eax
  00B3C61C  call    sub_41D990
  00B3C621  add     esp, 8
  00B3C624  lea     ecx, [esp+48h+var_28]
  00B3C628  mov     byte ptr [esp+48h+var_4], 0
  00B3C62D  call    sub_B02FF0   ; <<< 提交（C→S 闭合点）
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00B3C62D  call    sub_B02FF0
  00B3C632  mov     edx, [esp+48h+arg_0]
  00B3C636  push    offset word_F641DC
  00B3C63B  push    edx
  00B3C63C  push    offset aFrameCount
  00B3C641  push    esi
  00B3C642  call    sub_41D990
  00B3C647  add     esp, 8
  00B3C64A  mov     ecx, eax
  00B3C64C  call    sub_B03580
  00B3C651  push    eax
  00B3C652  call    sub_41D990
  00B3C657  mov     eax, [esp+50h+arg_4]
  00B3C65B  add     esp, 8
  00B3C65E  push    offset word_F641DC
  00B3C663  push    eax
  00B3C664  push    offset aAiEntId
  00B3C669  push    esi
  00B3C66A  call    sub_41D990
  00B3C66F  add     esp, 8
  00B3C672  mov     ecx, eax
  00B3C674  call    sub_B032A0
  00B3C679  push    eax
  00B3C67A  call    sub_41D990
  00B3C67F  mov     ecx, [esp+50h+arg_8]
  00B3C683  add     esp, 8
  00B3C686  push    ecx
  00B3C687  push    offset aGroupId
  00B3C68C  push    esi
  00B3C68D  call    sub_41D990
  00B3C692  add     esp, 8
  00B3C695  mov     ecx, eax
  00B3C697  call    sub_B032A0
  00B3C69C  push    offset aByte
  00B3C6A1  mov     edx, ebx
  00B3C6A3  sub     edx, ebp
  00B3C6A5  push    edx
  00B3C6A6  push    offset asc_EDAD58
  00B3C6AB  push    esi
  00B3C6AC  call    sub_41D990
  00B3C6B1  add     esp, 8
  00B3C6B4  mov     ecx, eax
  00B3C6B6  call    sub_B03580
  00B3C6BB  push    eax
  00B3C6BC  call    sub_41D990
  00B3C6C1  add     esp, 8
  00B3C6C4  mov     esi, eax
  00B3C6C6  push    0Ah
  00B3C6C8  mov     ecx, esi
  00B3C6CA  call    sub_B036E0
  00B3C6CF  mov     ecx, esi
  00B3C6D1  call    sub_40DDF0
  00B3C6D6  mov     eax, [edi]
  00B3C6D8  mov     edx, [eax+58h]
```

## 4. 发送去向切片

```asm
  00B3C6D6  mov     eax, [edi]
  00B3C6D8  mov     edx, [eax+58h]
  00B3C6DB  sub     ebx, ebp
  00B3C6DD  push    ebx
  00B3C6DE  push    ebp
  00B3C6DF  mov     ecx, edi
  00B3C6E1  call    edx
  00B3C6E3  test    al, al
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `00B3C58C` | u16 / 2 |
| `frame_count` | `0xB3C598`;`0xB3C59C` | u32 / 4 |
| `AI_ent_id` | `0xB3C5A9`;`0xB3C5B6` | u16 / 2 |
| `group_id` | `0xB3C5BF` | u16 / 2 |
