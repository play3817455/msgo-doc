# 汇编证据 —— CS-0xDEE6-lounge-pilot_tutorial_flag_set

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0x00B8B380`（`0x00B8B380`..`0x00B8B533`），函数 `sub_B8B380`
- 命令名字符串：`)<-_proto_lounge_client::send_pilot_tutorial_flag_set(` @ `0x00EEA510`
- opcode 写入：`0x00B8B3F1`
- 声明容量：`0xA`（分配器容量 `push` @ `0x00B8B3C3`）
- 提交（`sub_B02FF0`）：`0x00B8B464`
- 发送去向：`vt[0x58]` @ `0x00B8B4C4`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00B8B3CC  push    eax
  00B8B3CD  lea     ecx, [esp+44h+var_2C]
  00B8B3D1  call    sub_ABB2F0   ; <<< 初始化 {cur,end}（游标自 buf+2 起）
  00B8B3D6  lea     ecx, [ebp+0Ah]
  00B8B3D9  lea     eax, [ebp+2]
  00B8B3DC  cmp     eax, ecx
  00B8B3DE  mov     [esp+40h+var_4], 0
  00B8B3E6  ja      loc_B8B51E
  00B8B3EC  lea     ebx, [eax+8]
  00B8B3EF  cmp     ebx, ecx
  00B8B3F1  mov     word ptr [ebp+0], 0DEE6h   ; <<< 内联写线（u16）
  00B8B3F7  ja      loc_B8B51E
  00B8B3FD  mov     ecx, [esp+40h+arg_0]
  00B8B401  mov     edx, [esp+40h+arg_4]
  00B8B405  mov     [eax], ecx   ; <<< 内联写线（u32）
  00B8B407  mov     [eax+4], edx   ; <<< 内联写线（u32）
  00B8B40A  mov     edi, [esi+7A30h]
  00B8B410  test    edi, edi
  00B8B412  jz      loc_B8B4C2
  00B8B418  lea     eax, [esp+40h+var_28]
  00B8B41C  push    eax
  00B8B41D  call    sub_CA0CE0
  00B8B422  add     esp, 4
  00B8B425  mov     ecx, [esi+8]
  00B8B428  push    offset aProtoLoungeCli_354
  00B8B42D  push    ecx
  00B8B42E  push    offset aId
  00B8B433  push    eax
  00B8B434  push    edi
  00B8B435  mov     byte ptr [esp+54h+var_4], 1
  00B8B43A  call    sub_B03020
  00B8B43F  add     esp, 8
  00B8B442  push    eax
  00B8B443  call    sub_41D990
  00B8B448  add     esp, 8
  00B8B44B  mov     ecx, eax
  00B8B44D  call    sub_ADC810
  00B8B452  push    eax
  00B8B453  call    sub_41D990
  00B8B458  add     esp, 8
  00B8B45B  lea     ecx, [esp+40h+var_28]
  00B8B45F  mov     byte ptr [esp+40h+var_4], 0
  00B8B464  call    sub_B02FF0   ; <<< 提交（C→S 闭合点）
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00B8B464  call    sub_B02FF0
  00B8B469  mov     edx, [esp+40h+arg_4]
  00B8B46D  mov     eax, [esp+40h+arg_0]
  00B8B471  push    edx
  00B8B472  push    eax
  00B8B473  push    offset aTutoFlag
  00B8B478  push    edi
  00B8B479  call    sub_41D990
  00B8B47E  add     esp, 8
  00B8B481  mov     ecx, eax
  00B8B483  call    sub_B08500
  00B8B488  push    offset aByte
  00B8B48D  mov     ecx, ebx
  00B8B48F  sub     ecx, ebp
  00B8B491  push    ecx
  00B8B492  push    offset asc_EDAD58
  00B8B497  push    edi
  00B8B498  call    sub_41D990
  00B8B49D  add     esp, 8
  00B8B4A0  mov     ecx, eax
  00B8B4A2  call    sub_B03580
  00B8B4A7  push    eax
  00B8B4A8  call    sub_41D990
  00B8B4AD  add     esp, 8
  00B8B4B0  mov     edi, eax
  00B8B4B2  push    0Ah
  00B8B4B4  mov     ecx, edi
  00B8B4B6  call    sub_B036E0
  00B8B4BB  mov     ecx, edi
  00B8B4BD  call    sub_40DDF0
  00B8B4C2  mov     edx, [esi]
  00B8B4C4  mov     eax, [edx+58h]
```

## 4. 发送去向切片

```asm
  00B8B4C2  mov     edx, [esi]
  00B8B4C4  mov     eax, [edx+58h]
  00B8B4C7  sub     ebx, ebp
  00B8B4C9  push    ebx
  00B8B4CA  push    ebp
  00B8B4CB  mov     ecx, esi
  00B8B4CD  call    eax
  00B8B4CF  test    al, al
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `00B8B3F1` | u16 / 2 |
| `tuto_flag` | `0xB8B405`;`0xB8B407` | u64 / 8 |
