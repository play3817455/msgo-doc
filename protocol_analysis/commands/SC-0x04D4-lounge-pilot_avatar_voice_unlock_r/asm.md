# 汇编证据 —— SC-0x04D4-lounge-pilot_avatar_voice_unlock_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 case 入口 + 解码缓冲申请（容量 `0x48` = 72）

```asm
; VA: 0xB5327F .. 0xB532AB
0xB5327F  push    31h                      ; ← 本 case 错误码
0xB53281  mov     ecx, esi
0xB53283  call    sub_B41120
0xB53288  test    al, al
0xB5328A  jz      loc_B890FE
0xB53290  mov     ecx, [esi+0Ch]
0xB53293  mov     eax, [ecx]
0xB53295  mov     edx, [eax+78h]           ; vt[0x78] = 申请解码缓冲
0xB53298  push    48h                      ; ← 容量 72（= 负载长）
0xB5329A  call    edx
0xB5329C  mov     [esp+2C5Ch+var_2C48], eax ; 缓冲基址
0xB532A0  mov     eax, [esi+0Ch]
0xB532A3  push    eax
0xB532A4  lea     ecx, [esp+2C60h+var_28BC]
0xB532AB  call    sub_ABB2F0               ; 初始化 {cur,end} 读游标
```

## E2 前两个字段（u32 × 2）

```asm
; VA: 0xB532C9 .. 0xB53318
0xB532C4  call    sub_B41470               ; 预留 4B（非字段）
0xB532D3  call    sub_B02DD0               ; ← result（u32，槽 var_2C34）
0xB53301  call    sub_B41470               ; 预留 4B（非字段）
0xB53310  call    sub_B02DD0               ; ← custom_id（u32，槽 var_2C38）
```

## E3 第 3 字段：定长数组 `hav_voice[8]`（u64 × 8）

```asm
; VA: 0xB5331C .. 0xB5334D
0xB5331C  lea     ecx, [esp+2C5Ch+var_2C48]
0xB53320  push    ecx                      ; arg_0 = &缓冲游标
0xB53321  lea     ecx, [esp+2C60h+var_2C24] ; this = &数组槽
0xB53325  call    sub_B05ED0               ; ← 数组预留：claim 0x40 = 64B
0xB5332A  mov     ebx, [esp+2C5Ch+var_2C24] ; 数组基址
0xB5332E  xor     edi, edi
0xB53330  lea     edx, [esp+2C5Ch+var_2C44]
0xB53334  push    edx                      ; 读游标
0xB53335  push    ebx
0xB53336  call    sub_B06200               ; ← 读 1 个 u64
0xB5333B  add     esp, 8
0xB5333E  test    al, al
0xB53340  jz      short loc_B5334F          ; 失败 ⇒ push 31h 报错
0xB53342  add     edi, 1
0xB53345  add     ebx, 8                   ; ← 元素步进 8
0xB53348  cmp     edi, 8                   ; ← 元素个数硬编码 8
0xB5334B  jb      short loc_B53330
```

数组预留器（claim 量取证）：

```asm
; VA: 0xB05ED0 .. 0xB05EDD
0xB05ED0  mov     eax, ecx
0xB05ED2  mov     ecx, [esp+arg_0]
0xB05ED6  mov     edx, [ecx]
0xB05ED8  mov     [eax], edx
0xB05EDA  add     dword ptr [ecx], 40h     ; ← 数组整体 claim 64 字节
0xB05EDD  retn    4
```

u64 读取器（元素宽度取证）：

```asm
; VA: 0xB06200 .. 0xB06226
0xB06204  mov     ecx, [eax]
0xB06206  lea     edx, [ecx+8]             ; ← 需要 8 字节
0xB06209  cmp     edx, [eax+4]
0xB0620C  jbe     short loc_B06211
0xB0620E  xor     al, al
0xB06210  retn
0xB06211  mov     edx, [esp+arg_0]
0xB06216  mov     esi, [ecx]
0xB06218  mov     [edx], esi               ; ← 低 4 字节
0xB0621A  mov     ecx, [ecx+4]
0xB0621D  mov     [edx+4], ecx             ; ← 高 4 字节
0xB06220  add     dword ptr [eax], 8       ; ← 游标 +8
0xB06223  mov     al, 1
0xB06226  retn
```

## E4 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB5335C .. 0xB53366
0xB5335C  mov     eax, [esp+2C5Ch+var_2C44]   ; 读完后的游标
0xB53360  cmp     eax, [esp+2C5Ch+var_2C40]   ; vs 报文末尾
0xB53366  jz      short loc_B5337F            ; ← 不等 ⇒ push 31h 报错
```

## E5 含义取证：3 条日志格式串

```asm
; VA: 0xB533ED .. 0xB53498（节选）
0xB533F3  push    offset word_F641DC         ; ","
0xB533F9  push    offset aResult             ; ← "result="
0xB53423  push    offset aCustomId           ; ← "custom_id="
0xB5343E  push    offset aHavVoice           ; ← "hav_voice={"
0xB53459  call    sub_B08500                ; u64 十进制打印器（元素 0）
0xB53470  push    offset word_F641DC         ; ","（元素 1..7 循环，0xB5348B cmp ebx,8）
0xB5348D  push    offset unk_EDABE4          ; "}"
```

## E6 去向：`vt[0xD4]`（3 个实参）

```asm
; VA: 0xB534D2 .. 0xB534F1
0xB534D2  mov     ecx, [esp+2C5Ch+var_2C24]   ; hav_voice 数组基址
0xB534D6  mov     edx, [esp+2C5Ch+var_2C38]   ; custom_id 槽
0xB534DA  mov     eax, [esi]
0xB534DC  push    ecx                         ; 实参 3 = 数组基址
0xB534DD  mov     ecx, [edx]
0xB534DF  mov     edx, [esp+2C60h+var_2C34]   ; result 槽
0xB534E3  push    ecx                         ; 实参 2 = custom_id
0xB534E4  mov     ecx, [edx]
0xB534E6  mov     edx, [eax+0D4h]             ; ← vt[0xD4]
0xB534EC  push    ecx                         ; 实参 1 = result
0xB534ED  mov     ecx, esi
0xB534EF  call    edx
0xB534F1  add     dword ptr [esi+0E88h], 1    ; 本命令接收计数（64 位）
0xB53506  adc     dword ptr [esi+0E8Ch], 0
```
