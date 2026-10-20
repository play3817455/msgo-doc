# 汇编证据 —— SC-0x2AAF-lounge-dailycup_get_point_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x48` @ `0xB59DA7`）

```asm
; VA: 0xB59D8B .. （块入口，含守卫与容量申请）
00B59D8B  push    23Dh
00B59D90  mov     ecx, esi
00B59D92  call    sub_B41120
00B59D97  test    al, al
00B59D99  jz      loc_B890FE
00B59D9F  mov     ecx, [esi+0Ch]
00B59DA2  mov     eax, [ecx]
00B59DA4  mov     edx, [eax+78h]
00B59DA7  push    48h ; 'H'
00B59DA9  call    edx
00B59DAB  mov     [esp+2C5Ch+var_2C3C], eax
00B59DAF  mov     eax, [esi+0Ch]
00B59DB2  push    eax
00B59DB3  lea     ecx, [esp+2C60h+var_27A4]
```

## E2 字段 1：`result`（u32，偏移 0，长度 4）

```asm
; VA: 0x0xB59DE2 附近（每日杯（dailycup）积分查询结果码）
00B59DD8  mov     eax, [esp+2C5Ch+var_2C38]
00B59DDC  lea     edx, [esp+2C5Ch+var_2C44]
00B59DE0  push    edx
00B59DE1  push    eax
00B59DE2  call    sub_B02DD0
00B59DE7  add     esp, 8
00B59DEA  test    al, al
00B59DEC  jnz     short loc_B59E0A
00B59DEE  mov     edx, [esi]
00B59DF0  mov     eax, [edx+64h]
```

## E3 字段 2：`dc_point`（struct{41/槽68}，偏移 4，长度 41）

```asm
; VA: 0x0xB59E22 附近（每日杯积分明细（线上 41B；缓冲槽 68））
00B59E18  mov     eax, [esp+2C5Ch+var_2C48]
00B59E1C  lea     edx, [esp+2C5Ch+var_2C44]
00B59E20  push    edx
00B59E21  push    eax
00B59E22  call    sub_B47120
00B59E27  add     esp, 8
00B59E2A  test    al, al
00B59E2C  jz      short loc_B59DEE
00B59E2E  mov     ebx, [esp+2C5Ch+var_2C44]
00B59E32  cmp     ebx, [esp+2C5Ch+var_2C40]
```

## E4 字段 3：`dc_point.is_dc`（i8，偏移 +0，长度 1）

```asm
; VA: 0x0xB47120 附近（本次是否掉线（DC））
00B59D8B  push    23Dh
00B59D90  mov     ecx, esi
00B59D92  call    sub_B41120
00B59D97  test    al, al
00B59D99  jz      loc_B890FE
00B59D9F  mov     ecx, [esi+0Ch]
```

## E5 字段 4：`dc_point.bef_dcpoint`（u32，偏移 +1，长度 4）

```asm
; VA: 0x0xB47120 附近（掉线前积分）
00B59D8B  push    23Dh
00B59D90  mov     ecx, esi
00B59D92  call    sub_B41120
00B59D97  test    al, al
00B59D99  jz      loc_B890FE
00B59D9F  mov     ecx, [esi+0Ch]
```

## E6 字段 5：`dc_point.aft_dcpoint`（u32，偏移 +5，长度 4）

```asm
; VA: 0x0xB47120 附近（掉线后积分）
00B59D8B  push    23Dh
00B59D90  mov     ecx, esi
00B59D92  call    sub_B41120
00B59D97  test    al, al
00B59D99  jz      loc_B890FE
00B59D9F  mov     ecx, [esi+0Ch]
```

## E7 字段 6：`dc_point.reward_item_ids`（u32[4]，偏移 +9，长度 16）

```asm
; VA: 0x0xB47120 附近（奖励道具 ID 列表（固定 4 项））
00B59D8B  push    23Dh
00B59D90  mov     ecx, esi
00B59D92  call    sub_B41120
00B59D97  test    al, al
00B59D99  jz      loc_B890FE
00B59D9F  mov     ecx, [esi+0Ch]
```

## E8 字段 7：`dc_point.reward_item_nums`（u32[4]，偏移 +25，长度 16）

```asm
; VA: 0x0xB47120 附近（奖励道具数量列表（固定 4 项））
00B59D8B  push    23Dh
00B59D90  mov     ecx, esi
00B59D92  call    sub_B41120
00B59D97  test    al, al
00B59D99  jz      loc_B890FE
00B59D9F  mov     ecx, [esi+0Ch]
```

## E9 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB59E32
00B59E21  push    eax
00B59E22  call    sub_B47120
00B59E27  add     esp, 8
00B59E2A  test    al, al
00B59E2C  jz      short loc_B59DEE
00B59E2E  mov     ebx, [esp+2C5Ch+var_2C44]
00B59E32  cmp     ebx, [esp+2C5Ch+var_2C40]
00B59E36  mov     ecx, esi
00B59E38  jz      short loc_B59E54
00B59E3A  mov     edx, [esi]
00B59E3C  mov     eax, [edx+64h]
00B59E3F  push    1
00B59E41  push    23Dh
00B59E46  call    eax
```
