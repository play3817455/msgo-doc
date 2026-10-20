# 汇编证据 —— CS-0xEDD6-battle-daily_record_progress

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0x00B40200`（`0x00B40200`..`0x00B40386`），函数 `sub_B40200`
- 命令名字符串：`)<-_proto_battle_client::send_daily_record_progress(` @ `0x00EE17DC`
- opcode 写入：`0x00B40259`
- 声明容量：`0x2`（分配器容量 `push` @ `0x00B40246`）
- 提交（`sub_B02FF0`）：`0x00B402C3`
- 发送去向：`vt[0x58]` @ `0x00B40304`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00B4024F  push    eax
  00B40250  lea     ecx, [esp+44h+var_2C]
  00B40254  call    sub_ABB2F0   ; <<< 初始化 {cur,end}（游标自 buf+2 起）
  00B40259  mov     word ptr [edi], 0EDD6h   ; <<< 内联写线（u16）
  00B4025E  mov     ebp, [esi+4038h]
  00B40264  test    ebp, ebp
  00B40266  mov     [esp+40h+var_4], 0
  00B4026E  lea     ebx, [edi+2]
  00B40271  jz      loc_B40302
  00B40277  lea     ecx, [esp+40h+var_28]
  00B4027B  push    ecx
  00B4027C  call    sub_CA0CE0
  00B40281  add     esp, 4
  00B40284  mov     edx, [esi+8]
  00B40287  push    offset aProtoBattleCli_284
  00B4028C  push    edx
  00B4028D  push    offset aId
  00B40292  push    eax
  00B40293  push    ebp
  00B40294  mov     byte ptr [esp+54h+var_4], 1
  00B40299  call    sub_B03020
  00B4029E  add     esp, 8
  00B402A1  push    eax
  00B402A2  call    sub_41D990
  00B402A7  add     esp, 8
  00B402AA  mov     ecx, eax
  00B402AC  call    sub_ADC810
  00B402B1  push    eax
  00B402B2  call    sub_41D990
  00B402B7  add     esp, 8
  00B402BA  lea     ecx, [esp+40h+var_28]
  00B402BE  mov     byte ptr [esp+40h+var_4], 0
  00B402C3  call    sub_B02FF0   ; <<< 提交（C→S 闭合点）
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00B402C3  call    sub_B02FF0
  00B402C8  push    offset aByte
  00B402CD  mov     eax, ebx
  00B402CF  sub     eax, edi
  00B402D1  push    eax
  00B402D2  push    offset asc_EDAD58
  00B402D7  push    ebp
  00B402D8  call    sub_41D990
  00B402DD  add     esp, 8
  00B402E0  mov     ecx, eax
  00B402E2  call    sub_B03580
  00B402E7  push    eax
  00B402E8  call    sub_41D990
  00B402ED  add     esp, 8
  00B402F0  mov     ebp, eax
  00B402F2  push    0Ah
  00B402F4  mov     ecx, ebp
  00B402F6  call    sub_B036E0
  00B402FB  mov     ecx, ebp
  00B402FD  call    sub_40DDF0
  00B40302  mov     edx, [esi]
  00B40304  mov     eax, [edx+58h]
```

## 4. 发送去向切片

```asm
  00B40302  mov     edx, [esi]
  00B40304  mov     eax, [edx+58h]
  00B40307  sub     ebx, edi
  00B40309  push    ebx
  00B4030A  push    edi
  00B4030B  mov     ecx, esi
  00B4030D  call    eax
  00B4030F  test    al, al
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `00B40259` | u16 / 2 |
