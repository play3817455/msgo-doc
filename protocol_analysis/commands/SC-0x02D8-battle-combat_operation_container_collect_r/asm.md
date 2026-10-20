# 汇编证据 —— SC-0x02D8-battle-combat_operation_container_collect_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 case 入口 + 解码缓冲申请（容量 6）

```asm
; VA: 0xB0D137 .. 0xB0D166
0xB0D137  push    0F4h                     ; ← 本 case 开关/错误码
0xB0D13C  mov     ecx, esi
0xB0D13E  call    sub_B05DA0
0xB0D143  test    al, al
0xB0D145  jz      loc_B317C7
0xB0D14B  mov     ecx, [esi+0Ch]
0xB0D14E  mov     eax, [ecx]
0xB0D150  mov     edx, [eax+78h]
0xB0D153  push    6                        ; ← 容量 6（旁证，不是线长）
0xB0D155  call    edx
0xB0D157  mov     [esp+1B3Ch+var_1B14], eax
0xB0D15B  mov     eax, [esi+0Ch]
0xB0D15E  push    eax
0xB0D15F  lea     ecx, [esp+1B40h+var_18A0]
0xB0D166  call    sub_ABB2F0
```

## E2 字段 1：预留 u16 槽（非字段）+ `sub_B02DF0` 读 u16（负载 +0）

```asm
; VA: 0xB0D16B .. 0xB0D193
0xB0D16B  lea     ecx, [esp+1B3Ch+var_1B14]
0xB0D16F  push    ecx
0xB0D170  lea     ecx, [esp+1B40h+var_1B20]   ; 槽
0xB0D174  mov     [esp+1B40h+var_4], 13Bh
0xB0D17F  call    sub_B413B0               ; 预留 2 字节槽（非字段）
0xB0D184  mov     eax, [esp+1B3Ch+var_1B20]
0xB0D188  lea     edx, [esp+1B3Ch+var_1B28]   ; 游标结构
0xB0D18C  push    edx
0xB0D18D  push    eax
0xB0D18E  call    sub_B02DF0               ; ← 读 u16（ent_id）
0xB0D193  add     esp, 8
```

预留函数本体 + `sub_B02DF0` 本体（读 **u16**，游标 +2）：

```asm
; VA: 0xB413B0 .. 0xB413BD
0xB413B0  mov     eax, ecx
0xB413B2  mov     ecx, [esp+arg_0]
0xB413B6  mov     edx, [ecx]
0xB413B8  mov     [eax], edx
0xB413BA  add     dword ptr [ecx], 2
0xB413BD  retn    4

; VA: 0xB02DF0 .. 0xB02E10
0xB02DF0  mov     eax, [esp+arg_4]
0xB02DF4  mov     ecx, [eax]
0xB02DF6  lea     edx, [ecx+2]
0xB02DF9  cmp     edx, [eax+4]
0xB02DFC  jbe     short loc_B02E01
0xB02DFE  xor     al, al
0xB02E00  retn
0xB02E01  mov     cx, [ecx]                ; ← 读 u16（word）
0xB02E04  mov     edx, [esp+arg_0]
0xB02E08  mov     [edx], cx
0xB02E0B  add     dword ptr [eax], 2        ; ← 游标 +2 ⇒ 宽度 2
0xB02E0E  mov     al, 1
0xB02E10  retn
```

## E3 字段 2：预留 u32 槽（非字段）+ `sub_B02DD0` 读 u32（负载 +2）

```asm
; VA: 0xB0D1B6 .. 0xB0D1D3
0xB0D1B6  lea     ecx, [esp+1B3Ch+var_1B14]
0xB0D1BA  push    ecx
0xB0D1BB  lea     ecx, [esp+1B40h+var_1B2C]   ; 槽
0xB0D1BF  call    sub_B41470               ; 预留 4 字节槽（非字段）
0xB0D1C4  mov     eax, [esp+1B3Ch+var_1B2C]
0xB0D1C8  lea     edx, [esp+1B3Ch+var_1B28]
0xB0D1CC  push    edx
0xB0D1CD  push    eax
0xB0D1CE  call    sub_B02DD0               ; ← 读 u32（result）
0xB0D1D3  add     esp, 8
```

`sub_B02DD0` 本体（读 **u32**，游标 +4）见 `../SC-0x00C7-lounge-msma_trialms_back_r/asm.md` E2。

## E4 长度闭合（负载恰好 6 字节：2 + 4）

```asm
; VA: 0xB0D1DA .. 0xB0D1E4
0xB0D1DA  mov     ebx, [esp+1B3Ch+var_1B28]   ; 读完后的游标
0xB0D1DE  cmp     ebx, [esp+1B3Ch+var_1B24]   ; vs 报文末尾
0xB0D1E2  mov     ecx, esi
0xB0D1E4  jz      short loc_B0D200            ; ← 不等则 push 0F4h 报错
```

## E5 含义取证：块内日志格式串

```asm
; VA: 0xB0D271 .. 0xB0D2A3
0xB0D271  mov     eax, [esp+1B3Ch+var_1B20]   ; u16 槽
0xB0D275  movzx   ecx, word ptr [eax]
0xB0D27E  push    offset aEntId               ; ← "ent_id="
...
0xB0D299  mov     edx, [esp+1B44h+var_1B2C]   ; u32 槽
0xB0D29D  mov     eax, [edx]
0xB0D2A3  push    offset aResult              ; ← "result="
0xB0D2B3  call    sub_B03580
```

## E6 去向：`vt[0x2F4](u16 ent_id, u32 result)`

```asm
; VA: 0xB0D2EB .. 0xB0D306
0xB0D2EB  mov     eax, [esp+1B3Ch+var_1B2C]   ; u32 槽
0xB0D2EF  mov     ecx, [eax]
0xB0D2F1  mov     eax, [esp+1B3Ch+var_1B20]   ; u16 槽
0xB0D2F5  mov     edx, [esi]
0xB0D2F7  mov     edx, [edx+2F4h]            ; ← vt[0x2F4]
0xB0D2FD  push    ecx
0xB0D2FE  movzx   ecx, word ptr [eax]
0xB0D301  push    ecx
0xB0D302  mov     ecx, esi
0xB0D304  call    edx                        ; vt[0x2F4](ent_id, result)
0xB0D306  add     dword ptr [esi+30A0h], 1
```
