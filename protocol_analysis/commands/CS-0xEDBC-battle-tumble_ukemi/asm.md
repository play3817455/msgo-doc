# 汇编证据 —— CS-0xEDBC-battle-tumble_ukemi

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0x00B35980`（`0x00B35980`..`0x00B35B65`），函数 `sub_B35980`
- 命令名字符串：`)<-_proto_battle_client::send_tumble_ukemi(` @ `0x00EE0B64`
- opcode 写入：`0x00B359F4`
- 声明容量：`0xA`（分配器容量 `push` @ `0x00B359C6`）
- 提交（`sub_B02FF0`）：`0x00B35A73`
- 发送去向：`vt[0x58]` @ `0x00B35AF6`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00B359CF  push    eax
  00B359D0  lea     ecx, [esp+44h+var_2C]
  00B359D4  call    sub_ABB2F0   ; <<< 初始化 {cur,end}（游标自 buf+2 起）
  00B359D9  lea     eax, [ebp+0Ah]
  00B359DC  lea     ecx, [ebp+2]
  00B359DF  cmp     ecx, eax
  00B359E1  mov     [esp+40h+var_4], 0
  00B359E9  ja      loc_B35B50
  00B359EF  lea     edx, [ecx+2]
  00B359F2  cmp     edx, eax
  00B359F4  mov     word ptr [ebp+0], 0EDBCh   ; <<< 内联写线（u16）
  00B359FA  ja      loc_B35B50
  00B35A00  mov     si, word ptr [esp+40h+arg_0]
  00B35A05  lea     ebx, [edx+4]
  00B35A08  cmp     ebx, eax
  00B35A0A  mov     [ecx], si   ; <<< 内联写线（u16）
  00B35A0D  ja      loc_B35B50
  00B35A13  mov     ecx, [esp+40h+arg_4]
  00B35A17  mov     [edx], ecx   ; <<< 内联写线（u32）
  00B35A19  mov     esi, [edi+3DA4h]
  00B35A1F  test    esi, esi
  00B35A21  jz      loc_B35AF4
  00B35A27  lea     edx, [esp+40h+var_28]
  00B35A2B  push    edx
  00B35A2C  call    sub_CA0CE0
  00B35A31  add     esp, 4
  00B35A34  mov     ecx, [edi+8]
  00B35A37  push    offset aProtoBattleCli_260
  00B35A3C  push    ecx
  00B35A3D  push    offset aId
  00B35A42  push    eax
  00B35A43  push    esi
  00B35A44  mov     byte ptr [esp+54h+var_4], 1
  00B35A49  call    sub_B03020
  00B35A4E  add     esp, 8
  00B35A51  push    eax
  00B35A52  call    sub_41D990
  00B35A57  add     esp, 8
  00B35A5A  mov     ecx, eax
  00B35A5C  call    sub_ADC810
  00B35A61  push    eax
  00B35A62  call    sub_41D990
  00B35A67  add     esp, 8
  00B35A6A  lea     ecx, [esp+40h+var_28]
  00B35A6E  mov     byte ptr [esp+40h+var_4], 0
  00B35A73  call    sub_B02FF0   ; <<< 提交（C→S 闭合点）
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00B35A73  call    sub_B02FF0
  00B35A78  mov     edx, [esp+40h+arg_0]
  00B35A7C  push    offset word_F641DC
  00B35A81  push    edx
  00B35A82  push    offset aAiEntId
  00B35A87  push    esi
  00B35A88  call    sub_41D990
  00B35A8D  add     esp, 8
  00B35A90  mov     ecx, eax
  00B35A92  call    sub_B032A0
  00B35A97  push    eax
  00B35A98  call    sub_41D990
  00B35A9D  mov     eax, [esp+48h+arg_4]
  00B35AA1  add     esp, 8
  00B35AA4  push    eax
  00B35AA5  push    offset aTmp
  00B35AAA  push    esi
  00B35AAB  call    sub_41D990
  00B35AB0  add     esp, 8
  00B35AB3  mov     ecx, eax
  00B35AB5  call    sub_B03580
  00B35ABA  push    offset aByte
  00B35ABF  mov     ecx, ebx
  00B35AC1  sub     ecx, ebp
  00B35AC3  push    ecx
  00B35AC4  push    offset asc_EDAD58
  00B35AC9  push    esi
  00B35ACA  call    sub_41D990
  00B35ACF  add     esp, 8
  00B35AD2  mov     ecx, eax
  00B35AD4  call    sub_B03580
  00B35AD9  push    eax
  00B35ADA  call    sub_41D990
  00B35ADF  add     esp, 8
  00B35AE2  mov     esi, eax
  00B35AE4  push    0Ah
  00B35AE6  mov     ecx, esi
  00B35AE8  call    sub_B036E0
  00B35AED  mov     ecx, esi
  00B35AEF  call    sub_40DDF0
  00B35AF4  mov     edx, [edi]
  00B35AF6  mov     eax, [edx+58h]
```

## 4. 发送去向切片

```asm
  00B35AF4  mov     edx, [edi]
  00B35AF6  mov     eax, [edx+58h]
  00B35AF9  sub     ebx, ebp
  00B35AFB  push    ebx
  00B35AFC  push    ebp
  00B35AFD  mov     ecx, edi
  00B35AFF  call    eax
  00B35B01  test    al, al
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `00B359F4` | u16 / 2 |
| `AI_ent_id` | `0xB35A00`;`0xB35A0A` | u16 / 2 |
| `tmp` | `0xB35A13`;`0xB35A17` | u32 / 4 |
