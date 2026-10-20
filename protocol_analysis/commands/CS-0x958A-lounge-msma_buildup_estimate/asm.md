# 汇编证据 —— CS-0x958A-lounge-msma_buildup_estimate

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B96550 @ `0xb96550`（`0xb96550`..`0xb967d6`）
- 命令名字符串：`)<-_proto_lounge_client::send_msma_buildup_estimate(` @ `0xeeb8c0`
- opcode 写入：`0xb965cc`
- 声明容量：`0x16`（分配器容量 `push` @ `0xb96596`）

## 2. 组包块切片（游标初始化 → 逐字段写线 → 提交）

```asm
  0xb9659a  mov     ebp, eax
  0xb9659c  mov     eax, [edi+0Ch]
  0xb9659f  push    eax
  0xb965a0  lea     ecx, [esp+4Ch+var_34]
  0xb965a4  call    sub_ABB2F0
  0xb965a9  lea     ecx, [ebp+16h]
  0xb965ac  lea     eax, [ebp+2]
  0xb965af  cmp     eax, ecx
  0xb965b1  mov     [esp+48h+var_4], 0
  0xb965b9  mov     [esp+48h+var_30], ebp
  0xb965bd  mov     dword ptr [esp+48h+var_2C], ecx
  0xb965c1  ja      loc_B967C1
  0xb965c7  lea     edx, [eax+8]
  0xb965ca  cmp     edx, ecx
  0xb965cc  mov     word ptr [ebp+0], 958Ah
  0xb965d2  ja      loc_B967C1
  0xb965d8  mov     esi, [esp+48h+arg_0]
  0xb965dc  mov     [eax], esi
  0xb965de  mov     esi, [esp+48h+arg_4]
  0xb965e2  mov     [eax+4], esi
  0xb965e5  lea     eax, [edx+4]
  0xb965e8  cmp     eax, ecx
  0xb965ea  ja      loc_B967C1
  0xb965f0  mov     ecx, [esp+48h+arg_8]
  0xb965f4  mov     [edx], ecx
  0xb965f6  lea     edx, [esp+48h+var_30]
  0xb965fa  mov     [esp+48h+var_30], eax
  0xb965fe  push    edx
  0xb965ff  lea     eax, [esp+4Ch+arg_C]
  0xb96603  push    eax
  0xb96604  call    sub_B02DA0
  0xb96609  add     esp, 8
  0xb9660c  test    al, al
  0xb9660e  jz      loc_B967C1
  0xb96614  lea     ecx, [esp+48h+var_30]
  0xb96618  push    ecx
  0xb96619  lea     edx, [esp+4Ch+arg_10]
  0xb9661d  push    edx
  0xb9661e  call    sub_B02DA0
  0xb96623  add     esp, 8
  0xb96626  test    al, al
  0xb96628  jz      loc_B967C1
  0xb9662e  mov     esi, [edi+7DD4h]
  0xb96634  test    esi, esi
  0xb96636  mov     ebx, [esp+48h+var_30]
  0xb9663a  jz      loc_B96762
  0xb96640  lea     eax, [esp+48h+var_28]
  0xb96644  push    eax
  0xb96645  call    sub_CA0CE0
  0xb9664a  add     esp, 4
  0xb9664d  mov     ecx, [edi+8]
  0xb96650  push    offset aProtoLoungeCli_449; ")<-_proto_lounge_client::send_msma_buil"...
  0xb96655  push    ecx
  0xb96656  push    offset aId; " (id:"
  0xb9665b  push    eax
  0xb9665c  push    esi
  0xb9665d  mov     byte ptr [esp+5Ch+var_4], 1
  0xb96662  call    sub_B03020
  0xb96667  add     esp, 8
  0xb9666a  push    eax
  0xb9666b  call    sub_41D990
  0xb96670  add     esp, 8
  0xb96673  mov     ecx, eax
  0xb96675  call    sub_ADC810
  0xb9667a  push    eax
  0xb9667b  call    sub_41D990
  0xb96680  add     esp, 8
  0xb96683  lea     ecx, [esp+48h+var_28]
  0xb96687  mov     byte ptr [esp+48h+var_4], 0
  0xb9668c  call    sub_B02FF0
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。
> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B02B40`=写 NUL 串（其**紧邻之前的 `push N`** = 串槽预算）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb966a0  push    offset aUniqidMs; "uniqid_ms="
  0xb966c8  push    offset aTicketId; "ticket_id="
  0xb966f0  push    offset aUsenum; "usenum="
  0xb96713  push    offset aParamIdx; "param_idx="
  0xb96728  push    offset aByte; "]byte"
  0xb96732  push    offset asc_EDAD58; " ) ["
```

## 4. 发送去向切片

```asm
  0xb96764  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xb965cc` | u16 |
| `uniqid_ms` | `0xB965DC, 0xB965E2` | u64 |
| `ticket_id` | `0xB965F4` | u32 |
| `usenum` | `0xB96604` | u16 |
| `param_idx` | `0xB9661E` | u16 |
