# 汇编证据 —— SC-0x00C7-msma_trialms_back_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 case 体入口 + 解码缓冲申请（容量 12）

```asm
; VA: 0xB51C95 .. 0xB51CB5
0xB51C95  push    13Eh                     ; 本 case 的开关/错误码
0xB51C9A  mov     ecx, esi
0xB51C9C  call    sub_B41120               ; case 级开关检查（按 case 号查 [edi+538h+idx*30h] 状态）
0xB51CA1  test    al, al
0xB51CA3  jz      loc_B890FE               ; 未通过 ⇒ 统一收尾
0xB51CA9  mov     ecx, [esi+0Ch]           ; 解码缓冲分配器虚表
0xB51CAC  mov     eax, [ecx]
0xB51CAE  mov     edx, [eax+78h]
0xB51CB1  push    0Ch                      ; ← 容量 12（旁证，不是线长）
0xB51CB3  call    edx
```

## E2 字段 1：预留 u32 槽（非字段）+ `sub_B02DD0` 读 u32（负载 +0）

```asm
; VA: 0xB51CC9 .. 0xB51CF1
0xB51CC9  lea     ecx, [esp+2C5Ch+var_2C3C]   ; 游标结构 {cur,end}
0xB51CCD  push    ecx
0xB51CCE  lea     ecx, [esp+2C60h+var_2C04]   ; dst = 解码缓冲槽
0xB51CD2  mov     [esp+2C60h+var_4], 15Dh
0xB51CDD  call    sub_B41470               ; 预留 4 字节槽（非字段）
0xB51CE2  mov     eax, [esp+2C5Ch+var_2C04]
0xB51CE6  lea     edx, [esp+2C5Ch+var_2C44]
0xB51CEA  push    edx
0xB51CEB  push    eax
0xB51CEC  call    sub_B02DD0               ; ← 读 u32（带边界检查）
0xB51CF1  add     esp, 8
```

预留函数本体（只推进「解码缓冲」指针，不读 wire）：

```asm
; VA: 0xB41470 .. 0xB4147C
0xB41470  mov     eax, ecx
0xB41472  mov     ecx, [esp+arg_0]
0xB41476  mov     edx, [ecx]
0xB41478  mov     [eax], edx
0xB4147A  add     dword ptr [ecx], 4        ; ← 槽宽 4
0xB4147D  retn    4
```

`sub_B02DD0` 本体（读 **u32**，游标 +4）：

```asm
; VA: 0xB02DD0 .. 0xB02DEE
0xB02DD0  mov     eax, [esp+arg_4]          ; cursor 结构 {cur@+0, end@+4}
0xB02DD4  mov     ecx, [eax]
0xB02DD6  lea     edx, [ecx+4]
0xB02DD9  cmp     edx, [eax+4]
0xB02DDC  jbe     short loc_B02DE1
0xB02DDE  xor     al, al                    ; 越界 ⇒ 返回 0
0xB02DE0  retn
0xB02DE1  mov     ecx, [ecx]                ; ← 读 u32（dword）
0xB02DE3  mov     edx, [esp+arg_0]
0xB02DE7  mov     [edx], ecx
0xB02DE9  add     dword ptr [eax], 4        ; ← 游标 +4 ⇒ 宽度 4
0xB02DEC  mov     al, 1
0xB02DEE  retn
```

## E3 字段 2：预留 u64 槽（非字段）+ `sub_B06200` 读 u64（负载 +4）

```asm
; VA: 0xB51D14 .. 0xB51D31
0xB51D14  lea     ecx, [esp+2C5Ch+var_2C3C]
0xB51D18  push    ecx
0xB51D19  lea     ecx, [esp+2C60h+var_2C20]
0xB51D1D  call    sub_B41A10               ; 预留 8 字节槽（非字段）
0xB51D22  mov     ebx, [esp+2C5Ch+var_2C20]
0xB51D26  lea     edx, [esp+2C5Ch+var_2C44]
0xB51D2A  push    edx
0xB51D2B  push    ebx
0xB51D2C  call    sub_B06200               ; ← 读 u64（带边界检查）
0xB51D31  add     esp, 8
```

