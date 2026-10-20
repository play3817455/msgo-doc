# 汇编证据 —— SC-0x20F5-entity_msma_fix

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 分发路径：默认分支块调用本函数（证明「不经 switch」）

```asm
; VA: 0xB31240 .. 0xB31270（在 sub_B0CC20 内）
0xB31242  sub     eax, 0FE50h
0xB31247  jz      loc_B314FE
0xB3124D  sub     eax, 6Bh
0xB31250  jz      short loc_B31273
0xB31252  push    ebx          ; ← jumptable 0xB22835 的 default case 块
0xB31253  push    edi
0xB31254  mov     ecx, esi
0xB31256  call    sub_B0C210   ; ← 未识别 opcode 交给它做二级判定
0xB3125B  mov     ecx, [esp+1B3Ch+var_C]   ; 之后直接收尾返回
```

实测（用具体值模拟 `sub_B0CC20` 的比较树）：`0x20F5` ⇒ `DEFJUMP 0xB31252`；
对照组 `0x3CC` ⇒ `BODY 0xB0CD3B`（正常 case）、`0x8D1F` ⇒ 跳转表。

## E2 opcode 读取与复检（证明 opcode = 0x20F5）

```asm
; VA: 0xB0C237 .. 0xB0C265（sub_B0C210 序言）
0xB0C237  mov     edi, ecx
0xB0C239  mov     eax, [esp+58h+arg_0]     ; eax = buf
0xB0C23D  mov     ecx, [esp+58h+arg_4]     ; ecx = len
0xB0C241  lea     ebx, [eax+ecx]           ; ebx = end
0xB0C244  lea     esi, [eax+2]             ; esi = buf+2（负载游标）
0xB0C247  cmp     esi, ebx
0xB0C251  ja      short loc_B0C271         ; len < 2 ⇒ 错误 0x131
0xB0C253  movzx   eax, word ptr [eax]      ; ← opcode 读取，u16（零扩展 ⇒ 无符号）
0xB0C256  cmp     ax, 20F5h                ; ← opcode 判定
0xB0C25C  jz      short loc_B0C286         ; 命中 ⇒ 正式处理
0xB0C25E  mov     edx, [edi]               ; 未命中 ⇒ vt[0x64](0x131) 报错
0xB0C260  mov     eax, [edx+64h]
0xB0C263  push    0
0xB0C265  push    131h
```

## E3 字段 1：内联读 u16（负载 +0）

```asm
; VA: 0xB0C286 .. 0xB0C2D2
0xB0C286  push    5Eh                       ; 本 case 的开关/阈值
0xB0C288  call    sub_B05DA0
0xB0C28D  test    al, al
0xB0C28F  jz      loc_B0C563
0xB0C295  mov     ecx, [edi+0Ch]            ; 取「解码缓冲分配器」虚表
0xB0C298  mov     edx, [ecx]
0xB0C29A  mov     eax, [edx+78h]
0xB0C29D  push    0Bh                       ; ← 缓冲容量 11（旁证，不是线长）
0xB0C29F  call    eax
0xB0C2B0  mov     ecx, ebp                  ; ecx = out（解码缓冲基址）
0xB0C2B2  lea     eax, [esi+2]              ; eax = buf+4
0xB0C2B5  add     ebp, 2
0xB0C2B8  cmp     eax, ebx                  ; ← 边界检查：buf+4 <= end
0xB0C2C6  ja      loc_B0C2FF                ; 越界 ⇒ 错误 0x5E
0xB0C2C8  mov     dx, [esi]                 ; ← 读 u16 @ buf+2
0xB0C2CB  mov     [ecx], dx                 ; 写到 out+0
```

## E4 字段 2..5：经 `sub_B02DF0` 读 u16（负载 +2/+4/+6/+8）

`sub_B02DF0(dst, &cursor)` 本体（读 **u16**，带边界检查，游标 +2）：

