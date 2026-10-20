# 汇编证据 —— CS-0xE4B8-lounge-you9_cps_HDB_response

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0x00BA5130`（`0x00BA5130`..`0x00BA52DD`），函数 `sub_BA5130`
- 命令名字符串：`)<-_proto_lounge_client::send_you9_cps_HDB_response(` @ `0x00EED0C0`
- opcode 写入：`0x00BA51A4`
- 声明容量：`0x6`（分配器容量 `push` @ `0x00BA5176`）
- 提交（`sub_B02FF0`）：`0x00BA5210`
- 发送去向：`vt[0x58]` @ `0x00BA526B`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00BA517F  push    eax
  00BA5180  lea     ecx, [esp+44h+var_2C]
  00BA5184  call    sub_ABB2F0   ; <<< 初始化 {cur,end}（游标自 buf+2 起）
  00BA5189  lea     ecx, [ebp+6]
  00BA518C  lea     eax, [ebp+2]
  00BA518F  cmp     eax, ecx
  00BA5191  mov     [esp+40h+var_4], 0
  00BA5199  ja      loc_BA52C8
  00BA519F  lea     ebx, [eax+4]
  00BA51A2  cmp     ebx, ecx
  00BA51A4  mov     word ptr [ebp+0], 0E4B8h   ; <<< 内联写线（u16）
  00BA51AA  ja      loc_BA52C8
  00BA51B0  mov     ecx, [esp+40h+arg_0]
  00BA51B4  mov     [eax], ecx   ; <<< 内联写线（u32）
  00BA51B6  mov     edi, [esi+8218h]
  00BA51BC  test    edi, edi
  00BA51BE  jz      loc_BA5269
  00BA51C4  lea     edx, [esp+40h+var_28]
  00BA51C8  push    edx
  00BA51C9  call    sub_CA0CE0
  00BA51CE  add     esp, 4
  00BA51D1  mov     ecx, [esi+8]
  00BA51D4  push    offset aProtoLoungeCli_594
  00BA51D9  push    ecx
  00BA51DA  push    offset aId
  00BA51DF  push    eax
  00BA51E0  push    edi
  00BA51E1  mov     byte ptr [esp+54h+var_4], 1
  00BA51E6  call    sub_B03020
  00BA51EB  add     esp, 8
  00BA51EE  push    eax
  00BA51EF  call    sub_41D990
  00BA51F4  add     esp, 8
  00BA51F7  mov     ecx, eax
  00BA51F9  call    sub_ADC810
  00BA51FE  push    eax
  00BA51FF  call    sub_41D990
  00BA5204  add     esp, 8
  00BA5207  lea     ecx, [esp+40h+var_28]
  00BA520B  mov     byte ptr [esp+40h+var_4], 0
  00BA5210  call    sub_B02FF0   ; <<< 提交（C→S 闭合点）
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00BA5210  call    sub_B02FF0
  00BA5215  mov     edx, [esp+40h+arg_0]
  00BA5219  push    edx
  00BA521A  push    offset aCpsResult
  00BA521F  push    edi
  00BA5220  call    sub_41D990
  00BA5225  add     esp, 8
  00BA5228  mov     ecx, eax
  00BA522A  call    sub_B03580
  00BA522F  push    offset aByte
  00BA5234  mov     eax, ebx
  00BA5236  sub     eax, ebp
  00BA5238  push    eax
  00BA5239  push    offset asc_EDAD58
  00BA523E  push    edi
  00BA523F  call    sub_41D990
  00BA5244  add     esp, 8
  00BA5247  mov     ecx, eax
  00BA5249  call    sub_B03580
  00BA524E  push    eax
  00BA524F  call    sub_41D990
  00BA5254  add     esp, 8
  00BA5257  mov     edi, eax
  00BA5259  push    0Ah
  00BA525B  mov     ecx, edi
  00BA525D  call    sub_B036E0
  00BA5262  mov     ecx, edi
  00BA5264  call    sub_40DDF0
  00BA5269  mov     edx, [esi]
  00BA526B  mov     eax, [edx+58h]
```

## 4. 发送去向切片

```asm
  00BA5269  mov     edx, [esi]
  00BA526B  mov     eax, [edx+58h]
  00BA526E  sub     ebx, ebp
  00BA5270  push    ebx
  00BA5271  push    ebp
  00BA5272  mov     ecx, esi
  00BA5274  call    eax
  00BA5276  test    al, al
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `00BA51A4` | u16 / 2 |
| `cps_result` | `0xBA51B4` | u32 / 4 |
