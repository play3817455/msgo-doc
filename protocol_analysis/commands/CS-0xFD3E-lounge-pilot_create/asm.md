# 汇编证据 —— CS-0xFD3E-lounge-pilot_create

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0x00B8A100`（`0x00B8A100`..`0x00B8A303`），函数 `sub_B8A100`
- 命令名字符串：`)<-_proto_lounge_client::send_pilot_create( ` @ `0x00EEA340`
- opcode 写入：`0x00B8A184`
- 声明容量：`0xA6`（分配器容量 `push` @ `0x00B8A143`）
- 提交（`sub_B02FF0`）：`0x00B8A20F`
- 发送去向：`vt[0x58]` @ `0x00B8A294`

## 2. 组包块切片

```asm
  00B8A140  mov     edx, [eax+78h]
  00B8A143  push    0A6h                     ; <<< 容量 0xA6 = 166
  00B8A148  call    edx
  00B8A154  call    sub_ABB2F0               ; <<< 初始化 {cur,end}
  00B8A184  mov     word ptr [ebp+0], 0FD3Eh ; <<< opcode
  00B8A18E  call    sub_B06360               ; <<< 复合写入器：pilot（159B）
  00B8A1B3  mov     [eax], ecx               ; <<< u32 slot (arg_4)
  00B8A20F  call    sub_B02FF0               ; <<< 提交
```

## 3. 复合写入器 `sub_B06360`（pilot，逐字段累加 = 159B）

```asm
  00B06378  mov     edx, [edi]
  00B0637A  mov     [eax], edx               ; +0    u32 pilot_id
  00B0638F  mov     dl, [eax+edi+4]          ; +4    u8[25] name（循环 0x19 次）
  00B063AE  mov     dl, [edi+1Dh]            ; +1D   u8 troops
  00B063C4  mov     dl, [edi+1Eh]            ; +1E   u8 level
  00B063DA  mov     dl, [edi+1Fh]            ; +1F   u8 mil_class
  00B063F0  mov     dx, [edi+20h]            ; +20   u16 byword
  00B06404  mov     edx, [edi+24h]           ; +24   u32 cmdr_fame
  00B06411  call    sub_B02DA0               ; +28   u16 rate_vslocal
  00B06422  call    sub_B02DA0               ; +2A   u16 rate_vslocal_4ev
  00B06433  call    sub_B02DA0               ; +2C   u16 rate_vslocal_clan
  00B06444  call    sub_B02D80               ; +30   u32 level_point
  00B06455  call    sub_B06290               ; +34   avatar（18B）
  00B06466  call    sub_B02D80               ; +4C   u32 clan_id
  00B06486  call    sub_B061C0               ; +50   u8[31] clan_name（循环 0x1F 次）
  00B064A3  call    sub_B061C0               ; +6F   u8 clan_emb_base
  00B064B8  call    sub_B061C0               ; +70   u8 clan_emb_parts1
  00B064CD  call    sub_B061C0               ; +71   u8 clan_emb_parts2
  00B064E2  call    sub_B02D80               ; +74   u32 cupteam_id
  00B064F6  call    sub_B061C0               ; +78   u8[31] cupteam_name（循环 0x1F 次）
  00B06512  call    sub_B02D80               ; +98   u32 accum_point
  00B06526  call    sub_B02D80               ; +9C   u32 rank
  00B0653A  call    sub_B02D80               ; +A0   u32 base_accump
  00B0654E  call    sub_B02D80               ; +A4   u32 req_accump
  00B06568  call    sub_B02D80               ; +A8   u32 penalty
```

## 4. 提交后的 trace 打印块 / 结构体打印器成员名

```asm
  00B8A21E  push    offset aPilot              ; "pilot=" → sub_B08AD0（结构体打印器）
  00B8A243  push    offset aSlot               ; "slot="  → sub_B03580(u32)
  00B08AF0  push    offset aPilotId            ; 打印器成员：pilot_id=  @[edi+0]
  00B08B17  push    offset aName               ; name=      @[edi+4]
  00B08B41  push    offset aTroops             ; troops=    @[edi+1Dh]（movsx）
  00B08B69  push    offset aLevel              ; level=     @[edi+1Eh]（movsx）
  00B08B91  push    offset aMilClass           ; mil_class= @[edi+1Fh]（movsx）
  00B08BB9  push    offset aByword             ; byword=    @[edi+20h]（movzx word）
  00B08BE0  push    offset aCmdrFame           ; cmdr_fame= @[edi+24h]
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | ``00B8A184`` | u16 / 2 |
| `pilot` | ``0xB8A18E`` | struct(pilot) / 159 |
| `slot` | ``0xB8A1B3`` | u32 / 4 |
