# 汇编证据 —— SC-0x056D-battle-battleship_cooltime_notice

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 case 入口 + 解码缓冲申请（容量 `6`）

```asm
; VA: 0xB0DA13 .. 0xB0DA42
0xB0DA13  push    102h                     ; ← 本 case 错误码
0xB0DA18  mov     ecx, esi
0xB0DA1A  call    sub_B05DA0
0xB0DA1F  test    al, al
0xB0DA21  jz      loc_B317C7
0xB0DA27  mov     ecx, [esi+0Ch]
0xB0DA2A  mov     eax, [ecx]
0xB0DA2C  mov     edx, [eax+78h]           ; vt[0x78] = 申请解码缓冲
0xB0DA2F  push    6                        ; ← 容量 6（= 负载长）
0xB0DA31  call    edx
0xB0DA33  mov     [esp+1B3Ch+var_1B14], eax ; 缓冲基址
0xB0DA37  mov     eax, [esi+0Ch]
0xB0DA3A  push    eax
0xB0DA3B  lea     ecx, [esp+1B40h+var_1840]
0xB0DA42  call    sub_ABB2F0               ; 初始化 {cur,end} 读游标
```

## E2 两个字段

```asm
; VA: 0xB0DA47 .. 0xB0DAB4
0xB0DA5B  call    sub_B413B0               ; 预留 2B（非字段）
0xB0DA6A  call    sub_B02DF0               ; ← to_ent_id（u16，槽 var_1B20）
0xB0DA9B  call    sub_B41470               ; 预留 4B（非字段）
0xB0DAAA  call    sub_B02DD0               ; ← remain_msec（u32，槽 var_1B2C）
```

宽度判定依据：

```asm
; VA: 0xB02DF6/0xB02E0B（u16：+2）
0xB02DF6  lea     edx, [ecx+2]
0xB02E0B  add     dword ptr [eax], 2
; VA: 0xB02DD6/0xB02DE9（u32：+4）
0xB02DD6  lea     edx, [ecx+4]
0xB02DE9  add     dword ptr [eax], 4
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB0DAB6 .. 0xB0DAC0
0xB0DAB6  mov     ebx, [esp+1B3Ch+var_1B28]   ; 读完后的游标
0xB0DABA  cmp     ebx, [esp+1B3Ch+var_1B24]   ; vs 报文末尾
0xB0DAC0  jz      short loc_B0DADC            ; ← 不等 ⇒ push 102h 报错
```

## E4 含义取证：日志格式串

```asm
; VA: 0xB0DB4D .. 0xB0DB8F
0xB0DB54  push    offset word_F641DC         ; ","
0xB0DB5A  push    offset aToEntId            ; ← "to_ent_id="
0xB0DB6A  call    sub_B032A0                ; 十六进制打印器
0xB0DB7F  push    offset aRemainMsec         ; ← "remain_msec="
0xB0DB8F  call    sub_B03580                ; 十进制打印器
```

## E5 去向：`vt[0x310]`

```asm
; VA: 0xB0DBC7 .. 0xB0DBF0
0xB0DBC7  mov     eax, [esp+1B3Ch+var_1B2C]   ; remain_msec 槽
0xB0DBCB  mov     ecx, [eax]
0xB0DBCD  mov     eax, [esp+1B3Ch+var_1B20]   ; to_ent_id 槽
0xB0DBD1  mov     edx, [esi]
0xB0DBD3  mov     edx, [edx+310h]             ; ← vt[0x310]
0xB0DBD9  push    ecx                         ; 实参 2 = remain_msec
0xB0DBDA  movzx   ecx, word ptr [eax]
0xB0DBDD  push    ecx                         ; 实参 1 = to_ent_id
0xB0DBDE  mov     ecx, esi
0xB0DBE0  call    edx
0xB0DBE2  add     dword ptr [esi+3340h], 1    ; 本命令接收计数（64 位）
0xB0DBF0  adc     dword ptr [esi+3344h], 0
```
