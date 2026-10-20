# 汇编证据 —— CS-0xE041-battle-msma_spawn_list_get

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0x00B33DA0`（`0x00B33DA0`..`0x00B33F23`），函数 `sub_B33DA0`
- 命令名字符串：`)<-_proto_battle_client::send_msma_spawn_list_get(` @ `0x00EE098C`
- opcode 写入：`0x00B33DF9`
- 声明容量：`0x2`（分配器容量 `push` @ `0x00B33DE6`）
- 提交（`sub_B02FF0`）：`0x00B33E63`
- 发送去向：`vt[0x58]` @ `0x00B33EA4`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00B33DEF  push    eax
  00B33DF0  lea     ecx, [esp+44h+var_2C]
  00B33DF4  call    sub_ABB2F0   ; <<< 初始化 {cur,end}（游标自 buf+2 起）
  00B33DF9  mov     word ptr [edi], 0E041h   ; <<< 内联写线（u16）
  00B33DFE  mov     ebp, [esi+3D10h]
  00B33E04  test    ebp, ebp
  00B33E06  mov     [esp+40h+var_4], 0
  00B33E0E  lea     ebx, [edi+2]
  00B33E11  jz      loc_B33EA2
  00B33E17  lea     ecx, [esp+40h+var_28]
  00B33E1B  push    ecx
  00B33E1C  call    sub_CA0CE0
  00B33E21  add     esp, 4
  00B33E24  mov     edx, [esi+8]
  00B33E27  push    offset aProtoBattleCli_220
  00B33E2C  push    edx
  00B33E2D  push    offset aId
  00B33E32  push    eax
  00B33E33  push    ebp
  00B33E34  mov     byte ptr [esp+54h+var_4], 1
  00B33E39  call    sub_B03020
  00B33E3E  add     esp, 8
  00B33E41  push    eax
  00B33E42  call    sub_41D990
  00B33E47  add     esp, 8
  00B33E4A  mov     ecx, eax
  00B33E4C  call    sub_ADC810
  00B33E51  push    eax
  00B33E52  call    sub_41D990
  00B33E57  add     esp, 8
  00B33E5A  lea     ecx, [esp+40h+var_28]
  00B33E5E  mov     byte ptr [esp+40h+var_4], 0
  00B33E63  call    sub_B02FF0   ; <<< 提交（C→S 闭合点）
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00B33E63  call    sub_B02FF0
  00B33E68  push    offset aByte
  00B33E6D  mov     eax, ebx
  00B33E6F  sub     eax, edi
  00B33E71  push    eax
  00B33E72  push    offset asc_EDAD58
  00B33E77  push    ebp
  00B33E78  call    sub_41D990
  00B33E7D  add     esp, 8
  00B33E80  mov     ecx, eax
  00B33E82  call    sub_B03580
  00B33E87  push    eax
  00B33E88  call    sub_41D990
  00B33E8D  add     esp, 8
  00B33E90  mov     ebp, eax
  00B33E92  push    0Ah
  00B33E94  mov     ecx, ebp
  00B33E96  call    sub_B036E0
  00B33E9B  mov     ecx, ebp
  00B33E9D  call    sub_40DDF0
  00B33EA2  mov     edx, [esi]
  00B33EA4  mov     eax, [edx+58h]
```

## 4. 发送去向切片

```asm
  00B33EA2  mov     edx, [esi]
  00B33EA4  mov     eax, [edx+58h]
  00B33EA7  sub     ebx, edi
  00B33EA9  push    ebx
  00B33EAA  push    edi
  00B33EAB  mov     ecx, esi
  00B33EAD  call    eax
  00B33EAF  test    al, al
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `00B33DF9` | u16 / 2 |
