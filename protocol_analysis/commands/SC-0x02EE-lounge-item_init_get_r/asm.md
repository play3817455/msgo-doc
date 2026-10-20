# 汇编证据 —— SC-0x02EE-lounge-item_init_get_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 case 入口 + 解码缓冲申请（容量 0xF400）

```asm
; VA: 0xB524F6 .. 0xB52528
0xB524F6  push    140h                     ; ← 本 case 开关/错误码
0xB524FB  mov     ecx, esi
0xB524FD  call    sub_B41120
0xB52502  test    al, al
0xB52504  jz      loc_B890FE
0xB5250A  mov     ecx, [esi+0Ch]
0xB5250D  mov     eax, [ecx]
0xB5250F  mov     edx, [eax+78h]
0xB52512  push    0F400h                   ; ← 容量 62464（列表上限场景的缓冲上限）
0xB52517  call    edx
0xB52519  mov     [esp+2C5Ch+var_2C28], eax
0xB5251D  mov     eax, [esi+0Ch]
0xB52520  push    eax
0xB52521  lea     ecx, [esp+2C60h+var_2BDC]
0xB52528  call    sub_ABB2F0
```

## E2 定长骨架（4×u16 + 6×u32）

```asm
; VA: 0xB5252D .. 0xB525E2   （4 个 u16，槽 var_2C48 / var_2C38 / var_2C34 / var_2C30）
0xB52541  call    sub_B413B0               ; 预留 2 字节槽（非字段）
0xB52550  call    sub_B02DF0               ; ← slot_num_main（u16）
0xB52581  call    sub_B413B0
0xB52590  call    sub_B02DF0               ; ← slot_num_consume（u16）
0xB525A5  call    sub_B413B0
0xB525B4  call    sub_B02DF0               ; ← slot_num_trash（u16）
0xB525C9  call    sub_B413B0
0xB525D8  call    sub_B02DF0               ; ← slot_num_plan（u16）

; VA: 0xB525E8 .. 0xB526D8   （6 个 u32，槽 var_2C0C/2C08/2BFC/2BF0/2BEC/2BD4）
0xB525F1  call    sub_B41470
0xB52600  call    sub_B02DD0               ; ← sort_tm_sec_main（u32）
0xB52619  call    sub_B41470
0xB52628  call    sub_B02DD0               ; ← sort_tm_usec_main
0xB52641  call    sub_B41470
0xB52650  call    sub_B02DD0               ; ← sort_tm_sec_consume
0xB52669  call    sub_B41470
0xB52678  call    sub_B02DD0               ; ← sort_tm_usec_consume
0xB52691  call    sub_B41470
0xB526A0  call    sub_B02DD0               ; ← sort_tm_sec_plan
0xB526BC  call    sub_B41470
0xB526CE  call    sub_B02DD0               ; ← sort_tm_usec_plan
```

读取器本体（**宽度判定依据**）：

```asm
; VA: 0xB02DF0 .. 0xB02E10   （u16：游标 +2）
0xB02E01  mov     cx, [ecx]
0xB02E0B  add     dword ptr [eax], 2

; VA: 0xB02DD0 .. 0xB02DEE   （u32：游标 +4）
0xB02DE1  mov     ecx, [ecx]
0xB02DE9  add     dword ptr [eax], 4
```

## E3 列表 1：`count_main` + `sub_B416C0` 分配 + 循环 `sub_B434F0`

```asm
; VA: 0xB526DE .. 0xB5271A
0xB526DE  lea     ecx, [esp+2C5Ch+var_2C44]   ; 游标
0xB526E2  push    ecx
0xB526E3  lea     edx, [esp+2C60h+var_2C24]   ; ← count_main
0xB526E7  push    edx
0xB526E8  call    sub_B02DD0               ; 读 u32（A1）
0xB52710  mov     ebx, [esp+2C5Ch+var_2C24]
0xB52714  cmp     ebx, 12Ch                ; ← 上限 300
0xB5271A  ja      short loc_B526F4          ; 超限 ⇒ 错误
0xB5271C  push    ebx
0xB5271D  lea     eax, [esp+2C60h+var_2C28]
0xB52721  push    eax
0xB52722  lea     ecx, [esp+2C64h+var_2C18]
0xB52726  call    sub_B416C0               ; 缓冲数组预留（每元素 +0x18）
0xB5272B  xor     edi, edi
0xB5272D  test    ebx, ebx
0xB5272F  jbe     short loc_B52774
0xB52740  mov     eax, [esp+2C5Ch+var_2C04]
0xB52744  lea     edx, [esp+2C5Ch+var_2C44]
0xB52748  push    edx
0xB52749  push    eax
0xB5274A  call    sub_B434F0               ; ← 读 1 个元素（22 字节）
0xB52752  test    al, al
0xB52754  jz      short loc_B52764
0xB52756  add     [esp+2C5Ch+var_2C04], 18h  ; ← 缓冲步进 24
0xB5275B  add     edi, 1
0xB5275E  cmp     edi, ebx
0xB52760  jb      short loc_B52740
```

