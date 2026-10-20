# 汇编证据 —— SC-0x1ED8-battle-roomlobby_ban_vote_cancel_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x4` @ `0xB1274E`）

```asm
; VA: 0xB12735 .. （块入口，含守卫与容量申请）
00B12735  push    1Bh
00B12737  mov     ecx, esi
00B12739  call    sub_B05DA0
00B1273E  test    al, al
00B12740  jz      loc_B317C7
00B12746  mov     ecx, [esi+0Ch]
00B12749  mov     eax, [ecx]
00B1274B  mov     edx, [eax+78h]
00B1274E  push    4
00B12750  call    edx
00B12752  mov     [esp+1B3Ch+var_1B14], eax
00B12756  mov     eax, [esi+0Ch]
00B12759  push    eax
00B1275A  lea     ecx, [esp+1B40h+var_176C]
```

## E2 字段 1：`result`（u32，偏移 0，长度 4）

```asm
; VA: 0x0xB12789 附近（驱逐投票取消结果码）
00B1277F  mov     eax, [esp+1B3Ch+var_1B2C]
00B12783  lea     edx, [esp+1B3Ch+var_1B28]
00B12787  push    edx
00B12788  push    eax
00B12789  call    sub_B02DD0
00B1278E  add     esp, 8
00B12791  test    al, al
00B12793  mov     ecx, esi
00B12795  jnz     short loc_B127AE
00B12797  mov     edx, [esi]
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB127B2
00B1279C  push    1
00B1279E  push    1Bh
00B127A0  call    eax
00B127A2  lea     ecx, [esp+1B3Ch+var_176C]
00B127A9  jmp     loc_B317B7
00B127AE  mov     ebx, [esp+1B3Ch+var_1B28]
00B127B2  cmp     ebx, [esp+1B3Ch+var_1B24]
00B127B6  jnz     short loc_B12797
00B127B8  push    1Bh
00B127BA  call    sub_B05D90
00B127BF  mov     edi, eax
00B127C1  test    edi, edi
00B127C3  jz      loc_B12875
00B127C9  lea     ecx, [esp+1B3Ch+var_4E0]
```
