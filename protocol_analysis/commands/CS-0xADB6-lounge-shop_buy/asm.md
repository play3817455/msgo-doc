# 汇编证据 —— CS-0xADB6-lounge-shop_buy

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B9CD70 @ `0xB9CD70`（`0xB9CD70`..`0xB9D179`）
- 命令名字符串：`)<-_proto_lounge_client::send_shop_buy(` @ `0xEEC350`
- opcode 写入：`0xB9CDF2`
- 声明容量：`0x0382`（分配器容量 `push` @ `0xB9CDB6`）
- 发送去向：`vt[0x58]` @ `0xB9D107`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00b9cdb6  push    382h
  00b9cdf2  mov     word ptr [ebp+0], 0ADB6h   ; 字段 0 `opcode` => 2
  00b9ce02  mov     [ecx], esi   ; 字段 1 `shopitemid` => 4
  00b9ce1b  mov     [edx], al   ; 字段 2 `id_type` => 1
  00b9ce23  call    sub_B02D80   ; 字段 3 `num` => 4
  00b9ce3d  call    sub_B061C0   ; 字段 4 `tab_type` => 1
  00b9ce57  call    sub_B061C0   ; 字段 5 `is_cp` => 1
  00b9ce71  call    sub_B02D80   ; 字段 6 `total_price` => 4
  00b9ce8d  call    sub_B02B40   ; 字段 7 `gift_pilot_name` => var(≤25)
  00b9cea9  call    sub_B02B40   ; 字段 8 `subject` => var(≤73)
  00b9cec8  call    sub_B02B40   ; 字段 9 `body` => var(≤766)
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00EE3FD8  push offset a<name>; "shopitemid="
  00EE316C  push offset a<name>; "id_type="
  00EE1AE8  push offset a<name>; "num="
  00EE3FCC  push offset a<name>; "tab_type="
  00EE3FC4  push offset a<name>; "is_cp="
  00EE3FB4  push offset a<name>; "total_price="
  00EE3C44  push offset a<name>; "gift_pilot_name=""
  00EE41DC  push offset a<name>; "subject=""
  00EE41D4  push offset a<name>; "body=""
```

## 4. 发送去向切片

```asm
  00b9d107  mov     edx, [eax+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB9CDF2` | u16 / 2 |
| `shopitemid` | `0xB9CE02` | u32 / 4 |
| `id_type` | `0xB9CE1B` | u8 / 1 |
| `num` | `0xB9CE23` | u32 / 4 |
| `tab_type` | `0xB9CE3D` | u8 / 1 |
| `is_cp` | `0xB9CE57` | u8 / 1 |
| `total_price` | `0xB9CE71` | u32 / 4 |
| `gift_pilot_name` | `0xB9CE8D` | str / var(≤25) |
| `subject` | `0xB9CEA9` | str / var(≤73) |
| `body` | `0xB9CEC8` | str / var(≤766) |
