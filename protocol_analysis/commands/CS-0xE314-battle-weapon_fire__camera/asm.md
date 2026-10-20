# 汇编证据 —— CS-0xE314-battle-weapon_fire__camera

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0x00B3A580`（`0x00B3A580`..`0x00B3A857`），函数 `sub_B3A580`
- 命令名字符串：`)<-_proto_battle_client::send_weapon_fire__camera(` @ `0x00EE0FE0`
- opcode 写入：`0x00B3A600`
- 声明容量：`0x76`（分配器容量 `push` @ `0x00B3A5C6`）
- 提交（`sub_B02FF0`）：`0x00B3A6E5`
- 发送去向：`vt[0x58]` @ `0x00B3A7E5`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00B3A5D4  mov     [esp+50h+var_34], edi
  00B3A5D8  call    sub_ABB2F0   ; <<< 初始化 {cur,end}（游标自 buf+2 起）
  00B3A5DD  lea     ecx, [edi+76h]
  00B3A5E0  lea     eax, [edi+2]
  00B3A5E3  cmp     eax, ecx
  00B3A5E5  mov     [esp+4Ch+var_4], 0
  00B3A5ED  mov     [esp+4Ch+var_30], edi
  00B3A5F1  mov     dword ptr [esp+4Ch+var_2C], ecx
  00B3A5F5  ja      loc_B3A842
  00B3A5FB  lea     edx, [eax+4]
  00B3A5FE  cmp     edx, ecx
  00B3A600  mov     word ptr [edi], 0E314h   ; <<< 内联写线（u16）
  00B3A605  ja      loc_B3A842
  00B3A60B  mov     ebp, [esp+4Ch+arg_8]
  00B3A60F  cmp     ebp, 33h
  00B3A612  mov     ecx, [esp+4Ch+arg_0]
  00B3A616  mov     [eax], ecx   ; <<< 内联写线（u32）
  00B3A618  mov     [esp+4Ch+var_30], edx
  00B3A61C  ja      loc_B3A842
  00B3A622  lea     edx, [esp+4Ch+var_30]
  00B3A626  push    edx
  00B3A627  lea     eax, [esp+50h+arg_8]
  00B3A62B  push    eax
  00B3A62C  call    sub_B02D80   ; <<< 写线原语 u32
  00B3A631  add     esp, 8
  00B3A634  test    al, al
  00B3A636  jz      loc_B3A842
  00B3A63C  mov     ecx, [esp+4Ch+var_30]
  00B3A640  xor     eax, eax
  00B3A642  test    ebp, ebp
  00B3A644  jbe     short loc_B3A672
  00B3A646  lea     edx, [ecx+2]
  00B3A649  lea     esp, [esp+0]
  00B3A650  cmp     edx, dword ptr [esp+4Ch+var_2C]
  00B3A654  ja      loc_B3A842
  00B3A65A  mov     esi, [esp+4Ch+arg_4]
  00B3A65E  mov     si, [esi+eax*2]
  00B3A662  mov     [ecx], si   ; <<< 内联写线（u16）
  00B3A665  add     eax, 1
  00B3A668  add     ecx, 2
  00B3A66B  add     edx, 2
  00B3A66E  cmp     eax, ebp
  00B3A670  jb      short loc_B3A650
  00B3A672  lea     eax, [ecx+2]
  00B3A675  cmp     eax, dword ptr [esp+4Ch+var_2C]
  00B3A679  mov     [esp+4Ch+arg_8], eax
  00B3A67D  ja      loc_B3A842
  00B3A683  mov     dx, word ptr [esp+4Ch+arg_C]
  00B3A688  mov     [ecx], dx   ; <<< 内联写线（u16）
  00B3A68B  mov     esi, [ebx+3E3Ch]
  00B3A691  test    esi, esi
  00B3A693  jz      loc_B3A7E1
  00B3A699  lea     eax, [esp+4Ch+var_28]
  00B3A69D  push    eax
  00B3A69E  call    sub_CA0CE0
  00B3A6A3  add     esp, 4
  00B3A6A6  mov     ecx, [ebx+8]
  00B3A6A9  push    offset aProtoBattleCli_254
  00B3A6AE  push    ecx
  00B3A6AF  push    offset aId
  00B3A6B4  push    eax
  00B3A6B5  push    esi
  00B3A6B6  mov     byte ptr [esp+60h+var_4], 1
  00B3A6BB  call    sub_B03020
  00B3A6C0  add     esp, 8
  00B3A6C3  push    eax
  00B3A6C4  call    sub_41D990
  00B3A6C9  add     esp, 8
  00B3A6CC  mov     ecx, eax
  00B3A6CE  call    sub_ADC810
  00B3A6D3  push    eax
  00B3A6D4  call    sub_41D990
  00B3A6D9  add     esp, 8
  00B3A6DC  lea     ecx, [esp+4Ch+var_28]
  00B3A6E0  mov     byte ptr [esp+4Ch+var_4], 0
  00B3A6E5  call    sub_B02FF0   ; <<< 提交（C→S 闭合点）
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00B3A6E5  call    sub_B02FF0
  00B3A6EA  mov     edx, [esp+4Ch+arg_0]
  00B3A6EE  push    offset word_F641DC
  00B3A6F3  push    edx
  00B3A6F4  push    offset aFrameCount
  00B3A6F9  push    esi
  00B3A6FA  call    sub_41D990
  00B3A6FF  add     esp, 8
  00B3A702  mov     ecx, eax
  00B3A704  call    sub_B03580
  00B3A709  push    eax
  00B3A70A  call    sub_41D990
  00B3A70F  push    offset aEntIds
  00B3A714  push    esi
  00B3A715  call    sub_41D990
  00B3A71A  add     esp, 10h
  00B3A71D  test    ebp, ebp
  00B3A71F  jbe     short loc_B3A730
  00B3A721  mov     eax, [esp+4Ch+arg_4]
  00B3A725  movzx   ecx, word ptr [eax]
  00B3A728  push    ecx
  00B3A729  mov     ecx, esi
  00B3A72B  call    sub_B032A0
  00B3A730  mov     edi, 1
  00B3A735  cmp     ebp, edi
  00B3A737  jbe     short loc_B3A765
  00B3A739  lea     esp, [esp+0]
  00B3A740  mov     edx, [esp+4Ch+arg_4]
  00B3A744  movzx   eax, word ptr [edx+edi*2]
  00B3A748  push    eax
  00B3A749  push    offset word_F641DC
  00B3A74E  push    esi
  00B3A74F  call    sub_41D990
  00B3A754  add     esp, 8
  00B3A757  mov     ecx, eax
  00B3A759  call    sub_B032A0
  00B3A75E  add     edi, 1
  00B3A761  cmp     edi, ebp
  00B3A763  jb      short loc_B3A740
  00B3A765  push    offset word_F641DC
  00B3A76A  push    offset unk_EDABE4
  00B3A76F  push    esi
  00B3A770  call    sub_41D990
  00B3A775  add     esp, 8
  00B3A778  push    eax
  00B3A779  call    sub_41D990
  00B3A77E  mov     ecx, [esp+54h+arg_C]
  00B3A782  add     esp, 8
  00B3A785  push    ecx
  00B3A786  push    offset aAiEntId
  00B3A78B  push    esi
  00B3A78C  call    sub_41D990
  00B3A791  add     esp, 8
  00B3A794  mov     ecx, eax
  00B3A796  call    sub_B032A0
  00B3A79B  mov     edx, [esp+4Ch+arg_8]
  00B3A79F  sub     edx, [esp+4Ch+var_34]
  00B3A7A3  push    offset aByte
  00B3A7A8  push    edx
  00B3A7A9  push    offset asc_EDAD58
  00B3A7AE  push    esi
  00B3A7AF  call    sub_41D990
  00B3A7B4  add     esp, 8
  00B3A7B7  mov     ecx, eax
  00B3A7B9  call    sub_B03580
  00B3A7BE  push    eax
  00B3A7BF  call    sub_41D990
  00B3A7C4  add     esp, 8
  00B3A7C7  mov     esi, eax
  00B3A7C9  push    0Ah
  00B3A7CB  mov     ecx, esi
  00B3A7CD  call    sub_B036E0
  00B3A7D2  mov     ecx, esi
  00B3A7D4  call    sub_40DDF0
  00B3A7D9  mov     edi, [esp+4Ch+var_34]
  00B3A7DD  mov     eax, [esp+4Ch+arg_8]
  00B3A7E1  mov     esi, eax
  00B3A7E3  mov     eax, [ebx]
  00B3A7E5  mov     edx, [eax+58h]
```

## 4. 发送去向切片

```asm
  00B3A7E1  mov     esi, eax
  00B3A7E3  mov     eax, [ebx]
  00B3A7E5  mov     edx, [eax+58h]
  00B3A7E8  sub     esi, edi
  00B3A7EA  push    esi
  00B3A7EB  push    edi
  00B3A7EC  mov     ecx, ebx
  00B3A7EE  call    edx
  00B3A7F0  test    al, al
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `00B3A600` | u16 / 2 |
| `frame_count` | `0xB3A612`;`0xB3A616` | u32 / 4 |
| `ent_ids_num` | `0xB3A60F`;`0xB3A62C` | u32 / 4 |
| `ent_ids` | `0xB3A65E`;`0xB3A662`;`0xB3A66E` | array<u16,N> / var |
| `AI_ent_id` | `0xB3A683`;`0xB3A688` | u16 / 2 |
