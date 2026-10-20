# 汇编证据 —— SC-0x300A-lounge-party_invite_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xC` @ `0xB5A83A`）

```asm
; VA: 0xB5A825 .. （块入口，含守卫与容量申请）
00B5A825  call    sub_B41120
00B5A82A  test    al, al
00B5A82C  jz      loc_B890FE
00B5A832  mov     ecx, [esi+0Ch]
00B5A835  mov     eax, [ecx]
00B5A837  mov     edx, [eax+78h]
00B5A83A  push    0Ch
00B5A83C  call    edx
00B5A83E  mov     [esp+2C5Ch+var_2C48], eax
00B5A842  mov     eax, [esi+0Ch]
00B5A845  push    eax
00B5A846  lea     ecx, [esp+2C60h+var_29AC]
00B5A84D  call    sub_ABB2F0
00B5A852  lea     ecx, [esp+2C5Ch+var_2C48]
```

## E2 字段 1：`result`（u32，偏移 0，长度 4）

```asm
; VA: 0x0xB5A875 附近（邀请入队结果码）
00B5A86B  mov     eax, [esp+2C5Ch+var_2C30]
00B5A86F  lea     edx, [esp+2C5Ch+var_2C44]
00B5A873  push    edx
00B5A874  push    eax
00B5A875  call    sub_B02DD0
00B5A87A  add     esp, 8
00B5A87D  test    al, al
00B5A87F  jnz     short loc_B5A89D
00B5A881  mov     edx, [esi]
00B5A883  mov     eax, [edx+64h]
```

## E3 字段 2：`pilot_id`（u32，偏移 4，长度 4）

```asm
; VA: 0x0xB5A8B5 附近（被邀请驾驶员 ID）
00B5A8AB  mov     eax, [esp+2C5Ch+var_2C34]
00B5A8AF  lea     edx, [esp+2C5Ch+var_2C44]
00B5A8B3  push    edx
00B5A8B4  push    eax
00B5A8B5  call    sub_B02DD0
00B5A8BA  add     esp, 8
00B5A8BD  test    al, al
00B5A8BF  jz      short loc_B5A881
00B5A8C1  lea     ecx, [esp+2C5Ch+var_2C48]
00B5A8C5  push    ecx
```

## E4 字段 3：`reason`（u32，偏移 8，长度 4）

```asm
; VA: 0x0xB5A8D9 附近（原因/结果细分码）
00B5A8CF  mov     eax, [esp+2C5Ch+var_2C38]
00B5A8D3  lea     edx, [esp+2C5Ch+var_2C44]
00B5A8D7  push    edx
00B5A8D8  push    eax
00B5A8D9  call    sub_B02DD0
00B5A8DE  add     esp, 8
00B5A8E1  test    al, al
00B5A8E3  jz      short loc_B5A881
00B5A8E5  mov     ebx, [esp+2C5Ch+var_2C44]
00B5A8E9  cmp     ebx, [esp+2C5Ch+var_2C40]
```

## E5 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB5A8E9
00B5A8D8  push    eax
00B5A8D9  call    sub_B02DD0
00B5A8DE  add     esp, 8
00B5A8E1  test    al, al
00B5A8E3  jz      short loc_B5A881
00B5A8E5  mov     ebx, [esp+2C5Ch+var_2C44]
00B5A8E9  cmp     ebx, [esp+2C5Ch+var_2C40]
00B5A8ED  mov     ecx, esi
00B5A8EF  jz      short loc_B5A90B
00B5A8F1  mov     edx, [esi]
00B5A8F3  mov     eax, [edx+64h]
00B5A8F6  push    1
00B5A8F8  push    0B2h
00B5A8FD  call    eax
```
