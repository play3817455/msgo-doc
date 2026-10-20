# 汇编证据 —— CS-0xDFC4-lounge-msma_adop_opened

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0x00BA6F00`（`0x00BA6F00`..`0x00BA7086`），函数 `sub_BA6F00`
- 命令名字符串：`)<-_proto_lounge_client::send_msma_adop_opened(` @ `0x00EED3C0`
- opcode 写入：`0x00BA6F59`
- 声明容量：`0x2`（分配器容量 `push` @ `0x00BA6F46`）
- 提交（`sub_B02FF0`）：`0x00BA6FC3`
- 发送去向：`vt[0x58]` @ `0x00BA7004`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00BA6F4F  push    eax
  00BA6F50  lea     ecx, [esp+44h+var_2C]
  00BA6F54  call    sub_ABB2F0   ; <<< 初始化 {cur,end}（游标自 buf+2 起）
  00BA6F59  mov     word ptr [edi], 0DFC4h   ; <<< 内联写线（u16）
  00BA6F5E  mov     ebp, [esi+82C0h]
  00BA6F64  test    ebp, ebp
  00BA6F66  mov     [esp+40h+var_4], 0
  00BA6F6E  lea     ebx, [edi+2]
  00BA6F71  jz      loc_BA7002
  00BA6F77  lea     ecx, [esp+40h+var_28]
  00BA6F7B  push    ecx
  00BA6F7C  call    sub_CA0CE0
  00BA6F81  add     esp, 4
  00BA6F84  mov     edx, [esi+8]
  00BA6F87  push    offset aProtoLoungeCli_589
  00BA6F8C  push    edx
  00BA6F8D  push    offset aId
  00BA6F92  push    eax
  00BA6F93  push    ebp
  00BA6F94  mov     byte ptr [esp+54h+var_4], 1
  00BA6F99  call    sub_B03020
  00BA6F9E  add     esp, 8
  00BA6FA1  push    eax
  00BA6FA2  call    sub_41D990
  00BA6FA7  add     esp, 8
  00BA6FAA  mov     ecx, eax
  00BA6FAC  call    sub_ADC810
  00BA6FB1  push    eax
  00BA6FB2  call    sub_41D990
  00BA6FB7  add     esp, 8
  00BA6FBA  lea     ecx, [esp+40h+var_28]
  00BA6FBE  mov     byte ptr [esp+40h+var_4], 0
  00BA6FC3  call    sub_B02FF0   ; <<< 提交（C→S 闭合点）
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00BA6FC3  call    sub_B02FF0
  00BA6FC8  push    offset aByte
  00BA6FCD  mov     eax, ebx
  00BA6FCF  sub     eax, edi
  00BA6FD1  push    eax
  00BA6FD2  push    offset asc_EDAD58
  00BA6FD7  push    ebp
  00BA6FD8  call    sub_41D990
  00BA6FDD  add     esp, 8
  00BA6FE0  mov     ecx, eax
  00BA6FE2  call    sub_B03580
  00BA6FE7  push    eax
  00BA6FE8  call    sub_41D990
  00BA6FED  add     esp, 8
  00BA6FF0  mov     ebp, eax
  00BA6FF2  push    0Ah
  00BA6FF4  mov     ecx, ebp
  00BA6FF6  call    sub_B036E0
  00BA6FFB  mov     ecx, ebp
  00BA6FFD  call    sub_40DDF0
  00BA7002  mov     edx, [esi]
  00BA7004  mov     eax, [edx+58h]
```

## 4. 发送去向切片

```asm
  00BA7002  mov     edx, [esi]
  00BA7004  mov     eax, [edx+58h]
  00BA7007  sub     ebx, edi
  00BA7009  push    ebx
  00BA700A  push    edi
  00BA700B  mov     ecx, esi
  00BA700D  call    eax
  00BA700F  test    al, al
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `00BA6F59` | u16 / 2 |
