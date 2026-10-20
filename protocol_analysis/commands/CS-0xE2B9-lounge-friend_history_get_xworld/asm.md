# 汇编证据 —— CS-0xE2B9-lounge-friend_history_get_xworld

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0x00B9AE00`（`0x00B9AE00`..`0x00B9AF86`），函数 `sub_B9AE00`
- 命令名字符串：`)<-_proto_lounge_client::send_friend_history_get_xworld(` @ `0x00EEC04C`
- opcode 写入：`0x00B9AE59`
- 声明容量：`0x2`（分配器容量 `push` @ `0x00B9AE46`）
- 提交（`sub_B02FF0`）：`0x00B9AEC3`
- 发送去向：`vt[0x58]` @ `0x00B9AF04`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00B9AE4F  push    eax
  00B9AE50  lea     ecx, [esp+44h+var_2C]
  00B9AE54  call    sub_ABB2F0   ; <<< 初始化 {cur,end}（游标自 buf+2 起）
  00B9AE59  mov     word ptr [edi], 0E2B9h   ; <<< 内联写线（u16）
  00B9AE5E  mov     ebp, [esi+7F10h]
  00B9AE64  test    ebp, ebp
  00B9AE66  mov     [esp+40h+var_4], 0
  00B9AE6E  lea     ebx, [edi+2]
  00B9AE71  jz      loc_B9AF02
  00B9AE77  lea     ecx, [esp+40h+var_28]
  00B9AE7B  push    ecx
  00B9AE7C  call    sub_CA0CE0
  00B9AE81  add     esp, 4
  00B9AE84  mov     edx, [esi+8]
  00B9AE87  push    offset aProtoLoungeCli_368
  00B9AE8C  push    edx
  00B9AE8D  push    offset aId
  00B9AE92  push    eax
  00B9AE93  push    ebp
  00B9AE94  mov     byte ptr [esp+54h+var_4], 1
  00B9AE99  call    sub_B03020
  00B9AE9E  add     esp, 8
  00B9AEA1  push    eax
  00B9AEA2  call    sub_41D990
  00B9AEA7  add     esp, 8
  00B9AEAA  mov     ecx, eax
  00B9AEAC  call    sub_ADC810
  00B9AEB1  push    eax
  00B9AEB2  call    sub_41D990
  00B9AEB7  add     esp, 8
  00B9AEBA  lea     ecx, [esp+40h+var_28]
  00B9AEBE  mov     byte ptr [esp+40h+var_4], 0
  00B9AEC3  call    sub_B02FF0   ; <<< 提交（C→S 闭合点）
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00B9AEC3  call    sub_B02FF0
  00B9AEC8  push    offset aByte
  00B9AECD  mov     eax, ebx
  00B9AECF  sub     eax, edi
  00B9AED1  push    eax
  00B9AED2  push    offset asc_EDAD58
  00B9AED7  push    ebp
  00B9AED8  call    sub_41D990
  00B9AEDD  add     esp, 8
  00B9AEE0  mov     ecx, eax
  00B9AEE2  call    sub_B03580
  00B9AEE7  push    eax
  00B9AEE8  call    sub_41D990
  00B9AEED  add     esp, 8
  00B9AEF0  mov     ebp, eax
  00B9AEF2  push    0Ah
  00B9AEF4  mov     ecx, ebp
  00B9AEF6  call    sub_B036E0
  00B9AEFB  mov     ecx, ebp
  00B9AEFD  call    sub_40DDF0
  00B9AF02  mov     edx, [esi]
  00B9AF04  mov     eax, [edx+58h]
```

## 4. 发送去向切片

```asm
  00B9AF02  mov     edx, [esi]
  00B9AF04  mov     eax, [edx+58h]
  00B9AF07  sub     ebx, edi
  00B9AF09  push    ebx
  00B9AF0A  push    edi
  00B9AF0B  mov     ecx, esi
  00B9AF0D  call    eax
  00B9AF0F  test    al, al
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `00B9AE59` | u16 / 2 |
