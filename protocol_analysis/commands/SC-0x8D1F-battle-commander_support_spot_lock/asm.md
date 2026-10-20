# 汇编证据 —— SC-0x8D1F-battle-commander_support_spot_lock

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x2` @ `B236AA`）

```asm
; VA: B236AA（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
B236AA  push    0x2          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— index：偏移 0，长度 1，线类型 u8（点位序号（日志串 `index=`））
B236E5  call    sub_B06230     ; 读取 u8
; 块内日志格式串 @B237D2 → 含义锚点

; 字段 2 —— is_lock：偏移 1，长度 1，线类型 u8（是否锁定（日志串 `is_lock=`））
B23725  call    sub_B06230     ; 读取 u8
; 块内日志格式串 @B237F7 → 含义锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B23735
B23735  cmp     cursor, end      ; 不等则走 vt[0x64] 报错
; 收尾：push <模块id>; call sub_B05D90
```

## E4 去向（用途锚点）

```asm
; VA: B2384E —— `vt[0x2B0]`（2 实参）
B2384E  mov     <reg>, [obj]
;       mov     <reg>, [<reg>+0x2B0h]
;       call    <reg>
```
