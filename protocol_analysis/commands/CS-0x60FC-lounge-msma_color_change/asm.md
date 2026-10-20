# 汇编证据 —— CS-0x60FC-lounge-msma_color_change

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B94C60 @ `0xb94c60`（`0xb94c60`..`0xb94e52`）
- 命令名字符串：`)<-_proto_lounge_client::send_msma_color_change(` @ `0xeeb654`
- opcode 写入：`0xb94cd4`
- 声明容量：`0xE`

## 2. 组包块切片（游标初始化 → 提交）

```asm
  0xb94caa  mov     ebp, eax
  0xb94cac  mov     eax, [edi+0Ch]
  0xb94caf  push    eax
  0xb94cb0  lea     ecx, [esp+44h+var_2C]
  0xb94cb4  call    sub_ABB2F0
  0xb94cb9  lea     ecx, [ebp+0Eh]
  0xb94cbc  lea     eax, [ebp+2]
  0xb94cbf  cmp     eax, ecx
  0xb94cc1  mov     [esp+40h+var_4], 0
  0xb94cc9  ja      loc_B94E3D
  0xb94ccf  lea     edx, [eax+8]
  0xb94cd2  cmp     edx, ecx
  0xb94cd4  mov     word ptr [ebp+0], 60FCh
  0xb94cda  ja      loc_B94E3D
  0xb94ce0  mov     esi, [esp+40h+arg_0]
  0xb94ce4  mov     [eax], esi
  0xb94ce6  mov     esi, [esp+40h+arg_4]
  0xb94cea  lea     ebx, [edx+4]
  0xb94ced  cmp     ebx, ecx
  0xb94cef  mov     [eax+4], esi
  0xb94cf2  ja      loc_B94E3D
  0xb94cf8  mov     ecx, [esp+40h+arg_8]
  0xb94cfc  mov     [edx], ecx
  0xb94cfe  mov     esi, [edi+7D74h]
  0xb94d04  test    esi, esi
  0xb94d06  jz      loc_B94DDE
  0xb94d0c  lea     edx, [esp+40h+var_28]
  0xb94d10  push    edx
  0xb94d11  call    sub_CA0CE0
  0xb94d16  add     esp, 4
  0xb94d19  mov     ecx, [edi+8]
  0xb94d1c  push    offset aProtoLoungeCli_462; ")<-_proto_lounge_client::send_msma_colo"...
  0xb94d21  push    ecx
  0xb94d22  push    offset aId; " (id:"
  0xb94d27  push    eax
  0xb94d28  push    esi
  0xb94d29  mov     byte ptr [esp+54h+var_4], 1
  0xb94d2e  call    sub_B03020
  0xb94d33  add     esp, 8
  0xb94d36  push    eax
  0xb94d37  call    sub_41D990
  0xb94d3c  add     esp, 8
  0xb94d3f  mov     ecx, eax
  0xb94d41  call    sub_ADC810
  0xb94d46  push    eax
  0xb94d47  call    sub_41D990
  0xb94d4c  add     esp, 8
  0xb94d4f  lea     ecx, [esp+40h+var_28]
  0xb94d53  mov     byte ptr [esp+40h+var_4], 0
  0xb94d58  call    sub_B02FF0   <<<COMMIT
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb94d6c  push    offset aUniqidMs; "uniqid_ms="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb94d8f  push    offset aColor; "color="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb94da4  push    offset aByte; "]byte"
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
```

## 4. 发送去向切片

```asm
  0xb94de0  mov     edx, [eax+58h]
  0xb94de3  sub     ebx, ebp
  0xb94de5  push    ebx
  0xb94de6  push    ebp
  0xb94de7  mov     ecx, edi
  0xb94de9  call    edx
  0xb94deb  test    al, al
  0xb94ded  jz      short loc_B94E3D
  0xb94def  mov     eax, [edi+79A8h]
  0xb94df5  test    eax, eax
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。
> 本批 50 条**全部命中同一去向槽 `vt[0x58]`**（与批次-16/17 一致）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB94CD4` | u16 |
| `uniqid_ms` | `0xB94CE4` | u64 |
| `color` | `0xB94CFC` | u32 |