预留函数本体 + `sub_B06200` 本体（读 **u64**：两次 4 字节搬运 + 游标 +8）：

```asm
; VA: 0xB41A10 .. 0xB41A1D
0xB41A10  mov     eax, ecx
0xB41A12  mov     ecx, [esp+arg_0]
0xB41A16  mov     edx, [ecx]
0xB41A18  mov     [eax], edx
0xB41A1A  add     dword ptr [ecx], 8        ; ← 槽宽 8
0xB41A1D  retn    4

; VA: 0xB06200 .. 0xB06226
0xB06200  mov     eax, [esp+arg_4]
0xB06204  mov     ecx, [eax]
0xB06206  lea     edx, [ecx+8]              ; ← 需要 8 字节可用
0xB06209  cmp     edx, [eax+4]
0xB0620C  jbe     short loc_B06211
0xB0620E  xor     al, al
0xB06210  retn
0xB06211  mov     edx, [esp+arg_0]
0xB06215  push    esi
0xB06216  mov     esi, [ecx]               ; 低 4 字节
0xB06218  mov     [edx], esi
0xB0621A  mov     ecx, [ecx+4]             ; 高 4 字节
0xB0621D  mov     [edx+4], ecx
0xB06220  add     dword ptr [eax], 8        ; ← 游标 +8 ⇒ 宽度 8
0xB06223  mov     al, 1
0xB06225  pop     esi
0xB06226  retn
```

## E4 长度闭合（负载恰好 12 字节：4 + 8）

```asm
; VA: 0xB51D54 .. 0xB51D5C
0xB51D54  mov     eax, [esp+2C5Ch+var_2C44]   ; 读完后的游标
0xB51D58  cmp     eax, [esp+2C5Ch+var_2C40]   ; vs 报文末尾
0xB51D5C  jz      short loc_B51D78            ; ← 不等则 push 13Eh 报错
```

## E5 含义取证：块内日志格式串（`result=` / `uniqid_ms=`）

```asm
; VA: 0xB51DE9 .. 0xB51E2A
0xB51DE9  mov     eax, [esp+2C5Ch+var_2C04]   ; 字段 1 槽
0xB51DED  mov     ecx, [eax]
0xB51DEF  push    offset word_F641DC          ; ","
0xB51DF4  push    ecx
0xB51DF5  push    offset aResult             ; ← "result="
0xB51DFA  push    edi
0xB51DFB  call    sub_41D990                 ; sprintf
...
0xB51E10  mov     edx, [ebx+4]               ; 字段 2 槽高 4 字节
0xB51E13  mov     eax, [ebx]                 ; 字段 2 槽低 4 字节
0xB51E18  push    edx
0xB51E19  push    eax
0xB51E1A  push    offset aUniqidMs           ; ← "uniqid_ms="
0xB51E1F  push    edi
0xB51E20  call    sub_41D990
```

（`ebx` = `var_2C20`，即 E3 中 `sub_B41A10` 返回的 u64 槽地址，`0xB51D22`。）

## E6 去向：2 个值一次性交 `vt[0x328]`

```asm
; VA: 0xB51E66 .. 0xB51E87
0xB51E66  mov     eax, [ebx+4]               ; u64 高
0xB51E69  mov     ecx, [ebx]                 ; u64 低
0xB51E6B  mov     edx, [esi]
0xB51E6D  mov     edx, [edx+328h]            ; ← vt[0x328]
0xB51E73  push    eax
0xB51E74  mov     eax, [esp+2C60h+var_2C04]  ; 字段 1 槽
0xB51E78  push    ecx
0xB51E79  mov     ecx, [eax]
0xB51E7B  push    ecx
0xB51E7C  mov     ecx, esi
0xB51E7E  call    edx                        ; vt[0x328](result, uniqid_ms)
0xB51E80  add     dword ptr [esi+40F8h], 1   ; 接收计数自增
0xB51E87  lea     ecx, [esp+2C5Ch+var_2798]
0xB51E8E  adc     dword ptr [esi+40FCh], 0
```
