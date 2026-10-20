# 汇编证据 —— SC-0x0124-lounge-xwar_forcegauge_get_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 case 入口 + 解码缓冲申请（容量 0x90 = 144）

```asm
; VA: 0xB51E9A .. 0xB51ECC
0xB51E9A  push    0A1h                     ; ← 本 case 开关/错误码
0xB51E9F  mov     ecx, esi
0xB51EA1  call    sub_B41120
0xB51EA6  test    al, al
0xB51EA8  jz      loc_B890FE
0xB51EAE  mov     ecx, [esi+0Ch]
0xB51EB1  mov     eax, [ecx]
0xB51EB3  mov     edx, [eax+78h]
0xB51EB6  push    90h                      ; ← 容量 144 = 4+4+65+65+4+2（按定长槽预算）
0xB51EBB  call    edx
0xB51EBD  mov     [esp+2C5Ch+var_2C2C], eax
0xB51EC1  mov     eax, [esi+0Ch]
0xB51EC4  push    eax
0xB51EC5  lea     ecx, [esp+2C60h+var_2B40]
0xB51ECC  call    sub_ABB2F0
```

## E2 字段 1/2：`sub_B02DD0` 读 u32（负载 +0 / +4）

```asm
; VA: 0xB51ED1 .. 0xB51F39   （字段 1 → var_2C00）
0xB51EE5  call    sub_B41470               ; 预留 4 字节槽（非字段）
0xB51EEA  mov     eax, [esp+2C5Ch+var_2C00]
0xB51EF2  push    edx
0xB51EF3  push    eax
0xB51EF4  call    sub_B02DD0               ; ← 读 u32（e_fgauge）
0xB51F39  add     esp, 8

; VA: 0xB51F1C .. 0xB51F39   （字段 2 → var_2C10）
0xB51F25  call    sub_B41470               ; 预留 4 字节槽（非字段）
0xB51F2A  mov     eax, [esp+2C5Ch+var_2C10]
0xB51F32  push    edx
0xB51F33  push    eax
0xB51F34  call    sub_B02DD0               ; ← 读 u32（z_fgauge）
0xB51F39  add     esp, 8
```

`sub_B02DD0` 本体（读 **u32**，游标 +4）见 `../SC-0x00C7-lounge-msma_trialms_back_r/asm.md` E2。

## E3 字段 3/4：`sub_B02BA0` 读 NUL 结尾字符串（变长）

```asm
; VA: 0xB51F40 .. 0xB51F80
0xB51F40  mov     edi, [esp+2C5Ch+var_2C2C]   ; edi = 解码缓冲基址
0xB51F44  mov     eax, edi
0xB51F46  push    41h                      ; ← 槽上限 65
0xB51F48  lea     ecx, [esp+2C60h+var_2C44]   ; 游标结构
0xB51F4C  push    ecx
0xB51F4D  push    eax
0xB51F4E  mov     [esp+2C68h+var_2C20], eax   ; ← 字段 3 槽地址
0xB51F52  add     edi, 41h                 ; 下一个 65 字节槽
0xB51F55  call    sub_B02BA0               ; ← 读字符串 ranking_term_now
0xB51F5A  add     esp, 0Ch
0xB51F5D  test    al, al
0xB51F5F  jz      short loc_B51F00
0xB51F61  mov     eax, edi
0xB51F63  push    41h
0xB51F65  lea     ecx, [esp+2C60h+var_2C44]
0xB51F69  push    ecx
0xB51F6A  add     edi, 41h
0xB51F6D  push    eax
0xB51F6E  mov     [esp+2C68h+var_2C3C], eax   ; ← 字段 4 槽地址
0xB51F72  mov     [esp+2C68h+var_2C2C], edi
0xB51F76  call    sub_B02BA0               ; ← 读字符串 ranking_term_last
0xB51F7B  add     esp, 0Ch
```

`sub_B02BA0` 本体（读 **NUL 结尾单字节串**：消费 = 串长 + 1）：

```asm
; VA: 0xB02BA0 .. 0xB02BF4
0xB02BA0  mov     edx, [esp+arg_8]          ; N = 槽上限（41h）
0xB02BA4  push    edi
0xB02BA5  mov     edi, [esp+4+arg_4]        ; cursor 结构
0xB02BA9  mov     ecx, [edi]                ; cur
0xB02BAB  mov     eax, [edi+4]
0xB02BAE  sub     eax, ecx
0xB02BB0  cmp     edx, eax
0xB02BB2  jge     short loc_B02BB6
0xB02BB4  mov     eax, edx                  ; N = min(N, 剩余字节)
0xB02BB6  test    eax, eax
0xB02BB8  jge     short loc_B02BBE
0xB02BBA  xor     al, al
0xB02BBC  pop     edi
0xB02BBD  retn
0xB02BBE  push    esi
0xB02BBF  push    eax
0xB02BC0  push    0
0xB02BC2  push    ecx
0xB02BC3  call    sub_CC8400               ; ← 在 [cur, cur+N) 内找 NUL
0xB02BC8  mov     esi, eax
0xB02BCA  add     esp, 0Ch
0xB02BCD  test    esi, esi
0xB02BCF  jnz     short loc_B02BD6
0xB02BD1  pop     esi
0xB02BD2  xor     al, al
0xB02BD4  pop     edi
0xB02BD5  retn
0xB02BD6  mov     eax, [edi]                ; cur
0xB02BD8  mov     edx, [esp+8+arg_0]        ; dst
0xB02BDC  add     esi, 1                    ; 含 NUL
0xB02BDF  mov     ecx, esi
0xB02BE1  sub     ecx, eax                  ; len + 1
0xB02BE3  push    ecx
0xB02BE4  push    eax                       ; src = cur
0xB02BE5  push    edx                       ; dst
0xB02BE6  call    sub_CC56B0               ; ← memcpy（按字节 ⇒ 单字节编码）
0xB02BEB  add     esp, 0Ch
0xB02BEE  mov     [edi], esi                ; ← 游标 = NUL 之后 ⇒ 消费 len+1
0xB02BF0  pop     esi
0xB02BF1  mov     al, 1
0xB02BF3  pop     edi
0xB02BF4  retn
```

