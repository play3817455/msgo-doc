# 汇编证据 —— SC-0x0DA1-lounge-msma_msset_apply_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 case 入口 + 解码缓冲申请（容量 `8`）

```asm
; VA: 0xB5522D .. 0xB5525C
0xB5522D  push    12Eh                     ; ← 本 case 错误码
0xB55232  mov     ecx, esi
0xB55234  call    sub_B41120
0xB55239  test    al, al
0xB5523B  jz      loc_B890FE
0xB55241  mov     ecx, [esi+0Ch]
0xB55244  mov     eax, [ecx]
0xB55246  mov     edx, [eax+78h]
0xB55249  push    8                        ; ← 容量 8 == 线长
0xB5524B  call    edx
0xB5524D  mov     [esp+2C5Ch+var_2C48], eax
0xB55251  mov     eax, [esi+0Ch]
0xB55254  push    eax
0xB55255  lea     ecx, [esp+2C60h+var_29B0]
0xB5525C  call    sub_ABB2F0               ; 初始化线游标 {cur,end}
```

## E2 字段 1：`result`（u32，偏移 0）

```asm
; VA: 0xB55261 .. 0xB5528E
0xB55261  lea     ecx, [esp+2C5Ch+var_2C48]
0xB55265  push    ecx
0xB55266  lea     ecx, [esp+2C60h+var_2C30] ; 槽
0xB55275  call    sub_B41470               ; 缓冲预留 4B（非字段）
0xB5527A  mov     eax, [esp+2C5Ch+var_2C30]
0xB5527E  lea     edx, [esp+2C5Ch+var_2C44] ; &线游标
0xB55282  push    edx
0xB55283  push    eax
0xB55284  call    sub_B02DD0               ; ← 读 u32
0xB55289  add     esp, 8
0xB5528C  test    al, al
0xB5528E  jnz     short loc_B552AC         ; 成功分支
```

## E3 字段 2：`deck_type`（u16，偏移 4）

```asm
; VA: 0xB552AC .. 0xB552CC
0xB552AC  lea     ecx, [esp+2C5Ch+var_2C48]
0xB552B0  push    ecx
0xB552B1  lea     ecx, [esp+2C60h+var_2C34] ; 槽
0xB552B5  call    sub_B413B0               ; 缓冲预留 2B（非字段）
0xB552BA  mov     eax, [esp+2C5Ch+var_2C34]
0xB552BE  lea     edx, [esp+2C5Ch+var_2C44]
0xB552C2  push    edx
0xB552C3  push    eax
0xB552C4  call    sub_B02DF0               ; ← 读 u16
0xB552C9  add     esp, 8
0xB552CC  test    al, al
0xB552CE  jz      short loc_B55290         ; 失败 ⇒ 报错
```

## E4 字段 3：`slot`（u16，偏移 6）

```asm
; VA: 0xB552D0 .. 0xB552F0
0xB552D0  lea     ecx, [esp+2C5Ch+var_2C48]
0xB552D4  push    ecx
0xB552D5  lea     ecx, [esp+2C60h+var_2C38] ; 槽
0xB552D9  call    sub_B413B0               ; 缓冲预留 2B（非字段）
0xB552DE  mov     eax, [esp+2C5Ch+var_2C38]
0xB552E2  lea     edx, [esp+2C5Ch+var_2C44]
0xB552E6  push    edx
0xB552E7  push    eax
0xB552E8  call    sub_B02DF0               ; ← 读 u16
0xB552ED  add     esp, 8
0xB552F0  test    al, al
0xB552F2  jz      short loc_B55290         ; 失败 ⇒ 报错
```

## E5 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB552F4 .. 0xB55300
0xB552F4  mov     ebx, [esp+2C5Ch+var_2C44] ; 读完后的线游标
0xB552F8  cmp     ebx, [esp+2C5Ch+var_2C40] ; vs 报文末尾
0xB552FC  mov     ecx, esi
0xB552FE  jz      short loc_B5531A          ; ← 不等 ⇒ push 12Eh 报错
0xB55300  mov     edx, [esi]
```

## E6 含义取证：块内日志 `result=` / `deck_type=` / `slot=`

```asm
; VA: 0xB5538B .. 0xB553FD
0xB5538B  mov     eax, [esp+2C5Ch+var_2C30]
0xB5538F  mov     ecx, [eax]                ; result
0xB55397  push    offset aResult            ; ← "result="
0xB5539D  call    sub_41D990
0xB553A7  call    sub_B03580                ; 十进制打印器
0xB553B2  mov     edx, [esp+2C64h+var_2C34]
0xB553B6  movzx   eax, word ptr [edx]       ; deck_type
0xB553C2  push    offset aDeckType          ; ← "deck_type="
0xB553D2  call    sub_B032A0                ; u16 十进制打印器
0xB553DD  mov     ecx, [esp+2C64h+var_2C38]
0xB553E1  movzx   edx, word ptr [ecx]       ; slot
0xB553E8  push    offset aSlot              ; ← "slot="
0xB553F8  call    sub_B032A0
```

## E7 去向：`vt[0x308](result, deck_type, slot)`

```asm
; VA: 0xB55430 .. 0xB55453
0xB55430  mov     ecx, [esp+2C5Ch+var_2C38] ; slot 槽
0xB55434  movzx   edx, word ptr [ecx]       ; edx = slot
0xB55437  mov     ecx, [esp+2C5Ch+var_2C34] ; deck_type 槽
0xB5543B  mov     eax, [esi]
0xB5543D  mov     eax, [eax+308h]           ; ← vt[0x308]
0xB55443  push    edx                       ; 实参 3 = slot
0xB55444  movzx   edx, word ptr [ecx]       ; edx = deck_type
0xB55447  mov     ecx, [esp+2C60h+var_2C30] ; result 槽
0xB5544B  push    edx                       ; 实参 2 = deck_type
0xB5544C  mov     edx, [ecx]                ; edx = result
0xB5544E  push    edx                       ; 实参 1 = result
0xB5544F  mov     ecx, esi
0xB55451  call    eax
0xB55453  add     dword ptr [esi+3DF8h], 1   ; 本命令接收计数（64 位）
0xB55461  adc     dword ptr [esi+3DFCh], 0
```
