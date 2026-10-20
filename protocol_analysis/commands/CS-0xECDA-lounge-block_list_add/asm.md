# 汇编证据 —— CS-0xECDA-lounge-block_list_add

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0x00B9B490`（`0x00B9B490`..`0x00B9B71E`），函数 `sub_B9B490`
- 命令名字符串：`)<-_proto_lounge_client::send_block_list_add(` @ `0x00EEC138`
- opcode 写入：`0x00B9B50C`
- 声明容量：`0x2A`（分配器容量 `push` @ `0x00B9B4D6`）
- 提交（`sub_B02FF0`）：`0x00B9B5C9`
- 发送去向：`vt[0x58]` @ `0x00B9B6AC`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00B9B4DF  push    eax
  00B9B4E0  lea     ecx, [esp+4Ch+var_34]
  00B9B4E4  call    sub_ABB2F0   ; <<< 初始化 {cur,end}（游标自 buf+2 起）
  00B9B4E9  lea     ecx, [ebp+2Ah]
  00B9B4EC  lea     eax, [ebp+2]
  00B9B4EF  cmp     eax, ecx
  00B9B4F1  mov     [esp+48h+var_4], 0
  00B9B4F9  mov     [esp+48h+var_30], ebp
  00B9B4FD  mov     dword ptr [esp+48h+var_2C], ecx
  00B9B501  ja      loc_B9B709
  00B9B507  lea     edx, [eax+4]
  00B9B50A  cmp     edx, ecx
  00B9B50C  mov     word ptr [ebp+0], 0ECDAh   ; <<< 内联写线（u16）
  00B9B512  ja      loc_B9B709
  00B9B518  mov     esi, [esp+48h+arg_0]
  00B9B51C  mov     [eax], esi   ; <<< 内联写线（u32）
  00B9B51E  mov     eax, edx
  00B9B520  lea     edx, [eax+4]
  00B9B523  cmp     edx, ecx
  00B9B525  ja      loc_B9B709
  00B9B52B  mov     ecx, [esp+48h+arg_4]
  00B9B52F  mov     [esp+48h+var_30], edx
  00B9B533  push    19h
  00B9B535  lea     edx, [esp+4Ch+var_30]
  00B9B539  mov     [eax], ecx   ; <<< 内联写线（u32）
  00B9B53B  mov     eax, [esp+4Ch+arg_8]
  00B9B53F  push    edx
  00B9B540  push    eax
  00B9B541  call    sub_B02B40   ; <<< 写线原语 str
  00B9B546  add     esp, 0Ch
  00B9B549  test    al, al
  00B9B54B  jz      loc_B9B709
  00B9B551  lea     ecx, [esp+48h+var_30]
  00B9B555  push    ecx
  00B9B556  lea     edx, [esp+4Ch+arg_C]
  00B9B55A  push    edx
  00B9B55B  call    sub_B02D80   ; <<< 写线原语 u32
  00B9B560  add     esp, 8
  00B9B563  test    al, al
  00B9B565  jz      loc_B9B709
  00B9B56B  mov     esi, [edi+7F38h]
  00B9B571  test    esi, esi
  00B9B573  mov     ebx, [esp+48h+var_30]
  00B9B577  jz      loc_B9B6AA
  00B9B57D  lea     eax, [esp+48h+var_28]
  00B9B581  push    eax
  00B9B582  call    sub_CA0CE0
  00B9B587  add     esp, 4
  00B9B58A  mov     ecx, [edi+8]
  00B9B58D  push    offset aProtoLoungeCli_386
  00B9B592  push    ecx
  00B9B593  push    offset aId
  00B9B598  push    eax
  00B9B599  push    esi
  00B9B59A  mov     byte ptr [esp+5Ch+var_4], 1
  00B9B59F  call    sub_B03020
  00B9B5A4  add     esp, 8
  00B9B5A7  push    eax
  00B9B5A8  call    sub_41D990
  00B9B5AD  add     esp, 8
  00B9B5B0  mov     ecx, eax
  00B9B5B2  call    sub_ADC810
  00B9B5B7  push    eax
  00B9B5B8  call    sub_41D990
  00B9B5BD  add     esp, 8
  00B9B5C0  lea     ecx, [esp+48h+var_28]
  00B9B5C4  mov     byte ptr [esp+48h+var_4], 0
  00B9B5C9  call    sub_B02FF0   ; <<< 提交（C→S 闭合点）
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00B9B5C9  call    sub_B02FF0
  00B9B5CE  mov     edx, [esp+48h+arg_0]
  00B9B5D2  push    offset word_F641DC
  00B9B5D7  push    edx
  00B9B5D8  push    offset aPilotid
  00B9B5DD  push    esi
  00B9B5DE  call    sub_41D990
  00B9B5E3  add     esp, 8
  00B9B5E6  mov     ecx, eax
  00B9B5E8  call    sub_B03580
  00B9B5ED  push    eax
  00B9B5EE  call    sub_41D990
  00B9B5F3  mov     eax, [esp+50h+arg_4]
  00B9B5F7  add     esp, 8
  00B9B5FA  push    offset word_F641DC
  00B9B5FF  push    eax
  00B9B600  push    offset aWorldId
  00B9B605  push    esi
  00B9B606  call    sub_41D990
  00B9B60B  add     esp, 8
  00B9B60E  mov     ecx, eax
  00B9B610  call    sub_B03580
  00B9B615  push    eax
  00B9B616  call    sub_41D990
  00B9B61B  mov     ecx, [esp+50h+arg_8]
  00B9B61F  add     esp, 8
  00B9B622  push    offset word_F641DC
  00B9B627  push    offset asc_EDAD54
  00B9B62C  push    ecx
  00B9B62D  push    offset aToPilotName
  00B9B632  push    esi
  00B9B633  call    sub_41D990
  00B9B638  add     esp, 8
  00B9B63B  push    eax
  00B9B63C  call    sub_41D990
  00B9B641  add     esp, 8
  00B9B644  push    eax
  00B9B645  call    sub_41D990
  00B9B64A  add     esp, 8
  00B9B64D  push    eax
  00B9B64E  call    sub_41D990
  00B9B653  mov     edx, [esp+50h+arg_C]
  00B9B657  add     esp, 8
  00B9B65A  push    edx
  00B9B65B  push    offset aSendSysmes
  00B9B660  push    esi
  00B9B661  call    sub_41D990
  00B9B666  add     esp, 8
  00B9B669  mov     ecx, eax
  00B9B66B  call    sub_B03580
  00B9B670  push    offset aByte
  00B9B675  mov     eax, ebx
  00B9B677  sub     eax, ebp
  00B9B679  push    eax
  00B9B67A  push    offset asc_EDAD58
  00B9B67F  push    esi
  00B9B680  call    sub_41D990
  00B9B685  add     esp, 8
  00B9B688  mov     ecx, eax
  00B9B68A  call    sub_B03580
  00B9B68F  push    eax
  00B9B690  call    sub_41D990
  00B9B695  add     esp, 8
  00B9B698  mov     esi, eax
  00B9B69A  push    0Ah
  00B9B69C  mov     ecx, esi
  00B9B69E  call    sub_B036E0
  00B9B6A3  mov     ecx, esi
  00B9B6A5  call    sub_40DDF0
  00B9B6AA  mov     edx, [edi]
  00B9B6AC  mov     eax, [edx+58h]
```

## 4. 发送去向切片

```asm
  00B9B6AA  mov     edx, [edi]
  00B9B6AC  mov     eax, [edx+58h]
  00B9B6AF  sub     ebx, ebp
  00B9B6B1  push    ebx
  00B9B6B2  push    ebp
  00B9B6B3  mov     ecx, edi
  00B9B6B5  call    eax
  00B9B6B7  test    al, al
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `00B9B50C` | u16 / 2 |
| `pilotid` | `0xB9B518`;`0xB9B51C` | u32 / 4 |
| `world_id` | `0xB9B52B`;`0xB9B539` | u32 / 4 |
| `to_pilot_name` | `0xB9B533`;`0xB9B541` | str / var |
| `send_sysmes` | `0xB9B55B` | u32 / 4 |
