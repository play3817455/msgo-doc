# 汇编证据 —— SC-0x1E0F-battle-preset_voice_down

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xBF` @ `0xB11F1B`）

```asm
; VA: 0xB11F02 .. （块入口，含守卫与容量申请）
00B11F02  push    65h ; 'e'
00B11F04  mov     ecx, esi
00B11F06  call    sub_B05DA0
00B11F0B  test    al, al
00B11F0D  jz      loc_B317C7
00B11F13  mov     ecx, [esi+0Ch]
00B11F16  mov     eax, [ecx]
00B11F18  mov     edx, [eax+78h]
00B11F1B  push    0BFh
00B11F20  call    edx
00B11F22  mov     [esp+1B3Ch+var_1B1C], eax
00B11F26  mov     eax, [esi+0Ch]
00B11F29  push    eax
00B11F2A  lea     ecx, [esp+1B40h+var_1A1C]
```

## E2 字段 1：`ent_id`（u16，偏移 0，长度 2）

```asm
; VA: 0x0xB11F59 附近（语音实体 ID）
00B11F4F  mov     eax, [esp+1B3Ch+var_1AEC]
00B11F53  lea     edx, [esp+1B3Ch+var_1B28]
00B11F57  push    edx
00B11F58  push    eax
00B11F59  call    sub_B02DF0
00B11F5E  add     esp, 8
00B11F61  test    al, al
00B11F63  jnz     short loc_B11F7E
00B11F65  mov     edx, [esi]
00B11F67  mov     eax, [edx+64h]
```

## E3 字段 2：`voice_id`（u32，偏移 2，长度 4）

```asm
; VA: 0x0xB11F96 附近（预置语音 ID）
00B11F8C  mov     eax, [esp+1B3Ch+var_1B00]
00B11F90  lea     edx, [esp+1B3Ch+var_1B28]
00B11F94  push    edx
00B11F95  push    eax
00B11F96  call    sub_B02DD0
00B11F9B  add     esp, 8
00B11F9E  test    al, al
00B11FA0  jz      short loc_B11F65
00B11FA2  lea     ecx, [esp+1B3Ch+var_1B1C]
00B11FA6  push    ecx
```

## E4 字段 3：`voice_volume`（u8，偏移 6，长度 1）

```asm
; VA: 0x0xB11FBA 附近（语音音量）
00B11FB0  mov     eax, [esp+1B3Ch+var_1B0C]
00B11FB4  lea     edx, [esp+1B3Ch+var_1B28]
00B11FB8  push    edx
00B11FB9  push    eax
00B11FBA  call    sub_B06230
00B11FBF  add     esp, 8
00B11FC2  test    al, al
00B11FC4  jz      short loc_B11F65
00B11FC6  lea     ecx, [esp+1B3Ch+var_1B1C]
00B11FCA  push    ecx
```

## E5 字段 4：`is_cutin`（u8，偏移 7，长度 1）

```asm
; VA: 0x0xB11FDE 附近（是否过场插播）
00B11FD4  mov     eax, [esp+1B3Ch+var_1B18]
00B11FD8  lea     edx, [esp+1B3Ch+var_1B28]
00B11FDC  push    edx
00B11FDD  push    eax
00B11FDE  call    sub_B06230
00B11FE3  add     esp, 8
00B11FE6  test    al, al
00B11FE8  jz      loc_B11F65
00B11FEE  lea     ecx, [esp+1B3Ch+var_1B1C]
00B11FF2  push    ecx
```

## E6 字段 5：`is_party`（u8，偏移 8，长度 1）

```asm
; VA: 0x0xB12006 附近（是否队伍相关）
00B11FFC  mov     eax, [esp+1B3Ch+var_1B20]
00B12000  lea     edx, [esp+1B3Ch+var_1B28]
00B12004  push    edx
00B12005  push    eax
00B12006  call    sub_B06230
00B1200B  add     esp, 8
00B1200E  test    al, al
00B12010  jz      loc_B11F65
00B12016  lea     ecx, [esp+1B3Ch+var_1B1C]
00B1201A  push    ecx
```

## E7 字段 6：`is_use_textmsg`（u8，偏移 9，长度 1）

```asm
; VA: 0x0xB1202E 附近（是否用文本消息替代语音）
00B12024  mov     eax, [esp+1B3Ch+var_1B2C]
00B12028  lea     edx, [esp+1B3Ch+var_1B28]
00B1202C  push    edx
00B1202D  push    eax
00B1202E  call    sub_B06230
00B12033  add     esp, 8
00B12036  test    al, al
00B12038  jz      loc_B11F65
00B1203E  mov     edx, [esp+1B3Ch+var_1B1C]
00B12042  push    0B5h
```

## E8 字段 7：`textmsg`（str，偏移 10，长度 L+1）

```asm
; VA: 0x0xB1204D 附近（文本消息（NUL 结尾；槽预算 181））
00B12042  push    0B5h
00B12047  lea     ecx, [esp+1B40h+var_1B28]
00B1204B  push    ecx
00B1204C  push    edx
00B1204D  call    sub_B02BA0
00B12052  add     esp, 0Ch
00B12055  test    al, al
00B12057  mov     ecx, esi
00B12059  jnz     short loc_B12072
00B1205B  mov     eax, [esi]
```

## E9 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB12076
00B12060  push    1
00B12062  push    65h ; 'e'
00B12064  call    edx
00B12066  lea     ecx, [esp+1B3Ch+var_1A1C]
00B1206D  jmp     loc_B317B7
00B12072  mov     ebx, [esp+1B3Ch+var_1B28]
00B12076  cmp     ebx, [esp+1B3Ch+var_1B24]
00B1207A  jnz     short loc_B1205B
00B1207C  push    65h ; 'e'
00B1207E  call    sub_B05D90
00B12083  mov     edi, eax
00B12085  test    edi, edi
00B12087  jz      loc_B12244
00B1208D  lea     eax, [esp+1B3Ch+var_1350]
```
