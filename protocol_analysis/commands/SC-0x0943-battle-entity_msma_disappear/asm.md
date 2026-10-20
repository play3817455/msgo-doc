# 汇编证据 —— SC-0x0943-battle-entity_msma_disappear

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 case 入口 + 解码缓冲申请（容量 `8`）

```asm
; VA: 0xB0DFA1 .. 0xB0DFC9
0xB0DFA1  call    sub_B05DA0               ; ← battle case 入口（错误码 0x57 在错误路径）
0xB0DFA6  test    al, al
0xB0DFA8  jz      loc_B317C7
0xB0DFAE  mov     ecx, [esi+0Ch]
0xB0DFB1  mov     eax, [ecx]
0xB0DFB3  mov     edx, [eax+78h]
0xB0DFB6  push    8                        ; ← 容量 8 == 线长
0xB0DFB8  call    edx
0xB0DFBA  mov     [esp+1B3Ch+var_1B2C], eax ; 缓冲游标
0xB0DFBE  mov     eax, [esi+0Ch]
0xB0DFC1  push    eax
0xB0DFC2  lea     ecx, [esp+1B40h+var_1910]
0xB0DFC9  call    sub_ABB2F0               ; 初始化 {cur,end} 读游标
```

## E2 字段 1：`ent_id`（u16，偏移 0）

```asm
; VA: 0xB0DFCE .. 0xB0DFF1
0xB0DFCE  lea     ecx, [esp+1B3Ch+var_1B2C]   ; &缓冲游标
0xB0DFD2  push    ecx
0xB0DFD3  lea     ecx, [esp+1B40h+var_1B0C]   ; 槽
0xB0DFE2  call    sub_B413B0                  ; 缓冲预留 2B（非字段）
0xB0DFE7  mov     eax, [esp+1B3Ch+var_1B0C]
0xB0DFEB  lea     edx, [esp+1B3Ch+var_1B28]   ; &线游标
0xB0DFEF  push    edx
0xB0DFF0  push    eax
0xB0DFF1  call    sub_B02DF0                  ; ← 读 u16
```

## E3 字段 2：`reason`（u32，偏移 2）

```asm
; VA: 0xB0E016 .. 0xB0E02E
0xB0E016  lea     ecx, [esp+1B3Ch+var_1B2C]
0xB0E01A  push    ecx
0xB0E01B  lea     ecx, [esp+1B40h+var_1B18]   ; 槽
0xB0E01F  call    sub_B41470                  ; 缓冲预留 4B（非字段）
0xB0E024  mov     eax, [esp+1B3Ch+var_1B18]
0xB0E028  lea     edx, [esp+1B3Ch+var_1B28]
0xB0E02C  push    edx
0xB0E02D  push    eax
0xB0E02E  call    sub_B02DD0                  ; ← 读 u32
```

## E4 字段 3：`not_use`（u16，偏移 6）

```asm
; VA: 0xB0E03A .. 0xB0E052
0xB0E03A  lea     ecx, [esp+1B3Ch+var_1B2C]
0xB0E03E  push    ecx
0xB0E03F  lea     ecx, [esp+1B40h+var_1B20]   ; 槽
0xB0E043  call    sub_B413B0                  ; 缓冲预留 2B（非字段）
0xB0E048  mov     eax, [esp+1B3Ch+var_1B20]
0xB0E04C  lea     edx, [esp+1B3Ch+var_1B28]
0xB0E050  push    edx
0xB0E051  push    eax
0xB0E052  call    sub_B02DF0                  ; ← 读 u16
```

## E5 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB0E05E .. 0xB0E068
0xB0E05E  mov     ebx, [esp+1B3Ch+var_1B28]   ; 读完后的游标
0xB0E062  cmp     ebx, [esp+1B3Ch+var_1B24]   ; vs 报文末尾
0xB0E066  mov     ecx, esi
0xB0E068  jz      short loc_B0E081            ; ← 不等 ⇒ push 57h 报错
```

## E6 含义取证：块内日志格式串

```asm
; VA: 0xB0E0EF .. 0xB0E15C
0xB0E0EF  mov     eax, [esp+1B3Ch+var_1B0C]
0xB0E0F3  movzx   ecx, word ptr [eax]         ; ent_id（零扩展）
0xB0E0FC  push    offset aEntId               ; ← "ent_id="
0xB0E10C  call    sub_B032A0                  ; 十六进制打印器
0xB0E126  push    offset aReason              ; ← "reason="
0xB0E136  call    sub_B03580                  ; 十进制打印器
0xB0E14C  push    offset aNotUse              ; ← "not_use="
0xB0E15C  call    sub_B032A0                  ; 十六进制打印器
```

## E7 去向：`vt[0x15C]`（ent_id, reason, not_use）

```asm
; VA: 0xB0E194 .. 0xB0E1B5
0xB0E194  mov     ecx, [esp+1B3Ch+var_1B20]   ; not_use 槽
0xB0E198  movzx   edx, word ptr [ecx]
0xB0E19B  mov     ecx, [esp+1B3Ch+var_1B18]   ; reason 槽
0xB0E19F  mov     eax, [esi]
0xB0E1A1  mov     eax, [eax+15Ch]             ; ← vt[0x15C]
0xB0E1A7  push    edx                         ; 实参 3 = not_use
0xB0E1A8  mov     edx, [ecx]                  ; reason
0xB0E1AA  mov     ecx, [esp+1B40h+var_1B0C]   ; ent_id 槽
0xB0E1AE  push    edx                         ; 实参 2 = reason
0xB0E1AF  movzx   edx, word ptr [ecx]
0xB0E1B2  push    edx                         ; 实参 1 = ent_id
0xB0E1B3  mov     ecx, esi
0xB0E1B5  call    eax
0xB0E1B7  add     dword ptr [esi+1330h], 1    ; 本命令接收计数（64 位）
0xB0E1C5  adc     dword ptr [esi+1334h], 0
```
