# 汇编证据 —— CS-0x3F68-lounge-pilot_tutorial_step_next

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B8AFF0 @ `0x00b8aff0`（`0x00b8aff0`..`0x00b8b197`）
- 命令名字符串：`)<-_proto_lounge_client::send_pilot_tutorial_step_next(` @ `0xeea498`
- 声明容量：`0x6`（分配器指纹 @ `0xB8B033`）

## 2. 组包块切片（游标初始化 → 提交）

```asm
00B8B041  call sub_ABB2F0
00B8B046  lea ecx, [ebp+6]
00B8B049  lea eax, [ebp+2]
00B8B04C  cmp eax, ecx
00B8B04E  mov [esp+40h+var_4], 0
00B8B056  ja loc_B8B182
00B8B05C  lea ebx, [eax+4]
00B8B05F  cmp ebx, ecx
00B8B061  mov word ptr [ebp+0], 3F68h
00B8B067  ja loc_B8B182
00B8B06D  mov ecx, [esp+40h+arg_0]
00B8B071  mov [eax], ecx
00B8B073  mov edi, [esi+7A28h]
00B8B079  test edi, edi
00B8B07B  jz loc_B8B126
00B8B081  lea edx, [esp+40h+var_28]
00B8B085  push edx
00B8B086  call sub_CA0CE0
00B8B08B  add esp, 4
00B8B08E  mov ecx, [esi+8]
00B8B091  push offset aProtoLoungeCli_352; ")<-_proto_lounge_client::send_pilot_tut"...
00B8B096  push ecx
00B8B097  push offset aId; " (id:"
00B8B09C  push eax
00B8B09D  push edi
00B8B09E  mov byte ptr [esp+54h+var_4], 1
00B8B0A3  call sub_B03020
00B8B0A8  add esp, 8
00B8B0AB  push eax
00B8B0AC  call sub_41D990
00B8B0B1  add esp, 8
00B8B0B4  mov ecx, eax
00B8B0B6  call sub_ADC810
00B8B0BB  push eax
00B8B0BC  call sub_41D990
00B8B0C1  add esp, 8
00B8B0C4  lea ecx, [esp+40h+var_28]
00B8B0C8  mov byte ptr [esp+40h+var_4], 0
```

## 3. 发送去向切片（提交之后的实际发送）

```asm
00B8B11F  mov ecx, edi
00B8B121  call sub_40DDF0
00B8B126  mov edx, [esi]
00B8B128  mov eax, [edx+58h]
00B8B12B  sub ebx, ebp
00B8B12D  push ebx
00B8B12E  push ebp
00B8B12F  mov ecx, esi
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB8B061` | u16（2 字节） |
| `tuto_step_now` | `0xB8B071` | u32（4 字节） |
