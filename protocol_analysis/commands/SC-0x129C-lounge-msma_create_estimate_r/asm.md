# 汇编证据 —— SC-0x129C-lounge-msma_create_estimate_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 case 入口 + 解码缓冲申请（容量 `0x8`）

```asm
; VA: 0xB55853 .. 0xB5588B
0xB55853  call    sub_B41120               ; case 起始守卫（不读线）
0xB55858  test    al, al
0xB5585A  jz      loc_B890FE
0xB55860  mov     ecx, [esi+0Ch]
0xB55863  mov     eax, [ecx]
0xB55865  mov     edx, [eax+78h]
0xB55868  push    8                        ; ← 容量 8
0xB5586A  call    edx
0xB5586C  mov     [esp+2C5Ch+var_2C3C], eax ; 解码缓冲基址
0xB55870  mov     eax, [esi+0Ch]
0xB55873  push    eax
0xB55874  lea     ecx, [esp+2C60h+var_2804]
0xB5587B  call    sub_ABB2F0               ; 初始化线游标
```

## E2 字段 1：`result`（u32，偏移 0）

```asm
; VA: 0xB55880 .. 0xB558B1
0xB55880  lea     ecx, [esp+2C5Ch+var_2C3C]
0xB55884  push    ecx
0xB55885  lea     ecx, [esp+2C60h+var_2C38]
0xB55894  call    sub_B41470               ; u32 槽预留（推进缓冲游标，不是字段）
0xB55899  mov     eax, [esp+2C5Ch+var_2C38]
0xB5589D  lea     edx, [esp+2C5Ch+var_2C44] ; &线游标
0xB558A1  push    edx
0xB558A2  push    eax
0xB558A3  call    sub_B02DD0               ; ← 读 u32（消费 4 字节）
0xB558A8  add     esp, 8
0xB558AB  test    al, al
0xB558AD  jnz     short loc_B558CB         ; 成功分支
0xB558B6  push    101h                     ; ← 错误码
```

## E3 字段 2：`price`（u32，偏移 4）+ 长度闭合

```asm
; VA: 0xB558CB .. 0xB55910
0xB558CB  lea     ecx, [esp+2C5Ch+var_2C3C]
0xB558CF  push    ecx
0xB558D0  lea     ecx, [esp+2C60h+var_2C48]
0xB558D4  call    sub_B41470               ; u32 槽预留（非字段）
0xB558D9  mov     eax, [esp+2C5Ch+var_2C48]
0xB558DD  lea     edx, [esp+2C5Ch+var_2C44]
0xB558E1  push    edx
0xB558E2  push    eax
0xB558E3  call    sub_B02DD0               ; ← 读 u32（消费 4 字节）
0xB558E8  add     esp, 8
0xB558EB  test    al, al
0xB558ED  jz      short loc_B558AF
0xB558EF  mov     ebx, [esp+2C5Ch+var_2C44] ; 读完后的线游标
0xB558F3  cmp     ebx, [esp+2C5Ch+var_2C40] ; vs 报文末尾
0xB558F9  jz      short loc_B55915         ; ← 不等 ⇒ push 1 / push 101h 报错
```

## E4 含义取证：块内日志 `result=` / `price=`

```asm
; VA: 0xB55986 .. 0xB559C7
0xB55986  mov     eax, [esp+2C5Ch+var_2C38] ; result 槽
0xB5598A  mov     ecx, [eax]
0xB55992  push    offset aResult            ; ← "result="
0xB559A2  call    sub_B03580               ; u32 打印器
0xB559AD  mov     edx, [esp+2C64h+var_2C48] ; price 槽
0xB559B1  mov     eax, [edx]
0xB559B7  push    offset aPrice             ; ← "price="
0xB559C7  call    sub_B03580
```

## E5 去向：`vt[0x2A8](result, price)`

```asm
; VA: 0xB559FF .. 0xB55A27
0xB559FF  mov     eax, [esp+2C5Ch+var_2C48] ; price 槽
0xB55A03  mov     ecx, [eax]
0xB55A05  mov     eax, [esp+2C5Ch+var_2C38] ; result 槽
0xB55A09  mov     edx, [esi]
0xB55A0B  mov     edx, [edx+2A8h]           ; ← vt[0x2A8]
0xB55A11  push    ecx                       ; 实参 2 = price
0xB55A12  mov     ecx, [eax]
0xB55A14  push    ecx                       ; 实参 1 = result
0xB55A15  mov     ecx, esi
0xB55A17  call    edx
0xB55A19  add     dword ptr [esi+3588h], 1  ; 本命令接收计数（64 位）
```
