# 汇编证据 —— SC-0x0A7A-lounge-storage_msma_extend_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 case 入口 + 解码缓冲申请（容量 `8`）

```asm
; VA: 0xB54ED0 .. 0xB54EFF
0xB54ED0  push    1F7h                     ; ← 本 case 错误码
0xB54ED5  mov     ecx, esi
0xB54ED7  call    sub_B41120
0xB54EDC  test    al, al
0xB54EDE  jz      loc_B890FE
0xB54EE4  mov     ecx, [esi+0Ch]
0xB54EE7  mov     eax, [ecx]
0xB54EE9  mov     edx, [eax+78h]
0xB54EEC  push    8                        ; ← 容量 8 == 线长
0xB54EEE  call    edx
0xB54EF0  mov     [esp+2C5Ch+var_2C3C], eax ; 缓冲游标
0xB54EF4  mov     eax, [esi+0Ch]
0xB54EF7  push    eax
0xB54EF8  lea     ecx, [esp+2C60h+var_280C]
0xB54EFF  call    sub_ABB2F0               ; 初始化 {cur,end} 读游标
```

## E2 字段 1：`result`（u32，偏移 0）

```asm
; VA: 0xB54F04 .. 0xB54F27
0xB54F04  lea     ecx, [esp+2C5Ch+var_2C3C]
0xB54F08  push    ecx
0xB54F09  lea     ecx, [esp+2C60h+var_2C38]   ; 槽
0xB54F18  call    sub_B41470                  ; 缓冲预留 4B（非字段）
0xB54F1D  mov     eax, [esp+2C5Ch+var_2C38]
0xB54F21  lea     edx, [esp+2C5Ch+var_2C44]   ; &线游标
0xB54F25  push    edx
0xB54F26  push    eax
0xB54F27  call    sub_B02DD0                  ; ← 读 u32
```

## E3 字段 2：`slot_num`（u32，偏移 4）

```asm
; VA: 0xB54F4F .. 0xB54F67
0xB54F4F  lea     ecx, [esp+2C5Ch+var_2C3C]
0xB54F53  push    ecx
0xB54F54  lea     ecx, [esp+2C60h+var_2C48]   ; 槽
0xB54F58  call    sub_B41470                  ; 缓冲预留 4B（非字段）
0xB54F5D  mov     eax, [esp+2C5Ch+var_2C48]
0xB54F61  lea     edx, [esp+2C5Ch+var_2C44]
0xB54F65  push    edx
0xB54F66  push    eax
0xB54F67  call    sub_B02DD0                  ; ← 读 u32
```

## E4 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB54F73 .. 0xB54F7D
0xB54F73  mov     ebx, [esp+2C5Ch+var_2C44]   ; 读完后的游标
0xB54F77  cmp     ebx, [esp+2C5Ch+var_2C40]   ; vs 报文末尾
0xB54F7B  mov     ecx, esi
0xB54F7D  jz      short loc_B54F99            ; ← 不等 ⇒ push 1F7h 报错
```

## E5 含义取证 + 去向：日志 `result=`/`slot_num=` 与 `vt[0x4B4]`

```asm
; VA: 0xB5500A .. 0xB5509B
0xB5500A  mov     eax, [esp+2C5Ch+var_2C38]   ; result 槽
0xB5500E  mov     ecx, [eax]
0xB55010  push    offset word_F641DC          ; ","
0xB55016  push    offset aResult              ; ← "result="
0xB55026  call    sub_B03580                  ; 十进制打印器
0xB55031  mov     edx, [esp+2C64h+var_2C48]   ; slot_num 槽
0xB5503B  push    offset aSlotNum             ; ← "slot_num="
0xB5504B  call    sub_B03580                  ; 十进制打印器
0xB55083  mov     eax, [esp+2C5Ch+var_2C48]   ; slot_num 槽
0xB55087  mov     ecx, [eax]
0xB55089  mov     eax, [esp+2C5Ch+var_2C38]   ; result 槽
0xB5508D  mov     edx, [esi]
0xB5508F  mov     edx, [edx+4B4h]             ; ← vt[0x4B4]
0xB55095  push    ecx                         ; 实参 2 = slot_num
0xB55096  mov     ecx, [eax]
0xB55098  push    ecx                         ; 实参 1 = result
0xB55099  mov     ecx, esi
0xB5509B  call    edx
0xB5509D  add     dword ptr [esi+63A8h], 1    ; 本命令接收计数（64 位）
0xB550AB  adc     dword ptr [esi+63ACh], 0
```
