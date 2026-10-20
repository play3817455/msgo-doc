# 汇编证据 —— SC-0x16AA-battle-eqparts_execute

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 case 入口 + 解码缓冲申请（容量 `0x2086`）

```asm
; VA: 0xB10671 .. 0xB106A1
0xB10671  call    sub_B05DA0               ; case 起始守卫（不读线）
0xB10676  test    al, al
0xB10678  jz      loc_B317C7
0xB1067E  mov     ecx, [esi+0Ch]
0xB10681  mov     eax, [ecx]
0xB10683  mov     edx, [eax+78h]
0xB10686  push    2086h                    ; ← 容量 8326 = 2 + 4 + 416×20
0xB1068B  call    edx
0xB1068D  mov     [esp+1B3Ch+var_1B14], eax ; 解码缓冲基址
0xB10691  mov     eax, [esi+0Ch]
0xB10694  push    eax
0xB10695  lea     ecx, [esp+1B40h+var_18E4]
0xB1069C  call    sub_ABB2F0               ; 初始化线游标
```

## E2 字段 1：`ent_id`（u16，偏移 0）

```asm
; VA: 0xB106A1 .. 0xB106D0
0xB106B5  call    sub_B413B0               ; u16 槽预留（非字段）
0xB106C4  call    sub_B02DF0               ; ← 读 u16（消费 2 字节）
0xB106CC  test    al, al
0xB106CE  jnz     short loc_B106EC
0xB106D7  push    0A3h                     ; ← 错误码
```

## E3 字段 2：`parts_num`（u32，偏移 2）+ 上限 416

```asm
; VA: 0xB106EC .. 0xB1072A
0xB106EC  lea     ecx, [esp+1B3Ch+var_1B28]
0xB106F0  push    ecx
0xB106F1  lea     edx, [esp+1B40h+var_1B08]
0xB106F5  push    edx
0xB106F6  call    sub_B02DD0               ; ← 读 u32（消费 4 字节）
0xB106FE  test    al, al
0xB10700  jnz     short loc_B1071E
0xB10709  push    0A3h
0xB1071E  mov     ebx, [esp+1B3Ch+var_1B08] ; N
0xB10722  cmp     ebx, 1A0h                ; ← 上限 416
0xB10728  ja      short loc_B10702         ; > 416 ⇒ 报错
```

## E4 字段 3：数组预留 `sub_B06090`（步进 `0x14 = 20`，非字段）+ 元素循环

```asm
; VA: 0xB1072A .. 0xB10769
0xB1072A  push    ebx                      ; N
0xB1072B  lea     eax, [esp+1B40h+var_1B14] ; 缓冲游标
0xB1072F  push    eax
0xB10730  call    sub_B06090               ; 预留 N×0x14（推进缓冲游标，不是字段）
0xB10739  xor     edi, edi
0xB1073B  test    ebx, ebx
0xB1073D  jbe     short loc_B1077B
0xB1073F  mov     ecx, [esp+1B3Ch+var_1B08]
0xB10743  mov     [esp+1B3Ch+var_1B2C], ecx ; 元素槽游标（初值=数组基址）
0xB10747  mov     eax, [esp+1B3Ch+var_1B2C]
0xB1074B  lea     edx, [esp+1B3Ch+var_1B28] ; &线游标
0xB1074F  push    edx
0xB10750  push    eax
0xB10751  call    sub_B06CF0               ; ← 元素读取器（消费 17B）
0xB10759  test    al, al
0xB1075B  jz      short loc_B1076B
0xB1075D  add     [esp+1B3Ch+var_1B2C], 14h ; ← 缓冲步进 20（≠ 元素线长 17）
0xB10762  add     edi, 1
0xB10765  cmp     edi, ebx
0xB10767  jb      short loc_B10747
```

```asm
; sub_B06090 函数体（0xB06090 .. 0xB060BB）：每槽步进 0x14 = 20
0xB06090  mov     edx, [esp+arg_0]         ; &缓冲游标
0xB06094  mov     eax, ecx                 ; out
0xB0609B  mov     [eax+4], esi             ; out[4] = N
0xB060A0  mov     [eax], ecx               ; out[0] = 基址
0xB060B0  add     dword ptr [edx], 14h     ; ← 每元素步进 0x14 = 20
0xB060B6  cmp     ecx, [eax+4]
0xB060B9  jl      short loc_B060B0
```

