# 汇编证据 —— SC-0x0906-lounge-player_navi_get_list_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 case 入口 + 解码缓冲申请（容量 `0xC4` = 196）

```asm
; VA: 0xB54919 .. 0xB5494B
0xB54919  push    247h                     ; ← 本 case 错误码
0xB5491E  mov     ecx, esi
0xB54920  call    sub_B41120
0xB54925  test    al, al
0xB54927  jz      loc_B890FE
0xB5492D  mov     ecx, [esi+0Ch]
0xB54930  mov     eax, [ecx]
0xB54932  mov     edx, [eax+78h]
0xB54935  push    0C4h                     ; ← 容量 196 = 4 + 8*24
0xB5493A  call    edx
0xB5493C  mov     [esp+2C5Ch+var_2C3C], eax ; 缓冲游标
0xB54940  mov     eax, [esi+0Ch]
0xB54943  push    eax
0xB54944  lea     ecx, [esp+2C60h+var_281C]
0xB5494B  call    sub_ABB2F0               ; 初始化 {cur,end} 读游标
```

## E2 字段 1：`count`（u32，上限 24）

```asm
; VA: 0xB54950 .. 0xB54994
0xB54950  lea     ecx, [esp+2C5Ch+var_2C44]   ; &线游标
0xB54954  push    ecx
0xB54955  lea     edx, [esp+2C60h+var_2C38]   ; &槽
0xB54959  push    edx
0xB54965  call    sub_B02DD0                  ; ← 读 u32
0xB5496A  add     esp, 8
0xB5496D  test    al, al
0xB5496F  jnz     short loc_B5498D            ; 成功分支
0xB5498D  mov     ebx, [esp+2C5Ch+var_2C38]   ; ebx = count
0xB54991  cmp     ebx, 18h                    ; ← 上限 24
0xB54994  ja      short loc_B54971            ; 越界 ⇒ push 247h 报错
```

## E3 字段 2：数组预留（`sub_B41690`，槽步进 8）

```asm
; VA: 0xB54996 .. 0xB549AF
0xB54996  push    ebx                         ; N = count
0xB54997  lea     eax, [esp+2C60h+var_2C3C]   ; 缓冲游标
0xB5499B  push    eax
0xB5499C  lea     ecx, [esp+2C64h+var_2C18]   ; 出参 {基址, N}
0xB549A0  call    sub_B41690                  ; ← 定长数组预留（8 字节/元素）
; sub_B41690 @0xB41690：0xB416B0 add [edx],8 ⇒ 槽步进 8
0xB549A7  test    ebx, ebx
0xB549A9  jbe     short loc_B549E7            ; N==0 ⇒ 直接闭合
0xB549AB  mov     ecx, [esp+2C5Ch+var_2C18]
0xB549AF  mov     [esp+2C5Ch+var_2C48], ecx   ; 元素指针 = 数组基址
```

## E4 字段 2：元素循环读取（复合读取器 `sub_B434B0`）+ 步进 8

```asm
; VA: 0xB549B3 .. 0xB549D3
0xB549B3  mov     eax, [esp+2C5Ch+var_2C48]   ; 当前元素指针
0xB549B7  lea     edx, [esp+2C5Ch+var_2C44]   ; &线游标
0xB549BB  push    edx
0xB549BC  push    eax
0xB549BD  call    sub_B434B0                  ; ← 复合读取器：消费 8B（2×u32）
0xB549C2  add     esp, 8
0xB549C5  test    al, al
0xB549C7  jz      short loc_B549D7
0xB549C9  add     [esp+2C5Ch+var_2C48], 8     ; ← 元素步进 = 8（线长）
0xB549CE  add     edi, 1
0xB549D1  cmp     edi, ebx
0xB549D3  jb      short loc_B549B3
```

## E5 复合读取器 `sub_B434B0` 整函数（`0xB434B0..0xB434E3`）

```asm
; VA: 0xB434B0 .. 0xB434E3
0xB434B0  mov     eax, [esp+arg_4]            ; &线游标
0xB434B4  mov     ecx, [eax]
0xB434B6  lea     edx, [ecx+4]
0xB434B9  cmp     edx, [eax+4]                ; 边界检查（成员 1）
0xB434BC  ja      short loc_B434E0
0xB434BE  mov     ecx, [ecx]                  ; ← 成员 1 = navi_id（u32）
0xB434C0  mov     edx, [esp+arg_0]            ; dst
0xB434C4  mov     [edx], ecx
0xB434C6  add     dword ptr [eax], 4          ; 游标 +4
0xB434C9  mov     ecx, [eax]
0xB434CB  push    esi
0xB434CC  lea     esi, [ecx+4]
0xB434CF  cmp     esi, [eax+4]                ; 边界检查（成员 2）
0xB434D2  pop     esi
0xB434D3  ja      short loc_B434E0
0xB434D5  mov     ecx, [ecx]                  ; ← 成员 2 = status（u32）
0xB434D7  mov     [edx+4], ecx
0xB434DA  add     dword ptr [eax], 4          ; 游标 +4
0xB434DD  mov     al, 1
0xB434DF  retn
0xB434E0  xor     al, al
0xB434E2  retn
```

## E6 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB549E7 .. 0xB549F1
0xB549E7  mov     ecx, [esp+2C5Ch+var_2C44]   ; 读完后的游标
0xB549EB  cmp     ecx, [esp+2C5Ch+var_2C40]   ; vs 报文末尾
0xB549EF  mov     ecx, esi
0xB549F1  jz      short loc_B54A0D            ; ← 不等 ⇒ push 247h 报错
```

## E7 含义取证：块内日志串 + 元素打印器

```asm
; VA: 0xB54A7E .. 0xB54AA3
0xB54A7E  push    offset aPlayerNaviList      ; ← "player_navi_list={"
0xB54A96  call    sub_B49C80                  ; ← 元素打印器（第 1 个元素）
0xB54AB6  push    offset word_F641DC          ; ","
0xB54AC5  call    sub_B49C80                  ; 后续元素（每元素步进 8：0xB54ACD add ebx,8）

; --- 元素打印器 sub_B49C80 @0xB49C80 . VA: 0xB49C95 .. 0xB49CE2
0xB49C95  mov     eax, [edi]                  ; 成员 1
0xB49CA0  push    offset aNaviId              ; ← "navi_id="
0xB49CBB  mov     ecx, [edi+4]                ; 成员 2
0xB49CC2  push    offset aStatus              ; ← "status="
0xB49CE9  retn
```

## E8 去向：`vt[0x57C]`（数组基址 + 计数）

```asm
; VA: 0xB54B1C .. 0xB54B30
0xB54B1C  mov     ebx, [esp+2C5Ch+var_2C38]   ; count
0xB54B20  mov     edx, [esi]
0xB54B22  mov     eax, [esp+2C5Ch+var_2C18]   ; 数组基址
0xB54B26  mov     edx, [edx+57Ch]             ; ← vt[0x57C]
0xB54B2C  push    ebx                         ; 实参 2 = count
0xB54B2D  push    eax                         ; 实参 1 = 数组基址
0xB54B2E  mov     ecx, esi
0xB54B30  call    edx
0xB54B32  add     dword ptr [esi+72A8h], 1    ; 本命令接收计数（64 位）
0xB54B40  adc     dword ptr [esi+72ACh], 0
```
