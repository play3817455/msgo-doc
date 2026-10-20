# 汇编证据 —— SC-0x88A8-lounge-storage_item_extend_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x8` @ `B6ACC5`）

```asm
; VA: B6ACC5（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
B6ACC5  push    0x8          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码（日志串 `result=`））
B6AD00  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B6ADEF → 含义锚点

; 字段 2 —— slot_num：偏移 4，长度 4，线类型 u32（扩容后槽位数（日志串 `slot_num=`））
B6AD40  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B6AE14 → 含义锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B6AD50
B6AD50  cmp     cursor, end      ; 不等则走 vt[0x64] 报错
; 收尾：push <模块id>; call sub_B41110
```

## E4 去向（用途锚点）

```asm
; VA: B6AE68 —— `vt[0x4BC]`（2 实参）
B6AE68  mov     <reg>, [obj]
;       mov     <reg>, [<reg>+0x4BCh]
;       call    <reg>
```
