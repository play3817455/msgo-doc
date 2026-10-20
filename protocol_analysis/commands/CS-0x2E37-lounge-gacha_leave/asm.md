# 汇编证据 —— CS-0x2E37-lounge-gacha_leave

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B9DB10 @ `0x00b9db10`（`0x00b9db10`..`0x00b9dc96`）
- 命令名字符串：`)<-_proto_lounge_client::send_gacha_leave(` @ `0xeec468`
- 声明容量：`0x2`（分配器指纹 @ `0xB9DB56`）

## 2. 组包块切片（游标初始化 → 提交）

```asm
00B9DB64  call sub_ABB2F0
00B9DB69  mov word ptr [edi], 2E37h
00B9DB6E  mov ebp, [esi+7FD8h]
00B9DB74  test ebp, ebp
00B9DB76  mov [esp+40h+var_4], 0
00B9DB7E  lea ebx, [edi+2]
00B9DB81  jz loc_B9DC12
00B9DB87  lea ecx, [esp+40h+var_28]
00B9DB8B  push ecx
00B9DB8C  call sub_CA0CE0
00B9DB91  add esp, 4
00B9DB94  mov edx, [esi+8]
00B9DB97  push offset aProtoLoungeCli_534; ")<-_proto_lounge_client::send_gacha_lea"...
00B9DB9C  push edx
00B9DB9D  push offset aId; " (id:"
00B9DBA2  push eax
00B9DBA3  push ebp
00B9DBA4  mov byte ptr [esp+54h+var_4], 1
00B9DBA9  call sub_B03020
00B9DBAE  add esp, 8
00B9DBB1  push eax
00B9DBB2  call sub_41D990
00B9DBB7  add esp, 8
00B9DBBA  mov ecx, eax
00B9DBBC  call sub_ADC810
00B9DBC1  push eax
00B9DBC2  call sub_41D990
00B9DBC7  add esp, 8
00B9DBCA  lea ecx, [esp+40h+var_28]
00B9DBCE  mov byte ptr [esp+40h+var_4], 0
```

## 3. 发送去向切片（提交之后的实际发送）

```asm
00B9DC0B  mov ecx, ebp
00B9DC0D  call sub_40DDF0
00B9DC12  mov edx, [esi]
00B9DC14  mov eax, [edx+58h]
00B9DC17  sub ebx, edi
00B9DC19  push ebx
00B9DC1A  push edi
00B9DC1B  mov ecx, esi
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB9DB69` | u16（2 字节） |
