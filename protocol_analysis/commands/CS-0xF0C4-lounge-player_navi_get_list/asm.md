# 汇编证据 —— CS-0xF0C4-lounge-player_navi_get_list

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0x00BA7240`（`0x00BA7240`..`0x00BA73C6`），函数 `sub_BA7240`
- 命令名字符串：`)<-_proto_lounge_client::send_player_navi_get_list(` @ `0x00EED428`
- opcode 写入：`0x00BA7299`
- 声明容量：`0x2`（分配器容量 `push` @ `0x00BA7286`）
- 提交（`sub_B02FF0`）：`0x00BA7303`
- 发送去向：`vt[0x58]` @ `0x00BA7344`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00BA728F  push    eax
  00BA7290  lea     ecx, [esp+44h+var_2C]
  00BA7294  call    sub_ABB2F0   ; <<< 初始化 {cur,end}（游标自 buf+2 起）
  00BA7299  mov     word ptr [edi], 0F0C4h   ; <<< 内联写线（u16）
  00BA729E  mov     ebp, [esi+82C8h]
  00BA72A4  test    ebp, ebp
  00BA72A6  mov     [esp+40h+var_4], 0
  00BA72AE  lea     ebx, [edi+2]
  00BA72B1  jz      loc_BA7342
  00BA72B7  lea     ecx, [esp+40h+var_28]
  00BA72BB  push    ecx
  00BA72BC  call    sub_CA0CE0
  00BA72C1  add     esp, 4
  00BA72C4  mov     edx, [esi+8]
  00BA72C7  push    offset aProtoLoungeCli_398
  00BA72CC  push    edx
  00BA72CD  push    offset aId
  00BA72D2  push    eax
  00BA72D3  push    ebp
  00BA72D4  mov     byte ptr [esp+54h+var_4], 1
  00BA72D9  call    sub_B03020
  00BA72DE  add     esp, 8
  00BA72E1  push    eax
  00BA72E2  call    sub_41D990
  00BA72E7  add     esp, 8
  00BA72EA  mov     ecx, eax
  00BA72EC  call    sub_ADC810
  00BA72F1  push    eax
  00BA72F2  call    sub_41D990
  00BA72F7  add     esp, 8
  00BA72FA  lea     ecx, [esp+40h+var_28]
  00BA72FE  mov     byte ptr [esp+40h+var_4], 0
  00BA7303  call    sub_B02FF0   ; <<< 提交（C→S 闭合点）
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00BA7303  call    sub_B02FF0
  00BA7308  push    offset aByte
  00BA730D  mov     eax, ebx
  00BA730F  sub     eax, edi
  00BA7311  push    eax
  00BA7312  push    offset asc_EDAD58
  00BA7317  push    ebp
  00BA7318  call    sub_41D990
  00BA731D  add     esp, 8
  00BA7320  mov     ecx, eax
  00BA7322  call    sub_B03580
  00BA7327  push    eax
  00BA7328  call    sub_41D990
  00BA732D  add     esp, 8
  00BA7330  mov     ebp, eax
  00BA7332  push    0Ah
  00BA7334  mov     ecx, ebp
  00BA7336  call    sub_B036E0
  00BA733B  mov     ecx, ebp
  00BA733D  call    sub_40DDF0
  00BA7342  mov     edx, [esi]
  00BA7344  mov     eax, [edx+58h]
```

## 4. 发送去向切片

```asm
  00BA7342  mov     edx, [esi]
  00BA7344  mov     eax, [edx+58h]
  00BA7347  sub     ebx, edi
  00BA7349  push    ebx
  00BA734A  push    edi
  00BA734B  mov     ecx, esi
  00BA734D  call    eax
  00BA734F  test    al, al
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `00BA7299` | u16 / 2 |
