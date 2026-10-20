# 汇编证据 —— CS-0x6007-battle-wrestle_chase_move_end

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B40F20 @ `0xb40f20`（`0xb40f20`..`0xb41108`）
- 命令名字符串：`)<-_proto_battle_client::send_wrestle_chase_move_end(` @ `0xee191c`
- opcode 写入：`0xb40f94`
- 声明容量：`0xA`

## 2. 组包块切片（游标初始化 → 提交）

```asm
  0xb40f6a  mov     ebp, eax
  0xb40f6c  mov     eax, [edi+0Ch]
  0xb40f6f  push    eax
  0xb40f70  lea     ecx, [esp+44h+var_2C]
  0xb40f74  call    sub_ABB2F0
  0xb40f79  lea     eax, [ebp+0Ah]
  0xb40f7c  lea     ecx, [ebp+2]
  0xb40f7f  cmp     ecx, eax
  0xb40f81  mov     [esp+40h+var_4], 0
  0xb40f89  ja      loc_B410F3
  0xb40f8f  lea     edx, [ecx+4]
  0xb40f92  cmp     edx, eax
  0xb40f94  mov     word ptr [ebp+0], 6007h
  0xb40f9a  ja      loc_B410F3
  0xb40fa0  mov     esi, [esp+40h+arg_0]
  0xb40fa4  lea     ebx, [edx+2]
  0xb40fa7  cmp     ebx, eax
  0xb40fa9  mov     [ecx], esi
  0xb40fab  ja      loc_B410F3
  0xb40fb1  mov     cx, word ptr [esp+40h+arg_4]
  0xb40fb6  mov     [edx], cx
  0xb40fb9  mov     esi, [edi+40A8h]
  0xb40fbf  test    esi, esi
  0xb40fc1  jz      loc_B41094
  0xb40fc7  lea     edx, [esp+40h+var_28]
  0xb40fcb  push    edx
  0xb40fcc  call    sub_CA0CE0
  0xb40fd1  add     esp, 4
  0xb40fd4  mov     ecx, [edi+8]
  0xb40fd7  push    offset aProtoBattleCli_234; ")<-_proto_battle_client::send_wrestle_c"...
  0xb40fdc  push    ecx
  0xb40fdd  push    offset aId; " (id:"
  0xb40fe2  push    eax
  0xb40fe3  push    esi
  0xb40fe4  mov     byte ptr [esp+54h+var_4], 1
  0xb40fe9  call    sub_B03020
  0xb40fee  add     esp, 8
  0xb40ff1  push    eax
  0xb40ff2  call    sub_41D990
  0xb40ff7  add     esp, 8
  0xb40ffa  mov     ecx, eax
  0xb40ffc  call    sub_ADC810
  0xb41001  push    eax
  0xb41002  call    sub_41D990
  0xb41007  add     esp, 8
  0xb4100a  lea     ecx, [esp+40h+var_28]
  0xb4100e  mov     byte ptr [esp+40h+var_4], 0
  0xb41013  call    sub_B02FF0   <<<COMMIT
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb41022  push    offset aFrameCount; "frame_count="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb41045  push    offset aAiEntId; "AI_ent_id="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb4105a  push    offset aByte; "]byte"
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
```

## 4. 发送去向切片

```asm
  0xb41096  mov     eax, [edx+58h]
  0xb41099  sub     ebx, ebp
  0xb4109b  push    ebx
  0xb4109c  push    ebp
  0xb4109d  mov     ecx, edi
  0xb4109f  call    eax
  0xb410a1  test    al, al
  0xb410a3  jz      short loc_B410F3
  0xb410a5  mov     eax, [edi+3BF0h]
  0xb410ab  test    eax, eax
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。
> 本批 50 条**全部命中同一去向槽 `vt[0x58]`**（与批次-16/17 一致）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB40F94` | u16 |
| `frame_count` | `0xB40FA9` | u32 |
| `AI_ent_id` | `0xB40FB6` | u16 |
