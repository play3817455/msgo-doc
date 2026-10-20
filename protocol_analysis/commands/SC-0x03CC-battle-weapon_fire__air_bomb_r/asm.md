# 汇编证据 —— SC-0x03CC-battle-weapon_fire__air_bomb_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 case 入口 + 解码缓冲申请（容量 0x12 = 18）

```asm
; VA: 0xB0CD3B .. 0xB0CD63
0xB0CD3B  call    sub_B05DA0               ; case 级开关检查（前置 push 86h = 开关号）
0xB0CD40  test    al, al
0xB0CD42  jz      loc_B317C7
0xB0CD48  mov     ecx, [esi+0Ch]
0xB0CD4B  mov     eax, [ecx]
0xB0CD4D  mov     edx, [eax+78h]
0xB0CD50  push    12h                      ; ← 容量 18（旁证，不是线长）
0xB0CD52  call    edx
0xB0CD54  mov     [esp+1B3Ch+var_1B1C], eax
0xB0CD58  mov     eax, [esi+0Ch]
0xB0CD5B  push    eax
0xB0CD5C  lea     ecx, [esp+1B40h+var_1A4C]
0xB0CD63  call    sub_ABB2F0
```

## E2 字段 1..3：u16 + u32 + u32

```asm
; VA: 0xB0CD68 .. 0xB0CDF4
0xB0CD7C  call    sub_B413B0               ; 预留 2 字节槽
0xB0CD8B  call    sub_B02DF0               ; ← ent_id（u16，槽 var_1AF0）
0xB0CDBC  call    sub_B41470               ; 预留 4 字节槽
0xB0CDCB  call    sub_B02DD0               ; ← itemid（u32，槽 var_1AF8）
0xB0CDE0  call    sub_B41470               ; 预留 4 字节槽
0xB0CDEF  call    sub_B02DD0               ; ← airbomb_id（u32，槽 var_1AEC）
```

读取器本体：

```asm
; VA: 0xB02DF0 .. 0xB02E10   （u16：游标 +2）
0xB02E01  mov     cx, [ecx]
0xB02E0B  add     dword ptr [eax], 2

; VA: 0xB02DD0 .. 0xB02DEE   （u32：游标 +4）
0xB02DE1  mov     ecx, [ecx]
0xB02DE9  add     dword ptr [eax], 4
```

## E3 字段 4..6：3 × u16（target_x/y/z）

```asm
; VA: 0xB0CDFB .. 0xB0CE6B
0xB0CE04  call    sub_B413B0
0xB0CE13  call    sub_B02DF0               ; ← target_x（槽 var_1B00）
0xB0CE2C  call    sub_B413B0
0xB0CE3B  call    sub_B02DF0               ; ← target_y（槽 var_1B0C）
0xB0CE54  call    sub_B413B0
0xB0CE63  call    sub_B02DF0               ; ← target_z（槽 var_1B18）
```

## E4 字段 7..8：2 × u8（`sub_B05E30` 预留 + `sub_B06230` 读）

```asm
; VA: 0xB0CE73 .. 0xB0CEBB
0xB0CE7C  call    sub_B05E30               ; 预留 1 字节槽
0xB0CE8B  call    sub_B06230               ; ← shot0_drop1_impact2（u8，槽 var_1B20）
0xB0CEA4  call    sub_B05E30
0xB0CEB3  call    sub_B06230               ; ← fx_opt（u8，槽 var_1B2C）
```

预留函数 + 读取器本体（读 **u8**，游标 +1）：

```asm
; VA: 0xB05E30 .. 0xB05E3D
0xB05E30  mov     eax, ecx
0xB05E32  mov     ecx, [esp+arg_0]
0xB05E36  mov     edx, [ecx]
0xB05E38  mov     [eax], edx
0xB05E3A  add     dword ptr [ecx], 1
0xB05E3D  retn    4

; VA: 0xB06230 .. 0xB0624E
0xB06230  mov     eax, [esp+arg_4]
0xB06234  mov     ecx, [eax]
0xB06236  lea     edx, [ecx+1]
0xB06239  cmp     edx, [eax+4]
0xB0623C  jbe     short loc_B06241
0xB0623E  xor     al, al
0xB06240  retn
0xB06241  mov     cl, [ecx]                ; ← 读 u8（byte）
0xB06243  mov     edx, [esp+arg_0]
0xB06247  mov     [edx], cl
0xB06249  add     dword ptr [eax], 1        ; ← 游标 +1 ⇒ 宽度 1
0xB0624C  mov     al, 1
0xB0624E  retn
```

