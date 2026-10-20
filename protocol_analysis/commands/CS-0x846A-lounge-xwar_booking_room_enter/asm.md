# 汇编证据 —— CS-0x846A-lounge-xwar_booking_room_enter

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B918E0 @ `0xb918e0`（`0xb918e0`..`0xb91ac6`）
- 命令名字符串：`)<-_proto_lounge_client::send_xwar_booking_room_enter(` @ `0xeeb0b8`
- opcode 写入：`0xb91954`
- 声明容量：`0xA`（分配器容量 `push` @ `0xb91926`）

## 2. 组包块切片（游标初始化 → 逐字段写线 → 提交）

```asm
  0xb9192a  mov     ebp, eax
  0xb9192c  mov     eax, [edi+0Ch]
  0xb9192f  push    eax
  0xb91930  lea     ecx, [esp+44h+var_2C]
  0xb91934  call    sub_ABB2F0
  0xb91939  lea     ecx, [ebp+0Ah]
  0xb9193c  lea     eax, [ebp+2]
  0xb9193f  cmp     eax, ecx
  0xb91941  mov     [esp+40h+var_4], 0
  0xb91949  ja      loc_B91AB1
  0xb9194f  lea     edx, [eax+4]
  0xb91952  cmp     edx, ecx
  0xb91954  mov     word ptr [ebp+0], 846Ah
  0xb9195a  ja      loc_B91AB1
  0xb91960  mov     esi, [esp+40h+arg_0]
  0xb91964  lea     ebx, [edx+4]
  0xb91967  cmp     ebx, ecx
  0xb91969  mov     [eax], esi
  0xb9196b  ja      loc_B91AB1
  0xb91971  mov     ecx, [esp+40h+arg_4]
  0xb91975  mov     [edx], ecx
  0xb91977  mov     esi, [edi+7C60h]
  0xb9197d  test    esi, esi
  0xb9197f  jz      loc_B91A52
  0xb91985  lea     edx, [esp+40h+var_28]
  0xb91989  push    edx
  0xb9198a  call    sub_CA0CE0
  0xb9198f  add     esp, 4
  0xb91992  mov     ecx, [edi+8]
  0xb91995  push    offset aProtoLoungeCli_359; ")<-_proto_lounge_client::send_xwar_book"...
  0xb9199a  push    ecx
  0xb9199b  push    offset aId; " (id:"
  0xb919a0  push    eax
  0xb919a1  push    esi
  0xb919a2  mov     byte ptr [esp+54h+var_4], 1
  0xb919a7  call    sub_B03020
  0xb919ac  add     esp, 8
  0xb919af  push    eax
  0xb919b0  call    sub_41D990
  0xb919b5  add     esp, 8
  0xb919b8  mov     ecx, eax
  0xb919ba  call    sub_ADC810
  0xb919bf  push    eax
  0xb919c0  call    sub_41D990
  0xb919c5  add     esp, 8
  0xb919c8  lea     ecx, [esp+40h+var_28]
  0xb919cc  mov     byte ptr [esp+40h+var_4], 0
  0xb919d1  call    sub_B02FF0
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。
> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B02B40`=写 NUL 串（其**紧邻之前的 `push N`** = 串槽预算）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb919e0  push    offset aMatchingType; "matching_type="
  0xb91a03  push    offset aRoomId; "room_id="
  0xb91a18  push    offset aByte; "]byte"
  0xb91a22  push    offset asc_EDAD58; " ) ["
```

## 4. 发送去向切片

```asm
  0xb91a54  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xb91954` | u16 |
| `matching_type` | `0xB91969` | u32 |
| `room_id` | `0xB91975` | u32 |
