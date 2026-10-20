# 汇编证据 —— SC-0x0863-lounge-restrictitem_buy_info_notice

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 case 入口 + 解码缓冲申请（容量 `0x44` = 68）

```asm
; VA: 0xB53E24 .. 0xB53E5D
0xB53E24  push    203h                     ; ← 本 case 错误码
0xB53E29  mov     ecx, esi
0xB53E2B  call    sub_B41120
0xB53E30  test    al, al
0xB53E32  jz      loc_B890FE
0xB53E38  mov     ecx, [esi+0Ch]
0xB53E3B  mov     eax, [ecx]
0xB53E3D  mov     edx, [eax+78h]           ; vt[0x78] = 申请解码缓冲
0xB53E40  push    44h ; 'D'                ; ← 容量 68 = 4 + 4*16
0xB53E42  call    edx
0xB53E44  mov     [esp+2C5Ch+var_2C20], eax ; 缓冲游标
0xB53E48  mov     eax, [esi+0Ch]
0xB53E4B  push    eax
0xB53E4C  lea     ecx, [esp+2C60h+var_2824]
0xB53E53  call    sub_ABB2F0               ; 初始化 {cur,end} 读游标
```

## E2 字段 1：`count`（u32，上限 16）

```asm
; VA: 0xB53E58 .. 0xB53E9C
0xB53E58  lea     ecx, [esp+2C5Ch+var_2C44]   ; &线游标
0xB53E5C  push    ecx
0xB53E5D  lea     edx, [esp+2C60h+var_2C3C]   ; &槽
0xB53E61  push    edx
0xB53E62  mov     [esp+2C64h+var_4], 233h
0xB53E6D  call    sub_B02DD0                  ; ← 读 u32
0xB53E72  add     esp, 8
0xB53E75  test    al, al
0xB53E77  jnz     short loc_B53E95            ; 成功分支
0xB53E95  mov     ebx, [esp+2C5Ch+var_2C3C]   ; ebx = count
0xB53E99  cmp     ebx, 10h                    ; ← 上限 16
0xB53E9C  ja      short loc_B53E79            ; 越界 ⇒ push 203h 报错
```

## E3 字段 2：数组预留（`sub_B41850`，槽步进 4）

```asm
; VA: 0xB53E9E .. 0xB53EAD
0xB53E9E  push    ebx                         ; N = count
0xB53E9F  lea     eax, [esp+2C60h+var_2C20]   ; 缓冲游标
0xB53EA3  push    eax
0xB53EA4  lea     ecx, [esp+2C64h+var_2C18]   ; 出参 {基址, N}
0xB53EA8  call    sub_B41850                  ; ← 定长数组预留（4 字节/元素）
; sub_B41850 @0xB41850：0xB41870 add [edx],4 ⇒ 槽步进 4
0xB53EAD  xor     edi, edi                    ; 元素下标
0xB53EAF  test    ebx, ebx
0xB53EB1  jbe     short loc_B53EF4            ; N==0 ⇒ 直接闭合
0xB53EB3  mov     ecx, [esp+2C5Ch+var_2C18]
0xB53EB7  mov     [esp+2C5Ch+var_2C48], ecx   ; 元素指针 = 数组基址
```

## E4 字段 2：元素循环读取 + 步进 4

```asm
; VA: 0xB53EC0 .. 0xB53EE0
0xB53EC0  mov     eax, [esp+2C5Ch+var_2C48]   ; 当前元素指针
0xB53EC4  lea     edx, [esp+2C5Ch+var_2C44]   ; &线游标
0xB53EC8  push    edx
0xB53EC9  push    eax
0xB53ECA  call    sub_B02DD0                  ; ← 读 u32 进元素
0xB53ECF  add     esp, 8
0xB53ED2  test    al, al
0xB53ED4  jz      short loc_B53EE4
0xB53ED6  add     [esp+2C5Ch+var_2C48], 4     ; ← 元素步进 = 4（线长，非结构体大小）
0xB53EDB  add     edi, 1
0xB53EDE  cmp     edi, ebx
0xB53EE0  jb      short loc_B53EC0
```

## E5 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB53EF4 .. 0xB53EFE
0xB53EF4  mov     ecx, [esp+2C5Ch+var_2C44]   ; 读完后的游标
0xB53EF8  cmp     ecx, [esp+2C5Ch+var_2C40]   ; vs 报文末尾
0xB53EFC  mov     ecx, esi
0xB53EFE  jz      short loc_B53F1A            ; ← 不等 ⇒ push 203h 报错
```

## E6 含义取证：块内日志格式串

```asm
; VA: 0xB53F8F .. 0xB53FEC
0xB53F8F  push    offset aRestrictitemBu      ; ← "restrictitem_buy={"
0xB53F94  push    edi
0xB53F95  call    sub_41D990
0xB53FA1  mov     eax, [esp+2C5Ch+var_2C18]   ; 数组基址
0xB53FA5  mov     ecx, [eax]                  ; 第 1 个元素
0xB53FAA  call    sub_B03580                  ; 十进制打印器
0xB53FCC  push    offset word_F641DC          ; ← ","
0xB53FC4  mov     eax, [edx+edi*4]            ; 后续元素（步进 4）
0xB53FEC  push    offset unk_EDABE4           ; "}"
```

## E7 去向：`vt[0x4D4]`（数组基址 + 计数）

```asm
; VA: 0xB54031 .. 0xB54041
0xB54031  mov     edx, [esi]
0xB54033  mov     eax, [esp+2C5Ch+var_2C18]   ; 数组基址
0xB54037  mov     edx, [edx+4D4h]             ; ← vt[0x4D4]
0xB5403D  push    ebx                         ; 实参 2 = count
0xB5403E  push    eax                         ; 实参 1 = 数组基址
0xB5403F  mov     ecx, esi
0xB54041  call    edx
0xB54043  add     dword ptr [esi+65E8h], 1    ; 本命令接收计数（64 位）
0xB54051  adc     dword ptr [esi+65ECh], 0
```
