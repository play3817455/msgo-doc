# 汇编证据 —— SC-0x1146-auth-worldlist_select_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 case 入口 + 解码缓冲申请（容量 `0xE7`）+ 线游标初始化

```asm
; VA: 0xB04068 .. 0xB04095
0xB04068  push    0Dh                      ; ← 本 case 错误码
0xB0406A  call    sub_B02C90               ; auth case 起始守卫（不读线）
0xB0406F  test    al, al
0xB04071  jz      loc_B04C46
0xB04077  mov     ecx, [esi+0Ch]
0xB0407A  mov     eax, [ecx]
0xB0407C  mov     edx, [eax+78h]
0xB0407F  push    0E7h                     ; ← 容量 0xE7 = 231 = 4+49+129+4+4+41
0xB04084  call    edx
0xB04086  mov     ebp, eax                 ; ebp = 缓冲游标（auth 用手工推进）
0xB0408B  push    eax
0xB0408C  lea     ecx, [esp+128h+var_110]
0xB04090  call    sub_ABB2F0               ; 初始化线游标 {cur,end}
```

## E2 字段 1：`result`（u32，偏移 0）

```asm
; VA: 0xB04095 .. 0xB040B9
0xB04095  mov     eax, ebp
0xB04097  lea     ecx, [esp+124h+var_10C]  ; &线游标
0xB0409B  push    ecx
0xB0409C  push    eax                      ; dst
0xB040A8  mov     [esp+12Ch+var_100], eax  ; 保存槽地址（日志/去向取值用）
0xB040AC  add     ebp, 4                   ; 缓冲游标 +4
0xB040AF  call    sub_B02DD0               ; ← 读 u32
0xB040B4  add     esp, 8
0xB040B7  test    al, al
0xB040B9  jnz     short loc_B040C4         ; 成功分支
```

## E3 字段 2：`world_name_en`（NUL 串，预算 `0x31`）

```asm
; VA: 0xB040C4 .. 0xB040DF
0xB040C4  mov     eax, ebp
0xB040C6  push    31h                      ; ← 串槽预算 49（含 NUL）
0xB040C8  lea     ecx, [esp+128h+var_10C]  ; &线游标
0xB040CC  push    ecx
0xB040CD  push    eax
0xB040CE  mov     [esp+130h+var_F4], eax   ; 保存槽地址
0xB040D2  add     ebp, 31h                 ; 缓冲游标 += 49
0xB040D5  call    sub_B02BA0               ; ← 读 NUL 串：消费 = strlen+1
0xB040DA  add     esp, 0Ch
0xB040DD  test    al, al
0xB040DF  jz      short loc_B040BB         ; 失败 ⇒ 报错
```

## E4 字段 3：`loungesv_host`（NUL 串，预算 `0x81`）

```asm
; VA: 0xB040E1 .. 0xB04102
0xB040E1  mov     eax, ebp
0xB040E3  push    81h                      ; ← 串槽预算 129（含 NUL）
0xB040E8  lea     ecx, [esp+128h+var_10C]
0xB040EC  push    ecx
0xB040ED  push    eax
0xB040EE  mov     [esp+130h+var_F8], eax   ; 保存槽地址
0xB040F2  add     ebp, 81h                 ; 缓冲游标 += 129
0xB040F8  call    sub_B02BA0               ; ← 读 NUL 串
0xB040FD  add     esp, 0Ch
0xB04100  test    al, al
0xB04102  jz      short loc_B040BB
```

## E5 字段 4：`loungesv_port`（u32，偏移可变）

```asm
; VA: 0xB04104 .. 0xB0411B
0xB04104  mov     eax, ebp
0xB04106  lea     ecx, [esp+124h+var_10C]
0xB0410A  push    ecx
0xB0410B  push    eax
0xB0410C  mov     [esp+12Ch+var_104], eax  ; 保存槽地址
0xB04110  add     ebp, 4
0xB04113  call    sub_B02DD0               ; ← 读 u32
0xB0411B  test    al, al
0xB0411D  jz      short loc_B040BB
```

## E6 字段 5：`userid`（u32，偏移可变）

