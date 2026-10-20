# 汇编证据 —— SC-0x12EC-battle-room_chat_down

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 case 入口 + 解码缓冲申请（容量 `0xDB`）

```asm
; VA: 0xB0F774 .. 0xB0F7A3
0xB0F774  push    28h                      ; ← 本 case 错误码
0xB0F776  mov     ecx, esi
0xB0F778  call    sub_B05DA0               ; case 起始守卫（不读线）
0xB0F77D  test    al, al
0xB0F77F  jz      loc_B317C7
0xB0F785  mov     ecx, [esi+0Ch]
0xB0F788  mov     eax, [ecx]
0xB0F78A  mov     edx, [eax+78h]
0xB0F78D  push    0DBh                     ; ← 容量 219 = 1+1+4+4+25+181+1+1+1
0xB0F792  call    edx
0xB0F794  mov     [esp+1B3Ch+var_1B1C], eax ; 解码缓冲基址（串缓冲起点）
```

## E2 字段 1/2：`team`（u8@0）、`troops`（u8@1）

```asm
; VA: 0xB0F7BC .. 0xB0F812
0xB0F7BC  call    sub_B05E30               ; u8 槽预留（非字段）
0xB0F7CB  call    sub_B06230               ; ← 读 u8（消费 1）→ team
0xB0F7F9  call    sub_B05E30               ; u8 槽预留（非字段）
0xB0F808  call    sub_B06230               ; ← 读 u8（消费 1）→ troops
```

## E3 字段 3/4：`world_id`（u32@2）、`pilot_id`（u32@6）

```asm
; VA: 0xB0F81D .. 0xB0F858
0xB0F81D  call    sub_B41470               ; u32 槽预留（非字段）
0xB0F82C  call    sub_B02DD0               ; ← 读 u32（消费 4）→ world_id
0xB0F841  call    sub_B41470               ; u32 槽预留（非字段）
0xB0F850  call    sub_B02DD0               ; ← 读 u32（消费 4）→ pilot_id
```

## E4 字段 5/6：两个 NUL 串（`pilot_name` 槽 25、`msg` 槽 181）

```asm
; VA: 0xB0F860 .. 0xB0F8A8
0xB0F860  mov     edi, [esp+1B3Ch+var_1B1C] ; 串缓冲基址
0xB0F864  mov     eax, edi
0xB0F866  push    19h                      ; ← 串 1 槽位预算 25
0xB0F868  lea     ecx, [esp+1B40h+var_1B28] ; &线游标
0xB0F86C  push    ecx
0xB0F86D  push    eax                       ; 目标 = 缓冲基址
0xB0F86E  mov     [esp+1B48h+var_1B08], eax ; 记下 pilot_name 指针
0xB0F872  add     edi, 19h
0xB0F875  call    sub_B02BA0               ; ← 读 NUL 串（消费 = 串长+1，上限 25）
0xB0F885  mov     eax, edi                  ; 目标 = 缓冲基址 + 0x19
0xB0F887  push    0B5h                     ; ← 串 2 槽位预算 181
0xB0F891  add     edi, 0B5h
0xB0F898  mov     [esp+1B48h+var_1B14], eax ; 记下 msg 指针
0xB0F8A0  call    sub_B02BA0               ; ← 读 NUL 串（消费 = 串长+1，上限 181）
```

```asm
; sub_B02BA0 函数体（0xB02BA0 .. 0xB02BF4）：变长串读取
0xB02BA0  mov     edx, [esp+arg_8]         ; maxlen
0xB02BA9  mov     ecx, [edi]               ; 游标 cur
0xB02BAB  mov     eax, [edi+4]
0xB02BAE  sub     eax, ecx                 ; remaining
0xB02BB0  cmp     edx, eax
0xB02BB2  jge     short loc_B02BB6
0xB02BB4  mov     eax, edx                 ; 扫描上限 = min(maxlen, remaining)
0xB02BC3  call    sub_CC8400               ; 找 NUL
0xB02BDC  add     esi, 1                   ; ← 含 NUL 字节
0xB02BEE  mov     [edi], esi               ; 游标推进到 NUL 之后
```

## E5 字段 7/8/9：`is_all`、`is_party`、`is_audience`（各 u8）

```asm
; VA: 0xB0F8B0 .. 0xB0F922
0xB0F8B9  call    sub_B05E30               ; u8 槽预留
0xB0F8C8  call    sub_B06230               ; ← 读 u8 → is_all
0xB0F8E1  call    sub_B05E30
0xB0F8F0  call    sub_B06230               ; ← 读 u8 → is_party
0xB0F909  call    sub_B05E30
0xB0F918  call    sub_B06230               ; ← 读 u8 → is_audience
```

## E6 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB0F928 .. 0xB0F93D
0xB0F928  mov     ebx, [esp+1B3Ch+var_1B28] ; 读完后的线游标
0xB0F92C  cmp     ebx, [esp+1B3Ch+var_1B24] ; vs 报文末尾
0xB0F932  jz      short loc_B0F94B         ; ← 不等 ⇒ push 1 / push 28h 报错
```

## E7 含义取证：块内日志（9 个字段名一一对位）

```asm
; VA: 0xB0F9B9 .. 0xB0FB30
0xB0F9BD  push    offset word_F641DC
0xB0F9C3  push    offset aTeam             ; ← "team="
0xB0F9D2  call    sub_B0C1F0               ; 1 字节打印器（仅打印用 movsx）
0xB0F9ED  push    offset aTroops           ; ← "troops="
0xB0FA19  push    offset aWorldId          ; ← "world_id="
0xB0FA43  push    offset aPilotId          ; ← "pilot_id="
0xB0FA70  push    offset aPilotName        ; ← "pilot_name=\""
0xB0FAA8  push    offset aMsg              ; ← "msg=\""
0xB0FADB  push    offset aIsAll            ; ← "is_all="
0xB0FB05  push    offset aIsParty          ; ← "is_party="
0xB0FB2A  push    offset aIsAudience       ; ← "is_audience="
```

## E8 去向：`vt[0xD4](team, troops, world_id, pilot_id, pilot_name, msg, is_all, is_party, is_audience)`

```asm
; VA: 0xB0FB74 .. 0xB0FBD5
0xB0FB74  mov     eax, [esp+1B3Ch+var_1B2C] ; is_audience 槽
0xB0FB78  movzx   ecx, byte ptr [eax]       ; ← 零扩展
0xB0FB7F  push    ecx                       ; 实参 9 = is_audience
0xB0FB87  push    ecx                       ; 实参 8 = is_party
0xB0FB91  push    ecx                       ; 实参 7 = is_all
0xB0FB9C  push    eax                       ; 实参 6 = msg 指针
0xB0FBA1  push    ecx                       ; 实参 5 = pilot_name 指针
0xB0FBA8  push    ecx                       ; 实参 4 = pilot_id
0xB0FBAF  push    ecx                       ; 实参 3 = world_id
0xB0FBB7  push    ecx                       ; 实参 2 = troops
0xB0FBBB  push    ecx                       ; 实参 1 = team
0xB0FBBE  call    edx                       ; edx = [esi]+0D4h ⇒ vt[0xD4]
0xB0FBC0  add     dword ptr [esi+0A60h], 1  ; 本命令接收计数（64 位）
```
