# 汇编证据 —— CS-0x645D-lounge-party_create

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B91AD0 @ `0xb91ad0`（`0xb91ad0`..`0xb91d27`）
- 命令名字符串：`)<-_proto_lounge_client::send_party_create(` @ `0xeeb0f0`
- opcode 写入：`0xb91b4c`
- 声明容量：`0x4A`

## 2. 组包块切片（游标初始化 → 提交）

```asm
  0xb91b1a  mov     ebp, eax
  0xb91b1c  mov     eax, [edi+0Ch]
  0xb91b1f  push    eax
  0xb91b20  lea     ecx, [esp+4Ch+var_34]
  0xb91b24  call    sub_ABB2F0
  0xb91b29  lea     ecx, [ebp+4Ah]
  0xb91b2c  lea     eax, [ebp+2]
  0xb91b2f  cmp     eax, ecx
  0xb91b31  mov     [esp+48h+var_4], 0
  0xb91b39  mov     [esp+48h+var_30], ebp
  0xb91b3d  mov     dword ptr [esp+48h+var_2C], ecx
  0xb91b41  ja      loc_B91D12
  0xb91b47  lea     edx, [eax+1]
  0xb91b4a  cmp     edx, ecx
  0xb91b4c  mov     word ptr [ebp+0], 645Dh
  0xb91b52  ja      loc_B91D12
  0xb91b58  mov     cl, byte ptr [esp+48h+arg_0]
  0xb91b5c  mov     [esp+48h+var_30], edx
  0xb91b60  push    3Dh ; '='
  0xb91b62  lea     edx, [esp+4Ch+var_30]
  0xb91b66  mov     [eax], cl
  0xb91b68  mov     eax, [esp+4Ch+arg_4]
  0xb91b6c  push    edx
  0xb91b6d  push    eax
  0xb91b6e  call    sub_B02B40   <<< pushN=61(0x3D)
  0xb91b73  add     esp, 0Ch
  0xb91b76  test    al, al
  0xb91b78  jz      loc_B91D12
  0xb91b7e  lea     ecx, [esp+48h+var_30]
  0xb91b82  push    ecx
  0xb91b83  lea     edx, [esp+4Ch+arg_8]
  0xb91b87  push    edx
  0xb91b88  call    sub_B02D80
  0xb91b8d  add     esp, 8
  0xb91b90  test    al, al
  0xb91b92  jz      loc_B91D12
  0xb91b98  mov     esi, [edi+7C6Ch]
  0xb91b9e  test    esi, esi
  0xb91ba0  mov     ebx, [esp+48h+var_30]
  0xb91ba4  jz      loc_B91CB1
  0xb91baa  lea     eax, [esp+48h+var_28]
  0xb91bae  push    eax
  0xb91baf  call    sub_CA0CE0
  0xb91bb4  add     esp, 4
  0xb91bb7  mov     ecx, [edi+8]
  0xb91bba  push    offset aProtoLoungeCli_509; ")<-_proto_lounge_client::send_party_cre"...
  0xb91bbf  push    ecx
  0xb91bc0  push    offset aId; " (id:"
  0xb91bc5  push    eax
  0xb91bc6  push    esi
  0xb91bc7  mov     byte ptr [esp+5Ch+var_4], 1
  0xb91bcc  call    sub_B03020
  0xb91bd1  add     esp, 8
  0xb91bd4  push    eax
  0xb91bd5  call    sub_41D990
  0xb91bda  add     esp, 8
  0xb91bdd  mov     ecx, eax
  0xb91bdf  call    sub_ADC810
  0xb91be4  push    eax
  0xb91be5  call    sub_41D990
  0xb91bea  add     esp, 8
  0xb91bed  lea     ecx, [esp+48h+var_28]
  0xb91bf1  mov     byte ptr [esp+48h+var_4], 0
  0xb91bf6  call    sub_B02FF0   <<<COMMIT
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb91c05  push    offset aIsRecruiting; "is_recruiting="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb91c34  push    offset aComment_0; "comment=\""
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb91c62  push    offset aPartyType; "party_type="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb91c77  push    offset aByte; "]byte"
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
```

## 4. 发送去向切片

```asm
  0xb91cb3  mov     edx, [eax+58h]
  0xb91cb6  mov     esi, ebx
  0xb91cb8  sub     esi, ebp
  0xb91cba  push    esi
  0xb91cbb  push    ebp
  0xb91cbc  mov     ecx, edi
  0xb91cbe  call    edx
  0xb91cc0  test    al, al
  0xb91cc2  jz      short loc_B91D12
  0xb91cc4  mov     eax, [edi+79A8h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。
> 本批 50 条**全部命中同一去向槽 `vt[0x58]`**（与批次-16/17 一致）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB91B4C` | u16 |
| `is_recruiting` | `0xB91B66` | u8 |
| `comment` | `0xB91B6E` | bytes |
| `party_type` | `0xB91B88` | u32 |
