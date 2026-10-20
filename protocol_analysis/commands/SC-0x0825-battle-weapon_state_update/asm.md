# 汇编证据 —— SC-0x0825-battle-weapon_state_update

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 case 入口 + 解码缓冲申请（容量 `6`）

```asm
; VA: 0xB0E1D1 .. 0xB0E1FD
0xB0E1D1  push    73h                      ; ← 本 case 错误码
0xB0E1D3  mov     ecx, esi
0xB0E1D5  call    sub_B05DA0
0xB0E1DA  test    al, al
0xB0E1DC  jz      loc_B317C7
0xB0E1E2  mov     ecx, [esi+0Ch]
0xB0E1E5  mov     edx, [ecx]
0xB0E1E7  mov     eax, [edx+78h]           ; vt[0x78] = 申请解码缓冲
0xB0E1EA  push    6                        ; ← 容量 6（= 负载长）
0xB0E1EC  call    eax
0xB0E1EE  mov     ecx, [esi+0Ch]
0xB0E1F1  push    ecx
0xB0E1F2  lea     ecx, [esp+1B40h+var_18F0]
0xB0E1F9  mov     [esp+1B40h+var_1B2C], eax ; 缓冲基址
0xB0E1FD  call    sub_ABB2F0               ; 初始化 {cur,end} 读游标
```

## E2 三个字段（u16 × 3）

```asm
; VA: 0xB0E202 .. 0xB0E290
0xB0E216  call    sub_B413B0               ; 预留 2B（非字段）
0xB0E225  call    sub_B02DF0               ; ← ent_id（u16，槽 var_1B0C）
0xB0E253  call    sub_B413B0               ; 预留 2B（非字段）
0xB0E262  call    sub_B02DF0               ; ← weapon_state（u16，槽 var_1B18）
0xB0E277  call    sub_B413B0               ; 预留 2B（非字段）
0xB0E286  call    sub_B02DF0               ; ← weapon_change_flag（u16，槽 var_1B20）
```

宽度判定依据（读原语本体）：

```asm
; VA: 0xB02DF0 .. 0xB02E10
0xB02DF6  lea     edx, [ecx+2]             ; ← 需要 2 字节
0xB02E01  mov     cx, [ecx]
0xB02E08  mov     [edx], cx                ; ← 取 2 字节
0xB02E0B  add     dword ptr [eax], 2       ; ← 游标 +2
0xB02E0E  mov     al, 1
0xB02E10  retn
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB0E292 .. 0xB0E29C
0xB0E292  mov     ebx, [esp+1B3Ch+var_1B28]   ; 读完后的游标
0xB0E296  cmp     ebx, [esp+1B3Ch+var_1B24]   ; vs 报文末尾
0xB0E29C  jz      short loc_B0E2B5            ; ← 不等 ⇒ push 73h 报错
```

## E4 含义取证：日志格式串

```asm
; VA: 0xB0E323 .. 0xB0E391
0xB0E32A  push    offset word_F641DC         ; ","
0xB0E330  push    offset aEntId              ; ← "ent_id="
0xB0E340  call    sub_B032A0                ; 十六进制打印器
0xB0E35B  push    offset aWeaponState        ; ← "weapon_state="
0xB0E36B  call    sub_B032A0
0xB0E381  push    offset aWeaponChangeFl     ; ← "weapon_change_flag="
0xB0E391  call    sub_B032A0
```

## E5 去向：`vt[0x1A0]`

```asm
; VA: 0xB0E3C9 .. 0xB0E3FB
0xB0E3C9  mov     ecx, [esp+1B3Ch+var_1B20]   ; 槽 = weapon_change_flag
0xB0E3CD  movzx   edx, word ptr [ecx]
0xB0E3D0  mov     ecx, [esp+1B3Ch+var_1B18]   ; 槽 = weapon_state
0xB0E3D4  mov     eax, [esi]
0xB0E3D6  mov     eax, [eax+1A0h]             ; ← vt[0x1A0]
0xB0E3DC  push    edx                         ; 实参 3 = weapon_change_flag
0xB0E3DD  movzx   edx, word ptr [ecx]
0xB0E3E0  mov     ecx, [esp+1B40h+var_1B0C]   ; 槽 = ent_id
0xB0E3E4  push    edx                         ; 实参 2 = weapon_state
0xB0E3E5  movzx   edx, word ptr [ecx]
0xB0E3E8  push    edx                         ; 实参 1 = ent_id
0xB0E3E9  mov     ecx, esi
0xB0E3EB  call    eax
0xB0E3ED  add     dword ptr [esi+1870h], 1    ; 本命令接收计数（64 位）
0xB0E3FB  adc     dword ptr [esi+1874h], 0
```
