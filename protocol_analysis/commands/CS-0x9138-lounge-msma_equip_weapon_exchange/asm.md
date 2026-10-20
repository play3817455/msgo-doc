# 汇编证据 —— CS-0x9138-lounge-msma_equip_weapon_exchange

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B93600 @ `0xb93600`（`0xb93600`..`0xb93846`）
- 命令名字符串：`)<-_proto_lounge_client::send_msma_equip_weapon_exchange(` @ `0xeeb3c4`
- opcode 写入：`0xb9367c`
- 声明容量：`0x12`（分配器容量 `push` @ `0xb93646`）

## 2. 组包块切片（游标初始化 → 逐字段写线 → 提交）

```asm
  0xb9364a  mov     ebp, eax
  0xb9364c  mov     eax, [edi+0Ch]
  0xb9364f  push    eax
  0xb93650  lea     ecx, [esp+4Ch+var_34]
  0xb93654  call    sub_ABB2F0
  0xb93659  lea     ecx, [ebp+12h]
  0xb9365c  lea     eax, [ebp+2]
  0xb9365f  cmp     eax, ecx
  0xb93661  mov     [esp+48h+var_4], 0
  0xb93669  mov     [esp+48h+var_30], ebp
  0xb9366d  mov     dword ptr [esp+48h+var_2C], ecx
  0xb93671  ja      loc_B93831
  0xb93677  lea     edx, [eax+8]
  0xb9367a  cmp     edx, ecx
  0xb9367c  mov     word ptr [ebp+0], 9138h
  0xb93682  ja      loc_B93831
  0xb93688  mov     esi, [esp+48h+arg_0]
  0xb9368c  mov     [eax], esi
  0xb9368e  mov     esi, [esp+48h+arg_4]
  0xb93692  mov     [eax+4], esi
  0xb93695  lea     eax, [edx+2]
  0xb93698  cmp     eax, ecx
  0xb9369a  ja      loc_B93831
  0xb936a0  mov     cx, word ptr [esp+48h+arg_8]
  0xb936a5  mov     [edx], cx
  0xb936a8  lea     edx, [esp+48h+var_30]
  0xb936ac  mov     [esp+48h+var_30], eax
  0xb936b0  push    edx
  0xb936b1  lea     eax, [esp+4Ch+arg_C]
  0xb936b5  push    eax
  0xb936b6  call    sub_B02DA0
  0xb936bb  add     esp, 8
  0xb936be  test    al, al
  0xb936c0  jz      loc_B93831
  0xb936c6  mov     esi, [edi+7D08h]
  0xb936cc  test    esi, esi
  0xb936ce  mov     ebx, [esp+48h+var_30]
  0xb936d2  jz      loc_B937D2
  0xb936d8  lea     ecx, [esp+48h+var_28]
  0xb936dc  push    ecx
  0xb936dd  call    sub_CA0CE0
  0xb936e2  add     esp, 4
  0xb936e5  mov     edx, [edi+8]
  0xb936e8  push    offset aProtoLoungeCli_429; ")<-_proto_lounge_client::send_msma_equi"...
  0xb936ed  push    edx
  0xb936ee  push    offset aId; " (id:"
  0xb936f3  push    eax
  0xb936f4  push    esi
  0xb936f5  mov     byte ptr [esp+5Ch+var_4], 1
  0xb936fa  call    sub_B03020
  0xb936ff  add     esp, 8
  0xb93702  push    eax
  0xb93703  call    sub_41D990
  0xb93708  add     esp, 8
  0xb9370b  mov     ecx, eax
  0xb9370d  call    sub_ADC810
  0xb93712  push    eax
  0xb93713  call    sub_41D990
  0xb93718  add     esp, 8
  0xb9371b  lea     ecx, [esp+48h+var_28]
  0xb9371f  mov     byte ptr [esp+48h+var_4], 0
  0xb93724  call    sub_B02FF0
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。
> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B02B40`=写 NUL 串（其**紧邻之前的 `push N`** = 串槽预算）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb93738  push    offset aUniqidMs; "uniqid_ms="
  0xb93760  push    offset aEqSlot1; "eq_slot1="
  0xb93783  push    offset aEqSlot2; "eq_slot2="
  0xb93798  push    offset aByte; "]byte"
  0xb937a2  push    offset asc_EDAD58; " ) ["
```

## 4. 发送去向切片

```asm
  0xb937d4  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xb9367c` | u16 |
| `uniqid_ms` | `0xB9368C, 0xB93692` | u64 |
| `eq_slot1` | `0xB936A5` | u16 |
| `eq_slot2` | `0xB936B6` | u16 |