## E5 长度闭合（负载恰好 18 字节：2+4+4+2+2+2+1+1）

```asm
; VA: 0xB0CEC3 .. 0xB0CECD
0xB0CEC3  mov     ebx, [esp+1B3Ch+var_1B28]   ; 读完后的游标
0xB0CEC7  cmp     ebx, [esp+1B3Ch+var_1B24]   ; vs 报文末尾
0xB0CECB  mov     ecx, esi
0xB0CECD  jz      short loc_B0CEE9            ; ← 不等则 push 86h 报错
```

## E6 含义取证：块内日志格式串（8 条）

```asm
; VA: 0xB0CF5A .. 0xB0D089
0xB0CF5E  movzx   ecx, word ptr [eax]
0xB0CF67  push    offset aEntId               ; "ent_id="
0xB0CF86  mov     eax, [edx]
0xB0CF91  push    offset aItemid              ; "itemid="
0xB0CFB0  mov     edx, [ecx]
0xB0CFBB  push    offset aAirbombId           ; "airbomb_id="
0xB0CFDA  movzx   ecx, word ptr [eax]
0xB0CFE6  push    offset aTargetX             ; "target_x="
0xB0D005  movzx   eax, word ptr [edx]
0xB0D011  push    offset aTargetY             ; "target_y="
0xB0D030  movzx   edx, word ptr [ecx]
0xB0D03C  push    offset aTargetZ             ; "target_z="
0xB0D064  push    offset aShot0Drop1Impa      ; "shot0_drop1_impact2="
0xB0D089  push    offset aFxOpt               ; "fx_opt="
```

`shot0_drop1_impact2` / `fx_opt` 的打印走 `sub_B0C1F0`（**符号扩展**取 1 字节，与线类型 u8 的「零扩展读取」不冲突 —— 读取侧为 `mov cl,[ecx]`）：

```asm
; VA: 0xB0C1F0 .. 0xB0C207
0xB0C1F0  mov     eax, [esp+arg_4]
0xB0C1F4  movsx   ecx, byte ptr [eax]
0xB0C1FD  mov     ecx, esi
0xB0C1FF  call    sub_B03580               ; 打印有符号整数
```

## E7 去向：8 个值一次性交 `vt[0x1C4]`

```asm
; VA: 0xB0D0D3 .. 0xB0D11B
0xB0D0D3  mov     eax, [esp+1B3Ch+var_1B2C]   ; fx_opt 槽
0xB0D0D7  movzx   ecx, byte ptr [eax]
0xB0D0DA  mov     eax, [esp+1B3Ch+var_1B20]   ; shot0_drop1_impact2 槽
0xB0D0DE  push    ecx                         ; fx_opt
0xB0D0DF  movzx   ecx, byte ptr [eax]
0xB0D0E2  mov     eax, [esp+1B40h+var_1B18]   ; target_z
0xB0D0E6  push    ecx                         ; shot0_drop1_impact2
0xB0D0E7  movzx   ecx, word ptr [eax]
0xB0D0EA  mov     eax, [esp+1B44h+var_1B0C]   ; target_y
0xB0D0EE  mov     edx, [esi]
0xB0D0F0  push    ecx                         ; target_z
0xB0D0F1  movzx   ecx, word ptr [eax]
0xB0D0F4  mov     eax, [esp+1B48h+var_1B00]   ; target_x
0xB0D0F8  mov     edx, [edx+1C4h]             ; ← vt[0x1C4]
0xB0D0FE  push    ecx                         ; target_y
0xB0D0FF  movzx   ecx, word ptr [eax]
0xB0D102  mov     eax, [esp+1B4Ch+var_1AEC]   ; airbomb_id
0xB0D106  push    ecx                         ; target_x
0xB0D107  mov     ecx, [eax]
0xB0D109  mov     eax, [esp+1B50h+var_1AF8]   ; itemid
0xB0D10D  push    ecx                         ; airbomb_id
0xB0D10E  mov     ecx, [eax]
0xB0D110  mov     eax, [esp+1B54h+var_1AF0]   ; ent_id
0xB0D114  push    ecx                         ; itemid
0xB0D115  movzx   ecx, word ptr [eax]
0xB0D118  push    ecx                         ; ent_id
0xB0D119  mov     ecx, esi
0xB0D11B  call    edx                         ; vt[0x1C4](ent_id, itemid, airbomb_id, target_x, target_y, target_z, stage, fx_opt)
0xB0D11D  add     dword ptr [esi+1C00h], 1
```
