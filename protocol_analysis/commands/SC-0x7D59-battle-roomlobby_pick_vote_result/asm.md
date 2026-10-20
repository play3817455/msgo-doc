# 汇编证据 —— SC-0x7D59-battle-roomlobby_pick_vote_result

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x30` @ `B210CE`）

```asm
; VA: B210CE（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
B210CE  push    0x30          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— state：偏移 0，长度 4，线类型 u32（房间状态（日志串 `state=`））
B21109  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B21273 → 含义锚点

; 字段 2 —— vote_count：偏移 4，长度 20，线类型 u32[5]（投票计数（固定 5 元素逐席位；日志串 `vote_count={`））
B21148  call    sub_B02DD0 ×5     ; 读取 u32[5]
; 块内日志格式串 @B2128E → 含义锚点

; 字段 3 —— pick_msma_id：偏移 24，长度 20，线类型 u32[5]（被选机体 ID（固定 5 元素；日志串 `pick_msma_id={`））
B21188  call    sub_B02DD0 ×5     ; 读取 u32[5]
; 块内日志格式串 @B212EE → 含义锚点

; 字段 4 —— member_count：偏移 44，长度 4，线类型 u32（成员数（日志串 `member_count=`））
B211C6  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B21358 → 含义锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B211DA
B211DA  cmp     cursor, end      ; 不等则走 vt[0x64] 报错
; 收尾：push <模块id>; call sub_B05D90
```

## E4 去向（用途锚点）

```asm
; VA: B213B0 —— `vt[0xC4]`（4 实参）
B213B0  mov     <reg>, [obj]
;       mov     <reg>, [<reg>+0xC4h]
;       call    <reg>
```

## E5 复合读取器 / 预留原语（本命令专用取证）

```asm
; sub_B41740（u32 阵列预留，槽步进 0x14=20）：@0xB21137、@0xB21177
; 循环上界字面量 5：cmp edi,5 @0xB2115A、@0xB2119A；元素读取 call sub_B02DD0 @0xB21148、@0xB21188
```