```asm
; VA: 0xB0411F .. 0xB04136
0xB0411F  mov     eax, ebp
0xB04121  lea     ecx, [esp+124h+var_10C]
0xB04125  push    ecx
0xB04126  push    eax
0xB04127  mov     [esp+12Ch+var_F0], eax   ; 保存槽地址
0xB0412B  add     ebp, 4
0xB0412E  call    sub_B02DD0               ; ← 读 u32
0xB04136  test    al, al
0xB04138  jz      short loc_B040BB
```

## E7 字段 6：`otp`（NUL 串，预算 `0x29`，最后一个字段）

```asm
; VA: 0xB0413A .. 0xB0414C
0xB0413A  push    29h                      ; ← 串槽预算 41（含 NUL）
0xB0413C  lea     ecx, [esp+128h+var_10C]  ; &线游标
0xB04140  push    ecx
0xB04141  push    ebp                      ; dst = 当前缓冲游标（此后不再推进）
0xB04142  call    sub_B02BA0               ; ← 读 NUL 串
0xB0414A  test    al, al
0xB0414C  jz      loc_B040BB
```

## E8 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB04152 .. 0xB0415C
0xB04152  mov     ebx, [esp+124h+var_10C]  ; 读完后的线游标
0xB04156  cmp     ebx, [esp+124h+var_108]  ; vs 报文末尾
0xB0415A  jnz     loc_B040BB               ; ← 不等 ⇒ push 0Dh 报错
```

## E9 含义取证：块内 6 条日志（顺序与线序一致）

```asm
; VA: 0xB041C5 .. 0xB042BF
0xB041C5  mov     eax, [esp+124h+var_100]  ; result 槽
0xB041D1  push    offset aResult           ; ← "result="
0xB041EC  mov     edx, [esp+12Ch+var_F4]   ; world_name_en 槽
0xB041FE  push    offset aWorldNameEn      ; ← "world_name_en=\""
0xB04224  mov     eax, [esp+12Ch+var_F8]   ; loungesv_host 槽
0xB04236  push    offset aLoungesvHost     ; ← "loungesv_host=\""
0xB0425C  mov     ecx, [esp+12Ch+var_104]  ; loungesv_port 槽
0xB0426B  push    offset aLoungesvPort     ; ← "loungesv_port="
0xB04286  mov     eax, [esp+12Ch+var_F0]   ; userid 槽
0xB04295  push    offset aUserid           ; ← "userid="
0xB042B3  push    offset asc_EDAD54        ; "\""
0xB042B9  push    offset aOtp              ; ← "otp=\""
```

## E10 去向：`vt[0x80](result, world_name_en, loungesv_host, loungesv_port, userid, otp)`

```asm
; VA: 0xB04316 .. 0xB04342
0xB04316  mov     eax, [esp+124h+var_F0]   ; userid 槽
0xB0431A  mov     ecx, [eax]               ; ecx = userid
0xB0431C  mov     eax, [esp+124h+var_104]  ; loungesv_port 槽
0xB04320  mov     edx, [esi]
0xB04322  mov     edx, [edx+80h]           ; ← vt[0x80]
0xB04328  push    ebp                      ; 实参 6 = otp（串首地址 = 当前缓冲游标）
0xB04329  push    ecx                      ; 实参 5 = userid
0xB0432A  mov     ecx, [eax]               ; ecx = loungesv_port
0xB0432C  mov     eax, [esp+12Ch+var_F8]   ; loungesv_host 槽
0xB04330  push    ecx                      ; 实参 4 = loungesv_port
0xB04331  mov     ecx, [esp+130h+var_F4]   ; world_name_en 槽
0xB04335  push    eax                      ; 实参 3 = loungesv_host
0xB04336  mov     eax, [esp+134h+var_100]  ; result 槽
0xB0433A  push    ecx                      ; 实参 2 = world_name_en
0xB0433B  mov     ecx, [eax]               ; ecx = result
0xB0433D  push    ecx                      ; 实参 1 = result
0xB0433E  mov     ecx, esi
0xB04340  call    edx
0xB04342  add     dword ptr [esi+310h], 1  ; 本命令接收计数（64 位）
0xB04349  adc     dword ptr [esi+314h], 0
```

> 注：`0xB04160 mov edi,[esi+3BCh]` / `0xB04166 test edi,edi` / `0xB04168 jz loc_B04316` —— 日志对象为空则**跳过整段日志**，
> 但合流点 `0xB04316` 位于 `call vt[0x80]` **之前**，故业务去向与日志开关无关。
