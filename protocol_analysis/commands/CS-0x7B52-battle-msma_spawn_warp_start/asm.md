# 汇编证据 —— CS-0x7B52-battle-msma_spawn_warp_start

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B34240 @ `0xb34240`（`0xb34240`..`0xb343ea`）
- 命令名字符串：`)<-_proto_battle_client::send_msma_spawn_warp_start(` @ `0xee09f4`
- opcode 写入：`0xb342b4`
- 声明容量：`0x6`（分配器容量 `push` @ `0xb34286`）

## 2. 组包块切片（游标初始化 → 逐字段写线 → 提交）

```asm
  0xb3428a  mov     ebp, eax
  0xb3428c  mov     eax, [esi+0Ch]
  0xb3428f  push    eax
  0xb34290  lea     ecx, [esp+44h+var_2C]
  0xb34294  call    sub_ABB2F0
  0xb34299  lea     ecx, [ebp+6]
  0xb3429c  lea     eax, [ebp+2]
  0xb3429f  cmp     eax, ecx
  0xb342a1  mov     [esp+40h+var_4], 0
  0xb342a9  ja      loc_B343D5
  0xb342af  lea     ebx, [eax+4]
  0xb342b2  cmp     ebx, ecx
  0xb342b4  mov     word ptr [ebp+0], 7B52h
  0xb342ba  ja      loc_B343D5
  0xb342c0  mov     ecx, [esp+40h+arg_0]
  0xb342c4  mov     [eax], ecx
  0xb342c6  mov     edi, [esi+3D30h]
  0xb342cc  test    edi, edi
  0xb342ce  jz      loc_B34379
  0xb342d4  lea     edx, [esp+40h+var_28]
  0xb342d8  push    edx
  0xb342d9  call    sub_CA0CE0
  0xb342de  add     esp, 4
  0xb342e1  mov     ecx, [esi+8]
  0xb342e4  push    offset aProtoBattleCli_221; ")<-_proto_battle_client::send_msma_spaw"...
  0xb342e9  push    ecx
  0xb342ea  push    offset aId; " (id:"
  0xb342ef  push    eax
  0xb342f0  push    edi
  0xb342f1  mov     byte ptr [esp+54h+var_4], 1
  0xb342f6  call    sub_B03020
  0xb342fb  add     esp, 8
  0xb342fe  push    eax
  0xb342ff  call    sub_41D990
  0xb34304  add     esp, 8
  0xb34307  mov     ecx, eax
  0xb34309  call    sub_ADC810
  0xb3430e  push    eax
  0xb3430f  call    sub_41D990
  0xb34314  add     esp, 8
  0xb34317  lea     ecx, [esp+40h+var_28]
  0xb3431b  mov     byte ptr [esp+40h+var_4], 0
  0xb34320  call    sub_B02FF0
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。
> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B02B40`=写 NUL 串（其**紧邻之前的 `push N`** = 串槽预算）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb3432a  push    offset aIsCancel; "is_cancel="
  0xb3433f  push    offset aByte; "]byte"
  0xb34349  push    offset asc_EDAD58; " ) ["
```

## 4. 发送去向切片

```asm
  0xb3437b  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xb342b4` | u16 |
| `is_cancel` | `0xB342C4` | u32 |
