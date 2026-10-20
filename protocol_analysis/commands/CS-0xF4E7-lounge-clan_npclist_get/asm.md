# 汇编证据 —— CS-0xF4E7-lounge-clan_npclist_get

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0x00B9F6A0`（`0x00B9F6A0`..`0x00B9F826`），函数 `sub_B9F6A0`
- 命令名字符串：`)<-_proto_lounge_client::send_clan_npclist_get(` @ `0x00EEC760`
- opcode 写入：`0x00B9F6F9`
- 声明容量：`0x2`（分配器容量 `push` @ `0x00B9F6E6`）
- 提交（`sub_B02FF0`）：`0x00B9F763`
- 发送去向：`vt[0x58]` @ `0x00B9F7A4`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00B9F6EF  push    eax
  00B9F6F0  lea     ecx, [esp+44h+var_2C]
  00B9F6F4  call    sub_ABB2F0   ; <<< 初始化 {cur,end}（游标自 buf+2 起）
  00B9F6F9  mov     word ptr [edi], 0F4E7h   ; <<< 内联写线（u16）
  00B9F6FE  mov     ebp, [esi+8060h]
  00B9F704  test    ebp, ebp
  00B9F706  mov     [esp+40h+var_4], 0
  00B9F70E  lea     ebx, [edi+2]
  00B9F711  jz      loc_B9F7A2
  00B9F717  lea     ecx, [esp+40h+var_28]
  00B9F71B  push    ecx
  00B9F71C  call    sub_CA0CE0
  00B9F721  add     esp, 4
  00B9F724  mov     edx, [esi+8]
  00B9F727  push    offset aProtoLoungeCli_475
  00B9F72C  push    edx
  00B9F72D  push    offset aId
  00B9F732  push    eax
  00B9F733  push    ebp
  00B9F734  mov     byte ptr [esp+54h+var_4], 1
  00B9F739  call    sub_B03020
  00B9F73E  add     esp, 8
  00B9F741  push    eax
  00B9F742  call    sub_41D990
  00B9F747  add     esp, 8
  00B9F74A  mov     ecx, eax
  00B9F74C  call    sub_ADC810
  00B9F751  push    eax
  00B9F752  call    sub_41D990
  00B9F757  add     esp, 8
  00B9F75A  lea     ecx, [esp+40h+var_28]
  00B9F75E  mov     byte ptr [esp+40h+var_4], 0
  00B9F763  call    sub_B02FF0   ; <<< 提交（C→S 闭合点）
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00B9F763  call    sub_B02FF0
  00B9F768  push    offset aByte
  00B9F76D  mov     eax, ebx
  00B9F76F  sub     eax, edi
  00B9F771  push    eax
  00B9F772  push    offset asc_EDAD58
  00B9F777  push    ebp
  00B9F778  call    sub_41D990
  00B9F77D  add     esp, 8
  00B9F780  mov     ecx, eax
  00B9F782  call    sub_B03580
  00B9F787  push    eax
  00B9F788  call    sub_41D990
  00B9F78D  add     esp, 8
  00B9F790  mov     ebp, eax
  00B9F792  push    0Ah
  00B9F794  mov     ecx, ebp
  00B9F796  call    sub_B036E0
  00B9F79B  mov     ecx, ebp
  00B9F79D  call    sub_40DDF0
  00B9F7A2  mov     edx, [esi]
  00B9F7A4  mov     eax, [edx+58h]
```

## 4. 发送去向切片

```asm
  00B9F7A2  mov     edx, [esi]
  00B9F7A4  mov     eax, [edx+58h]
  00B9F7A7  sub     ebx, edi
  00B9F7A9  push    ebx
  00B9F7AA  push    edi
  00B9F7AB  mov     ecx, esi
  00B9F7AD  call    eax
  00B9F7AF  test    al, al
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `00B9F6F9` | u16 / 2 |
