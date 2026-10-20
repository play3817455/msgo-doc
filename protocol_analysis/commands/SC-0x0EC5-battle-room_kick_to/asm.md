# 汇编证据 —— SC-0x0EC5-battle-room_kick_to

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 case 入口：先校验「游标 == 末尾」（⇒ 无负载）

```asm
; VA: 0xB0F360 .. 0xB0F37B
0xB0F360  push    2Dh                      ; ← 本 case 错误码
0xB0F362  mov     ecx, esi
0xB0F364  call    sub_B05DA0               ; case 起始守卫（不读线）
0xB0F369  test    al, al
0xB0F36B  jz      loc_B317C7
0xB0F371  mov     ebx, [esp+1B3Ch+var_1B28] ; 线游标（尚未被任何字段推进）
0xB0F375  cmp     ebx, [esp+1B3Ch+var_1B24] ; vs 报文末尾
0xB0F379  mov     ecx, esi
0xB0F37B  jz      short loc_B0F3A0         ; ← 相等即正常；不等 ⇒ push 2Dh 报错
```

## E2 无解码缓冲申请（对比：有字段的 case 此处会有 `push N; call [eax+78h]`）

```asm
; VA: 0xB0F3A0 .. 0xB0F3BE —— 直接取日志对象，没有任何缓冲申请 / 字段预留 / bounded 读取
0xB0F3A0  push    2Dh
0xB0F3A2  call    sub_B05D90               ; 取日志对象（非字段）
0xB0F3A7  mov     edi, eax
0xB0F3A9  test    edi, edi
0xB0F3AB  jz      loc_B0F447
0xB0F3B1  lea     eax, [esp+1B3Ch+var_550]
0xB0F3B8  push    eax
0xB0F3B9  call    sub_CA0CE0               ; 清临时串
```

## E3 块内仅一条自身 trace（`recv_room_kick_to`）

```asm
; VA: 0xB0F3C1 .. 0xB0F3F5
0xB0F3C1  mov     ecx, [esi+8]
0xB0F3C4  push    offset aProtoBattleCli_14; ← ")->_proto_battle_client::recv_room_kick_to( "
0xB0F3C9  push    ecx
0xB0F3CA  push    offset aId              ; " (id:"
0xB0F3CF  push    eax
0xB0F3D0  push    edi
0xB0F3DC  call    sub_B03020
0xB0F3E5  call    sub_41D990
0xB0F3EF  call    sub_ADC810
0xB0F3F5  call    sub_41D990
```

## E4 去向：`vt[0xE0]()`（无实参）

```asm
; VA: 0xB0F447 .. 0xB0F45A
0xB0F447  mov     edx, [esi]
0xB0F449  mov     eax, [edx+0E0h]          ; ← vt[0xE0]
0xB0F44F  mov     ecx, esi
0xB0F451  call    eax                      ; ← 无 push ⇒ 无实参
0xB0F453  add     dword ptr [esi+0B50h], 1 ; 本命令接收计数（64 位）
0xB0F45A  adc     dword ptr [esi+0B54h], 0
```
