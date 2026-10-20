# 汇编证据 —— CS-0x6E16-lounge-party_invite_refuse

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B91EE0 @ `0xb91ee0`（`0xb91ee0`..`0xb9215c`）
- 命令名字符串：`)<-_proto_lounge_client::send_party_invite_refuse(` @ `0xeeb150`
- opcode 写入：`0xb91f5c`
- 声明容量：`0x12`（分配器容量 `push` @ `0xb91f26`）

## 2. 组包块切片（游标初始化 → 逐字段写线 → 提交）

```asm
  0xb91f2a  mov     ebp, eax
  0xb91f2c  mov     eax, [edi+0Ch]
  0xb91f2f  push    eax
  0xb91f30  lea     ecx, [esp+4Ch+var_34]
  0xb91f34  call    sub_ABB2F0
  0xb91f39  lea     ecx, [ebp+12h]
  0xb91f3c  lea     eax, [ebp+2]
  0xb91f3f  cmp     eax, ecx
  0xb91f41  mov     [esp+48h+var_4], 0
  0xb91f49  mov     [esp+48h+var_30], ebp
  0xb91f4d  mov     dword ptr [esp+48h+var_2C], ecx
  0xb91f51  ja      loc_B92147
  0xb91f57  lea     edx, [eax+4]
  0xb91f5a  cmp     edx, ecx
  0xb91f5c  mov     word ptr [ebp+0], 6E16h
  0xb91f62  ja      loc_B92147
  0xb91f68  mov     esi, [esp+48h+arg_0]
  0xb91f6c  mov     [eax], esi
  0xb91f6e  mov     eax, edx
  0xb91f70  lea     edx, [eax+4]
  0xb91f73  cmp     edx, ecx
  0xb91f75  ja      loc_B92147
  0xb91f7b  mov     ecx, [esp+48h+arg_4]
  0xb91f7f  mov     [esp+48h+var_30], edx
  0xb91f83  lea     edx, [esp+48h+var_30]
  0xb91f87  mov     [eax], ecx
  0xb91f89  push    edx
  0xb91f8a  lea     eax, [esp+4Ch+arg_8]
  0xb91f8e  push    eax
  0xb91f8f  call    sub_B02D80
  0xb91f94  add     esp, 8
  0xb91f97  test    al, al
  0xb91f99  jz      loc_B92147
  0xb91f9f  lea     ecx, [esp+48h+var_30]
  0xb91fa3  push    ecx
  0xb91fa4  lea     edx, [esp+4Ch+arg_C]
  0xb91fa8  push    edx
  0xb91fa9  call    sub_B02D80
  0xb91fae  add     esp, 8
  0xb91fb1  test    al, al
  0xb91fb3  jz      loc_B92147
  0xb91fb9  mov     esi, [edi+7C80h]
  0xb91fbf  test    esi, esi
  0xb91fc1  mov     ebx, [esp+48h+var_30]
  0xb91fc5  jz      loc_B920E8
  0xb91fcb  lea     eax, [esp+48h+var_28]
  0xb91fcf  push    eax
  0xb91fd0  call    sub_CA0CE0
  0xb91fd5  add     esp, 4
  0xb91fd8  mov     ecx, [edi+8]
  0xb91fdb  push    offset aProtoLoungeCli_513; ")<-_proto_lounge_client::send_party_inv"...
  0xb91fe0  push    ecx
  0xb91fe1  push    offset aId; " (id:"
  0xb91fe6  push    eax
  0xb91fe7  push    esi
  0xb91fe8  mov     byte ptr [esp+5Ch+var_4], 1
  0xb91fed  call    sub_B03020
  0xb91ff2  add     esp, 8
  0xb91ff5  push    eax
  0xb91ff6  call    sub_41D990
  0xb91ffb  add     esp, 8
  0xb91ffe  mov     ecx, eax
  0xb92000  call    sub_ADC810
  0xb92005  push    eax
  0xb92006  call    sub_41D990
  0xb9200b  add     esp, 8
  0xb9200e  lea     ecx, [esp+48h+var_28]
  0xb92012  mov     byte ptr [esp+48h+var_4], 0
  0xb92017  call    sub_B02FF0
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。
> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B02B40`=写 NUL 串（其**紧邻之前的 `push N`** = 串槽预算）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb92026  push    offset aPartyId; "party_id="
  0xb9204e  push    offset aChannelId; "channel_id="
  0xb92076  push    offset aPilotId; "pilot_id="
  0xb92099  push    offset aReason; "reason="
  0xb920ae  push    offset aByte; "]byte"
  0xb920b8  push    offset asc_EDAD58; " ) ["
```

## 4. 发送去向切片

```asm
  0xb920ea  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xb91f5c` | u16 |
| `party_id` | `0xB91F6C` | u32 |
| `channel_id` | `0xB91F87` | u32 |
| `pilot_id` | `0xB91F8F` | u32 |
| `reason` | `0xB91FA9` | u32 |
