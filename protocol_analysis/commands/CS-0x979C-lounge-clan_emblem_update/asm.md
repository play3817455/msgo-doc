# 汇编证据 —— CS-0x979C-lounge-clan_emblem_update

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_BA06E0 @ `0xBA06E0`（`0xBA06E0`..`0xBA0920`）
- 命令名字符串：`)<-_proto_lounge_client::send_clan_emblem_update(` @ `0xEEC908`
- opcode 写入：`0xBA075C`
- 声明容量：`0x000E`（分配器容量 `push` @ `0xBA0726`）
- 发送去向：`vt[0x58]` @ `0xBA08AC`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00ba0726  push    0Eh
  00ba075c  mov     word ptr [ebp+0], 979Ch   ; 字段 0 `opcode` => 2
  00ba076c  mov     [eax], dl   ; 字段 1 `emb_base` => 1
  00ba078b  mov     [esi], cl   ; 字段 2 `emb_parts1` => 1
  00ba078d  call    sub_B061C0   ; 字段 3 `emb_parts2` => 1
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00EE3378  push offset a<name>; "emb_base="
  00EE336C  push offset a<name>; "emb_parts1="
  00EE3360  push offset a<name>; "emb_parts2="
```

## 4. 发送去向切片

```asm
  00ba08ac  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xBA075C` | u16 / 2 |
| `emb_base` | `0xBA076C` | u8 / 1 |
| `emb_parts1` | `0xBA078B` | u8 / 1 |
| `emb_parts2` | `0xBA078D` | u8 / 1 |
