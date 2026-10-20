# 汇编证据 —— CS-0xF86A-lounge-datafile_download

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0x00B89BE0`（`0x00B89BE0`..`0x00B89DF6`），函数 `sub_B89BE0`
- 命令名字符串：`)<-_proto_lounge_client::send_datafile_download( ` @ `0x00EEA2A4`
- opcode 写入：`0x00B89C69`
- 声明容量：`0x106`（分配器容量 `push` @ `0x00B89C23`）
- 提交（`sub_B02FF0`）：`0x00B89CF4`
- 发送去向：`vt[0x58]` @ `0x00B89D87`

## 2. 组包块切片

```asm
  00B89C20  mov     edx, [eax+78h]
  00B89C23  push    106h                     ; <<< 容量 0x106 = 262
  00B89C28  call    edx
  00B89C34  call    sub_ABB2F0               ; <<< 初始化 {cur,end}
  00B89C5E  push    100h                     ; <<< 串槽预算 256
  00B89C69  mov     word ptr [ebp+0], 0F86Ah ; <<< opcode
  00B89C73  call    sub_B02B40               ; <<< 写 NUL 串（arg_0）
  00B89C98  mov     [eax], ecx               ; <<< u32 (arg_4)
  00B89CF4  call    sub_B02FF0               ; <<< 提交
```

## 3. 提交后的 trace 打印块

```asm
  00B89D08  push    offset aFilepath          ; "filepath=\"" → 串打印
  00B89D36  push    offset aHashval           ; "hashval="     → sub_B03580(u32)
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | ``00B89C69`` | u16 / 2 |
| `filepath` | ``0xB89C5E`,`0xB89C73`` | bytes / var |
| `hashval` | ``0xB89C98`` | u32 / 4 |
