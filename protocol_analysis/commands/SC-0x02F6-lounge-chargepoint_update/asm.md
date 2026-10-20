# 汇编证据 —— SC-0x02F6-lounge-chargepoint_update

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 case 入口 + 解码缓冲申请（容量 4）

```asm
; VA: 0xB53112 .. 0xB5313E
0xB53112  push    40h                      ; ← 本 case 开关/错误码
0xB53114  mov     ecx, esi
0xB53116  call    sub_B41120
0xB5311B  test    al, al
0xB5311D  jz      loc_B890FE
0xB53123  mov     ecx, [esi+0Ch]
0xB53126  mov     eax, [ecx]
0xB53128  mov     edx, [eax+78h]
0xB5312B  push    4                        ; ← 容量 4（旁证，不是线长）
0xB5312D  call    edx
0xB5312F  mov     [esp+2C5Ch+var_2C3C], eax
0xB53133  mov     eax, [esi+0Ch]
0xB53136  push    eax
0xB53137  lea     ecx, [esp+2C60h+var_2690]
0xB5313E  call    sub_ABB2F0
```

## E2 字段 1：预留 u32 槽（非字段）+ `sub_B02DD0` 读 u32（负载 +0）

```asm
; VA: 0xB53143 .. 0xB5316B
0xB53143  lea     ecx, [esp+2C5Ch+var_2C3C]
0xB53147  push    ecx
0xB53148  lea     ecx, [esp+2C60h+var_2C48]   ; 槽
0xB5314C  mov     [esp+2C60h+var_4], 48h
0xB53157  call    sub_B41470               ; 预留 4 字节槽（非字段）
0xB5315C  mov     eax, [esp+2C5Ch+var_2C48]
0xB53160  lea     edx, [esp+2C5Ch+var_2C44]
0xB53164  push    edx
0xB53165  push    eax
0xB53166  call    sub_B02DD0               ; ← 读 u32
0xB5316B  add     esp, 8
```

预留函数本体 + `sub_B02DD0` 本体（读 **u32**，游标 +4）：

```asm
; VA: 0xB41470 .. 0xB4147D
0xB41470  mov     eax, ecx
0xB41472  mov     ecx, [esp+arg_0]
0xB41476  mov     edx, [ecx]
0xB41478  mov     [eax], edx
0xB4147A  add     dword ptr [ecx], 4
0xB4147D  retn    4

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
; VA: 0xB5318B .. 0xB53193
0xB5318B  mov     ebx, [esp+2C5Ch+var_2C44]   ; 读完后的游标
0xB5318F  cmp     ebx, [esp+2C5Ch+var_2C40]   ; vs 报文末尾
0xB53193  jnz     short loc_B53174            ; ← 不等则 push 40h 报错
```

## E4 含义取证：块内日志格式串

```asm
; VA: 0xB53203 .. 0xB53210
0xB53203  mov     eax, [esp+2C5Ch+var_2C48]   ; 字段槽
0xB53207  mov     ecx, [eax]
0xB53209  push    ecx
0xB5320A  push    offset aChargepoint        ; ← "chargepoint="
0xB5320F  push    edi
0xB53210  call    sub_41D990                  ; sprintf
```

## E5 去向：`vt[0xF8](u32 chargepoint)`

```asm
; VA: 0xB53252 .. 0xB53265
0xB53252  mov     eax, [esp+2C5Ch+var_2C48]   ; 字段槽
0xB53256  mov     ecx, [eax]
0xB53258  mov     edx, [esi]
0xB5325A  mov     edx, [edx+0F8h]            ; ← vt[0xF8]
0xB53260  push    ecx
0xB53261  mov     ecx, esi
0xB53263  call    edx
0xB53265  add     dword ptr [esi+1158h], 1   ; 接收计数自增
```
