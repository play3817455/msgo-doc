# 汇编证据 —— SC-0x1113-battle-game_script_play

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 case 入口 + 解码缓冲申请（容量 `0x43`）+ 为 `src` 预留 65B 槽

```asm
; VA: 0xB0F127 .. 0xB0F172
0xB0F127  push    3Dh                      ; ← 本 case 错误码
0xB0F129  mov     ecx, esi
0xB0F12B  call    sub_B05DA0               ; case 起始守卫（不读线）
0xB0F130  test    al, al
0xB0F132  jz      loc_B317C7
0xB0F138  mov     ecx, [esi+0Ch]
0xB0F13B  mov     eax, [ecx]
0xB0F13D  mov     edx, [eax+78h]
0xB0F140  push    43h                      ; ← 容量 0x43 = 67 = 65 + 1 + 1
0xB0F142  call    edx
0xB0F144  mov     edi, eax                 ; edi = 缓冲基址
0xB0F14A  lea     ecx, [esp+1B40h+var_1930]
0xB0F151  call    sub_ABB2F0               ; 初始化线游标 {cur,end}
0xB0F156  mov     eax, edi
0xB0F158  push    41h                      ; ← src 串槽预算 65（同时是 sub_B02BA0 的 maxlen）
0xB0F15A  lea     ecx, [esp+1B40h+var_1B28] ; &线游标
0xB0F15E  push    ecx
0xB0F15F  add     edi, 41h                 ; 缓冲游标推过 65B 槽
0xB0F162  push    eax                      ; dst = 缓冲基址
0xB0F16E  mov     [esp+1B48h+var_1B08], eax ; ← 保存 src 串首地址（去向实参用）
0xB0F172  mov     [esp+1B48h+var_1B14], edi
```

## E2 字段 1：`src`（NUL 串，偏移 0，预算 65）

```asm
; VA: 0xB0F176 .. 0xB0F180
0xB0F176  call    sub_B02BA0               ; ← 读 NUL 串：消费 = strlen+1 ≤ 65
0xB0F17B  add     esp, 0Ch
0xB0F17E  test    al, al
0xB0F180  jnz     short loc_B0F19B         ; 成功分支
```

## E3 字段 2：`is_with_resume`（u8）

```asm
; VA: 0xB0F19B .. 0xB0F1BD
0xB0F19B  lea     ecx, [esp+1B3Ch+var_1B14] ; 缓冲游标指针
0xB0F19F  push    ecx
0xB0F1A0  lea     ecx, [esp+1B40h+var_1B20] ; 槽
0xB0F1A4  call    sub_B05E30               ; 预留 1B（非字段）
0xB0F1A9  mov     eax, [esp+1B3Ch+var_1B20]
0xB0F1AD  lea     edx, [esp+1B3Ch+var_1B28] ; &线游标
0xB0F1B1  push    edx
0xB0F1B2  push    eax
0xB0F1B3  call    sub_B06230               ; ← 读 u8
0xB0F1BD  jz      short loc_B0F182         ; 失败 ⇒ 报错
```

## E4 字段 3：`script_thread`（u8）

```asm
; VA: 0xB0F1BF .. 0xB0F1E1
0xB0F1BF  lea     ecx, [esp+1B3Ch+var_1B14]
0xB0F1C3  push    ecx
0xB0F1C4  lea     ecx, [esp+1B40h+var_1B2C] ; 槽
0xB0F1C8  call    sub_B05E30               ; 预留 1B（非字段）
0xB0F1CD  mov     eax, [esp+1B3Ch+var_1B2C]
0xB0F1D1  lea     edx, [esp+1B3Ch+var_1B28]
0xB0F1D5  push    edx
0xB0F1D6  push    eax
0xB0F1D7  call    sub_B06230               ; ← 读 u8
0xB0F1E1  jz      short loc_B0F182         ; 失败 ⇒ 报错
```

## E5 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB0F1E3 .. 0xB0F1EF
0xB0F1E3  mov     ebx, [esp+1B3Ch+var_1B28] ; 读完后的线游标
0xB0F1E7  cmp     ebx, [esp+1B3Ch+var_1B24] ; vs 报文末尾
0xB0F1EB  mov     ecx, esi
0xB0F1ED  jz      short loc_B0F206          ; ← 不等 ⇒ push 3Dh 报错
```

## E6 含义取证：块内日志 `src="` / `is_with_resume=` / `script_thread=`

```asm
; VA: 0xB0F274 .. 0xB0F2E1
0xB0F274  mov     eax, [esp+1B3Ch+var_1B08] ; src 串首地址
0xB0F278  push    offset word_F641DC         ; ","
0xB0F27D  push    offset asc_EDAD54         ; "\""
0xB0F282  push    eax
0xB0F283  push    offset aSrc               ; ← "src=\""
0xB0F2A9  mov     ecx, [esp+1B44h+var_1B20] ; is_with_resume 槽
0xB0F2B6  push    offset aIsWithResume      ; ← "is_with_resume="
0xB0F2D3  mov     edx, [esp+1B44h+var_1B2C] ; script_thread 槽
0xB0F2DB  push    offset aScriptThread      ; ← "script_thread="
```

## E7 去向：`vt[0x10C](src, is_with_resume, script_thread)`

```asm
; VA: 0xB0F325 .. 0xB0F346
0xB0F325  mov     ecx, [esp+1B3Ch+var_1B2C] ; script_thread 槽
0xB0F329  movzx   edx, byte ptr [ecx]
0xB0F32C  mov     ecx, [esp+1B3Ch+var_1B20] ; is_with_resume 槽
0xB0F330  mov     eax, [esi]
0xB0F332  push    edx                       ; 实参 3 = script_thread
0xB0F333  movzx   edx, byte ptr [ecx]
0xB0F336  mov     ecx, [esp+1B40h+var_1B08] ; src 串首地址
0xB0F33A  push    edx                       ; 实参 2 = is_with_resume
0xB0F33B  mov     edx, [eax+10Ch]           ; ← vt[0x10C]
0xB0F341  push    ecx                       ; 实参 1 = src
0xB0F342  mov     ecx, esi
0xB0F344  call    edx
0xB0F346  add     dword ptr [esi+0E50h], 1   ; 本命令接收计数（64 位）
0xB0F354  adc     dword ptr [esi+0E54h], 0
```
