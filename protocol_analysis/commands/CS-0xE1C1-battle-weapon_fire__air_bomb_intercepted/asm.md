# 汇编证据 —— CS-0xE1C1-battle-weapon_fire__air_bomb_intercepted

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0x00B38E50`（`0x00B38E50`..`0x00B3908A`），函数 `sub_B38E50`
- 命令名字符串：`)<-_proto_battle_client::send_weapon_fire__air_bomb_intercepted(` @ `0x00EE0EB8`
- opcode 写入：`0x00B38ECC`
- 声明容量：`0xE`（分配器容量 `push` @ `0x00B38E96`）
- 提交（`sub_B02FF0`）：`0x00B38F6D`
- 发送去向：`vt[0x58]` @ `0x00B39018`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00B38E9F  push    eax
  00B38EA0  lea     ecx, [esp+4Ch+var_34]
  00B38EA4  call    sub_ABB2F0   ; <<< 初始化 {cur,end}（游标自 buf+2 起）
  00B38EA9  lea     eax, [ebp+0Eh]
  00B38EAC  lea     ecx, [ebp+2]
  00B38EAF  cmp     ecx, eax
  00B38EB1  mov     [esp+48h+var_4], 0
  00B38EB9  mov     [esp+48h+var_30], ebp
  00B38EBD  mov     dword ptr [esp+48h+var_2C], eax
  00B38EC1  ja      loc_B39075
  00B38EC7  lea     edx, [ecx+2]
  00B38ECA  cmp     edx, eax
  00B38ECC  mov     word ptr [ebp+0], 0E1C1h   ; <<< 内联写线（u16）
  00B38ED2  ja      loc_B39075
  00B38ED8  mov     si, word ptr [esp+48h+arg_0]
  00B38EDD  mov     [ecx], si   ; <<< 内联写线（u16）
  00B38EE0  lea     ecx, [edx+4]
  00B38EE3  cmp     ecx, eax
  00B38EE5  ja      loc_B39075
  00B38EEB  mov     eax, [esp+48h+arg_4]
  00B38EEF  mov     [esp+48h+var_30], ecx
  00B38EF3  lea     ecx, [esp+48h+var_30]
  00B38EF7  mov     [edx], eax   ; <<< 内联写线（u32）
  00B38EF9  push    ecx
  00B38EFA  lea     edx, [esp+4Ch+arg_8]
  00B38EFE  push    edx
  00B38EFF  call    sub_B02D80   ; <<< 写线原语 u32
  00B38F04  add     esp, 8
  00B38F07  test    al, al
  00B38F09  jz      loc_B39075
  00B38F0F  mov     esi, [edi+3E14h]
  00B38F15  test    esi, esi
  00B38F17  mov     ebx, [esp+48h+var_30]
  00B38F1B  jz      loc_B39016
  00B38F21  lea     eax, [esp+48h+var_28]
  00B38F25  push    eax
  00B38F26  call    sub_CA0CE0
  00B38F2B  add     esp, 4
  00B38F2E  mov     ecx, [edi+8]
  00B38F31  push    offset aProtoBattleCli_238
  00B38F36  push    ecx
  00B38F37  push    offset aId
  00B38F3C  push    eax
  00B38F3D  push    esi
  00B38F3E  mov     byte ptr [esp+5Ch+var_4], 1
  00B38F43  call    sub_B03020
  00B38F48  add     esp, 8
  00B38F4B  push    eax
  00B38F4C  call    sub_41D990
  00B38F51  add     esp, 8
  00B38F54  mov     ecx, eax
  00B38F56  call    sub_ADC810
  00B38F5B  push    eax
  00B38F5C  call    sub_41D990
  00B38F61  add     esp, 8
  00B38F64  lea     ecx, [esp+48h+var_28]
  00B38F68  mov     byte ptr [esp+48h+var_4], 0
  00B38F6D  call    sub_B02FF0   ; <<< 提交（C→S 闭合点）
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00B38F6D  call    sub_B02FF0
  00B38F72  mov     edx, [esp+48h+arg_0]
  00B38F76  push    offset word_F641DC
  00B38F7B  push    edx
  00B38F7C  push    offset aEntId
  00B38F81  push    esi
  00B38F82  call    sub_41D990
  00B38F87  add     esp, 8
  00B38F8A  mov     ecx, eax
  00B38F8C  call    sub_B032A0
  00B38F91  push    eax
  00B38F92  call    sub_41D990
  00B38F97  mov     eax, [esp+50h+arg_4]
  00B38F9B  add     esp, 8
  00B38F9E  push    offset word_F641DC
  00B38FA3  push    eax
  00B38FA4  push    offset aAirbombId
  00B38FA9  push    esi
  00B38FAA  call    sub_41D990
  00B38FAF  add     esp, 8
  00B38FB2  mov     ecx, eax
  00B38FB4  call    sub_B03580
  00B38FB9  push    eax
  00B38FBA  call    sub_41D990
  00B38FBF  mov     ecx, [esp+50h+arg_8]
  00B38FC3  add     esp, 8
  00B38FC6  push    ecx
  00B38FC7  push    offset aArmsId
  00B38FCC  push    esi
  00B38FCD  call    sub_41D990
  00B38FD2  add     esp, 8
  00B38FD5  mov     ecx, eax
  00B38FD7  call    sub_B03580
  00B38FDC  push    offset aByte
  00B38FE1  mov     edx, ebx
  00B38FE3  sub     edx, ebp
  00B38FE5  push    edx
  00B38FE6  push    offset asc_EDAD58
  00B38FEB  push    esi
  00B38FEC  call    sub_41D990
  00B38FF1  add     esp, 8
  00B38FF4  mov     ecx, eax
  00B38FF6  call    sub_B03580
  00B38FFB  push    eax
  00B38FFC  call    sub_41D990
  00B39001  add     esp, 8
  00B39004  mov     esi, eax
  00B39006  push    0Ah
  00B39008  mov     ecx, esi
  00B3900A  call    sub_B036E0
  00B3900F  mov     ecx, esi
  00B39011  call    sub_40DDF0
  00B39016  mov     eax, [edi]
  00B39018  mov     edx, [eax+58h]
```

## 4. 发送去向切片

```asm
  00B39016  mov     eax, [edi]
  00B39018  mov     edx, [eax+58h]
  00B3901B  sub     ebx, ebp
  00B3901D  push    ebx
  00B3901E  push    ebp
  00B3901F  mov     ecx, edi
  00B39021  call    edx
  00B39023  test    al, al
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `00B38ECC` | u16 / 2 |
| `ent_id` | `0xB38ED8`;`0xB38EDD` | u16 / 2 |
| `airbomb_id` | `0xB38EEB`;`0xB38EF7` | u32 / 4 |
| `arms_id` | `0xB38EFF` | u32 / 4 |
