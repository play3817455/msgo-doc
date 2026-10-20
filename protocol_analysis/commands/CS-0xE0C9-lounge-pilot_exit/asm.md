# 汇编证据 —— CS-0xE0C9-lounge-pilot_exit

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0x00B8AB70`（`0x00B8AB70`..`0x00B8ACF0`），函数 `sub_B8AB70`
- 命令名字符串：`)<-_proto_lounge_client::send_pilot_exit(` @ `0x00EEA400`
- opcode 写入：`0x00B8ABC6`
- 声明容量：`0x2`（分配器容量 `push` @ `0x00B8ABB3`）
- 提交（`sub_B02FF0`）：`0x00B8AC30`
- 发送去向：`vt[0x58]` @ `0x00B8AC71`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00B8ABBC  push    eax
  00B8ABBD  lea     ecx, [esp+44h+var_2C]
  00B8ABC1  call    sub_ABB2F0   ; <<< 初始化 {cur,end}（游标自 buf+2 起）
  00B8ABC6  mov     word ptr [edi], 0E0C9h   ; <<< 内联写线（u16）
  00B8ABCB  mov     ebp, [esi+7A10h]
  00B8ABD1  test    ebp, ebp
  00B8ABD3  mov     [esp+40h+var_4], 0
  00B8ABDB  lea     ebx, [edi+2]
  00B8ABDE  jz      loc_B8AC6F
  00B8ABE4  lea     ecx, [esp+40h+var_28]
  00B8ABE8  push    ecx
  00B8ABE9  call    sub_CA0CE0
  00B8ABEE  add     esp, 4
  00B8ABF1  mov     edx, [esi+8]
  00B8ABF4  push    offset aProtoLoungeCli_360
  00B8ABF9  push    edx
  00B8ABFA  push    offset aId
  00B8ABFF  push    eax
  00B8AC00  push    ebp
  00B8AC01  mov     byte ptr [esp+54h+var_4], 1
  00B8AC06  call    sub_B03020
  00B8AC0B  add     esp, 8
  00B8AC0E  push    eax
  00B8AC0F  call    sub_41D990
  00B8AC14  add     esp, 8
  00B8AC17  mov     ecx, eax
  00B8AC19  call    sub_ADC810
  00B8AC1E  push    eax
  00B8AC1F  call    sub_41D990
  00B8AC24  add     esp, 8
  00B8AC27  lea     ecx, [esp+40h+var_28]
  00B8AC2B  mov     byte ptr [esp+40h+var_4], 0
  00B8AC30  call    sub_B02FF0   ; <<< 提交（C→S 闭合点）
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00B8AC30  call    sub_B02FF0
  00B8AC35  push    offset aByte
  00B8AC3A  mov     eax, ebx
  00B8AC3C  sub     eax, edi
  00B8AC3E  push    eax
  00B8AC3F  push    offset asc_EDAD58
  00B8AC44  push    ebp
  00B8AC45  call    sub_41D990
  00B8AC4A  add     esp, 8
  00B8AC4D  mov     ecx, eax
  00B8AC4F  call    sub_B03580
  00B8AC54  push    eax
  00B8AC55  call    sub_41D990
  00B8AC5A  add     esp, 8
  00B8AC5D  mov     ebp, eax
  00B8AC5F  push    0Ah
  00B8AC61  mov     ecx, ebp
  00B8AC63  call    sub_B036E0
  00B8AC68  mov     ecx, ebp
  00B8AC6A  call    sub_40DDF0
  00B8AC6F  mov     edx, [esi]
  00B8AC71  mov     eax, [edx+58h]
```

## 4. 发送去向切片

```asm
  00B8AC6F  mov     edx, [esi]
  00B8AC71  mov     eax, [edx+58h]
  00B8AC74  sub     ebx, edi
  00B8AC76  push    ebx
  00B8AC77  push    edi
  00B8AC78  mov     ecx, esi
  00B8AC7A  call    eax
  00B8AC7C  test    al, al
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `00B8ABC6` | u16 / 2 |
