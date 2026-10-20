# 汇编证据 —— SC-0x0BCE-battle-score_update_coopwave

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 case 入口 + 解码缓冲申请（容量 `0x16` = 22）

```asm
; VA: 0xB0E879 .. 0xB0E8A8
0xB0E879  push    0ADh                     ; ← 本 case 错误码
0xB0E87E  mov     ecx, esi
0xB0E880  call    sub_B05DA0
0xB0E885  test    al, al
0xB0E887  jz      loc_B317C7
0xB0E88D  mov     ecx, [esi+0Ch]
0xB0E890  mov     eax, [ecx]
0xB0E892  mov     edx, [eax+78h]
0xB0E895  push    16h                      ; ← 容量 22 == 线长
0xB0E897  call    edx
0xB0E899  mov     [esp+1B3Ch+var_1AF4], eax ; 缓冲游标
0xB0E89D  mov     eax, [esi+0Ch]
0xB0E8A0  push    eax
0xB0E8A1  lea     ecx, [esp+1B40h+var_1A20]
0xB0E8A8  call    sub_ABB2F0               ; 初始化 {cur,end} 读游标
```

## E2 字段 1..7：读取序列（u32/u16 交错，按线序）

```asm
; VA: 0xB0E8C1 .. 0xB0E9D0（每字段 = 预留 + bounded 读取器，只计读取器一次）
0xB0E8D0  call    sub_B02DD0               ; 字段 1 reason          u32（偏移 0）
0xB0E910  call    sub_B02DD0               ; 字段 2 world_id        u32（偏移 4）
0xB0E934  call    sub_B02DD0               ; 字段 3 pilot_id        u32（偏移 8）
0xB0E958  call    sub_B02DF0               ; 字段 4 point_gain      u16（偏移 12）
0xB0E980  call    sub_B02DD0               ; 字段 5 point_total     u32（偏移 14）
0xB0E9A8  call    sub_B02DF0               ; 字段 6 n_cont_kill     u16（偏移 18）
0xB0E9D0  call    sub_B02DF0               ; 字段 7 bonus_cont_kill u16（偏移 20）
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB0E9E0 .. 0xB0E9EA
0xB0E9E0  mov     ebx, [esp+1B3Ch+var_1B28]   ; 读完后的游标
0xB0E9E4  cmp     ebx, [esp+1B3Ch+var_1B24]   ; vs 报文末尾
0xB0E9E8  mov     ecx, esi
0xB0E9EA  jz      short loc_B0EA06            ; ← 不等 ⇒ push 0ADh 报错
```

## E4 含义取证：块内日志格式串（7 个字段各有 `xxx=`）

```asm
; VA: 0xB0EA77 .. 0xB0EB8D
0xB0EA83  push    offset aReason              ; ← "reason="            （十进制）
0xB0EAAD  push    offset aWorldId             ; ← "world_id="
0xB0EAD7  push    offset aPilotId             ; ← "pilot_id="
0xB0EB02  push    offset aPointGain           ; ← "point_gain="        （十六进制）
0xB0EB2C  push    offset aPointTotal          ; ← "point_total="       （十进制）
0xB0EB57  push    offset aNContKill           ; ← "n_cont_kill="       （十六进制）
0xB0EB7D  push    offset aBonusContKill       ; ← "bonus_cont_kill="   （十六进制）
0xB0EB12  call    sub_B032A0                  ; 十六进制打印器
0xB0EB3C  call    sub_B03580                  ; 十进制打印器
```

## E5 去向：`vt[0x228]`（7 个实参）

```asm
; VA: 0xB0EBC5 .. 0xB0EC03
0xB0EBC9  movzx   ecx, word ptr [eax]         ; bonus_cont_kill
0xB0EBD0  push    ecx                         ; 实参 7 = bonus_cont_kill
0xB0EBD1  movzx   ecx, word ptr [eax]         ; n_cont_kill
0xB0EBDA  mov     edx, [edx+228h]             ; ← vt[0x228]
0xB0EBE0  push    ecx                         ; 实参 6 = n_cont_kill
0xB0EBE1  mov     ecx, [eax]                  ; point_total
0xB0EBE7  push    ecx                         ; 实参 5 = point_total
0xB0EBE8  movzx   ecx, word ptr [eax]         ; point_gain
0xB0EBEF  push    ecx                         ; 实参 4 = point_gain
0xB0EBF6  push    ecx                         ; 实参 3 = pilot_id
0xB0EBFD  push    ecx                         ; 实参 2 = world_id
0xB0EC00  push    ecx                         ; 实参 1 = reason
0xB0EC01  mov     ecx, esi
0xB0EC03  call    edx
0xB0EC05  add     dword ptr [esi+2350h], 1    ; 本命令接收计数（64 位）
0xB0EC13  adc     dword ptr [esi+2354h], 0
```
