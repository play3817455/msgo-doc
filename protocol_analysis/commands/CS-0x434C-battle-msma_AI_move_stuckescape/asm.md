# 汇编证据 —— CS-0x434C-battle-msma_AI_move_stuckescape

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B3D600 @ `0x00b3d600`（`0x00b3d600`..`0x00b3d8c2`）
- 命令名字符串：`)<-_proto_battle_client::send_msma_AI_move_stuckescape(` @ `0xee1308`
- 声明容量：`0x16`（分配器指纹 @ `0xB3D646`）

## 2. 组包块切片（游标初始化 → 提交）

```asm
00B3D654  call sub_ABB2F0
00B3D659  lea ecx, [ebp+16h]
00B3D65C  lea eax, [ebp+2]
00B3D65F  cmp eax, ecx
00B3D661  mov [esp+48h+var_4], 0
00B3D669  mov [esp+48h+var_30], ebp
00B3D66D  mov dword ptr [esp+48h+var_2C], ecx
00B3D671  ja loc_B3D8AD
00B3D677  lea edx, [eax+2]
00B3D67A  cmp edx, ecx
00B3D67C  mov word ptr [ebp+0], 434Ch
00B3D682  ja loc_B3D8AD
00B3D688  mov si, word ptr [esp+48h+arg_0]
00B3D68D  mov [eax], si
00B3D690  mov eax, edx
00B3D692  lea edx, [eax+2]
00B3D695  cmp edx, ecx
00B3D697  ja loc_B3D8AD
00B3D69D  mov cx, word ptr [esp+48h+arg_4]
00B3D6A2  mov [esp+48h+var_30], edx
00B3D6A6  lea edx, [esp+48h+var_30]
00B3D6AA  mov [eax], cx
00B3D6AD  push edx
00B3D6AE  lea eax, [esp+4Ch+arg_8]
00B3D6B2  push eax
00B3D6B3  call sub_B02DA0
00B3D6B8  add esp, 8
00B3D6BB  test al, al
00B3D6BD  jz loc_B3D8AD
00B3D6C3  lea ecx, [esp+48h+var_30]
00B3D6C7  push ecx
00B3D6C8  lea edx, [esp+4Ch+arg_C]
00B3D6CC  push edx
00B3D6CD  call sub_B02DA0
00B3D6D2  add esp, 8
00B3D6D5  test al, al
00B3D6D7  jz loc_B3D8AD
00B3D6DD  lea eax, [esp+48h+var_30]
00B3D6E1  push eax
00B3D6E2  lea ecx, [esp+4Ch+arg_10]
00B3D6E6  push ecx
00B3D6E7  call sub_B02DA0
00B3D6EC  add esp, 8
00B3D6EF  test al, al
00B3D6F1  jz loc_B3D8AD
00B3D6F7  mov esi, [edi+3F0Ch]
00B3D6FD  test esi, esi
00B3D6FF  mov ebx, [esp+48h+var_30]
00B3D703  jz loc_B3D84E
00B3D709  lea edx, [esp+48h+var_28]
00B3D70D  push edx
00B3D70E  call sub_CA0CE0
00B3D713  add esp, 4
00B3D716  mov ecx, [edi+8]
00B3D719  push offset aProtoBattleCli_268; ")<-_proto_battle_client::send_msma_AI_m"...
00B3D71E  push ecx
00B3D71F  push offset aId; " (id:"
00B3D724  push eax
00B3D725  push esi
00B3D726  mov byte ptr [esp+5Ch+var_4], 1
00B3D72B  call sub_B03020
00B3D730  add esp, 8
00B3D733  push eax
00B3D734  call sub_41D990
00B3D739  add esp, 8
00B3D73C  mov ecx, eax
00B3D73E  call sub_ADC810
00B3D743  push eax
00B3D744  call sub_41D990
00B3D749  add esp, 8
00B3D74C  lea ecx, [esp+48h+var_28]
00B3D750  mov byte ptr [esp+48h+var_4], 0
```

## 3. 发送去向切片（提交之后的实际发送）

```asm
00B3D847  mov ecx, esi
00B3D849  call sub_40DDF0
00B3D84E  mov edx, [edi]
00B3D850  mov eax, [edx+58h]
00B3D853  sub ebx, ebp
00B3D855  push ebx
00B3D856  push ebp
00B3D857  mov ecx, edi
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB3D67C` | u16（2 字节） |
| `AI_ent_id` | `0xB3D68D` | u16（2 字节） |
| `to_x` | `0xB3D6AA` | u16（2 字节） |
| `to_y` | `0xB3D6B3` | u16（2 字节） |
| `to_z` | `0xB3D6CD` | u16（2 字节） |
| `msec` | `0xB3D6E7` | u16（2 字节） |
