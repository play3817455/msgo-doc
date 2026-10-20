# 汇编证据 —— CS-0xE41F-lounge-pilot_module_unlock

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0x00B8C0C0`（`0x00B8C0C0`..`0x00B8C26A`），函数 `sub_B8C0C0`
- 命令名字符串：`)<-_proto_lounge_client::send_pilot_module_unlock(` @ `0x00EEA69C`
- opcode 写入：`0x00B8C134`
- 声明容量：`0x6`（分配器容量 `push` @ `0x00B8C106`）
- 提交（`sub_B02FF0`）：`0x00B8C1A0`
- 发送去向：`vt[0x58]` @ `0x00B8C1FB`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00B8C10F  push    eax
  00B8C110  lea     ecx, [esp+44h+var_2C]
  00B8C114  call    sub_ABB2F0   ; <<< 初始化 {cur,end}（游标自 buf+2 起）
  00B8C119  lea     ecx, [ebp+6]
  00B8C11C  lea     eax, [ebp+2]
  00B8C11F  cmp     eax, ecx
  00B8C121  mov     [esp+40h+var_4], 0
  00B8C129  ja      loc_B8C255
  00B8C12F  lea     ebx, [eax+4]
  00B8C132  cmp     ebx, ecx
  00B8C134  mov     word ptr [ebp+0], 0E41Fh   ; <<< 内联写线（u16）
  00B8C13A  ja      loc_B8C255
  00B8C140  mov     ecx, [esp+40h+arg_0]
  00B8C144  mov     [eax], ecx   ; <<< 内联写线（u32）
  00B8C146  mov     edi, [esi+7A84h]
  00B8C14C  test    edi, edi
  00B8C14E  jz      loc_B8C1F9
  00B8C154  lea     edx, [esp+40h+var_28]
  00B8C158  push    edx
  00B8C159  call    sub_CA0CE0
  00B8C15E  add     esp, 4
  00B8C161  mov     ecx, [esi+8]
  00B8C164  push    offset aProtoLoungeCli_426
  00B8C169  push    ecx
  00B8C16A  push    offset aId
  00B8C16F  push    eax
  00B8C170  push    edi
  00B8C171  mov     byte ptr [esp+54h+var_4], 1
  00B8C176  call    sub_B03020
  00B8C17B  add     esp, 8
  00B8C17E  push    eax
  00B8C17F  call    sub_41D990
  00B8C184  add     esp, 8
  00B8C187  mov     ecx, eax
  00B8C189  call    sub_ADC810
  00B8C18E  push    eax
  00B8C18F  call    sub_41D990
  00B8C194  add     esp, 8
  00B8C197  lea     ecx, [esp+40h+var_28]
  00B8C19B  mov     byte ptr [esp+40h+var_4], 0
  00B8C1A0  call    sub_B02FF0   ; <<< 提交（C→S 闭合点）
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00B8C1A0  call    sub_B02FF0
  00B8C1A5  mov     edx, [esp+40h+arg_0]
  00B8C1A9  push    edx
  00B8C1AA  push    offset aModuleId
  00B8C1AF  push    edi
  00B8C1B0  call    sub_41D990
  00B8C1B5  add     esp, 8
  00B8C1B8  mov     ecx, eax
  00B8C1BA  call    sub_B03580
  00B8C1BF  push    offset aByte
  00B8C1C4  mov     eax, ebx
  00B8C1C6  sub     eax, ebp
  00B8C1C8  push    eax
  00B8C1C9  push    offset asc_EDAD58
  00B8C1CE  push    edi
  00B8C1CF  call    sub_41D990
  00B8C1D4  add     esp, 8
  00B8C1D7  mov     ecx, eax
  00B8C1D9  call    sub_B03580
  00B8C1DE  push    eax
  00B8C1DF  call    sub_41D990
  00B8C1E4  add     esp, 8
  00B8C1E7  mov     edi, eax
  00B8C1E9  push    0Ah
  00B8C1EB  mov     ecx, edi
  00B8C1ED  call    sub_B036E0
  00B8C1F2  mov     ecx, edi
  00B8C1F4  call    sub_40DDF0
  00B8C1F9  mov     edx, [esi]
  00B8C1FB  mov     eax, [edx+58h]
```

## 4. 发送去向切片

```asm
  00B8C1F9  mov     edx, [esi]
  00B8C1FB  mov     eax, [edx+58h]
  00B8C1FE  sub     ebx, ebp
  00B8C200  push    ebx
  00B8C201  push    ebp
  00B8C202  mov     ecx, esi
  00B8C204  call    eax
  00B8C206  test    al, al
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `00B8C134` | u16 / 2 |
| `module_id` | `0xB8C144` | u32 / 4 |
