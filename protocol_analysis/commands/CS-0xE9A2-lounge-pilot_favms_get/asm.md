# 汇编证据 —— CS-0xE9A2-lounge-pilot_favms_get

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0x00B8E4D0`（`0x00B8E4D0`..`0x00B8E6B3`），函数 `sub_B8E4D0`
- 命令名字符串：`)<-_proto_lounge_client::send_pilot_favms_get(` @ `0x00EEAAC4`
- opcode 写入：`0x00B8E544`
- 声明容量：`0xA`（分配器容量 `push` @ `0x00B8E516`）
- 提交（`sub_B02FF0`）：`0x00B8E5C1`
- 发送去向：`vt[0x58]` @ `0x00B8E644`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00B8E51F  push    eax
  00B8E520  lea     ecx, [esp+44h+var_2C]
  00B8E524  call    sub_ABB2F0   ; <<< 初始化 {cur,end}（游标自 buf+2 起）
  00B8E529  lea     ecx, [ebp+0Ah]
  00B8E52C  lea     eax, [ebp+2]
  00B8E52F  cmp     eax, ecx
  00B8E531  mov     [esp+40h+var_4], 0
  00B8E539  ja      loc_B8E69E
  00B8E53F  lea     edx, [eax+4]
  00B8E542  cmp     edx, ecx
  00B8E544  mov     word ptr [ebp+0], 0E9A2h   ; <<< 内联写线（u16）
  00B8E54A  ja      loc_B8E69E
  00B8E550  mov     esi, [esp+40h+arg_0]
  00B8E554  lea     ebx, [edx+4]
  00B8E557  cmp     ebx, ecx
  00B8E559  mov     [eax], esi   ; <<< 内联写线（u32）
  00B8E55B  ja      loc_B8E69E
  00B8E561  mov     ecx, [esp+40h+arg_4]
  00B8E565  mov     [edx], ecx   ; <<< 内联写线（u32）
  00B8E567  mov     esi, [edi+7B54h]
  00B8E56D  test    esi, esi
  00B8E56F  jz      loc_B8E642
  00B8E575  lea     edx, [esp+40h+var_28]
  00B8E579  push    edx
  00B8E57A  call    sub_CA0CE0
  00B8E57F  add     esp, 4
  00B8E582  mov     ecx, [edi+8]
  00B8E585  push    offset aProtoLoungeCli_363
  00B8E58A  push    ecx
  00B8E58B  push    offset aId
  00B8E590  push    eax
  00B8E591  push    esi
  00B8E592  mov     byte ptr [esp+54h+var_4], 1
  00B8E597  call    sub_B03020
  00B8E59C  add     esp, 8
  00B8E59F  push    eax
  00B8E5A0  call    sub_41D990
  00B8E5A5  add     esp, 8
  00B8E5A8  mov     ecx, eax
  00B8E5AA  call    sub_ADC810
  00B8E5AF  push    eax
  00B8E5B0  call    sub_41D990
  00B8E5B5  add     esp, 8
  00B8E5B8  lea     ecx, [esp+40h+var_28]
  00B8E5BC  mov     byte ptr [esp+40h+var_4], 0
  00B8E5C1  call    sub_B02FF0   ; <<< 提交（C→S 闭合点）
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00B8E5C1  call    sub_B02FF0
  00B8E5C6  mov     edx, [esp+40h+arg_0]
  00B8E5CA  push    offset word_F641DC
  00B8E5CF  push    edx
  00B8E5D0  push    offset aPilotId
  00B8E5D5  push    esi
  00B8E5D6  call    sub_41D990
  00B8E5DB  add     esp, 8
  00B8E5DE  mov     ecx, eax
  00B8E5E0  call    sub_B03580
  00B8E5E5  push    eax
  00B8E5E6  call    sub_41D990
  00B8E5EB  mov     eax, [esp+48h+arg_4]
  00B8E5EF  add     esp, 8
  00B8E5F2  push    eax
  00B8E5F3  push    offset aWorldId
  00B8E5F8  push    esi
  00B8E5F9  call    sub_41D990
  00B8E5FE  add     esp, 8
  00B8E601  mov     ecx, eax
  00B8E603  call    sub_B03580
  00B8E608  push    offset aByte
  00B8E60D  mov     ecx, ebx
  00B8E60F  sub     ecx, ebp
  00B8E611  push    ecx
  00B8E612  push    offset asc_EDAD58
  00B8E617  push    esi
  00B8E618  call    sub_41D990
  00B8E61D  add     esp, 8
  00B8E620  mov     ecx, eax
  00B8E622  call    sub_B03580
  00B8E627  push    eax
  00B8E628  call    sub_41D990
  00B8E62D  add     esp, 8
  00B8E630  mov     esi, eax
  00B8E632  push    0Ah
  00B8E634  mov     ecx, esi
  00B8E636  call    sub_B036E0
  00B8E63B  mov     ecx, esi
  00B8E63D  call    sub_40DDF0
  00B8E642  mov     edx, [edi]
  00B8E644  mov     eax, [edx+58h]
```

## 4. 发送去向切片

```asm
  00B8E642  mov     edx, [edi]
  00B8E644  mov     eax, [edx+58h]
  00B8E647  sub     ebx, ebp
  00B8E649  push    ebx
  00B8E64A  push    ebp
  00B8E64B  mov     ecx, edi
  00B8E64D  call    eax
  00B8E64F  test    al, al
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `00B8E544` | u16 / 2 |
| `pilot_id` | `0xB8E559` | u32 / 4 |
| `world_id` | `0xB8E565` | u32 / 4 |
