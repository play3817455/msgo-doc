# 汇编证据 —— SC-0x0B3E-battle-roomlobby_pilot_mindex_update_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 case 入口 + 解码缓冲申请（容量 `0xE` = 14）

```asm
; VA: 0xB0E407 .. 0xB0E433
0xB0E407  push    0Bh                      ; ← 本 case 错误码
0xB0E409  mov     ecx, esi
0xB0E40B  call    sub_B05DA0
0xB0E410  test    al, al
0xB0E412  jz      loc_B317C7
0xB0E418  mov     ecx, [esi+0Ch]
0xB0E41B  mov     edx, [ecx]
0xB0E41D  mov     eax, [edx+78h]
0xB0E420  push    0Eh                      ; ← 容量 14 == 线长
0xB0E422  call    eax
0xB0E424  mov     ecx, [esi+0Ch]
0xB0E427  push    ecx
0xB0E428  lea     ecx, [esp+1B40h+var_19CC]
0xB0E42F  mov     [esp+1B40h+var_1AFC], eax ; 缓冲游标
0xB0E433  call    sub_ABB2F0               ; 初始化 {cur,end} 读游标
```

## E2 字段 1..3：`result` / `world_id` / `pilot_id`（3×u32）

```asm
; VA: 0xB0E438 .. 0xB0E4BC（每字段 = 预留 + bounded 读取器，只计读取器一次）
0xB0E44C  call    sub_B41470               ; 预留 4B（非字段）
0xB0E45B  call    sub_B02DD0               ; ← 字段 1 result   u32（偏移 0）
0xB0E489  call    sub_B41470               ; 预留 4B（非字段）
0xB0E498  call    sub_B02DD0               ; ← 字段 2 world_id u32（偏移 4）
0xB0E4AD  call    sub_B41470               ; 预留 4B（非字段）
0xB0E4BC  call    sub_B02DD0               ; ← 字段 3 pilot_id u32（偏移 8）
```

## E3 字段 4..5：`member_index` / `is_commander`（2×u8）

```asm
; VA: 0xB0E4C8 .. 0xB0E510
0xB0E4D1  call    sub_B05E30               ; 预留 1B（非字段）
0xB0E4E0  call    sub_B06230               ; ← 字段 4 member_index u8（偏移 12）
0xB0E4F9  call    sub_B05E30               ; 预留 1B（非字段）
0xB0E508  call    sub_B06230               ; ← 字段 5 is_commander  u8（偏移 13）
; sub_B06230 内：0xB06249 add dword ptr [eax], 1 ⇒ 游标 +1
```

## E4 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB0E518 .. 0xB0E522
0xB0E518  mov     ebx, [esp+1B3Ch+var_1B28]   ; 读完后的游标
0xB0E51C  cmp     ebx, [esp+1B3Ch+var_1B24]   ; vs 报文末尾
0xB0E520  mov     ecx, esi
0xB0E522  jz      short loc_B0E53B            ; ← 不等 ⇒ push 0Bh 报错
```

## E5 含义取证：块内日志格式串

```asm
; VA: 0xB0E5A9 .. 0xB0E665
0xB0E5B5  push    offset aResult              ; ← "result="
0xB0E5C5  call    sub_B03580                  ; 十进制打印器
0xB0E5DF  push    offset aWorldId             ; ← "world_id="
0xB0E609  push    offset aPilotId             ; ← "pilot_id="
0xB0E631  push    offset aMemberIndex         ; ← "member_index="
0xB0E640  call    sub_B0C1F0                  ; 单字节打印器
0xB0E656  push    offset aIsCommander         ; ← "is_commander="
0xB0E665  call    sub_B0C1F0                  ; 单字节打印器
```

## E6 去向：`vt[0x8C]`（5 个实参，u8 先零扩展）

```asm
; VA: 0xB0E6A0 .. 0xB0E6CF
0xB0E6A0  mov     eax, [esp+1B3Ch+var_1B2C]   ; is_commander 槽
0xB0E6A4  movzx   ecx, byte ptr [eax]         ; 零扩展
0xB0E6A7  mov     eax, [esp+1B3Ch+var_1B20]   ; member_index 槽
0xB0E6AB  mov     edx, [esi]
0xB0E6AD  mov     edx, [edx+8Ch]              ; ← vt[0x8C]
0xB0E6B3  push    ecx                         ; 实参 5 = is_commander
0xB0E6B4  movzx   ecx, byte ptr [eax]
0xB0E6B7  mov     eax, [esp+1B40h+var_1B18]   ; pilot_id 槽
0xB0E6BB  push    ecx                         ; 实参 4 = member_index
0xB0E6BC  mov     ecx, [eax]
0xB0E6BE  mov     eax, [esp+1B44h+var_1B0C]   ; world_id 槽
0xB0E6C2  push    ecx                         ; 实参 3 = pilot_id
0xB0E6C3  mov     ecx, [eax]
0xB0E6C5  mov     eax, [esp+1B48h+var_1B00]   ; result 槽
0xB0E6C9  push    ecx                         ; 实参 2 = world_id
0xB0E6CA  mov     ecx, [eax]
0xB0E6CC  push    ecx                         ; 实参 1 = result
0xB0E6CD  mov     ecx, esi
0xB0E6CF  call    edx
0xB0E6D1  add     dword ptr [esi+4F0h], 1     ; 本命令接收计数（64 位）
0xB0E6DF  adc     dword ptr [esi+4F4h], 0
```
