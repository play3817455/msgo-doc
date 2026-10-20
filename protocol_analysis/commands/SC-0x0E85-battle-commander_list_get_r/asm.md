# 汇编证据 —— SC-0x0E85-battle-commander_list_get_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 case 入口 + 解码缓冲申请（容量 `0x18`）

```asm
; VA: 0xB0EC1F .. 0xB0EC4E
0xB0EC1F  push    0D2h                     ; ← 本 case 错误码
0xB0EC24  mov     ecx, esi
0xB0EC26  call    sub_B05DA0               ; case 起始守卫（不读线）
0xB0EC2B  test    al, al
0xB0EC2D  jz      loc_B317C7
0xB0EC33  mov     ecx, [esi+0Ch]
0xB0EC36  mov     eax, [ecx]
0xB0EC38  mov     edx, [eax+78h]
0xB0EC3B  push    18h                      ; ← 容量 0x18 = 24 = 8 + 4×4（上限场景线长）
0xB0EC3D  call    edx
0xB0EC3F  mov     [esp+1B3Ch+var_1B14], eax
0xB0EC47  lea     ecx, [esp+1B40h+var_1908]
0xB0EC4E  call    sub_ABB2F0               ; 初始化线游标 {cur,end}
```

## E2 字段 1：`result`（u32，偏移 0）

```asm
; VA: 0xB0EC53 .. 0xB0EC80
0xB0EC53  lea     ecx, [esp+1B3Ch+var_1B14]
0xB0EC57  push    ecx
0xB0EC58  lea     ecx, [esp+1B40h+var_1B20] ; 槽
0xB0EC67  call    sub_B41470               ; 缓冲预留 4B（非字段）
0xB0EC6C  mov     eax, [esp+1B3Ch+var_1B20]
0xB0EC70  lea     edx, [esp+1B3Ch+var_1B28] ; &线游标
0xB0EC74  push    edx
0xB0EC75  push    eax
0xB0EC76  call    sub_B02DD0               ; ← 读 u32
0xB0EC7B  add     esp, 8
0xB0EC7E  test    al, al
0xB0EC80  jnz     short loc_B0EC9E         ; 成功分支
```

## E3 字段 2：`count`（u32，偏移 4）+ 上限检查 `≤ 4`

```asm
; VA: 0xB0EC9E .. 0xB0ECD7
0xB0EC9E  lea     ecx, [esp+1B3Ch+var_1B28]
0xB0ECA2  push    ecx
0xB0ECA3  lea     edx, [esp+1B40h+var_1B08] ; 槽
0xB0ECA8  call    sub_B02DD0               ; ← 读 u32（计数）
0xB0ECAD  add     esp, 8
0xB0ECB0  test    al, al
0xB0ECB2  jnz     short loc_B0ECD0         ; 成功分支
0xB0ECD0  mov     ebx, [esp+1B3Ch+var_1B08]
0xB0ECD4  cmp     ebx, 4                   ; ← 计数上限 4
0xB0ECD7  ja      short loc_B0ECB4         ; > 4 ⇒ 报错
```

## E4 字段 3：数组预留 `sub_B41850`（4B/槽，非字段）

```asm
; VA: 0xB0ECD9 .. 0xB0ECE8
0xB0ECD9  push    ebx                      ; 元素个数 N
0xB0ECDA  lea     eax, [esp+1B40h+var_1B14] ; 解码缓冲游标
0xB0ECDE  push    eax
0xB0ECDF  lea     ecx, [esp+1B44h+var_1B08] ; 输出：数组基址
0xB0ECE3  call    sub_B41850               ; 预留 N×4 字节（推进缓冲游标，不是字段）
0xB0ECE8  xor     edi, edi
0xB0ECEA  test    ebx, ebx
0xB0ECEC  jbe     short loc_B0ED2A         ; N == 0 ⇒ 无数组字节
```

## E5 字段 3 的元素读取（u32 × N，线长 4/元素）

```asm
; VA: 0xB0ECEE .. 0xB0ED18
0xB0ECEE  mov     ecx, [esp+1B3Ch+var_1B08] ; 数组基址
0xB0ECF2  mov     [esp+1B3Ch+var_1B2C], ecx
0xB0ECF6  mov     eax, [esp+1B3Ch+var_1B2C] ; 元素槽
0xB0ECFA  lea     edx, [esp+1B3Ch+var_1B28] ; &线游标
0xB0ECFE  push    edx
0xB0ECFF  push    eax
0xB0ED00  call    sub_B02DD0               ; ← 读 u32
0xB0ED05  add     esp, 8
0xB0ED08  test    al, al
0xB0ED0A  jz      short loc_B0ED1A         ; 失败 ⇒ 报错
0xB0ED0C  add     [esp+1B3Ch+var_1B2C], 4  ; ← 元素槽步进 4
0xB0ED11  add     edi, 1
0xB0ED14  cmp     edi, ebx                 ; 循环 N 次
0xB0ED16  jb      short loc_B0ECF6
```

## E6 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB0ED2A .. 0xB0ED36
0xB0ED2A  mov     ecx, [esp+1B3Ch+var_1B28] ; 读完后的线游标
0xB0ED2E  cmp     ecx, [esp+1B3Ch+var_1B24] ; vs 报文末尾
0xB0ED34  jz      short loc_B0ED50          ; ← 不等 ⇒ push 0D2h 报错
```

## E7 含义取证：块内日志 `result=` 与 `commander_id={...}`

```asm
; VA: 0xB0EDC1 .. 0xB0EE4B
0xB0EDC1  mov     eax, [esp+1B3Ch+var_1B20]
0xB0EDC5  mov     ecx, [eax]                ; result
0xB0EDCD  push    offset aResult            ; ← "result="
0xB0EDE8  push    offset aCommanderId       ; ← "commander_id={"
0xB0EDF6  test    ebx, ebx
0xB0EDF8  jbe     short loc_B0EE08
0xB0EDFA  mov     edx, [esp+1B3Ch+var_1B08] ; 数组基址
0xB0EDFE  mov     eax, [edx]                ; 元素 0
0xB0EE03  call    sub_B03580                ; 十进制打印
0xB0EE15  mov     ecx, [esp+1B3Ch+var_1B08]
0xB0EE19  mov     edx, [esp+1B3Ch+var_1B2C] ; 元素下标
0xB0EE1D  mov     eax, [ecx+edx*4]          ; ← 元素线长 4（下标 × 4）
0xB0EE21  push    offset word_F641DC        ; ","
0xB0EE45  push    offset unk_EDABE4         ; "}"
```

## E8 去向：`vt[0x290](result, commander_id 数组, count)`

```asm
; VA: 0xB0EE8A .. 0xB0EEA3
0xB0EE8A  mov     eax, [esp+1B3Ch+var_1B08] ; 数组基址
0xB0EE8E  mov     ecx, [esp+1B3Ch+var_1B20] ; result 槽
0xB0EE92  mov     edx, [esi]
0xB0EE94  mov     edx, [edx+290h]           ; ← vt[0x290]
0xB0EE9A  push    ebx                       ; 实参 3 = count
0xB0EE9B  push    eax                       ; 实参 2 = 数组基址
0xB0EE9C  mov     eax, [ecx]                ; result
0xB0EE9E  push    eax                       ; 实参 1 = result
0xB0EE9F  mov     ecx, esi
0xB0EEA1  call    edx
0xB0EEA3  add     dword ptr [esi+2A40h], 1   ; 本命令接收计数（64 位）
0xB0EEB1  adc     dword ptr [esi+2A44h], 0
```
