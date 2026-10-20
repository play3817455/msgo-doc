# 汇编证据 —— SC-0x07E9-battle-room_kick_vote_get_enable_pilots_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 case 入口 + 解码缓冲申请（容量 `0x1AC` = 428）

```asm
; VA: 0xB0DBFC .. 0xB0DC2B
0xB0DBFC  push    31h                      ; ← 本 case 错误码
0xB0DBFE  mov     ecx, esi
0xB0DC00  call    sub_B05DA0
0xB0DC05  test    al, al
0xB0DC07  jz      loc_B317C7
0xB0DC0D  mov     ecx, [esi+0Ch]
0xB0DC10  mov     eax, [ecx]
0xB0DC12  mov     edx, [eax+78h]
0xB0DC15  push    1ACh                     ; ← 容量 428 = 12 + 4×(52+52)
0xB0DC1A  call    edx
0xB0DC1C  mov     [esp+1B3Ch+var_1B20], eax ; 缓冲基址
0xB0DC20  mov     eax, [esi+0Ch]
0xB0DC23  push    eax
0xB0DC24  lea     ecx, [esp+1B40h+var_19B4]
0xB0DC2B  call    sub_ABB2F0               ; 初始化 {cur,end} 读游标
```

## E2 第 1 组「计数 + 数组」（`A ≤ 52`）

```asm
; VA: 0xB0DC30 .. 0xB0DCB2
0xB0DC30  lea     ecx, [esp+1B3Ch+var_1B28]   ; 线游标
0xB0DC35  lea     edx, [esp+1B40h+var_1AF4]   ; &计数 A
0xB0DC45  call    sub_B02DD0                  ; ← 读 A（u32）
0xB0DC6A  mov     ebx, [esp+1B3Ch+var_1AF4]
0xB0DC6E  cmp     ebx, 34h                    ; ← 上限检查 52
0xB0DC71  ja      short loc_B0DC51            ; 超限 ⇒ push 31h 报错
0xB0DC73  push    ebx
0xB0DC74  lea     eax, [esp+1B40h+var_1B20]
0xB0DC78  push    eax
0xB0DC79  lea     ecx, [esp+1B44h+var_1B08]   ; this = &数组槽
0xB0DC7D  call    sub_B41850                  ; ← 数组预留（u32 × A，步进 4）
0xB0DC84  test    ebx, ebx
0xB0DC86  jbe     short loc_B0DCC1
0xB0DC90  mov     eax, [esp+1B3Ch+var_1B2C]   ; 元素地址
0xB0DC94  lea     edx, [esp+1B3Ch+var_1B28]
0xB0DC99  push    edx
0xB0DC9A  call    sub_B02DD0                  ; ← 读 1 个 u32（enable_worlds[i]）
0xB0DCA6  add     [esp+1B3Ch+var_1B2C], 4     ; ← 元素步进 4
0xB0DCAB  add     edi, 1
0xB0DCAE  cmp     edi, ebx
0xB0DCB0  jb      short loc_B0DC90
```

数组预留器（步进取证）：

```asm
; VA: 0xB41850 .. 0xB4187B
0xB41856  push    esi
0xB4185B  mov     [eax+4], esi            ; 元素个数
0xB41870  add     dword ptr [edx], 4      ; ← 每元素推进 4 字节
0xB41873  add     ecx, 1
0xB41876  cmp     ecx, [eax+4]
0xB41879  jl      short loc_B41870
0xB4187B  retn    8
```

## E3 第 2 组「计数 + 数组」（`B ≤ 52`，**机器草案漏掉的一段**）

