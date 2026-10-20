# 汇编证据 —— CS-0xFBC1-battle-weapon_fire__funnel

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0x00B3A860`（`0x00B3A860`..`0x00B3AB26`），函数 `sub_B3A860`
- 命令名字符串：`)<-_proto_battle_client::send_weapon_fire__funnel( ` @ `0x00EE1014`
- opcode 写入：`0x00B3A8E0`
- 声明容量：`0x56`（分配器容量 `push` @ `0x00B3A8A6`）
- 提交（`sub_B02FF0`）：`0x00B3A9BB`
- 发送去向：`vt[0x58]` @ `0x00B3AAB4`

## 2. 组包块切片

```asm
  00B3A8A3  mov     edx, [eax+78h]
  00B3A8A6  push    56h ; 'V'                ; <<< 容量 0x56 = 86
  00B3A8A8  call    edx
  00B3A8B8  call    sub_ABB2F0               ; <<< 初始化 {cur,end}
  00B3A8E0  mov     word ptr [edi], 0FBC1h   ; <<< opcode
  00B3A8EF  mov     [ecx], esi               ; <<< u32 (arg_0)
  00B3A907  mov     [edx], cl                ; <<< u8  (arg_4)
  00B3A91D  call    sub_B02D80               ; <<< u32 计数 (arg_C)
  00B3A92F  test    ebp, ebp                 ; 循环 fire_points_num 次
  00B3A945  call    sub_B06580               ; <<< 元素写原语（3×u16 = 6B）
  00B3A955  add     [esp+4Ch+arg_C], 6       ; <<< 元素步进 = 6
  00B3A9BB  call    sub_B02FF0               ; <<< 提交
```

## 3. 元素写原语 `sub_B06580`（3×u16 ⇒ 6B）

```asm
  00B06593  mov     si, [ecx]
  00B06596  mov     [edx], si                ; x (u16, 游标 +2)
  00B065AA  mov     [edx], si                ; y (u16, 游标 +2)
  00B065BE  mov     [edx], cx                ; z (u16, 游标 +2)
```

## 4. 提交后的 trace 打印块

```asm
  00B3A9CA  push    offset aFromEntId          ; "from_ent_id=" → sub_B03580(u32)
  00B3A9F2  push    offset aWslotIdx           ; "wslot_idx="   → sub_B0C1F0(1B)
  00B3AA0F  push    offset aFirePoints         ; "fire_points={"
  00B3AA27  call    sub_B0A5D0                 ; 元素打印器：x= / y= / z=（均 u16）
  00B3AA64  push    offset unk_EDABE4          ; "}"
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | ``00B3A8E0`` | u16 / 2 |
| `from_ent_id` | ``0xB3A8EF`` | u32 / 4 |
| `wslot_idx` | ``0xB3A907`` | u8 / 1 |
| `fire_points_num` | ``0xB3A91D`,`0xB3A900`` | u32 / 4 |
| `fire_points` | ``0xB3A945`,`0xB3A955`` | array<fire_point,12> / 6×N |
