# 汇编证据 —— SC-0x0C41-lounge-exchange_play_bonus_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 case 入口 + 解码缓冲申请（容量 `8`）

```asm
; VA: 0xB54CE9 .. 0xB54D18
0xB54CE9  push    180h                     ; ← 本 case 错误码
0xB54CEE  mov     ecx, esi
0xB54CF0  call    sub_B41120
0xB54CF5  test    al, al
0xB54CF7  jz      loc_B890FE
0xB54CFD  mov     ecx, [esi+0Ch]
0xB54D00  mov     eax, [ecx]
0xB54D02  mov     edx, [eax+78h]
0xB54D05  push    8                        ; ← 容量 8 == 线长
0xB54D07  call    edx
0xB54D09  mov     [esp+2C5Ch+var_2C3C], eax ; 缓冲游标
0xB54D0D  mov     eax, [esi+0Ch]
0xB54D10  push    eax
0xB54D11  lea     ecx, [esp+2C60h+var_2814]
0xB54D18  call    sub_ABB2F0               ; 初始化 {cur,end} 读游标
```

## E2 字段 1：`result`（u32，偏移 0）

```asm
; VA: 0xB54D1D .. 0xB54D40
0xB54D1D  lea     ecx, [esp+2C5Ch+var_2C3C]
0xB54D21  push    ecx
0xB54D22  lea     ecx, [esp+2C60h+var_2C38]   ; 槽
0xB54D31  call    sub_B41470                  ; 缓冲预留 4B（非字段）
0xB54D36  mov     eax, [esp+2C5Ch+var_2C38]
0xB54D3A  lea     edx, [esp+2C5Ch+var_2C44]   ; &线游标
0xB54D3E  push    edx
0xB54D3F  push    eax
0xB54D40  call    sub_B02DD0                  ; ← 读 u32
```

## E3 字段 2：`reward_id`（u32，偏移 4）

```asm
; VA: 0xB54D68 .. 0xB54D80
0xB54D68  lea     ecx, [esp+2C5Ch+var_2C3C]
0xB54D6C  push    ecx
0xB54D6D  lea     ecx, [esp+2C60h+var_2C48]   ; 槽
0xB54D71  call    sub_B41470                  ; 缓冲预留 4B（非字段）
0xB54D76  mov     eax, [esp+2C5Ch+var_2C48]
0xB54D7A  lea     edx, [esp+2C5Ch+var_2C44]
0xB54D7E  push    edx
0xB54D7F  push    eax
0xB54D80  call    sub_B02DD0                  ; ← 读 u32
```

## E4 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB54D8C .. 0xB54D96
0xB54D8C  mov     ebx, [esp+2C5Ch+var_2C44]   ; 读完后的游标
0xB54D90  cmp     ebx, [esp+2C5Ch+var_2C40]   ; vs 报文末尾
0xB54D94  mov     ecx, esi
0xB54D96  jz      short loc_B54DB2            ; ← 不等 ⇒ push 180h 报错
```

## E5 含义取证 + 去向：日志 `result=`/`reward_id=` 与 `vt[0x3BC]`

```asm
; VA: 0xB54E23 .. 0xB54EB4
0xB54E29  push    offset word_F641DC          ; ","
0xB54E2F  push    offset aResult              ; ← "result="
0xB54E3F  call    sub_B03580                  ; 十进制打印器
0xB54E53  push    offset aRewardId            ; ← "reward_id="
0xB54E64  call    sub_B03580                  ; 十进制打印器
0xB54E9C  mov     eax, [esp+2C5Ch+var_2C48]   ; reward_id 槽
0xB54EA0  mov     ecx, [eax]
0xB54EA2  mov     eax, [esp+2C5Ch+var_2C38]   ; result 槽
0xB54EA6  mov     edx, [esi]
0xB54EA8  mov     edx, [edx+3BCh]             ; ← vt[0x3BC]
0xB54EAE  push    ecx                         ; 实参 2 = reward_id
0xB54EAF  mov     ecx, [eax]
0xB54EB1  push    ecx                         ; 实参 1 = result
0xB54EB2  mov     ecx, esi
0xB54EB4  call    edx
0xB54EB6  add     dword ptr [esi+4D58h], 1    ; 本命令接收计数（64 位）
0xB54EC4  adc     dword ptr [esi+4D5Ch], 0
```
