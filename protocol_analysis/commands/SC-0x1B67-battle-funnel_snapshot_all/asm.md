# 汇编证据 —— SC-0x1B67-battle-funnel_snapshot_all

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x4E4` @ `0xB11082`）

```asm
; VA: 0xB1106D .. （块入口，含守卫与容量申请）
00B1106D  call    sub_B05DA0
00B11072  test    al, al
00B11074  jz      loc_B317C7
00B1107A  mov     ecx, [esi+0Ch]
00B1107D  mov     eax, [ecx]
00B1107F  mov     edx, [eax+78h]
00B11082  push    4E4h
00B11087  call    edx
00B11089  mov     [esp+1B3Ch+var_1B14], eax
00B1108D  mov     eax, [esi+0Ch]
00B11090  push    eax
00B11091  lea     ecx, [esp+1B40h+var_1830]
00B11098  call    sub_ABB2F0
00B1109D  lea     ecx, [esp+1B3Ch+var_1B28]
```

## E2 字段 1：`snapshot_num`（u32，偏移 0，长度 4）

```asm
; VA: 0x0xB110B2 附近（随附快照条目数 N）
00B110A1  push    ecx
00B110A2  lea     edx, [esp+1B40h+var_1B20]
00B110A6  push    edx
00B110A7  mov     [esp+1B44h+var_4], 0B5h
00B110B2  call    sub_B02DD0
00B110B7  add     esp, 8
00B110BA  test    al, al
00B110BC  jnz     short loc_B110DA
00B110BE  mov     eax, [esi]
00B110C0  mov     edx, [eax+64h]
```

## E3 字段 2：`snapshot_arr`（array<elem 10>，偏移 4，长度 10·N）

```asm
; VA: 0x0xB1110A 附近（快照数组（元素线上 10B / 缓冲槽步进 12B））
00B11100  mov     eax, [esp+1B3Ch+var_1B2C]
00B11104  lea     edx, [esp+1B3Ch+var_1B28]
00B11108  push    edx
00B11109  push    eax
00B1110A  call    sub_B081C0
00B1110F  add     esp, 8
00B11112  test    al, al
00B11114  jz      short loc_B11124
00B11116  add     [esp+1B3Ch+var_1B2C], 0Ch
00B1111B  add     edi, 1
```

## E4 字段 3：`snapshot_arr.ent_id`（u32，偏移 +0，长度 4）

```asm
; VA: 0x0xB081CE 附近（快照所属实体 ID）
00B1106D  call    sub_B05DA0
00B11072  test    al, al
00B11074  jz      loc_B317C7
00B1107A  mov     ecx, [esi+0Ch]
00B1107D  mov     eax, [ecx]
00B1107F  mov     edx, [eax+78h]
```

## E5 字段 4：`snapshot_arr.wslot_idx`（i8，偏移 +4，长度 1）

```asm
; VA: 0x0xB081E4 附近（武器槽下标）
00B1106D  call    sub_B05DA0
00B11072  test    al, al
00B11074  jz      loc_B317C7
00B1107A  mov     ecx, [esi+0Ch]
00B1107D  mov     eax, [ecx]
00B1107F  mov     edx, [eax+78h]
```

## E6 字段 5：`snapshot_arr.move_info`（bytes[5]，偏移 +5，长度 5）

```asm
; VA: 0x0xB081FB 附近（移动/姿态信息（定长 5B））
00B1106D  call    sub_B05DA0
00B11072  test    al, al
00B11074  jz      loc_B317C7
00B1107A  mov     ecx, [esi+0Ch]
00B1107D  mov     eax, [ecx]
00B1107F  mov     edx, [eax+78h]
```

## E7 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB11138
00B11126  mov     eax, [edx+64h]
00B11129  push    1
00B1112B  push    96h
00B11130  mov     ecx, esi
00B11132  call    eax
00B11134  mov     ecx, [esp+1B3Ch+var_1B28]
00B11138  cmp     ecx, [esp+1B3Ch+var_1B24]
00B1113C  mov     ecx, esi
00B1113E  jz      short loc_B1115A
00B11140  mov     edx, [esi]
00B11142  mov     eax, [edx+64h]
00B11145  push    1
00B11147  push    96h
00B1114C  call    eax
```
