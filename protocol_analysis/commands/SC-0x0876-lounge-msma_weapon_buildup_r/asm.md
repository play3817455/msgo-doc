# 汇编证据 —— SC-0x0876-lounge-msma_weapon_buildup_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 case 入口 + 解码缓冲申请（容量 `0x24` = 36）

```asm
; VA: 0xB542C3 .. 0xB542F7
0xB542C3  push    112h                     ; ← 本 case 错误码
0xB542C8  mov     ecx, esi
0xB542CA  call    sub_B41120
0xB542CF  test    al, al
0xB542D1  jz      loc_B890FE
0xB542D7  mov     ecx, [esi+0Ch]
0xB542DA  mov     eax, [ecx]
0xB542DC  mov     edx, [eax+78h]
0xB542DF  push    24h ; '$'                ; ← 容量 36 == 线长
0xB542E1  call    edx
0xB542E3  mov     [esp+2C5Ch+var_2C28], eax ; 缓冲游标
0xB542E7  mov     eax, [esi+0Ch]
0xB542EA  push    eax
0xB542EB  lea     ecx, [esp+2C60h+var_2BA4]
0xB542F2  call    sub_ABB2F0               ; 初始化 {cur,end} 读游标
```

## E2 字段 1：`result`（u32，偏移 0）

```asm
; VA: 0xB5430B .. 0xB5431A
0xB5430B  call    sub_B41470               ; 缓冲预留 4B（非字段）
0xB54310  mov     eax, [esp+2C5Ch+var_2BEC]
0xB54314  lea     edx, [esp+2C5Ch+var_2C44]   ; &线游标
0xB54318  push    edx
0xB54319  push    eax
0xB5431A  call    sub_B02DD0               ; ← 读 u32
```

## E3 字段 2：`uniqid_ms`（u64，偏移 4）

```asm
; VA: 0xB54342 .. 0xB5435A
0xB54342  lea     ecx, [esp+2C5Ch+var_2C28]
0xB54346  push    ecx
0xB54347  lea     ecx, [esp+2C60h+var_2C3C]   ; 槽（8B）
0xB5434B  call    sub_B41A10               ; 缓冲预留 8B（非字段）
0xB54350  mov     ebx, [esp+2C5Ch+var_2C3C]
0xB54354  lea     edx, [esp+2C5Ch+var_2C44]
0xB54358  push    edx
0xB54359  push    ebx
0xB5435A  call    sub_B06200               ; ← 读 u64
```

## E4 字段 3..10：`item_id`/`ticket_id`/`usenum`/`param_target`/`workres`/`buildup_cnt`/`up_param`/`mech_npcpict`

```asm
; VA: 0xB5438B .. 0xB544AA（每字段 = 预留 + bounded 读取器，只计读取器一次）
0xB5439A  call    sub_B02DD0               ; 字段 3  item_id      u32（偏移 12）
0xB543BE  call    sub_B02DD0               ; 字段 4  ticket_id    u32（偏移 16）
0xB543E2  call    sub_B02DF0               ; 字段 5  usenum       u16（偏移 20）
0xB5440A  call    sub_B02DF0               ; 字段 6  param_target u16（偏移 22）
0xB54432  call    sub_B02DD0               ; 字段 7  workres      u32（偏移 24）
0xB5445A  call    sub_B02DF0               ; 字段 8  buildup_cnt  u16（偏移 28）
0xB54482  call    sub_B02DF0               ; 字段 9  up_param     u16（偏移 30）
0xB544AA  call    sub_B02DD0               ; 字段 10 mech_npcpict u32（偏移 32）
```

## E5 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB544BA .. 0xB544C4
0xB544BA  mov     eax, [esp+2C5Ch+var_2C44]   ; 读完后的游标
0xB544BE  cmp     eax, [esp+2C5Ch+var_2C40]   ; vs 报文末尾
0xB544C2  mov     ecx, esi
0xB544C4  jz      short loc_B544E0            ; ← 不等 ⇒ push 112h 报错
```

## E6 含义取证：块内日志格式串（10 个字段各有 `xxx=`）

```asm
; VA: 0xB5455D .. 0xB546D6
0xB5455D  push    offset aResult              ; "result="
0xB54587  push    offset aUniqidMs            ; "uniqid_ms="   （sub_B08500 64 位打印）
0xB545B1  push    offset aItemId              ; "item_id="
0xB545DB  push    offset aTicketId            ; "ticket_id="
0xB54606  push    offset aUsenum              ; "usenum="      （sub_B032A0 十六进制打印）
0xB54631  push    offset aParamTarget         ; "param_target="
0xB5465B  push    offset aWorkres             ; "workres="
0xB54686  push    offset aBuildupCnt          ; "buildup_cnt="
0xB546B1  push    offset aUpParam             ; "up_param="
0xB546D6  push    offset aMechNpcpict         ; "mech_npcpict="
```

## E7 去向：`vt[0x2CC]`（10 个实参，逆序入栈）

```asm
; VA: 0xB54722 .. 0xB5477C
0xB5474D  mov     edx, [edx+2CCh]             ; ← vt[0x2CC]
0xB5472C  push    ecx                         ; 实参 10 = mech_npcpict
0xB54734  push    ecx                         ; 实参  9 = up_param
0xB5473C  push    ecx                         ; 实参  8 = buildup_cnt
0xB54743  push    ecx                         ; 实参  7 = workres
0xB54753  push    ecx                         ; 实参  6 = param_target
0xB5475B  push    ecx                         ; 实参  5 = usenum
0xB54765  push    ecx                         ; 实参  4 = ticket_id
0xB5476B  push    ecx                         ; 实参  3 = item_id
0xB5476E  push    eax                         ; 实参  2 = uniqid_ms 高 32 位
0xB54776  push    ecx                         ; 实参  2 = uniqid_ms 低 32 位
0xB54779  push    ecx                         ; 实参  1 = result
0xB5477C  call    edx
0xB5477E  add     dword ptr [esi+38B8h], 1    ; 本命令接收计数（64 位）
0xB5478C  adc     dword ptr [esi+38BCh], 0
```
