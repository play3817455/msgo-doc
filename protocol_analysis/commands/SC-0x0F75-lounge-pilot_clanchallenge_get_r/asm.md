# 汇编证据 —— SC-0x0F75-lounge-pilot_clanchallenge_get_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 case 入口 + 解码缓冲申请（容量 `0x76`）

```asm
; VA: 0xB5546D .. 0xB55499
0xB5546D  push    76h                      ; ← 本 case 错误码
0xB5546F  mov     ecx, esi
0xB55471  call    sub_B41120
0xB55476  test    al, al
0xB55478  jz      loc_B890FE
0xB5547E  mov     ecx, [esi+0Ch]
0xB55481  mov     edx, [ecx]
0xB55483  mov     eax, [edx+78h]
0xB55486  push    76h                      ; ← 容量 0x76 = 118 = 7×16 + 6
0xB55488  call    eax
0xB5548A  mov     ecx, [esi+0Ch]
0xB5548D  push    ecx
0xB5548E  lea     ecx, [esp+2C60h+var_2AD4]
0xB55495  mov     [esp+2C60h+var_2C2C], eax
0xB55499  call    sub_ABB2F0               ; 初始化线游标 {cur,end}
```

## E2 字段 1：数组预留 `sub_B413F0`（`+0x70 = 7×16`，非字段）

```asm
; VA: 0xB5549E .. 0xB554B7
0xB5549E  lea     edx, [esp+2C5Ch+var_2C2C]
0xB554A2  push    edx                      ; &缓冲游标
0xB554A3  lea     ecx, [esp+2C60h+var_2C08] ; 输出：数组基址
0xB554B2  call    sub_B413F0               ; ← 缓冲游标 += 0x70（112 = 7×16），不带线上计数
0xB554B7  mov     ebx, [esp+2C5Ch+var_2C08]
```

```asm
; sub_B413F0 函数体（0xB413F0 .. 0xB41400）
0xB413F0  mov     eax, ecx                 ; eax = 输出槽
0xB413F2  mov     ecx, [esp+arg_0]
0xB413F6  mov     edx, [ecx]               ; cur
0xB413F8  mov     [eax], edx               ; *out = cur
0xB413FA  add     dword ptr [ecx], 70h     ; ← 固定 112 字节 = 7 × 16
0xB413FD  retn    4
```

## E3 字段 1 的元素读取循环（7 次 × `sub_B44700`，缓冲步进 `0x10`）

```asm
; VA: 0xB554BB .. 0xB554DD
0xB554BB  xor     edi, edi
0xB554C0  lea     eax, [esp+2C5Ch+var_2C44] ; &线游标
0xB554C4  push    eax
0xB554C5  push    ebx                      ; 元素地址
0xB554C6  call    sub_B44700               ; ← 复合元素读取器（消费 9B）
0xB554CB  add     esp, 8
0xB554CE  test    al, al
0xB554D0  jz      short loc_B554DF         ; 失败 ⇒ push 76h 报错
0xB554D2  add     edi, 1
0xB554D5  add     ebx, 10h                 ; ← 缓冲步进 16（结构体跨度，≠ 线长 9）
0xB554D8  cmp     edi, 7                   ; ← 固定 7 个元素
0xB554DB  jb      short loc_B554C0
```

```asm
; sub_B44700 整函数（0xB44700 .. 0xB44749）：元素线长 = 4 + 4 + 1 = 9
0xB44700  mov     eax, [esp+arg_4]         ; &线游标
0xB44704  mov     ecx, [eax]               ; cur
0xB44706  lea     edx, [ecx+4]
0xB44709  cmp     edx, [eax+4]             ; 边界检查
0xB4470C  ja      short loc_B44742
0xB4470E  mov     edx, [ecx]               ; ← u32 @ elem+0
0xB44710  mov     ecx, [esp+arg_0]         ; 元素地址
0xB44714  mov     [ecx], edx
0xB44716  add     dword ptr [eax], 4       ; 游标 +4
0xB44719  mov     edx, [eax]
0xB4471B  push    esi
0xB4471C  lea     esi, [edx+4]
0xB4471F  cmp     esi, [eax+4]
0xB44722  ja      short loc_B44745
0xB44724  mov     edx, [edx]               ; ← u32 @ elem+4
0xB44726  mov     [ecx+4], edx
0xB44729  add     dword ptr [eax], 4       ; 游标 +4
0xB4472C  mov     esi, [eax]
0xB4472E  lea     edx, [esi+1]
0xB44731  cmp     edx, [eax+4]
0xB44734  ja      short loc_B44745
0xB44736  mov     dl, [esi]                ; ← 1 字节 @ elem+8
0xB44738  mov     [ecx+8], dl
0xB4473B  add     dword ptr [eax], 1       ; 游标 +1
0xB4473E  mov     al, 1
0xB44741  retn
```

## E4 字段 2..6：尾部 5 个标量（u8 / u16 / u8 / u8 / u8）

