# 汇编证据 —— CS-0xFF32-lounge-gacha_lineup

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0x00B9DCA0`（`0x00B9DCA0`..`0x00B9DE4D`），函数 `sub_B9DCA0`
- 命令名字符串：`)<-_proto_lounge_client::send_gacha_lineup( ` @ `0x00EEC494`
- opcode 写入：`0x00B9DD14`
- 声明容量：`0x6`（分配器容量 `push` @ `0x00B9DCE6`）
- 提交（`sub_B02FF0`）：`0x00B9DD80`
- 发送去向：`vt[0x58]` @ `0x00B9DDDB`

## 2. 组包块切片

```asm
  00B9DCE3  mov     edx, [eax+78h]
  00B9DCE6  push    6                        ; <<< 容量 6
  00B9DCE8  call    edx
  00B9DCF4  call    sub_ABB2F0               ; <<< 初始化 {cur,end}
  00B9DD14  mov     word ptr [ebp+0], 0FF32h ; <<< opcode
  00B9DD24  mov     [eax], ecx               ; <<< u32 (arg_0)
  00B9DD80  call    sub_B02FF0               ; <<< 提交
```

## 3. 提交后的 trace 打印块

```asm
  00B9DD8A  push    offset aGachaType          ; "gacha_type=" → sub_B03580(u32)
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | ``00B9DD14`` | u16 / 2 |
| `gacha_type` | ``0xB9DD24`` | u32 / 4 |
