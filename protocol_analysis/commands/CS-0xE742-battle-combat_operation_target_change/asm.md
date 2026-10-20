# 汇编证据 —— CS-0xE742-battle-combat_operation_target_change

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0x00B3F1B0`（`0x00B3F1B0`..`0x00B3F3EE`），函数 `sub_B3F1B0`
- 命令名字符串：`)<-_proto_battle_client::send_combat_operation_target_change(` @ `0x00EE1604`
- opcode 写入：`0x00B3F22C`
- 声明容量：`0xE`（分配器容量 `push` @ `0x00B3F1F6`）
- 提交（`sub_B02FF0`）：`0x00B3F2D1`
- 发送去向：`vt[0x58]` @ `0x00B3F37C`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00B3F1FF  push    eax
  00B3F200  lea     ecx, [esp+4Ch+var_34]
  00B3F204  call    sub_ABB2F0   ; <<< 初始化 {cur,end}（游标自 buf+2 起）
  00B3F209  lea     ecx, [ebp+0Eh]
  00B3F20C  lea     eax, [ebp+2]
  00B3F20F  cmp     eax, ecx
  00B3F211  mov     [esp+48h+var_4], 0
  00B3F219  mov     [esp+48h+var_30], ebp
  00B3F21D  mov     dword ptr [esp+48h+var_2C], ecx
  00B3F221  ja      loc_B3F3D9
  00B3F227  lea     edx, [eax+2]
  00B3F22A  cmp     edx, ecx
  00B3F22C  mov     word ptr [ebp+0], 0E742h   ; <<< 内联写线（u16）
  00B3F232  ja      loc_B3F3D9
  00B3F238  mov     si, word ptr [esp+48h+arg_0]
  00B3F23D  mov     [eax], si   ; <<< 内联写线（u16）
  00B3F240  mov     eax, edx
  00B3F242  lea     edx, [eax+2]
  00B3F245  cmp     edx, ecx
  00B3F247  ja      loc_B3F3D9
  00B3F24D  mov     cx, word ptr [esp+48h+arg_4]
  00B3F252  mov     [esp+48h+var_30], edx
  00B3F256  lea     edx, [esp+48h+var_30]
  00B3F25A  mov     [eax], cx   ; <<< 内联写线（u16）
  00B3F25D  push    edx
  00B3F25E  lea     eax, [esp+4Ch+arg_8]
  00B3F262  push    eax
  00B3F263  call    sub_B02DA0   ; <<< 写线原语 u16
  00B3F268  add     esp, 8
  00B3F26B  test    al, al
  00B3F26D  jz      loc_B3F3D9
  00B3F273  mov     esi, [edi+3FCCh]
  00B3F279  test    esi, esi
  00B3F27B  mov     ebx, [esp+48h+var_30]
  00B3F27F  jz      loc_B3F37A
  00B3F285  lea     ecx, [esp+48h+var_28]
  00B3F289  push    ecx
  00B3F28A  call    sub_CA0CE0
  00B3F28F  add     esp, 4
  00B3F292  mov     edx, [edi+8]
  00B3F295  push    offset aProtoBattleCli_281
  00B3F29A  push    edx
  00B3F29B  push    offset aId
  00B3F2A0  push    eax
  00B3F2A1  push    esi
  00B3F2A2  mov     byte ptr [esp+5Ch+var_4], 1
  00B3F2A7  call    sub_B03020
  00B3F2AC  add     esp, 8
  00B3F2AF  push    eax
  00B3F2B0  call    sub_41D990
  00B3F2B5  add     esp, 8
  00B3F2B8  mov     ecx, eax
  00B3F2BA  call    sub_ADC810
  00B3F2BF  push    eax
  00B3F2C0  call    sub_41D990
  00B3F2C5  add     esp, 8
  00B3F2C8  lea     ecx, [esp+48h+var_28]
  00B3F2CC  mov     byte ptr [esp+48h+var_4], 0
  00B3F2D1  call    sub_B02FF0   ; <<< 提交（C→S 闭合点）
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00B3F2D1  call    sub_B02FF0
  00B3F2D6  mov     eax, [esp+48h+arg_0]
  00B3F2DA  push    offset word_F641DC
  00B3F2DF  push    eax
  00B3F2E0  push    offset aTargetX
  00B3F2E5  push    esi
  00B3F2E6  call    sub_41D990
  00B3F2EB  add     esp, 8
  00B3F2EE  mov     ecx, eax
  00B3F2F0  call    sub_B032A0
  00B3F2F5  push    eax
  00B3F2F6  call    sub_41D990
  00B3F2FB  mov     ecx, [esp+50h+arg_4]
  00B3F2FF  add     esp, 8
  00B3F302  push    offset word_F641DC
  00B3F307  push    ecx
  00B3F308  push    offset aTargetY
  00B3F30D  push    esi
  00B3F30E  call    sub_41D990
  00B3F313  add     esp, 8
  00B3F316  mov     ecx, eax
  00B3F318  call    sub_B032A0
  00B3F31D  push    eax
  00B3F31E  call    sub_41D990
  00B3F323  mov     edx, [esp+50h+arg_8]
  00B3F327  add     esp, 8
  00B3F32A  push    edx
  00B3F32B  push    offset aTargetZ
  00B3F330  push    esi
  00B3F331  call    sub_41D990
  00B3F336  add     esp, 8
  00B3F339  mov     ecx, eax
  00B3F33B  call    sub_B032A0
  00B3F340  push    offset aByte
  00B3F345  mov     eax, ebx
  00B3F347  sub     eax, ebp
  00B3F349  push    eax
  00B3F34A  push    offset asc_EDAD58
  00B3F34F  push    esi
  00B3F350  call    sub_41D990
  00B3F355  add     esp, 8
  00B3F358  mov     ecx, eax
  00B3F35A  call    sub_B03580
  00B3F35F  push    eax
  00B3F360  call    sub_41D990
  00B3F365  add     esp, 8
  00B3F368  mov     esi, eax
  00B3F36A  push    0Ah
  00B3F36C  mov     ecx, esi
  00B3F36E  call    sub_B036E0
  00B3F373  mov     ecx, esi
  00B3F375  call    sub_40DDF0
  00B3F37A  mov     edx, [edi]
  00B3F37C  mov     eax, [edx+58h]
```

## 4. 发送去向切片

```asm
  00B3F37A  mov     edx, [edi]
  00B3F37C  mov     eax, [edx+58h]
  00B3F37F  sub     ebx, ebp
  00B3F381  push    ebx
  00B3F382  push    ebp
  00B3F383  mov     ecx, edi
  00B3F385  call    eax
  00B3F387  test    al, al
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `00B3F22C` | u16 / 2 |
| `target_x` | `0xB3F238`;`0xB3F23D` | u16 / 2 |
| `target_y` | `0xB3F24D`;`0xB3F25A` | u16 / 2 |
| `target_z` | `0xB3F263` | u16 / 2 |
