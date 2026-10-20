# 汇编证据 —— SC-0x0D24-lounge-pilot_bot_checkcode_request

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 case 入口 + 解码缓冲申请（容量 `0xD`）

```asm
; VA: 0xB550B7 .. 0xB550E5
0xB550B7  push    3Ch                      ; ← 本 case 错误码
0xB550B9  mov     ecx, esi
0xB550BB  call    sub_B41120
0xB550C0  test    al, al
0xB550C2  jz      loc_B890FE
0xB550C8  mov     ecx, [esi+0Ch]
0xB550CB  mov     eax, [ecx]
0xB550CD  mov     edx, [eax+78h]
0xB550D0  push    0Dh                      ; ← 容量 0xD == 串槽预算
0xB550D2  call    edx
0xB550D4  mov     edi, eax                 ; 缓冲首址（稍后作为字段去向实参）
0xB550D6  mov     eax, [esi+0Ch]
0xB550D9  push    eax
0xB550DA  lea     ecx, [esp+2C60h+var_2670]
0xB550E1  mov     [esp+2C60h+var_2C3C], edi
0xB550E5  call    sub_ABB2F0               ; 用传输层缓冲初始化线游标 {cur,end}
```

## E2 字段 1：`code`（NUL 串，偏移 0，预算 13）

```asm
; VA: 0xB550EA .. 0xB55109
0xB550EA  push    0Dh                      ; ← 本字段最大字节数（含 NUL）== 容量
0xB550EC  lea     ecx, [esp+2C60h+var_2C44] ; &线游标
0xB550F0  push    ecx
0xB550F1  push    edi                      ; dst = 缓冲首址
0xB550FD  call    sub_B02BA0               ; ← 读 NUL 串：消费 = strlen+1，≤ maxlen
0xB55102  add     esp, 0Ch
0xB55105  test    al, al
0xB55109  jnz     short loc_B55122         ; 成功分支
```

## E3 长度闭合（游标 == 报文末尾 ⇒ 后面无其它字段）

```asm
; VA: 0xB55122 .. 0xB5512E
0xB55122  mov     ebx, [esp+2C5Ch+var_2C44] ; 读完后的线游标
0xB55126  cmp     ebx, [esp+2C5Ch+var_2C40] ; vs 报文末尾
0xB5512A  jnz     short loc_B5510B         ; ← 不等 ⇒ push 3Ch 报错
0xB5512C  push    3Ch
0xB5512E  call    sub_B41110               ; 取日志对象（非字段）
```

## E4 含义取证：块内日志 `code="`

```asm
; VA: 0xB5519A .. 0xB551BC
0xB5519A  mov     eax, [esp+2C5Ch+var_2C3C] ; 缓冲首址
0xB5519E  push    offset asc_EDAD54         ; "\""
0xB551A3  push    eax
0xB551A4  push    offset aCode              ; ← "code=\""
0xB551A9  push    edi
0xB551AA  call    sub_41D990
```

## E5 去向：`vt[0xF0]`（唯一实参 = 串首地址）

```asm
; VA: 0xB551F7 .. 0xB5520F
0xB551F7  mov     edx, [esi]
0xB551F9  mov     eax, [esp+2C5Ch+var_2C3C] ; = 缓冲首址（NUL 串）
0xB551FD  mov     edx, [edx+0F0h]           ; ← vt[0xF0]
0xB55203  push    eax                       ; 实参 1 = code 串首地址
0xB55204  mov     ecx, esi
0xB55206  call    edx
0xB55208  add     dword ptr [esi+1098h], 1   ; 本命令接收计数（64 位）
0xB55216  adc     dword ptr [esi+109Ch], 0
```

## E6 参照：`sub_B02BA0` 的消费量语义（变长串原语）

```asm
; VA: 0xB02BA0 .. 0xB02BF4（函数体）
0xB02BA0  mov     edx, [esp+arg_8]          ; maxlen
0xB02BA9  mov     ecx, [edi]                ; cur
0xB02BAB  mov     eax, [edi+4]              ; end
0xB02BAE  sub     eax, ecx                  ; 剩余可读
0xB02BB0  cmp     edx, eax
0xB02BB2  jge     short loc_B02BB6
0xB02BB4  mov     eax, edx                  ; eax = min(maxlen, 剩余)
0xB02BB6  test    eax, eax
0xB02BB8  jge     short loc_B02BBE
0xB02BBA  xor     al, al                    ; 剩余为负 ⇒ 失败
0xB02BC3  call    sub_CC8400                ; 在 [cur, cur+eax) 内找 NUL
0xB02BC8  mov     esi, eax
0xB02BCD  test    esi, esi
0xB02BCF  jnz     short loc_B02BD6
0xB02BD1  pop     esi
0xB02BD2  xor     al, al                    ; 未在预算内找到 NUL ⇒ 失败
0xB02BDC  add     esi, 1                    ; 游标 = NUL 地址 + 1
0xB02BE3  push    ecx
0xB02BE4  push    eax
0xB02BE5  push    edx
0xB02BE6  call    sub_CC56B0                ; memcpy(dst, cur, len)
0xB02BEE  mov     [edi], esi                ; ← 线游标 += (串长 + 1)
```