## E4 字段 5/6：u32 `lose_troops`（+）与 u16 `expup_fgauge`（+）

```asm
; VA: 0xB51F86 .. 0xB51FCB   （字段 5 → var_2C24）
0xB51F8F  call    sub_B41470               ; 预留 4 字节槽（非字段）
0xB51F94  mov     eax, [esp+2C5Ch+var_2C24]
0xB51F9C  push    edx
0xB51F9D  push    eax
0xB51F9E  call    sub_B02DD0               ; ← 读 u32（lose_troops）

; VA: 0xB51FAE .. 0xB51FCC   （字段 6 → var_2C04）
0xB51FB7  call    sub_B413B0               ; 预留 2 字节槽（非字段）
0xB51FBC  mov     eax, [esp+2C5Ch+var_2C04]
0xB51FC4  push    edx
0xB51FC5  push    eax
0xB51FC6  call    sub_B02DF0               ; ← 读 u16（expup_fgauge）
```

`sub_B02DF0` 本体（读 **u16**，游标 +2）见 `../SC-0x0120-battle-entity_msma_show/asm.md` E2。

## E5 长度闭合（游标 == 末尾；变长部分由此闭合）

```asm
; VA: 0xB51FD6 .. 0xB51FE0
0xB51FD6  mov     ebx, [esp+2C5Ch+var_2C44]   ; 读完后的游标
0xB51FDA  cmp     ebx, [esp+2C5Ch+var_2C40]   ; vs 报文末尾
0xB51FDE  mov     ecx, esi
0xB51FE0  jz      short loc_B51FFC            ; ← 不等则 push 0A1h 报错
```

## E6 含义取证：块内日志格式串（6 条）

```asm
; VA: 0xB5206D .. 0xB52163
0xB5206D  mov     eax, [esp+2C5Ch+var_2C00]   ; 字段 1
0xB52071  mov     ecx, [eax]
0xB52079  push    offset aEFgauge             ; ← "e_fgauge="
...
0xB52094  mov     edx, [esp+2C64h+var_2C10]   ; 字段 2
0xB520A3  push    offset aZFgauge             ; ← "z_fgauge="
...
0xB520BE  mov     ecx, [esp+2C64h+var_2C20]   ; 字段 3（槽指针）
0xB520D0  push    offset aRankingTermNow      ; ← "ranking_term_now=\""
...
0xB520F6  mov     edx, [esp+2C64h+var_2C3C]   ; 字段 4（槽指针）
0xB52108  push    offset aRankingTermLas      ; ← "ranking_term_last=\""
...
0xB5212E  mov     eax, [esp+2C64h+var_2C24]   ; 字段 5
0xB5213D  push    offset aLoseTroops          ; ← "lose_troops="
...
0xB52158  mov     edx, [esp+2C64h+var_2C04]   ; 字段 6
0xB5215C  movzx   eax, word ptr [edx]
0xB52163  push    offset aExpupFgauge         ; ← "expup_fgauge="
```

## E7 去向：6 个值一次性交 `vt[0x1D4]`

```asm
; VA: 0xB521AB .. 0xB521DC
0xB521AB  mov     eax, [esp+2C5Ch+var_2C04]   ; expup_fgauge
0xB521AF  movzx   ecx, word ptr [eax]
0xB521B2  mov     eax, [esp+2C5Ch+var_2C24]   ; lose_troops
0xB521B6  mov     edx, [esi]
0xB521B8  mov     edx, [edx+1D4h]             ; ← vt[0x1D4]
0xB521BE  push    ecx
0xB521BF  mov     ecx, [eax]
0xB521C1  mov     eax, [esp+2C60h+var_2C3C]   ; ranking_term_last 槽
0xB521C5  push    ecx
0xB521C6  mov     ecx, [esp+2C64h+var_2C20]   ; ranking_term_now 槽
0xB521CA  push    eax
0xB521CB  mov     eax, [esp+2C68h+var_2C10]   ; z_fgauge
0xB521CF  push    ecx
0xB521D0  mov     ecx, [eax]
0xB521D2  mov     eax, [esp+2C6Ch+var_2C00]   ; e_fgauge
0xB521D6  push    ecx
0xB521D7  mov     ecx, [eax]
0xB521D9  push    ecx
0xB521DA  mov     ecx, esi
0xB521DC  call    edx                         ; vt[0x1D4](e_fgauge, z_fgauge, now, last, lose_troops, expup_fgauge)
0xB521DE  add     dword ptr [esi+2388h], 1
```
