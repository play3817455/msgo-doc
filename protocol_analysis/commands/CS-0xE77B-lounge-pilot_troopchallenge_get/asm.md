# 汇编证据 —— CS-0xE77B-lounge-pilot_troopchallenge_get

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0x00B8EE90`（`0x00B8EE90`..`0x00B8F013`），函数 `sub_B8EE90`
- 命令名字符串：`)<-_proto_lounge_client::send_pilot_troopchallenge_get(` @ `0x00EEAC30`
- opcode 写入：`0x00B8EEE9`
- 声明容量：`0x2`（分配器容量 `push` @ `0x00B8EED6`）
- 提交（`sub_B02FF0`）：`0x00B8EF53`
- 发送去向：`vt[0x58]` @ `0x00B8EF94`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00B8EEDF  push    eax
  00B8EEE0  lea     ecx, [esp+44h+var_2C]
  00B8EEE4  call    sub_ABB2F0   ; <<< 初始化 {cur,end}（游标自 buf+2 起）
  00B8EEE9  mov     word ptr [edi], 0E77Bh   ; <<< 内联写线（u16）
  00B8EEEE  mov     ebp, [esi+7B8Ch]
  00B8EEF4  test    ebp, ebp
  00B8EEF6  mov     [esp+40h+var_4], 0
  00B8EEFE  lea     ebx, [edi+2]
  00B8EF01  jz      loc_B8EF92
  00B8EF07  lea     ecx, [esp+40h+var_28]
  00B8EF0B  push    ecx
  00B8EF0C  call    sub_CA0CE0
  00B8EF11  add     esp, 4
  00B8EF14  mov     edx, [esi+8]
  00B8EF17  push    offset aProtoLoungeCli_525
  00B8EF1C  push    edx
  00B8EF1D  push    offset aId
  00B8EF22  push    eax
  00B8EF23  push    ebp
  00B8EF24  mov     byte ptr [esp+54h+var_4], 1
  00B8EF29  call    sub_B03020
  00B8EF2E  add     esp, 8
  00B8EF31  push    eax
  00B8EF32  call    sub_41D990
  00B8EF37  add     esp, 8
  00B8EF3A  mov     ecx, eax
  00B8EF3C  call    sub_ADC810
  00B8EF41  push    eax
  00B8EF42  call    sub_41D990
  00B8EF47  add     esp, 8
  00B8EF4A  lea     ecx, [esp+40h+var_28]
  00B8EF4E  mov     byte ptr [esp+40h+var_4], 0
  00B8EF53  call    sub_B02FF0   ; <<< 提交（C→S 闭合点）
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00B8EF53  call    sub_B02FF0
  00B8EF58  push    offset aByte
  00B8EF5D  mov     eax, ebx
  00B8EF5F  sub     eax, edi
  00B8EF61  push    eax
  00B8EF62  push    offset asc_EDAD58
  00B8EF67  push    ebp
  00B8EF68  call    sub_41D990
  00B8EF6D  add     esp, 8
  00B8EF70  mov     ecx, eax
  00B8EF72  call    sub_B03580
  00B8EF77  push    eax
  00B8EF78  call    sub_41D990
  00B8EF7D  add     esp, 8
  00B8EF80  mov     ebp, eax
  00B8EF82  push    0Ah
  00B8EF84  mov     ecx, ebp
  00B8EF86  call    sub_B036E0
  00B8EF8B  mov     ecx, ebp
  00B8EF8D  call    sub_40DDF0
  00B8EF92  mov     edx, [esi]
  00B8EF94  mov     eax, [edx+58h]
```

## 4. 发送去向切片

```asm
  00B8EF92  mov     edx, [esi]
  00B8EF94  mov     eax, [edx+58h]
  00B8EF97  sub     ebx, edi
  00B8EF99  push    ebx
  00B8EF9A  push    edi
  00B8EF9B  mov     ecx, esi
  00B8EF9D  call    eax
  00B8EF9F  test    al, al
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `00B8EEE9` | u16 / 2 |
