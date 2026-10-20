# 汇编证据 —— SC-0x2A05-lounge-msma_deckslot_change_terminal

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `无（未申请解码缓冲）` @ `-`）

```asm
; VA: 0xB59650 .. （块入口，含守卫与容量申请）
00B59650  call    sub_B41120
00B59655  test    al, al
00B59657  jz      loc_B890FE
00B5965D  mov     ebx, [esp+2C5Ch+var_2C44]
00B59661  cmp     ebx, [esp+2C5Ch+var_2C40]
00B59665  mov     ecx, esi
00B59667  jz      short loc_B5968F
00B59669  mov     edx, [esi]
00B5966B  mov     eax, [edx+64h]
00B5966E  push    1
00B59670  push    0D3h
00B59675  call    eax
00B59677  mov     ecx, [esp+2C5Ch+var_C]
00B5967E  mov     large fs:0, ecx
```

## E2 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB59661
00B59650  call    sub_B41120
00B59655  test    al, al
00B59657  jz      loc_B890FE
00B5965D  mov     ebx, [esp+2C5Ch+var_2C44]
00B59661  cmp     ebx, [esp+2C5Ch+var_2C40]
00B59665  mov     ecx, esi
00B59667  jz      short loc_B5968F
00B59669  mov     edx, [esi]
00B5966B  mov     eax, [edx+64h]
00B5966E  push    1
00B59670  push    0D3h
00B59675  call    eax
```
