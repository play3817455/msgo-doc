# 汇编证据 —— CS-0x753A-lounge-block_list_remove

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B9B720 @ `0xb9b720`（`0xb9b720`..`0xb9b9ae`）
- 命令名字符串：`)<-_proto_lounge_client::send_block_list_remove(` @ `0xeec168`
- opcode 写入：`0xb9b79c`
- 声明容量：`0x2A`（分配器容量 `push` @ `0xb9b766`）

## 2. 组包块切片（游标初始化 → 逐字段写线 → 提交）

```asm
  0xb9b76a  mov     ebp, eax
  0xb9b76c  mov     eax, [edi+0Ch]
  0xb9b76f  push    eax
  0xb9b770  lea     ecx, [esp+4Ch+var_34]
  0xb9b774  call    sub_ABB2F0
  0xb9b779  lea     ecx, [ebp+2Ah]
  0xb9b77c  lea     eax, [ebp+2]
  0xb9b77f  cmp     eax, ecx
  0xb9b781  mov     [esp+48h+var_4], 0
  0xb9b789  mov     [esp+48h+var_30], ebp
  0xb9b78d  mov     dword ptr [esp+48h+var_2C], ecx
  0xb9b791  ja      loc_B9B999
  0xb9b797  lea     edx, [eax+4]
  0xb9b79a  cmp     edx, ecx
  0xb9b79c  mov     word ptr [ebp+0], 753Ah
  0xb9b7a2  ja      loc_B9B999
  0xb9b7a8  mov     esi, [esp+48h+arg_0]
  0xb9b7ac  mov     [eax], esi
  0xb9b7ae  mov     eax, edx
  0xb9b7b0  lea     edx, [eax+4]
  0xb9b7b3  cmp     edx, ecx
  0xb9b7b5  ja      loc_B9B999
  0xb9b7bb  mov     ecx, [esp+48h+arg_4]
  0xb9b7bf  mov     [esp+48h+var_30], edx
  0xb9b7c3  push    19h
  0xb9b7c5  lea     edx, [esp+4Ch+var_30]
  0xb9b7c9  mov     [eax], ecx
  0xb9b7cb  mov     eax, [esp+4Ch+arg_8]
  0xb9b7cf  push    edx
  0xb9b7d0  push    eax
  0xb9b7d1  call    sub_B02B40
  0xb9b7d6  add     esp, 0Ch
  0xb9b7d9  test    al, al
  0xb9b7db  jz      loc_B9B999
  0xb9b7e1  lea     ecx, [esp+48h+var_30]
  0xb9b7e5  push    ecx
  0xb9b7e6  lea     edx, [esp+4Ch+arg_C]
  0xb9b7ea  push    edx
  0xb9b7eb  call    sub_B02D80
  0xb9b7f0  add     esp, 8
  0xb9b7f3  test    al, al
  0xb9b7f5  jz      loc_B9B999
  0xb9b7fb  mov     esi, [edi+7F40h]
  0xb9b801  test    esi, esi
  0xb9b803  mov     ebx, [esp+48h+var_30]
  0xb9b807  jz      loc_B9B93A
  0xb9b80d  lea     eax, [esp+48h+var_28]
  0xb9b811  push    eax
  0xb9b812  call    sub_CA0CE0
  0xb9b817  add     esp, 4
  0xb9b81a  mov     ecx, [edi+8]
  0xb9b81d  push    offset aProtoLoungeCli_387; ")<-_proto_lounge_client::send_block_lis"...
  0xb9b822  push    ecx
  0xb9b823  push    offset aId; " (id:"
  0xb9b828  push    eax
  0xb9b829  push    esi
  0xb9b82a  mov     byte ptr [esp+5Ch+var_4], 1
  0xb9b82f  call    sub_B03020
  0xb9b834  add     esp, 8
  0xb9b837  push    eax
  0xb9b838  call    sub_41D990
  0xb9b83d  add     esp, 8
  0xb9b840  mov     ecx, eax
  0xb9b842  call    sub_ADC810
  0xb9b847  push    eax
  0xb9b848  call    sub_41D990
  0xb9b84d  add     esp, 8
  0xb9b850  lea     ecx, [esp+48h+var_28]
  0xb9b854  mov     byte ptr [esp+48h+var_4], 0
  0xb9b859  call    sub_B02FF0
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。
> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B02B40`=写 NUL 串（其**紧邻之前的 `push N`** = 串槽预算）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb9b868  push    offset aPilotid; "pilotid="
  0xb9b890  push    offset aWorldId; "world_id="
  0xb9b8b7  push    offset asc_EDAD54; "\""
  0xb9b8bd  push    offset aToPilotName; "to_pilot_name=\""
  0xb9b8eb  push    offset aSendSysmes; "send_sysmes="
  0xb9b900  push    offset aByte; "]byte"
  0xb9b90a  push    offset asc_EDAD58; " ) ["
```

## 4. 发送去向切片

```asm
  0xb9b93c  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xb9b79c` | u16 |
| `pilotid` | `0xB9B7AC` | u32 |
| `world_id` | `0xB9B7C9` | u32 |
| `to_pilot_name` | `0xB9B7D1` | bytes |
| `send_sysmes` | `0xB9B7EB` | u32 |
