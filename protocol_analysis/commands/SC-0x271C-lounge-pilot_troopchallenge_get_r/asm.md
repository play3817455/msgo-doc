# 汇编证据 —— SC-0x271C-lounge-pilot_troopchallenge_get_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xF4` @ `0xB58FD2`）

```asm
; VA: 0xB58FBD .. （块入口，含守卫与容量申请）
00B58FBD  call    sub_B41120
00B58FC2  test    al, al
00B58FC4  jz      loc_B890FE
00B58FCA  mov     ecx, [esi+0Ch]
00B58FCD  mov     eax, [ecx]
00B58FCF  mov     edx, [eax+78h]
00B58FD2  push    0F4h
00B58FD7  call    edx
00B58FD9  mov     [esp+2C5Ch+var_2C48], eax
00B58FDD  mov     eax, [esi+0Ch]
00B58FE0  push    eax
00B58FE1  lea     ecx, [esp+2C60h+var_2770]
00B58FE8  call    sub_ABB2F0
00B58FED  lea     ecx, [esp+2C5Ch+var_2C48]
```

## E2 字段 1：`result`（u32，偏移 0，长度 4）

```asm
; VA: 0x0xB59010 附近（查询结果码）
00B59006  mov     eax, [esp+2C5Ch+var_2C34]
00B5900A  lea     edx, [esp+2C5Ch+var_2C44]
00B5900E  push    edx
00B5900F  push    eax
00B59010  call    sub_B02DD0
00B59015  add     esp, 8
00B59018  test    al, al
00B5901A  jnz     short loc_B59035
00B5901C  mov     edx, [esi]
00B5901E  mov     eax, [edx+64h]
```

## E3 字段 2：`trchallenge_info`（struct{13/槽200}，偏移 4，长度 13）

```asm
; VA: 0x0xB59056 附近（部队挑战信息结构（线上 13B；缓冲槽 200））
00B59049  lea     esp, [esp+0]
00B59050  lea     edx, [esp+2C5Ch+var_2C44]
00B59054  push    edx
00B59055  push    ebx
00B59056  call    sub_B07540
00B5905B  add     esp, 8
00B5905E  test    al, al
00B59060  jz      short loc_B5906F
00B59062  add     edi, 1
00B59065  add     ebx, 14h
```

## E8 字段 7：`allclear_num`（u32[10]，偏移 17，长度 40）

```asm
; VA: 0x0xB59096 附近（各关全清次数（固定 10 项 u32，无线上计数））
00B5908E  xor     edi, edi
00B59090  lea     ecx, [esp+2C5Ch+var_2C44]
00B59094  push    ecx
00B59095  push    ebx
00B59096  call    sub_B02DD0
00B5909B  add     esp, 8
00B5909E  test    al, al
00B590A0  jz      short loc_B590AF
00B590A2  add     edi, 1
00B590A5  add     ebx, 4
```

## E9 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB590C0
00B590B1  mov     eax, [edx+64h]
00B590B4  push    1
00B590B6  push    78h ; 'x'
00B590B8  mov     ecx, esi
00B590BA  call    eax
00B590BC  mov     ecx, [esp+2C5Ch+var_2C44]
00B590C0  cmp     ecx, [esp+2C5Ch+var_2C40]
00B590C4  mov     ecx, esi
00B590C6  jz      short loc_B590DF
00B590C8  mov     edx, [esi]
00B590CA  mov     eax, [edx+64h]
00B590CD  push    1
00B590CF  push    78h ; 'x'
00B590D1  call    eax
```
