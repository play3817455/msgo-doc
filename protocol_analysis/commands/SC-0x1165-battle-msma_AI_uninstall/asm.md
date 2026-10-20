# 汇编证据 —— SC-0x1165-battle-msma_AI_uninstall

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 case 入口 + 解码缓冲申请（容量 `0x2`）

```asm
; VA: 0xB0F479 .. 0xB0F4B6
0xB0F479  push    0B6h                     ; ← 本 case 错误码
0xB0F47E  mov     ecx, esi
0xB0F480  call    sub_B05DA0               ; case 起始守卫（不读线）
0xB0F485  test    al, al
0xB0F487  jz      loc_B317C7
0xB0F48D  mov     ecx, [esi+0Ch]
0xB0F490  mov     edx, [ecx]
0xB0F492  mov     eax, [edx+78h]
0xB0F495  push    2                        ; ← 容量 2
0xB0F497  call    eax
0xB0F499  mov     ecx, [esi+0Ch]
0xB0F49C  push    ecx
0xB0F49D  lea     ecx, [esp+1B40h+var_177C]
0xB0F4A4  mov     [esp+1B40h+var_1B14], eax ; 解码缓冲基址
0xB0F4A8  call    sub_ABB2F0               ; 初始化线游标 {cur,end}
```

## E2 字段 1：`AI_ent_id`（u16，偏移 0）

```asm
; VA: 0xB0F4AD .. 0xB0F4DA
0xB0F4AD  lea     edx, [esp+1B3Ch+var_1B14] ; 解码缓冲游标
0xB0F4B1  push    edx
0xB0F4B2  lea     ecx, [esp+1B40h+var_1B2C] ; 输出：槽地址
0xB0F4B6  mov     [esp+1B40h+var_4], 0E5h
0xB0F4C1  call    sub_B413B0               ; u16 槽预留（推进缓冲游标，不是字段）
0xB0F4C6  mov     ecx, [esp+1B3Ch+var_1B2C]
0xB0F4CA  lea     eax, [esp+1B3Ch+var_1B28] ; &线游标
0xB0F4CE  push    eax
0xB0F4CF  push    ecx                       ; 槽地址
0xB0F4D0  call    sub_B02DF0               ; ← 读 u16（消费 2 字节）
0xB0F4D5  add     esp, 8
0xB0F4D8  test    al, al
0xB0F4DC  jnz     short loc_B0F4F8         ; 成功分支
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB0F4F8 .. 0xB0F507
0xB0F4F8  mov     ebx, [esp+1B3Ch+var_1B28] ; 读完后的线游标
0xB0F4FC  cmp     ebx, [esp+1B3Ch+var_1B24] ; vs 报文末尾
0xB0F500  jnz     short loc_B0F4DE           ; ← 不等 ⇒ push 1 / push 0B6h 报错
0xB0F502  push    0B6h
0xB0F507  call    sub_B05D90                 ; 取本命令日志句柄
```

## E4 含义取证：块内日志串 `AI_ent_id=`

```asm
; VA: 0xB0F573 .. 0xB0F58B
0xB0F573  mov     eax, [esp+1B3Ch+var_1B2C] ; 槽地址
0xB0F577  movzx   ecx, word ptr [eax]       ; ← 2 字节取值
0xB0F57A  push    ecx
0xB0F57B  push    offset aAiEntId          ; ← "AI_ent_id="
0xB0F581  call    sub_41D990
0xB0F58B  call    sub_B032A0               ; u16 打印器
```

## E5 去向：`vt[0x244](AI_ent_id)`

```asm
; VA: 0xB0F5C3 .. 0xB0F5EC
0xB0F5C3  mov     eax, [esp+1B3Ch+var_1B2C] ; 槽地址
0xB0F5C7  movzx   ecx, word ptr [eax]       ; AI_ent_id
0xB0F5CA  mov     edx, [esi]
0xB0F5CC  mov     edx, [edx+244h]           ; ← vt[0x244]
0xB0F5D2  push    ecx                       ; 实参 1 = AI_ent_id
0xB0F5D3  mov     ecx, esi
0xB0F5D5  call    edx
0xB0F5D7  add     dword ptr [esi+2500h], 1  ; 本命令接收计数（64 位）
0xB0F5E5  adc     dword ptr [esi+2504h], 0
```
