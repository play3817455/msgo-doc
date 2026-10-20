# 汇编证据 —— SC-0x07E8-lounge-party_info_edit_notice

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 case 入口 + 解码缓冲申请（容量 `0x42` = 66）

```asm
; VA: 0xB5405D .. 0xB5408C
0xB5405D  push    0BFh                     ; ← 本 case 错误码
0xB54062  mov     ecx, esi
0xB54064  call    sub_B41120
0xB54069  test    al, al
0xB5406B  jz      loc_B890FE
0xB54071  mov     ecx, [esi+0Ch]
0xB54074  mov     eax, [ecx]
0xB54076  mov     edx, [eax+78h]           ; vt[0x78] = 申请解码缓冲
0xB54079  push    42h                      ; ← 容量 66 = 1 + 0x3D + 4
0xB5407B  call    edx
0xB5407D  mov     [esp+2C5Ch+var_2C24], eax ; 缓冲基址（后续同时充当缓冲游标）
0xB54081  mov     eax, [esi+0Ch]
0xB54084  push    eax
0xB54085  lea     ecx, [esp+2C60h+var_29D8]
0xB5408C  call    sub_ABB2F0               ; 初始化 {cur,end} 读游标
```

## E2 字段 1：`is_recruiting`（u8）

```asm
; VA: 0xB5409A .. 0xB540B9
0xB540A5  call    sub_B05E30               ; 缓冲预留 1B（非字段）
0xB540B4  call    sub_B06230               ; ← 读 u8（槽 var_2C38）
```

## E3 字段 2：`comment`（变长 NUL 串，槽位预算 `0x3D` = 61）

```asm
; VA: 0xB540DC .. 0xB540FA
0xB540DC  mov     eax, [esp+2C5Ch+var_2C24]   ; 缓冲游标 == 当前串槽
0xB540E0  mov     ecx, eax
0xB540E2  push    3Dh                         ; ← 槽位预算（上限 61），不是串长
0xB540E4  lea     edx, [esp+2C60h+var_2C44]   ; 线游标
0xB540E8  push    edx
0xB540E9  add     eax, 3Dh                    ; ← 下一槽 = 当前 + 61
0xB540EC  push    ecx                         ; dst = 串槽
0xB540ED  mov     [esp+2C68h+var_2C3C], ecx   ; 串指针（后续作为实参）
0xB540F1  mov     [esp+2C68h+var_2C24], eax   ; 推进缓冲游标
0xB540F5  call    sub_B02BA0                  ; ← 读 NUL 结尾串：消费 = 串长 L + 1
0xB540FA  add     esp, 0Ch
```

## E4 字段 3：`party_type`（u32）

```asm
; VA: 0xB5411D .. 0xB5413A
0xB5411D  lea     eax, [esp+2C5Ch+var_2C24]   ; &缓冲游标（此时 = 原基址 + 0x3D）
0xB54121  push    eax
0xB54122  lea     ecx, [esp+2C60h+var_2C48]   ; &槽
0xB54126  call    sub_B41470                  ; 预留 4B（非字段）
0xB5412B  mov     edx, [esp+2C5Ch+var_2C48]
0xB5412F  lea     ecx, [esp+2C5Ch+var_2C44]
0xB54133  push    ecx
0xB54134  push    edx
0xB54135  call    sub_B02DD0                  ; ← 读 u32
```

## E5 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB54141 .. 0xB5414B
0xB54141  mov     ebx, [esp+2C5Ch+var_2C44]   ; 读完后的游标
0xB54145  cmp     ebx, [esp+2C5Ch+var_2C40]   ; vs 报文末尾
0xB5414B  jz      short loc_B54167            ; ← 不等 ⇒ push 0BFh 报错
```

## E6 含义取证：块内日志格式串

```asm
; VA: 0xB541D8 .. 0xB54251
0xB541DC  push    offset word_F641DC         ; ","
0xB541E2  push    offset aIsRecruiting       ; ← "is_recruiting="
0xB541F1  call    sub_B0C1F0                ; 布尔/单字节打印器
0xB5420B  push    offset asc_EDAD54          ; "\""
0xB54211  push    offset aComment_0          ; ← "comment=\""
0xB54241  push    offset aPartyType          ; ← "party_type="
0xB54251  call    sub_B03580                ; 十进制打印器
```

## E7 去向：`vt[0x218]`（3 个实参）

```asm
; VA: 0xB54289 .. 0xB542B7
0xB54289  mov     ecx, [esp+2C5Ch+var_2C48]   ; party_type 槽
0xB5428D  mov     edx, [ecx]                  ; party_type
0xB5428F  mov     ecx, [esp+2C5Ch+var_2C3C]   ; comment 串指针
0xB54293  mov     eax, [esi]
0xB54295  push    edx                         ; 实参 3 = party_type
0xB54296  mov     edx, [esp+2C60h+var_2C38]   ; is_recruiting 槽
0xB5429A  push    ecx                         ; 实参 2 = comment
0xB5429B  movzx   ecx, byte ptr [edx]
0xB5429E  mov     edx, [eax+218h]             ; ← vt[0x218]
0xB542A4  push    ecx                         ; 实参 1 = is_recruiting（零扩展）
0xB542A5  mov     ecx, esi
0xB542A7  call    edx
0xB542A9  add     dword ptr [esi+2928h], 1    ; 本命令接收计数（64 位）
0xB542B7  adc     dword ptr [esi+292Ch], 0
```