```asm
; VA: 0xB554EC .. 0xB555C1
0xB554F0  lea     ecx, [esp+2C60h+var_2C0C] ; 槽：is_perfect
0xB554F5  call    sub_B05E30               ; 预留 1B（非字段）
0xB55504  call    sub_B06230               ; ← 读 u8（is_perfect）
0xB55529  lea     ecx, [esp+2C60h+var_2C30] ; 槽：year
0xB55532  call    sub_B413B0               ; 预留 2B（非字段）
0xB55541  call    sub_B02DF0               ; ← 读 u16（year）
0xB55552  lea     ecx, [esp+2C60h+var_2C34] ; 槽：month
0xB55556  call    sub_B05E30               ; 预留 1B
0xB55565  call    sub_B06230               ; ← 读 u8（month）
0xB55576  lea     ecx, [esp+2C60h+var_2C38] ; 槽：day
0xB5557A  call    sub_B05E30               ; 预留 1B
0xB55589  call    sub_B06230               ; ← 读 u8（day）
0xB5559E  lea     ecx, [esp+2C60h+var_2C48] ; 槽：clan_forbidden
0xB555A2  call    sub_B05E30               ; 预留 1B
0xB555B1  call    sub_B06230               ; ← 读 u8（clan_forbidden）
0xB555C1  mov     ecx, [esp+2C5Ch+var_2C44] ; 读完后的线游标
0xB555C5  cmp     ecx, [esp+2C5Ch+var_2C40] ; vs 报文末尾
0xB555CB  jz      short loc_B555E4          ; ← 不等 ⇒ push 76h 报错
```

## E5 含义取证：块内日志（`pclanchlg={` + 元素打印器 + 5 个标量）

```asm
; VA: 0xB55652 .. 0xB55776
0xB55652  push    offset aPclanchlg         ; ← "pclanchlg={"
0xB5565D  mov     ebx, [esp+2C64h+var_2C08] ; 数组基址
0xB55663  call    sub_B4BDE0                ; ← 元素打印器（id= / val= / is_clear=）
0xB5566E  mov     [esp+2C5Ch+var_2C3C], 6
0xB55676  push    ebx
0xB55677  push    offset word_F641DC         ; ","
0xB55686  call    sub_B4BDE0                ; 其余 6 个元素
0xB55691  sub     [esp+2C5Ch+var_2C3C], 1   ; 共 1 + 6 = 7 次
0xB5569D  push    offset unk_EDABE4         ; "}"
0xB556BE  push    offset aIsPerfect          ; ← "is_perfect="
0xB556EB  push    offset aYear               ; ← "year="
0xB55713  push    offset aMonth              ; ← "month="
0xB5573D  push    offset aDay                ; ← "day="
0xB55762  push    offset aClanForbidden      ; ← "clan_forbidden="
```

```asm
; 元素打印器 sub_B4BDE0（0xB4BDE0 .. 0xB4BE72）—— 元素成员名 + 内存偏移
0xB4BDF5  mov     eax, [edi]                ; [elem+0]
0xB4BE00  push    offset aId_0              ; ← "id="
0xB4BE1B  mov     ecx, [edi+4]              ; [elem+4]
0xB4BE27  push    offset aVal               ; ← "val="
0xB4BE42  movsx   edx, byte ptr [edi+8]     ; [elem+8]，符号扩展 ⇒ 语义为 i8
0xB4BE4A  push    offset aIsClear           ; ← "is_clear="
```

## E6 去向：`vt[0x174](pclanchlg 数组, is_perfect, year, month, day, clan_forbidden)`

```asm
; VA: 0xB557B0 .. 0xB557E9
0xB557B0  mov     ecx, [esp+2C5Ch+var_2C48] ; clan_forbidden 槽
0xB557B4  movzx   edx, byte ptr [ecx]
0xB557B7  mov     ecx, [esp+2C5Ch+var_2C38] ; day 槽
0xB557BB  mov     eax, [esi]
0xB557BD  push    edx                       ; 实参 6 = clan_forbidden
0xB557BE  movzx   edx, byte ptr [ecx]
0xB557C1  mov     ecx, [esp+2C5Ch+var_2C34] ; month 槽
0xB557C5  push    edx                       ; 实参 5 = day
0xB557C6  movzx   edx, byte ptr [ecx]
0xB557C9  mov     ecx, [esp+2C5Ch+var_2C30] ; year 槽
0xB557CD  push    edx                       ; 实参 4 = month
0xB557CE  movzx   edx, word ptr [ecx]
0xB557D1  mov     ecx, [esp+2C5Ch+var_2C0C] ; is_perfect 槽
0xB557D5  push    edx                       ; 实参 3 = year
0xB557D6  movzx   edx, byte ptr [ecx]
0xB557D9  mov     ecx, [esp+2C5Ch+var_2C08] ; 数组基址
0xB557DD  push    edx                       ; 实参 2 = is_perfect
0xB557DE  mov     edx, [eax+174h]           ; ← vt[0x174]
0xB557E4  push    ecx                       ; 实参 1 = 数组基址
0xB557E5  mov     ecx, esi
0xB557E7  call    edx
0xB557E9  add     dword ptr [esi+1B78h], 1   ; 本命令接收计数（64 位）
0xB557F7  adc     dword ptr [esi+1B7Ch], 0
```
