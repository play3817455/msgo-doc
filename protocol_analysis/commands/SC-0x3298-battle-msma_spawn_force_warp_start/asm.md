# 汇编证据 —— SC-0x3298-battle-msma_spawn_force_warp_start

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x6` @ `0xB135B8`）

```asm
; VA: 0xB135B8（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB135B8  push    0x6          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— ent_id：偏移 0，长度 2，线类型 u16（实体 ID）
0xB135F3  call    sub_B02DF0     ; 读 u16
; 块内日志格式串 "ent_id=" → 含义锚点：0xB136DA

; 字段 2 —— countdown_msec：偏移 2，长度 4，线类型 u32（倒计时（毫秒））
0xB13630  call    sub_B02DD0     ; 读 u32
; 块内日志格式串 "countdown_msec=" → 含义锚点：0xB136FF

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB13661
0xB13661  push    <模块/错误码>
0xB13661  call    sub_B05D90     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB13760
0xB13760  mov     edx, [obj]
;       mov     edx, [edx+0x148h]
;       call    edx          ; vt[0x148]（2 实参）
```
