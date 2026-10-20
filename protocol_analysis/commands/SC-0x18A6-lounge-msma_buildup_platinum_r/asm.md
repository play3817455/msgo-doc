# 汇编证据 —— SC-0x18A6-lounge-msma_buildup_platinum_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x2A` @ `0xB562B3`）

```asm
; VA: 0xB56297 .. （块入口，含守卫与容量申请）
00B56297  push    108h
00B5629C  mov     ecx, esi
00B5629E  call    sub_B41120
00B562A3  test    al, al
00B562A5  jz      loc_B890FE
00B562AB  mov     ecx, [esi+0Ch]
00B562AE  mov     eax, [ecx]
00B562B0  mov     edx, [eax+78h]
00B562B3  push    2Ah ; '*'
00B562B5  call    edx
00B562B7  mov     [esp+2C5Ch+var_2C28], eax
00B562BB  mov     eax, [esi+0Ch]
00B562BE  push    eax
00B562BF  lea     ecx, [esp+2C60h+var_2B58]
```

## E2 字段 1：`result`（u32，偏移 0，长度 4）

```asm
; VA: 0x0xB562EE 附近（强化（白金）处理结果码）
00B562E4  mov     eax, [esp+2C5Ch+var_2BFC]
00B562E8  lea     edx, [esp+2C5Ch+var_2C44]
00B562EC  push    edx
00B562ED  push    eax
00B562EE  call    sub_B02DD0
00B562F3  add     esp, 8
00B562F6  test    al, al
00B562F8  jnz     short loc_B56316
00B562FA  mov     edx, [esi]
00B562FC  mov     eax, [edx+64h]
```

## E3 字段 2：`uniqid_ms`（u64，偏移 4，长度 8）

```asm
; VA: 0x0xB5632E 附近（机体唯一 ID）
00B56324  mov     eax, [esp+2C5Ch+var_2C08]
00B56328  lea     edx, [esp+2C5Ch+var_2C44]
00B5632C  push    edx
00B5632D  push    eax
00B5632E  call    sub_B06200
00B56333  add     esp, 8
00B56336  test    al, al
00B56338  jz      short loc_B562FA
00B5633A  lea     ecx, [esp+2C5Ch+var_2C28]
00B5633E  push    ecx
```

## E4 字段 3：`ticket_id`（u32，偏移 12，长度 4）

```asm
; VA: 0x0xB56352 附近（消耗的强化票 ID）
00B56348  mov     eax, [esp+2C5Ch+var_2C0C]
00B5634C  lea     edx, [esp+2C5Ch+var_2C44]
00B56350  push    edx
00B56351  push    eax
00B56352  call    sub_B02DD0
00B56357  add     esp, 8
00B5635A  test    al, al
00B5635C  jz      short loc_B562FA
00B5635E  lea     ecx, [esp+2C5Ch+var_2C28]
00B56362  push    ecx
```

## E5 字段 4：`usenum`（u16，偏移 16，长度 2）

```asm
; VA: 0x0xB56376 附近（本次使用材料数量）
00B5636C  mov     eax, [esp+2C5Ch+var_2C30]
00B56370  lea     edx, [esp+2C5Ch+var_2C44]
00B56374  push    edx
00B56375  push    eax
00B56376  call    sub_B02DF0
00B5637B  add     esp, 8
00B5637E  test    al, al
00B56380  jz      loc_B562FA
00B56386  lea     ecx, [esp+2C5Ch+var_2C28]
00B5638A  push    ecx
```

## E6 字段 5：`workres`（u32，偏移 18，长度 4）

```asm
; VA: 0x0xB5639E 附近（强化作业结果资源 ID）
00B56394  mov     eax, [esp+2C5Ch+var_2C34]
00B56398  lea     edx, [esp+2C5Ch+var_2C44]
00B5639C  push    edx
00B5639D  push    eax
00B5639E  call    sub_B02DD0
00B563A3  add     esp, 8
00B563A6  test    al, al
00B563A8  jz      loc_B562FA
00B563AE  lea     ecx, [esp+2C5Ch+var_2C28]
00B563B2  push    ecx
```

## E7 字段 6：`buildup_cnt`（u16，偏移 22，长度 2）

```asm
; VA: 0x0xB563C6 附近（累计强化次数）
00B563BC  mov     eax, [esp+2C5Ch+var_2C38]
00B563C0  lea     edx, [esp+2C5Ch+var_2C44]
00B563C4  push    edx
00B563C5  push    eax
00B563C6  call    sub_B02DF0
00B563CB  add     esp, 8
00B563CE  test    al, al
00B563D0  jz      loc_B562FA
00B563D6  lea     ecx, [esp+2C5Ch+var_2C28]
00B563DA  push    ecx
```

## E8 字段 7：`up_params`（u16[7]，偏移 24，长度 14）

```asm
; VA: 0x0xB563F6 附近（强化参数数组（固定 7×u16，无线上计数））
00B563EA  lea     ebx, [ebx+0]
00B563F0  lea     edx, [esp+2C5Ch+var_2C44]
00B563F4  push    edx
00B563F5  push    ebx
00B563F6  call    sub_B02DF0
00B563FB  add     esp, 8
00B563FE  test    al, al
00B56400  jz      short loc_B5640F
00B56402  add     edi, 1
00B56405  add     ebx, 2
```

## E9 字段 8：`mech_npcpict`（u32，偏移 38，长度 4）

```asm
; VA: 0x0xB56437 附近（机体 NPC 立绘 ID）
00B5642D  mov     edx, [esp+2C5Ch+var_2C48]
00B56431  lea     ecx, [esp+2C5Ch+var_2C44]
00B56435  push    ecx
00B56436  push    edx
00B56437  call    sub_B02DD0
00B5643C  add     esp, 8
00B5643F  test    al, al
00B56441  mov     ecx, esi
00B56443  jnz     short loc_B5645F
00B56445  mov     eax, [esi]
```

## E10 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB56463
00B5644A  push    1
00B5644C  push    108h
00B56451  call    edx
00B56453  lea     ecx, [esp+2C5Ch+var_2B58]
00B5645A  jmp     loc_B890EE
00B5645F  mov     eax, [esp+2C5Ch+var_2C44]
00B56463  cmp     eax, [esp+2C5Ch+var_2C40]
00B56467  jz      short loc_B56483
00B56469  mov     edx, [esi]
00B5646B  mov     eax, [edx+64h]
00B5646E  push    1
00B56470  push    108h
00B56475  call    eax
00B56477  lea     ecx, [esp+2C5Ch+var_2B58]
```
