# 汇编证据 —— CS-0xF741-battle-roomlobby_game_start

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0x00B32330`（`0x00B32330`..`0x00B324B0`），函数 `sub_B32330`
- 命令名字符串：`)<-_proto_battle_client::send_roomlobby_game_start(` @ `0x00EE065C`
- opcode 写入：`0x00B32386`
- 声明容量：`0x2`（分配器容量 `push` @ `0x00B32373`）
- 提交（`sub_B02FF0`）：`0x00B323F0`
- 发送去向：`vt[0x58]` @ `0x00B32431`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00B3237C  push    eax
  00B3237D  lea     ecx, [esp+44h+var_2C]
  00B32381  call    sub_ABB2F0   ; <<< 初始化 {cur,end}（游标自 buf+2 起）
  00B32386  mov     word ptr [edi], 0F741h   ; <<< 内联写线（u16）
  00B3238B  mov     ebp, [esi+3C48h]
  00B32391  test    ebp, ebp
  00B32393  mov     [esp+40h+var_4], 0
  00B3239B  lea     ebx, [edi+2]
  00B3239E  jz      loc_B3242F
  00B323A4  lea     ecx, [esp+40h+var_28]
  00B323A8  push    ecx
  00B323A9  call    sub_CA0CE0
  00B323AE  add     esp, 4
  00B323B1  mov     edx, [esi+8]
  00B323B4  push    offset aProtoBattleCli_218
  00B323B9  push    edx
  00B323BA  push    offset aId
  00B323BF  push    eax
  00B323C0  push    ebp
  00B323C1  mov     byte ptr [esp+54h+var_4], 1
  00B323C6  call    sub_B03020
  00B323CB  add     esp, 8
  00B323CE  push    eax
  00B323CF  call    sub_41D990
  00B323D4  add     esp, 8
  00B323D7  mov     ecx, eax
  00B323D9  call    sub_ADC810
  00B323DE  push    eax
  00B323DF  call    sub_41D990
  00B323E4  add     esp, 8
  00B323E7  lea     ecx, [esp+40h+var_28]
  00B323EB  mov     byte ptr [esp+40h+var_4], 0
  00B323F0  call    sub_B02FF0   ; <<< 提交（C→S 闭合点）
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00B323F0  call    sub_B02FF0
  00B323F5  push    offset aByte
  00B323FA  mov     eax, ebx
  00B323FC  sub     eax, edi
  00B323FE  push    eax
  00B323FF  push    offset asc_EDAD58
  00B32404  push    ebp
  00B32405  call    sub_41D990
  00B3240A  add     esp, 8
  00B3240D  mov     ecx, eax
  00B3240F  call    sub_B03580
  00B32414  push    eax
  00B32415  call    sub_41D990
  00B3241A  add     esp, 8
  00B3241D  mov     ebp, eax
  00B3241F  push    0Ah
  00B32421  mov     ecx, ebp
  00B32423  call    sub_B036E0
  00B32428  mov     ecx, ebp
  00B3242A  call    sub_40DDF0
  00B3242F  mov     edx, [esi]
  00B32431  mov     eax, [edx+58h]
```

## 4. 发送去向切片

```asm
  00B3242F  mov     edx, [esi]
  00B32431  mov     eax, [edx+58h]
  00B32434  sub     ebx, edi
  00B32436  push    ebx
  00B32437  push    edi
  00B32438  mov     ecx, esi
  00B3243A  call    eax
  00B3243C  test    al, al
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `00B32386` | u16 / 2 |
