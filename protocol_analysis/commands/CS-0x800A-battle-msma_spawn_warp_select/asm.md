# 汇编证据 —— CS-0x800A-battle-msma_spawn_warp_select

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B343F0 @ `0xb343f0`（`0xb343f0`..`0xb3466b`）
- 命令名字符串：`)<-_proto_battle_client::send_msma_spawn_warp_select(` @ `0xee0a2c`
- opcode 写入：`0xb3446c`
- 声明容量：`0x12`（分配器容量 `push` @ `0xb34436`）

## 2. 组包块切片（游标初始化 → 逐字段写线 → 提交）

```asm
  0xb3443a  mov     ebp, eax
  0xb3443c  mov     eax, [edi+0Ch]
  0xb3443f  push    eax
  0xb34440  lea     ecx, [esp+4Ch+var_34]
  0xb34444  call    sub_ABB2F0
  0xb34449  lea     ecx, [ebp+12h]
  0xb3444c  lea     eax, [ebp+2]
  0xb3444f  cmp     eax, ecx
  0xb34451  mov     [esp+48h+var_4], 0
  0xb34459  mov     [esp+48h+var_30], ebp
  0xb3445d  mov     dword ptr [esp+48h+var_2C], ecx
  0xb34461  ja      loc_B34656
  0xb34467  lea     edx, [eax+4]
  0xb3446a  cmp     edx, ecx
  0xb3446c  mov     word ptr [ebp+0], 800Ah
  0xb34472  ja      loc_B34656
  0xb34478  mov     esi, [esp+48h+arg_0]
  0xb3447c  mov     [eax], esi
  0xb3447e  mov     eax, edx
  0xb34480  lea     edx, [eax+4]
  0xb34483  cmp     edx, ecx
  0xb34485  ja      loc_B34656
  0xb3448b  mov     ecx, [esp+48h+arg_4]
  0xb3448f  mov     [esp+48h+var_30], edx
  0xb34493  lea     edx, [esp+48h+var_30]
  0xb34497  mov     [eax], ecx
  0xb34499  push    edx
  0xb3449a  lea     eax, [esp+4Ch+arg_8]
  0xb3449e  push    eax
  0xb3449f  call    sub_B061C0
  0xb344a4  add     esp, 8
  0xb344a7  test    al, al
  0xb344a9  jz      loc_B34656
  0xb344af  lea     ecx, [esp+48h+var_30]
  0xb344b3  push    ecx
  0xb344b4  lea     edx, [esp+4Ch+arg_C]
  0xb344b8  push    edx
  0xb344b9  call    sub_B02DA0
  0xb344be  add     esp, 8
  0xb344c1  test    al, al
  0xb344c3  jz      loc_B34656
  0xb344c9  mov     esi, [edi+3D40h]
  0xb344cf  test    esi, esi
  0xb344d1  mov     ebx, [esp+48h+var_30]
  0xb344d5  jz      loc_B345FA
  0xb344db  lea     eax, [esp+48h+var_28]
  0xb344df  push    eax
  0xb344e0  call    sub_CA0CE0
  0xb344e5  add     esp, 4
  0xb344e8  mov     ecx, [edi+8]
  0xb344eb  push    offset aProtoBattleCli_216; ")<-_proto_battle_client::send_msma_spaw"...
  0xb344f0  push    ecx
  0xb344f1  push    offset aId; " (id:"
  0xb344f6  push    eax
  0xb344f7  push    esi
  0xb344f8  mov     byte ptr [esp+5Ch+var_4], 1
  0xb344fd  call    sub_B03020
  0xb34502  add     esp, 8
  0xb34505  push    eax
  0xb34506  call    sub_41D990
  0xb3450b  add     esp, 8
  0xb3450e  mov     ecx, eax
  0xb34510  call    sub_ADC810
  0xb34515  push    eax
  0xb34516  call    sub_41D990
  0xb3451b  add     esp, 8
  0xb3451e  lea     ecx, [esp+48h+var_28]
  0xb34522  mov     byte ptr [esp+48h+var_4], 0
  0xb34527  call    sub_B02FF0
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。
> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B02B40`=写 NUL 串（其**紧邻之前的 `push N`** = 串槽预算）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb34536  push    offset aPostIndex_0; "post_index="
  0xb3455e  push    offset aSptSpotIndex; "spt_spot_index="
  0xb34586  push    offset aIsBtlshipRide; "is_btlship_ride="
  0xb345ab  push    offset aRespawnEntId; "respawn_ent_id="
  0xb345c0  push    offset aByte; "]byte"
  0xb345ca  push    offset asc_EDAD58; " ) ["
```

## 4. 发送去向切片

```asm
  0xb345fc  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xb3446c` | u16 |
| `post_index` | `0xB3447C` | u32 |
| `spt_spot_index` | `0xB34497` | u32 |
| `is_btlship_ride` | `0xB3449F` | u8 |
| `respawn_ent_id` | `0xB344B9` | u16 |
