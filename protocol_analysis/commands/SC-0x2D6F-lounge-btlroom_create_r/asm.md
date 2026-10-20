# 汇编证据 —— SC-0x2D6F-lounge-btlroom_create_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x10` @ `0xB5A56D`）

```asm
; VA: 0xB5A551 .. （块入口，含守卫与容量申请）
00B5A551  push    8Dh
00B5A556  mov     ecx, esi
00B5A558  call    sub_B41120
00B5A55D  test    al, al
00B5A55F  jz      loc_B890FE
00B5A565  mov     ecx, [esi+0Ch]
00B5A568  mov     eax, [ecx]
00B5A56A  mov     edx, [eax+78h]
00B5A56D  push    10h
00B5A56F  call    edx
00B5A571  mov     [esp+2C5Ch+var_2C24], eax
00B5A575  mov     eax, [esi+0Ch]
00B5A578  push    eax
00B5A579  lea     ecx, [esp+2C60h+var_2AA4]
```

## E2 字段 1：`result`（u32，偏移 0，长度 4）

```asm
; VA: 0x0xB5A5A8 附近（创建对战房间结果码）
00B5A59E  mov     eax, [esp+2C5Ch+var_2C30]
00B5A5A2  lea     edx, [esp+2C5Ch+var_2C44]
00B5A5A6  push    edx
00B5A5A7  push    eax
00B5A5A8  call    sub_B02DD0
00B5A5AD  add     esp, 8
00B5A5B0  test    al, al
00B5A5B2  jnz     short loc_B5A5D0
00B5A5B4  mov     edx, [esi]
00B5A5B6  mov     eax, [edx+64h]
```

## E3 字段 2：`matching_type`（u32，偏移 4，长度 4）

```asm
; VA: 0x0xB5A5E8 附近（匹配类型）
00B5A5DE  mov     eax, [esp+2C5Ch+var_2C34]
00B5A5E2  lea     edx, [esp+2C5Ch+var_2C44]
00B5A5E6  push    edx
00B5A5E7  push    eax
00B5A5E8  call    sub_B02DD0
00B5A5ED  add     esp, 8
00B5A5F0  test    al, al
00B5A5F2  jz      short loc_B5A5B4
00B5A5F4  lea     ecx, [esp+2C5Ch+var_2C24]
00B5A5F8  push    ecx
```

## E4 字段 3：`mission_id`（u32，偏移 8，长度 4）

```asm
; VA: 0x0xB5A60C 附近（任务 ID）
00B5A602  mov     eax, [esp+2C5Ch+var_2C38]
00B5A606  lea     edx, [esp+2C5Ch+var_2C44]
00B5A60A  push    edx
00B5A60B  push    eax
00B5A60C  call    sub_B02DD0
00B5A611  add     esp, 8
00B5A614  test    al, al
00B5A616  jz      short loc_B5A5B4
00B5A618  lea     ecx, [esp+2C5Ch+var_2C24]
00B5A61C  push    ecx
```

## E5 字段 4：`room_id`（u32，偏移 12，长度 4）

```asm
; VA: 0x0xB5A630 附近（新建房间 ID）
00B5A626  mov     eax, [esp+2C5Ch+var_2C48]
00B5A62A  lea     edx, [esp+2C5Ch+var_2C44]
00B5A62E  push    edx
00B5A62F  push    eax
00B5A630  call    sub_B02DD0
00B5A635  add     esp, 8
00B5A638  test    al, al
00B5A63A  jz      loc_B5A5B4
00B5A640  mov     ebx, [esp+2C5Ch+var_2C44]
00B5A644  cmp     ebx, [esp+2C5Ch+var_2C40]
```

## E6 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB5A644
00B5A62F  push    eax
00B5A630  call    sub_B02DD0
00B5A635  add     esp, 8
00B5A638  test    al, al
00B5A63A  jz      loc_B5A5B4
00B5A640  mov     ebx, [esp+2C5Ch+var_2C44]
00B5A644  cmp     ebx, [esp+2C5Ch+var_2C40]
00B5A648  mov     ecx, esi
00B5A64A  jz      short loc_B5A666
00B5A64C  mov     edx, [esi]
00B5A64E  mov     eax, [edx+64h]
00B5A651  push    1
00B5A653  push    8Dh
00B5A658  call    eax
```
