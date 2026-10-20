# 汇编证据 —— SC-0x090C-lounge-pilot_money_update

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 case 入口 + 解码缓冲申请（容量 `4`）

```asm
; VA: 0xB547AC .. 0xB547D8
0xB547AC  push    23h ; '#'                ; ← 本 case 错误码
0xB547AE  mov     ecx, esi
0xB547B0  call    sub_B41120
0xB547B5  test    al, al
0xB547B7  jz      loc_B890FE
0xB547BD  mov     ecx, [esi+0Ch]
0xB547C0  mov     eax, [ecx]
0xB547C2  mov     edx, [eax+78h]
0xB547C5  push    4                        ; ← 容量 4 == 线长
0xB547C7  call    edx
0xB547C9  mov     [esp+2C5Ch+var_2C3C], eax ; 缓冲游标
0xB547CD  mov     eax, [esi+0Ch]
0xB547D0  push    eax
0xB547D1  lea     ecx, [esp+2C60h+var_2680]
0xB547D8  call    sub_ABB2F0               ; 初始化 {cur,end} 读游标
```

## E2 字段 1：`money`（u32，偏移 0）

```asm
; VA: 0xB547E2 .. 0xB54800
0xB547E1  push    ecx                         ; &缓冲游标
0xB547E2  lea     ecx, [esp+2C60h+var_2C48]   ; 槽
0xB547F1  call    sub_B41470                  ; 缓冲预留 4B（非字段）
0xB547F6  mov     eax, [esp+2C5Ch+var_2C48]
0xB547FA  lea     edx, [esp+2C5Ch+var_2C44]   ; &线游标
0xB547FE  push    edx
0xB547FF  push    eax
0xB54800  call    sub_B02DD0                  ; ← 读 u32
0xB54805  add     esp, 8
```

## E3 长度闭合（游标 == 报文末尾；成功 = 落空继续）

```asm
; VA: 0xB54825 .. 0xB5482D
0xB54825  mov     ebx, [esp+2C5Ch+var_2C44]   ; 读完后的游标
0xB54829  cmp     ebx, [esp+2C5Ch+var_2C40]   ; vs 报文末尾
0xB5482D  jnz     short loc_B5480E            ; ← 不等 ⇒ push 23h 报错
```

## E4 含义取证 + 去向：日志 `money=` 与 `vt[0xAC]`

```asm
; VA: 0xB5489D .. 0xB548FD
0xB5489D  mov     eax, [esp+2C5Ch+var_2C48]   ; money 槽
0xB548A1  mov     ecx, [eax]
0xB548A4  push    offset aMoney                ; ← "money="
0xB548B4  call    sub_B03580                  ; 十进制打印器
0xB548EC  mov     eax, [esp+2C5Ch+var_2C48]   ; money 槽
0xB548F0  mov     ecx, [eax]
0xB548F2  mov     edx, [esi]
0xB548F4  mov     edx, [edx+0ACh]             ; ← vt[0xAC]
0xB548FA  push    ecx                         ; 唯一实参 = money
0xB548FB  mov     ecx, esi
0xB548FD  call    edx
0xB548FF  add     dword ptr [esi+0BE8h], 1    ; 本命令接收计数（64 位）
0xB5490D  adc     dword ptr [esi+0BECh], 0
```
