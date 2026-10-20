# 汇编证据 —— CS-0x4E38-lounge-msma_over_custom_buildup

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_BA7EE0 @ `0xba7ee0`（`0xba7ee0`..`0xba80ed`）
- 命令名字符串：`)<-_proto_lounge_client::send_msma_over_custom_buildup(` @ `0xeed5d0`
- opcode 写入：`0xba7f5c`
- 声明容量：`0x36`

## 2. 组包块切片（游标初始化 → 提交）

```asm
  0xba7f2a  mov     ebp, eax
  0xba7f2c  mov     eax, [edi+0Ch]
  0xba7f2f  push    eax
  0xba7f30  lea     ecx, [esp+4Ch+var_34]
  0xba7f34  call    sub_ABB2F0
  0xba7f39  lea     ecx, [ebp+36h]
  0xba7f3c  lea     eax, [ebp+2]
  0xba7f3f  cmp     eax, ecx
  0xba7f41  mov     [esp+48h+var_4], 0
  0xba7f49  mov     [esp+48h+var_30], ebp
  0xba7f4d  mov     dword ptr [esp+48h+var_2C], ecx
  0xba7f51  ja      loc_BA80D8
  0xba7f57  lea     edx, [eax+8]
  0xba7f5a  cmp     edx, ecx
  0xba7f5c  mov     word ptr [ebp+0], 4E38h
  0xba7f62  ja      loc_BA80D8
  0xba7f68  mov     ecx, [esp+48h+arg_0]
  0xba7f6c  mov     [eax], ecx
  0xba7f6e  mov     ecx, [esp+48h+arg_4]
  0xba7f72  mov     [esp+48h+var_30], edx
  0xba7f76  lea     edx, [esp+48h+var_30]
  0xba7f7a  mov     [eax+4], ecx
  0xba7f7d  mov     eax, [esp+48h+arg_8]
  0xba7f81  push    edx
  0xba7f82  push    eax
  0xba7f83  call    sub_B41DA0
  0xba7f88  add     esp, 8
  0xba7f8b  test    al, al
  0xba7f8d  jz      loc_BA80D8
  0xba7f93  mov     esi, [edi+832Ch]
  0xba7f99  test    esi, esi
  0xba7f9b  mov     ebx, [esp+48h+var_30]
  0xba7f9f  jz      loc_BA8079
  0xba7fa5  lea     ecx, [esp+48h+var_28]
  0xba7fa9  push    ecx
  0xba7faa  call    sub_CA0CE0
  0xba7faf  add     esp, 4
  0xba7fb2  mov     edx, [edi+8]
  0xba7fb5  push    offset aProtoLoungeCli_464; ")<-_proto_lounge_client::send_msma_over"...
  0xba7fba  push    edx
  0xba7fbb  push    offset aId; " (id:"
  0xba7fc0  push    eax
  0xba7fc1  push    esi
  0xba7fc2  mov     byte ptr [esp+5Ch+var_4], 1
  0xba7fc7  call    sub_B03020
  0xba7fcc  add     esp, 8
  0xba7fcf  push    eax
  0xba7fd0  call    sub_41D990
  0xba7fd5  add     esp, 8
  0xba7fd8  mov     ecx, eax
  0xba7fda  call    sub_ADC810
  0xba7fdf  push    eax
  0xba7fe0  call    sub_41D990
  0xba7fe5  add     esp, 8
  0xba7fe8  lea     ecx, [esp+48h+var_28]
  0xba7fec  mov     byte ptr [esp+48h+var_4], 0
  0xba7ff1  call    sub_B02FF0   <<<COMMIT
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xba8005  push    offset aUniqMsid; "uniq_msid="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xba8028  push    offset aBuildupInfo; "buildup_info="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xba803f  push    offset aByte; "]byte"
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
```

## 4. 发送去向切片

```asm
  0xba807b  mov     eax, [edx+58h]
  0xba807e  sub     ebx, ebp
  0xba8080  push    ebx
  0xba8081  push    ebp
  0xba8082  mov     ecx, edi
  0xba8084  call    eax
  0xba8086  test    al, al
  0xba8088  jz      short loc_BA80D8
  0xba808a  mov     eax, [edi+79A8h]
  0xba8090  test    eax, eax
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。
> 本批 50 条**全部命中同一去向槽 `vt[0x58]`**（与批次-16/17 一致）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xBA7F5C` | u16 |
| `uniq_msid` | `0xBA7F6C` | u64 |
| `buildup_info` | `0xBA7F83` | struct |
