# 汇编证据 —— SC-0x8CB2-lounge-item_del

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x8` @ `B6BB6E`）

```asm
; VA: B6BB6E（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
B6BB6E  push    0x8          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— uniqid：偏移 0，长度 8，线类型 u64（道具唯一 ID（日志串 `uniqid=`））
B6BBA9  call    sub_B06200     ; 读取 u64
; 块内日志格式串 @B6BC6F → 含义锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B6BBD5
B6BBD5  cmp     cursor, end      ; 不等则走 vt[0x64] 报错
; 收尾：push <模块id>; call sub_B41110
```

## E4 去向（用途锚点）

```asm
; VA: B6BCC2 —— `vt[0x338]`（2 实参）
B6BCC2  mov     <reg>, [obj]
;       mov     <reg>, [<reg>+0x338h]
;       call    <reg>
```
