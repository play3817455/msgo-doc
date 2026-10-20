# 汇编证据 —— CS-0xFBAC-lounge-pilot_rental_module_unlock

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0x00B8C420`（`0x00B8C420`..`0x00B8C603`），函数 `sub_B8C420`
- 命令名字符串：`)<-_proto_lounge_client::send_pilot_rental_module_unlock( ` @ `0x00EEA710`
- opcode 写入：`0x00B8C494`
- 声明容量：`0xA`（分配器容量 `push` @ `0x00B8C466`）
- 提交（`sub_B02FF0`）：`0x00B8C511`
- 发送去向：`vt[0x58]` @ `0x00B8C594`

## 2. 组包块切片

```asm
  00B8C463  mov     edx, [eax+78h]
  00B8C466  push    0Ah                      ; <<< 容量 0xA = 10
  00B8C468  call    edx
  00B8C474  call    sub_ABB2F0               ; <<< 初始化 {cur,end}
  00B8C494  mov     word ptr [ebp+0], 0FBACh ; <<< opcode
  00B8C4A9  mov     [eax], esi               ; <<< u32 (arg_0)
  00B8C4B5  mov     [edx], ecx               ; <<< u32 (arg_4)
  00B8C511  call    sub_B02FF0               ; <<< 提交
```

## 3. 提交后的 trace 打印块

```asm
  00B8C520  push    offset aModuleId           ; "module_id=" → sub_B03580(u32)
  00B8C543  push    offset aCount              ; "count="     → sub_B03580(u32)
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | ``00B8C494`` | u16 / 2 |
| `module_id` | ``0xB8C4A9`` | u32 / 4 |
| `count` | ``0xB8C4B5`` | u32 / 4 |
