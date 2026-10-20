# 汇编证据 —— CS-0x6BCD-battle-msma_AI_hate_control

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B3D210 @ `0xb3d210`（`0xb3d210`..`0xb3d44e`）
- 命令名字符串：`)<-_proto_battle_client::send_msma_AI_hate_control(` @ `0xee1298`
- opcode 写入：`0xb3d28c`
- 声明容量：`0xE`

## 2. 组包块切片（游标初始化 → 提交）

```asm
  0xb3d25a  mov     ebp, eax
  0xb3d25c  mov     eax, [edi+0Ch]
  0xb3d25f  push    eax
  0xb3d260  lea     ecx, [esp+4Ch+var_34]
  0xb3d264  call    sub_ABB2F0
  0xb3d269  lea     ecx, [ebp+0Eh]
  0xb3d26c  lea     eax, [ebp+2]
  0xb3d26f  cmp     eax, ecx
  0xb3d271  mov     [esp+48h+var_4], 0
  0xb3d279  mov     [esp+48h+var_30], ebp
  0xb3d27d  mov     dword ptr [esp+48h+var_2C], ecx
  0xb3d281  ja      loc_B3D439
  0xb3d287  lea     edx, [eax+2]
  0xb3d28a  cmp     edx, ecx
  0xb3d28c  mov     word ptr [ebp+0], 6BCDh
  0xb3d292  ja      loc_B3D439
  0xb3d298  mov     si, word ptr [esp+48h+arg_0]
  0xb3d29d  mov     [eax], si
  0xb3d2a0  mov     eax, edx
  0xb3d2a2  lea     edx, [eax+2]
  0xb3d2a5  cmp     edx, ecx
  0xb3d2a7  ja      loc_B3D439
  0xb3d2ad  mov     cx, word ptr [esp+48h+arg_4]
  0xb3d2b2  mov     [esp+48h+var_30], edx
  0xb3d2b6  lea     edx, [esp+48h+var_30]
  0xb3d2ba  mov     [eax], cx
  0xb3d2bd  push    edx
  0xb3d2be  lea     eax, [esp+4Ch+arg_8]
  0xb3d2c2  push    eax
  0xb3d2c3  call    sub_B02DA0
  0xb3d2c8  add     esp, 8
  0xb3d2cb  test    al, al
  0xb3d2cd  jz      loc_B3D439
  0xb3d2d3  mov     esi, [edi+3EF0h]
  0xb3d2d9  test    esi, esi
  0xb3d2db  mov     ebx, [esp+48h+var_30]
  0xb3d2df  jz      loc_B3D3DA
  0xb3d2e5  lea     ecx, [esp+48h+var_28]
  0xb3d2e9  push    ecx
  0xb3d2ea  call    sub_CA0CE0
  0xb3d2ef  add     esp, 4
  0xb3d2f2  mov     edx, [edi+8]
  0xb3d2f5  push    offset aProtoBattleCli_207; ")<-_proto_battle_client::send_msma_AI_h"...
  0xb3d2fa  push    edx
  0xb3d2fb  push    offset aId; " (id:"
  0xb3d300  push    eax
  0xb3d301  push    esi
  0xb3d302  mov     byte ptr [esp+5Ch+var_4], 1
  0xb3d307  call    sub_B03020
  0xb3d30c  add     esp, 8
  0xb3d30f  push    eax
  0xb3d310  call    sub_41D990
  0xb3d315  add     esp, 8
  0xb3d318  mov     ecx, eax
  0xb3d31a  call    sub_ADC810
  0xb3d31f  push    eax
  0xb3d320  call    sub_41D990
  0xb3d325  add     esp, 8
  0xb3d328  lea     ecx, [esp+48h+var_28]
  0xb3d32c  mov     byte ptr [esp+48h+var_4], 0
  0xb3d331  call    sub_B02FF0   <<<COMMIT
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb3d340  push    offset aAiEntId; "AI_ent_id="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb3d368  push    offset aTargetEntId; "target_ent_id="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb3d38b  push    offset aHateAdjust; "hate_adjust="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb3d3a0  push    offset aByte; "]byte"
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
```

## 4. 发送去向切片

```asm
  0xb3d3dc  mov     eax, [edx+58h]
  0xb3d3df  sub     ebx, ebp
  0xb3d3e1  push    ebx
  0xb3d3e2  push    ebp
  0xb3d3e3  mov     ecx, edi
  0xb3d3e5  call    eax
  0xb3d3e7  test    al, al
  0xb3d3e9  jz      short loc_B3D439
  0xb3d3eb  mov     eax, [edi+3BF0h]
  0xb3d3f1  test    eax, eax
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。
> 本批 50 条**全部命中同一去向槽 `vt[0x58]`**（与批次-16/17 一致）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB3D28C` | u16 |
| `AI_ent_id` | `0xB3D29D` | u16 |
| `target_ent_id` | `0xB3D2BA` | u16 |
| `hate_adjust` | `0xB3D2C3` | u16 |
