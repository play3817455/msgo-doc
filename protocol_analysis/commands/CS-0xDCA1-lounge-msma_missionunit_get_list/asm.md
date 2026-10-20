# 汇编证据 —— CS-0xDCA1-lounge-msma_missionunit_get_list

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0x00B996C0`（`0x00B996C0`..`0x00B99846`），函数 `sub_B996C0`
- 命令名字符串：`)<-_proto_lounge_client::send_msma_missionunit_get_list(` @ `0x00EEBD88`
- opcode 写入：`0x00B99719`
- 声明容量：`0x2`（分配器容量 `push` @ `0x00B99706`）
- 提交（`sub_B02FF0`）：`0x00B99783`
- 发送去向：`vt[0x58]` @ `0x00B997C4`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00B9970F  push    eax
  00B99710  lea     ecx, [esp+44h+var_2C]
  00B99714  call    sub_ABB2F0   ; <<< 初始化 {cur,end}（游标自 buf+2 起）
  00B99719  mov     word ptr [edi], 0DCA1h   ; <<< 内联写线（u16）
  00B9971E  mov     ebp, [esi+7E8Ch]
  00B99724  test    ebp, ebp
  00B99726  mov     [esp+40h+var_4], 0
  00B9972E  lea     ebx, [edi+2]
  00B99731  jz      loc_B997C2
  00B99737  lea     ecx, [esp+40h+var_28]
  00B9973B  push    ecx
  00B9973C  call    sub_CA0CE0
  00B99741  add     esp, 4
  00B99744  mov     edx, [esi+8]
  00B99747  push    offset aProtoLoungeCli_395
  00B9974C  push    edx
  00B9974D  push    offset aId
  00B99752  push    eax
  00B99753  push    ebp
  00B99754  mov     byte ptr [esp+54h+var_4], 1
  00B99759  call    sub_B03020
  00B9975E  add     esp, 8
  00B99761  push    eax
  00B99762  call    sub_41D990
  00B99767  add     esp, 8
  00B9976A  mov     ecx, eax
  00B9976C  call    sub_ADC810
  00B99771  push    eax
  00B99772  call    sub_41D990
  00B99777  add     esp, 8
  00B9977A  lea     ecx, [esp+40h+var_28]
  00B9977E  mov     byte ptr [esp+40h+var_4], 0
  00B99783  call    sub_B02FF0   ; <<< 提交（C→S 闭合点）
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00B99783  call    sub_B02FF0
  00B99788  push    offset aByte
  00B9978D  mov     eax, ebx
  00B9978F  sub     eax, edi
  00B99791  push    eax
  00B99792  push    offset asc_EDAD58
  00B99797  push    ebp
  00B99798  call    sub_41D990
  00B9979D  add     esp, 8
  00B997A0  mov     ecx, eax
  00B997A2  call    sub_B03580
  00B997A7  push    eax
  00B997A8  call    sub_41D990
  00B997AD  add     esp, 8
  00B997B0  mov     ebp, eax
  00B997B2  push    0Ah
  00B997B4  mov     ecx, ebp
  00B997B6  call    sub_B036E0
  00B997BB  mov     ecx, ebp
  00B997BD  call    sub_40DDF0
  00B997C2  mov     edx, [esi]
  00B997C4  mov     eax, [edx+58h]
```

## 4. 发送去向切片

```asm
  00B997C2  mov     edx, [esi]
  00B997C4  mov     eax, [edx+58h]
  00B997C7  sub     ebx, edi
  00B997C9  push    ebx
  00B997CA  push    edi
  00B997CB  mov     ecx, esi
  00B997CD  call    eax
  00B997CF  test    al, al
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `00B99719` | u16 / 2 |
