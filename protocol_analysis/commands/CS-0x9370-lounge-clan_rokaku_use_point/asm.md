# 汇编证据 —— CS-0x9370-lounge-clan_rokaku_use_point

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_BA2A80 @ `0xba2a80`（`0xba2a80`..`0xba2d40`）
- 命令名字符串：`)<-_proto_lounge_client::send_clan_rokaku_use_point(` @ `0xeeccb0`
- opcode 写入：`0xba2afc`
- 声明容量：`0x16`（分配器容量 `push` @ `0xba2ac6`）

## 2. 组包块切片（游标初始化 → 逐字段写线 → 提交）

```asm
  0xba2aca  mov     ebp, eax
  0xba2acc  mov     eax, [edi+0Ch]
  0xba2acf  push    eax
  0xba2ad0  lea     ecx, [esp+4Ch+var_34]
  0xba2ad4  call    sub_ABB2F0
  0xba2ad9  lea     ecx, [ebp+16h]
  0xba2adc  lea     eax, [ebp+2]
  0xba2adf  cmp     eax, ecx
  0xba2ae1  mov     [esp+48h+var_4], 0
  0xba2ae9  mov     [esp+48h+var_30], ebp
  0xba2aed  mov     dword ptr [esp+48h+var_2C], ecx
  0xba2af1  ja      loc_BA2D2B
  0xba2af7  lea     edx, [eax+4]
  0xba2afa  cmp     edx, ecx
  0xba2afc  mov     word ptr [ebp+0], 9370h
  0xba2b02  ja      loc_BA2D2B
  0xba2b08  mov     esi, [esp+48h+arg_0]
  0xba2b0c  mov     [eax], esi
  0xba2b0e  mov     eax, edx
  0xba2b10  lea     edx, [eax+4]
  0xba2b13  cmp     edx, ecx
  0xba2b15  ja      loc_BA2D2B
  0xba2b1b  mov     ecx, [esp+48h+arg_4]
  0xba2b1f  mov     [esp+48h+var_30], edx
  0xba2b23  lea     edx, [esp+48h+var_30]
  0xba2b27  mov     [eax], ecx
  0xba2b29  push    edx
  0xba2b2a  lea     eax, [esp+4Ch+arg_8]
  0xba2b2e  push    eax
  0xba2b2f  call    sub_B02D80
  0xba2b34  add     esp, 8
  0xba2b37  test    al, al
  0xba2b39  jz      loc_BA2D2B
  0xba2b3f  lea     ecx, [esp+48h+var_30]
  0xba2b43  push    ecx
  0xba2b44  lea     edx, [esp+4Ch+arg_C]
  0xba2b48  push    edx
  0xba2b49  call    sub_B02D80
  0xba2b4e  add     esp, 8
  0xba2b51  test    al, al
  0xba2b53  jz      loc_BA2D2B
  0xba2b59  lea     eax, [esp+48h+var_30]
  0xba2b5d  push    eax
  0xba2b5e  lea     ecx, [esp+4Ch+arg_10]
  0xba2b62  push    ecx
  0xba2b63  call    sub_B061C0
  0xba2b68  add     esp, 8
  0xba2b6b  test    al, al
  0xba2b6d  jz      loc_BA2D2B
  0xba2b73  mov     esi, [edi+813Ch]
  0xba2b79  test    esi, esi
  0xba2b7b  mov     ebx, [esp+48h+var_30]
  0xba2b7f  jz      loc_BA2CCC
  0xba2b85  lea     edx, [esp+48h+var_28]
  0xba2b89  push    edx
  0xba2b8a  call    sub_CA0CE0
  0xba2b8f  add     esp, 4
  0xba2b92  mov     ecx, [edi+8]
  0xba2b95  push    offset aProtoLoungeCli_568; ")<-_proto_lounge_client::send_clan_roka"...
  0xba2b9a  push    ecx
  0xba2b9b  push    offset aId; " (id:"
  0xba2ba0  push    eax
  0xba2ba1  push    esi
  0xba2ba2  mov     byte ptr [esp+5Ch+var_4], 1
  0xba2ba7  call    sub_B03020
  0xba2bac  add     esp, 8
  0xba2baf  push    eax
  0xba2bb0  call    sub_41D990
  0xba2bb5  add     esp, 8
  0xba2bb8  mov     ecx, eax
  0xba2bba  call    sub_ADC810
  0xba2bbf  push    eax
  0xba2bc0  call    sub_41D990
  0xba2bc5  add     esp, 8
  0xba2bc8  lea     ecx, [esp+48h+var_28]
  0xba2bcc  mov     byte ptr [esp+48h+var_4], 0
  0xba2bd1  call    sub_B02FF0
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。
> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B02B40`=写 NUL 串（其**紧邻之前的 `push N`** = 串槽预算）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xba2be0  push    offset aTreeId; "tree_id="
  0xba2c08  push    offset aNodeNo; "node_no="
  0xba2c30  push    offset aIdxNo; "idx_no="
  0xba2c58  push    offset aPointUse; "point_use="
  0xba2c7b  push    offset aIsSupply; "is_supply="
  0xba2c92  push    offset aByte; "]byte"
  0xba2c9c  push    offset asc_EDAD58; " ) ["
```

## 4. 发送去向切片

```asm
  0xba2cce  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xba2afc` | u16 |
| `tree_id` | `0xBA2B0C` | u32 |
| `node_no` | `0xBA2B27` | u32 |
| `idx_no` | `0xBA2B2F` | u32 |
| `point_use` | `0xBA2B49` | u32 |
| `is_supply` | `0xBA2B63` | u8 |
