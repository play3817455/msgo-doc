# 汇编证据 —— SC-0x7DA2-lounge-dailycup_booking_update

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x4` @ `B68EA2`）

```asm
; VA: B68EA2（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
B68EA2  push    0x4          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— fixed_team_num：偏移 0，长度 4，线类型 u32（已确定队伍数（日志串 `fixed_team_num=`））
B68EDD  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B68F87 → 含义锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B68F09
B68F09  cmp     cursor, end      ; 不等则走 vt[0x64] 报错
; 收尾：push <模块id>; call sub_B41110
```

## E4 去向（用途锚点）

```asm
; VA: B68FD7 —— `vt[0x554]`（1 实参）
B68FD7  mov     <reg>, [obj]
;       mov     <reg>, [<reg>+0x554h]
;       call    <reg>
```
