# 汇编证据 —— SC-0x0C5F-battle-commander_candidacy_start

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E0 case 起始守卫（不是字段）

```asm
; VA: 0xB0E701 .. 0xB0E70F
0xB0E701  push    0D6h                     ; ← 本 case 错误码
0xB0E706  mov     ecx, esi
0xB0E708  call    sub_B05DA0               ; 按命令号查使能位 [ebx+edi+18Dh] 并递增接收计数（不读线）
0xB0E70D  test    al, al
0xB0E70F  jz      loc_B317C7               ; 守卫失败 ⇒ 公共退出
```

## E1 解码缓冲申请（容量 `2`）+ 线游标初始化

```asm
; VA: 0xB0E715 .. 0xB0E730
0xB0E715  mov     ecx, [esi+0Ch]
0xB0E718  mov     eax, [ecx]
0xB0E71A  mov     edx, [eax+78h]
0xB0E71D  push    2                        ; ← 容量 2 == 线长
0xB0E71F  call    edx
0xB0E721  mov     [esp+1B3Ch+var_1B14], eax ; 解码缓冲基址
0xB0E725  mov     eax, [esi+0Ch]
0xB0E728  push    eax
0xB0E729  lea     ecx, [esp+1B40h+var_1790]
0xB0E730  call    sub_ABB2F0               ; 用传输层缓冲初始化线游标 {cur,end}
```

## E2 字段 1：`remain_sec`（u16，偏移 0）

```asm
; VA: 0xB0E735 .. 0xB0E764
0xB0E735  lea     ecx, [esp+1B3Ch+var_1B14]
0xB0E739  push    ecx
0xB0E73A  lea     ecx, [esp+1B40h+var_1B2C] ; 槽地址
0xB0E749  call    sub_B413B0               ; 缓冲预留 2B（非字段）
0xB0E74E  mov     eax, [esp+1B3Ch+var_1B2C]
0xB0E752  lea     edx, [esp+1B3Ch+var_1B28] ; &线游标
0xB0E756  push    edx
0xB0E757  push    eax
0xB0E758  call    sub_B02DF0               ; ← 读 u16
0xB0E75D  add     esp, 8
0xB0E760  test    al, al
0xB0E762  mov     ecx, esi
0xB0E764  jnz     short loc_B0E780         ; 成功分支
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB0E780 .. 0xB0E78A
0xB0E780  mov     ebx, [esp+1B3Ch+var_1B28] ; 读完后的线游标
0xB0E784  cmp     ebx, [esp+1B3Ch+var_1B24] ; vs 报文末尾
0xB0E788  jnz     short loc_B0E766         ; ← 不等 ⇒ push 0D6h 报错
0xB0E78A  push    0D6h
```

## E4 含义取证：块内日志 `remain_sec=`

```asm
; VA: 0xB0E7FB .. 0xB0E813
0xB0E7FB  mov     eax, [esp+1B3Ch+var_1B2C]
0xB0E7FF  movzx   ecx, word ptr [eax]      ; 槽里的 u16
0xB0E802  push    ecx
0xB0E803  push    offset aRemainSec        ; ← "remain_sec="
0xB0E808  push    edi
0xB0E809  call    sub_41D990
0xB0E813  call    sub_B032A0               ; 十进制打印器
```

## E5 去向：`vt[0x29C]`

```asm
; VA: 0xB0E84B .. 0xB0E866
0xB0E84B  mov     eax, [esp+1B3Ch+var_1B2C]
0xB0E84F  movzx   ecx, word ptr [eax]      ; remain_sec
0xB0E852  mov     edx, [esi]
0xB0E854  mov     edx, [edx+29Ch]          ; ← vt[0x29C]
0xB0E85A  push    ecx                     ; 实参 1 = remain_sec
0xB0E85B  mov     ecx, esi
0xB0E85D  call    edx
0xB0E85F  add     dword ptr [esi+2B00h], 1 ; 本命令接收计数（64 位）
0xB0E866  adc     dword ptr [esi+2B04h], 0
```
