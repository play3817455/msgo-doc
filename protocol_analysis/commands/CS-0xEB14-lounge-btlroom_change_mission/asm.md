# 汇编证据 —— CS-0xEB14-lounge-btlroom_change_mission

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0x00B905D0`（`0x00B905D0`..`0x00B9082F`），函数 `sub_B905D0`
- 命令名字符串：`)<-_proto_lounge_client::send_btlroom_change_mission(` @ `0x00EEAE80`
- opcode 写入：`0x00B90653`
- 声明容量：`0x56`（分配器容量 `push` @ `0x00B90616`）
- 提交（`sub_B02FF0`）：`0x00B90700`
- 发送去向：`vt[0x58]` @ `0x00B907BD`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00B9061F  push    eax
  00B90620  lea     ecx, [esp+4Ch+var_34]
  00B90624  call    sub_ABB2F0   ; <<< 初始化 {cur,end}（游标自 buf+2 起）
  00B90629  lea     ecx, [ebp+56h]
  00B9062C  lea     eax, [ebp+2]
  00B9062F  cmp     eax, ecx
  00B90631  mov     [esp+48h+var_4], 0
  00B90639  mov     [esp+48h+var_30], ebp
  00B9063D  mov     dword ptr [esp+48h+var_2C], ecx
  00B90641  ja      loc_B9081A
  00B90647  mov     edx, [esp+48h+arg_0]
  00B9064B  push    49h
  00B9064D  lea     ecx, [esp+4Ch+var_30]
  00B90651  push    ecx
  00B90652  push    edx
  00B90653  mov     word ptr [ebp+0], 0EB14h   ; <<< 内联写线（u16）
  00B90659  mov     [esp+54h+var_30], eax
  00B9065D  call    sub_B02B40   ; <<< 写线原语 str
  00B90662  add     esp, 0Ch
  00B90665  test    al, al
  00B90667  jz      loc_B9081A
  00B9066D  mov     ecx, [esp+48h+var_30]
  00B90671  lea     eax, [ecx+4]
  00B90674  cmp     eax, dword ptr [esp+48h+var_2C]
  00B90678  ja      loc_B9081A
  00B9067E  mov     edx, dword ptr [esp+48h+arg_4]
  00B90682  mov     [esp+48h+var_30], eax
  00B90686  lea     eax, [esp+48h+var_30]
  00B9068A  mov     [ecx], edx   ; <<< 内联写线（u32）
  00B9068C  push    eax
  00B9068D  lea     ecx, [esp+4Ch+arg_8]
  00B90691  push    ecx
  00B90692  call    sub_B061C0   ; <<< 写线原语 u8
  00B90697  add     esp, 8
  00B9069A  test    al, al
  00B9069C  jz      loc_B9081A
  00B906A2  mov     esi, [edi+7C00h]
  00B906A8  test    esi, esi
  00B906AA  mov     ebx, [esp+48h+var_30]
  00B906AE  jz      loc_B907BB
  00B906B4  lea     edx, [esp+48h+var_28]
  00B906B8  push    edx
  00B906B9  call    sub_CA0CE0
  00B906BE  add     esp, 4
  00B906C1  mov     ecx, [edi+8]
  00B906C4  push    offset aProtoLoungeCli_410
  00B906C9  push    ecx
  00B906CA  push    offset aId
  00B906CF  push    eax
  00B906D0  push    esi
  00B906D1  mov     byte ptr [esp+5Ch+var_4], 1
  00B906D6  call    sub_B03020
  00B906DB  add     esp, 8
  00B906DE  push    eax
  00B906DF  call    sub_41D990
  00B906E4  add     esp, 8
  00B906E7  mov     ecx, eax
  00B906E9  call    sub_ADC810
  00B906EE  push    eax
  00B906EF  call    sub_41D990
  00B906F4  add     esp, 8
  00B906F7  lea     ecx, [esp+48h+var_28]
  00B906FB  mov     byte ptr [esp+48h+var_4], 0
  00B90700  call    sub_B02FF0   ; <<< 提交（C→S 闭合点）
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00B90700  call    sub_B02FF0
  00B90705  mov     edx, [esp+48h+arg_0]
  00B90709  push    offset word_F641DC
  00B9070E  push    offset asc_EDAD54
  00B90713  push    edx
  00B90714  push    offset aRoomName
  00B90719  push    esi
  00B9071A  call    sub_41D990
  00B9071F  add     esp, 8
  00B90722  push    eax
  00B90723  call    sub_41D990
  00B90728  add     esp, 8
  00B9072B  push    eax
  00B9072C  call    sub_41D990
  00B90731  add     esp, 8
  00B90734  push    eax
  00B90735  call    sub_41D990
  00B9073A  mov     eax, dword ptr [esp+50h+arg_4]
  00B9073E  add     esp, 8
  00B90741  push    offset word_F641DC
  00B90746  push    eax
  00B90747  push    offset aMissionId
  00B9074C  push    esi
  00B9074D  call    sub_41D990
  00B90752  add     esp, 8
  00B90755  mov     ecx, eax
  00B90757  call    sub_B03580
  00B9075C  push    eax
  00B9075D  call    sub_41D990
  00B90762  add     esp, 8
  00B90765  lea     ecx, [esp+48h+arg_8]
  00B90769  push    ecx
  00B9076A  push    offset aIsLock
  00B9076F  push    esi
  00B90770  call    sub_41D990
  00B90775  add     esp, 8
  00B90778  push    eax
  00B90779  call    sub_B0C1F0
  00B9077E  add     esp, 8
  00B90781  push    offset aByte
  00B90786  mov     edx, ebx
  00B90788  sub     edx, ebp
  00B9078A  push    edx
  00B9078B  push    offset asc_EDAD58
  00B90790  push    esi
  00B90791  call    sub_41D990
  00B90796  add     esp, 8
  00B90799  mov     ecx, eax
  00B9079B  call    sub_B03580
  00B907A0  push    eax
  00B907A1  call    sub_41D990
  00B907A6  add     esp, 8
  00B907A9  mov     esi, eax
  00B907AB  push    0Ah
  00B907AD  mov     ecx, esi
  00B907AF  call    sub_B036E0
  00B907B4  mov     ecx, esi
  00B907B6  call    sub_40DDF0
  00B907BB  mov     eax, [edi]
  00B907BD  mov     edx, [eax+58h]
```

## 4. 发送去向切片

```asm
  00B907BB  mov     eax, [edi]
  00B907BD  mov     edx, [eax+58h]
  00B907C0  sub     ebx, ebp
  00B907C2  push    ebx
  00B907C3  push    ebp
  00B907C4  mov     ecx, edi
  00B907C6  call    edx
  00B907C8  test    al, al
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `00B90653` | u16 / 2 |
| `room_name` | `0xB9064B`;`0xB9065D` | str / var |
| `mission_id` | `0xB9067E`;`0xB9068A` | u32 / 4 |
| `is_lock` | `0xB90692` | u8 / 1 |
