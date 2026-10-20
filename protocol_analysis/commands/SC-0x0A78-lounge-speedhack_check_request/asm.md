# 汇编证据 —— SC-0x0A78-lounge-speedhack_check_request

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 case 入口 + 解码缓冲申请（容量 `4`）

```asm
; VA: 0xB54B4C .. 0xB54B7B
0xB54B4C  push    215h                     ; ← 本 case 错误码
0xB54B51  mov     ecx, esi
0xB54B53  call    sub_B41120
0xB54B58  test    al, al
0xB54B5A  jz      loc_B890FE
0xB54B60  mov     ecx, [esi+0Ch]
0xB54B63  mov     eax, [ecx]
0xB54B65  mov     edx, [eax+78h]
0xB54B68  push    4                        ; ← 容量 4 == 线长
0xB54B6A  call    edx
0xB54B6C  mov     [esp+2C5Ch+var_2C3C], eax ; 缓冲游标
0xB54B70  mov     eax, [esi+0Ch]
0xB54B73  push    eax
0xB54B74  lea     ecx, [esp+2C60h+var_2678]
0xB54B7B  call    sub_ABB2F0               ; 初始化 {cur,end} 读游标
```

## E2 字段 1：`sec`（u32，偏移 0）

```asm
; VA: 0xB54B80 .. 0xB54BA3
0xB54B80  lea     ecx, [esp+2C5Ch+var_2C3C]   ; &缓冲游标
0xB54B84  push    ecx
0xB54B85  lea     ecx, [esp+2C60h+var_2C48]   ; 槽
0xB54B94  call    sub_B41470                  ; 缓冲预留 4B（非字段）
0xB54B99  mov     eax, [esp+2C5Ch+var_2C48]
0xB54B9D  lea     edx, [esp+2C5Ch+var_2C44]   ; &线游标
0xB54BA1  push    edx
0xB54BA2  push    eax
0xB54BA3  call    sub_B02DD0                  ; ← 读 u32
0xB54BA8  add     esp, 8
```

## E3 长度闭合（游标 == 报文末尾；成功 = 落空继续）

```asm
; VA: 0xB54BCB .. 0xB54BD3
0xB54BCB  mov     ebx, [esp+2C5Ch+var_2C44]   ; 读完后的游标
0xB54BCF  cmp     ebx, [esp+2C5Ch+var_2C40]   ; vs 报文末尾
0xB54BD3  jnz     short loc_B54BB1            ; ← 不等 ⇒ push 215h 报错
```

## E4 含义取证 + 去向：日志 `sec=` 与 `vt[0x508]`

```asm
; VA: 0xB54C46 .. 0xB54CA6
0xB54C46  mov     eax, [esp+2C5Ch+var_2C48]   ; sec 槽
0xB54C4A  mov     ecx, [eax]
0xB54C4D  push    offset aSec                 ; ← "sec="
0xB54C5D  call    sub_B03580                  ; 十进制打印器
0xB54C95  mov     eax, [esp+2C5Ch+var_2C48]   ; sec 槽
0xB54C99  mov     ecx, [eax]
0xB54C9B  mov     edx, [esi]
0xB54C9D  mov     edx, [edx+508h]             ; ← vt[0x508]
0xB54CA3  push    ecx                         ; 唯一实参 = sec
0xB54CA4  mov     ecx, esi
0xB54CA6  call    edx
0xB54CA8  add     dword ptr [esi+6948h], 1    ; 本命令接收计数（64 位）
0xB54CB6  adc     dword ptr [esi+694Ch], 0
```
