# 汇编证据 —— CS-0xFFC6-lounge-chargepoint_charge_url_get

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0x00B8CB10`（`0x00B8CB10`..`0x00B8CC93`），函数 `sub_B8CB10`
- 命令名字符串：`)<-_proto_lounge_client::send_chargepoint_charge_url_get( ` @ `0x00EEA7F8`
- opcode 写入：`0x00B8CB69`
- 声明容量：`0x2`（分配器容量 `push` @ `0x00B8CB56`）
- 提交（`sub_B02FF0`）：`0x00B8CBD3`
- 发送去向：`vt[0x58]` @ `0x00B8CC14`

## 2. 组包块切片（零负载：容量 2，仅写 opcode）

```asm
  00B8CB53  mov     edx, [eax+78h]
  00B8CB56  push    2                        ; <<< 容量 2
  00B8CB58  call    edx
  00B8CB64  call    sub_ABB2F0               ; <<< 初始化 {cur,end}
  00B8CB69  mov     word ptr [edi], 0FFC6h   ; <<< opcode（唯一写线）
  00B8CB7E  lea     ebx, [edi+2]             ; 负载结束游标 = buf+2
  00B8CBD3  call    sub_B02FF0               ; <<< 提交
```

## 3. 发送去向切片（长度 = 游标 − 缓冲首址 = 2）

```asm
  00B8CC12  mov     edx, [esi]
  00B8CC14  mov     eax, [edx+58h]
  00B8CC17  sub     ebx, edi                 ; 长度 = 2 − 0 = 2
  00B8CC19  push    ebx
  00B8CC1A  push    edi
  00B8CC1B  mov     ecx, esi
  00B8CC1D  call    eax
  00B8CC1F  test    al, al
  00B8CC21  jnz     short loc_B8CC4A         ; <<< 成功走跳转（本例成功分支在 jnz 目标处）
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | ``00B8CB69`` | u16 / 2 |
