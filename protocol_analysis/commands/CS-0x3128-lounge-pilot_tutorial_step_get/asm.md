# 汇编证据 —— CS-0x3128-lounge-pilot_tutorial_step_get

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B8ACF0 @ `0x00b8acf0`（`0x00b8acf0`..`0x00b8ae70`）
- 命令名字符串：`)<-_proto_lounge_client::send_pilot_tutorial_step_get(` @ `0xeea42c`
- 声明容量：`0x2`（分配器指纹 @ `0xB8AD33`）

## 2. 组包块切片（游标初始化 → 提交）

```asm
00B8AD41  call sub_ABB2F0
00B8AD46  mov word ptr [edi], 3128h
00B8AD4B  mov ebp, [esi+7A18h]
00B8AD51  test ebp, ebp
00B8AD53  mov [esp+40h+var_4], 0
00B8AD5B  lea ebx, [edi+2]
00B8AD5E  jz loc_B8ADEF
00B8AD64  lea ecx, [esp+40h+var_28]
00B8AD68  push ecx
00B8AD69  call sub_CA0CE0
00B8AD6E  add esp, 4
00B8AD71  mov edx, [esi+8]
00B8AD74  push offset aProtoLoungeCli_356; ")<-_proto_lounge_client::send_pilot_tut"...
00B8AD79  push edx
00B8AD7A  push offset aId; " (id:"
00B8AD7F  push eax
00B8AD80  push ebp
00B8AD81  mov byte ptr [esp+54h+var_4], 1
00B8AD86  call sub_B03020
00B8AD8B  add esp, 8
00B8AD8E  push eax
00B8AD8F  call sub_41D990
00B8AD94  add esp, 8
00B8AD97  mov ecx, eax
00B8AD99  call sub_ADC810
00B8AD9E  push eax
00B8AD9F  call sub_41D990
00B8ADA4  add esp, 8
00B8ADA7  lea ecx, [esp+40h+var_28]
00B8ADAB  mov byte ptr [esp+40h+var_4], 0
```

## 3. 发送去向切片（提交之后的实际发送）

```asm
00B8ADE8  mov ecx, ebp
00B8ADEA  call sub_40DDF0
00B8ADEF  mov edx, [esi]
00B8ADF1  mov eax, [edx+58h]
00B8ADF4  sub ebx, edi
00B8ADF6  push ebx
00B8ADF7  push edi
00B8ADF8  mov ecx, esi
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB8AD46` | u16（2 字节） |
