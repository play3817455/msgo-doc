# 汇编证据 —— SC-0x1E2F-battle-msma_spawn_list_get_r_one

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x10C` @ `0xB11D3F`）

```asm
; VA: 0xB11D26 .. （块入口，含守卫与容量申请）
00B11D26  push    48h ; 'H'
00B11D28  mov     ecx, esi
00B11D2A  call    sub_B05DA0
00B11D2F  test    al, al
00B11D31  jz      loc_B317C7
00B11D37  mov     ecx, [esi+0Ch]
00B11D3A  mov     eax, [ecx]
00B11D3C  mov     edx, [eax+78h]
00B11D3F  push    10Ch
00B11D44  call    edx
00B11D46  mov     [esp+1B3Ch+var_1B14], eax
00B11D4A  mov     eax, [esi+0Ch]
00B11D4D  push    eax
00B11D4E  lea     ecx, [esp+1B40h+var_182C]
```

## E2 字段 1：`index`（u32，偏移 0，长度 4）

```asm
; VA: 0x0xB11D7D 附近（机体列表下标）
00B11D73  mov     eax, [esp+1B3Ch+var_1B20]
00B11D77  lea     edx, [esp+1B3Ch+var_1B28]
00B11D7B  push    edx
00B11D7C  push    eax
00B11D7D  call    sub_B02DD0
00B11D82  add     esp, 8
00B11D85  test    al, al
00B11D87  jnz     short loc_B11DA2
00B11D89  mov     edx, [esi]
00B11D8B  mov     eax, [edx+64h]
```

## E3 字段 2：`ms`（struct{264}，偏移 4，长度 264）

```asm
; VA: 0x0xB11DBA 附近（机体出生列表条目快照（264B 定长结构体，无线上计数））
00B11DB0  mov     eax, [esp+1B3Ch+var_1B2C]
00B11DB4  lea     edx, [esp+1B3Ch+var_1B28]
00B11DB8  push    edx
00B11DB9  push    eax
00B11DBA  call    sub_B06D80
00B11DBF  add     esp, 8
00B11DC2  test    al, al
00B11DC4  jz      short loc_B11D89
00B11DC6  mov     ebx, [esp+1B3Ch+var_1B28]
00B11DCA  cmp     ebx, [esp+1B3Ch+var_1B24]
```

## E6 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB11DCA
00B11DB9  push    eax
00B11DBA  call    sub_B06D80
00B11DBF  add     esp, 8
00B11DC2  test    al, al
00B11DC4  jz      short loc_B11D89
00B11DC6  mov     ebx, [esp+1B3Ch+var_1B28]
00B11DCA  cmp     ebx, [esp+1B3Ch+var_1B24]
00B11DCE  mov     ecx, esi
00B11DD0  jz      short loc_B11DE9
00B11DD2  mov     edx, [esi]
00B11DD4  mov     eax, [edx+64h]
00B11DD7  push    1
00B11DD9  push    48h ; 'H'
00B11DDB  call    eax
```
