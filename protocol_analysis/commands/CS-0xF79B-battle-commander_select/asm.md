# 汇编证据 —— CS-0xF79B-battle-commander_select

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0x00B3DEA0`（`0x00B3DEA0`..`0x00B3E04D`），函数 `sub_B3DEA0`
- 命令名字符串：`)<-_proto_battle_client::send_commander_select(` @ `0x00EE13E0`
- opcode 写入：`0x00B3DF14`
- 声明容量：`0x6`（分配器容量 `push` @ `0x00B3DEE6`）
- 提交（`sub_B02FF0`）：`0x00B3DF80`
- 发送去向：`vt[0x58]` @ `0x00B3DFDB`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00B3DEEF  push    eax
  00B3DEF0  lea     ecx, [esp+44h+var_2C]
  00B3DEF4  call    sub_ABB2F0   ; <<< 初始化 {cur,end}（游标自 buf+2 起）
  00B3DEF9  lea     ecx, [ebp+6]
  00B3DEFC  lea     eax, [ebp+2]
  00B3DEFF  cmp     eax, ecx
  00B3DF01  mov     [esp+40h+var_4], 0
  00B3DF09  ja      loc_B3E038
  00B3DF0F  lea     ebx, [eax+4]
  00B3DF12  cmp     ebx, ecx
  00B3DF14  mov     word ptr [ebp+0], 0F79Bh   ; <<< 内联写线（u16）
  00B3DF1A  ja      loc_B3E038
  00B3DF20  mov     ecx, [esp+40h+arg_0]
  00B3DF24  mov     [eax], ecx   ; <<< 内联写线（u32）
  00B3DF26  mov     edi, [esi+3F44h]
  00B3DF2C  test    edi, edi
  00B3DF2E  jz      loc_B3DFD9
  00B3DF34  lea     edx, [esp+40h+var_28]
  00B3DF38  push    edx
  00B3DF39  call    sub_CA0CE0
  00B3DF3E  add     esp, 4
  00B3DF41  mov     ecx, [esi+8]
  00B3DF44  push    offset aProtoBattleCli_292
  00B3DF49  push    ecx
  00B3DF4A  push    offset aId
  00B3DF4F  push    eax
  00B3DF50  push    edi
  00B3DF51  mov     byte ptr [esp+54h+var_4], 1
  00B3DF56  call    sub_B03020
  00B3DF5B  add     esp, 8
  00B3DF5E  push    eax
  00B3DF5F  call    sub_41D990
  00B3DF64  add     esp, 8
  00B3DF67  mov     ecx, eax
  00B3DF69  call    sub_ADC810
  00B3DF6E  push    eax
  00B3DF6F  call    sub_41D990
  00B3DF74  add     esp, 8
  00B3DF77  lea     ecx, [esp+40h+var_28]
  00B3DF7B  mov     byte ptr [esp+40h+var_4], 0
  00B3DF80  call    sub_B02FF0   ; <<< 提交（C→S 闭合点）
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00B3DF80  call    sub_B02FF0
  00B3DF85  mov     edx, [esp+40h+arg_0]
  00B3DF89  push    edx
  00B3DF8A  push    offset aCommanderId_0
  00B3DF8F  push    edi
  00B3DF90  call    sub_41D990
  00B3DF95  add     esp, 8
  00B3DF98  mov     ecx, eax
  00B3DF9A  call    sub_B03580
  00B3DF9F  push    offset aByte
  00B3DFA4  mov     eax, ebx
  00B3DFA6  sub     eax, ebp
  00B3DFA8  push    eax
  00B3DFA9  push    offset asc_EDAD58
  00B3DFAE  push    edi
  00B3DFAF  call    sub_41D990
  00B3DFB4  add     esp, 8
  00B3DFB7  mov     ecx, eax
  00B3DFB9  call    sub_B03580
  00B3DFBE  push    eax
  00B3DFBF  call    sub_41D990
  00B3DFC4  add     esp, 8
  00B3DFC7  mov     edi, eax
  00B3DFC9  push    0Ah
  00B3DFCB  mov     ecx, edi
  00B3DFCD  call    sub_B036E0
  00B3DFD2  mov     ecx, edi
  00B3DFD4  call    sub_40DDF0
  00B3DFD9  mov     edx, [esi]
  00B3DFDB  mov     eax, [edx+58h]
```

## 4. 发送去向切片

```asm
  00B3DFD9  mov     edx, [esi]
  00B3DFDB  mov     eax, [edx+58h]
  00B3DFDE  sub     ebx, ebp
  00B3DFE0  push    ebx
  00B3DFE1  push    ebp
  00B3DFE2  mov     ecx, esi
  00B3DFE4  call    eax
  00B3DFE6  test    al, al
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `00B3DF14` | u16 / 2 |
| `commander_id` | `0xB3DF24` | u32 / 4 |
