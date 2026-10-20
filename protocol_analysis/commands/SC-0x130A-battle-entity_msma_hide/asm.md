# 汇编证据 —— SC-0x130A-battle-entity_msma_hide

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 case 入口 + 解码缓冲申请（容量 `0x2`）

```asm
; VA: 0xB0F609 .. 0xB0F63F
0xB0F609  call    sub_B05DA0               ; case 起始守卫（不读线）
0xB0F60E  test    al, al
0xB0F610  jz      loc_B317C7
0xB0F616  mov     ecx, [esi+0Ch]
0xB0F619  mov     eax, [ecx]
0xB0F61B  mov     edx, [eax+78h]
0xB0F61E  push    2                        ; ← 容量 2
0xB0F620  call    edx
0xB0F622  mov     [esp+1B3Ch+var_1B14], eax ; 解码缓冲基址
0xB0F626  mov     eax, [esi+0Ch]
0xB0F629  push    eax
0xB0F62A  lea     ecx, [esp+1B40h+var_1774]
0xB0F631  call    sub_ABB2F0               ; 初始化线游标
```

## E2 字段 1：`ent_id`（u16，偏移 0）

```asm
; VA: 0xB0F636 .. 0xB0F665
0xB0F636  lea     ecx, [esp+1B3Ch+var_1B14]
0xB0F63A  push    ecx
0xB0F63B  lea     ecx, [esp+1B40h+var_1B2C]
0xB0F63F  mov     [esp+1B40h+var_4], 7Bh
0xB0F64A  call    sub_B413B0               ; u16 槽预留（推进缓冲游标，不是字段）
0xB0F64F  mov     eax, [esp+1B3Ch+var_1B2C]
0xB0F653  lea     edx, [esp+1B3Ch+var_1B28] ; &线游标
0xB0F657  push    edx
0xB0F658  push    eax
0xB0F659  call    sub_B02DF0               ; ← 读 u16（消费 2 字节）
0xB0F65E  add     esp, 8
0xB0F661  test    al, al
0xB0F665  jnz     short loc_B0F67E         ; 成功分支
0xB0F66E  push    5Ch                      ; ← 错误码
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB0F67E .. 0xB0F68A
0xB0F67E  mov     ebx, [esp+1B3Ch+var_1B28] ; 读完后的线游标
0xB0F682  cmp     ebx, [esp+1B3Ch+var_1B24] ; vs 报文末尾
0xB0F686  jnz     short loc_B0F667           ; ← 不等 ⇒ push 1 / push 5Ch 报错
0xB0F688  push    5Ch
0xB0F68A  call    sub_B05D90                 ; 取本命令日志句柄
```

## E4 含义取证：块内日志串 `ent_id=`

```asm
; VA: 0xB0F6F6 .. 0xB0F70E
0xB0F6F6  mov     eax, [esp+1B3Ch+var_1B2C] ; 槽地址
0xB0F6FA  movzx   ecx, word ptr [eax]       ; ← 2 字节取值
0xB0F6FD  push    ecx
0xB0F6FE  push    offset aEntId            ; ← "ent_id="
0xB0F704  call    sub_41D990
0xB0F70E  call    sub_B032A0               ; u16 打印器
```

## E5 去向：`vt[0x170](ent_id)`

```asm
; VA: 0xB0F746 .. 0xB0F76F
0xB0F746  mov     eax, [esp+1B3Ch+var_1B2C] ; 槽地址
0xB0F74A  movzx   ecx, word ptr [eax]       ; ent_id
0xB0F74D  mov     edx, [esi]
0xB0F74F  mov     edx, [edx+170h]           ; ← vt[0x170]
0xB0F755  push    ecx                       ; 实参 1 = ent_id
0xB0F756  mov     ecx, esi
0xB0F758  call    edx
0xB0F75A  add     dword ptr [esi+1420h], 1  ; 本命令接收计数（64 位）
0xB0F768  adc     dword ptr [esi+1424h], 0
```
