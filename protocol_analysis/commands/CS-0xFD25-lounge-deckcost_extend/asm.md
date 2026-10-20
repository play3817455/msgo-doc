# 汇编证据 —— CS-0xFD25-lounge-deckcost_extend

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0x00BA4460`（`0x00BA4460`..`0x00BA4646`），函数 `sub_BA4460`
- 命令名字符串：`)<-_proto_lounge_client::send_deckcost_extend( ` @ `0x00EECF40`
- opcode 写入：`0x00BA44D4`
- 声明容量：`0xA`（分配器容量 `push` @ `0x00BA44A6`）
- 提交（`sub_B02FF0`）：`0x00BA4551`
- 发送去向：`vt[0x58]` @ `0x00BA45D4`

## 2. 组包块切片

```asm
  00BA44A3  mov     edx, [eax+78h]
  00BA44A6  push    0Ah                      ; <<< 容量 0xA = 10
  00BA44A8  call    edx
  00BA44B4  call    sub_ABB2F0               ; <<< 初始化 {cur,end}
  00BA44D4  mov     word ptr [ebp+0], 0FD25h ; <<< opcode
  00BA44E9  mov     [eax], esi               ; <<< u32 (arg_0)
  00BA44F5  mov     [edx], ecx               ; <<< u32 (arg_4)
  00BA4551  call    sub_B02FF0               ; <<< 提交
```

## 3. 提交后的 trace 打印块

```asm
  00BA4560  push    offset aUseBc              ; "use_bc="   → sub_B03580(u32)
  00BA4583  push    offset aTokenId            ; "token_id=" → sub_B03580(u32)
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | ``00BA44D4`` | u16 / 2 |
| `use_bc` | ``0xBA44E9`` | u32 / 4 |
| `token_id` | ``0xBA44F5`` | u32 / 4 |
