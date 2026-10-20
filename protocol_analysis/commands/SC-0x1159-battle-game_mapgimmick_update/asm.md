# 汇编证据 —— SC-0x1159-battle-game_mapgimmick_update

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 case 入口 + 解码缓冲申请（容量 `0x404`）

```asm
; VA: 0xB0EEFE .. 0xB0EF2D
0xB0EEFE  push    42h                      ; ← 本 case 错误码
0xB0EF00  mov     ecx, esi
0xB0EF02  call    sub_B05DA0               ; case 起始守卫（不读线）
0xB0EF07  test    al, al
0xB0EF09  jz      loc_B317C7
0xB0EF0F  mov     ecx, [esi+0Ch]
0xB0EF12  mov     eax, [ecx]
0xB0EF14  mov     edx, [eax+78h]
0xB0EF17  push    404h                     ; ← 容量 0x404 = 1028 = 4 + 32×32
0xB0EF1C  call    edx
0xB0EF1E  mov     [esp+1B3Ch+var_1B14], eax
0xB0EF22  mov     eax, [esi+0Ch]
0xB0EF25  push    eax
0xB0EF26  lea     ecx, [esp+1B40h+var_1838]
0xB0EF2D  call    sub_ABB2F0               ; 初始化线游标 {cur,end}
```

## E2 字段 1：`count`（u32，偏移 0）+ 上限检查 `≤ 0x20`

```asm
; VA: 0xB0EF32 .. 0xB0EF73
0xB0EF32  lea     ecx, [esp+1B3Ch+var_1B28] ; &线游标
0xB0EF36  push    ecx
0xB0EF37  lea     edx, [esp+1B40h+var_1B20] ; 槽
0xB0EF3B  push    edx
0xB0EF47  call    sub_B02DD0               ; ← 读 u32（计数）
0xB0EF4C  add     esp, 8
0xB0EF4F  test    al, al
0xB0EF51  jnz     short loc_B0EF6C         ; 成功分支
0xB0EF6C  mov     ebx, [esp+1B3Ch+var_1B20]
0xB0EF70  cmp     ebx, 20h                 ; ← 计数上限 32
0xB0EF73  ja      short loc_B0EF53         ; > 32 ⇒ 报错
```

## E3 字段 2：数组预留 `sub_B05FC0`（步进 `0x20 = 32`，非字段）

```asm
; VA: 0xB0EF75 .. 0xB0EF88
0xB0EF75  push    ebx                      ; 元素个数 N
0xB0EF76  lea     eax, [esp+1B40h+var_1B14] ; 解码缓冲游标
0xB0EF7A  push    eax
0xB0EF7B  lea     ecx, [esp+1B44h+var_1B08] ; 输出：数组基址
0xB0EF7F  call    sub_B05FC0               ; 预留 N×32 字节（推进缓冲游标，不是字段）
0xB0EF84  xor     edi, edi
0xB0EF86  test    ebx, ebx
0xB0EF88  jbe     short loc_B0EFC3         ; N == 0 ⇒ 无数组字节
```

```asm
; sub_B05FC0 函数体（0xB05FC0 .. 0xB05FEE）
0xB05FC0  mov     edx, [esp+arg_0]
0xB05FC4  mov     eax, ecx
0xB05FC7  mov     esi, [esp+4+arg_4]       ; N
0xB05FCB  mov     [eax+4], esi             ; out[4] = N
0xB05FCE  mov     ecx, [edx]
0xB05FD0  mov     [eax], ecx               ; out[0] = 基址
0xB05FD2  xor     ecx, ecx
0xB05FD7  jle     short locret_B05FEB
0xB05FE0  add     dword ptr [edx], 20h     ; ← 每元素步进 0x20 = 32
0xB05FE6  cmp     ecx, [eax+4]
0xB05FE9  jl      short loc_B05FE0
```

## E4 字段 2 的元素读取循环（N 次 × `sub_B07DB0`，缓冲步进 `0x20`）

```asm
; VA: 0xB0EF8A .. 0xB0EFC3
0xB0EF8A  mov     ecx, [esp+1B3Ch+var_1B08] ; 数组基址
0xB0EF8E  mov     [esp+1B3Ch+var_1B2C], ecx
0xB0EF92  mov     eax, [esp+1B3Ch+var_1B2C]
0xB0EF96  lea     edx, [esp+1B3Ch+var_1B28] ; &线游标
0xB0EF9A  push    edx
0xB0EF9B  push    eax
0xB0EF9C  call    sub_B07DB0               ; ← 复合元素读取器（消费 7B）
0xB0EFA1  add     esp, 8
0xB0EFA4  test    al, al
0xB0EFA6  jz      short loc_B0EFB6         ; 失败 ⇒ 报错
0xB0EFA8  add     [esp+1B3Ch+var_1B2C], 20h ; ← 缓冲步进 32（结构体跨度 ≠ 线长 7）
0xB0EFAD  add     edi, 1
0xB0EFB0  cmp     edi, ebx
0xB0EFB2  jb      short loc_B0EF92
```

