# 汇编证据 —— SC-0x049D-battle-wrestle_chase_move_start_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 case 入口 + 解码缓冲申请（容量 `0x14` = 20）

```asm
; VA: 0xB0D48F .. 0xB0D4BE
0xB0D48F  push    12Bh                     ; ← 本 case 错误码
0xB0D494  mov     ecx, esi
0xB0D496  call    sub_B05DA0               ; battle case 入口/开关
0xB0D49B  test    al, al
0xB0D49D  jz      loc_B317C7
0xB0D4A3  mov     ecx, [esi+0Ch]
0xB0D4A6  mov     eax, [ecx]
0xB0D4A8  mov     edx, [eax+78h]           ; vt[0x78] = 申请解码缓冲
0xB0D4AB  push    14h                      ; ← 容量 20（= 负载长）
0xB0D4AD  call    edx
0xB0D4AF  mov     [esp+1B3Ch+var_1B1C], eax ; 缓冲基址（= 缓冲游标起点）
0xB0D4B3  mov     eax, [esi+0Ch]
0xB0D4B6  push    eax
0xB0D4B7  lea     ecx, [esp+1B40h+var_1A38]
0xB0D4BE  call    sub_ABB2F0               ; 初始化 {cur,end} 读游标
```

## E2 八个字段（预留槽 + 有界读取 成对出现）

```asm
; VA: 0xB0D4CC .. 0xB0D61E
; ① ent_id (u16)   槽 var_1AF0
0xB0D4D7  call    sub_B413B0               ; 预留 2B（非字段）
0xB0D4E6  call    sub_B02DF0               ; ← 读 u16
; ② itemid (u32)   槽 var_1AF8
0xB0D517  call    sub_B41470               ; 预留 4B（非字段）
0xB0D526  call    sub_B02DD0               ; ← 读 u32
; ③ dir_h (u16)    槽 var_1AEC
0xB0D53B  call    sub_B413B0
0xB0D54A  call    sub_B02DF0               ; ← 读 u16
; ④ wrestle_id (u32)  槽 var_1B00
0xB0D55F  call    sub_B41470
0xB0D56E  call    sub_B02DD0               ; ← 读 u32
; ⑤ target_ent_id (u16)  槽 var_1B0C
0xB0D587  call    sub_B413B0
0xB0D596  call    sub_B02DF0               ; ← 读 u16
; ⑥ target_pos_x (u16)   槽 var_1B18
0xB0D5AF  call    sub_B413B0
0xB0D5BE  call    sub_B02DF0               ; ← 读 u16
; ⑦ target_pos_y (u16)   槽 var_1B20
0xB0D5D7  call    sub_B413B0
0xB0D5E6  call    sub_B02DF0               ; ← 读 u16
; ⑧ target_pos_z (u16)   槽 var_1B2C
0xB0D5FF  call    sub_B413B0
0xB0D60E  call    sub_B02DF0               ; ← 读 u16
```

宽度判定依据（读原语本体，游标推进量即字段宽度）：

```asm
; VA: 0xB02DF0 .. 0xB02E10   （u16）
0xB02DF6  lea     edx, [ecx+2]             ; ← 需要 2 字节
0xB02E01  mov     cx, [ecx]
0xB02E08  mov     [edx], cx                ; ← 取 2 字节
0xB02E0B  add     dword ptr [eax], 2       ; ← 游标 +2

; VA: 0xB02DD0 .. 0xB02DEE   （u32）
0xB02DD6  lea     edx, [ecx+4]             ; ← 需要 4 字节
0xB02DE1  mov     ecx, [ecx]
0xB02DE7  mov     [edx], ecx               ; ← 取 4 字节
0xB02DE9  add     dword ptr [eax], 4       ; ← 游标 +4
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB0D61E .. 0xB0D628
0xB0D61E  mov     ebx, [esp+1B3Ch+var_1B28]   ; 读完后的游标
0xB0D622  cmp     ebx, [esp+1B3Ch+var_1B24]   ; vs 报文末尾
0xB0D628  jz      short loc_B0D644            ; ← 不等 ⇒ push 12Bh 报错
```

## E4 含义取证：块内 8 条日志格式串（顺序 == 线序）

```asm
; VA: 0xB0D6B5 .. 0xB0D7FD（节选）
0xB0D6BC  push    offset word_F641DC         ; ","
0xB0D6C2  push    offset aEntId              ; ← "ent_id="
0xB0D6EC  push    offset aItemid             ; ← "itemid="
0xB0D717  push    offset aDirH               ; ← "dir_h="
0xB0D741  push    offset aWrestleId          ; ← "wrestle_id="
0xB0D76C  push    offset aTargetEntId        ; ← "target_ent_id="
0xB0D797  push    offset aTargetPosX         ; ← "target_pos_x="
0xB0D7C2  push    offset aTargetPosY         ; ← "target_pos_y="
0xB0D7E8  push    offset aTargetPosZ         ; ← "target_pos_z="
```

## E5 去向：`vt[0x38C]`（8 个实参，压栈顺序 = 逆线序）

```asm
; VA: 0xB0D830 .. 0xB0D888
0xB0D830  mov     eax, [esp+1B3Ch+var_1B2C]   ; 槽 = target_pos_z
0xB0D834  movzx   ecx, word ptr [eax]
0xB0D83B  push    ecx                         ; 实参 8 = target_pos_z
0xB0D83C  movzx   ecx, word ptr [eax]         ; var_1B20 = target_pos_y
0xB0D843  push    ecx                         ; 实参 7
0xB0D844  movzx   ecx, word ptr [eax]         ; var_1B18 = target_pos_x
0xB0D84D  push    ecx                         ; 实参 6
0xB0D84E  movzx   ecx, word ptr [eax]         ; var_1B0C = target_ent_id
0xB0D85B  push    ecx                         ; 实参 5
0xB0D85C  mov     ecx, [eax]                  ; var_1B00 = wrestle_id (u32)
0xB0D862  push    ecx                         ; 实参 4
0xB0D863  movzx   ecx, word ptr [eax]         ; var_1AEC = dir_h
0xB0D86A  push    ecx                         ; 实参 3
0xB0D86B  mov     ecx, [eax]                  ; var_1AF8 = itemid (u32)
0xB0D871  push    ecx                         ; 实参 2
0xB0D872  movzx   ecx, word ptr [eax]         ; var_1AF0 = ent_id
0xB0D875  push    ecx                         ; 实参 1
0xB0D851  mov     edx, [edx+38Ch]             ; ← vt[0x38C]
0xB0D876  mov     ecx, esi
0xB0D878  call    edx
0xB0D87A  add     dword ptr [esi+3AF0h], 1    ; 本命令接收计数（64 位）
0xB0D888  adc     dword ptr [esi+3AF4h], 0
```
