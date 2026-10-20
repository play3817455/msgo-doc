# 汇编证据 —— SC-0x1E8D-lounge-msma_equip_rental_modules_update_requip_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x8` @ `0xB57FBB`）

```asm
; VA: 0xB57F9F .. （块入口，含守卫与容量申请）
00B57F9F  push    0ECh
00B57FA4  mov     ecx, esi
00B57FA6  call    sub_B41120
00B57FAB  test    al, al
00B57FAD  jz      loc_B890FE
00B57FB3  mov     ecx, [esi+0Ch]
00B57FB6  mov     eax, [ecx]
00B57FB8  mov     edx, [eax+78h]
00B57FBB  push    8
00B57FBD  call    edx
00B57FBF  mov     [esp+2C5Ch+var_2C3C], eax
00B57FC3  mov     eax, [esi+0Ch]
00B57FC6  push    eax
00B57FC7  lea     ecx, [esp+2C60h+var_27D4]
```

## E2 字段 1：`result`（u32，偏移 0，长度 4）

```asm
; VA: 0x0xB57FF6 附近（租用模块改装结果码）
00B57FEC  mov     eax, [esp+2C5Ch+var_2C38]
00B57FF0  lea     edx, [esp+2C5Ch+var_2C44]
00B57FF4  push    edx
00B57FF5  push    eax
00B57FF6  call    sub_B02DD0
00B57FFB  add     esp, 8
00B57FFE  test    al, al
00B58000  jnz     short loc_B5801E
00B58002  mov     edx, [esi]
00B58004  mov     eax, [edx+64h]
```

## E3 字段 2：`module_id`（u32，偏移 4，长度 4）

```asm
; VA: 0x0xB58036 附近（模块 ID）
00B5802C  mov     eax, [esp+2C5Ch+var_2C48]
00B58030  lea     edx, [esp+2C5Ch+var_2C44]
00B58034  push    edx
00B58035  push    eax
00B58036  call    sub_B02DD0
00B5803B  add     esp, 8
00B5803E  test    al, al
00B58040  jz      short loc_B58002
00B58042  mov     ebx, [esp+2C5Ch+var_2C44]
00B58046  cmp     ebx, [esp+2C5Ch+var_2C40]
```

## E4 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB58046
00B58035  push    eax
00B58036  call    sub_B02DD0
00B5803B  add     esp, 8
00B5803E  test    al, al
00B58040  jz      short loc_B58002
00B58042  mov     ebx, [esp+2C5Ch+var_2C44]
00B58046  cmp     ebx, [esp+2C5Ch+var_2C40]
00B5804A  mov     ecx, esi
00B5804C  jz      short loc_B58068
00B5804E  mov     edx, [esi]
00B58050  mov     eax, [edx+64h]
00B58053  push    1
00B58055  push    0ECh
00B5805A  call    eax
```
