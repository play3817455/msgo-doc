# 汇编证据 —— CS-0x3B8F-auth-overplay_resettime_get

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B05C10 @ `0x00b05c10`（`0x00b05c10`..`0x00b05d90`）
- 命令名字符串：`)<-_proto_auth_client::send_overplay_resettime_get(` @ `0xedb11c`
- 声明容量：`0x2`（分配器指纹 @ `0xB05C53`）

## 2. 组包块切片（游标初始化 → 提交）

```asm
00B05C61  call sub_ABB2F0
00B05C66  mov word ptr [edi], 3B8Fh
00B05C6B  mov ebp, [esi+3C0h]
00B05C71  test ebp, ebp
00B05C73  mov [esp+40h+var_4], 0
00B05C7B  lea ebx, [edi+2]
00B05C7E  jz loc_B05D0F
00B05C84  lea ecx, [esp+40h+var_28]
00B05C88  push ecx
00B05C89  call sub_CA0CE0
00B05C8E  add esp, 4
00B05C91  mov edx, [esi+8]
00B05C94  push offset aProtoAuthClien; ")<-_proto_auth_client::send_overplay_re"...
00B05C99  push edx
00B05C9A  push offset aId; " (id:"
00B05C9F  push eax
00B05CA0  push ebp
00B05CA1  mov byte ptr [esp+54h+var_4], 1
00B05CA6  call sub_B03020
00B05CAB  add esp, 8
00B05CAE  push eax
00B05CAF  call sub_41D990
00B05CB4  add esp, 8
00B05CB7  mov ecx, eax
00B05CB9  call sub_ADC810
00B05CBE  push eax
00B05CBF  call sub_41D990
00B05CC4  add esp, 8
00B05CC7  lea ecx, [esp+40h+var_28]
00B05CCB  mov byte ptr [esp+40h+var_4], 0
```

## 3. 发送去向切片（提交之后的实际发送）

```asm
00B05D08  mov ecx, ebp
00B05D0A  call sub_40DDF0
00B05D0F  mov edx, [esi]
00B05D11  mov eax, [edx+58h]
00B05D14  sub ebx, edi
00B05D16  push ebx
00B05D17  push edi
00B05D18  mov ecx, esi
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB05C66` | u16（2 字节） |
