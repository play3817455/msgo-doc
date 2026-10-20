# 汇编证据 —— SC-0x0120-battle-entity_msma_show

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 case 入口 + 解码缓冲申请（容量 2）

```asm
; VA: 0xB0D320 .. 0xB0D34C
0xB0D320  push    5Dh                      ; ← 本 case 开关/错误码
0xB0D322  mov     ecx, esi
0xB0D324  call    sub_B05DA0               ; case 级开关检查
0xB0D329  test    al, al
0xB0D32B  jz      loc_B317C7
0xB0D331  mov     ecx, [esi+0Ch]
0xB0D334  mov     eax, [ecx]
0xB0D336  mov     edx, [eax+78h]
0xB0D339  push    2                        ; ← 容量 2（旁证，不是线长）
0xB0D33B  call    edx
0xB0D33D  mov     [esp+1B3Ch+var_1B14], eax
0xB0D341  mov     eax, [esi+0Ch]
0xB0D344  push    eax
0xB0D345  lea     ecx, [esp+1B40h+var_1804]
0xB0D34C  call    sub_ABB2F0               ; 初始化 {cur,end}（非 IO）
```

## E2 字段 1：预留 u16 槽（非字段）+ `sub_B02DF0` 读 u16（负载 +0）

```asm
; VA: 0xB0D351 .. 0xB0D379
0xB0D351  lea     ecx, [esp+1B3Ch+var_1B14]
0xB0D355  push    ecx
0xB0D356  lea     ecx, [esp+1B40h+var_1B2C]   ; 槽
0xB0D35A  mov     [esp+1B40h+var_4], 7Dh
0xB0D365  call    sub_B413B0               ; 预留 2 字节槽（非字段）
0xB0D36A  mov     eax, [esp+1B3Ch+var_1B2C]
0xB0D36E  lea     edx, [esp+1B3Ch+var_1B28]   ; 游标结构
0xB0D372  push    edx
0xB0D373  push    eax
0xB0D374  call    sub_B02DF0               ; ← 读 u16
0xB0D379  add     esp, 8
```

预留函数本体 + `sub_B02DF0` 本体（读 **u16**，游标 +2）：

```asm
; VA: 0xB413B0 .. 0xB413BD
0xB413B0  mov     eax, ecx
0xB413B2  mov     ecx, [esp+arg_0]
0xB413B6  mov     edx, [ecx]
0xB413B8  mov     [eax], edx
0xB413BA  add     dword ptr [ecx], 2        ; ← 槽宽 2
0xB413BD  retn    4

; VA: 0xB02DF0 .. 0xB02E10
0xB02DF0  mov     eax, [esp+arg_4]
0xB02DF4  mov     ecx, [eax]
0xB02DF6  lea     edx, [ecx+2]
0xB02DF9  cmp     edx, [eax+4]
0xB02DFC  jbe     short loc_B02E01
0xB02DFE  xor     al, al
0xB02E00  retn
0xB02E01  mov     cx, [ecx]                ; ← 读 u16（word）
0xB02E04  mov     edx, [esp+arg_0]
0xB02E08  mov     [edx], cx
0xB02E0B  add     dword ptr [eax], 2        ; ← 游标 +2 ⇒ 宽度 2
0xB02E0E  mov     al, 1
0xB02E10  retn
```

## E3 长度闭合（负载恰好 2 字节）

```asm
; VA: 0xB0D399 .. 0xB0D3A1
0xB0D399  mov     ebx, [esp+1B3Ch+var_1B28]   ; 读完后的游标
0xB0D39D  cmp     ebx, [esp+1B3Ch+var_1B24]   ; vs 报文末尾
0xB0D3A1  jnz     short loc_B0D382            ; ← 不等则 push 5Dh 报错
```

## E4 含义取证：块内日志格式串

```asm
; VA: 0xB0D411 .. 0xB0D41F
0xB0D411  mov     eax, [esp+1B3Ch+var_1B2C]   ; 字段槽
0xB0D415  movzx   ecx, word ptr [eax]           ; ← 按 u16 取值
0xB0D418  push    ecx
0xB0D419  push    offset aEntId               ; ← "ent_id="
0xB0D41E  push    edi
0xB0D41F  call    sub_41D990                  ; sprintf
```

## E5 去向：`vt[0x174](u16 ent_id)`

```asm
; VA: 0xB0D461 .. 0xB0D475
0xB0D461  mov     eax, [esp+1B3Ch+var_1B2C]   ; 字段槽
0xB0D465  movzx   ecx, word ptr [eax]
0xB0D468  mov     edx, [esi]
0xB0D46A  mov     edx, [edx+174h]            ; ← vt[0x174]
0xB0D470  push    ecx
0xB0D471  mov     ecx, esi
0xB0D473  call    edx
0xB0D475  add     dword ptr [esi+1450h], 1   ; 接收计数自增
```
