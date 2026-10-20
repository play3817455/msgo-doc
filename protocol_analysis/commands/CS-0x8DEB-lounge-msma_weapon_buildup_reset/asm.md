# 汇编证据 —— CS-0x8DEB-lounge-msma_weapon_buildup_reset

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B976A0 @ `0xb976a0`（`0xb976a0`..`0xb97892`）
- 命令名字符串：`)<-_proto_lounge_client::send_msma_weapon_buildup_reset(` @ `0xeeba64`
- opcode 写入：`0xb97714`
- 声明容量：`0xE`（分配器容量 `push` @ `0xb976e6`）

## 2. 组包块切片（游标初始化 → 逐字段写线 → 提交）

```asm
  0xb976ea  mov     ebp, eax
  0xb976ec  mov     eax, [edi+0Ch]
  0xb976ef  push    eax
  0xb976f0  lea     ecx, [esp+44h+var_2C]
  0xb976f4  call    sub_ABB2F0
  0xb976f9  lea     ecx, [ebp+0Eh]
  0xb976fc  lea     eax, [ebp+2]
  0xb976ff  cmp     eax, ecx
  0xb97701  mov     [esp+40h+var_4], 0
  0xb97709  ja      loc_B9787D
  0xb9770f  lea     edx, [eax+8]
  0xb97712  cmp     edx, ecx
  0xb97714  mov     word ptr [ebp+0], 8DEBh
  0xb9771a  ja      loc_B9787D
  0xb97720  mov     esi, [esp+40h+arg_0]
  0xb97724  mov     [eax], esi
  0xb97726  mov     esi, [esp+40h+arg_4]
  0xb9772a  lea     ebx, [edx+4]
  0xb9772d  cmp     ebx, ecx
  0xb9772f  mov     [eax+4], esi
  0xb97732  ja      loc_B9787D
  0xb97738  mov     ecx, [esp+40h+arg_8]
  0xb9773c  mov     [edx], ecx
  0xb9773e  mov     esi, [edi+7E0Ch]
  0xb97744  test    esi, esi
  0xb97746  jz      loc_B9781E
  0xb9774c  lea     edx, [esp+40h+var_28]
  0xb97750  push    edx
  0xb97751  call    sub_CA0CE0
  0xb97756  add     esp, 4
  0xb97759  mov     ecx, [edi+8]
  0xb9775c  push    offset aProtoLoungeCli_455; ")<-_proto_lounge_client::send_msma_weap"...
  0xb97761  push    ecx
  0xb97762  push    offset aId; " (id:"
  0xb97767  push    eax
  0xb97768  push    esi
  0xb97769  mov     byte ptr [esp+54h+var_4], 1
  0xb9776e  call    sub_B03020
  0xb97773  add     esp, 8
  0xb97776  push    eax
  0xb97777  call    sub_41D990
  0xb9777c  add     esp, 8
  0xb9777f  mov     ecx, eax
  0xb97781  call    sub_ADC810
  0xb97786  push    eax
  0xb97787  call    sub_41D990
  0xb9778c  add     esp, 8
  0xb9778f  lea     ecx, [esp+40h+var_28]
  0xb97793  mov     byte ptr [esp+40h+var_4], 0
  0xb97798  call    sub_B02FF0
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。
> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B02B40`=写 NUL 串（其**紧邻之前的 `push N`** = 串槽预算）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb977ac  push    offset aUniqidMs; "uniqid_ms="
  0xb977cf  push    offset aItemId; "item_id="
  0xb977e4  push    offset aByte; "]byte"
  0xb977ee  push    offset asc_EDAD58; " ) ["
```

## 4. 发送去向切片

```asm
  0xb97820  mov     edx, [eax+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xb97714` | u16 |
| `uniqid_ms` | `0xB97724, 0xB9772F` | u64 |
| `item_id` | `0xB9773C` | u32 |
