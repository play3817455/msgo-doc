# 汇编证据 —— CS-0xE650-battle-msma_spawn_select

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0x00B33F30`（`0x00B33F30`..`0x00B34231`），函数 `sub_B33F30`
- 命令名字符串：`)<-_proto_battle_client::send_msma_spawn_select(` @ `0x00EE09C0`
- opcode 写入：`0x00B33FAC`
- 声明容量：`0x1A`（分配器容量 `push` @ `0x00B33F76`）
- 提交（`sub_B02FF0`）：`0x00B3409B`
- 发送去向：`vt[0x58]` @ `0x00B341C2`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00B33F7F  push    eax
  00B33F80  lea     ecx, [esp+4Ch+var_34]
  00B33F84  call    sub_ABB2F0   ; <<< 初始化 {cur,end}（游标自 buf+2 起）
  00B33F89  lea     ecx, [ebp+1Ah]
  00B33F8C  lea     eax, [ebp+2]
  00B33F8F  cmp     eax, ecx
  00B33F91  mov     [esp+48h+var_4], 0
  00B33F99  mov     [esp+48h+var_30], ebp
  00B33F9D  mov     dword ptr [esp+48h+var_2C], ecx
  00B33FA1  ja      loc_B3421C
  00B33FA7  lea     edx, [eax+4]
  00B33FAA  cmp     edx, ecx
  00B33FAC  mov     word ptr [ebp+0], 0E650h   ; <<< 内联写线（u16）
  00B33FB2  ja      loc_B3421C
  00B33FB8  mov     esi, [esp+48h+arg_0]
  00B33FBC  mov     [eax], esi   ; <<< 内联写线（u32）
  00B33FBE  mov     eax, edx
  00B33FC0  lea     edx, [eax+4]
  00B33FC3  cmp     edx, ecx
  00B33FC5  ja      loc_B3421C
  00B33FCB  mov     ecx, [esp+48h+arg_4]
  00B33FCF  mov     [esp+48h+var_30], edx
  00B33FD3  lea     edx, [esp+48h+var_30]
  00B33FD7  mov     [eax], ecx   ; <<< 内联写线（u32）
  00B33FD9  push    edx
  00B33FDA  lea     eax, [esp+4Ch+arg_8]
  00B33FDE  push    eax
  00B33FDF  call    sub_B02D80   ; <<< 写线原语 u32
  00B33FE4  add     esp, 8
  00B33FE7  test    al, al
  00B33FE9  jz      loc_B3421C
  00B33FEF  lea     ecx, [esp+48h+var_30]
  00B33FF3  push    ecx
  00B33FF4  lea     edx, [esp+4Ch+arg_C]
  00B33FF8  push    edx
  00B33FF9  call    sub_B061C0   ; <<< 写线原语 u8
  00B33FFE  add     esp, 8
  00B34001  test    al, al
  00B34003  jz      loc_B3421C
  00B34009  lea     eax, [esp+48h+var_30]
  00B3400D  push    eax
  00B3400E  lea     ecx, [esp+4Ch+arg_10]
  00B34012  push    ecx
  00B34013  call    sub_B061C0   ; <<< 写线原语 u8
  00B34018  add     esp, 8
  00B3401B  test    al, al
  00B3401D  jz      loc_B3421C
  00B34023  lea     edx, [esp+48h+var_30]
  00B34027  push    edx
  00B34028  lea     eax, [esp+4Ch+arg_14]
  00B3402C  push    eax
  00B3402D  call    sub_B02DA0   ; <<< 写线原语 u16
  00B34032  add     esp, 8
  00B34035  test    al, al
  00B34037  jz      loc_B3421C
  00B3403D  mov     esi, [edi+3D24h]
  00B34043  test    esi, esi
  00B34045  mov     ebx, [esp+48h+var_30]
  00B34049  jz      loc_B341C0
  00B3404F  lea     ecx, [esp+48h+var_28]
  00B34053  push    ecx
  00B34054  call    sub_CA0CE0
  00B34059  add     esp, 4
  00B3405C  mov     edx, [edi+8]
  00B3405F  push    offset aProtoBattleCli_215
  00B34064  push    edx
  00B34065  push    offset aId
  00B3406A  push    eax
  00B3406B  push    esi
  00B3406C  mov     byte ptr [esp+5Ch+var_4], 1
  00B34071  call    sub_B03020
  00B34076  add     esp, 8
  00B34079  push    eax
  00B3407A  call    sub_41D990
  00B3407F  add     esp, 8
  00B34082  mov     ecx, eax
  00B34084  call    sub_ADC810
  00B34089  push    eax
  00B3408A  call    sub_41D990
  00B3408F  add     esp, 8
  00B34092  lea     ecx, [esp+48h+var_28]
  00B34096  mov     byte ptr [esp+48h+var_4], 0
  00B3409B  call    sub_B02FF0   ; <<< 提交（C→S 闭合点）
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00B3409B  call    sub_B02FF0
  00B340A0  mov     eax, [esp+48h+arg_0]
  00B340A4  push    offset word_F641DC
  00B340A9  push    eax
  00B340AA  push    offset aMsIndex
  00B340AF  push    esi
  00B340B0  call    sub_41D990
  00B340B5  add     esp, 8
  00B340B8  mov     ecx, eax
  00B340BA  call    sub_B03580
  00B340BF  push    eax
  00B340C0  call    sub_41D990
  00B340C5  mov     ecx, [esp+50h+arg_4]
  00B340C9  add     esp, 8
  00B340CC  push    offset word_F641DC
  00B340D1  push    ecx
  00B340D2  push    offset aPostIndex_0
  00B340D7  push    esi
  00B340D8  call    sub_41D990
  00B340DD  add     esp, 8
  00B340E0  mov     ecx, eax
  00B340E2  call    sub_B03580
  00B340E7  push    eax
  00B340E8  call    sub_41D990
  00B340ED  mov     edx, [esp+50h+arg_8]
  00B340F1  add     esp, 8
  00B340F4  push    offset word_F641DC
  00B340F9  push    edx
  00B340FA  push    offset aSptSpotIndex
  00B340FF  push    esi
  00B34100  call    sub_41D990
  00B34105  add     esp, 8
  00B34108  mov     ecx, eax
  00B3410A  call    sub_B03580
  00B3410F  push    eax
  00B34110  call    sub_41D990
  00B34115  add     esp, 8
  00B34118  push    offset word_F641DC
  00B3411D  lea     eax, [esp+4Ch+arg_C]
  00B34121  push    eax
  00B34122  push    offset aIsBtlshipRide
  00B34127  push    esi
  00B34128  call    sub_41D990
  00B3412D  add     esp, 8
  00B34130  push    eax
  00B34131  call    sub_B0C1F0
  00B34136  add     esp, 8
  00B34139  push    eax
  00B3413A  call    sub_41D990
  00B3413F  add     esp, 8
  00B34142  push    offset word_F641DC
  00B34147  lea     ecx, [esp+4Ch+arg_10]
  00B3414B  push    ecx
  00B3414C  push    offset aIsMsmaRide
  00B34151  push    esi
  00B34152  call    sub_41D990
  00B34157  add     esp, 8
  00B3415A  push    eax
  00B3415B  call    sub_B0C1F0
  00B34160  add     esp, 8
  00B34163  push    eax
  00B34164  call    sub_41D990
  00B34169  mov     edx, [esp+50h+arg_14]
  00B3416D  add     esp, 8
  00B34170  push    edx
  00B34171  push    offset aRespawnEntId
  00B34176  push    esi
  00B34177  call    sub_41D990
  00B3417C  add     esp, 8
  00B3417F  mov     ecx, eax
  00B34181  call    sub_B032A0
  00B34186  push    offset aByte
  00B3418B  mov     eax, ebx
  00B3418D  sub     eax, ebp
  00B3418F  push    eax
  00B34190  push    offset asc_EDAD58
  00B34195  push    esi
  00B34196  call    sub_41D990
  00B3419B  add     esp, 8
  00B3419E  mov     ecx, eax
  00B341A0  call    sub_B03580
  00B341A5  push    eax
  00B341A6  call    sub_41D990
  00B341AB  add     esp, 8
  00B341AE  mov     esi, eax
  00B341B0  push    0Ah
  00B341B2  mov     ecx, esi
  00B341B4  call    sub_B036E0
  00B341B9  mov     ecx, esi
  00B341BB  call    sub_40DDF0
  00B341C0  mov     edx, [edi]
  00B341C2  mov     eax, [edx+58h]
```

## 4. 发送去向切片

```asm
  00B341C0  mov     edx, [edi]
  00B341C2  mov     eax, [edx+58h]
  00B341C5  sub     ebx, ebp
  00B341C7  push    ebx
  00B341C8  push    ebp
  00B341C9  mov     ecx, edi
  00B341CB  call    eax
  00B341CD  test    al, al
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `00B33FAC` | u16 / 2 |
| `ms_index` | `0xB33FB8`;`0xB33FBC` | u32 / 4 |
| `post_index` | `0xB33FCB`;`0xB33FD7` | u32 / 4 |
| `spt_spot_index` | `0xB33FDF` | u32 / 4 |
| `is_btlship_ride` | `0xB33FF9` | u8 / 1 |
| `is_msma_ride` | `0xB34013` | u8 / 1 |
| `respawn_ent_id` | `0xB3402D` | u16 / 2 |
