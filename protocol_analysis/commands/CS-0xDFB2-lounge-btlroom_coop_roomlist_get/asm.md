# 汇编证据 —— CS-0xDFB2-lounge-btlroom_coop_roomlist_get

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0x00B90B70`（`0x00B90B70`..`0x00B90CF6`），函数 `sub_B90B70`
- 命令名字符串：`)<-_proto_lounge_client::send_btlroom_coop_roomlist_get(` @ `0x00EEAF34`
- opcode 写入：`0x00B90BC9`
- 声明容量：`0x2`（分配器容量 `push` @ `0x00B90BB6`）
- 提交（`sub_B02FF0`）：`0x00B90C33`
- 发送去向：`vt[0x58]` @ `0x00B90C74`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00B90BBF  push    eax
  00B90BC0  lea     ecx, [esp+44h+var_2C]
  00B90BC4  call    sub_ABB2F0   ; <<< 初始化 {cur,end}（游标自 buf+2 起）
  00B90BC9  mov     word ptr [edi], 0DFB2h   ; <<< 内联写线（u16）
  00B90BCE  mov     ebp, [esi+7C18h]
  00B90BD4  test    ebp, ebp
  00B90BD6  mov     [esp+40h+var_4], 0
  00B90BDE  lea     ebx, [edi+2]
  00B90BE1  jz      loc_B90C72
  00B90BE7  lea     ecx, [esp+40h+var_28]
  00B90BEB  push    ecx
  00B90BEC  call    sub_CA0CE0
  00B90BF1  add     esp, 4
  00B90BF4  mov     edx, [esi+8]
  00B90BF7  push    offset aProtoLoungeCli_512
  00B90BFC  push    edx
  00B90BFD  push    offset aId
  00B90C02  push    eax
  00B90C03  push    ebp
  00B90C04  mov     byte ptr [esp+54h+var_4], 1
  00B90C09  call    sub_B03020
  00B90C0E  add     esp, 8
  00B90C11  push    eax
  00B90C12  call    sub_41D990
  00B90C17  add     esp, 8
  00B90C1A  mov     ecx, eax
  00B90C1C  call    sub_ADC810
  00B90C21  push    eax
  00B90C22  call    sub_41D990
  00B90C27  add     esp, 8
  00B90C2A  lea     ecx, [esp+40h+var_28]
  00B90C2E  mov     byte ptr [esp+40h+var_4], 0
  00B90C33  call    sub_B02FF0   ; <<< 提交（C→S 闭合点）
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00B90C33  call    sub_B02FF0
  00B90C38  push    offset aByte
  00B90C3D  mov     eax, ebx
  00B90C3F  sub     eax, edi
  00B90C41  push    eax
  00B90C42  push    offset asc_EDAD58
  00B90C47  push    ebp
  00B90C48  call    sub_41D990
  00B90C4D  add     esp, 8
  00B90C50  mov     ecx, eax
  00B90C52  call    sub_B03580
  00B90C57  push    eax
  00B90C58  call    sub_41D990
  00B90C5D  add     esp, 8
  00B90C60  mov     ebp, eax
  00B90C62  push    0Ah
  00B90C64  mov     ecx, ebp
  00B90C66  call    sub_B036E0
  00B90C6B  mov     ecx, ebp
  00B90C6D  call    sub_40DDF0
  00B90C72  mov     edx, [esi]
  00B90C74  mov     eax, [edx+58h]
```

## 4. 发送去向切片

```asm
  00B90C72  mov     edx, [esi]
  00B90C74  mov     eax, [edx+58h]
  00B90C77  sub     ebx, edi
  00B90C79  push    ebx
  00B90C7A  push    edi
  00B90C7B  mov     ecx, esi
  00B90C7D  call    eax
  00B90C7F  test    al, al
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `00B90BC9` | u16 / 2 |
