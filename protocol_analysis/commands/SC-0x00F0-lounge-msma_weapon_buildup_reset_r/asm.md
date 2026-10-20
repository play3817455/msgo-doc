# 汇编证据 —— SC-0x00F0-msma_weapon_buildup_reset_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 case 入口 + 解码缓冲申请（容量 16）

```asm
; VA: 0xB51A58 .. 0xB51A85
0xB51A58  call    sub_B41120               ; case 级开关检查（前置 push 118h = 开关号）
0xB51A5D  test    al, al
0xB51A5F  jz      loc_B890FE
0xB51A65  mov     ecx, [esi+0Ch]
0xB51A68  mov     eax, [ecx]
0xB51A6A  mov     edx, [eax+78h]
0xB51A6D  push    10h                      ; ← 容量 16（旁证，不是线长）
0xB51A6F  call    edx
0xB51A71  mov     [esp+2C5Ch+var_2C04], eax
0xB51A75  mov     eax, [esi+0Ch]
0xB51A78  push    eax
0xB51A79  lea     ecx, [esp+2C60h+var_2928]
0xB51A80  call    sub_ABB2F0               ; 用传输层缓冲初始化 {cur,end}（非 IO）
```

## E2 字段 1：`sub_B02DD0` 读 u32（负载 +0）

```asm
; VA: 0xB51A85 .. 0xB51AAD
0xB51A85  lea     ecx, [esp+2C5Ch+var_2C04]
0xB51A89  push    ecx
0xB51A8A  lea     ecx, [esp+2C60h+var_2C00]   ; 槽
0xB51A8E  mov     [esp+2C60h+var_4], 135h
0xB51A99  call    sub_B41470               ; 预留 4 字节槽（非字段）
0xB51A9E  mov     eax, [esp+2C5Ch+var_2C00]
0xB51AA2  lea     edx, [esp+2C5Ch+var_2C44]
0xB51AA6  push    edx
0xB51AA7  push    eax
0xB51AA8  call    sub_B02DD0               ; ← 读 u32
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
0xB02DE9  add     dword ptr [eax], 4        ; ← 游标 +4
0xB02DEC  mov     al, 1
0xB02DEE  retn
```

## E3 字段 2：`sub_B06200` 读 u64（负载 +4）

```asm
; VA: 0xB51AD0 .. 0xB51AF0
0xB51AD0  lea     ecx, [esp+2C5Ch+var_2C04]
0xB51AD4  push    ecx
0xB51AD5  lea     ecx, [esp+2C60h+var_2C10]
0xB51AD9  call    sub_B41A10               ; 预留 8 字节槽（非字段）
0xB51ADE  mov     eax, [esp+2C5Ch+var_2C10]
0xB51AE2  lea     edx, [esp+2C5Ch+var_2C44]
0xB51AE6  push    edx
0xB51AE7  push    eax
0xB51AE8  call    sub_B06200               ; ← 读 u64
0xB51AED  add     esp, 8
0xB51AF0  test    al, al
```

`sub_B06200` 本体（读 **u64**，游标 +8）见 `../SC-0x00C7-lounge-msma_trialms_back_r/asm.md` E3
（`0xB06206 lea edx,[ecx+8]`、`0xB06216 mov esi,[ecx]`、`0xB0621A mov ecx,[ecx+4]`、`0xB06220 add dword ptr [eax], 8`）。

## E4 字段 3：`sub_B02DD0` 读 u32（负载 +12）

```asm
; VA: 0xB51AF4 .. 0xB51B14
0xB51AF4  lea     ecx, [esp+2C5Ch+var_2C04]
0xB51AF8  push    ecx
0xB51AF9  lea     ecx, [esp+2C60h+var_2C24]
0xB51AFD  call    sub_B41470               ; 预留 4 字节槽（非字段）
0xB51B02  mov     eax, [esp+2C5Ch+var_2C24]
0xB51B06  lea     edx, [esp+2C5Ch+var_2C44]
0xB51B0A  push    edx
0xB51B0B  push    eax
0xB51B0C  call    sub_B02DD0               ; ← 读 u32
0xB51B11  add     esp, 8
```

## E5 长度闭合（负载恰好 16 字节：4 + 8 + 4）

```asm
; VA: 0xB51B18 .. 0xB51B22
0xB51B18  mov     ebx, [esp+2C5Ch+var_2C44]   ; 读完后的游标
0xB51B1C  cmp     ebx, [esp+2C5Ch+var_2C40]   ; vs 报文末尾
0xB51B20  mov     ecx, esi
0xB51B22  jz      short loc_B51B3E            ; ← 不等则 push 118h 报错
```

## E6 含义取证：块内日志格式串（`result=` / `uniqid_ms=` / `item_id=`）

```asm
; VA: 0xB51BAF .. 0xB51C0E
0xB51BAF  mov     eax, [esp+2C5Ch+var_2C00]   ; 字段 1 槽
0xB51BB3  mov     ecx, [eax]
0xB51BB5  push    offset word_F641DC          ; ","
0xB51BBA  push    ecx
0xB51BBB  push    offset aResult             ; ← "result="
0xB51BC0  push    edi
0xB51BC1  call    sub_41D990
...
0xB51BD6  mov     eax, [esp+2C64h+var_2C10]   ; 字段 2 槽（u64）
0xB51BDA  mov     edx, [eax+4]
0xB51BDD  mov     eax, [eax]
0xB51BE9  push    offset aUniqidMs           ; ← "uniqid_ms="
...
0xB51C04  mov     ecx, [esp+2C64h+var_2C24]   ; 字段 3 槽
0xB51C08  mov     edx, [ecx]
0xB51C0E  push    offset aItemId             ; ← "item_id="
```

## E7 去向：3 个值一次性交 `vt[0x2D8]`

```asm
; VA: 0xB51C56 .. 0xB51C7B
0xB51C56  mov     eax, [esp+2C5Ch+var_2C24]   ; item_id 槽
0xB51C5A  mov     ecx, [eax]
0xB51C5C  mov     eax, [esp+2C5Ch+var_2C10]   ; u64 槽
0xB51C60  mov     edx, [esi]
0xB51C62  mov     edx, [edx+2D8h]            ; ← vt[0x2D8]
0xB51C68  push    ecx                        ; item_id
0xB51C69  mov     ecx, [eax+4]               ; u64 高
0xB51C6C  mov     eax, [eax]                 ; u64 低
0xB51C6E  push    ecx
0xB51C6F  mov     ecx, [esp+2C64h+var_2C00]   ; result 槽
0xB51C73  push    eax
0xB51C74  mov     eax, [ecx]
0xB51C76  push    eax
0xB51C77  mov     ecx, esi
0xB51C79  call    edx                        ; vt[0x2D8](result, uniqid_ms, item_id)
0xB51C7B  add     dword ptr [esi+39D8h], 1
```