缓冲数组预留函数（**缓冲步进 = 0x18**）：

```asm
; VA: 0xB416C0 .. 0xB416EB
0xB416C0  mov     edx, [esp+arg_0]
0xB416C4  mov     eax, ecx
0xB416CB  mov     [eax+4], esi
0xB416CE  mov     ecx, [edx]
0xB416D0  mov     [eax], ecx
0xB416D4  test    esi, esi
0xB416D7  jle     short locret_B416EB
0xB416E0  add     dword ptr [edx], 18h          ; ← 每元素推进 24 字节
0xB416E3  add     ecx, 1
0xB416E6  cmp     ecx, [eax+4]
0xB416E9  jl      short loc_B416E0
0xB416EB  retn    8
```

## E4 元素读取器 `sub_B434F0`（**元素线长 = 8+4+4+4+2 = 22**）

```asm
; VA: 0xB434F0 .. 0xB43561
0xB434F0  mov     eax, [esp+arg_4]
0xB434F4  mov     edx, [eax]
0xB434F6  lea     ecx, [edx+8]              ; ① 需要 8 字节
0xB434F9  cmp     ecx, [eax+4]
0xB434FC  ja      short loc_B4355A
0xB434FE  mov     ecx, [esp+arg_0]          ; dst
0xB43503  mov     esi, [edx]
0xB43505  mov     [ecx], esi                ; ← uniqid 低 4 字节
0xB43507  mov     edx, [edx+4]
0xB4350A  mov     [ecx+4], edx              ; ← uniqid 高 4 字节
0xB4350D  add     dword ptr [eax], 8        ; ← 游标 +8
0xB43510  mov     edx, [eax]
0xB43512  lea     esi, [edx+4]              ; ② 4 字节
0xB43515  cmp     esi, [eax+4]
0xB43518  ja      short loc_B4355D
0xB4351A  mov     edx, [edx]
0xB4351C  mov     [ecx+8], edx              ; ← item_id
0xB4351F  add     dword ptr [eax], 4        ; ← 游标 +4
0xB43522  mov     edx, [eax]
0xB43524  lea     esi, [edx+4]              ; ③ 4 字节
0xB43527  cmp     esi, [eax+4]
0xB4352A  ja      short loc_B4355D
0xB4352C  mov     edx, [edx]
0xB4352E  mov     [ecx+0Ch], edx            ; ← tm_sec
0xB43531  add     dword ptr [eax], 4        ; ← 游标 +4
0xB43534  mov     edx, [eax]
0xB43536  lea     esi, [edx+4]              ; ④ 4 字节
0xB43539  cmp     esi, [eax+4]
0xB4353C  ja      short loc_B4355D
0xB4353E  mov     edx, [edx]
0xB43540  mov     [ecx+10h], edx            ; ← tm_usec
0xB43543  add     dword ptr [eax], 4        ; ← 游标 +4
0xB43546  push    eax
0xB43547  add     ecx, 14h
0xB4354A  push    ecx
0xB4354B  call    sub_B02DF0               ; ⑤ u16（stack，游标 +2）
0xB43550  add     esp, 8
0xB43553  test    al, al
0xB43555  setnz   al
0xB43558  pop     esi
0xB43559  retn
```
⇒ 元素消费字节数 = `8 + 4 + 4 + 4 + 2` = **22**；内存槽偏移为 `+0/+8/+0Ch/+10h/+14h`（步进 0x18=24）。

## E5 元素打印器 `sub_B49CF0`（成员名取证）

```asm
; VA: 0xB49CF0 .. 0xB49DD3（摘）
0xB49D05  mov     eax, [edi+4]
0xB49D08  mov     ecx, [edi]
0xB49D14  push    offset aUniqid             ; ← "uniqid="（u64 两半）
0xB49D24  call    sub_B083A0
0xB49D2F  mov     edx, [edi+8]
0xB49D3B  push    offset aItemId             ; ← "item_id="
0xB49D56  mov     eax, [edi+0Ch]
0xB49D62  push    offset aTmSec              ; ← "tm_sec="
0xB49D7D  mov     ecx, [edi+10h]
0xB49D89  push    offset aTmUsec             ; ← "tm_usec="
0xB49DA4  movzx   edx, word ptr [edi+14h]    ; ← 第 5 成员按 u16 取
0xB49DAC  push    offset aStack              ; ← "stack="
```

## E6 其余三个列表（同构，仅计数上限不同）

```asm
; VA: 0xB52774 .. 0xB528EE
0xB5277E  call    sub_B02DD0               ; ← count_consume（var_2C2C）
0xB52792  cmp     ebx, 64h                 ; ← 上限 100
0xB527A5  call    sub_B416C0
0xB527CA  call    sub_B434F0               ; 元素读取
0xB527D6  add     [esp+2C5Ch+var_2C04], 18h

0xB527FE  call    sub_B02DD0               ; ← count_trash（var_2C00）
0xB52812  cmp     ebx, 514h                ; ← 上限 1300
0xB5282B  call    sub_B416C0
0xB5284B  call    sub_B434F0
0xB52857  add     [esp+2C5Ch+var_2C04], 18h

0xB5287F  call    sub_B02DD0               ; ← count_plan（var_2C10）
0xB52893  cmp     ebx, 384h                ; ← 上限 900
0xB528A9  call    sub_B416C0
0xB528C6  call    sub_B434F0
0xB528D2  add     [esp+2C5Ch+var_2C04], 18h
```

