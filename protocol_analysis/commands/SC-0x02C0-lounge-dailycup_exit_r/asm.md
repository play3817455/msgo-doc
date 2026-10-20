# 汇编证据 —— SC-0x02C0-lounge-dailycup_exit_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 case 入口 + 解码缓冲申请（容量 4）

```asm
; VA: 0xB52213 .. 0xB5223B
0xB52213  call    sub_B41120               ; case 级开关检查（前置 push 23Bh = 开关号）
0xB52218  test    al, al
0xB5221A  jz      loc_B890FE
0xB52220  mov     ecx, [esi+0Ch]
0xB52223  mov     eax, [ecx]
0xB52225  mov     edx, [eax+78h]
0xB52228  push    4                        ; ← 容量 4（旁证，不是线长）
0xB5222A  call    edx
0xB5222C  mov     [esp+2C5Ch+var_2C3C], eax
0xB52230  mov     eax, [esi+0Ch]
0xB52233  push    eax
0xB52234  lea     ecx, [esp+2C60h+var_271C]
0xB5223B  call    sub_ABB2F0
```

## E2 字段 1：预留 u32 槽（非字段）+ `sub_B02DD0` 读 u32（负载 +0）

```asm
; VA: 0xB52240 .. 0xB52268
0xB52240  lea     ecx, [esp+2C5Ch+var_2C3C]
0xB52244  push    ecx
0xB52245  lea     ecx, [esp+2C60h+var_2C04]   ; 槽
0xB52249  mov     [esp+2C60h+var_4], 27Ch
0xB52254  call    sub_B41470               ; 预留 4 字节槽（非字段）
0xB52259  mov     eax, [esp+2C5Ch+var_2C04]
0xB5225D  lea     edx, [esp+2C5Ch+var_2C44]
0xB52261  push    edx
0xB52262  push    eax
0xB52263  call    sub_B02DD0               ; ← 读 u32
0xB52268  add     esp, 8
```

预留函数本体：

```asm
; VA: 0xB41470 .. 0xB4147D
0xB41470  mov     eax, ecx
0xB41472  mov     ecx, [esp+arg_0]
0xB41476  mov     edx, [ecx]
0xB41478  mov     [eax], edx
0xB4147A  add     dword ptr [ecx], 4
0xB4147D  retn    4
```

`sub_B02DD0` 本体（读 **u32**，游标 +4）：

```asm
; VA: 0xB02DD0 .. 0xB02DEE
0xB02DD0  mov     eax, [esp+arg_4]
0xB02DD4  mov     ecx, [eax]
0xB02DD6  lea     edx, [ecx+4]
0xB02DD9  cmp     edx, [eax+4]
0xB02DDC  jbe     short loc_B02DE1
0xB02DDE  xor     al, al
0xB02DE0  retn
0xB02DE1  mov     ecx, [ecx]                ; ← 读 u32
0xB02DE3  mov     edx, [esp+arg_0]
0xB02DE7  mov     [edx], ecx
0xB02DE9  add     dword ptr [eax], 4        ; ← 游标 +4 ⇒ 宽度 4
0xB02DEC  mov     al, 1
0xB02DEE  retn
```

## E3 长度闭合（负载恰好 4 字节）

```asm
; VA: 0xB5228B .. 0xB52293
0xB5228B  mov     ebx, [esp+2C5Ch+var_2C44]   ; 读完后的游标
0xB5228F  cmp     ebx, [esp+2C5Ch+var_2C40]   ; vs 报文末尾
0xB52293  jnz     short loc_B52271            ; ← 不等则 push 23Bh 报错
```

## E4 含义取证：块内日志格式串

```asm
; VA: 0xB52306 .. 0xB52313
0xB52306  mov     eax, [esp+2C5Ch+var_2C04]   ; 字段槽
0xB5230A  mov     ecx, [eax]
0xB5230C  push    ecx
0xB5230D  push    offset aResult             ; ← "result="
0xB52312  push    edi
0xB52313  call    sub_41D990                  ; sprintf
```

## E5 去向：`vt[0x568](u32 result)`

```asm
; VA: 0xB52355 .. 0xB52368
0xB52355  mov     eax, [esp+2C5Ch+var_2C04]   ; 字段槽
0xB52359  mov     ecx, [eax]
0xB5235B  mov     edx, [esi]
0xB5235D  mov     edx, [edx+568h]            ; ← vt[0x568]
0xB52363  push    ecx
0xB52364  mov     ecx, esi
0xB52366  call    edx
0xB52368  add     dword ptr [esi+7068h], 1   ; 接收计数自增
```