```asm
; VA: 0xB0DCC1 .. 0xB0DD36
0xB0DCC1  lea     ecx, [esp+1B3Ch+var_1B28]
0xB0DCC6  lea     edx, [esp+1B40h+var_1AFC]   ; &计数 B
0xB0DCCB  call    sub_B02DD0                  ; ← 读 B（u32）
0xB0DCDB  mov     ebx, [esp+1B3Ch+var_1AFC]
0xB0DCDF  cmp     ebx, 34h                    ; ← 上限检查 52
0xB0DCE2  ja      loc_B0DC51
0xB0DCE8  push    ebx
0xB0DCE9  lea     eax, [esp+1B40h+var_1B20]
0xB0DCED  push    eax
0xB0DCEE  lea     ecx, [esp+1B44h+var_1B14]
0xB0DCF2  call    sub_B41850                  ; ← 数组预留（u32 × B）
0xB0DCF9  test    ebx, ebx
0xB0DCFB  jbe     short loc_B0DD36
0xB0DD05  mov     eax, [esp+1B3Ch+var_1B2C]
0xB0DD09  lea     edx, [esp+1B3Ch+var_1B28]
0xB0DD0E  push    edx
0xB0DD0F  call    sub_B02DD0                  ; ← 读 1 个 u32（enable_pilots[i]）
0xB0DD1B  add     [esp+1B3Ch+var_1B2C], 4     ; ← 元素步进 4
0xB0DD20  add     edi, 1
0xB0DD23  cmp     edi, ebx
0xB0DD25  jb      short loc_B0DD05
```

## E4 尾字段：`result`（u32）

```asm
; VA: 0xB0DD36 .. 0xB0DD56
0xB0DD36  lea     ecx, [esp+1B3Ch+var_1B20]
0xB0DD3A  push    ecx
0xB0DD3B  lea     ecx, [esp+1B40h+var_1B2C]
0xB0DD3F  call    sub_B41470                  ; 预留 4B（非字段）
0xB0DD4E  call    sub_B02DD0                  ; ← 读 result（u32）
```

## E5 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB0DD73 .. 0xB0DD7D
0xB0DD73  mov     ecx, [esp+1B3Ch+var_1B28]   ; 读完后的游标
0xB0DD77  cmp     ecx, [esp+1B3Ch+var_1B24]   ; vs 报文末尾
0xB0DD7D  jz      short loc_B0DD96            ; ← 不等 ⇒ push 31h 报错
```

## E6 含义取证：3 条日志格式串 + 数组逐元素打印

```asm
; VA: 0xB0DE04 .. 0xB0DEF9
0xB0DE04  push    offset aEnableWorlds       ; ← "enable_worlds={"
0xB0DE12  cmp     [esp+1B3Ch+var_1AF4], 0    ; 循环 A 次（0xB0DE52 cmp ebx,[var_1AF4]）
0xB0DE40  call    sub_41D990
0xB0DE4A  call    sub_B03580                ; 十进制打印元素
0xB0DE5D  push    offset unk_EDABE4          ; "}"
0xB0DE71  push    offset aEnablePilots       ; ← "enable_pilots={"
0xB0DE7F  cmp     [esp+1B3Ch+var_1AFC], 0    ; 循环 B 次（0xB0DEC0 cmp ebx,[var_1AFC]）
0xB0DEE9  push    offset aResult             ; ← "result="
0xB0DEF9  call    sub_B03580
```

## E7 去向：`vt[0xE8]`（5 个实参）

```asm
; VA: 0xB0DF39 .. 0xB0DF6A
0xB0DF39  mov     eax, [esp+1B3Ch+var_1B2C]   ; result 槽
0xB0DF3D  mov     ecx, [eax]
0xB0DF3F  mov     eax, [esp+1B3Ch+var_1B14]   ; enable_pilots 数组基址
0xB0DF43  mov     edx, [esi]
0xB0DF45  mov     edx, [edx+0E8h]             ; ← vt[0xE8]
0xB0DF4B  push    ecx                         ; 实参 5 = result
0xB0DF4C  mov     ecx, [esp+1B40h+var_1AF4]   ; A
0xB0DF50  push    ebx                         ; 实参 4 = B
0xB0DF51  push    eax                         ; 实参 3 = enable_pilots 基址
0xB0DF52  mov     eax, [esp+1B48h+var_1B08]   ; enable_worlds 数组基址
0xB0DF56  push    ecx                         ; 实参 2 = A
0xB0DF57  push    eax                         ; 实参 1 = enable_worlds 基址
0xB0DF58  mov     ecx, esi
0xB0DF5A  call    edx
0xB0DF5C  add     dword ptr [esi+0C10h], 1    ; 本命令接收计数（64 位）
0xB0DF6A  adc     dword ptr [esi+0C14h], 0
```