## E7 尾字段（4×u32）

```asm
; VA: 0xB528F0 .. 0xB5299C
0xB528FC  call    sub_B41470
0xB5290E  call    sub_B02DD0               ; ← msma_plan_sort_type（var_2BD0）
0xB5292A  call    sub_B41470
0xB5293C  call    sub_B02DD0               ; ← msma_plan_sort_order（var_2BCC）
0xB52958  call    sub_B41470
0xB5296A  call    sub_B02DD0               ; ← sort_plan_sec（var_2BC8）
0xB52983  call    sub_B41470
0xB52992  call    sub_B02DD0               ; ← sort_plan_usec（var_2C04）
```

## E8 长度闭合（整包精确消费完）

```asm
; VA: 0xB529A2 .. 0xB529AC
0xB529A2  mov     ecx, [esp+2C5Ch+var_2C44]   ; 读完后的游标
0xB529A6  cmp     ecx, [esp+2C5Ch+var_2C40]   ; vs 报文末尾
0xB529AA  mov     ecx, esi
0xB529AC  jz      short loc_B529C8            ; ← 不等则 push 140h 报错
```

## E9 含义取证：18 条日志格式串（节选）

```asm
; VA: 0xB52A39 .. 0xB52E54（每条 push offset aXxx）
0xB52A46  push    offset aSlotNumMain        ; "slot_num_main="
0xB52A71  push    offset aSlotNumConsume     ; "slot_num_consume="
0xB52A9C  push    offset aSlotNumTrash       ; "slot_num_trash="
0xB52AC7  push    offset aSlotNumPlan        ; "slot_num_plan="
0xB52AF1  push    offset aSortTmSecMain      ; "sort_tm_sec_main="
0xB52B1B  push    offset aSortTmUsecMain     ; "sort_tm_usec_main="
0xB52B45  push    offset aSortTmSecConsu     ; "sort_tm_sec_consume="
0xB52B6F  push    offset aSortTmUsecCons      ; "sort_tm_usec_consume="
0xB52B99  push    offset aSortTmSecPlan      ; "sort_tm_sec_plan="
0xB52BC6  push    offset aSortTmUsecPlan     ; "sort_tm_usec_plan="
0xB52BE1  push    offset aItmlistMain        ; "itmlist_main={"
0xB52C5B  push    offset aItmlistConsume     ; "itmlist_consume={"
0xB52CD1  push    offset aItmlistTrash       ; "itmlist_trash={"
0xB52D4D  push    offset aItmlistPlan        ; "itmlist_plan={"
0xB52DD5  push    offset aMsmaPlanSortTy     ; "msma_plan_sort_type="
0xB52E02  push    offset aMsmaPlanSortOr     ; "msma_plan_sort_order="
0xB52E2F  push    offset aSortPlanSec        ; "sort_plan_sec="
0xB52E54  push    offset aSortPlanUsec       ; "sort_plan_usec="
```

## E10 去向：整包交 `vt[0x32C]`（22 个实参）

```asm
; VA: 0xB52EA4 .. 0xB52F59（push 顺序 = 从最后实参到第一实参）
0xB52EA4  mov     ecx, [esp+2C5Ch+var_2C04]   ; sort_plan_usec
0xB52EAA  push    edx                         ; sort_plan_usec
0xB52EAB  mov     ecx, [esp+2C5Ch+var_2BC8]   ; sort_plan_sec
0xB52EB4  push    edx                         ; sort_plan_sec
0xB52EBF  mov     ecx, [esp+2C5Ch+var_2BD0]   ; msma_plan_sort_type
0xB52EC8  push    edx                         ; msma_plan_sort_type
0xB52EC9  mov     ecx, [esp+2C5Ch+var_2C20]   ; 计划列表基址
0xB52ED1  push    ebx                         ; count_plan
0xB52ED2  push    ecx                         ; 计划列表基址
0xB52ED3  mov     ecx, [esp+2C5Ch+var_2BC4]   ; 垃圾列表基址
0xB52EDF  push    ecx
0xB52EE0  mov     ecx, [esp+2C7Ch+var_2BF8]   ; 消耗列表基址
0xB52EEC  push    ecx
0xB52EED  mov     ecx, [esp+2C84h+var_2C18]   ; 主列表基址
0xB52EF9  push    ecx
...（各 sort_tm_* / slot_num_* 依次压栈）
0xB52F50  mov     edx, [eax+32Ch]              ; ← vt[0x32C]
0xB52F57  mov     ecx, esi
0xB52F59  call    edx
0xB52F5B  add     dword ptr [esi+4158h], 1     ; 接收计数自增
```
