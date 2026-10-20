# 汇编证据 —— SC-0x143D-lounge-clan_create_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 case 入口 + 解码缓冲申请（容量 `0x5`）

```asm
; VA: 0xB55C1E .. 0xB55C52
0xB55C1E  push    1AFh                     ; ← 本 case 错误码
0xB55C23  mov     ecx, esi
0xB55C25  call    sub_B41120               ; case 起始守卫（不读线）
0xB55C2A  test    al, al
0xB55C2C  jz      loc_B890FE
0xB55C32  mov     ecx, [esi+0Ch]
0xB55C35  mov     eax, [ecx]
0xB55C37  mov     edx, [eax+78h]
0xB55C3A  push    5                        ; ← 容量 5（= 4 + 1）
0xB55C3C  call    edx
0xB55C3E  mov     [esp+2C5Ch+var_2C3C], eax ; 解码缓冲基址
0xB55C42  mov     eax, [esi+0Ch]
0xB55C45  push    eax
0xB55C46  lea     ecx, [esp+2C60h+var_27F4]
0xB55C4D  call    sub_ABB2F0               ; 初始化线游标
```

## E2 字段 1：`result`（u32，偏移 0）

```asm
; VA: 0xB55C52 .. 0xB55C7F
0xB55C52  lea     ecx, [esp+2C5Ch+var_2C3C]
0xB55C56  push    ecx
0xB55C57  lea     ecx, [esp+2C60h+var_2C38]
0xB55C66  call    sub_B41470               ; u32 槽预留（非字段）
0xB55C6B  mov     eax, [esp+2C5Ch+var_2C38]
0xB55C6F  lea     edx, [esp+2C5Ch+var_2C44]
0xB55C73  push    edx
0xB55C74  push    eax
0xB55C75  call    sub_B02DD0               ; ← 读 u32（消费 4 字节）
0xB55C7A  add     esp, 8
0xB55C7D  test    al, al
0xB55C7F  jnz     short loc_B55C9D         ; 成功分支
0xB55C88  push    1AFh                     ; ← 错误码
```

## E3 字段 2：`clan_kind`（u8，偏移 4）+ 长度闭合

```asm
; VA: 0xB55C9D .. 0xB55CE2
0xB55C9D  lea     ecx, [esp+2C5Ch+var_2C3C]
0xB55CA1  push    ecx
0xB55CA2  lea     ecx, [esp+2C60h+var_2C48]
0xB55CA6  call    sub_B05E30               ; u8 槽预留（非字段）
0xB55CAB  mov     eax, [esp+2C5Ch+var_2C48]
0xB55CAF  lea     edx, [esp+2C5Ch+var_2C44]
0xB55CB3  push    edx
0xB55CB4  push    eax
0xB55CB5  call    sub_B06230               ; ← 读 u8（消费 1 字节）
0xB55CBA  add     esp, 8
0xB55CBD  test    al, al
0xB55CBF  jz      short loc_B55C81
0xB55CC1  mov     ebx, [esp+2C5Ch+var_2C44] ; 读完后的线游标
0xB55CC5  cmp     ebx, [esp+2C5Ch+var_2C40] ; vs 报文末尾
0xB55CCB  jz      short loc_B55CE7         ; ← 不等 ⇒ push 1 / push 1AFh 报错
```

## E4 含义取证：块内日志 `result=` / `clan_kind=`

```asm
; VA: 0xB55D58 .. 0xB55D96
0xB55D58  mov     eax, [esp+2C5Ch+var_2C38] ; result 槽
0xB55D5C  mov     ecx, [eax]
0xB55D64  push    offset aResult            ; ← "result="
0xB55D74  call    sub_B03580               ; u32 打印器
0xB55D7F  mov     edx, [esp+2C64h+var_2C48] ; clan_kind 槽
0xB55D87  push    offset aClanKind          ; ← "clan_kind="
0xB55D96  call    sub_B0C1F0               ; 1 字节打印器（内部 movsx，仅打印用）
```

## E5 去向：`vt[0x420](result, clan_kind)`

```asm
; VA: 0xB55DD1 .. 0xB55DFA
0xB55DD1  mov     ecx, [esp+2C5Ch+var_2C48] ; clan_kind 槽
0xB55DD5  movzx   edx, byte ptr [ecx]       ; ← 零扩展（无符号语义）
0xB55DD8  mov     ecx, [esp+2C5Ch+var_2C38] ; result 槽
0xB55DDC  mov     eax, [esi]
0xB55DDE  mov     eax, [eax+420h]           ; ← vt[0x420]
0xB55DE4  push    edx                       ; 实参 2 = clan_kind
0xB55DE5  mov     edx, [ecx]
0xB55DE7  push    edx                       ; 实参 1 = result
0xB55DE8  mov     ecx, esi
0xB55DEA  call    eax
0xB55DEC  add     dword ptr [esi+5628h], 1  ; 本命令接收计数（64 位）
0xB55DFA  adc     dword ptr [esi+562Ch], 0
```
