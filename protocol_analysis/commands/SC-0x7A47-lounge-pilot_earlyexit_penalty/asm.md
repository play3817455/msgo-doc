# 汇编证据 —— SC-0x7A47-lounge-pilot_earlyexit_penalty

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x4` @ `B682AE`）

```asm
; VA: B682AE（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
B682AE  push    0x4          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— penalty_sec：偏移 0，长度 4，线类型 u32（提前退出惩罚秒数（日志串 `penalty_sec=`））
B682E9  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B6838D → 含义锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B68312
B68312  cmp     cursor, end      ; 不等则走 vt[0x64] 报错
; 收尾：push <模块id>; call sub_B41110
```

## E4 去向（用途锚点）

```asm
; VA: B683DD —— `vt[0xD8]`（1 实参）
B683DD  mov     <reg>, [obj]
;       mov     <reg>, [<reg>+0xD8h]
;       call    <reg>
```
