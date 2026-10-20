# 汇编证据 —— SC-0x15B5-lounge-clan_npc_update_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 case 入口 + 解码缓冲申请（容量 `0x8`）

```asm
; VA: 0xB560B0 .. 0xB560E4
0xB560B0  push    1C1h                     ; ← 本 case 错误码
0xB560B5  mov     ecx, esi
0xB560B7  call    sub_B41120               ; case 起始守卫（不读线）
0xB560BC  test    al, al
0xB560BE  jz      loc_B890FE
0xB560C4  mov     ecx, [esi+0Ch]
0xB560C7  mov     eax, [ecx]
0xB560C9  mov     edx, [eax+78h]
0xB560CC  push    8                        ; ← 容量 8
0xB560CE  call    edx
0xB560D0  mov     [esp+2C5Ch+var_2C3C], eax ; 解码缓冲基址
0xB560D4  mov     eax, [esi+0Ch]
0xB560D7  push    eax
0xB560D8  lea     ecx, [esp+2C60h+var_27EC]
0xB560DF  call    sub_ABB2F0               ; 初始化线游标
```

## E2 字段 1：`result`（u32，偏移 0）

```asm
; VA: 0xB560FD .. 0xB5611F
0xB560FD  mov     eax, [esp+2C5Ch+var_2C38]
0xB56101  lea     edx, [esp+2C5Ch+var_2C44]
0xB56105  push    edx
0xB56106  push    eax
0xB56107  call    sub_B02DD0               ; ← 读 u32（消费 4 字节）
0xB5610C  add     esp, 8
0xB5610F  test    al, al
0xB56111  jnz     short loc_B5612F         ; 成功分支
0xB5611A  push    1C1h                     ; ← 错误码
```

（其前的 `0xB560F8 call sub_B41470` 为 u32 槽预留，**非字段**）

## E3 字段 2：`npc_id`（u32，偏移 4）+ 长度闭合

```asm
; VA: 0xB5612F .. 0xB56174
0xB56134  lea     ecx, [esp+2C60h+var_2C48]
0xB56138  call    sub_B41470               ; u32 槽预留（非字段）
0xB5613D  mov     eax, [esp+2C5Ch+var_2C48]
0xB56141  lea     edx, [esp+2C5Ch+var_2C44]
0xB56145  push    edx
0xB56146  push    eax
0xB56147  call    sub_B02DD0               ; ← 读 u32（消费 4 字节）
0xB5614C  add     esp, 8
0xB5614F  test    al, al
0xB56151  jz      short loc_B56113
0xB56153  mov     ebx, [esp+2C5Ch+var_2C44] ; 读完后的线游标
0xB56157  cmp     ebx, [esp+2C5Ch+var_2C40] ; vs 报文末尾
0xB5615D  jz      short loc_B56179         ; ← 不等 ⇒ push 1 / push 1C1h 报错
```

## E4 含义取证：块内日志 `result=` / `npc_id=`

```asm
; VA: 0xB561EA .. 0xB5622B
0xB561EA  mov     eax, [esp+2C5Ch+var_2C38] ; result 槽
0xB561EE  mov     ecx, [eax]
0xB561F6  push    offset aResult            ; ← "result="
0xB56206  call    sub_B03580               ; u32 打印器
0xB56211  mov     edx, [esp+2C64h+var_2C48] ; npc_id 槽
0xB56215  mov     eax, [edx]
0xB5621B  push    offset aNpcId             ; ← "npc_id="
0xB5622B  call    sub_B03580
```

## E5 去向：`vt[0x444](result, npc_id)`

```asm
; VA: 0xB56263 .. 0xB5628B
0xB56263  mov     eax, [esp+2C5Ch+var_2C48] ; npc_id 槽
0xB56267  mov     ecx, [eax]
0xB56269  mov     eax, [esp+2C5Ch+var_2C38] ; result 槽
0xB5626D  mov     edx, [esi]
0xB5626F  mov     edx, [edx+444h]           ; ← vt[0x444]
0xB56275  push    ecx                       ; 实参 2 = npc_id
0xB56276  mov     ecx, [eax]
0xB56278  push    ecx                       ; 实参 1 = result
0xB56279  mov     ecx, esi
0xB5627B  call    edx
0xB5627D  add     dword ptr [esi+5988h], 1  ; 本命令接收计数（64 位）
0xB5628B  adc     dword ptr [esi+598Ch], 0
```