```asm
; sub_B07DB0 整函数（0xB07DB0 .. 0xB07DFB）：元素线长 = 4 + 1 + 2 = 7
0xB07DB0  mov     eax, [esp+arg_4]         ; &线游标
0xB07DB4  mov     ecx, [eax]
0xB07DB6  lea     edx, [ecx+4]
0xB07DB9  cmp     edx, [eax+4]
0xB07DBC  ja      short loc_B07DF4
0xB07DBE  mov     ecx, [ecx]               ; ← u32 @ elem+0
0xB07DC0  mov     edx, [esp+arg_0]
0xB07DC4  mov     [edx], ecx
0xB07DC6  add     dword ptr [eax], 4       ; 游标 +4
0xB07DC9  mov     ecx, [eax]
0xB07DCC  lea     esi, [ecx+1]
0xB07DCF  cmp     esi, [eax+4]
0xB07DD2  ja      short loc_B07DF7
0xB07DD4  mov     cl, [ecx]                ; ← 1 字节 @ elem+4
0xB07DD6  mov     [edx+4], cl
0xB07DD9  add     dword ptr [eax], 1       ; 游标 +1
0xB07DDC  mov     ecx, [eax]
0xB07DDE  lea     esi, [ecx+2]
0xB07DE1  cmp     esi, [eax+4]
0xB07DE4  ja      short loc_B07DF7
0xB07DE6  mov     cx, [ecx]                ; ← 2 字节 @ elem+6
0xB07DE9  mov     [edx+6], cx
0xB07DED  add     dword ptr [eax], 2       ; 游标 +2
0xB07DF0  mov     al, 1
0xB07DF3  retn
```

## E5 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB0EFC3 .. 0xB0EFCF
0xB0EFC3  mov     ecx, [esp+1B3Ch+var_1B28] ; 读完后的线游标
0xB0EFC7  cmp     ecx, [esp+1B3Ch+var_1B24] ; vs 报文末尾
0xB0EFCD  jz      short loc_B0EFE6          ; ← 不等 ⇒ push 42h 报错
```

## E6 含义取证：块内日志 `gimmick_progress={` + 元素打印器

```asm
; VA: 0xB0F054 .. 0xB0F0B8
0xB0F054  push    offset aGimmickProgres    ; ← "gimmick_progress={"
0xB0F05A  call    sub_41D990
0xB0F066  mov     eax, [esp+1B3Ch+var_1B08] ; 数组基址
0xB0F06C  call    sub_B0B280                ; ← 元素打印器（元素 0）
0xB0F079  mov     ebx, [esp+1B3Ch+var_1B08]
0xB0F081  add     ebx, 20h                  ; ← 元素内存步进 32
0xB0F090  push    ebx
0xB0F091  push    offset word_F641DC         ; ","
0xB0F0A0  call    sub_B0B280                ; 其余 N-1 个元素
0xB0F0A8  add     ebx, 20h
0xB0F0B0  jnz     short loc_B0F090
0xB0F0B2  push    offset unk_EDABE4         ; "}"
```

```asm
; 元素打印器 sub_B0B280（0xB0B280 .. 0xB0B313）—— 元素成员名 + 内存偏移
0xB0B295  mov     eax, [edi]                ; [elem+0]
0xB0B2A0  push    offset aGaugeNow          ; ← "gauge_now="
0xB0B2BB  movsx   ecx, byte ptr [edi+4]     ; [elem+4]，符号扩展 ⇒ 语义为 i8
0xB0B2C8  push    offset aStat              ; ← "stat="
0xB0B2E3  movzx   edx, word ptr [edi+6]     ; [elem+6]，2 字节
0xB0B2EB  push    offset aAccessEntId       ; ← "access_ent_id="
```

## E7 去向：`vt[0x11C](gimmick_progress 数组, count)`

```asm
; VA: 0xB0F0F7 .. 0xB0F10D
0xB0F0F7  mov     ebx, [esp+1B3Ch+var_1B20] ; count
0xB0F0FB  mov     edx, [esi]
0xB0F0FD  mov     eax, [esp+1B3Ch+var_1B08] ; 数组基址
0xB0F101  mov     edx, [edx+11Ch]           ; ← vt[0x11C]
0xB0F107  push    ebx                       ; 实参 2 = count
0xB0F108  push    eax                       ; 实参 1 = 数组基址
0xB0F109  mov     ecx, esi
0xB0F10B  call    edx
0xB0F10D  add     dword ptr [esi+0F40h], 1   ; 本命令接收计数（64 位）
0xB0F11B  adc     dword ptr [esi+0F44h], 0
```
