# 汇编证据 —— CS-0x2EE8-lounge-pilot_dailyrecord_collect_complete

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B8E850 @ `0x00b8e850`（`0x00b8e850`..`0x00b8e9d3`）
- 命令名字符串：`)<-_proto_lounge_client::send_pilot_dailyrecord_collect_complete(` @ `0xeeab30`
- 声明容量：`0x2`（分配器指纹 @ `0xB8E896`）

## 2. 组包块切片（游标初始化 → 提交）

```asm
00B8E8A4  call sub_ABB2F0
00B8E8A9  mov word ptr [edi], 2EE8h
00B8E8AE  mov ebp, [esi+7B68h]
00B8E8B4  test ebp, ebp
00B8E8B6  mov [esp+40h+var_4], 0
00B8E8BE  lea ebx, [edi+2]
00B8E8C1  jz loc_B8E952
00B8E8C7  lea ecx, [esp+40h+var_28]
00B8E8CB  push ecx
00B8E8CC  call sub_CA0CE0
00B8E8D1  add esp, 4
00B8E8D4  mov edx, [esi+8]
00B8E8D7  push offset aProtoLoungeCli_520; ")<-_proto_lounge_client::send_pilot_dai"...
00B8E8DC  push edx
00B8E8DD  push offset aId; " (id:"
00B8E8E2  push eax
00B8E8E3  push ebp
00B8E8E4  mov byte ptr [esp+54h+var_4], 1
00B8E8E9  call sub_B03020
00B8E8EE  add esp, 8
00B8E8F1  push eax
00B8E8F2  call sub_41D990
00B8E8F7  add esp, 8
00B8E8FA  mov ecx, eax
00B8E8FC  call sub_ADC810
00B8E901  push eax
00B8E902  call sub_41D990
00B8E907  add esp, 8
00B8E90A  lea ecx, [esp+40h+var_28]
00B8E90E  mov byte ptr [esp+40h+var_4], 0
```

## 3. 发送去向切片（提交之后的实际发送）

```asm
00B8E94B  mov ecx, ebp
00B8E94D  call sub_40DDF0
00B8E952  mov edx, [esi]
00B8E954  mov eax, [edx+58h]
00B8E957  sub ebx, edi
00B8E959  push ebx
00B8E95A  push edi
00B8E95B  mov ecx, esi
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB8E8A9` | u16（2 字节） |
