# 汇编证据 —— SC-0x0249-lounge-clan_shop_buying_history_update

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 case 入口 + 解码缓冲申请（容量 8：按 u64 槽预留）

```asm
; VA: 0xB52382 .. 0xB523B1
0xB52382  push    1EDh                     ; ← 本 case 开关/错误码
0xB52387  mov     ecx, esi
0xB52389  call    sub_B41120
0xB5238E  test    al, al
0xB52390  jz      loc_B890FE
0xB52396  mov     ecx, [esi+0Ch]
0xB52399  mov     eax, [ecx]
0xB5239B  mov     edx, [eax+78h]
0xB5239E  push    8                        ; ← 容量 8（槽位富余，见 E3；不是线长）
0xB523A0  call    edx
0xB523A2  mov     [esp+2C5Ch+var_2C3C], eax
0xB523A6  mov     eax, [esi+0Ch]
0xB523A9  push    eax
0xB523AA  lea     ecx, [esp+2C60h+var_2724]
0xB523B1  call    sub_ABB2F0
```

## E2 预留 8 字节槽（非字段）+ `sub_B46AB0` 一次读入 u32 + u16

```asm
; VA: 0xB523B6 .. 0xB523DE
0xB523B6  lea     ecx, [esp+2C5Ch+var_2C3C]
0xB523BA  push    ecx
0xB523BB  lea     ecx, [esp+2C60h+var_2C04]   ; 槽地址
0xB523BF  mov     [esp+2C60h+var_4], 21Bh
0xB523CA  call    sub_B41A10               ; 预留 8 字节槽（非字段）
0xB523CF  mov     eax, [esp+2C5Ch+var_2C04]
0xB523D3  lea     edx, [esp+2C5Ch+var_2C44]   ; 游标结构
0xB523D7  push    edx
0xB523D8  push    eax
0xB523D9  call    sub_B46AB0               ; ← 一次读 u32 + u16（共 6 字节）
0xB523DE  add     esp, 8
```

预留函数本体：

```asm
; VA: 0xB41A10 .. 0xB41A1D
0xB41A10  mov     eax, ecx
0xB41A12  mov     ecx, [esp+arg_0]
0xB41A16  mov     edx, [ecx]
0xB41A18  mov     [eax], edx
0xB41A1A  add     dword ptr [ecx], 8        ; ← 槽宽 8
0xB41A1D  retn    4
```

`sub_B46AB0` 本体（**线长 = 4 + 2 = 6**）：

```asm
; VA: 0xB46AB0 .. 0xB46AE4
0xB46AB0  mov     eax, [esp+arg_4]          ; cursor 结构
0xB46AB4  mov     ecx, [eax]
0xB46AB6  lea     edx, [ecx+4]
0xB46AB9  cmp     edx, [eax+4]
0xB46ABC  ja      short loc_B46AE2          ; 越界 ⇒ 失败
0xB46ABE  mov     ecx, [ecx]                ; ← 读 u32（item_id）
0xB46AC0  mov     edx, [esp+arg_0]          ; dst
0xB46AC4  mov     [edx], ecx
0xB46AC6  add     dword ptr [eax], 4        ; ← 游标 +4
0xB46AC9  mov     ecx, [eax]
0xB46ACB  push    esi
0xB46ACC  lea     esi, [ecx+2]
0xB46ACF  cmp     esi, [eax+4]
0xB46AD2  pop     esi
0xB46AD3  ja      short loc_B46AE2
0xB46AD5  mov     cx, [ecx]                 ; ← 读 u16（num）
0xB46AD8  mov     [edx+4], cx
0xB46ADC  add     dword ptr [eax], 2        ; ← 游标 +2
0xB46ADF  mov     al, 1
0xB46AE1  retn
0xB46AE2  xor     al, al
0xB46AE4  retn
```

## E3 长度闭合（负载恰好 6 字节，槽位 8 只是富余）

```asm
; VA: 0xB52401 .. 0xB52409
0xB52401  mov     ebx, [esp+2C5Ch+var_2C44]   ; 读完后的游标
0xB52405  cmp     ebx, [esp+2C5Ch+var_2C40]   ; vs 报文末尾
0xB52409  jnz     short loc_B523E7            ; ← 不等则 push 1EDh 报错
```

## E4 含义取证：结构体打印器 `sub_B47AA0`（`cshist_item={` / `item_id=` / `num=`）

```asm
; 调用点 VA: 0xB5247C .. 0xB52490
0xB5247C  mov     eax, [esp+2C5Ch+var_2C04]   ; 槽指针（整个结构体）
0xB52480  push    eax
0xB52481  push    offset aCshistItem          ; ← "cshist_item="
0xB52486  push    edi
0xB52487  call    sub_41D990
0xB5248C  add     esp, 8
0xB5248F  push    eax
0xB52490  call    sub_B47AA0                  ; ← 结构体格式化

; 格式化器本体 VA: 0xB47AA0 .. 0xB47B0A
0xB47AA6  push    offset asc_EDAC3C           ; "{"
0xB47AAC  call    sub_41D990
0xB47AB5  mov     eax, [edi]                   ; edi = 结构体指针
0xB47AC0  push    offset aItemId               ; ← "item_id="
0xB47AD0  call    sub_B03580
0xB47ADB  movzx   ecx, word ptr [edi+4]        ; ← 第 2 成员按 u16 取
0xB47AE3  push    offset aNum                  ; ← "num="
0xB47AF3  call    sub_B032A0
0xB47AF8  push    offset unk_EDABE4            ; "}"
```

## E5 去向：整个结构体（指针）交 `vt[0x4A4]`

```asm
; VA: 0xB524CB .. 0xB524DC
0xB524CB  mov     edx, [esi]
0xB524CD  mov     eax, [esp+2C5Ch+var_2C04]   ; 槽地址（结构体指针）
0xB524D1  mov     edx, [edx+4A4h]             ; ← vt[0x4A4]
0xB524D7  push    eax
0xB524D8  mov     ecx, esi
0xB524DA  call    edx                         ; vt[0x4A4](cshist_item*)
0xB524DC  add     dword ptr [esi+61C8h], 1    ; 接收计数自增
```
