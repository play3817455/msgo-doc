# 汇编证据 —— CS-0x5FAB-lounge-msma_weapon_buildup

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B96E30 @ `0xb96e30`（`0xb96e30`..`0xb970f8`）
- 命令名字符串：`)<-_proto_lounge_client::send_msma_weapon_buildup(` @ `0xeeb9b0`
- opcode 写入：`0xb96eac`
- 声明容量：`0x1A`

## 2. 组包块切片（游标初始化 → 提交）

```asm
  0xb96e7a  mov     ebp, eax
  0xb96e7c  mov     eax, [edi+0Ch]
  0xb96e7f  push    eax
  0xb96e80  lea     ecx, [esp+4Ch+var_34]
  0xb96e84  call    sub_ABB2F0
  0xb96e89  lea     ecx, [ebp+1Ah]
  0xb96e8c  lea     eax, [ebp+2]
  0xb96e8f  cmp     eax, ecx
  0xb96e91  mov     [esp+48h+var_4], 0
  0xb96e99  mov     [esp+48h+var_30], ebp
  0xb96e9d  mov     dword ptr [esp+48h+var_2C], ecx
  0xb96ea1  ja      loc_B970E3
  0xb96ea7  lea     edx, [eax+8]
  0xb96eaa  cmp     edx, ecx
  0xb96eac  mov     word ptr [ebp+0], 5FABh
  0xb96eb2  ja      loc_B970E3
  0xb96eb8  mov     esi, [esp+48h+arg_0]
  0xb96ebc  mov     [eax], esi
  0xb96ebe  mov     esi, [esp+48h+arg_4]
  0xb96ec2  mov     [eax+4], esi
  0xb96ec5  lea     eax, [edx+4]
  0xb96ec8  cmp     eax, ecx
  0xb96eca  ja      loc_B970E3
  0xb96ed0  mov     ecx, [esp+48h+arg_8]
  0xb96ed4  mov     [edx], ecx
  0xb96ed6  lea     edx, [esp+48h+var_30]
  0xb96eda  mov     [esp+48h+var_30], eax
  0xb96ede  push    edx
  0xb96edf  lea     eax, [esp+4Ch+arg_C]
  0xb96ee3  push    eax
  0xb96ee4  call    sub_B02D80
  0xb96ee9  add     esp, 8
  0xb96eec  test    al, al
  0xb96eee  jz      loc_B970E3
  0xb96ef4  lea     ecx, [esp+48h+var_30]
  0xb96ef8  push    ecx
  0xb96ef9  lea     edx, [esp+4Ch+arg_10]
  0xb96efd  push    edx
  0xb96efe  call    sub_B02DA0
  0xb96f03  add     esp, 8
  0xb96f06  test    al, al
  0xb96f08  jz      loc_B970E3
  0xb96f0e  lea     eax, [esp+48h+var_30]
  0xb96f12  push    eax
  0xb96f13  lea     ecx, [esp+4Ch+arg_14]
  0xb96f17  push    ecx
  0xb96f18  call    sub_B02DA0
  0xb96f1d  add     esp, 8
  0xb96f20  test    al, al
  0xb96f22  jz      loc_B970E3
  0xb96f28  mov     esi, [edi+7DF4h]
  0xb96f2e  test    esi, esi
  0xb96f30  mov     ebx, [esp+48h+var_30]
  0xb96f34  jz      loc_B97084
  0xb96f3a  lea     edx, [esp+48h+var_28]
  0xb96f3e  push    edx
  0xb96f3f  call    sub_CA0CE0
  0xb96f44  add     esp, 4
  0xb96f47  mov     ecx, [edi+8]
  0xb96f4a  push    offset aProtoLoungeCli_451; ")<-_proto_lounge_client::send_msma_weap"...
  0xb96f4f  push    ecx
  0xb96f50  push    offset aId; " (id:"
  0xb96f55  push    eax
  0xb96f56  push    esi
  0xb96f57  mov     byte ptr [esp+5Ch+var_4], 1
  0xb96f5c  call    sub_B03020
  0xb96f61  add     esp, 8
  0xb96f64  push    eax
  0xb96f65  call    sub_41D990
  0xb96f6a  add     esp, 8
  0xb96f6d  mov     ecx, eax
  0xb96f6f  call    sub_ADC810
  0xb96f74  push    eax
  0xb96f75  call    sub_41D990
  0xb96f7a  add     esp, 8
  0xb96f7d  lea     ecx, [esp+48h+var_28]
  0xb96f81  mov     byte ptr [esp+48h+var_4], 0
  0xb96f86  call    sub_B02FF0   <<<COMMIT
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb96f9a  push    offset aUniqidMs; "uniqid_ms="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb96fc2  push    offset aItemId; "item_id="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb96fea  push    offset aTicketId; "ticket_id="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb97012  push    offset aUsenum; "usenum="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb97035  push    offset aParamTarget; "param_target="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb9704a  push    offset aByte; "]byte"
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
```

## 4. 发送去向切片

```asm
  0xb97086  mov     edx, [eax+58h]
  0xb97089  sub     ebx, ebp
  0xb9708b  push    ebx
  0xb9708c  push    ebp
  0xb9708d  mov     ecx, edi
  0xb9708f  call    edx
  0xb97091  test    al, al
  0xb97093  jz      short loc_B970E3
  0xb97095  mov     eax, [edi+79A8h]
  0xb9709b  test    eax, eax
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。
> 本批 50 条**全部命中同一去向槽 `vt[0x58]`**（与批次-16/17 一致）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB96EAC` | u16 |
| `uniqid_ms` | `0xB96EBC` | u64 |
| `item_id` | `0xB96ED4` | u32 |
| `ticket_id` | `0xB96EE4` | u32 |
| `usenum` | `0xB96EFE` | u16 |
| `param_target` | `0xB96F18` | u16 |
