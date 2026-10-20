# 汇编证据 —— CS-0xFC2B-lounge-player_navi_unlock

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0x00BA73D0`（`0x00BA73D0`..`0x00BA75B6`），函数 `sub_BA73D0`
- 命令名字符串：`)<-_proto_lounge_client::send_player_navi_unlock( ` @ `0x00EED460`
- opcode 写入：`0x00BA7444`
- 声明容量：`0xA`（分配器容量 `push` @ `0x00BA7416`）
- 提交（`sub_B02FF0`）：`0x00BA74C1`
- 发送去向：`vt[0x58]` @ `0x00BA7544`

## 2. 组包块切片

```asm
  00BA7413  mov     edx, [eax+78h]
  00BA7416  push    0Ah                      ; <<< 容量 0xA = 10
  00BA7418  call    edx
  00BA7424  call    sub_ABB2F0               ; <<< 初始化 {cur,end}
  00BA7444  mov     word ptr [ebp+0], 0FC2Bh ; <<< opcode
  00BA7459  mov     [eax], esi               ; <<< u32 (arg_0)
  00BA7465  mov     [edx], ecx               ; <<< u32 (arg_4)
  00BA74C1  call    sub_B02FF0               ; <<< 提交
```

## 3. 提交后的 trace 打印块

```asm
  00BA74D0  push    offset aNaviId             ; "navi_id="  → sub_B03580(u32)
  00BA74F3  push    offset aUnlockby           ; "unlockBy=" → sub_B03580(u32)
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | ``00BA7444`` | u16 / 2 |
| `navi_id` | ``0xBA7459`` | u32 / 4 |
| `unlockBy` | ``0xBA7465`` | u32 / 4 |
