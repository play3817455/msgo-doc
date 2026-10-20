# 汇编证据 —— CS-0x9226-lounge-party_info_edit

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B92650 @ `0xb92650`（`0xb92650`..`0xb928a7`）
- 命令名字符串：`)<-_proto_lounge_client::send_party_info_edit(` @ `0xeeb210`
- opcode 写入：`0xb926cc`
- 声明容量：`0x4A`（分配器容量 `push` @ `0xb92696`）

## 2. 组包块切片（游标初始化 → 逐字段写线 → 提交）

```asm
  0xb9269a  mov     ebp, eax
  0xb9269c  mov     eax, [edi+0Ch]
  0xb9269f  push    eax
  0xb926a0  lea     ecx, [esp+4Ch+var_34]
  0xb926a4  call    sub_ABB2F0
  0xb926a9  lea     ecx, [ebp+4Ah]
  0xb926ac  lea     eax, [ebp+2]
  0xb926af  cmp     eax, ecx
  0xb926b1  mov     [esp+48h+var_4], 0
  0xb926b9  mov     [esp+48h+var_30], ebp
  0xb926bd  mov     dword ptr [esp+48h+var_2C], ecx
  0xb926c1  ja      loc_B92892
  0xb926c7  lea     edx, [eax+1]
  0xb926ca  cmp     edx, ecx
  0xb926cc  mov     word ptr [ebp+0], 9226h
  0xb926d2  ja      loc_B92892
  0xb926d8  mov     cl, byte ptr [esp+48h+arg_0]
  0xb926dc  mov     [esp+48h+var_30], edx
  0xb926e0  push    3Dh ; '='
  0xb926e2  lea     edx, [esp+4Ch+var_30]
  0xb926e6  mov     [eax], cl
  0xb926e8  mov     eax, [esp+4Ch+arg_4]
  0xb926ec  push    edx
  0xb926ed  push    eax
  0xb926ee  call    sub_B02B40
  0xb926f3  add     esp, 0Ch
  0xb926f6  test    al, al
  0xb926f8  jz      loc_B92892
  0xb926fe  lea     ecx, [esp+48h+var_30]
  0xb92702  push    ecx
  0xb92703  lea     edx, [esp+4Ch+arg_8]
  0xb92707  push    edx
  0xb92708  call    sub_B02D80
  0xb9270d  add     esp, 8
  0xb92710  test    al, al
  0xb92712  jz      loc_B92892
  0xb92718  mov     esi, [edi+7CA8h]
  0xb9271e  test    esi, esi
  0xb92720  mov     ebx, [esp+48h+var_30]
  0xb92724  jz      loc_B92831
  0xb9272a  lea     eax, [esp+48h+var_28]
  0xb9272e  push    eax
  0xb9272f  call    sub_CA0CE0
  0xb92734  add     esp, 4
  0xb92737  mov     ecx, [edi+8]
  0xb9273a  push    offset aProtoLoungeCli_558; ")<-_proto_lounge_client::send_party_inf"...
  0xb9273f  push    ecx
  0xb92740  push    offset aId; " (id:"
  0xb92745  push    eax
  0xb92746  push    esi
  0xb92747  mov     byte ptr [esp+5Ch+var_4], 1
  0xb9274c  call    sub_B03020
  0xb92751  add     esp, 8
  0xb92754  push    eax
  0xb92755  call    sub_41D990
  0xb9275a  add     esp, 8
  0xb9275d  mov     ecx, eax
  0xb9275f  call    sub_ADC810
  0xb92764  push    eax
  0xb92765  call    sub_41D990
  0xb9276a  add     esp, 8
  0xb9276d  lea     ecx, [esp+48h+var_28]
  0xb92771  mov     byte ptr [esp+48h+var_4], 0
  0xb92776  call    sub_B02FF0
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。
> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B02B40`=写 NUL 串（其**紧邻之前的 `push N`** = 串槽预算）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb92785  push    offset aIsRecruiting; "is_recruiting="
  0xb927ae  push    offset asc_EDAD54; "\""
  0xb927b4  push    offset aComment_0; "comment=\""
  0xb927e2  push    offset aPartyType; "party_type="
  0xb927f7  push    offset aByte; "]byte"
  0xb92801  push    offset asc_EDAD58; " ) ["
```

## 4. 发送去向切片

```asm
  0xb92833  mov     edx, [eax+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xb926cc` | u16 |
| `is_recruiting` | `0xB926E6` | u8 |
| `comment` | `0xB926EE` | bytes |
| `party_type` | `0xB92708` | u32 |