```asm
; VA: 0xB02DF0 .. 0xB02E10
0xB02DF0  mov     eax, [esp+arg_4]          ; cursor 结构 { cur@+0, end@+4 }
0xB02DF4  mov     ecx, [eax]
0xB02DF6  lea     edx, [ecx+2]
0xB02DF9  cmp     edx, [eax+4]
0xB02DFC  jbe     short loc_B02E01
0xB02DFE  xor     al, al                    ; 越界 ⇒ 返回 0
0xB02E00  retn
0xB02E01  mov     cx, [ecx]                 ; ← 读 u16（word）
0xB02E04  mov     edx, [esp+arg_0]
0xB02E08  mov     [edx], cx                 ; 写入 dst
0xB02E0B  add     dword ptr [eax], 2        ; ← 游标 +2 ⇒ 宽度 2
0xB02E0E  mov     al, 1
0xB02E10  retn
```

四处调用点：

```asm
; VA: 0xB0C2DE .. 0xB0C2E1（→ out+2）
0xB0C2D2  mov     [esp+58h+var_30], eax       ; var_30 = buf+4（游标）
0xB0C2D6  mov     eax, ebp                    ; eax = out+2
0xB0C2D8  push    ecx                         ; arg_4 = &cursor
0xB0C2D9  push    eax                         ; arg_0 = dst
0xB0C2DE  add     ebp, 2                      ; ebp → out+4
0xB0C2E1  call    sub_B02DF0

; VA: 0xB0C313 .. 0xB0C320（→ out+4）
; VA: 0xB0C32E .. 0xB0C33B（→ out+6）
; VA: 0xB0C349 .. 0xB0C356（→ out+8）
```
（`0xB0C319 mov [esp+60h+var_3C], eax`、`0xB0C334 mov [esp+60h+var_40], eax`、
`0xB0C34F mov [esp+60h+var_44], eax` 依次记下 out+4 / out+6 / out+8。）

## E5 字段 6：经 `sub_B06230` 读 u8（负载 +10）

`sub_B06230(dst, &cursor)` 本体（读 **u8**）：

```asm
; VA: 0xB06230 .. 0xB0624E
0xB06230  mov     eax, [esp+arg_4]
0xB06234  mov     ecx, [eax]
0xB06236  lea     edx, [ecx+1]
0xB06239  cmp     edx, [eax+4]
0xB0623C  jbe     short loc_B06241
0xB0623E  xor     al, al
0xB06240  retn
0xB06241  mov     cl, [ecx]                 ; ← 读 u8（byte）
0xB06243  mov     edx, [esp+arg_0]
0xB06247  mov     [edx], cl
0xB06249  add     dword ptr [eax], 1        ; ← 游标 +1 ⇒ 宽度 1
0xB0624C  mov     al, 1
0xB0624E  retn
```

调用点：

```asm
; VA: 0xB0C362 .. 0xB0C368（→ out+10）
0xB0C362  lea     ecx, [esp+58h+var_30]
0xB0C366  push    ecx
0xB0C367  push    ebp                         ; ebp = out+10
0xB0C368  call    sub_B06230
```

## E6 长度闭合（证明负载恰好 11 字节）

```asm
; VA: 0xB0C378 .. 0xB0C380
0xB0C378  mov     ebx, [esp+58h+var_30]    ; 读完后的游标
0xB0C37C  cmp     ebx, [esp+58h+var_2C]    ; vs 报文末尾（0xB0C24D 处 ebx=end 存入）
0xB0C380  jnz     loc_B0C2ED               ; ← 不等 ⇒ 错误 0x5E
```

## E7 去向：6 个值一次性交 `vt[0x68]`

```asm
; VA: 0xB0C50E .. 0xB0C54B
0xB0C50E  movzx   eax, byte ptr [ebp+0]    ; ebp = out+10 ⇒ u8（第 6 个实参）
0xB0C519  movzx   eax, word ptr [ecx]      ; var_44 = out+8  ⇒ u16
0xB0C524  movzx   eax, word ptr [ecx]      ; var_40 = out+6  ⇒ u16
0xB0C52C  movzx   eax, word ptr [ecx]      ; var_3C = out+4  ⇒ u16
0xB0C534  movzx   eax, word ptr [ecx]      ; var_38 = out+2  ⇒ u16
0xB0C53B  movzx   eax, word ptr [ecx]      ; var_34 = out+0  ⇒ u16
0xB0C540  mov     ecx, edi
0xB0C542  call    edx                        ; vt[0x68](out+0, out+2, out+4, out+6, out+8, out+10)
0xB0C544  add     dword ptr [edi+1480h], 1   ; 64 位接收计数自增
0xB0C54B  adc     dword ptr [edi+1484h], 0
```