```asm
; 元素读取器 sub_B06CF0 整函数（0xB06CF0 .. 0xB06D71）：线长 = 4+4+1+2+4+2 = 17
0xB06CFF  mov     edx, [eax]               ; ← u32 @ elem+0   → [edi+0]
0xB06D08  add     dword ptr [esi], 4
0xB06D15  mov     edx, [eax]               ; ← u32 @ elem+4   → [edi+4]
0xB06D1A  add     dword ptr [esi], 4
0xB06D27  mov     dl, [eax]                ; ← u8  @ elem+8   → [edi+8]
0xB06D2C  add     dword ptr [esi], 1
0xB06D39  mov     dx, [eax]                ; ← u16 @ elem+0xA → [edi+0Ah]
0xB06D44  add     dword ptr [esi], 2
0xB06D48  call    sub_B02DD0               ; ← u32 @ elem+0xC → [edi+0Ch]（消费 4）
0xB06D5D  add     edi, 10h
0xB06D62  call    sub_B02DF0               ; ← u16 @ elem+0x10→ [edi+0x10]（消费 2，成功路径）
```

## E5 长度闭合（循环之后：游标 == 报文末尾）

```asm
; VA: 0xB1077B .. 0xB1079C
0xB1077B  mov     ecx, [esp+1B3Ch+var_1B28] ; 读完数组后的线游标
0xB1077F  cmp     ecx, [esp+1B3Ch+var_1B24] ; vs 报文末尾
0xB10785  jz      short loc_B107A1          ; ← 不等 ⇒ push 1 / push 0A3h 报错
0xB1078E  push    0A3h
0xB10793  call    eax
```

## E6 含义取证：元素打印器 `sub_B09130`（6 个成员名 + 内存偏移）

```asm
; VA: 0xB09145 .. 0xB09221（元素打印器，元素内存步进 0x14）
0xB09145  mov     eax, [edi]
0xB09150  push    offset aItemId            ; ← "item_id="        [elem+0]
0xB0916B  mov     ecx, [edi+4]
0xB09177  push    offset aEffectMsec        ; ← "effect_msec="    [elem+4]
0xB09192  movsx   edx, byte ptr [edi+8]     ; ← [elem+8]，符号扩展 ⇒ i8
0xB0919F  push    offset aEffectCatego      ; ← "effect_catego="
0xB091BA  movzx   eax, word ptr [edi+0Ah]   ; ← [elem+0xA]，2 字节
0xB091C7  push    offset aEffectParam       ; ← "effect_param="
0xB091E2  mov     ecx, [edi+0Ch]            ; ← [elem+0xC]，4 字节
0xB091EE  push    offset aEffectValue       ; ← "effect_value="
0xB09209  movzx   edx, word ptr [edi+10h]   ; ← [elem+0x10]，2 字节
0xB09211  push    offset aEffectValue2      ; ← "effect_value2="
```

## E7 去向：`vt[0x20C](ent_id, parts_exec 数组, N)`

```asm
; VA: 0xB108DE .. 0xB10906
0xB108DE  mov     ecx, [esp+1B3Ch+var_1B08] ; 数组基址
0xB108E2  mov     edx, [esp+1B3Ch+var_1B20] ; ent_id 槽
0xB108E6  mov     eax, [esi]
0xB108E8  push    ebx                       ; 实参 3 = N
0xB108E9  push    ecx                       ; 实参 2 = 数组基址
0xB108EA  movzx   ecx, word ptr [edx]       ; ent_id
0xB108ED  mov     edx, [eax+20Ch]           ; ← vt[0x20C]
0xB108F3  push    ecx                       ; 实参 1 = ent_id
0xB108F4  mov     ecx, esi
0xB108F6  call    edx
0xB108F8  add     dword ptr [esi+2170h], 1  ; 本命令接收计数（64 位）
```
