# 汇编证据 —— SC-0x0587-lounge-pilot_dailyrecord_notice

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 case 入口 + 解码缓冲申请（容量 `1`）

```asm
; VA: 0xB5351A .. 0xB53542
0xB5351A  call    sub_B41120               ; lounge case 收尾/开关
0xB5351F  test    al, al
0xB53521  jz      loc_B890FE
0xB53527  mov     ecx, [esi+0Ch]
0xB5352A  mov     eax, [ecx]
0xB5352C  mov     edx, [eax+78h]           ; vt[0x78] = 申请解码缓冲
0xB5352F  push    1                        ; ← 容量 1（= 负载长）
0xB53531  call    edx
0xB53533  mov     [esp+2C5Ch+var_2C3C], eax ; 缓冲基址
0xB53537  mov     eax, [esi+0Ch]
0xB5353A  push    eax
0xB5353B  lea     ecx, [esp+2C60h+var_2688]
0xB53542  call    sub_ABB2F0               ; 初始化 {cur,end} 读游标
```

## E2 唯一字段：`is_open_info`（u8）

```asm
; VA: 0xB53547 .. 0xB5356F
0xB53547  lea     ecx, [esp+2C5Ch+var_2C3C]
0xB5354B  push    ecx                      ; arg_0 = &缓冲游标
0xB5354C  lea     ecx, [esp+2C60h+var_2C48] ; this = &槽
0xB53550  mov     [esp+2C60h+var_4], 7Ch
0xB5355B  call    sub_B05E30               ; 缓冲预留 1B（游标 +1，**非字段**）
0xB53560  mov     eax, [esp+2C5Ch+var_2C48]
0xB53564  lea     edx, [esp+2C5Ch+var_2C44] ; 读游标
0xB53568  push    edx
0xB53569  push    eax
0xB5356A  call    sub_B06230               ; ← 读 u8（带「剩余 ≥ 1」边界检查）
```

宽度判定依据（读原语本体）：

```asm
; VA: 0xB06230 .. 0xB0624E
0xB06230  mov     eax, [esp+arg_4]
0xB06234  mov     ecx, [eax]
0xB06236  lea     edx, [ecx+1]             ; ← 需要 1 字节
0xB06239  cmp     edx, [eax+4]
0xB0623C  jbe     short loc_B06241
0xB0623E  xor     al, al
0xB06240  retn
0xB06241  mov     cl, [ecx]                ; ← 取 1 字节
0xB06243  mov     edx, [esp+arg_0]
0xB06247  mov     [edx], cl
0xB06249  add     dword ptr [eax], 1       ; ← 游标 +1
0xB0624C  mov     al, 1
0xB0624E  retn
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB5358F .. 0xB53597
0xB5358F  mov     ebx, [esp+2C5Ch+var_2C44]   ; 读完后的游标
0xB53593  cmp     ebx, [esp+2C5Ch+var_2C40]   ; vs 报文末尾
0xB53597  jnz     short loc_B53578            ; ← 不等 ⇒ push 6Dh 报错
```

## E4 含义取证：trace 日志 `is_open_info=`

```asm
; VA: 0xB535BA .. 0xB5361B（节选）
0xB535BD  push    offset aProtoLoungeCli_8   ; ")->_proto_lounge_client::recv_pilot_dai…"
0xB535C3  push    offset aId                 ; " (id:"
0xB5360B  push    eax
0xB5360C  push    offset aIsOpenInfo         ; ← "is_open_info="
0xB5361B  call    sub_B0C1F0                ; 单字节/布尔打印器（与十进制/十六进制打印器不同）
```

## E5 去向：`vt[0x160]`（零扩展 u8 作 32 位实参）

```asm
; VA: 0xB53656 .. 0xB53678
0xB53656  mov     eax, [esp+2C5Ch+var_2C48]   ; 槽地址
0xB5365A  movzx   ecx, byte ptr [eax]          ; ← 零扩展（线上 1 字节）
0xB5365D  mov     edx, [esi]
0xB5365F  mov     edx, [edx+160h]              ; ← vt[0x160]
0xB53665  push    ecx
0xB53666  mov     ecx, esi
0xB53668  call    edx
0xB5366A  add     dword ptr [esi+19C8h], 1     ; 本命令接收计数（64 位）
0xB53678  adc     dword ptr [esi+19CCh], 0
```
