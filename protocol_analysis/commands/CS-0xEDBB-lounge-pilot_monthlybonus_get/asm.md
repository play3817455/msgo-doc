# 汇编证据 —— CS-0xEDBB-lounge-pilot_monthlybonus_get

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0x00B8F1B0`（`0x00B8F1B0`..`0x00B8F333`），函数 `sub_B8F1B0`
- 命令名字符串：`)<-_proto_lounge_client::send_pilot_monthlybonus_get(` @ `0x00EEACA8`
- opcode 写入：`0x00B8F209`
- 声明容量：`0x2`（分配器容量 `push` @ `0x00B8F1F6`）
- 提交（`sub_B02FF0`）：`0x00B8F273`
- 发送去向：`vt[0x58]` @ `0x00B8F2B4`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00B8F1FF  push    eax
  00B8F200  lea     ecx, [esp+44h+var_2C]
  00B8F204  call    sub_ABB2F0   ; <<< 初始化 {cur,end}（游标自 buf+2 起）
  00B8F209  mov     word ptr [edi], 0EDBBh   ; <<< 内联写线（u16）
  00B8F20E  mov     ebp, [esi+7BA8h]
  00B8F214  test    ebp, ebp
  00B8F216  mov     [esp+40h+var_4], 0
  00B8F21E  lea     ebx, [edi+2]
  00B8F221  jz      loc_B8F2B2
  00B8F227  lea     ecx, [esp+40h+var_28]
  00B8F22B  push    ecx
  00B8F22C  call    sub_CA0CE0
  00B8F231  add     esp, 4
  00B8F234  mov     edx, [esi+8]
  00B8F237  push    offset aProtoLoungeCli_518
  00B8F23C  push    edx
  00B8F23D  push    offset aId
  00B8F242  push    eax
  00B8F243  push    ebp
  00B8F244  mov     byte ptr [esp+54h+var_4], 1
  00B8F249  call    sub_B03020
  00B8F24E  add     esp, 8
  00B8F251  push    eax
  00B8F252  call    sub_41D990
  00B8F257  add     esp, 8
  00B8F25A  mov     ecx, eax
  00B8F25C  call    sub_ADC810
  00B8F261  push    eax
  00B8F262  call    sub_41D990
  00B8F267  add     esp, 8
  00B8F26A  lea     ecx, [esp+40h+var_28]
  00B8F26E  mov     byte ptr [esp+40h+var_4], 0
  00B8F273  call    sub_B02FF0   ; <<< 提交（C→S 闭合点）
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00B8F273  call    sub_B02FF0
  00B8F278  push    offset aByte
  00B8F27D  mov     eax, ebx
  00B8F27F  sub     eax, edi
  00B8F281  push    eax
  00B8F282  push    offset asc_EDAD58
  00B8F287  push    ebp
  00B8F288  call    sub_41D990
  00B8F28D  add     esp, 8
  00B8F290  mov     ecx, eax
  00B8F292  call    sub_B03580
  00B8F297  push    eax
  00B8F298  call    sub_41D990
  00B8F29D  add     esp, 8
  00B8F2A0  mov     ebp, eax
  00B8F2A2  push    0Ah
  00B8F2A4  mov     ecx, ebp
  00B8F2A6  call    sub_B036E0
  00B8F2AB  mov     ecx, ebp
  00B8F2AD  call    sub_40DDF0
  00B8F2B2  mov     edx, [esi]
  00B8F2B4  mov     eax, [edx+58h]
```

## 4. 发送去向切片

```asm
  00B8F2B2  mov     edx, [esi]
  00B8F2B4  mov     eax, [edx+58h]
  00B8F2B7  sub     ebx, edi
  00B8F2B9  push    ebx
  00B8F2BA  push    edi
  00B8F2BB  mov     ecx, esi
  00B8F2BD  call    eax
  00B8F2BF  test    al, al
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `00B8F209` | u16 / 2 |
