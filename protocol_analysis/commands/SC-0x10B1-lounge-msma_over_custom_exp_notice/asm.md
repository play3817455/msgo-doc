# 汇编证据 —— SC-0x10B1-lounge-msma_over_custom_exp_notice

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 case 入口 + 解码缓冲申请（容量 `0xC`）

```asm
; VA: 0xB55A33 .. 0xB55A62
0xB55A33  push    265h                     ; ← 本 case 错误码
0xB55A38  mov     ecx, esi
0xB55A3A  call    sub_B41120
0xB55A3F  test    al, al
0xB55A41  jz      loc_B890FE
0xB55A47  mov     ecx, [esi+0Ch]
0xB55A4A  mov     eax, [ecx]
0xB55A4C  mov     edx, [eax+78h]
0xB55A4F  push    0Ch                      ; ← 容量 0xC == 线长 12
0xB55A51  call    edx
0xB55A53  mov     [esp+2C5Ch+var_2C3C], eax
0xB55A5B  lea     ecx, [esp+2C60h+var_27FC]
0xB55A62  call    sub_ABB2F0               ; 初始化线游标 {cur,end}
```

## E2 字段 1：`uniq_msid`（u64，偏移 0）

```asm
; VA: 0xB55A67 .. 0xB55A94
0xB55A67  lea     ecx, [esp+2C5Ch+var_2C3C]
0xB55A6B  push    ecx
0xB55A6C  lea     ecx, [esp+2C60h+var_2C20] ; 槽
0xB55A7B  call    sub_B41A10               ; u64 槽预留（步进 8，非字段）
0xB55A80  mov     ebx, [esp+2C5Ch+var_2C20] ; 槽地址
0xB55A84  lea     edx, [esp+2C5Ch+var_2C44] ; &线游标
0xB55A88  push    edx
0xB55A89  push    ebx
0xB55A8A  call    sub_B06200               ; ← 读 8 字节（u64）
0xB55A8F  add     esp, 8
0xB55A92  test    al, al
0xB55A94  jnz     short loc_B55AB2         ; 成功分支
```

## E3 字段 2：`exp`（u32，偏移 8）

```asm
; VA: 0xB55AB2 .. 0xB55AD4
0xB55AB2  lea     eax, [esp+2C5Ch+var_2C3C]
0xB55AB6  push    eax
0xB55AB7  lea     ecx, [esp+2C60h+var_2C48] ; 槽
0xB55ABB  call    sub_B41470               ; 缓冲预留 4B（非字段）
0xB55AC0  mov     edx, [esp+2C5Ch+var_2C48]
0xB55AC4  lea     ecx, [esp+2C5Ch+var_2C44]
0xB55AC8  push    ecx
0xB55AC9  push    edx
0xB55ACA  call    sub_B02DD0               ; ← 读 u32
0xB55ACF  add     esp, 8
0xB55AD2  test    al, al
0xB55AD4  jz      short loc_B55A96         ; 失败 ⇒ 报错
```

## E4 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB55AD6 .. 0xB55AE2
0xB55AD6  mov     eax, [esp+2C5Ch+var_2C44] ; 读完后的线游标
0xB55ADA  cmp     eax, [esp+2C5Ch+var_2C40] ; vs 报文末尾
0xB55ADE  mov     ecx, esi
0xB55AE0  jz      short loc_B55AFC          ; ← 不等 ⇒ push 265h 报错
```

## E5 含义取证：块内日志 `uniq_msid=`（64 位）与 `exp=`

```asm
; VA: 0xB55B6D .. 0xB55BB3
0xB55B6D  mov     eax, [ebx+4]              ; ← u64 高 32 位
0xB55B70  mov     ecx, [ebx]                ; ← u64 低 32 位
0xB55B79  push    offset aUniqMsid          ; ← "uniq_msid="
0xB55B89  call    sub_B08500                ; 64 位打印器
0xB55B94  mov     edx, [esp+2C64h+var_2C48] ; exp 槽
0xB55B98  mov     eax, [edx]
0xB55B9E  push    offset aExp               ; ← "exp="
0xB55BAE  call    sub_B03580                ; 十进制打印器
```

## E6 去向：`vt[0x5C8](uniq_msid 低, uniq_msid 高, exp)`

```asm
; VA: 0xB55BEA .. 0xB55C04
0xB55BEA  mov     eax, [esp+2C5Ch+var_2C48] ; exp 槽
0xB55BEE  mov     ecx, [eax]                ; ecx = exp
0xB55BF0  mov     eax, [ebx+4]              ; uniq_msid 高 32 位
0xB55BF3  mov     edx, [esi]
0xB55BF5  mov     edx, [edx+5C8h]           ; ← vt[0x5C8]
0xB55BFB  push    ecx                       ; 实参 3 = exp
0xB55BFC  mov     ecx, [ebx]                ; uniq_msid 低 32 位
0xB55BFE  push    eax                       ; 实参 2 = uniq_msid 高
0xB55BFF  push    ecx                       ; 实参 1 = uniq_msid 低
0xB55C00  mov     ecx, esi
0xB55C02  call    edx
0xB55C04  add     dword ptr [esi+7848h], 1   ; 本命令接收计数（64 位）
0xB55C12  adc     dword ptr [esi+784Ch], 0
```
