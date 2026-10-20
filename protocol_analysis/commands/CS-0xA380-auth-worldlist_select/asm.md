# 汇编证据 —— CS-0xA380-auth-worldlist_select

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B05A30 @ `0xB05A30`（`0xB05A30`..`0xB05C10`）
- 命令名字符串：`)<-_proto_auth_client::send_worldlist_select(` @ `0xEDB0EC`
- opcode 写入：`0xB05AA1`
- 声明容量：`0x000A`（分配器容量 `push` @ `0xB05A73`）
- 发送去向：`vt[0x58]` @ `0xB05BA1`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00b05a73  push    0Ah
  00b05aa1  mov     word ptr [ebp+0], 0A380h   ; 字段 0 `opcode` => 2
  00b05ab6  mov     [eax], esi   ; 字段 1 `world_id` => 4
  00b05ac2  mov     [edx], ecx   ; 字段 2 `channeling_type` => 4
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00EDACD4  push offset a<name>; "world_id="
  00EDACC0  push offset a<name>; "channeling_type="
```

## 4. 发送去向切片

```asm
  00b05ba1  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB05AA1` | u16 / 2 |
| `world_id` | `0xB05AB6` | u32 / 4 |
| `channeling_type` | `0xB05AC2` | u32 / 4 |
