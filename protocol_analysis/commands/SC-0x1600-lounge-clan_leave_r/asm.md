# 汇编证据 —— SC-0x1600-lounge-clan_leave_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 case 入口 + 解码缓冲申请（容量 `0xD`）

```asm
; VA: 0xB55E21 .. 0xB55E49
0xB55E21  call    sub_B41120               ; case 起始守卫（不读线）
0xB55E26  test    al, al
0xB55E28  jz      loc_B890FE
0xB55E2E  mov     ecx, [esi+0Ch]
0xB55E31  mov     edx, [ecx]
0xB55E33  mov     eax, [edx+78h]
0xB55E36  push    0Dh                      ; ← 容量 13（= 4+4+1+4）
0xB55E38  call    eax
0xB55E3A  mov     ecx, [esi+0Ch]
0xB55E3D  push    ecx
0xB55E3E  lea     ecx, [esp+2C60h+var_2ABC]
0xB55E45  mov     [esp+2C60h+var_2C24], eax ; 解码缓冲基址
0xB55E49  call    sub_ABB2F0               ; 初始化线游标
```

## E2 字段 1/2：`result`（u32@0）、`clan_id`（u32@4）

```asm
; VA: 0xB55E4E .. 0xB55E94
0xB55E62  call    sub_B41470               ; u32 槽预留（非字段）
0xB55E71  call    sub_B02DD0               ; ← 读 u32（4 字节）→ result
0xB55E79  test    al, al
0xB55E7B  jnz     short loc_B55E99
0xB55E84  push    1B1h                     ; ← 错误码
0xB55E99  lea     ecx, [esp+2C5Ch+var_2C24]
0xB55EA2  call    sub_B41470               ; u32 槽预留（非字段）
0xB55EB1  call    sub_B02DD0               ; ← 读 u32（4 字节）→ clan_id
0xB55EB9  test    al, al
0xB55EBB  jz      short loc_B55E7D
```

## E3 字段 3/4：`clan_kind`（u8@8）、`deckcost`（u32@9）+ 长度闭合

```asm
; VA: 0xB55EBD .. 0xB55F2A
0xB55EC6  call    sub_B05E30               ; u8 槽预留（非字段）
0xB55ED5  call    sub_B06230               ; ← 读 u8（1 字节）→ clan_kind
0xB55EDD  test    al, al
0xB55EDF  jz      short loc_B55E7D
0xB55EEA  call    sub_B41470               ; u32 槽预留（非字段）
0xB55EF9  call    sub_B02DD0               ; ← 读 u32（4 字节）→ deckcost
0xB55F01  test    al, al
0xB55F03  jz      loc_B55E7D
0xB55F09  mov     ebx, [esp+2C5Ch+var_2C44] ; 读完后的线游标
0xB55F0D  cmp     ebx, [esp+2C5Ch+var_2C40] ; vs 报文末尾
0xB55F13  jz      short loc_B55F2F         ; ← 不等 ⇒ push 1 / push 1B1h 报错
```

## E4 含义取证：块内日志 `result=` / `clan_id=` / `clan_kind=` / `deckcost=`

```asm
; VA: 0xB55FA0 .. 0xB56035
0xB55FAC  push    offset aResult            ; ← "result="
0xB55FD6  push    offset aClanId            ; ← "clan_id="
0xB55FEB  push    eax
0xB55FFE  push    offset aClanKind          ; ← "clan_kind="
0xB5600D  call    sub_B0C1F0               ; 1 字节打印器（仅打印用 movsx）
0xB56025  push    offset aDeckcost          ; ← "deckcost="
0xB56035  call    sub_B03580               ; u32 打印器
```

## E5 去向：`vt[0x424](result, clan_id, clan_kind, deckcost)`

```asm
; VA: 0xB5606D .. 0xB560A4
0xB5606D  mov     eax, [esp+2C5Ch+var_2C48] ; deckcost 槽
0xB56071  mov     ecx, [eax]
0xB56073  mov     eax, [esp+2C5Ch+var_2C38] ; clan_kind 槽
0xB56077  mov     edx, [esi]
0xB56079  mov     edx, [edx+424h]           ; ← vt[0x424]
0xB5607F  push    ecx                       ; 实参 4 = deckcost
0xB56080  movzx   ecx, byte ptr [eax]       ; clan_kind（零扩展 ⇒ 无符号）
0xB56083  push    ecx                       ; 实参 3 = clan_kind
0xB56088  mov     ecx, [eax]                ; clan_id 槽 → 值
0xB5608A  push    ecx                       ; 实参 2 = clan_id
0xB5608E  mov     ecx, [eax]                ; result 槽 → 值
0xB56091  push    ecx                       ; 实参 1 = result
0xB56092  mov     ecx, esi
0xB56094  call    edx
0xB56096  add     dword ptr [esi+5688h], 1  ; 本命令接收计数（64 位）
```
