# 汇编证据 —— CS-0xDDD4-lounge-btlroom_ev_caravan_mission_start

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0x00B90830`（`0x00B90830`..`0x00B909DD`），函数 `sub_B90830`
- 命令名字符串：`)<-_proto_lounge_client::send_btlroom_ev_caravan_mission_start(` @ `0x00EEAEB8`
- opcode 写入：`0x00B908A4`
- 声明容量：`0x6`（分配器容量 `push` @ `0x00B90876`）
- 提交（`sub_B02FF0`）：`0x00B90910`
- 发送去向：`vt[0x58]` @ `0x00B9096B`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00B9087F  push    eax
  00B90880  lea     ecx, [esp+44h+var_2C]
  00B90884  call    sub_ABB2F0   ; <<< 初始化 {cur,end}（游标自 buf+2 起）
  00B90889  lea     ecx, [ebp+6]
  00B9088C  lea     eax, [ebp+2]
  00B9088F  cmp     eax, ecx
  00B90891  mov     [esp+40h+var_4], 0
  00B90899  ja      loc_B909C8
  00B9089F  lea     ebx, [eax+4]
  00B908A2  cmp     ebx, ecx
  00B908A4  mov     word ptr [ebp+0], 0DDD4h   ; <<< 内联写线（u16）
  00B908AA  ja      loc_B909C8
  00B908B0  mov     ecx, [esp+40h+arg_0]
  00B908B4  mov     [eax], ecx   ; <<< 内联写线（u32）
  00B908B6  mov     edi, [esi+7C08h]
  00B908BC  test    edi, edi
  00B908BE  jz      loc_B90969
  00B908C4  lea     edx, [esp+40h+var_28]
  00B908C8  push    edx
  00B908C9  call    sub_CA0CE0
  00B908CE  add     esp, 4
  00B908D1  mov     ecx, [esi+8]
  00B908D4  push    offset aProtoLoungeCli_561
  00B908D9  push    ecx
  00B908DA  push    offset aId
  00B908DF  push    eax
  00B908E0  push    edi
  00B908E1  mov     byte ptr [esp+54h+var_4], 1
  00B908E6  call    sub_B03020
  00B908EB  add     esp, 8
  00B908EE  push    eax
  00B908EF  call    sub_41D990
  00B908F4  add     esp, 8
  00B908F7  mov     ecx, eax
  00B908F9  call    sub_ADC810
  00B908FE  push    eax
  00B908FF  call    sub_41D990
  00B90904  add     esp, 8
  00B90907  lea     ecx, [esp+40h+var_28]
  00B9090B  mov     byte ptr [esp+40h+var_4], 0
  00B90910  call    sub_B02FF0   ; <<< 提交（C→S 闭合点）
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00B90910  call    sub_B02FF0
  00B90915  mov     edx, [esp+40h+arg_0]
  00B90919  push    edx
  00B9091A  push    offset aRoomId
  00B9091F  push    edi
  00B90920  call    sub_41D990
  00B90925  add     esp, 8
  00B90928  mov     ecx, eax
  00B9092A  call    sub_B03580
  00B9092F  push    offset aByte
  00B90934  mov     eax, ebx
  00B90936  sub     eax, ebp
  00B90938  push    eax
  00B90939  push    offset asc_EDAD58
  00B9093E  push    edi
  00B9093F  call    sub_41D990
  00B90944  add     esp, 8
  00B90947  mov     ecx, eax
  00B90949  call    sub_B03580
  00B9094E  push    eax
  00B9094F  call    sub_41D990
  00B90954  add     esp, 8
  00B90957  mov     edi, eax
  00B90959  push    0Ah
  00B9095B  mov     ecx, edi
  00B9095D  call    sub_B036E0
  00B90962  mov     ecx, edi
  00B90964  call    sub_40DDF0
  00B90969  mov     edx, [esi]
  00B9096B  mov     eax, [edx+58h]
```

## 4. 发送去向切片

```asm
  00B90969  mov     edx, [esi]
  00B9096B  mov     eax, [edx+58h]
  00B9096E  sub     ebx, ebp
  00B90970  push    ebx
  00B90971  push    ebp
  00B90972  mov     ecx, esi
  00B90974  call    eax
  00B90976  test    al, al
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `00B908A4` | u16 / 2 |
| `room_id` | `0xB908B4` | u32 / 4 |
