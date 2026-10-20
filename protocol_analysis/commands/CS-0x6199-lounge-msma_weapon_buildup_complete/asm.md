# 汇编证据 —— CS-0x6199-lounge-msma_weapon_buildup_complete

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B973D0 @ `0xb973d0`（`0xb973d0`..`0xb97698`）
- 命令名字符串：`)<-_proto_lounge_client::send_msma_weapon_buildup_complete(` @ `0xeeba24`
- opcode 写入：`0xb9744c`
- 声明容量：`0x1A`

## 2. 组包块切片（游标初始化 → 提交）

```asm
  0xb9741a  mov     ebp, eax
  0xb9741c  mov     eax, [edi+0Ch]
  0xb9741f  push    eax
  0xb97420  lea     ecx, [esp+4Ch+var_34]
  0xb97424  call    sub_ABB2F0
  0xb97429  lea     ecx, [ebp+1Ah]
  0xb9742c  lea     eax, [ebp+2]
  0xb9742f  cmp     eax, ecx
  0xb97431  mov     [esp+48h+var_4], 0
  0xb97439  mov     [esp+48h+var_30], ebp
  0xb9743d  mov     dword ptr [esp+48h+var_2C], ecx
  0xb97441  ja      loc_B97683
  0xb97447  lea     edx, [eax+8]
  0xb9744a  cmp     edx, ecx
  0xb9744c  mov     word ptr [ebp+0], 6199h
  0xb97452  ja      loc_B97683
  0xb97458  mov     esi, [esp+48h+arg_0]
  0xb9745c  mov     [eax], esi
  0xb9745e  mov     esi, [esp+48h+arg_4]
  0xb97462  mov     [eax+4], esi
  0xb97465  lea     eax, [edx+4]
  0xb97468  cmp     eax, ecx
  0xb9746a  ja      loc_B97683
  0xb97470  mov     ecx, [esp+48h+arg_8]
  0xb97474  mov     [edx], ecx
  0xb97476  lea     edx, [esp+48h+var_30]
  0xb9747a  mov     [esp+48h+var_30], eax
  0xb9747e  push    edx
  0xb9747f  lea     eax, [esp+4Ch+arg_C]
  0xb97483  push    eax
  0xb97484  call    sub_B02D80
  0xb97489  add     esp, 8
  0xb9748c  test    al, al
  0xb9748e  jz      loc_B97683
  0xb97494  lea     ecx, [esp+48h+var_30]
  0xb97498  push    ecx
  0xb97499  lea     edx, [esp+4Ch+arg_10]
  0xb9749d  push    edx
  0xb9749e  call    sub_B02DA0
  0xb974a3  add     esp, 8
  0xb974a6  test    al, al
  0xb974a8  jz      loc_B97683
  0xb974ae  lea     eax, [esp+48h+var_30]
  0xb974b2  push    eax
  0xb974b3  lea     ecx, [esp+4Ch+arg_14]
  0xb974b7  push    ecx
  0xb974b8  call    sub_B02DA0
  0xb974bd  add     esp, 8
  0xb974c0  test    al, al
  0xb974c2  jz      loc_B97683
  0xb974c8  mov     esi, [edi+7E04h]
  0xb974ce  test    esi, esi
  0xb974d0  mov     ebx, [esp+48h+var_30]
  0xb974d4  jz      loc_B97624
  0xb974da  lea     edx, [esp+48h+var_28]
  0xb974de  push    edx
  0xb974df  call    sub_CA0CE0
  0xb974e4  add     esp, 4
  0xb974e7  mov     ecx, [edi+8]
  0xb974ea  push    offset aProtoLoungeCli_453; ")<-_proto_lounge_client::send_msma_weap"...
  0xb974ef  push    ecx
  0xb974f0  push    offset aId; " (id:"
  0xb974f5  push    eax
  0xb974f6  push    esi
  0xb974f7  mov     byte ptr [esp+5Ch+var_4], 1
  0xb974fc  call    sub_B03020
  0xb97501  add     esp, 8
  0xb97504  push    eax
  0xb97505  call    sub_41D990
  0xb9750a  add     esp, 8
  0xb9750d  mov     ecx, eax
  0xb9750f  call    sub_ADC810
  0xb97514  push    eax
  0xb97515  call    sub_41D990
  0xb9751a  add     esp, 8
  0xb9751d  lea     ecx, [esp+48h+var_28]
  0xb97521  mov     byte ptr [esp+48h+var_4], 0
  0xb97526  call    sub_B02FF0   <<<COMMIT
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb9753a  push    offset aUniqidMs; "uniqid_ms="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb97562  push    offset aItemId; "item_id="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb9758a  push    offset aTicketId; "ticket_id="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb975b2  push    offset aUsenum; "usenum="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb975d5  push    offset aParamTarget; "param_target="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb975ea  push    offset aByte; "]byte"
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
```

## 4. 发送去向切片

```asm
  0xb97626  mov     edx, [eax+58h]
  0xb97629  sub     ebx, ebp
  0xb9762b  push    ebx
  0xb9762c  push    ebp
  0xb9762d  mov     ecx, edi
  0xb9762f  call    edx
  0xb97631  test    al, al
  0xb97633  jz      short loc_B97683
  0xb97635  mov     eax, [edi+79A8h]
  0xb9763b  test    eax, eax
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。
> 本批 50 条**全部命中同一去向槽 `vt[0x58]`**（与批次-16/17 一致）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB9744C` | u16 |
| `uniqid_ms` | `0xB9745C` | u64 |
| `item_id` | `0xB97474` | u32 |
| `ticket_id` | `0xB97484` | u32 |
| `usenum` | `0xB9749E` | u16 |
| `param_target` | `0xB974B8` | u16 |
