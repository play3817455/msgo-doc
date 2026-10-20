# 汇编证据 —— SC-0x14C5-battle-roomlobby_exit_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 case 入口 + 守卫（错误码 `0x17`）+ **入口即闭合校验**（⇒ 负载 0 字节）

```asm
; VA: 0xB10912 .. 0xB10952
0xB10912  push    17h                      ; ← 本 case 错误码
0xB10914  mov     ecx, esi
0xB10916  call    sub_B05DA0               ; case 起始守卫（不读线）
0xB1091B  test    al, al
0xB1091D  jz      loc_B317C7
0xB10923  mov     ebx, [esp+1B3Ch+var_1B28] ; 线游标（入口值）
0xB10927  cmp     ebx, [esp+1B3Ch+var_1B24] ; vs 报文末尾
0xB1092B  mov     ecx, esi
0xB1092D  jz      short loc_B10952          ; ← 相等才继续；不等 ⇒ push 1 / push 17h 报错
0xB1092F  mov     eax, [esi]
0xB10931  mov     edx, [eax+64h]
0xB10934  push    1
0xB10936  push    17h
0xB10938  call    edx
0xB1093A  mov     ecx, [esp+1B3Ch+var_C]    ; 报错路径直接返回
0xB10941  mov     large fs:0, ecx
0xB1094F  retn    8
```

## E2 无解码缓冲申请 / 无字段（判据）

```asm
; VA: 0xB10952 .. 0xB10963
0xB10952  push    17h
0xB10954  call    sub_B05D90               ; 取本命令日志句柄
0xB10959  mov     edi, eax
0xB1095B  test    edi, edi
0xB1095D  jz      loc_B109F9
0xB10963  lea     eax, [esp+1B3Ch+var_A20]
0xB1096B  call    sub_CA0CE0               ; 仅准备日志串缓冲，未申请线缓冲
; 全块无 push N; call [eax+78h]（解码缓冲申请）
; 全块无 sub_B41470 / sub_B413B0 / sub_B05E30（槽预留）
; 全块无 sub_B02DD0 / sub_B02DF0 / sub_B06230 / sub_B02BA0（bounded 读）
```

## E3 去向：`vt[0xAC]()`（无实参）

```asm
; VA: 0xB109F9 .. 0xB10A0C
0xB109F9  mov     edx, [esi]
0xB109FB  mov     eax, [edx+0ACh]           ; ← vt[0xAC]
0xB10A01  mov     ecx, esi
0xB10A03  call    eax                       ; ← 不 push 任何实参
0xB10A05  add     dword ptr [esi+730h], 1   ; 本命令接收计数（64 位）
0xB10A0C  adc     dword ptr [esi+734h], 0
```

## E4 块内唯一 trace 日志（名字串引用点）

```asm
; VA: 0xB10973 .. 0xB109A7
0xB10973  mov     ecx, [esi+8]
0xB10976  push    offset aProtoBattleCli_20 ; ← ")->_proto_battle_client::recv_roomlobby_exit_r( "
0xB1097C  push    offset aId               ; " (id:"
0xB1098E  call    sub_B03020
```
