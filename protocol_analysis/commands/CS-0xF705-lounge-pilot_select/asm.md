# 汇编证据 —— CS-0xF705-lounge-pilot_select

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0x00B8A8B0`（`0x00B8A8B0`..`0x00B8AB6A`），函数 `sub_B8A8B0`
- 命令名字符串：`)<-_proto_lounge_client::send_pilot_select(` @ `0x00EEA3D0`
- opcode 写入：`0x00B8A929`
- 声明容量：`0x16`（分配器容量 `push` @ `0x00B8A8F3`）
- 提交（`sub_B02FF0`）：`0x00B8A9FE`
- 发送去向：`vt[0x58]` @ `0x00B8AAFB`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00B8A8FC  push    eax
  00B8A8FD  lea     ecx, [esp+4Ch+var_34]
  00B8A901  call    sub_ABB2F0   ; <<< 初始化 {cur,end}（游标自 buf+2 起）
  00B8A906  lea     ecx, [ebp+16h]
  00B8A909  lea     eax, [ebp+2]
  00B8A90C  cmp     eax, ecx
  00B8A90E  mov     [esp+48h+var_4], 0
  00B8A916  mov     [esp+48h+var_30], ebp
  00B8A91A  mov     dword ptr [esp+48h+var_2C], ecx
  00B8A91E  ja      loc_B8AB55
  00B8A924  lea     edx, [eax+4]
  00B8A927  cmp     edx, ecx
  00B8A929  mov     word ptr [ebp+0], 0F705h   ; <<< 内联写线（u16）
  00B8A92F  ja      loc_B8AB55
  00B8A935  mov     esi, [esp+48h+arg_0]
  00B8A939  mov     [eax], esi   ; <<< 内联写线（u32）
  00B8A93B  mov     eax, edx
  00B8A93D  lea     edx, [eax+4]
  00B8A940  cmp     edx, ecx
  00B8A942  ja      loc_B8AB55
  00B8A948  mov     ecx, dword ptr [esp+48h+arg_4]
  00B8A94C  mov     [esp+48h+var_30], edx
  00B8A950  lea     edx, [esp+48h+var_30]
  00B8A954  mov     [eax], ecx   ; <<< 内联写线（u32）
  00B8A956  push    edx
  00B8A957  lea     eax, [esp+4Ch+arg_8]
  00B8A95B  push    eax
  00B8A95C  call    sub_B061C0   ; <<< 写线原语 u8
  00B8A961  add     esp, 8
  00B8A964  test    al, al
  00B8A966  jz      loc_B8AB55
  00B8A96C  lea     ecx, [esp+48h+var_30]
  00B8A970  push    ecx
  00B8A971  lea     edx, [esp+4Ch+arg_C]
  00B8A975  push    edx
  00B8A976  call    sub_B02D80   ; <<< 写线原语 u32
  00B8A97B  add     esp, 8
  00B8A97E  test    al, al
  00B8A980  jz      loc_B8AB55
  00B8A986  lea     eax, [esp+48h+var_30]
  00B8A98A  push    eax
  00B8A98B  lea     ecx, [esp+4Ch+arg_10]
  00B8A98F  push    ecx
  00B8A990  call    sub_B02D80   ; <<< 写线原语 u32
  00B8A995  add     esp, 8
  00B8A998  test    al, al
  00B8A99A  jz      loc_B8AB55
  00B8A9A0  mov     esi, [edi+7A04h]
  00B8A9A6  test    esi, esi
  00B8A9A8  mov     ebx, [esp+48h+var_30]
  00B8A9AC  jz      loc_B8AAF9
  00B8A9B2  lea     edx, [esp+48h+var_28]
  00B8A9B6  push    edx
  00B8A9B7  call    sub_CA0CE0
  00B8A9BC  add     esp, 4
  00B8A9BF  mov     ecx, [edi+8]
  00B8A9C2  push    offset aProtoLoungeCli_376
  00B8A9C7  push    ecx
  00B8A9C8  push    offset aId
  00B8A9CD  push    eax
  00B8A9CE  push    esi
  00B8A9CF  mov     byte ptr [esp+5Ch+var_4], 1
  00B8A9D4  call    sub_B03020
  00B8A9D9  add     esp, 8
  00B8A9DC  push    eax
  00B8A9DD  call    sub_41D990
  00B8A9E2  add     esp, 8
  00B8A9E5  mov     ecx, eax
  00B8A9E7  call    sub_ADC810
  00B8A9EC  push    eax
  00B8A9ED  call    sub_41D990
  00B8A9F2  add     esp, 8
  00B8A9F5  lea     ecx, [esp+48h+var_28]
  00B8A9F9  mov     byte ptr [esp+48h+var_4], 0
  00B8A9FE  call    sub_B02FF0   ; <<< 提交（C→S 闭合点）
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00B8A9FE  call    sub_B02FF0
  00B8AA03  mov     edx, [esp+48h+arg_0]
  00B8AA07  push    offset word_F641DC
  00B8AA0C  push    edx
  00B8AA0D  push    offset aTroops
  00B8AA12  push    esi
  00B8AA13  call    sub_41D990
  00B8AA18  add     esp, 8
  00B8AA1B  mov     ecx, eax
  00B8AA1D  call    sub_B03580
  00B8AA22  push    eax
  00B8AA23  call    sub_41D990
  00B8AA28  mov     eax, dword ptr [esp+50h+arg_4]
  00B8AA2C  add     esp, 8
  00B8AA2F  push    offset word_F641DC
  00B8AA34  push    eax
  00B8AA35  push    offset aPilotId
  00B8AA3A  push    esi
  00B8AA3B  call    sub_41D990
  00B8AA40  add     esp, 8
  00B8AA43  mov     ecx, eax
  00B8AA45  call    sub_B03580
  00B8AA4A  push    eax
  00B8AA4B  call    sub_41D990
  00B8AA50  add     esp, 8
  00B8AA53  push    offset word_F641DC
  00B8AA58  lea     ecx, [esp+4Ch+arg_8]
  00B8AA5C  push    ecx
  00B8AA5D  push    offset aIsTutorialSkip
  00B8AA62  push    esi
  00B8AA63  call    sub_41D990
  00B8AA68  add     esp, 8
  00B8AA6B  push    eax
  00B8AA6C  call    sub_B0C1F0
  00B8AA71  add     esp, 8
  00B8AA74  push    eax
  00B8AA75  call    sub_41D990
  00B8AA7A  mov     edx, [esp+50h+arg_C]
  00B8AA7E  add     esp, 8
  00B8AA81  push    offset word_F641DC
  00B8AA86  push    edx
  00B8AA87  push    offset aDbgComebackDis
  00B8AA8C  push    esi
  00B8AA8D  call    sub_41D990
  00B8AA92  add     esp, 8
  00B8AA95  mov     ecx, eax
  00B8AA97  call    sub_B03580
  00B8AA9C  push    eax
  00B8AA9D  call    sub_41D990
  00B8AAA2  mov     eax, [esp+50h+arg_10]
  00B8AAA6  add     esp, 8
  00B8AAA9  push    eax
  00B8AAAA  push    offset aChannelingType
  00B8AAAF  push    esi
  00B8AAB0  call    sub_41D990
  00B8AAB5  add     esp, 8
  00B8AAB8  mov     ecx, eax
  00B8AABA  call    sub_B03580
  00B8AABF  push    offset aByte
  00B8AAC4  mov     ecx, ebx
  00B8AAC6  sub     ecx, ebp
  00B8AAC8  push    ecx
  00B8AAC9  push    offset asc_EDAD58
  00B8AACE  push    esi
  00B8AACF  call    sub_41D990
  00B8AAD4  add     esp, 8
  00B8AAD7  mov     ecx, eax
  00B8AAD9  call    sub_B03580
  00B8AADE  push    eax
  00B8AADF  call    sub_41D990
  00B8AAE4  add     esp, 8
  00B8AAE7  mov     esi, eax
  00B8AAE9  push    0Ah
  00B8AAEB  mov     ecx, esi
  00B8AAED  call    sub_B036E0
  00B8AAF2  mov     ecx, esi
  00B8AAF4  call    sub_40DDF0
  00B8AAF9  mov     edx, [edi]
  00B8AAFB  mov     eax, [edx+58h]
```

## 4. 发送去向切片

```asm
  00B8AAF9  mov     edx, [edi]
  00B8AAFB  mov     eax, [edx+58h]
  00B8AAFE  sub     ebx, ebp
  00B8AB00  push    ebx
  00B8AB01  push    ebp
  00B8AB02  mov     ecx, edi
  00B8AB04  call    eax
  00B8AB06  test    al, al
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `00B8A929` | u16 / 2 |
| `troops` | `0xB8A935`;`0xB8A939` | u32 / 4 |
| `pilot_id` | `0xB8A948`;`0xB8A954` | u32 / 4 |
| `is_tutorial_skip` | `0xB8A95C` | u8 / 1 |
| `dbg_comeback_disable` | `0xB8A976` | u32 / 4 |
| `channeling_type` | `0xB8A990` | u32 / 4 |
